<#
.SYNOPSIS
    Instalador Standalone do Agente de Monitoramento SysAva.
    Autorizaao: admin
#>

$ErrorActionPreference = "Stop"

# --- AUTO-ELEVAO (SOLICITA ADMIN) ---
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host " Solicitando privilgios de Administrador..." -ForegroundColor Yellow
    $argList = "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    try {
        Start-Process powershell -ArgumentList $argList -Verb RunAs
    } catch {
        Write-Error "O script precisa ser executado como Administrador para instalar softwares e monitorar portas."
    }
    exit
}

# --- CONFIGURAO ---
$SERVER_IP = "192.168.1.100" # <--- ALTERE PARA O IP DO SEU PC (PROFESSOR)
$INSTALL_DIR = "C:\Local\SysVa_lab"
$PYTHON_DIR = Join-Path $INSTALL_DIR ".venv"
$LOG_PATH = Join-Path $INSTALL_DIR "agent_runtime.log"
$PYTHON_ZIP_URL = "https://www.python.org/ftp/python/3.13.1/python-3.13.1-embed-amd64.zip"
$GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"
$PYTHON_EXE = Join-Path $PYTHON_DIR "python.exe"
$INSTALL_DEBUG_LOG = Join-Path $INSTALL_DIR "install_debug.log"

Write-Host "--- Iniciando Instalao do Agente SysAva ---" -ForegroundColor Cyan

# Garante que a pasta base existe antes de iniciar o transcript
if (-not (Test-Path $INSTALL_DIR)) { New-Item -Path $INSTALL_DIR -ItemType Directory -Force | Out-Null }
Start-Transcript -Path $INSTALL_DEBUG_LOG -Append

# 1. Criar pastas
if (-not (Test-Path $INSTALL_DIR)) {
    New-Item -Path $INSTALL_DIR -ItemType Directory | Out-Null
    Write-Host "[OK] Pasta criada em $INSTALL_DIR"
}

Set-Location $INSTALL_DIR

# 2. Configurar Python (Baixar e Extrair se no existir)
$foundPythonExe = Get-ChildItem -Path $INSTALL_DIR -Filter "python.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if (-not $foundPythonExe) {
    Write-Host " Baixando Python Porttil..." -ForegroundColor Yellow
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $zipPath = Join-Path $INSTALL_DIR "python_dist.zip"
    Invoke-WebRequest -Uri $PYTHON_ZIP_URL -OutFile $zipPath -UseBasicParsing
    
    Write-Host "Extraindo arquivos para $PYTHON_DIR..." -ForegroundColor Yellow
    try {
        Unblock-File -Path $zipPath
        
        # Tentativa 1: .NET ZipFile (Mais confivel)
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        $zip = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
        foreach ($entry in $zip.Entries) {
            $targetPath = Join-Path $PYTHON_DIR $entry.FullName
            $targetDir = Split-Path $targetPath -Parent
            if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Path $targetDir -Force | Out-Null }
            if ($entry.Name -ne "") {
                [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $targetPath, $true)
            }
        }
        $zip.Dispose()
    } catch {
        Write-Host "Tentando extrao alternativa..." -ForegroundColor Yellow
        Expand-Archive -Path $zipPath -DestinationPath $PYTHON_DIR -Force
    } finally {
        if (Test-Path $zipPath) { Remove-Item $zipPath -Force -ErrorAction SilentlyContinue }
    }

    $foundPythonExe = Get-ChildItem -Path $INSTALL_DIR -Filter "python.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
}

if (-not $foundPythonExe) {
    Write-Error "ERRO: Falha ao localizar python.exe aps a extrao."
    exit 1
}

$PYTHON_EXE = $foundPythonExe.FullName
$PYTHON_HOME = Split-Path -Path $PYTHON_EXE -Parent

# Habilitar site-packages no Python Embeddable
$pthFile = Get-ChildItem -Path $PYTHON_HOME -Filter "python*._pth" | Select-Object -First 1
if ($pthFile) {
    $content = Get-Content $pthFile.FullName
    if ($content -match '#import site') {
        $content -replace '#import site', 'import site' | Set-Content $pthFile.FullName
        Write-Host "[OK] site-packages habilitado." -ForegroundColor Green
    }
}
Write-Host "[OK] Python configurado em: $PYTHON_EXE" -ForegroundColor Green

# 3. Instalar PIP e Dependncias
$pipExe = Join-Path $PYTHON_HOME "Scripts\pip.exe"
if (-not (Test-Path $pipExe)) {
    Write-Host " Instalando Gerenciador de Pacotes (PIP)..." -ForegroundColor Yellow
    $getPipPath = Join-Path $INSTALL_DIR "get-pip.py"
    Invoke-WebRequest -Uri $GET_PIP_URL -OutFile $getPipPath
    & $PYTHON_EXE $getPipPath --no-warn-script-location
    Remove-Item $getPipPath
    
    Write-Host " Instalando bibliotecas (psutil, requests, pygetwindow)..." -ForegroundColor Yellow
    & $PYTHON_EXE -m pip install setuptools wheel --no-warn-script-location
    & $PYTHON_EXE -m pip install psutil requests pygetwindow --no-warn-script-location
    Write-Host "[OK] Dependncias instaladas." -ForegroundColor Green
}

# 4. Criar o script Python do Agente (lab_agent.py)
$agentCode = @"
import psutil
import requests
import time
import socket
import getpass
import os
import threading
import ctypes
import logging
import subprocess
import sys
from ctypes import wintypes
import sqlite3
import shutil
import tempfile
import glob
import json

import concurrent.futures

try:
    import pygetwindow as gw
except:
    gw = None

logging.basicConfig(
    filename=r'$LOG_PATH',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

SERVER_URL = None
INTERVALO = 10

# --- Plataformas de jogos (bloqueio manual acionado pelo professor) ---
BLOCKED_PROCESS_KEYWORDS = [
    "roblox", "robloxplayer", "robloxstudio",
    "leagueclient", "league of legends",
]
BLOCKED_SITE_KEYWORDS = [
    "loki", "poki", "friv", "y8", "clickjogos", "gartic", "jogos", "jogar",
]
BROWSER_PROCESS_KEYWORDS = ["chrome", "msedge", "firefox", "brave", "opera", "iexplore"]
BLOCKED_SOCIAL_KEYWORDS = ["youtube", "youtu.be", "instagram", "tiktok", "facebook", "twitter", "x.com"]
BLOCKED_ANON_PROCESS = ["tor.exe", "torbrowser.exe", "i2prouter.exe", "obfs4proxy.exe"]
BLOCKED_ANON_KEYWORDS = ["tor browser", "torproject", "i2p"]

# --- Descoberta robusta do servidor ---
DISCOVERY_PORT = 5001
DISCOVERY_MAGIC = "SYSAVA_DISCOVER"
DISCOVERY_REPLY = "SYSAVA_SERVER"
SERVER_CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server_cache.txt")
HISTORY_INTERVAL = 180
HISTORY_MARKER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history_marker.txt")
AUTO_BLOCK = True
AUTO_BLOCK_INTERVAL = 4
BLOCKED_APPS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blocked_apps.json")

def check_ip(ip):
    try:
        url = f"http://{ip}:5000/health"
        r = requests.get(url, timeout=1.0)
        if r.status_code == 200 and r.json().get("status") == "online":
            return f"http://{ip}:5000/ping"
    except:
        return None

def load_cached_server():
    try:
        if os.path.exists(SERVER_CACHE_FILE):
            with open(SERVER_CACHE_FILE, "r", encoding="utf-8") as f:
                url = f.read().strip()
                return url or None
    except Exception as e:
        logging.error(f"Erro ao ler cache do servidor: {e}")
    return None

def save_cached_server(url):
    try:
        with open(SERVER_CACHE_FILE, "w", encoding="utf-8") as f:
            f.write(url)
    except Exception as e:
        logging.error(f"Erro ao salvar cache do servidor: {e}")

def discover_server_udp(local_ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(1.5)
        base = ".".join(local_ip.split('.')[:-1]) + "."
        targets = {"255.255.255.255", f"{base}255", "192.168.10.255", "192.168.11.255"}
        for t in targets:
            try:
                sock.sendto(DISCOVERY_MAGIC.encode(), (t, DISCOVERY_PORT))
            except Exception:
                pass
        while True:
            try:
                data, addr = sock.recvfrom(1024)
            except socket.timeout:
                break
            msg = data.decode(errors="ignore").strip()
            if msg.startswith(DISCOVERY_REPLY):
                url = check_ip(addr[0])
                if url:
                    sock.close()
                    logging.info(f"Servidor localizado via UDP broadcast: {addr[0]}")
                    return url
        sock.close()
    except Exception as e:
        logging.error(f"Erro na descoberta UDP: {e}")
    return None

def find_server(local_ip):
    global SERVER_URL

    cached = load_cached_server()
    if cached:
        try:
            ip = cached.split("//")[1].split(":")[0].split("/")[0]
            url = check_ip(ip)
            if url:
                logging.info(f"Servidor localizado via cache: {url}")
                SERVER_URL = url
                return True
        except Exception:
            pass

    url = discover_server_udp(local_ip)
    if url:
        SERVER_URL = url
        save_cached_server(url)
        return True

    base_ip = ".".join(local_ip.split('.')[:-1]) + "."
    logging.info(f"Buscando servidor SysAva na rede {base_ip}x...")

    ips = [f"{base_ip}{i}" for i in range(1, 255)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(check_ip, ips)
        for res in results:
            if res:
                logging.info(f"Servidor encontrado: {res}")
                SERVER_URL = res
                save_cached_server(res)
                return True
                
    logging.error("Nenhum servidor encontrado na rede local.")
    return False

def show_balloon(title, msg):
    try:
        ps_cmd = f'[void][System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms"); `$n = New-Object System.Windows.Forms.NotifyIcon; `$n.Icon = [System.Drawing.SystemIcons]::Information; `$n.BalloonTipTitle = "{title}"; `$n.BalloonTipText = "{msg}"; `$n.Visible = `$true; `$n.ShowBalloonTip(5000); Start-Sleep -Seconds 5; `$n.Dispose()'
        subprocess.Popen(["powershell", "-WindowStyle", "Hidden", "-Command", ps_cmd])
    except Exception as e:
        logging.error(f"Erro ao exibir balao: {e}")

def get_active_window():
    try:
        if gw:
            window = gw.getActiveWindow()
            return window.title if window else "Nenhuma"
        return "N/A"
    except: return "Erro"

def get_open_ports():
    ports = []
    try:
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'LISTEN': ports.append(conn.laddr.port)
    except: pass
    return sorted(list(set(ports)))

def run_winget_install(package_ids):
    for pkg in package_ids:
        logging.info(f"Instalando pacote: {pkg}...")
        os.system(f"winget install --id {pkg} --silent --accept-package-agreements --accept-source-agreements")

def kill_game_processes():
    killed = []
    for proc in psutil.process_iter(['name']):
        try:
            name = (proc.info.get('name') or "").lower()
            if any(k in name for k in BLOCKED_PROCESS_KEYWORDS):
                proc.kill()
                killed.append(proc.info.get('name'))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return killed

def close_windows_by_keywords(keywords):
    closed = []
    if not gw:
        return closed
    try:
        for win in gw.getAllWindows():
            title = win.title or ""
            if any(k in title.lower() for k in keywords):
                try:
                    win.close()
                    closed.append(title)
                except Exception:
                    pass
    except Exception as e:
        logging.error(f"Erro ao fechar janelas: {e}")
    return closed

def close_blocked_sites():
    return close_windows_by_keywords(BLOCKED_SITE_KEYWORDS)

def close_social_sites():
    return close_windows_by_keywords(BLOCKED_SITE_KEYWORDS + BLOCKED_SOCIAL_KEYWORDS)

def close_anon():
    killed = []
    for proc in psutil.process_iter(['name']):
        try:
            n = (proc.info.get('name') or "").lower()
            if n in BLOCKED_ANON_PROCESS:
                proc.kill()
                killed.append(proc.info.get('name'))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    closed = close_windows_by_keywords(BLOCKED_ANON_KEYWORDS)
    return killed, closed

def close_browsers():
    killed = []
    for proc in psutil.process_iter(['name']):
        try:
            name = (proc.info.get('name') or "").lower()
            if any(b in name for b in BROWSER_PROCESS_KEYWORDS):
                proc.kill()
                killed.append(proc.info.get('name'))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return killed

def block_games():
    killed = kill_game_processes()
    closed = close_blocked_sites()
    if killed or closed:
        logging.info(f"Bloqueio de jogos -> processos: {killed} | sites: {closed}")
    return killed, closed

def get_category(wt, procs):
    wt = wt.lower()
    if any(k in wt for k in BLOCKED_ANON_KEYWORDS) or any((p or "").lower() in BLOCKED_ANON_PROCESS for p in procs):
        return "Anônimo"
    if "roblox" in wt or any("roblox" in p.lower() for p in procs): return "Roblox"
    if any(k in wt for k in BLOCKED_SITE_KEYWORDS): return "Games"
    if any(t in wt for t in ["facebook", "instagram", "youtube", "tiktok", "whatsapp"]): return "Social"
    if any(t in wt for t in ["poki", "friv", "game", "jogos"]): return "Games"
    return "Produtivo"

def get_local_ip():
    """Tenta obter o IP real da interface de rede ativa evitando 127.0.0.1."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Não precisa ser alcançável, serve apenas para o SO escolher a interface correta
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

# --- Sessao interativa: pular de SYSTEM (sessao 0) para a sessao do aluno ---
INVALID_SESSION = 0xFFFFFFFF
CREATE_UNICODE_ENVIRONMENT = 0x00000400
CREATE_NO_WINDOW = 0x08000000

class _STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD), ("lpReserved", wintypes.LPWSTR), ("lpDesktop", wintypes.LPWSTR),
        ("lpTitle", wintypes.LPWSTR), ("dwX", wintypes.DWORD), ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD), ("dwYSize", wintypes.DWORD), ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD), ("dwFillAttribute", wintypes.DWORD), ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD), ("cbReserved2", wintypes.WORD), ("lpReserved2", ctypes.c_void_p),
        ("hStdInput", wintypes.HANDLE), ("hStdOutput", wintypes.HANDLE), ("hStdError", wintypes.HANDLE),
    ]

class _PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", wintypes.HANDLE), ("hThread", wintypes.HANDLE),
        ("dwProcessId", wintypes.DWORD), ("dwThreadId", wintypes.DWORD),
    ]

def is_system_process():
    try:
        return getpass.getuser().strip().upper() == "SYSTEM"
    except Exception:
        return False

def get_current_session():
    try:
        kernel32 = ctypes.windll.kernel32
        kernel32.GetCurrentProcessId.restype = wintypes.DWORD
        sid = wintypes.DWORD()
        kernel32.ProcessIdToSessionId(kernel32.GetCurrentProcessId(), ctypes.byref(sid))
        return sid.value
    except Exception:
        return -1

def get_active_console_session():
    try:
        kernel32 = ctypes.windll.kernel32
        kernel32.WTSGetActiveConsoleSessionId.restype = wintypes.DWORD
        return kernel32.WTSGetActiveConsoleSessionId()
    except Exception:
        return INVALID_SESSION

def relaunch_in_active_session():
    if "--session-agent" in sys.argv or not is_system_process():
        return False

    active = get_active_console_session()
    current = get_current_session()
    if active in (INVALID_SESSION, 0) or active == current:
        return False

    kernel32 = ctypes.windll.kernel32
    wtsapi32 = ctypes.windll.wtsapi32
    advapi32 = ctypes.windll.advapi32
    userenv = ctypes.windll.userenv

    hToken = wintypes.HANDLE()
    if not wtsapi32.WTSQueryUserToken(active, ctypes.byref(hToken)):
        logging.error(f"WTSQueryUserToken falhou na sessao {active} (err {ctypes.GetLastError()})")
        return False

    hDup = wintypes.HANDLE()
    env = ctypes.c_void_p()
    try:
        if not advapi32.DuplicateTokenEx(hToken, 0, None, 2, 1, ctypes.byref(hDup)):
            logging.error(f"DuplicateTokenEx falhou (err {ctypes.GetLastError()})")
            return False

        userenv.CreateEnvironmentBlock(ctypes.byref(env), hDup, False)

        si = _STARTUPINFO()
        si.cb = ctypes.sizeof(_STARTUPINFO)
        si.lpDesktop = "winsta0\\default"
        pi = _PROCESS_INFORMATION()
        cmd = f'"{sys.executable}" "{os.path.abspath(__file__)}" --session-agent'
        flags = CREATE_UNICODE_ENVIRONMENT | CREATE_NO_WINDOW

        ok = advapi32.CreateProcessAsUserW(
            hDup, None, ctypes.c_wchar_p(cmd), None, None, False,
            flags, env, None, ctypes.byref(si), ctypes.byref(pi)
        )
        if ok:
            logging.info(f"Agente relancado na sessao ativa {active} (pid {pi.dwProcessId}).")
            kernel32.CloseHandle(pi.hProcess)
            kernel32.CloseHandle(pi.hThread)
            return True

        logging.error(f"CreateProcessAsUserW falhou (err {ctypes.GetLastError()})")
        return False
    finally:
        if env:
            try: userenv.DestroyEnvironmentBlock(env)
            except Exception: pass
        if hDup:
            kernel32.CloseHandle(hDup)
        if hToken:
            kernel32.CloseHandle(hToken)

def _parse_aula_range(txt):
    txt = (txt or "").strip()
    if not txt:
        return []
    try:
        if "-" in txt:
            a, b = txt.split("-", 1)
            return list(range(int(a), int(b) + 1))
        return list(range(1, int(txt) + 1))
    except Exception:
        return []

def _chrome_epoch(ct):
    try:
        return ct / 1000000.0 - 11644473600
    except Exception:
        return 0

def _read_browser_history(db_path):
    out = []
    try:
        tmp = os.path.join(tempfile.gettempdir(), "sysava_hist_%s_%s" % (os.path.basename(db_path), os.getpid()))
        for suf in ("", "-wal", "-shm"):
            if os.path.exists(db_path + suf):
                try:
                    shutil.copy2(db_path + suf, tmp + suf)
                except Exception:
                    pass
        conn = sqlite3.connect(tmp)
        try:
            cur = conn.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 300")
            for url, title, t in cur.fetchall():
                out.append({"url": url or "", "title": title or "", "ts": _chrome_epoch(t)})
        finally:
            conn.close()
        for suf in ("", "-wal", "-shm"):
            try:
                os.remove(tmp + suf)
            except Exception:
                pass
    except Exception as e:
        logging.error(f"Erro lendo historico {db_path}: {e}")
    return out

def _load_history_marker():
    try:
        with open(HISTORY_MARKER_FILE, "r", encoding="utf-8") as f:
            return float(f.read().strip())
    except Exception:
        return None

def _save_history_marker(v):
    try:
        with open(HISTORY_MARKER_FILE, "w", encoding="utf-8") as f:
            f.write(str(v))
    except Exception:
        pass

def send_history(hostname, username, local_ip):
    if not SERVER_URL:
        return
    la = os.environ.get("LOCALAPPDATA", "")
    paths = []
    paths += glob.glob(os.path.join(la, "Google", "Chrome", "User Data", "*", "History"))
    paths += glob.glob(os.path.join(la, "Microsoft", "Edge", "User Data", "*", "History"))
    if not paths:
        return
    marker = _load_history_marker()
    now = time.time()
    if marker is None:
        _save_history_marker(now)
        return
    items = []
    for p in paths:
        for it in _read_browser_history(p):
            if it["ts"] > marker:
                it["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(it["ts"]))
                items.append(it)
    if not items:
        return
    try:
        requests.post(SERVER_URL.replace("/ping", "/api/historico"),
                      json={"maquina": hostname, "user": username, "ip": local_ip, "items": items[:500]}, timeout=5)
        _save_history_marker(now)
    except Exception as e:
        logging.error(f"Erro enviando historico: {e}")

def _load_blocked_apps():
    nomes = set(BLOCKED_PROCESS_KEYWORDS)
    try:
        if os.path.exists(BLOCKED_APPS_FILE):
            with open(BLOCKED_APPS_FILE, "r", encoding="utf-8") as f:
                dados = json.load(f)
            for n in dados.get("processos", []):
                if n:
                    nomes.add(str(n).lower())
    except Exception:
        pass
    return nomes

def watchdog():
    logging.info("Watchdog de processos (auto-bloqueio) iniciado.")
    while True:
        try:
            bloqueados = _load_blocked_apps()
            for proc in psutil.process_iter(['name']):
                try:
                    n = (proc.info.get('name') or "").lower()
                    if n and any(k in n for k in bloqueados):
                        proc.kill()
                        logging.info(f"WATCHDOG: bloqueado {proc.info.get('name')}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception as e:
            logging.error(f"Erro no watchdog: {e}")
        time.sleep(AUTO_BLOCK_INTERVAL)

def atualizar_monitor():
    if not SERVER_URL:
        return
    base = SERVER_URL.replace("/ping", "")
    url = base + "/download/lab_agent.ps1"
    try:
        tmp = os.path.join(tempfile.gettempdir(), "lab_agent_update.ps1")
        r = requests.get(url, timeout=20)
        if r.status_code != 200:
            logging.error(f"Atualizar: download falhou ({r.status_code})")
            return
        with open(tmp, "wb") as f:
            f.write(r.content)
        subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
                          "Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','%s'" % tmp])
        logging.info("Atualizacao iniciada (UAC vai pedir a senha de Administrador).")
        show_balloon("SysAva Lab", "Atualizacao iniciada. Autorize como Administrador.")
    except Exception as e:
        logging.error(f"Erro ao atualizar: {e}")

def monitor():
    global SERVER_URL

    if relaunch_in_active_session():
        return

    hostname = socket.gethostname()
    username = getpass.getuser()
    local_ip = get_local_ip()

    logging.info(f"Iniciando monitoramento na maquina {hostname} ({local_ip}) - Usuario: {username}")
    show_balloon("SysAva Lab", "O Agente de Monitoramento foi iniciado de forma oculta.")

    if AUTO_BLOCK:
        threading.Thread(target=watchdog, daemon=True).start()

    last_history = 0
    while True:
        if not SERVER_URL:
            if not find_server(local_ip):
                time.sleep(10)
                continue
                
        try:
            window_title = get_active_window()
            all_procs = [p.info['name'] for p in psutil.process_iter(['name'])]
            category = get_category(window_title, all_procs)
            open_ports = get_open_ports()
            
            payload = {
                "maquina": hostname, "user": username, "activity": window_title,
                "category": category, "ip": local_ip, "ports": open_ports, "last_seen": time.strftime("%H:%M:%S"),
                "procs": sorted({(n or "").lower() for n in all_procs if n})[:200]
            }
            
            res = requests.post(SERVER_URL, json=payload, timeout=5)
            if res.status_code == 200:
                cmd_data = res.json()
                if cmd_data.get("pending_command"):
                    cmd = cmd_data["pending_command"]
                    msg = cmd_data.get("command_msg", "")
                    logging.info(f"Comando recebido do servidor: {cmd} | Msg: {msg}")
                    if "Alerta" in cmd:
                        ctypes.windll.user32.MessageBoxW(0, msg, "Aviso do Laboratorio", 0x30)
                    elif "Bloquear Processo" in cmd or "Bloquear Jogos" in cmd:
                        killed, closed = block_games()
                        if not killed and not closed:
                            show_balloon("SysAva Lab", "Nenhum jogo ou site bloqueado foi encontrado.")
                    elif "Bloquear Sites" in cmd:
                        closed = close_social_sites()
                        logging.info(f"Sites bloqueados: {closed}")
                        if not closed:
                            show_balloon("SysAva Lab", "Nenhum site bloqueado foi encontrado.")
                    elif "Bloquear Anônimos" in cmd or "Anonimos" in cmd:
                        killed, closed = close_anon()
                        logging.info(f"Anonimos bloqueados -> processos: {killed} | janelas: {closed}")
                        if not killed and not closed:
                            show_balloon("SysAva Lab", "Nenhum anonimizador (Tor) encontrado.")
                    elif "Atualizar" in cmd:
                        logging.info("Comando de atualizacao do monitor recebido.")
                        atualizar_monitor()
                    elif "Bloquear Navegador" in cmd:
                        killed = close_browsers()
                        logging.info(f"Navegadores bloqueados: {killed}")
                    elif "Forçar Logoff" in cmd or "Logoff" in cmd:
                        logging.info("Executando logoff...")
                        os.system("shutdown /l /f")
                    elif "Desligar" in cmd:
                        logging.info("Executando desligamento...")
                        os.system("shutdown /s /f /t 0")
                    elif "Reiniciar" in cmd:
                        logging.info("Executando reinicializacao...")
                        os.system("shutdown /r /f /t 0")
                    elif "Estruturar Pastas" in cmd:
                        try:
                            parts = msg.split('|')
                            if len(parts) >= 4:
                                s, t, d, a = parts[0], parts[1], parts[2], parts[3]
                                aulas = parts[4] if len(parts) >= 5 else ""
                                path = os.path.join("C:\\Projetos", s, t, d, a)
                                os.makedirs(path, exist_ok=True)
                                criadas = 0
                                for n in _parse_aula_range(aulas):
                                    os.makedirs(os.path.join(path, f"Aula {n:02d}"), exist_ok=True)
                                    criadas += 1
                                logging.info(f"Estrutura de pastas criada: {path} (+{criadas} aulas)")
                        except Exception as e:
                            logging.error(f"Erro ao estruturar pastas: {e}")
                    elif "Instalar Kit Lab DS" in cmd:
                        kit = [
                            "Microsoft.VisualStudioCode",
                            "Microsoft.OpenJDK.17", 
                            "OpenJS.NodeJS.LTS",
                            "Apache.NetBeans"
                        ]
                        logging.info("Iniciando thread de instalacao do Kit Lab DS...")
                        threading.Thread(target=run_winget_install, args=(kit,), daemon=True).start()
        except requests.exceptions.RequestException as re:
            logging.error(f"Erro de conexao com o servidor: {re}")
            SERVER_URL = None # Fora a procurar novamente
        except Exception as e: 
            logging.error(f"Erro no loop principal: {e}")

        if time.time() - last_history > HISTORY_INTERVAL:
            last_history = time.time()
            threading.Thread(target=send_history, args=(hostname, username, local_ip), daemon=True).start()

        time.sleep(INTERVALO)

if __name__ == "__main__":
    monitor()
"@


Set-Content -Path "lab_agent.py" -Value $agentCode -Encoding UTF8
Write-Host "[OK] Script do agente criado." -ForegroundColor Green

Stop-Transcript

# 4b. Encerra uma instancia anterior do agente (permite atualizacao limpa)
Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -match 'lab_agent\.py' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Write-Host "[OK] Instancias anteriores do agente encerradas (se havia)." -ForegroundColor Green

# 5. Executar em segundo plano (Hidden)
Write-Host " Iniciando monitoramento oculto..." -ForegroundColor Green
$startInfo = New-Object System.Diagnostics.ProcessStartInfo
$startInfo.FileName = $PYTHON_EXE
$startInfo.Arguments = "$INSTALL_DIR\lab_agent.py"
$startInfo.WorkingDirectory = $INSTALL_DIR
$startInfo.WindowStyle = "Hidden"
$startInfo.CreateNoWindow = $true
[System.Diagnostics.Process]::Start($startInfo) | Out-Null

# 5b. Auto-inicializacao no logon via pasta Startup (nao depende do nome de grupo/tarefa)
$PYTHONW = Join-Path (Split-Path $PYTHON_EXE -Parent) "pythonw.exe"
if (-not (Test-Path -LiteralPath $PYTHONW)) { $PYTHONW = $PYTHON_EXE }
$taskScript = Join-Path $INSTALL_DIR "lab_agent.py"
$ok_startup = $false
try {
    $launcher = Join-Path $INSTALL_DIR "iniciar_agente.vbs"
    $vbs = 'Set sh = CreateObject("WScript.Shell")' + "`r`n" + 'sh.Run """' + $PYTHONW + '"" ""' + $taskScript + '""", 0, False' + "`r`n"
    Set-Content -Path $launcher -Value $vbs -Encoding ASCII
    $startup = Join-Path ([Environment]::GetFolderPath('CommonStartup')) "SysAva Agent.vbs"
    Copy-Item -LiteralPath $launcher -Destination $startup -Force
    Write-Host "[OK] Auto-inicializacao no logon via Startup: $startup" -ForegroundColor Green
    $ok_startup = $true
} catch {
    Write-Host "[AVISO] Falha no Startup comum ($($_.Exception.Message)). Tentando tarefa agendada..." -ForegroundColor Yellow
}
if (-not $ok_startup) {
    try {
        $action = New-ScheduledTaskAction -Execute $PYTHONW -Argument "`"$taskScript`""
        $trigger = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\$env:USERNAME"
        $principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
        $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit ([TimeSpan]::Zero)
        Register-ScheduledTask -TaskName "SysAva Agent" -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force | Out-Null
        Write-Host "[OK] Auto-inicializacao via tarefa agendada (usuario atual)." -ForegroundColor Green
    } catch {
        Write-Host "[AVISO] Nao foi possivel registrar a auto-inicializacao: $($_.Exception.Message)" -ForegroundColor Yellow
        Write-Host "        O agente esta rodando agora, mas nao voltara sozinho apos reiniciar." -ForegroundColor Yellow
    }
}

Write-Host "--- INSTALAO CONCLUDA ---" -ForegroundColor Cyan
