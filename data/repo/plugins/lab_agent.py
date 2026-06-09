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
import re

import concurrent.futures

try:
    import pygetwindow as gw # type: ignore
except:
    gw = None

logging.basicConfig(
    filename=r'C:\Local\SysVa_lab\agent_runtime.log', # Exemplo de caminho de log real
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

SERVER_URL = None
# IMPORTANTE: Se o notebook (servidor) trocar de IP/MAC, o agente para de achar.
# Recomenda-se deixar SERVER_MAC como None se não tiver certeza do MAC do Notebook do professor.
SERVER_MAC = "B8-F7-75-06-4B-36" #None 
# IP Estático do Servidor (Notebook) conforme sua topologia
KNOWN_SERVER_IP = "192.168.11.249"
INTERVALO = 10
 
def check_ip(ip):
    """Verifica se um IP específico está rodando o servidor SysAva."""
    try:
        # Formata URL para IPv6 (com colchetes) ou IPv4
        if ":" in ip and "[" not in ip:
            base_url = f"http://[{ip}]:8080"
        else:
            base_url = f"http://{ip}:8080"
            
        url = f"{base_url}/health"
        r = requests.get(url, timeout=1.2)
        if r.status_code == 200 and r.json().get("status") == "online":
            return f"{base_url}/ping"
    except:
        return None
    return None

def get_ip_by_mac(target_mac):
    """Busca na tabela ARP local o IP correspondente a um endereço MAC."""
    try:
        # Padroniza o MAC para comparação (minúsculas e hífen)
        target_mac = target_mac.lower().replace(":", "-")
        output = subprocess.check_output(["arp", "-a"], stderr=subprocess.STDOUT, text=True)
        for line in output.splitlines():
            if target_mac in line.lower().replace(":", "-"):
                parts = line.split()
                if len(parts) >= 1:
                    return parts[0] # O primeiro item da linha do ARP costuma ser o IP
    except Exception as e:
        logging.error(f"Erro ao consultar tabela ARP: {e}")
    return None

def find_server(local_ip):
    global SERVER_URL

    # 0. Tentativa Direta no IP conhecido (Alta Prioridade)
    if KNOWN_SERVER_IP:
        url = check_ip(KNOWN_SERVER_IP)
        if url:
            logging.info(f"Servidor localizado via IP Estático: {KNOWN_SERVER_IP}")
            SERVER_URL = url
            return True

    # 0.1 Tentativa via Multicast IPv6 (A "Terceira Rota")
    # Tenta o endereço de multicast "All Nodes" que alcança vizinhos na mesma rede física
    logging.info("Tentando descoberta via IPv6 Link-Local Multicast...")
    url_v6 = check_ip("ff02::1") # Multicast para todos os nós no link
    if url_v6:
        SERVER_URL = url_v6
        return True

    # 1. Tentativa rápida via MAC Address (Se configurado)
    if SERVER_MAC and SERVER_MAC.lower() != get_my_mac().lower(): # Adiciona verificação para não ser o próprio MAC
        mac_ip = get_ip_by_mac(SERVER_MAC)
        if mac_ip:
            url = check_ip(mac_ip)
            if url:
                logging.info(f"Servidor localizado via MAC {SERVER_MAC} no IP {mac_ip}")
                SERVER_URL = url
                return True

    # 2. Varredura de Rede (Subnet Scan)
    # Tenta na rede local e na provável rede do servidor (192.168.11 e 192.168.10)
    subnets_to_scan = [
        ".".join(local_ip.split('.')[:-1]) + ".",
        "192.168.10.",
        "192.168.11."
    ]
    
    for base_ip in list(set(subnets_to_scan)):
        logging.info(f"Buscando servidor SysAva na rede {base_ip}x...")
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

def get_my_mac():
    """Obtem o MAC Address da interface ativa."""
    try:
        output = subprocess.check_output("getmac", text=True)
        # Busca o primeiro padrão de MAC encontrado (XX-XX-XX-XX-XX-XX)
        match = re.search(r"([0-9A-F]{2}-){5}[0-9A-F]{2}", output, re.I)
        if match: return match.group(0).upper()
    except:
        pass
    return "N/A"

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