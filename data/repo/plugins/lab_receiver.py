from flask import Flask, request, jsonify, render_template_string
import json
import os
import time
import shutil
import subprocess
import re
import socket
import logging
import threading
import concurrent.futures
from filelock import FileLock, Timeout
import platform

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

# Template HTML moderno para o Dashboard
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>SysAva Lab Monitor</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; margin: 20px; color: #333; }
        .container { max-width: 1200px; margin: auto; }
        h1 { text-align: center; color: #1a73e8; margin-bottom: 30px; }
        .stats { display: flex; gap: 20px; margin-bottom: 30px; }
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); flex: 1; text-align: center; border-top: 5px solid #1a73e8; }
        .card h3 { margin: 0; font-size: 0.9em; text-transform: uppercase; color: #666; }
        .card p { font-size: 2.5em; font-weight: bold; margin: 10px 0 0; color: #1a73e8; }
        .card.warning { border-top-color: #f29900; }
        .card.warning p { color: #f29900; }
        .card.success { border-top-color: #188038; }
        .card.success p { color: #188038; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        th, td { padding: 15px; text-align: left; border-bottom: 1px solid #f0f0f0; }
        th { background: #1a73e8; color: white; font-weight: 500; text-transform: uppercase; font-size: 0.85em; }
        tr:hover { background-color: #f8f9fa; }
        .badge { padding: 4px 10px; border-radius: 20px; font-size: 0.85em; font-weight: bold; display: inline-block; }
        .status-roblox { color: #d93025; background: #fce8e6; }
        .status-games { color: #f29900; background: #fef7e0; }
        .status-social { color: #1a73e8; background: #e8f0fe; }
        .status-produtivo { color: #188038; background: #e6f4ea; }
        small { color: #777; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖥️ SysAva Lab Monitor</h1>
        <div class="stats">
            <div class="card"><h3>Total Máquinas</h3><p>{{ total }}</p></div>
            <div class="card warning"><h3>Distrações</h3><p>{{ distractions }}</p></div>
            <div class="card success"><h3>Produtivo</h3><p>{{ produtivo }}</p></div>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Máquina / IP</th>
                    <th>Usuário</th>
                    <th>Atividade Atual</th>
                    <th>Categoria</th>
                    <th>Último Sinal</th>
                </tr>
            </thead>
            <tbody>
                {% for name, info in machines.items() %}
                <tr>
                    <td><strong>{{ name }}</strong><br><small>{{ info.ip }}</small></td>
                    <td>{{ info.user }}</td>
                    <td>{{ info.activity }}</td>
                    <td><span class="badge status-{{ info.category|lower }}">{{ info.category }}</span></td>
                    <td>{{ info.last_seen }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
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
            
            try:
                arp_output = subprocess.check_output(['arp', '-a', ip], text=True)
                mac_match = re.search(r"([0-9a-f]{2}[:-]){5}[0-9a-f]{2}", arp_output, re.I)
                if mac_match:
                    details["mac"] = mac_match.group(0).upper()
            except:
                pass
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

@app.route('/diagnostics')
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

@app.route('/')
def dashboard():
    """Exibe um painel web simplificado com o status das máquinas."""
    raw_data = load_data()
    
    filtered_machines = {}
    now = time.time()
    
    # Filtra máquinas: Devem ter sinal nos últimos 5 minutos (300s)
    # Removido filtro de sub-rede para permitir monitoramento entre Wi-Fi e Cabo
    for name, info in raw_data.items():
        timestamp = info.get('timestamp', 0)
        
        # Verifica se a máquina enviou sinal recentemente
        is_active = (now - timestamp) < 300 
        
        if is_active:
            filtered_machines[name] = info

    total = len(filtered_machines)
    produtivo = sum(1 for m in filtered_machines.values() if m.get('category') == 'Produtivo')
    distractions = total - produtivo
    
    return render_template_string(
        DASHBOARD_TEMPLATE, 
        machines=filtered_machines, total=total, 
        produtivo=produtivo, distractions=distractions
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
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
    
    # app.run(host='::', port=5000, threaded=True, debug=False)