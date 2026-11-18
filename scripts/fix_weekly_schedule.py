"""Corrige duplicatas em `weekly_schedule` e restaura a UNIQUE constraint.

Causa raiz: `apps/api/backup_routes.py` (`/pull-from-cloud`) recriava a tabela
com `DROP TABLE` + `CREATE TABLE (... TEXT)`, removendo a PRIMARY KEY e a
UNIQUE(class_name, day_of_week, time_slot). A partir daí, cada sync passou a
inserir sem sobrescrever, gerando slots duplicados (vistos como "COLISÃO!" na
grade). O Supabase (fonte soberana da grade) está correto.

O script reconstrói a tabela com o schema canônico, usando como base o
Supabase (se acessível) ou a deduplicação local, e sempre cria um backup do
banco antes de gravar.

Uso:
    python scripts/fix_weekly_schedule.py            # simulação (dry-run)
    python scripts/fix_weekly_schedule.py --apply    # aplica (com backup)
    python scripts/fix_weekly_schedule.py --apply --no-cloud
"""

import argparse
import os
import shutil
import sqlite3
import sys
from collections import Counter
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

DB_PATH = os.path.join(PROJECT_ROOT, "data", "escola_ativa.db")
CHAVE = ("class_name", "day_of_week", "time_slot")
COLUNAS = ["id", "class_name", "day_of_week", "time_slot", "subject_name",
           "professor_name", "created_at", "class_id"]
DDL = """CREATE TABLE weekly_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT NOT NULL,
            day_of_week TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            subject_name TEXT NOT NULL,
            professor_name TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            class_id INTEGER,
            UNIQUE(class_name, day_of_week, time_slot))"""


def _score(row):
    """Prefere a linha 'real' (com created_at e class_id) na deduplicação."""
    return (1 if row.get("created_at") else 0,
            1 if row.get("class_id") not in (None, "") else 0)


def _dedup(rows):
    melhor = {}
    for r in rows:
        k = tuple(str(r.get(c)) for c in CHAVE)
        atual = melhor.get(k)
        if atual is None or _score(r) > _score(atual):
            melhor[k] = r
    return list(melhor.values())


def _carregar_cloud():
    try:
        from services import database as db
        client = db.get_supabase()
        if client is None:
            return None
        return client.table("weekly_schedule").select("*").execute().data or []
    except Exception as e:
        print(f"[aviso] Supabase indisponível: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Corrige duplicatas de weekly_schedule")
    parser.add_argument("--apply", action="store_true", help="Grava as mudanças (com backup)")
    parser.add_argument("--no-cloud", action="store_true", help="Não consulta o Supabase")
    args = parser.parse_args()

    if not os.path.exists(DB_PATH):
        print(f"[erro] Banco não encontrado: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    antes = [dict(r) for r in conn.execute("SELECT * FROM weekly_schedule")]
    ddl_atual = conn.execute(
        "SELECT sql FROM sqlite_master WHERE name='weekly_schedule'").fetchone()
    conn.close()

    contagem = Counter(tuple(str(r.get(c)) for c in CHAVE) for r in antes)
    duplicados = {k: v for k, v in contagem.items() if v > 1}
    print(f"Linhas atuais: {len(antes)} | slots únicos: {len(contagem)} | "
          f"slots duplicados: {len(duplicados)}")
    if "UNIQUE" in (ddl_atual[0] if ddl_atual else ""):
        print("Schema atual JÁ tem UNIQUE.")
    else:
        print("Schema atual NÃO tem UNIQUE (esta é a causa das duplicatas).")

    base = None
    origem = ""
    if not args.no_cloud:
        cloud = _carregar_cloud()
        if cloud:
            cloud_dup = Counter(tuple(str(r.get(c)) for c in CHAVE) for r in cloud)
            cloud_dup = {k: v for k, v in cloud_dup.items() if v > 1}
            print(f"Supabase: {len(cloud)} linhas | duplicados na nuvem: {len(cloud_dup)}")
            if not cloud_dup:
                base = _dedup(cloud)
                origem = "Supabase (fonte soberana)"
    if base is None:
        base = _dedup(antes)
        origem = "local (deduplicado)"

    print(f"Linhas finais: {len(base)} | origem: {origem}")

    if not args.apply:
        print("\n[dry-run] Nada foi alterado. Use --apply para gravar.")
        return

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = os.path.join(PROJECT_ROOT, "data", f"escola_ativa_backup_weekly_{stamp}.db")
    shutil.copy2(DB_PATH, backup)
    print(f"Backup: {backup}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS weekly_schedule")
    cur.execute(DDL)
    placeholders = ", ".join(["?"] * len(COLUNAS))
    cur.executemany(
        f"INSERT OR REPLACE INTO weekly_schedule ({', '.join(COLUNAS)}) "
        f"VALUES ({placeholders})",
        [tuple(r.get(c) for c in COLUNAS) for r in base],
    )
    conn.commit()
    total = cur.execute("SELECT COUNT(*) FROM weekly_schedule").fetchone()[0]
    conn.close()

    print(f"Linhas após: {total}")
    if total == len(base):
        print("OK — UNIQUE restaurada e duplicatas removidas.")
    else:
        print("ATENÇÃO: contagem divergente do esperado.")


if __name__ == "__main__":
    main()
