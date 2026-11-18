"""Cliente da API local de automação do iSeduc (aba Portal).

A API roda apenas localmente (`apps/api/api_service.py`, porta 8002). No
Streamlit Cloud ela não existe, então todas as chamadas falham de forma
graciosa e a UI mostra um aviso em vez de estourar. O endereço pode ser
configurado em `PORTAL_API_URL` (secrets do Streamlit ou variável de ambiente).
"""

import os

import requests

DEFAULT_URL = "http://127.0.0.1:8002"
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


def api_get_text(path: str, params: dict = None):
    """GET na API local esperando texto puro. Retorna (texto, erro)."""
    try:
        r = requests.get(f"{get_api_url()}{path}", params=params, timeout=TIMEOUT)
        r.raise_for_status()
        return r.text, None
    except Exception as e:
        return None, str(e)


def api_post(path: str, json: dict = None):
    """POST na API local com corpo JSON. Retorna (dados, erro)."""
    try:
        r = requests.post(f"{get_api_url()}{path}", json=json, timeout=POST_TIMEOUT)
        r.raise_for_status()
        try:
            return r.json(), None
        except Exception:
            return r.text, None
    except Exception as e:
        return None, str(e)


def api_post_params(path: str, params: dict = None):
    """POST na API local com parâmetros de query. Retorna (dados, erro)."""
    try:
        r = requests.post(f"{get_api_url()}{path}", params=params, timeout=POST_TIMEOUT)
        r.raise_for_status()
        try:
            return r.json(), None
        except Exception:
            return r.text, None
    except Exception as e:
        return None, str(e)


# ---------------------------------------------------------------------------
# Helpers de alto nível usados pela aba Portal
# ---------------------------------------------------------------------------
def turmas_completo():
    return api_get("/turmas-completo")


def subjects_for_class(class_id):
    return api_get(f"/api/classes/{class_id}/subjects")


def historico(**filtros):
    return api_get("/historico", params={k: v for k, v in filtros.items() if v is not None})


def planejamento_pendente(**filtros):
    return api_get("/planejamento/pendente", params={k: v for k, v in filtros.items() if v is not None})


def listar_aulas(pasta="pendentes", turma_id="", disciplina_id=""):
    return api_get("/aulas/listar", params={
        "pasta": pasta,
        "turma_id": turma_id or "",
        "disciplina_id": disciplina_id or "",
    })


def ler_plano(arquivo):
    return api_get_text(f"/get_plan_content/{arquivo}")


def excluir_plano(pasta, arquivo, apagar_planejamento=True):
    return api_post("/aulas/excluir", {"pasta": pasta, "arquivo": arquivo,
                                       "apagar_planejamento": apagar_planejamento})


def gerar_planos(output_dir="pendentes", force_overwrite=False, turma_id="",
                 disciplina_id="", estrategia=None, aula_min=None, aula_max=None):
    params = {
        "auto_confirm": True,
        "output_dir": output_dir,
        "force_overwrite": force_overwrite,
        "turma_id": turma_id or "",
        "disciplina_id": disciplina_id or "",
    }
    if estrategia:
        params["estrategia"] = estrategia
    if aula_min:
        params["aula_min"] = int(aula_min)
    if aula_max:
        params["aula_max"] = int(aula_max)
    return api_post_params("/gerar-txt-planos", params)


def registrar_lote(files=None, all_files=False):
    return api_post("/registrar_lote", {"files": files or [], "all": bool(all_files)})


def registrar_aula(filename):
    return api_post("/registrar_aula", {"filename": filename})


def registrar_status():
    return api_get("/registrar_status")


def raspagem_executar(turma=None, disciplina=None, reconciliar=False):
    params = {}
    if turma:
        params["turma"] = turma
    if disciplina:
        params["disciplina"] = disciplina
    if reconciliar:
        params["reconciliar"] = True
    return api_post_params("/raspagem/executar", params or None)


def raspagem_status():
    return api_get("/raspagem/status")


def raspagem_relatorio(data=None):
    return api_get("/raspagem/relatorio", params={"data": data} if data else None)


def painel(turma_id, disciplina_id):
    return api_get("/painel", params={"turma_id": turma_id, "disciplina_id": disciplina_id})


def consolidadas(turma_code=""):
    return api_get("/consolidadas", params={"turma_code": turma_code or ""})


def config_all():
    return api_get("/config/all")


def config_set(chave, valor, excluir=False):
    return api_post("/config/set", {"chave": chave, "valor": valor, "excluir": excluir})


def planejamento_reset(turma_id=None, disciplina_id=None):
    return api_post("/planejamento/reset", {"turma_id": turma_id, "disciplina_id": disciplina_id})


def feriados():
    return api_get("/feriados")


def sabados():
    return api_get("/sabados")


def grade_turmas():
    return api_get("/grade/turmas")


def grade_ver(turma):
    return api_get("/grade/ver", params={"turma": turma})


def grade_editar(operacao, turma, **campos):
    payload = {"operacao": operacao, "turma": turma}
    payload.update(campos)
    return api_post("/grade/editar", payload)


def weekly_schedule(class_name=None):
    return api_get("/weekly-schedule", params={"class_name": class_name} if class_name else None)
