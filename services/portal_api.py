"""Cliente da API local de automação do iSeduc (aba Portal).

A API roda apenas localmente (`apps/api/api_service.py`). No Streamlit Cloud
ela não existe, então todas as chamadas falham de forma graciosa e a UI mostra
um aviso em vez de estourar. O endereço pode ser configurado em `PORTAL_API_URL`
(secrets do Streamlit ou variável de ambiente).
"""

import os

import requests

DEFAULT_URL = "http://127.0.0.1:8000"
TIMEOUT = 8
POST_TIMEOUT = 120


def get_api_url() -> str:
    url = os.environ.get("PORTAL_API_URL", "")
    if not url:
        try:
            import streamlit as st
            url = st.secrets.get("PORTAL_API_URL", "")
        except Exception:
            url = ""
    return (url or DEFAULT_URL).rstrip("/")


def status():
    """Retorna (online: bool, detalhe: str) sobre a API local."""
    url = get_api_url()
    try:
        r = requests.get(f"{url}/health-check", timeout=TIMEOUT)
        if r.status_code == 200:
            return True, "API local online"
        return False, f"API respondeu HTTP {r.status_code}"
    except Exception as e:
        return False, f"offline ({type(e).__name__})"


def api_get(path: str, params: dict = None):
    """GET na API local. Retorna (dados, erro)."""
    try:
        r = requests.get(f"{get_api_url()}{path}", params=params, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)


def api_post(path: str, json: dict = None):
    """POST na API local. Retorna (dados, erro)."""
    try:
        r = requests.post(f"{get_api_url()}{path}", json=json, timeout=POST_TIMEOUT)
        r.raise_for_status()
        try:
            return r.json(), None
        except Exception:
            return r.text, None
    except Exception as e:
        return None, str(e)
