import socket
import requests
import os
import json
import psutil
from datetime import datetime
import time
import sys

import subprocess
# Configuração de cores para o terminal (ANSI)
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Controle de tempo para evitar logs excessivos no modo watch
last_log_time = 0

def get_local_ips():
    return [snic.address for interface, snics in psutil.net_if_addrs().items() 
            for snic in snics if snic.family == socket.AF_INET and not snic.address.startswith("127.")]

def get_receiver_process():
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            cmd = " ".join(proc.info['cmdline'] or [])
            if "lab_receiver.py" in cmd:
                return proc
        except: pass
    return None

def load_lab_data(status_path):
    if os.path.exists(status_path):
        try:
            with open(status_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Tenta recuperar o JSON se houver lixo no final do arquivo
            try:
                with open(status_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    last_brace = content.rfind('}')
                    if last_brace != -1:
                        return json.loads(content[:last_brace+1])
            except: pass
        except: pass
    return {}

def save_activity_log(data, log_path, watch_mode=False):
    """
    Salva um resumo da atividade no arquivo lab_receiver.log.
    No modo watch, grava apenas a cada 60 segundos para evitar arquivos gigantes.
    """
    global last_log_time
    now_ts = time.time()
    
    if watch_mode and (now_ts - last_log_time) < 60:
        return

    try:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        stats = {"Produtivo": 0, "Roblox": 0, "Games": 0, "Social": 0, "OFFLINE": 0}
        
        for maq, info in data.items():
            last_seen = info.get('last_seen', '00:00:00')
            try:
                ls_dt = datetime.strptime(last_seen, "%H:%M:%S").replace(
                    year=now.year, month=now.month, day=now.day)
                if (now - ls_dt).total_seconds() > 40:
                    stats["OFFLINE"] += 1; continue
            except: pass
            cat = info.get('category', 'N/A')
            stats[cat] = stats.get(cat, 0) + 1
            
        log_entry = f"[{timestamp}] Status -> Total: {len(data)} | Online: {len(data)-stats['OFFLINE']} | Roblox: {stats.get('Roblox',0)} | Prod: {stats.get('Produtivo',0)}\n"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
        last_log_time = now_ts
    except: pass

def print_monitor_table(data):
    if not data:
        print(f"   {Colors.WARNING}Nenhum computador enviando dados no momento.{Colors.ENDC}")
        return

    # Ordenação: Roblox e Games primeiro, depois por nome
    def sort_key(item):
        cat = item[1].get('category', '')
        priority = {"Roblox": 0, "Games": 1, "Social": 2, "Produtivo": 3}
        return (priority.get(cat, 9), item[0])

    # Cabeçalho da Tabela
    print(f"\n{Colors.BOLD}{'MÁQUINA':<18} | {'USUÁRIO':<12} | {'STATUS':<12} | {'JANELA ATIVA':<30}{Colors.ENDC}")
    print("-" * 75)

    stats = {"Produtivo": 0, "Roblox": 0, "Games": 0, "Social": 0}
    now = datetime.now()

    for maq, info in sorted(data.items(), key=sort_key):
        last_seen_str = info.get('last_seen', '00:00:00')
        try:
            last_seen_dt = datetime.strptime(last_seen_str, "%H:%M:%S").replace(
                year=now.year, month=now.month, day=now.day)
            diff = (now - last_seen_dt).total_seconds()
        except: diff = 999

        if diff > 40: # Máquina parou de responder
            status_text = "OFFLINE"
            color = Colors.WARNING
        else:
            cat = info.get('category', 'N/A')
            stats[cat] = stats.get(cat, 0) + 1
            status_text = cat
            color = Colors.ENDC
            if cat == "Roblox": color = Colors.FAIL
            elif cat == "Produtivo": color = Colors.OKGREEN
            elif cat in ["Games", "Social"]: color = Colors.WARNING

        user = info.get('user', '---')[:12]
        activity = info.get('activity', '---')[:30]
        
        print(f"{maq:<18} | {user:<12} | {color}{status_text:<12}{Colors.ENDC} | {activity:<30}")

    # Resumo de estatísticas
    total = len(data)
    prod = stats.get('Produtivo', 0)
    distracao = total - prod
    
    print("-" * 75)
    print(f"Resumo: {Colors.OKGREEN}{prod} Produtivos{Colors.ENDC} | {Colors.FAIL}{stats.get('Roblox', 0)} Roblox{Colors.ENDC} | {Colors.WARNING}{distracao - stats.get('Roblox',0)} Outros{Colors.ENDC} | Total: {total}")

def run_diagnostics(watch=False):
    if watch:
        os.system('cls' if os.name == 'nt' else 'clear')

    print(f"{Colors.BOLD}{'='*75}{Colors.ENDC}")
    print(f"{Colors.HEADER}🔍 RADAR DE ATIVIDADE DO LABORATÓRIO - {datetime.now().strftime('%H:%M:%S')}{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*75}{Colors.ENDC}")

    # 1. Verificação de Processo e Recursos
    print("\n⚙️  Status do Processo:")
    proc = get_receiver_process()
    if proc:
        with proc.oneshot():
            cpu = proc.cpu_percent(interval=0.1)
            ram = proc.memory_info().rss / (1024 * 1024)
            create_time = datetime.fromtimestamp(proc.create_time()).strftime("%H:%M:%S")
        print(f"   [{Colors.OKGREEN}OK{Colors.ENDC}] lab_receiver.py em execução (PID: {proc.pid})")
        print(f"   [i] Iniciado às: {create_time}")
        print(f"   [i] Consumo: CPU: {cpu}% | RAM: {ram:.2f} MB")
    else:
        plugin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "repo", "plugins")
        receiver_script_path = os.path.join(plugin_dir, "lab_receiver.bat")

        print(f"   [{Colors.FAIL}!!{Colors.ENDC}] {Colors.FAIL}ERRO: O processo 'lab_receiver.py' NÃO está rodando.{Colors.ENDC}")
        
        # Apenas oferece para iniciar se não estiver no modo watch
        if not watch:
            try:
                choice = input(f"   {Colors.OKBLUE}[?] Deseja iniciar o receptor agora? (S/n): {Colors.ENDC}").strip().lower()
                if choice == '' or choice == 's':
                    print(f"   {Colors.OKBLUE}   [i] Iniciando '{os.path.basename(receiver_script_path)}' em uma nova janela...{Colors.ENDC}")
                    subprocess.Popen(['start', 'cmd', '/c', receiver_script_path], shell=True, cwd=plugin_dir)
                    time.sleep(3) # Pausa para o processo iniciar
                    print(f"   {Colors.OKBLUE}   [i] Re-verificando status...{Colors.ENDC}")
                    
                    # Re-verifica o processo após a tentativa de início
                    proc = get_receiver_process()
                    if proc:
                        print(f"   [{Colors.OKGREEN}OK{Colors.ENDC}] Processo iniciado com sucesso (PID: {proc.pid}).")
                    else:
                        print(f"   [{Colors.FAIL}!!{Colors.ENDC}] {Colors.FAIL}Falha ao iniciar. Verifique a janela do receptor.{Colors.ENDC}")
                        # Se falhou, tenta mostrar o último erro real do log de erros
                        error_log_path = os.path.join(plugin_dir, "receiver_errors.log")
                        if os.path.exists(error_log_path):
                            try:
                                with open(error_log_path, 'r', encoding='utf-8', errors='ignore') as f:
                                    last_error = f.readlines()[-1].strip()
                                    print(f"   {Colors.WARNING}   -> Último erro registrado: {last_error}{Colors.ENDC}")
                            except: pass
                    # Pula para a próxima seção para evitar re-executar a lógica de início
                    print("\n🌐 Teste de Interfaces de Rede (Porta 5000):")
                    goto_next_section = True # Sinaliza para pular a próxima seção

            except (KeyboardInterrupt, EOFError):
                print("\nOperação cancelada.")

    # 2. Teste de Acessibilidade por Interface
    # A variável 'goto_next_section' é usada para controlar o fluxo
    # e evitar a duplicação da impressão do cabeçalho da seção.
    if not watch and 'goto_next_section' not in locals():
        print("\n🌐 Teste de Interfaces de Rede (Porta 5000):")
        ips = get_local_ips()
        for ip in ips:
            try:
                resp = requests.get(f"http://{ip}:5000/health", timeout=0.5)
                if resp.status_code == 200:
                    print(f"   [+] {ip:<15} -> {Colors.OKGREEN}ACESSÍVEL{Colors.ENDC}")
            except:
                print(f"   [-] {ip:<15} -> {Colors.WARNING}TIMEOUT{Colors.ENDC}")

    # 3. Monitoramento de Atividade (Novo!)
    print(f"\n🖥️  {Colors.BOLD}Atividade das Máquinas:{Colors.ENDC}")
    plugin_dir = os.path.join(os.path.dirname(__file__), "data", "repo", "plugins")
    status_path = os.path.join(plugin_dir, "lab_status.json")
    activity_log = os.path.join(plugin_dir, "lab_receiver.log")
    
    lab_data = load_lab_data(status_path)
    print_monitor_table(lab_data)
    
    # Salva o resumo no arquivo de log histórico solicitado
    save_activity_log(lab_data, activity_log, watch_mode=watch)

    if not watch:
        print("\n📂 Persistência e Logs:")
        if os.path.exists(status_path):
            mtime = datetime.fromtimestamp(os.path.getmtime(status_path))
            print(f"   [{Colors.OKGREEN}OK{Colors.ENDC}] lab_status.json atualizado em: {mtime.strftime('%H:%M:%S')}")
        
        log_path = os.path.join(plugin_dir, "receiver_errors.log")
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                if lines:
                    print(f"   {Colors.WARNING}Último log:{Colors.ENDC} {lines[-1].strip()}")

    print(f"\n{Colors.BOLD}{'='*75}{Colors.ENDC}")
    if not watch:
        print("Dica: Use 'python check_serv.py --watch' para monitoramento contínuo.")

if __name__ == "__main__":
    is_watch = "--watch" in sys.argv
    try:
        if is_watch:
            while True:
                run_diagnostics(watch=True)
                time.sleep(3)
        else:
            run_diagnostics()
    except KeyboardInterrupt:
        print("\nMonitoramento encerrado.")