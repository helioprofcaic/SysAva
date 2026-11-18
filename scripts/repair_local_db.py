"""Repara constraints do banco local perdidas pelo antigo `/pull-from-cloud`.

O endpoint `/pull-from-cloud` (`apps/api/backup_routes.py`) recriava cada
tabela sincronizada com `DROP TABLE` + `CREATE TABLE (... TEXT)`, removendo as
PRIMARY KEY / UNIQUE. Sem as constraints, os imports/syncs passaram a inserir
sem sobrescrever, gerando duplicatas (ex.: `attendance` e `weekly_schedule`).

Este script, para cada tabela com chave natural:
  1. detecta duplicatas exatas;
  2. remove-as (mantendo a linha mais recente, por `created_at`/rowid);
  3. (re)cria um índice UNIQUE que impede a recorrência.

É idempotente e faz backup do banco antes de gravar. O endpoint já foi
corrigido para não destruir o schema nas próximas sincronizações.

Uso:
    python scripts/repair_local_db.py            # simulação (dry-run)
    python scripts/repair_local_db.py --apply    # aplica (com backup)
"""

import argparse
import os
import shutil
import sqlite3
import sys
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

DB_PATH = os.path.join(PROJECT_ROOT, "data", "escola_ativa.db")

# (tabela, colunas da chave natural, colunas que podem ser NULL na chave)
TABELAS = [
    ("attendance", ["student_name", "class_name", "subject_id", "date"], {"subject_id"}),
    ("app_users", ["username"], set()),
    ("classes", ["code"], set()),
    ("subjects", ["name"], set()),
    ("class_subjects", ["class_id", "subject_id"], set()),
    ("lessons", ["subject_id", "title"], set()),
    ("student_enrollments", ["user_username", "class_id"], set()),
    ("historico_aulas", ["data_aula", "horario", "turma", "disciplina"], set()),
    ("weekly_schedule", ["class_name", "day_of_week", "time_slot"], set()),
    ("turma_disciplina_config", ["turma_id", "disciplina_id"], set()),
    # Tabelas cujo id é a chave (id veio como TEXT no pull e perdeu a PK):
    ("assessments", ["id"], set()),
    ("assessment_questions", ["id"], set()),
    ("quizzes", ["id"], set()),
    ("quiz_questions", ["id"], set()),
]


def _key_expr(colunas, nulos):
    """Expressão SQL da chave (IFNULL nas colunas anuláveis)."""
    partes = []
    for c in colunas:
        partes.append(f"IFNULL({c}, '')" if c in nulos else c)
    return ", ".join(partes)


def _contar(conn, tabela, colunas, nulos):
    expr = _key_expr(colunas, nulos)
    total = conn.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]
    unicos = conn.execute(
        f"SELECT COUNT(*) FROM (SELECT 1 FROM {tabela} GROUP BY {expr})").fetchone()[0]
    return total, unicos


def _dedup(conn, tabela, colunas, nulos):
    """Remove duplicatas da chave, mantendo a linha mais recente."""
    expr = _key_expr(colunas, nulos)
    colunas_tabela = [r[1] for r in conn.execute(f"PRAGMA table_info({tabela})")]
    ordem = "created_at DESC, rowid DESC" if "created_at" in colunas_tabela else "rowid DESC"
    antes = conn.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]
    conn.execute(f"""
        DELETE FROM {tabela}
        WHERE rowid IN (
            SELECT rowid FROM (
                SELECT rowid,
                       ROW_NUMBER() OVER (PARTITION BY {expr} ORDER BY {ordem}) AS rn
                FROM {tabela}
            ) WHERE rn > 1
        )
    """)
    depois = conn.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]
    return antes - depois


def _criar_indice(conn, tabela, colunas, nulos):
    nome = f"ux_{tabela}_key"
    expr = _key_expr(colunas, nulos)
    conn.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS {nome} ON {tabela} ({expr})")


def main():
    parser = argparse.ArgumentParser(description="Repara constraints/duplicatas do banco local")
    parser.add_argument("--apply", action="store_true", help="Grava as mudanças (com backup)")
    args = parser.parse_args()

    if not os.path.exists(DB_PATH):
        print(f"[erro] Banco não encontrado: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    existentes = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}

    print(f"{'TABELA':<26} {'LINHAS':>7} {'UNICAS':>7} {'A REMOVER':>10}  OBS")
    print("-" * 70)
    para_corrigir = []
    for tabela, colunas, nulos in TABELAS:
        if tabela not in existentes:
            continue
        cols = [r[1] for r in conn.execute(f"PRAGMA table_info({tabela})")]
        if not all(c in cols for c in colunas):
            print(f"{tabela:<26} {'-':>7} {'-':>7} {'-':>10}  colunas divergentes: faltam {[c for c in colunas if c not in cols]}")
            continue
        total, unicos = _contar(conn, tabela, colunas, nulos)
        remover = total - unicos
        obs = "ok" if remover == 0 else "DUPLICATAS"
        print(f"{tabela:<26} {total:>7} {unicos:>7} {remover:>10}  {obs}")
        if remover > 0:
            para_corrigir.append((tabela, colunas, nulos, remover))

    if not args.apply:
        print("\n[dry-run] Nada foi alterado. Use --apply para gravar.")
        conn.close()
        return

    conn.close()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = os.path.join(PROJECT_ROOT, "data", f"escola_ativa_backup_repair_{stamp}.db")
    shutil.copy2(DB_PATH, backup)
    print(f"\nBackup: {backup}")

    conn = sqlite3.connect(DB_PATH)
    for tabela, colunas, nulos, _remover in para_corrigir:
        removidas = _dedup(conn, tabela, colunas, nulos)
        conn.commit()
        print(f"  {tabela}: {removidas} duplicata(s) removida(s)")

    print("\nGarantindo índices UNIQUE:")
    for tabela, colunas, nulos in TABELAS:
        if tabela not in existentes:
            continue
        cols = [r[1] for r in conn.execute(f"PRAGMA table_info({tabela})")]
        if not all(c in cols for c in colunas):
            continue
        try:
            _criar_indice(conn, tabela, colunas, nulos)
            print(f"  {tabela}: ux_{tabela}_key ok")
        except sqlite3.Error as e:
            print(f"  {tabela}: FALHA no índice -> {e}")
    conn.commit()
    conn.close()
    print("\nConcluído.")


if __name__ == "__main__":
    main()
