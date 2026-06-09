from flask import Flask, request, jsonify, render_template_string
import json
import os
import time
import shutil
import subprocess
import re
import socket

app = Flask(__name__)
start_time = time.time()

# --- Memória RAM (Estado Vivo) ---
# Armazena o estado volátil das máquinas para acesso ultra-rápido
LIVE_CACHE = {}

# Define o caminho absoluto para evitar que o arquivo seja criado em locais inesperados
STATUS_FILE = os.path.join(os.path.dirname(__file__), "lab_status.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "lab_receiver.log")

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
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # Se o arquivo estiver corrompido, tenta ler a última versão válida ou limpa
            print(f"⚠️ Arquivo {STATUS_FILE} corrompido. Resetando...")
            return {}
    return {}

def save_data(data):
    """Grava os dados de forma atômica (escreve em temp e depois substitui)."""
    temp_file = STATUS_FILE + ".tmp"
    try:
        # 1. Escreve em um arquivo temporário primeiro
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno()) # Garante que os dados foram pro disco
        
        # 2. Substitui o arquivo oficial (operação atômica no SO)
        os.replace(temp_file, STATUS_FILE)
    except Exception as e:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        print(f"❌ Erro crítico ao salvar status: {e}")
        log_event(f"❌ Erro crítico ao salvar status: {e}")

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
                .timestamp { color: #888; }
                .latency { color: #ffeb3b; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📡 SysAva Server Diagnostics</h1>
                <p>Uptime: {{ uptime }}s | IP Servidor: {{ ip }} | Itens na RAM: {{ count }}</p>
            </div>
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
            now=now
        )
    except Exception as e:
        # Registra o erro no log do Flask (geralmente console) e retorna um 500 com detalhes
        app.logger.error(f"Erro ao renderizar página de diagnóstico: {e}", exc_info=True)
        return f"<h1>Erro Interno do Servidor (500)</h1><p>Detalhes: {e}</p>", 500

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
    # threaded=True permite que o Flask lide com múltiplas requisições ao mesmo tempo
    print("\n" + "="*50)
    print("🚀 SysAva Receiver v2 (RAM + Diagnostics) Online")
    print(f"📍 Endereco MAC: {get_my_mac()}")
    print(f"🔗 Rota IPv4: http://192.168.11.249:8080/diagnostics")
    print(f"🔗 Rota IPv6: http://[{get_local_ipv6()}]:8080/diagnostics")
    print("� Use este MAC no 'lab_agent.py' para busca automatica.")
    print("="*50 + "\n")
    
    # Rodar em '::' permite conexões IPv4 e IPv6 simultâneas
    app.run(host='::', port=8080, threaded=True, debug=False)