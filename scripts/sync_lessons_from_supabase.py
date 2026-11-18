"""Sincroniza a tabela `lessons` do Supabase para o SQLite local.

O gerador de planos (`apps/planejamento_registro/core/gerador.py`) e a API
local leem as aulas da tabela `lessons` do `data/escola_ativa.db`. Quando uma
disciplina tem aulas na nuvem mas não no local (ex.: PROGRAMAÇÃO PARA
DISPOSITIVOS MÓVEIS), o "Gerar planos" não produz nada.

Este script busca as aulas no Supabase e faz *upsert* no SQLite local por `id`
(mesmo conjunto de colunas nas duas pontas). Faz backup antes de gravar.

Uso:
    python scripts/sync_lessons_from_supabase.py --subject 5        # dry-run
    python scripts/sync_lessons_from_supabase.py --subject 5 --apply
    python scripts/sync_lessons_from_supabase.py --all --apply      # todas
    python scripts/sync_lessons_from_supabase.py --subject 5,8 --apply
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
COLUNAS = ["id", "title", "description", "video_url", "subject_id", "week",
           "full_content", "objective", "resources", "uuid", "status",
           "created_at", "updated_at", "uuid_id"]


def _fetch_lessons(subjects):
    from services import database as db
    client = db.get_supabase()
    if client is None:
        return None
    rows = []
    if subjects:
        for sid in subjects:
            res = client.table("lessons").select("*").eq("subject_id", int(sid)).execute()
            rows.extend(res.data or [])
    else:
        start = 0
        while True:
            res = client.table("lessons").select("*").range(start, start + 999).execute()
            d = res.data or []
            rows.extend(d)
            if len(d) < 1000:
                break
            start += 1000
    return rows


def main():
    parser = argparse.ArgumentParser(description="Sincroniza lessons Supabase -> SQLite local")
    parser.add_argument("--subject", help="IDs de disciplina (ex.: 5 ou 5,8). Padrão: todas.")
    parser.add_argument("--all", action="store_true", help="Sincroniza todas as disciplinas")
    parser.add_argument("--apply", action="store_true", help="Grava (com backup)")
    args = parser.parse_args()

    if not os.path.exists(DB_PATH):
        print(f"[erro] Banco local não encontrado: {DB_PATH}")
        return

    subjects = None
    if args.subject and not args.all:
        subjects = [s.strip() for s in args.subject.split(",") if s.strip()]

    cloud = _fetch_lessons(subjects)
    if cloud is None:
        print("[erro] Supabase indisponível.")
        return
    if not cloud:
        print("Nenhuma aula retornada do Supabase.")
        return

    # Deduplica por id (mantém a última ocorrência).
    por_id = {}
    for r in cloud:
        por_id[str(r.get("id"))] = r
    cloud = list(por_id.values())
    print(f"Supabase: {len(cloud)} aula(s)"
          + (f" (disciplinas {subjects})" if subjects else " (todas)"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    ids_cloud = {str(r.get("id")) for r in cloud}
    ids_local = {str(r[0]) for r in conn.execute("SELECT id FROM lessons")}
    novos = ids_cloud - ids_local
    print(f"Local hoje: {len(ids_local)} aula(s) | já presentes: {len(ids_cloud & ids_local)} "
          f"| novos: {len(novos)}")

    if not args.apply:
        print("\n[dry-run] Nada foi alterado. Use --apply para gravar.")
        conn.close()
        return

    conn.close()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = os.path.join(PROJECT_ROOT, "data", f"escola_ativa_backup_lessons_{stamp}.db")
    shutil.copy2(DB_PATH, backup)
    print(f"Backup: {backup}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    ph = ", ".join("?" * len(COLUNAS))
    inseridos = 0
    for r in cloud:
        cur.execute(
            f"INSERT OR REPLACE INTO lessons ({', '.join(COLUNAS)}) VALUES ({ph})",
            tuple(r.get(c) for c in COLUNAS),
        )
        inseridos += 1
    conn.commit()
    total = cur.execute("SELECT COUNT(*) FROM lessons").fetchone()[0]
    conn.close()
    print(f"Gravadas {inseridos} aula(s). Total local agora: {total}.")


if __name__ == "__main__":
    main()
