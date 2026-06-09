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

def find_server(local_ip):
    global SERVER_URL
    base_ip = ".".join(local_ip.split('.')[:-1]) + "."
    logging.info(f"Buscando servidor SysAva na rede {base_ip}x...")
    
    def check_ip(ip):
        try:
            url = f"http://{ip}:5000/health"
            r = requests.get(url, timeout=1.0)
            if r.status_code == 200 and r.json().get("status") == "online":
                return f"http://{ip}:5000/ping"
        except:
            return None

    ips = [f"{base_ip}{i}" for i in range(1, 255)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(check_ip, ips)
        for res in results:
            if res:
                logging.info(f"Servidor encontrado: {res}")
                SERVER_URL = res
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

def get_category(wt, procs):
    wt = wt.lower()
    if "roblox" in wt or any("roblox" in p.lower() for p in procs): return "Roblox"
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

def monitor():
    global SERVER_URL
    hostname = socket.gethostname()
    username = getpass.getuser()
    local_ip = get_local_ip()

    logging.info(f"Iniciando monitoramento na maquina {hostname} ({local_ip}) - Usuario: {username}")
    show_balloon("SysAva Lab", "O Agente de Monitoramento foi iniciado de forma oculta.")

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
                "category": category, "ip": local_ip, "ports": open_ports, "last_seen": time.strftime("%H:%M:%S")
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
                    elif "Bloquear Processo" in cmd:
                        for proc in psutil.process_iter():
                            if "roblox" in proc.name().lower(): 
                                logging.info(f"Bloqueando processo: {proc.name()}")
                                proc.kill()
                    elif "Desligar" in cmd:
                        logging.info("Executando desligamento...")
                        os.system("shutdown /s /f /t 10")
                    elif "Reiniciar" in cmd:
                        logging.info("Executando reinicializacao...")
                        os.system("shutdown /r /f /t 10")
                    elif "Estruturar Pastas" in cmd:
                        try:
                            parts = msg.split('|')
                            if len(parts) == 4:
                                s, t, d, a = parts
                                path = os.path.join("C:\\Projetos", s, t, d, a)
                                os.makedirs(path, exist_ok=True)
                                logging.info(f"Estrutura de pastas criada: {path}")
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
            
        time.sleep(INTERVALO)

if __name__ == "__main__":
    monitor()
"@


Set-Content -Path "lab_agent.py" -Value $agentCode -Encoding UTF8
Write-Host "[OK] Script do agente criado." -ForegroundColor Green

Stop-Transcript

# 5. Executar em segundo plano (Hidden)
Write-Host " Iniciando monitoramento oculto..." -ForegroundColor Green
$startInfo = New-Object System.Diagnostics.ProcessStartInfo
$startInfo.FileName = $PYTHON_EXE
$startInfo.Arguments = "$INSTALL_DIR\lab_agent.py"
$startInfo.WorkingDirectory = $INSTALL_DIR
$startInfo.WindowStyle = "Hidden"
$startInfo.CreateNoWindow = $true
[System.Diagnostics.Process]::Start($startInfo) | Out-Null

Write-Host "--- INSTALAO CONCLUDA ---" -ForegroundColor Cyan
