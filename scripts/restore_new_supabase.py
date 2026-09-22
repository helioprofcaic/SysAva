"""
Restaura o backup limpo (sem Base64) em um novo projeto Supabase.

Pre-requisitos:
  1. O schema ja foi aplicado no novo projeto (docs/NOVO_BANCO_SCHEMA.sql).
  2. Existe uma pasta de backup gerada por scripts/backup_clean.py
     (contendo backup_clean.db).

Credenciais (em ordem de prioridade):
  --url / --key na linha de comando, ou as variaveis de ambiente
  SUPABASE_URL / SUPABASE_KEY, ou .streamlit/secrets.toml do projeto.

Uso:
    python scripts/restore_new_supabase.py --url https://xxx.supabase.co --key <anon-key>
    python scripts/restore_new_supabase.py --source data/backup_clean_2026-09-22_0757
    python scripts/restore_new_supabase.py --dry-run
"""

import argparse
import glob
import json
import os
import sqlite3
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Apenas as 21 tabelas essenciais (ver docs/AUDITORIA_BANCO.md).
# Ordem respeita as dependencias de chaves estrangeiras.
# As tabelas de automacao (student_grades, settings, ...) ficam no SQLite.
TABLES_ORDER = [
    "schools", "classes", "subjects", "app_users", "class_subjects",
    "student_enrollments", "lessons", "quizzes", "quiz_questions",
    "forum_posts", "user_history", "assessments", "assessment_questions",
    "student_assessments", "student_assessment_answers", "schedules",
    "attendance", "weekly_schedule", "historico_aulas", "planejamento",
    "master_config",
]

PK_OVERRIDES = {
    "app_users": ["username"],
    "master_config": ["key"],
    "student_enrollments": ["user_username", "class_id"],
}

JSON_COLUMNS = {
    "subjects": ["aliases"],
    "master_config": ["value"],
    "quiz_questions": ["options"],
    "assessment_questions": ["options"],
}

BOOL_COLUMNS = {
    "app_users": ["is_active"],
    "class_subjects": ["is_active"],
    "attendance": ["is_present"],
    "historico_aulas": ["is_duplicate"],
}

BATCH_SIZE = 500


def _coerce(value, json_cols, bool_cols, col_name):
    if value is None:
        return None
    if col_name in bool_cols:
        if isinstance(value, str):
            return value.strip().lower() in ("1", "true", "t", "yes", "sim")
        return bool(value)
    if col_name in json_cols and isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            # Valor nao-JSON vira string JSON (aceito pelo JSONB)
            return json.dumps(value)
    return value


def _find_source(explicit):
    if explicit:
        if os.path.isdir(explicit):
            ready = os.path.join(explicit, "restore_ready.db")
            return ready if os.path.exists(ready) else os.path.join(explicit, "backup_clean.db")
        return explicit
    matches = sorted(glob.glob(os.path.join(project_root, "data", "backup_clean_*", "backup_clean.db")))
    if not matches:
        return None
    # Prefere a versao preparada (datas normalizadas + duplicatas removidas)
    ready = os.path.join(os.path.dirname(matches[-1]), "restore_ready.db")
    return ready if os.path.exists(ready) else matches[-1]


def _read_credentials(args):
    url = args.url or os.environ.get("SUPABASE_URL")
    key = args.key or os.environ.get("SUPABASE_KEY")
    if not url or not key:
        try:
            import tomllib
            with open(os.path.join(project_root, ".streamlit", "secrets.toml"), "rb") as f:
                secrets = tomllib.load(f)
            url = url or secrets.get("SUPABASE_URL")
            key = key or secrets.get("SUPABASE_KEY")
        except Exception:
            pass
    return url, key


def main():
    parser = argparse.ArgumentParser(description="Restaura o backup limpo no novo Supabase.")
    parser.add_argument("--source", help="Pasta do backup ou caminho do backup_clean.db.")
    parser.add_argument("--url", help="URL do novo projeto Supabase.")
    parser.add_argument("--key", help="Chave anon do novo projeto Supabase.")
    parser.add_argument("--dry-run", action="store_true", help="Nao grava nada, so mostra o plano.")
    args = parser.parse_args()

    source = _find_source(args.source)
    if not source or not os.path.exists(source):
        print("[ERRO] backup_clean.db nao encontrado. Rode antes: python scripts/backup_clean.py")
        return 1

    url, key = _read_credentials(args)
    if not args.dry_run and (not url or not key):
        print("[ERRO] Informe --url/--key (ou defina SUPABASE_URL/SUPABASE_KEY / secrets.toml).")
        return 1

    print(f"Backup : {source}")
    if url:
        print(f"Destino: {url}")
    if args.dry_run:
        print("MODO DRY-RUN: nada sera gravado.\n")

    conn = sqlite3.connect(source)
    conn.row_factory = sqlite3.Row

    client = None
    if not args.dry_run:
        from supabase import create_client
        client = create_client(url, key)

    existing = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    total_rows = 0

    for table in TABLES_ORDER:
        if table not in existing:
            continue
        rows = [dict(r) for r in conn.execute(f'SELECT * FROM "{table}"')]
        if not rows:
            print(f"  {table:28s} vazio, ignorado")
            continue

        json_cols = JSON_COLUMNS.get(table, [])
        bool_cols = BOOL_COLUMNS.get(table, [])
        clean_rows = [
            {k: _coerce(v, json_cols, bool_cols, k) for k, v in row.items()}
            for row in rows
        ]

        if args.dry_run:
            print(f"  {table:28s} {len(clean_rows)} linhas")
            total_rows += len(clean_rows)
            continue

        pk = PK_OVERRIDES.get(table)
        if pk is None:
            pk = ["id"] if "id" in clean_rows[0] else []
        on_conflict = ",".join(pk) if pk else None

        sent = 0
        for i in range(0, len(clean_rows), BATCH_SIZE):
            batch = clean_rows[i:i + BATCH_SIZE]
            query = client.table(table).upsert(batch, on_conflict=on_conflict) if on_conflict \
                else client.table(table).insert(batch)
            query.execute()
            sent += len(batch)
        print(f"  {table:28s} {sent} linhas restauradas")
        total_rows += sent

    conn.close()

    if not args.dry_run and client is not None:
        try:
            client.rpc("reset_identity_sequences").execute()
            print("\nSequencias (identity) reajustadas.")
        except Exception as e:
            print(f"\n[Aviso] Nao foi possivel reajustar as sequencias: {e}")

    print(f"\nTotal: {total_rows} linhas.")
    if args.dry_run:
        print("Rode sem --dry-run para gravar no novo projeto.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
