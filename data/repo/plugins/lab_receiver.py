from flask import Flask, request, jsonify, render_template_string, send_file, Response, session, redirect
import json
import os
import sys
import time
import shutil
import subprocess
import re
import socket
import logging
import threading
import functools
import secrets
import concurrent.futures
from filelock import FileLock, Timeout
import platform
import requests
import zipfile
import io

app = Flask(__name__)
start_time = time.time()

# --- Memória RAM (Estado Vivo) ---
# Armazena o estado volátil das máquinas para acesso ultra-rápido
LIVE_CACHE = {}

# --- Memória RAM para o Scanner de Rede ---
SCAN_RESULTS = []
IS_SCANNING = False
SCAN_LOCK = threading.Lock()

# Define o caminho absoluto para evitar que o arquivo seja criado em locais inesperados
STATUS_FILE = os.path.join(os.path.dirname(__file__), "lab_status.json")
LOCK_FILE = os.path.join(os.path.dirname(__file__), "lab_status.json.lock")
LOG_FILE = os.path.join(os.path.dirname(__file__), "lab_receiver.log")
ERROR_LOG_FILE = os.path.join(os.path.dirname(__file__), "receiver_errors.log")
SCAN_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "scan_config.json")

# Raiz do projeto (para importar services.database no /api/auth_ra)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# O receiver roda FORA do Streamlit. Carrega credenciais do .env (raiz do projeto
# ou um .env local, ao lado do servidor — modo portátil).
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
except Exception:
    pass
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# --- Descoberta UDP (agentes encontram o servidor mesmo com IP via DHCP) ---
HTTP_PORT = 5000
DISCOVERY_PORT = 5001
DISCOVERY_MAGIC = "SYSAVA_DISCOVER"
DISCOVERY_REPLY = "SYSAVA_SERVER"

# --- Login do professor (painel web do receiver) ---
SECRET_FILE = os.path.join(os.path.dirname(__file__), "receiver_secret.key")

def _get_secret_key():
    try:
        if os.path.exists(SECRET_FILE):
            with open(SECRET_FILE, "r", encoding="utf-8") as f:
                k = f.read().strip()
                if k:
                    return k
        k = secrets.token_hex(32)
        with open(SECRET_FILE, "w", encoding="utf-8") as f:
            f.write(k)
        return k
    except Exception:
        return "sysava-fallback-secret-key"

app.secret_key = _get_secret_key()

ACOES_CONTROLE = [
    "Enviar Alerta Visual",
    "Bloquear Jogos (Fechar Roblox/Loki/Games)",
    "Bloquear Sites (YouTube/Instagram/TikTok/Facebook)",
    "Bloquear Anônimos (Tor)",
    "Atualizar Monitor (baixar e reinstalar)",
    "Bloquear Navegador",
    "Forçar Logoff (Deslogar PC)",
    "Desligar PC (Shutdown)",
    "Reiniciar PC (Restart)",
]

NAV_KEYWORDS = ["chrome", "msedge", "firefox", "brave", "opera", "iexplore", "chromium"]
JOGO_KEYWORDS = ["roblox", "league", "steam", "epicgames", "minecraft", "gta", "fortnite",
                 "valorant", "cs2", "dota", "freefire", "battle.net", "riot", "discord"]

def login_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("monitor_user"):
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper

def _supabase_conf():
    url = (os.environ.get("SUPABASE_URL") or "").rstrip("/")
    key = os.environ.get("SUPABASE_KEY") or ""
    return url, key

def _rest_get(path, params):
    """GET no PostgREST do Supabase. Retorna lista (ou None em erro/offline)."""
    try:
        base, key = _supabase_conf()
        if not base or not key:
            return None
        r = requests.get(base + "/rest/v1/" + path,
                         headers={"apikey": key, "Authorization": "Bearer " + key},
                         params=params, timeout=8)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        log_event(f"Erro REST Supabase: {e}")
    return None

def _rest_insert(table, payload):
    """POST no PostgREST do Supabase (best-effort)."""
    try:
        base, key = _supabase_conf()
        if not base or not key:
            return False
        r = requests.post(base + "/rest/v1/" + table,
                          headers={"apikey": key, "Authorization": "Bearer " + key,
                                   "Content-Type": "application/json", "Prefer": "return=minimal"},
                          json=payload, timeout=8)
        return r.status_code in (200, 201, 204)
    except Exception as e:
        log_event(f"Erro REST insert: {e}")
        return False

def _bcrypt_ok(senha, hashed):
    try:
        import bcrypt
        if not hashed:
            return False
        return bcrypt.checkpw((senha or "").encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False

def _buscar_usuario(user):
    """Busca usuário por username OU ra (e por ilike). Retorna dict ou None."""
    user = (user or "").strip()
    if not user:
        return None
    sel = "username,password,name,role"
    rows = _rest_get("app_users", {"or": f"(username.eq.{user},ra.eq.{user})",
                                   "select": sel, "limit": "1"})
    if not rows:
        rows = _rest_get("app_users", {"username": f"ilike.{user}",
                                       "select": sel, "limit": "1"})
    return rows[0] if rows else None

def _validar_professor(user, senha):
    """Valida login/senha contra o SysAva (via REST) exigindo role teacher/admin."""
    try:
        u = _buscar_usuario(user)
        if not u:
            log_event(f"LOGIN FALHOU (usuario nao encontrado): '{user}'")
            return None
        if not _bcrypt_ok(senha, u.get("password", "")):
            log_event(f"LOGIN FALHOU (senha invalida): usuario '{u.get('username')}'")
            return None
        if u.get("role") not in ("teacher", "admin"):
            log_event(f"LOGIN FALHOU (sem permissao, role={u.get('role')}): '{u.get('username')}'")
            return None
        return u
    except Exception as e:
        log_event(f"Erro no login do painel: {e}")
    return None

# Template HTML moderno para o Dashboard
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>SysAva Lab Monitor</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; margin: 20px; color: #333; }
        .container { max-width: 1200px; margin: auto; }
        h1 { text-align: center; color: #1a73e8; margin: 10px 0 6px; }
        .topbar { text-align: center; margin-bottom: 18px; color: #555; }
        .topbar a { color: #1a73e8; text-decoration: none; }
        .stats { display: flex; gap: 20px; margin-bottom: 24px; }
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); flex: 1; text-align: center; border-top: 5px solid #1a73e8; }
        .card h3 { margin: 0; font-size: 0.9em; text-transform: uppercase; color: #666; }
        .card p { font-size: 2.5em; font-weight: bold; margin: 10px 0 0; color: #1a73e8; }
        .card.warning { border-top-color: #f29900; } .card.warning p { color: #f29900; }
        .card.success { border-top-color: #188038; } .card.success p { color: #188038; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #f0f0f0; }
        th { background: #1a73e8; color: white; font-weight: 500; text-transform: uppercase; font-size: 0.85em; }
        tr:hover { background-color: #f8f9fa; }
        .badge { padding: 4px 10px; border-radius: 20px; font-size: 0.85em; font-weight: bold; display: inline-block; }
        .status-roblox { color: #d93025; background: #fce8e6; }
        .status-games { color: #f29900; background: #fef7e0; }
        .status-social { color: #1a73e8; background: #e8f0fe; }
        .status-anônimo { color: #fff; background: #111; }
        .status-produtivo { color: #188038; background: #e6f4ea; }
        small { color: #777; }
        .toolbar { background: white; border-radius: 12px; padding: 16px; margin: 18px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
        .toolbar select, .toolbar input[type=text] { padding: 9px 10px; border: 1px solid #ccc; border-radius: 8px; font-size: 1em; }
        .toolbar input[type=text] { flex: 1; min-width: 200px; }
        button.go { background: #d93025; color: #fff; border: 0; padding: 10px 18px; border-radius: 8px; font-weight: bold; cursor: pointer; }
        button.refresh { background: #1a73e8; color: #fff; border: 0; padding: 8px 14px; border-radius: 8px; cursor: pointer; text-decoration: none; }
        .flash { padding: 12px 16px; border-radius: 10px; margin-bottom: 14px; font-weight: 600; }
        .flash.ok { background: #e6f4ea; color: #188038; }
        .flash.err { background: #fce8e6; color: #d93025; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖥️ SysAva Lab Monitor</h1>
        <div class="topbar">
            👤 {{ user }} &nbsp;|&nbsp; <a href="/logout">Sair</a> &nbsp;|&nbsp;
            <a href="/relatorios">📋 Relatórios</a> &nbsp;|&nbsp;
            <a href="/setup">⚙️ Instalação/downloads</a> &nbsp;|&nbsp; <a href="/">🔄 Atualizar</a>
        </div>

        {% if flash_ok %}<div class="flash ok">✅ {{ flash_ok }}</div>{% endif %}
        {% if flash_err %}<div class="flash err">⚠️ {{ flash_err }}</div>{% endif %}

        <div class="stats">
            <div class="card"><h3>Total Máquinas</h3><p>{{ total }}</p></div>
            <div class="card warning"><h3>Distrações</h3><p>{{ distractions }}</p></div>
            <div class="card success"><h3>Produtivo</h3><p>{{ produtivo }}</p></div>
        </div>

        <form method="post" action="/control">
            <table>
                <thead>
                    <tr>
                        <th><input type="checkbox" onclick="document.querySelectorAll('.ck').forEach(c=>c.checked=this.checked)"></th>
                        <th>Máquina / IP</th>
                        <th>Aluno (RA)</th>
                        <th>Atividade Atual</th>
                        <th>Categoria</th>
                        <th>Último Sinal</th>
                    </tr>
                </thead>
                <tbody>
                    {% for name, info in machines.items() %}
                    <tr>
                        <td><input class="ck" type="checkbox" name="maquinas" value="{{ name }}"></td>
                        <td><a href="/detalhes?maquina={{ name }}" title="Detalhes">🔎</a> <strong>{{ name }}</strong><br><small>{{ info.ip }}</small></td>
                        <td>{{ alunos.get(name) or info.user }}</td>
                        <td>{{ info.activity }}</td>
                        <td><span class="badge status-{{ info.category|lower }}">{{ info.category }}</span></td>
                        <td>{{ info.last_seen }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>

            <div class="toolbar">
                <strong>Ação:</strong>
                <select name="acao">
                    {% for a in acoes %}<option value="{{ a }}">{{ a }}</option>{% endfor %}
                </select>
                <input type="text" name="msg" placeholder="Mensagem do alerta (opcional)">
                <button class="go" type="submit" onclick="return confirm('Executar a ação nas máquinas selecionadas?')">🚀 Executar nas selecionadas</button>
            </div>
        </form>
    </div>
</body>
</html>
"""

DETALHES_TEMPLATE = """
<!DOCTYPE html><html lang="pt-br"><head><meta charset="UTF-8"><title>Detalhes - {{ maquina }}</title>
<style>
 body { font-family: 'Segoe UI', Arial, sans-serif; background: #0f1420; color: #e6e6e6; margin: 0; padding: 24px; }
 .wrap { max-width: 1000px; margin: auto; }
 h1 { color: #4da3ff; }
 .card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 16px; margin: 14px 0; }
 .cols { display: flex; gap: 16px; flex-wrap: wrap; }
 .col { flex: 1; min-width: 260px; background: #0d1117; border: 1px solid #30363d; border-radius: 10px; padding: 12px; }
 .col h3 { margin: 0 0 8px; font-size: 1em; color: #7fb2ff; }
 ul { margin: 0; padding-left: 18px; } li { font-size: .9em; line-height: 1.6; }
 .kv { color: #8b949e; } .val { color: #fff; }
 a { color: #7ee787; }
 .badge { padding: 3px 9px; border-radius: 12px; background: #1a73e8; color: #fff; font-size: .85em; }
</style></head><body><div class="wrap">
<p><a href="/">← Voltar ao painel</a></p>
<h1>🖥️ {{ maquina }}</h1>
<div class="card">
 <div><span class="kv">Aluno (RA):</span> <span class="val">{{ aluno or info.user }}</span> &nbsp; <span class="kv">IP:</span> <span class="val">{{ info.ip }}</span></div>
 <div><span class="kv">Janela ativa:</span> <span class="val">{{ info.activity }}</span></div>
 <div><span class="kv">Categoria:</span> <span class="badge">{{ info.category }}</span> &nbsp; <span class="kv">Último sinal:</span> <span class="val">{{ info.last_seen }}</span></div>
 <div><span class="kv">Portas:</span> <span class="val">{{ info.ports }}</span></div>
</div>
<div class="cols">
 <div class="col"><h3>🌐 Navegadores ({{ nav|length }})</h3><ul>{% for p in nav %}<li>{{ p }}</li>{% endfor %}{% if not nav %}<li class="kv">nenhum</li>{% endif %}</ul></div>
 <div class="col"><h3>🎮 Jogos ({{ jog|length }})</h3><ul>{% for p in jog %}<li>{{ p }}</li>{% endfor %}{% if not jog %}<li class="kv">nenhum</li>{% endif %}</ul></div>
 <div class="col"><h3>⚙️ Outros processos ({{ outros|length }})</h3><ul>{% for p in outros %}<li>{{ p }}</li>{% endfor %}</ul></div>
</div>
</div></body></html>
"""

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>SysAva Lab Monitor - Login</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0e1117; color: #e6e6e6; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .box { background: #161b22; border: 1px solid #30363d; border-radius: 14px; padding: 30px; width: 360px; box-shadow: 0 10px 30px rgba(0,0,0,0.4); }
        h2 { margin: 0 0 18px; color: #4da3ff; text-align: center; }
        label { display: block; font-size: .9em; color: #8b949e; margin: 10px 0 4px; }
        input { width: 100%; padding: 11px; border: 1px solid #30363d; border-radius: 8px; background: #0d1117; color: #fff; font-size: 1em; box-sizing: border-box; }
        button { width: 100%; margin-top: 18px; padding: 12px; border: 0; border-radius: 8px; background: #1f6feb; color: #fff; font-weight: bold; font-size: 1em; cursor: pointer; }
        .err { color: #ff7b72; text-align: center; margin-top: 12px; min-height: 18px; }
        small { color: #8b949e; display: block; text-align: center; margin-top: 14px; }
    </style>
</head>
<body>
    <form class="box" method="post" action="/login">
        <h2>🖥️ SysAva Lab Monitor</h2>
        <label>Usuário (login ou RA)</label>
        <input type="text" name="user" autofocus>
        <label>Senha</label>
        <input type="password" name="senha">
        <button type="submit">Entrar</button>
        <div class="err">{{ erro }}</div>
        <small>Acesso restrito a professores e administradores.</small>
    </form>
</body>
</html>
"""


# Arquivos liberados para download/atualizacao nas maquinas clientes
DOWNLOAD_WHITELIST = {
    "lab_agent.ps1": "Instalador do agente de monitoramento",
    "bloquear_hosts.ps1": "Bloqueio nao invasivo via hosts (script)",
    "bloquear_hosts.bat": "Bloqueio nao invasivo via hosts (duplo-clique)",
    "logo_sysava.png": "Logo do SysAva",
    "wallpaper_sysava.png": "Papel de parede do SysAva",
    "sysava_lock.ps1": "Tela de bloqueio (script)",
    "aplicar_papel_parede.ps1": "Aplica o papel de parede",
    "instalar_tela_sysava.ps1": "Instala a tela de bloqueio + papel de parede",
    "aplicar_dns_seguro.ps1": "DNS de filtro (protecao: adulto/malware)",
    "INICIAR_SERVIDOR.bat": "Servidor portatil - iniciar (duplo-clique)",
    "INICIAR_SERVIDOR.ps1": "Servidor portatil - script de bootstrap",
    "config.env.example": "Modelo de configuracao do servidor portatil",
}

SETUP_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>SysAva - Instalacao nas maquinas</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0e1117; color: #e6e6e6; margin: 0; padding: 24px; }
        .wrap { max-width: 860px; margin: auto; }
        h1 { color: #4da3ff; }
        .ip { background: #1a73e8; color: #fff; padding: 8px 14px; border-radius: 8px; display: inline-block; font-size: 1.15em; font-weight: bold; }
        .card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 18px; margin: 14px 0; }
        .card h2 { margin: 0 0 8px; font-size: 1.1em; }
        a.btn { display: inline-block; background: #238636; color: #fff; padding: 10px 16px; border-radius: 8px; text-decoration: none; margin: 6px 8px 0 0; font-weight: 600; }
        a.btn.blue { background: #1f6feb; }
        a.btn.gray { background: #30363d; }
        code { background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 2px 6px; color: #7ee787; }
        pre { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 12px; overflow-x: auto; color: #7ee787; }
        small { color: #8b949e; }
    </style>
</head>
<body>
    <div class="wrap">
        <h1>🖥️ SysAva — Instalar / Atualizar máquinas clientes</h1>
        <p>Servidor de arquivos: <span class="ip">http://{{ host }}</span></p>
        <p><small>Deixe este servidor ligado. Os arquivos sao lidos do disco a cada download — baixar de novo ja traz a versao mais recente (<b>atualizacao</b>).</small></p>

        <div class="card">
            <h2>1) Agente de monitoramento (instala e atualiza)</h2>
            <p>Instala o Python portatil, as dependencias e o agente. Rodar de novo <b>atualiza</b> o agente (a instancia antiga e encerrada automaticamente).</p>
            <a class="btn" href="/instalar_agente.bat">Instalador automatico (.bat)</a>
            <a class="btn blue" href="/download/lab_agent.ps1">lab_agent.ps1</a>
            <p><small>Ou, no PC cliente, abra o PowerShell como Administrador e cole:</small></p>
            <pre>powershell -NoProfile -ExecutionPolicy Bypass -Command "iwr http://{{ host }}/download/lab_agent.ps1 -OutFile $env:TEMP\\lab_agent.ps1 -UseBasicParsing; & $env:TEMP\\lab_agent.ps1"</pre>
        </div>

        <div class="card">
            <h2>2) Bloqueio nao invasivo (sem instalar nada)</h2>
            <p>Bloqueia o Roblox pelo arquivo <code>hosts</code> do Windows. Duplo-clique, pede Administrador.</p>
            <a class="btn" href="/instalar_hosts.bat">Aplicar bloqueio (.bat)</a>
            <a class="btn blue" href="/download/bloquear_hosts.ps1">bloquear_hosts.ps1</a>
            <a class="btn gray" href="/download/bloquear_hosts.bat">bloquear_hosts.bat</a>
            <p><small>Para remover depois: rode o <code>bloquear_hosts.ps1</code> com <code>-Revert</code>.</small></p>
        </div>

        <div class="card">
            <h2>3) Tela de bloqueio + Papel de parede</h2>
            <p>Aplica a marca do SysAva (papel de parede + tela de bloqueio) e uma tela que abre no logon, abre o <b>sysava.streamlit.app</b> e pede o <b>RA</b> do aluno para liberar. Requer Administrador.</p>
            <a class="btn" href="/instalar_tela.bat">Instalar tela de bloqueio (.bat)</a>
            <a class="btn blue" href="/download/instalar_tela_sysava.ps1">instalar_tela_sysava.ps1</a>
            <a class="btn gray" href="/download/wallpaper_sysava.png">wallpaper_sysava.png</a>
            <a class="btn gray" href="/download/logo_sysava.png">logo_sysava.png</a>
            <p><small>Para desfazer a tela de bloqueio: rebaixe o .bat com o par&acirc;metro <code>-Remover</code> (ou rode <code>instalar_tela_sysava.ps1 -Remover</code>).</small></p>
        </div>

        <div class="card">
            <h2>4) Proteção (DNS de filtro)</h2>
            <p>Define um DNS de família que bloqueia <b>conteúdo adulto e malware</b> (Cloudflare for Families) neste PC. Ideal: aplicar o mesmo DNS no <b>roteador/DHCP</b> do laboratório para valer em todas as máquinas.</p>
            <a class="btn" href="/instalar_dns.bat">Aplicar DNS de filtro (.bat)</a>
            <a class="btn blue" href="/download/aplicar_dns_seguro.ps1">aplicar_dns_seguro.ps1</a>
            <p><small>Para desfazer: rode o <code>aplicar_dns_seguro.ps1 -Revert</code>.</small></p>
        </div>

        <div class="card">
            <h2>5) Acompanhar as maquinas</h2>
            <a class="btn blue" href="/">Maquinas conectadas</a>
            <a class="btn gray" href="/diagnostics">Diagnostico da rede</a>
        </div>

        <div class="card">
            <h2>6) Servidor portatil (outro PC sempre ligado)</h2>
            <p>Para hospedar o monitor em um PC fixo (sem depender do notebook): copie a pasta <code>plugins</code> para o PC, crie um <code>.env</code> (modelo abaixo) e rode o <b>INICIAR_SERVIDOR.bat</b>. Ele baixa um Python portatil, instala as dependencias, abre o firewall e sobe o servidor.</p>
            <a class="btn" href="/download/INICIAR_SERVIDOR.bat">INICIAR_SERVIDOR.bat</a>
            <a class="btn blue" href="/download/INICIAR_SERVIDOR.ps1">INICIAR_SERVIDOR.ps1</a>
            <a class="btn gray" href="/download/config.env.example">config.env.example</a>
            <a class="btn" href="/servidor.zip">📦 servidor.zip (tudo)</a>
            <p><small>Ou rode só o <b>INICIAR_SERVIDOR.bat</b> na pasta nova: ele pergunta a URL de origem (ex.: <code>http://&lt;ip&gt;:5000</code>) e baixa tudo sozinho.</small></p>
        </div>
    </div>
</body>
</html>
"""

def get_my_mac():
    """Obtem o MAC Address da interface ativa para facilitar a configuracao dos agentes."""
    try:
        output = subprocess.check_output("getmac", text=True)
        # Busca o primeiro padrão de MAC encontrado (XX-XX-XX-XX-XX-XX)
        match = re.search(r"([0-9A-F]{2}-){5}[0-9A-F]{2}", output, re.I)
        if match: return match.group(0).upper()
    except:
        pass
    return "N/A (Verifique via ipconfig /all)"

def log_event(message):
    """Salva eventos importantes no arquivo de log."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_FILE, "a", encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
    except: pass

def run_udp_discovery():
    """Escuta pedidos de descoberta e responde com o endereço do servidor.
    Permite que os agentes achem o notebook do professor mesmo se o IP mudar (DHCP)."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    try:
        sock.bind(("", DISCOVERY_PORT))
    except OSError as e:
        log_event(f"UDP discovery indisponivel na porta {DISCOVERY_PORT}: {e}")
        return
    log_event(f"UDP discovery ativo na porta {DISCOVERY_PORT}.")
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if data.decode(errors="ignore").strip() == DISCOVERY_MAGIC:
                reply = f"{DISCOVERY_REPLY} {get_local_ip()}:{HTTP_PORT}"
                sock.sendto(reply.encode(), addr)
        except Exception:
            time.sleep(0.5)

def load_data():
    """Lê os dados com proteção contra JSON corrompido."""
    lock = FileLock(LOCK_FILE, timeout=1)
    try:
        with lock:
            if not os.path.exists(STATUS_FILE):
                return {}
            with open(STATUS_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content:
                    return {}
                return json.loads(content)
    except (Timeout, json.JSONDecodeError, IOError, OSError):
        # Se o arquivo estiver bloqueado, corrompido ou houver erro de IO, retorna vazio
        return {}

def save_data(data):
    """Grava os dados de forma atômica (escreve em temp e depois substitui)."""
    lock = FileLock(LOCK_FILE, timeout=1)
    try:
        with lock:
            with open(STATUS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
    except (Timeout, IOError, OSError) as e:
        log_event(f"Erro de IO ou Timeout ao salvar dados: {e}")

def get_local_ip():
    """Obtém o IP do servidor para identificar a rede do laboratório."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Não precisa conectar de verdade, apenas para o SO escolher a interface
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_local_ipv6():
    """Tenta obter o endereço IPv6 Link-Local."""
    try:
        s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        # Conecta a um endereço global fictício para forçar o SO a escolher a interface
        s.connect(('2001:4860:4860::8888', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Indisponível"

# --- Funções do Scanner de Rede (integradas do lab_sniffer.py) ---

def check_host(ip):
    """
    Verifica se um host está ativo e tenta identificar se é um servidor SysAva.
    Retorna um dicionário com os detalhes do host ou None.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-w', '500', ip]
    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            details = {"ip": ip, "status": "ATIVO", "mac": "N/A"}
            try:
                with socket.create_connection((ip, 5000), timeout=0.5):
                    details["status"] = "🚀 SERVIDOR SYSAVA"
            except (socket.timeout, ConnectionRefusedError):
                pass
            
            # Tenta obter o MAC Address de forma mais robusta
            try:
                arp_output = subprocess.check_output(['arp', '-a', ip], text=True)
                mac_match = re.search(r"([0-9a-f]{2}[:-]){5}[0-9a-f]{2}", arp_output, re.I)
                if mac_match:
                    details["mac"] = mac_match.group(0).upper()
                else:
                    # Fallback: Se o arp para um IP específico falhar, busca na tabela geral
                    arp_output_general = subprocess.check_output(['arp', '-a'], text=True)
                    # Procura uma linha que contenha o IP exato
                    for line in arp_output_general.splitlines():
                        if ip in line:
                            mac_match_general = re.search(r"([0-9a-f]{2}[:-]){5}[0-9a-f]{2}", line, re.I)
                            if mac_match_general:
                                details["mac"] = mac_match_general.group(0).upper()
                                break
            except Exception:
                pass # Se o comando arp falhar, mantém "N/A"
            return details
    except:
        pass
    return None

def run_network_scan_thread():
    """Função que executa a varredura em background."""
    global SCAN_RESULTS, IS_SCANNING
    
    # Carrega sub-redes extras de um arquivo de configuração
    extra_subnets = []
    if os.path.exists(SCAN_CONFIG_FILE):
        with open(SCAN_CONFIG_FILE, 'r') as f:
            config = json.load(f)
            extra_subnets = config.get("additional_subnets", [])
    else:
        # Cria o arquivo com valores padrão se não existir
        with open(SCAN_CONFIG_FILE, 'w') as f:
            json.dump({"additional_subnets": ["192.168.10.", "192.168.11."]}, f, indent=4)
        extra_subnets = ["192.168.10.", "192.168.11."]

    local_ip = get_local_ip()
    # Combina a sub-rede local com as extras, sem duplicatas
    subnets_to_scan = list(set([ ".".join(local_ip.split('.')[:-1]) + "." ] + extra_subnets))

    for subnet in subnets_to_scan:
        ips_to_scan = [f"{subnet}{i}" for i in range(1, 255)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            for result in executor.map(check_host, ips_to_scan):
                if result:
                    SCAN_RESULTS.append(result)
    IS_SCANNING = False

@app.route('/favicon.ico')
def favicon():
    """Silencia o erro 404 do navegador procurando por ícone."""
    return '', 204

@app.route('/setup')
@app.route('/instalar')
def setup_page():
    """Pagina de instalacao/atualizacao para as maquinas clientes."""
    return render_template_string(SETUP_TEMPLATE, host=request.host)

@app.route('/download/<path:name>')
def download_file(name):
    """Entrega apenas os arquivos liberados (evita expor qualquer arquivo da pasta)."""
    safe = os.path.basename(name)
    if safe not in DOWNLOAD_WHITELIST:
        return jsonify({"status": "error", "message": "Arquivo nao permitido."}), 404
    path = os.path.join(os.path.dirname(__file__), safe)
    if not os.path.exists(path):
        return jsonify({"status": "error", "message": "Arquivo nao encontrado."}), 404
    return send_file(path, as_attachment=True, download_name=safe)

def _make_install_bat(script_name, title, extra_args=None):
    """Gera um .bat que baixa o script deste servidor e o executa como Administrador."""
    extra = ""
    for a in (extra_args or []):
        extra += ",'" + a.replace("'", "''") + "'"
    ps = (
        f"$u='http://{request.host}/download/{script_name}'; "
        f"$p=Join-Path $env:TEMP '{script_name}'; "
        "Invoke-WebRequest -Uri $u -OutFile $p -UseBasicParsing; "
        "Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File',$p" + extra
    )
    body = (
        "@echo off\r\n"
        f"title {title}\r\n"
        "powershell -NoProfile -ExecutionPolicy Bypass -Command \"" + ps + "\"\r\n"
    )
    return Response(
        body,
        mimetype="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={script_name[:-4]}.bat"},
    )

@app.route('/instalar_agente.bat')
def instalar_agente_bat():
    return _make_install_bat("lab_agent.ps1", "SysAva - Instalar/Atualizar Agente")

@app.route('/instalar_hosts.bat')
def instalar_hosts_bat():
    return _make_install_bat("bloquear_hosts.ps1", "SysAva - Bloqueio via Hosts")

@app.route('/instalar_tela.bat')
def instalar_tela_bat():
    return _make_install_bat("instalar_tela_sysava.ps1", "SysAva - Tela de Bloqueio",
                             ["-Server", f"http://{request.host}"])

@app.route('/instalar_dns.bat')
def instalar_dns_bat():
    return _make_install_bat("aplicar_dns_seguro.ps1", "SysAva - DNS de Filtro (Protecao)")

SERVIDOR_ZIP_ITENS = [
    "lab_receiver.py", "audit_log.py", "INICIAR_SERVIDOR.ps1", "INICIAR_SERVIDOR.bat",
    "config.env.example", "lab_agent.ps1", "bloquear_hosts.ps1", "bloquear_hosts.bat",
    "instalar_tela_sysava.ps1", "sysava_lock.ps1", "aplicar_papel_parede.ps1",
    "aplicar_dns_seguro.ps1", "logo_sysava.png", "wallpaper_sysava.png", "blocked_apps.json",
    "gerar_logo_sysava.py",
]

@app.route('/servidor.zip')
def servidor_zip():
    """Empacota o servidor portatil (para baixar/copiar em outro PC)."""
    base = os.path.dirname(os.path.abspath(__file__))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name in SERVIDOR_ZIP_ITENS:
            p = os.path.join(base, name)
            if os.path.exists(p):
                z.write(p, name)
        catdir = os.path.join(base, "categorias")
        if os.path.isdir(catdir):
            for f in os.listdir(catdir):
                fp = os.path.join(catdir, f)
                if os.path.isfile(fp):
                    z.write(fp, "categorias/" + f)
    buf.seek(0)
    return Response(buf.read(), mimetype="application/zip",
                    headers={"Content-Disposition": "attachment; filename=servidor_sysava.zip"})

@app.route('/diagnostics')
@login_required
def diagnostics():
    """Página de detalhes para depuração do sistema em tempo real."""
    try:
        now = time.time()
        # Cria uma cópia para evitar RuntimeError: dictionary changed size during iteration
        cache_snapshot = dict(LIVE_CACHE) 
        
        diagnostics_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>SysAva - Diagnóstico de Rede</title>
            <meta http-equiv="refresh" content="2">
            <style>
                body { font-family: monospace; background: #0e1117; color: #00ff41; padding: 20px; }
                .header { border-bottom: 1px solid #00ff41; margin-bottom: 20px; padding-bottom: 10px; }
                .cache-item { margin-bottom: 10px; padding: 10px; border: 1px solid #333; }
                .scan-item { color: #92e8ff; }
                .scan-item.server { color: #ff79c6; font-weight: bold; }
                .timestamp { color: #888; }
                .latency { color: #ffeb3b; }
                button { background: #00ff41; border: none; padding: 10px 15px; color: #0e1117; font-weight: bold; cursor: pointer; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📡 SysAva Server Diagnostics</h1>
                <p>Uptime: {{ uptime }}s | IP Servidor: {{ ip }} | Itens na RAM: {{ count }}</p>
            </div>

            <h2>🌐 Scanner de Rede</h2>
            <form action="/scan" method="post" onsubmit="document.getElementById('scan-btn').innerText='Escaneando...'; document.getElementById('scan-btn').disabled=true;">
                <button id="scan-btn" type="submit" {% if is_scanning %}disabled{% endif %}>
                    {% if is_scanning %}Escaneando...{% else %}Iniciar Varredura de Rede{% endif %}
                </button>
            </form>
            <div id="scan-results">
                {% for host in scan_results %}
                    <div class="scan-item {% if 'SERVIDOR' in host.status %}server{% endif %}">
                        [+] Host: {{ host.ip.ljust(15) }} | Status: {{ host.status.ljust(18) }} | MAC: {{ host.mac }}
                    </div>
                {% endfor %}
            </div>

            <br>
            <h2>⚙️ Cache de Atividade (Agentes)</h2>
            <div id="logs">
                {% for name, info in cache.items() %}
                <div class="cache-item">
                    <strong>{{ name }}</strong> -> IP: {{ info.ip }} | 
                    <span class="latency">Atraso: {{ "%.2f"|format(now - info.timestamp) }}s</span><br>
                    <span class="timestamp">Último dado: {{ info }}</span>
                </div>
                {% endfor %}
            </div>
        </body>
        </html>
        """
        return render_template_string(
            diagnostics_html, 
            cache=cache_snapshot, 
            uptime=int(time.time() - start_time), 
            ip=get_local_ip(),
            count=len(LIVE_CACHE),
            now=now,
            is_scanning=IS_SCANNING,
            scan_results=SCAN_RESULTS
        )
    except Exception as e:
        # Registra o erro no log do Flask (geralmente console) e retorna um 500 com detalhes
        app.logger.error(f"Erro ao renderizar página de diagnóstico: {e}", exc_info=True)
        return f"<h1>Erro Interno do Servidor (500)</h1><p>Detalhes: {e}</p>", 500

@app.route('/update_scan_config', methods=['POST'])
def update_scan_config():
    """Atualiza o arquivo de configuração de sub-redes."""
    try:
        subnets_text = request.form.get('subnets', '')
        # Converte o texto (separado por vírgula ou nova linha) em uma lista limpa
        subnets_list = [s.strip() for s in re.split(r'[,\n]', subnets_text) if s.strip()]
        
        with open(SCAN_CONFIG_FILE, 'w') as f:
            json.dump({"additional_subnets": subnets_list}, f, indent=4)
    except Exception as e:
        app.logger.error(f"Erro ao atualizar scan_config.json: {e}")
    return '<script>window.location.href = "/diagnostics";</script><h1>Configuração salva. Redirecionando...</h1>'

@app.route('/scan', methods=['POST'])
def start_scan():
    """Endpoint para iniciar a varredura de rede em background."""
    global IS_SCANNING, SCAN_RESULTS
    
    with SCAN_LOCK:
        if not IS_SCANNING:
            IS_SCANNING = True
            SCAN_RESULTS = []
            scan_thread = threading.Thread(target=run_network_scan_thread, daemon=True)
            scan_thread.start()
            app.logger.info("Iniciando varredura de rede em background.")
        else:
            app.logger.warning("Tentativa de iniciar varredura enquanto outra já está em andamento.")
    return '<script>setTimeout(function(){ window.location.href = "/diagnostics"; }, 1000);</script><h1>Varredura iniciada... Redirecionando.</h1>'

@app.route('/api/diagnostics', methods=['GET'])
def get_diagnostics_data():
    """Endpoint que retorna os dados de diagnóstico em JSON para integração."""
    cache_snapshot = dict(LIVE_CACHE)
    return jsonify({
        "uptime": int(time.time() - start_time),
        "server_ip": get_local_ip(),
        "cache_count": len(LIVE_CACHE),
        "is_scanning": IS_SCANNING,
        "scan_results": SCAN_RESULTS,
        "live_cache": cache_snapshot,
        "server_timestamp": time.time()
    })

@app.route('/api/debug', methods=['GET'])
def get_debug_raw():
    """Retorna a RAM bruta para auditoria externa."""
    return jsonify({
        "server_time": time.time(),
        "ram_cache": LIVE_CACHE
    })

@app.route('/api/status', methods=['GET'])
def get_live_status():
    """Endpoint de alta velocidade para o Radar do SysAva."""
    now = time.time()
    # Filtra apenas máquinas que deram sinal nos últimos 30 segundos para o Radar Vivo
    active_now = {
        name: info for name, info in LIVE_CACHE.items() 
        if (now - info.get('timestamp', 0)) < 30
    }
    return jsonify(active_now)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """Login do professor para o painel web (valida contra o SysAva)."""
    erro = ""
    if request.method == 'POST':
        user = (request.form.get('user') or '').strip()
        senha = request.form.get('senha') or ''
        u = _validar_professor(user, senha)
        if u:
            session['monitor_user'] = u.get('name') or user
            session['monitor_login'] = u.get('username') or user
            log_event(f"LOGIN PAINEL: {session['monitor_login']} ({session['monitor_user']})")
            return redirect('/')
        erro = "Usuário ou senha inválidos (ou sem permissão)."
    return render_template_string(LOGIN_TEMPLATE, erro=erro)

@app.route('/logout')
def logout_page():
    log_event(f"LOGOUT PAINEL: {session.get('monitor_login')}")
    session.clear()
    return redirect('/login')

@app.route('/control', methods=['POST'])
@login_required
def control():
    """Executa uma ação nas máquinas selecionadas (grava o comando para o agente)."""
    acao = (request.form.get('acao') or '').strip()
    msg = (request.form.get('msg') or '').strip()
    maquinas = request.form.getlist('maquinas')
    if not maquinas or not acao:
        return redirect('/?erro=Selecione+ao+menos+uma+máquina+e+uma+ação')
    data = load_data()
    ts = time.strftime("%H:%M:%S")
    enviados = 0
    for m in maquinas:
        if m in data:
            data[m]['pending_command'] = acao
            data[m]['command_msg'] = msg
            data[m]['command_ts'] = ts
            enviados += 1
    save_data(data)
    quem = session.get('monitor_user', '?')
    log_event(f"COMANDO WEB '{acao}' para {enviados} maquina(s) por {quem}")
    return redirect(f"/?ok=Comando+'{acao}'+enviado+para+{enviados}+máquina(s)")

@app.route('/detalhes')
@login_required
def detalhes():
    """Detalhes de uma máquina: navegadores, jogos e demais processos em atividade."""
    maquina = request.args.get('maquina', '')
    data = load_data().get(maquina)
    if not data:
        return redirect('/?erro=Máquina+nao+encontrada+ou+offline')
    procs = data.get('procs') or []
    nav = [p for p in procs if any(k in p for k in NAV_KEYWORDS)]
    jog = [p for p in procs if any(k in p for k in JOGO_KEYWORDS)]
    outros = [p for p in procs if p not in nav and p not in jog]
    u = _load_users_map().get(maquina)
    aluno = ""
    if u:
        nm = (u.get('name') or '').strip()
        ra = (u.get('ra') or '').strip()
        aluno = (f"{nm} ({ra})" if nm and ra else (nm or ra)).strip()
    return render_template_string(DETALHES_TEMPLATE, maquina=maquina, info=data,
                                  nav=nav, jog=jog, outros=outros[:120], aluno=aluno)

@app.route('/relatorios')
@login_required
def relatorios():
    """Relatório de atividade dos usuários (IS-071) — lido da pasta oculta .relatorios."""
    a = _audit()
    if not a:
        return "<h1>Relatório indisponível</h1>", 500
    return a.gerar_html(limit=800)

@app.route('/')
@login_required
def dashboard():
    """Painel web com status das máquinas e controles."""
    raw_data = load_data()

    filtered_machines = {}
    now = time.time()

    # Filtra máquinas: Devem ter sinal nos últimos 5 minutos (300s)
    for name, info in raw_data.items():
        timestamp = info.get('timestamp', 0)
        if (now - timestamp) < 300:
            filtered_machines[name] = info

    total = len(filtered_machines)
    produtivo = sum(1 for m in filtered_machines.values() if m.get('category') == 'Produtivo')
    distractions = total - produtivo

    # Aluno identificado pela tela de bloqueio (lab_users.json) — a conta Windows e' sempre "ALUNO"
    users_map = _load_users_map()
    alunos = {}
    for name in filtered_machines:
        u = users_map.get(name)
        if u:
            nm = (u.get('name') or '').strip()
            ra = (u.get('ra') or '').strip()
            alunos[name] = (f"{nm} ({ra})" if nm and ra else (nm or ra)).strip()

    return render_template_string(
        DASHBOARD_TEMPLATE,
        machines=filtered_machines, total=total,
        produtivo=produtivo, distractions=distractions,
        user=session.get('monitor_user', ''),
        acoes=ACOES_CONTROLE,
        alunos=alunos,
        flash_ok=request.args.get('ok', ''),
        flash_err=request.args.get('erro', ''),
    )

@app.route('/health', methods=['GET'])
def health():
    """Rota simples para verificar se o servidor está online."""
    data = load_data()
    return jsonify({
        "status": "online",
        "uptime_seconds": int(time.time() - start_time),
        "machines_connected": len(data),
        "file_path": STATUS_FILE,
        "file_exists": os.path.exists(STATUS_FILE)
    }), 200

_RA_CACHE = {}

def _audit():
    """Usa o audit_log local (portátil) e, se não houver, o do services."""
    try:
        import audit_log as a
        return a
    except Exception:
        try:
            if PROJECT_ROOT not in sys.path:
                sys.path.insert(0, PROJECT_ROOT)
            from services import audit_log as a
            return a
        except Exception:
            return None
_MAQ_USERS_FILE = os.path.join(os.path.dirname(__file__), "lab_users.json")

def _load_users_map():
    if os.path.exists(_MAQ_USERS_FILE):
        try:
            with open(_MAQ_USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_users_map(data):
    try:
        with open(_MAQ_USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        log_event(f"Erro ao salvar lab_users.json: {e}")

def _label_for(maquina):
    """Rótulo amigável da máquina (lab_labels.json) para o histórico."""
    try:
        p = os.path.join(os.path.dirname(__file__), "lab_labels.json")
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f).get(maquina, maquina)
    except Exception:
        pass
    return maquina

def _associar_usuario_maquina(maquina, ra, name):
    if not maquina:
        return
    data = _load_users_map()
    prev = data.get(maquina) or {}
    today = time.strftime("%Y-%m-%d")
    ja_logado_hoje = (prev.get('ra') == ra and prev.get('logged_date') == today)

    entry = {"ra": ra, "name": name, "ts": time.time()}
    if ja_logado_hoje:
        entry["logged_date"] = prev.get('logged_date')
    else:
        entry["logged_date"] = today
    data[maquina] = entry
    _save_users_map(data)
    log_event(f"USUARIO ASSOCIADO: {maquina} -> {name} ({ra})")

    # Registra no histórico do aluno (no máximo 1x por aluno/maquina/dia)
    if not ja_logado_hoje:
        label = _label_for(maquina)
        ok = _rest_insert("user_history", {"username": ra, "activity": f"Entrou no {label} (tela de bloqueio)"})
        if not ok:
            log_event(f"Historico de {ra} nao gravado (REST offline?).")

@app.route('/api/auth_ra')
def auth_ra():
    """Valida o RA no SysAva e associa o aluno a maquina (tela de bloqueio).
    Modo simplificado: valida apenas o RA (sem senha)."""
    ra = (request.args.get('ra') or '').strip()
    maquina = (request.args.get('maquina') or '').strip()
    if not ra:
        return jsonify({"ok": False, "error": "Informe o RA."}), 400

    if ra in _RA_CACHE:
        name = _RA_CACHE[ra]
        _associar_usuario_maquina(maquina, ra, name)
        return jsonify({"ok": True, "name": name})

    u = _buscar_usuario(ra)
    if u:
        name = u.get('name') or ra
        _RA_CACHE[ra] = name
        _associar_usuario_maquina(maquina, ra, name)
        return jsonify({"ok": True, "name": name, "role": u.get('role', 'student')})
    return jsonify({"ok": False, "error": "RA nao encontrado."}), 404

@app.route('/api/historico', methods=['POST'])
def api_historico():
    """Recebe o histórico do navegador enviado pelos agentes (IS-071)."""
    data = request.json or {}
    maquina = data.get('maquina', '?')
    user = data.get('user', '')
    items = data.get('items', [])
    if not items:
        return jsonify({"status": "ok", "received": 0})
    a = _audit()
    if a:
        a.registrar_historico(maquina, user, items)
    return jsonify({"status": "ok", "received": len(items)})

@app.route('/ping', methods=['POST'])
def ping():
    data = request.json
    if not data or "maquina" not in data:
        return jsonify({"status": "error", "message": "Dados inválidos"}), 400
        
    maquina_name = data.get('maquina')
    now = time.time()
    
    # 1. Atualiza Memória RAM (Prioridade 1)
    data['timestamp'] = now
    LIVE_CACHE[maquina_name] = data
    
    # 2. Log de Manutenção (Prioridade 2)
    if LIVE_CACHE.get(maquina_name, {}).get('category') != data.get('category'):
        log_event(f"MUDANÇA DE ESTADO: {maquina_name} -> {data.get('category')}")

    # 3. Persistência de Vigilância (Prioridade 3)
    # Salva no JSON apenas para registro histórico/auditoria
    # (Pode ser otimizado para salvar em lote a cada X minutos)
    db_data = load_data()
    
    # Recupera comandos antes de atualizar para não perdê-los
    pending = db_data.get(maquina_name, {}).get("pending_command")
    msg = db_data.get(maquina_name, {}).get("command_msg")
    
    db_data[maquina_name] = data
    save_data(db_data)
    
    # Retorna comandos pendentes para o agente
    response = {"status": "ok"}
    if pending:
        response["pending_command"] = pending
        response["command_msg"] = msg
        
        # Limpa o comando no arquivo para evitar repetição
        db_data[maquina_name]["pending_command"] = None
        save_data(db_data)
        
    return jsonify(response)

if __name__ == '__main__':
    # --- Configuração de Logging Inteligente ---
    # Remove o logger padrão do Flask para evitar duplicação
    if app.logger.handlers:
        app.logger.removeHandler(app.logger.handlers[0])

    # Configura o logger de ACESSO para ir para lab_receiver.log
    access_logger = logging.getLogger('werkzeug')
    access_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    access_logger.addHandler(access_handler)

    # Configura o logger de ERROS para ir para receiver_errors.log
    error_handler = logging.FileHandler(ERROR_LOG_FILE, encoding='utf-8')
    error_handler.setLevel(logging.ERROR) # Captura apenas ERROR e CRITICAL
    app.logger.addHandler(error_handler)

    # threaded=True permite que o Flask lide com múltiplas requisições ao mesmo tempo
    # --- Verificação de Porta ---
    # Adicionamos uma verificação de porta mais confiável aqui
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('localhost', 5000)) == 0:
            print("[ERRO] A porta 5000 já está em uso. O receptor não pode iniciar.")
            app.logger.critical("PORTA 5000 JÁ EM USO.")
            # Saímos com um código de erro para o .bat não tentar reiniciar
            exit(1)


    print("\n" + "="*50)
    print("🚀 SysAva Receiver v2 (RAM + Diagnostics) Online")
    print(f"📍 Endereco MAC: {get_my_mac()}")
    print(f"🔗 Rota IPv4: http://{get_local_ip()}:5000/diagnostics")
    print(f"🔗 Rota IPv6: http://[{get_local_ipv6()}]:5000/diagnostics")
    print("� Use este MAC no 'lab_agent.py' para busca automatica.")
    print("="*50 + "\n")
    
    # Rodar em '::' permite conexões IPv4 e IPv6 simultâneas
    # Usamos Waitress como um servidor de produção mais robusto para Windows
    # Inicia o respondedor de descoberta UDP (broadcast) em segundo plano
    threading.Thread(target=run_udp_discovery, daemon=True).start()

    try:
        from waitress import serve
        serve(app, host='0.0.0.0', port=5000)
    except ImportError:
        print("[AVISO] waitress nao instalado; usando o servidor embutido do Flask.")
        print("[DICA] Para producao: pip install waitress")
        app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)