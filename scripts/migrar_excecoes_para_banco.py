"""Migra a lista negra local (data/excecoes_alunos.json) para o banco (IS-040).

A fonte de verdade passa a ser o Supabase:
  app_users.is_active = false  -> 'falta'   (aparece na chamada como Falta)
  app_users.is_portal = false  -> 'inativo' (excluido da lista de chamada)

Uso:
    python scripts/migrar_excecoes_para_banco.py --dry-run   # so mostra o diff
    python scripts/migrar_excecoes_para_banco.py             # aplica e regera o espelho

Depois de aplicar, o proprio script regrava data/excecoes_alunos.json a partir
do banco (espelho local) para os robos de apps/ continuarem funcionando.
"""

import sys
import os
import json
import argparse

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from services import database as db  # noqa: E402

EXCECOES_PATH = os.path.join(project_root, "data", "excecoes_alunos.json")


def load_local_excecoes():
    if not os.path.exists(EXCECOES_PATH):
        return {"blacklist": [], "blacklist_names": [], "dropouts": []}
    with open(EXCECOES_PATH, "r", encoding="utf-8") as fh:
        data = json.load(fh) or {}
    return {
        "blacklist": [str(x).strip() for x in data.get("blacklist", []) if str(x).strip()],
        "blacklist_names": [str(x).strip().upper() for x in data.get("blacklist_names", []) if str(x).strip()],
        "dropouts": [str(x).strip() for x in data.get("dropouts", []) if str(x).strip()],
    }


def main():
    parser = argparse.ArgumentParser(description="Migra a lista negra JSON para o banco")
    parser.add_argument("--dry-run", action="store_true", help="so mostra o plano, nao grava nada")
    args = parser.parse_args()

    if not db.is_db_connected():
        print("ERRO: banco offline (verifique SUPABASE_URL/SUPABASE_KEY no .env).")
        return 1

    exc = load_local_excecoes()
    flags = db.get_frequency_flags()
    if not flags:
        print("ERRO: nao foi possivel ler as flags de frequencia do banco.")
        return 1

    # Indexa o banco por username/RA e por nome
    por_ident = {}
    por_nome = {}
    for username, f in flags.items():
        ra = str(f.get("ra") or username).strip()
        por_ident[ra] = (username, f)
        por_ident[username] = (username, f)
        nome = str(f.get("name") or "").strip().upper()
        if nome:
            por_nome[nome] = (username, f)

    para_falta, para_inativo, so_no_banco, nao_encontrado = [], [], [], []

    for ra in exc["blacklist"]:
        hit = por_ident.get(ra)
        if not hit:
            for nome in exc["blacklist_names"]:
                if nome in por_nome:
                    hit = por_nome[nome]
                    break
        if not hit:
            nao_encontrado.append(ra)
            continue
        username, f = hit
        if f["frequencia_status"] != "falta":
            para_falta.append((username, f.get("name"), f["frequencia_status"]))

    for ra in exc["dropouts"]:
        hit = por_ident.get(ra)
        if not hit:
            nao_encontrado.append(ra)
            continue
        username, f = hit
        if f["frequencia_status"] != "inativo":
            para_inativo.append((username, f.get("name"), f["frequencia_status"]))

    json_ids = set(exc["blacklist"]) | set(exc["dropouts"])
    for username, f in flags.items():
        ra = str(f.get("ra") or username).strip()
        if f["frequencia_status"] != "normal" and ra not in json_ids:
            so_no_banco.append((username, f.get("name"), f["frequencia_status"]))

    print("=== PLANO DE MIGRACAO (JSON -> banco) ===")
    print(f"[falta]   {len(para_falta)} alunos do JSON que estao ativos no banco:")
    for username, nome, atual in para_falta:
        print(f"    {username} | {nome} | status atual: {atual}")
    print(f"[inativo] {len(para_inativo)} dropouts do JSON fora da lista no banco:")
    for username, nome, atual in para_inativo:
        print(f"    {username} | {nome} | status atual: {atual}")
    print(f"[banco]   {len(so_no_banco)} marcados apenas no banco (mantidos, entram no espelho):")
    for username, nome, st_ in so_no_banco:
        print(f"    {username} | {nome} | {st_}")
    print(f"[?]       {len(nao_encontrado)} no JSON sem correspondencia no banco: {nao_encontrado}")

    if args.dry_run:
        print("\nDRY-RUN: nada foi alterado.")
        return 0

    erros = 0
    # Reaplica todos os nao-normais (idempotente): garante que as colunas novas
    # de user_profiles sejam preenchidas apos o DDL ser executado.
    motivos = {}
    for u, _n, _s in para_falta:
        motivos[u] = "migracao do JSON (lista negra)"
    for u, _n, _s in para_inativo:
        motivos[u] = "migracao do JSON (dropout)"
    status_banco = {u: st_ for u, _n, st_ in so_no_banco}
    aplicar = []
    for username, f in flags.items():
        st_ = status_banco.get(username, f["frequencia_status"])
        if st_ == "normal":
            continue
        aplicar.append((username, f.get("name"), st_, motivos.get(username) or f.get("motivo") or "migracao do JSON"))
    for username, nome, st_, motivo in aplicar:
        _data, err = db.set_frequency_flag(username, st_, motivo=motivo)
        print(f"  {'OK ' if not err else 'ERRO'} {st_:7s} -> {username} ({nome}) {err or ''}")
        erros += 1 if err else 0

    ok, msg = db.sync_blacklist_json_mirror()
    print(f"espelho local: {'OK' if ok else 'FALHOU'} - {msg}")

    if erros:
        print(f"\nConcluido com {erros} erro(s).")
        return 1
    print("\nMigracao concluida.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
