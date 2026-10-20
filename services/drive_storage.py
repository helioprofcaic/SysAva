"""Sincronização de arquivos com o Google Drive via service account (bot).

A service account é a "conta bot" (ex.: bot-sysava@sysava.iam.gserviceaccount.com).
Ela precisa ter acesso de **Editor** à pasta do Drive.

Ordem de procura das credenciais:
1. ``st.secrets["gcp_service_account"]`` (tabela TOML com os campos do JSON)
2. ``st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"]`` (JSON em texto)
3. ``GOOGLE_SERVICE_ACCOUNT_JSON`` / ``GOOGLE_APPLICATION_CREDENTIALS`` no ambiente
4. ``data/drive_credentials.json`` ou ``drive_credentials.json`` (local, ignorado no git)

O ID da pasta vem de ``st.secrets["DRIVE_FOLDER_ID"]``, ``DRIVE_FOLDER_ID`` no
ambiente ou do padrão abaixo.
"""

from __future__ import annotations

import io
import json
import mimetypes
import os
from datetime import datetime
from typing import Optional

SCOPES = ["https://www.googleapis.com/auth/drive"]
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_FOLDER_ID = "1db5qPNH9vOQKIabfNgWpetvjQsYsUuQi"
_FOLDER_MIME = "application/vnd.google-apps.folder"
_GOOGLE_DOC_MIMES = {
    "application/vnd.google-apps.document",
    "application/vnd.google-apps.spreadsheet",
    "application/vnd.google-apps.presentation",
}

# Não sincroniza caches, logs nem backups grandes por padrão.
_SKIP_DIRS = {"__pycache__", ".git", ".relatorios", ".chrome_profile", ".pytest_cache"}
_SKIP_EXTS = {".pyc", ".pyo", ".log"}
DEFAULT_MAX_BYTES = 1_000_000  # 1 MB


def _secret(key: str, default=None):
    try:
        import streamlit as st
        return st.secrets.get(key, default)
    except Exception:
        return default


def load_service_account_info() -> dict:
    """Carrega o JSON da service account de secrets/ambiente/arquivo."""
    info = _secret("gcp_service_account")
    if info:
        if isinstance(info, str):
            return json.loads(info)
        return dict(info)

    raw = _secret("GOOGLE_SERVICE_ACCOUNT_JSON") or os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if raw:
        return json.loads(raw)

    path = (_secret("GOOGLE_SERVICE_ACCOUNT_FILE")
            or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
    candidates = []
    if path:
        candidates.append(path)
    candidates.extend([
        os.path.join(PROJECT_ROOT, "data", "drive_credentials.json"),
        os.path.join(PROJECT_ROOT, "drive_credentials.json"),
    ])
    for p in candidates:
        if p and os.path.exists(p):
            with open(p, "r", encoding="utf-8") as fh:
                return json.load(fh)

    raise RuntimeError(
        "Credenciais da service account do Drive não encontradas. "
        "Coloque o JSON em data/drive_credentials.json (local) ou em "
        "st.secrets['gcp_service_account'] (Cloud)."
    )


def get_folder_id() -> str:
    return str(_secret("DRIVE_FOLDER_ID")
               or os.environ.get("DRIVE_FOLDER_ID")
               or DEFAULT_FOLDER_ID)


def get_service():
    """Cliente autenticado do Google Drive (Drive API v3)."""
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    info = load_service_account_info()
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def list_files(folder_id: Optional[str] = None) -> list[dict]:
    """Lista os arquivos/pastas diretamente dentro de ``folder_id``."""
    svc = get_service()
    fid = folder_id or get_folder_id()
    out, token = [], None
    while True:
        resp = svc.files().list(
            q=f"'{fid}' in parents and trashed = false",
            fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)",
            pageSize=1000,
            pageToken=token,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()
        out.extend(resp.get("files", []))
        token = resp.get("nextPageToken")
        if not token:
            break
    return out


def credentials_available() -> bool:
    try:
        load_service_account_info()
        return True
    except Exception:
        return False


def find_child(name: str, parent_id: Optional[str] = None) -> Optional[dict]:
    parent = parent_id or get_folder_id()
    for item in list_files(parent):
        if item["name"] == name:
            return item
    return None


def _remote_mtime(item: dict) -> float:
    try:
        return datetime.fromisoformat(
            str(item.get("modifiedTime")).replace("Z", "+00:00")
        ).timestamp()
    except Exception:
        return 0.0


def sync_tree(folder_id: str, dest_dir: str,
              max_bytes: int = DEFAULT_MAX_BYTES,
              overwrite: bool = False) -> list[str]:
    """Baixa uma árvore do Drive preservando subpastas.

    Pula ``__pycache__``, logs, ``.pyc`` e arquivos maiores que ``max_bytes``.
    Só sobrescreve o local se o remoto for mais novo (ou ``overwrite=True``).
    """
    os.makedirs(dest_dir, exist_ok=True)
    baixados = []
    for item in list_files(folder_id):
        nome = item["name"]
        if item["mimeType"] == _FOLDER_MIME:
            if nome in _SKIP_DIRS:
                continue
            baixados.extend(sync_tree(item["id"], os.path.join(dest_dir, nome),
                                      max_bytes=max_bytes, overwrite=overwrite))
            continue
        if item["mimeType"] in _GOOGLE_DOC_MIMES:
            continue
        ext = os.path.splitext(nome)[1].lower()
        if ext in _SKIP_EXTS:
            continue
        try:
            size = int(item.get("size") or 0)
        except (TypeError, ValueError):
            size = 0
        if max_bytes and size > max_bytes:
            continue
        destino = os.path.join(dest_dir, nome.replace("/", "_"))
        if os.path.exists(destino) and not overwrite:
            if os.path.getmtime(destino) >= _remote_mtime(item) - 30:
                continue
        download_file(item["id"], destino)
        baixados.append(destino)
    return baixados


def sync_repo_down(dest_root: Optional[str] = None,
                   max_bytes: int = DEFAULT_MAX_BYTES,
                   overwrite: bool = False) -> list[str]:
    """Baixa a pasta ``repo`` do Drive para ``data/repo`` (plugins/Turmas/etc.)."""
    root_id = get_folder_id()
    repo = find_child("repo", root_id)
    destino = dest_root or os.path.join(PROJECT_ROOT, "data", "repo")
    if repo:
        return sync_tree(repo["id"], destino, max_bytes=max_bytes, overwrite=overwrite)
    # Fallback: a própria pasta configurada já é o repo
    return sync_tree(root_id, destino, max_bytes=max_bytes, overwrite=overwrite)


def sync_db_down(dest_path: Optional[str] = None, force: bool = False) -> Optional[str]:
    """Baixa ``escola_ativa.db`` do Drive (raiz ou pasta ``data``), se existir."""
    root_id = get_folder_id()
    item = find_child("escola_ativa.db", root_id)
    if not item:
        pasta_data = find_child("data", root_id)
        if pasta_data:
            item = find_child("escola_ativa.db", pasta_data["id"])
    if not item:
        return None
    destino = dest_path or os.path.join(PROJECT_ROOT, "data", "escola_ativa.db")
    if os.path.exists(destino) and not force:
        if os.path.getmtime(destino) >= _remote_mtime(item) - 30:
            return None
    download_file(item["id"], destino)
    return destino


def sync_db_up(local_path: Optional[str] = None) -> dict:
    """Envia o SQLite local para a raiz do Drive (backup/restauração no Cloud)."""
    origem = local_path or os.path.join(PROJECT_ROOT, "data", "escola_ativa.db")
    if not os.path.exists(origem):
        raise FileNotFoundError(origem)
    try:
        return upload_file(origem, folder_id=get_folder_id(), name="escola_ativa.db")
    except Exception as e:
        msg = str(e)
        if "storageQuotaExceeded" in msg or "storage quota" in msg.lower():
            raise RuntimeError(
                "A service account não tem cota para CRIAR arquivos no Meu Drive. "
                "Envie o escola_ativa.db uma vez pelo Drive web; depois as "
                "atualizações podem funcionar. Para upload automático, use um "
                "Shared Drive ou OAuth de uma conta comum (conta bot)."
            ) from e
        raise


def download_file(file_id: str, dest_path: str) -> str:
    """Baixa um arquivo binário do Drive para ``dest_path``."""
    from googleapiclient.http import MediaIoBaseDownload

    os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
    svc = get_service()
    request = svc.files().get_media(fileId=file_id)
    with io.FileIO(dest_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
    return dest_path


def upload_file(local_path: str, folder_id: Optional[str] = None,
                name: Optional[str] = None, mime_type: Optional[str] = None) -> dict:
    """Envia/atualiza um arquivo no Drive. Se existir com o mesmo nome, atualiza."""
    from googleapiclient.http import MediaFileUpload

    fid = folder_id or get_folder_id()
    svc = get_service()
    nome = name or os.path.basename(local_path)
    mime = mime_type or mimetypes.guess_type(local_path)[0] or "application/octet-stream"
    media = MediaFileUpload(local_path, mimetype=mime, resumable=True)

    existentes = svc.files().list(
        q=f"'{fid}' in parents and name = '{nome}' and trashed = false",
        fields="files(id, name)", pageSize=10,
        supportsAllDrives=True, includeItemsFromAllDrives=True,
    ).execute().get("files", [])
    if existentes:
        file_id = existentes[0]["id"]
        return svc.files().update(
            fileId=file_id, media_body=media,
            fields="id, name, modifiedTime",
        ).execute()
    return svc.files().create(
        body={"name": nome, "parents": [fid]},
        media_body=media, fields="id, name, modifiedTime",
    ).execute()


def download_folder(folder_id: str, dest_dir: str, recursive: bool = True) -> list[str]:
    """Baixa uma pasta inteira do Drive para ``dest_dir`` (preserva subpastas)."""
    os.makedirs(dest_dir, exist_ok=True)
    baixados = []
    for item in list_files(folder_id):
        nome = item["name"].replace("/", "_")
        dest = os.path.join(dest_dir, nome)
        if item["mimeType"] == _FOLDER_MIME:
            if recursive:
                baixados.extend(download_folder(item["id"], dest, recursive=True))
            continue
        if item["mimeType"] in _GOOGLE_DOC_MIMES:
            continue  # Docs/Sheets/Slides não são baixados como binário
        download_file(item["id"], dest)
        baixados.append(dest)
    return baixados


def delete_file(file_id: str) -> None:
    get_service().files().delete(fileId=file_id, supportsAllDrives=True).execute()
