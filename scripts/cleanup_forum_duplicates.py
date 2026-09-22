"""
Remove posts de bot duplicados no fórum do Supabase.

Considera duplicata quando o MESMO bot postou a MESMA mensagem (ignorando
espacos/quebras de linha) na MESMA aula. Mantem o post mais antigo de cada
grupo e remove os demais. Nao toca em posts de alunos.

Uso:
    python scripts/cleanup_forum_duplicates.py            # simulação (nao apaga)
    python scripts/cleanup_forum_duplicates.py --apply     # aplica a limpeza
    python scripts/cleanup_forum_duplicates.py --bots "EduBot,SysAva Bot"
"""

import argparse
import os
import sys
from collections import defaultdict

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

BOT_NAMES = ["EduBot", "SysAva Bot"]
BATCH = 200


def _client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        import tomllib
        with open(os.path.join(project_root, ".streamlit", "secrets.toml"), "rb") as f:
            sec = tomllib.load(f)
        url = url or sec.get("SUPABASE_URL")
        key = key or sec.get("SUPABASE_KEY")
    if not url or not key:
        raise SystemExit("[ERRO] SUPABASE_URL/SUPABASE_KEY nao encontrados.")
    from supabase import create_client
    return create_client(url, key)


def _norm(msg):
    return " ".join((msg or "").split())


def _fetch_bot_posts(client, bots):
    rows = []
    for bot in bots:
        start = 0
        while True:
            q = client.table("forum_posts").select("id,lesson_id,user_name,message,created_at")
            q = q.eq("user_name", bot) if bot == "SysAva Bot" else q.ilike("user_name", f"{bot}%")
            r = q.range(start, start + 999).execute()
            rows += r.data
            if len(r.data) < 1000:
                break
            start += 1000
    return rows


def main():
    parser = argparse.ArgumentParser(description="Limpa posts de bot duplicados no forum.")
    parser.add_argument("--apply", action="store_true", help="Aplica a limpeza (padrao: simulacao).")
    parser.add_argument("--bots", default=",".join(BOT_NAMES), help="Nomes/prefixos de bot separados por virgula.")
    args = parser.parse_args()

    bots = [b.strip() for b in args.bots.split(",") if b.strip()]
    client = _client()
    rows = _fetch_bot_posts(client, bots)

    groups = defaultdict(list)
    for r in rows:
        groups[(r["lesson_id"], _norm(r["message"]))].append(r)

    to_delete = []
    wasted = 0
    for (lesson_id, _msg), items in groups.items():
        if len(items) <= 1:
            continue
        items.sort(key=lambda x: (x.get("created_at") or "", x["id"]))
        keep, *dupes = items
        for d in dupes:
            to_delete.append(d["id"])
            wasted += len(d.get("message") or "")

    print("Posts de bot analisados : %d" % len(rows))
    print("Grupos com duplicata    : %d" % sum(1 for v in groups.values() if len(v) > 1))
    print("Posts a remover         : %d (~%.1f KB)" % (len(to_delete), wasted / 1024))

    if not to_delete:
        print("\nNada a fazer.")
        return 0

    if not args.apply:
        print("\n[SIMULACAO] Rode com --apply para remover.")
        return 0

    removed = 0
    for i in range(0, len(to_delete), BATCH):
        chunk = to_delete[i:i + BATCH]
        client.table("forum_posts").delete().in_("id", chunk).execute()
        removed += len(chunk)
    print("\nRemovidos: %d posts." % removed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
