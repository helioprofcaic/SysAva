# -*- coding: utf-8 -*-
"""Diagnóstico/sincronização manual com o Google Drive (service account).

Uso:
  python scripts/drive_check.py                 # lista a pasta configurada
  python scripts/drive_check.py --pull destino  # baixa a pasta inteira
  python scripts/drive_check.py --push arquivo  # envia/atualiza um arquivo
"""

import argparse
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from services import drive_storage as drive


def main():
    parser = argparse.ArgumentParser(description="Teste/sync do Google Drive (service account)")
    parser.add_argument("--folder", default=None, help="ID da pasta (padrão: DRIVE_FOLDER_ID)")
    parser.add_argument("--pull", default=None, help="Pasta local de destino para baixar tudo")
    parser.add_argument("--push", default=None, help="Arquivo local para enviar/atualizar")
    args = parser.parse_args()

    try:
        info = drive.load_service_account_info()
        print("Service account:", info.get("client_email"))
        fid = args.folder or drive.get_folder_id()
        print("Pasta:", fid)

        if args.pull:
            baixados = drive.download_folder(fid, args.pull)
            print(f"Baixados: {len(baixados)} arquivo(s) em {args.pull}")
            for p in baixados[:20]:
                print(" -", p)
            return

        if args.push:
            res = drive.upload_file(args.push, folder_id=fid)
            print("Enviado:", res)
            return

        arquivos = drive.list_files(fid)
        print(f"{len(arquivos)} item(ns):")
        for item in arquivos:
            tipo = "pasta" if item["mimeType"] == "application/vnd.google-apps.folder" else item["mimeType"]
            print(f" - {item['name']}  [{tipo}]  id={item['id']}")
    except Exception as e:
        print("ERRO:", type(e).__name__, e)
        sys.exit(1)


if __name__ == "__main__":
    main()
