"""
Prepara o backup limpo para restauracao no Supabase (normaliza e deduplica).

Nao altera o backup original: gera um `restore_ready.db` ao lado, com:
  - historico_aulas.data_aula convertido de dd/mm/aaaa para ISO (aaaa-mm-dd);
  - linhas sinteticas/corrompidas de attendance removidas (date nao-ISO);
  - duplicatas removidas respeitando as constraints UNIQUE do Supabase
    (historico_aulas, attendance, weekly_schedule).
Gera tambem `prep_report.json` com tudo o que foi ajustado/removido.

Uso:
    python scripts/prepare_restore.py
    python scripts/prepare_restore.py --source data/backup_clean_2026-09-22_0757
"""

import argparse
import glob
import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

ISO_GLOB = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]*"
BR_GLOB = "[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]"

# tabela -> colunas que formam a UNIQUE do Supabase
DEDUPE = {
    "historico_aulas": ["data_aula", "horario", "turma_id", "disciplina_id"],
    "attendance": ["student_name", "class_name", "subject_id", "date"],
    "weekly_schedule": ["class_name", "day_of_week", "time_slot"],
}


def _find_source(explicit):
    if explicit:
        if explicit.endswith(".db"):
            return explicit
        return os.path.join(explicit, "backup_clean.db")
    matches = sorted(glob.glob(os.path.join(project_root, "data", "backup_clean_*", "backup_clean.db")))
    if not matches:
        return None
    return matches[-1]


def _count(conn, sql, params=()):
    return conn.execute(sql, params).fetchone()[0]


def prepare(source, out_path):
    shutil.copy2(source, out_path)
    conn = sqlite3.connect(out_path)
    report = {"generated_at": datetime.now().isoformat(timespec="seconds"), "source": source, "steps": {}}

    # 1. historico_aulas: mantem dd/mm/aaaa (formato do portal/automacao).
    #    O Supabase guarda data_aula como TEXTO, entao nao convertemos para ISO.
    total_hist = _count(conn, "SELECT COUNT(*) FROM historico_aulas")
    br = _count(conn, f"SELECT COUNT(*) FROM historico_aulas WHERE data_aula GLOB '{BR_GLOB}'")
    report["steps"]["historico_aulas_datas_dd_mm_aaaa"] = br
    report["steps"]["historico_aulas_total"] = total_hist

    # 2. attendance: remove linhas com date nao-ISO (dados de teste corrompidos)
    att_total = _count(conn, "SELECT COUNT(*) FROM attendance")
    bad_rows = conn.execute(
        f"SELECT student_name, student_number, date FROM attendance WHERE date NOT GLOB '{ISO_GLOB}'"
    ).fetchall()
    conn.execute(f"DELETE FROM attendance WHERE date NOT GLOB '{ISO_GLOB}'")
    report["steps"]["attendance_removidas_corrompidas"] = len(bad_rows)
    report["steps"]["attendance_amostra_removida"] = [
        {"student_name": r[0], "student_number": r[1], "date": r[2]} for r in bad_rows[:10]
    ]
    report["steps"]["attendance_total_antes"] = att_total

    # 2a. Normaliza attendance.student_number (INTEGER no Supabase).
    #     Valores nao-numericos ou fora do intervalo de int4 viram NULL.
    fixed_sn = 0
    for rid, sn in conn.execute(
        "SELECT rowid, student_number FROM attendance WHERE student_number IS NOT NULL"
    ).fetchall():
        try:
            v = int(str(sn).strip())
            if not (-2147483648 <= v <= 2147483647):
                raise ValueError
        except Exception:
            conn.execute("UPDATE attendance SET student_number=NULL WHERE rowid=?", (rid,))
            fixed_sn += 1
    report["steps"]["attendance_student_number_normalizado"] = fixed_sn

    # 2b. Remove ids nao-numericos (nao cabem no BIGINT do Supabase) e orfaos.
    #     Ex.: aula "Test Import" com id UUID. Sao dados de teste, sem dependentes.
    nonnum = {}
    for table in ["lessons", "quizzes", "quiz_questions", "forum_posts", "user_history",
                  "assessments", "assessment_questions", "student_assessments",
                  "student_assessment_answers", "schedules", "attendance",
                  "weekly_schedule", "historico_aulas", "planejamento", "class_subjects"]:
        try:
            rows = conn.execute(
                f'SELECT id FROM "{table}" WHERE id IS NOT NULL AND CAST(id AS INTEGER) != id'
            ).fetchall()
        except sqlite3.OperationalError:
            continue
        if rows:
            ids = [r[0] for r in rows]
            conn.executemany(f'DELETE FROM "{table}" WHERE id = ?', [(i,) for i in ids])
            nonnum[table] = ids
    # Orfaos remanescentes (dependencias das linhas removidas)
    conn.execute("DELETE FROM quiz_questions WHERE quiz_id NOT IN (SELECT id FROM quizzes)")
    conn.execute("DELETE FROM quizzes WHERE lesson_id IS NOT NULL AND lesson_id NOT IN (SELECT id FROM lessons)")
    conn.execute("DELETE FROM forum_posts WHERE lesson_id IS NOT NULL AND lesson_id NOT IN (SELECT id FROM lessons)")
    report["steps"]["ids_nao_numericos_removidos"] = {k: len(v) for k, v in nonnum.items()}

    # 3. Deduplicacao pelas constraints UNIQUE
    for table, cols in DEDUPE.items():
        before = _count(conn, f'SELECT COUNT(*) FROM "{table}"')
        partition = ", ".join(f'"{c}"' for c in cols)
        sql = f"""
            DELETE FROM "{table}" WHERE rowid NOT IN (
                SELECT rowid FROM (
                    SELECT rowid,
                           ROW_NUMBER() OVER (
                               PARTITION BY {partition}
                               ORDER BY ("id" IS NULL), CAST("id" AS INTEGER) DESC, rowid DESC
                           ) AS rn
                    FROM "{table}"
                ) WHERE rn = 1
            )
        """
        conn.execute(sql)
        after = _count(conn, f'SELECT COUNT(*) FROM "{table}"')
        report["steps"][f"{table}_duplicatas_removidas"] = before - after
        report["steps"][f"{table}_total"] = after

    # 4. Preenche IDs nulos (linhas locais que nunca foram para o Supabase).
    #    Feito depois da dedupe para nao alterar qual linha e mantida.
    id_filled = {}
    tables_with_id = [
        r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        if any(c[1] == "id" for c in conn.execute(f'PRAGMA table_info("{r[0]}")'))
    ]
    for table in tables_with_id:
        max_id = conn.execute(f'SELECT COALESCE(MAX(CAST("id" AS INTEGER)),0) FROM "{table}"').fetchone()[0]
        nulls = conn.execute(f'SELECT rowid FROM "{table}" WHERE "id" IS NULL ORDER BY rowid').fetchall()
        if not nulls:
            continue
        for i, (rid,) in enumerate(nulls, start=1):
            conn.execute(f'UPDATE "{table}" SET "id"=? WHERE rowid=?', (max_id + i, rid))
        id_filled[table] = len(nulls)
    report["steps"]["ids_nulos_preenchidos"] = id_filled

    # 5. Deduplica por chave primaria (id) — ex.: assessments com linhas repetidas
    pk_dupes = {}
    for table in tables_with_id:
        before = conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
        conn.execute(f'DELETE FROM "{table}" WHERE rowid NOT IN (SELECT MAX(rowid) FROM "{table}" GROUP BY "id")')
        after = conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
        if before != after:
            pk_dupes[table] = before - after
    report["steps"]["duplicatas_de_pk_removidas"] = pk_dupes

    conn.commit()
    conn.close()
    return report


def main():
    parser = argparse.ArgumentParser(description="Prepara o backup limpo para o Supabase.")
    parser.add_argument("--source", help="Pasta do backup ou caminho do backup_clean.db.")
    parser.add_argument("--out", help="Caminho do restore_ready.db de saida.")
    args = parser.parse_args()

    source = _find_source(args.source)
    if not source or not os.path.exists(source):
        print("[ERRO] backup_clean.db nao encontrado. Rode antes: python scripts/backup_clean.py")
        return 1

    out_path = args.out or os.path.join(os.path.dirname(source), "restore_ready.db")
    report = prepare(source, out_path)

    with open(os.path.join(os.path.dirname(out_path), "prep_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Origem : {source}")
    print(f"Destino: {out_path}\n")
    for k, v in report["steps"].items():
        if isinstance(v, list):
            continue
        print(f"  {k:46s} {v}")
    print(f"\nRelatorio: {os.path.join(os.path.dirname(out_path), 'prep_report.json')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
