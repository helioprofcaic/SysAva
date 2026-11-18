# services/audit_log.py
"""Registro de atividade dos usuários no SysAva (IS-071).

Grava eventos em linhas JSON num arquivo diário, numa pasta OCULTA
(`data/repo/plugins/.relatorios/`), e gera relatórios HTML. Sem chamadas de
rede (não afeta o egress do Supabase).
"""
import os
import glob
import json
import html
import time
from datetime import datetime

_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BASE = os.path.join(_RAIZ, "data", "repo", "plugins", ".relatorios")


def _ensure_dir():
    os.makedirs(_BASE, exist_ok=True)
    # Marca a pasta como oculta no Windows (best-effort).
    try:
        import ctypes
        ctypes.windll.kernel32.SetFileAttributesW(_BASE, 0x02)  # FILE_ATTRIBUTE_HIDDEN
    except Exception:
        pass


def base_dir():
    return _BASE


def registrar(atividade, username="", name="", role="", pagina="", ip="", detalhe=""):
    """Acrescenta um evento ao log do dia. Nunca levanta exceção."""
    try:
        _ensure_dir()
        dia = time.strftime("%Y-%m-%d")
        path = os.path.join(_BASE, f"atividade-{dia}.log")
        linha = {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "username": username,
            "name": name,
            "role": role,
            "pagina": pagina,
            "ip": ip,
            "atividade": atividade,
            "detalhe": detalhe,
        }
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(linha, ensure_ascii=False) + "\n")
    except Exception:
        pass


def ler(limit=None, dia=None):
    """Lê os eventos (mais recentes primeiro)."""
    eventos = []
    try:
        _ensure_dir()
        pattern = f"atividade-{dia}.log" if dia else "atividade-*.log"
        for path in sorted(glob.glob(os.path.join(_BASE, pattern))):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        eventos.append(json.loads(line))
                    except Exception:
                        pass
    except Exception:
        pass
    eventos.sort(key=lambda e: e.get("ts", ""), reverse=True)
    return eventos[:limit] if limit else eventos


def gerar_html(limit=800, titulo="Relatório de Atividade — SysAva"):
    """Monta um relatório HTML navegável a partir dos logs."""
    eventos = ler(limit=limit)
    rows = []
    for e in eventos:
        rows.append(
            "<tr>"
            f"<td>{html.escape(str(e.get('ts', '')))}</td>"
            f"<td>{html.escape(str(e.get('name') or e.get('username', '')))}</td>"
            f"<td>{html.escape(str(e.get('role', '')))}</td>"
            f"<td>{html.escape(str(e.get('pagina', '')))}</td>"
            f"<td>{html.escape(str(e.get('atividade', '')))}</td>"
            f"<td>{html.escape(str(e.get('detalhe', '')))}</td>"
            f"<td>{html.escape(str(e.get('ip', '')))}</td>"
            "</tr>"
        )
    corpo = "".join(rows) or '<tr><td colspan="7">Nenhum evento registrado.</td></tr>'

    hist = ler_historico(limit=200)
    hrows = []
    for e in hist:
        u = html.escape(str(e.get("url", "")))
        hrows.append(
            "<tr>"
            f"<td>{html.escape(str(e.get('ts', '')))}</td>"
            f"<td>{html.escape(str(e.get('maquina', '')))}</td>"
            f"<td>{html.escape(str(e.get('user', '')))}</td>"
            f"<td>{html.escape(str(e.get('title', '')))}</td>"
            f"<td><a href='{u}' target='_blank' rel='noopener'>{u}</a></td>"
            "</tr>"
        )
    hcorpo = "".join(hrows) or '<tr><td colspan="5">Nenhuma visita registrada.</td></tr>'

    gerado = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""<!DOCTYPE html>
<html lang="pt-br"><head><meta charset="UTF-8"><title>{html.escape(titulo)}</title>
<style>
 body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0e1117; color: #e6e6e6; margin: 20px; }}
 h1 {{ color: #4da3ff; }}
 h2 {{ color: #7fb2ff; margin-top: 34px; }}
 table {{ width: 100%; border-collapse: collapse; }}
 th, td {{ padding: 8px 10px; border-bottom: 1px solid #30363d; text-align: left; font-size: .9em; }}
 th {{ background: #1a73e8; color: #fff; text-transform: uppercase; font-size: .8em; }}
 tr:hover {{ background: #161b22; }}
 a {{ color: #7ee787; }}
 small {{ color: #8b949e; }}
</style></head><body>
<h1>📋 {html.escape(titulo)}</h1>
<p><small>Gerado em {gerado} · {len(eventos)} evento(s) · pasta: {html.escape(_BASE)}</small></p>
<table><thead><tr><th>Quando</th><th>Usuário</th><th>Função</th><th>Página</th><th>Atividade</th><th>Detalhe</th><th>IP</th></tr></thead>
<tbody>{corpo}</tbody></table>

<h2>🌐 Histórico do navegador ({len(hist)})</h2>
<table><thead><tr><th>Quando</th><th>Máquina</th><th>Usuário</th><th>Título</th><th>URL</th></tr></thead>
<tbody>{hcorpo}</tbody></table>
</body></html>"""


def salvar_relatorio_html(limit=800):
    """Grava o relatório HTML na pasta oculta e retorna o caminho."""
    try:
        _ensure_dir()
        path = os.path.join(_BASE, "relatorio.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(gerar_html(limit=limit))
        return path
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Histórico do navegador (coletado pelo agente nos PCs)
# ---------------------------------------------------------------------------
def registrar_historico(maquina, user, items):
    """Grava visitas do navegador (recebidas do agente) no log do dia."""
    try:
        _ensure_dir()
        dia = time.strftime("%Y-%m-%d")
        path = os.path.join(_BASE, f"historico-{dia}.log")
        with open(path, "a", encoding="utf-8") as f:
            for it in items or []:
                linha = {
                    "ts": it.get("ts") or datetime.now().isoformat(timespec="seconds"),
                    "maquina": maquina,
                    "user": user,
                    "url": it.get("url", ""),
                    "title": it.get("title", ""),
                }
                f.write(json.dumps(linha, ensure_ascii=False) + "\n")
    except Exception:
        pass


def ler_historico(limit=300, dia=None):
    eventos = []
    try:
        _ensure_dir()
        pattern = f"historico-{dia}.log" if dia else "historico-*.log"
        for path in sorted(glob.glob(os.path.join(_BASE, pattern))):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        eventos.append(json.loads(line))
                    except Exception:
                        pass
    except Exception:
        pass
    eventos.sort(key=lambda e: e.get("ts", ""), reverse=True)
    return eventos[:limit] if limit else eventos
