import socket
import concurrent.futures
import subprocess
import os
import platform
import time

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def ping_host(ip):
    """Verifica se um host está ativo na rede."""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-w', '500', ip]
    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            # Se o host responder ao ping, tenta verificar se o agente do SysAva está lá (opcional)
            return (ip, "ATIVO")
    except:
        pass
    return None

def scan_network():
    local_ip = get_local_ip()
    prefix = ".".join(local_ip.split('.')[:-1]) + "."
    
    # Define faixas de busca: Rede Local Detectada e faixas comuns de Gateway/Wi-fi
    subnets = ["192.168.10.", "192.168.11.", prefix]
    subnets = list(set(subnets)) # Remove duplicatas

    # Tenta listar vizinhos IPv6 (Link-Local)
    print(f"🛰️  Buscando vizinhos IPv6 (Link-Local)...")
    try:
        v6_output = subprocess.check_output(["netsh", "interface", "ipv6", "show", "neighbors"], text=True)
        v6_nodes = re.findall(r'fe80::[a-f0-9:]+', v6_output.lower())
        for node in set(v6_nodes):
            print(f"   [v6] Vizinho detectado: {node}")
    except:
        pass

    print(f"🚀 Iniciando Sniffer SysAva...")
    print(f"📍 IP Local: {local_ip}")
    print(f"🔍 Escaneando sub-redes: {subnets}")
    print("-" * 50)

    try:
        found_count = 0
        for subnet in subnets:
            print(f"🛰️  Sondando faixa {subnet}x...")
            ips = [f"{subnet}{i}" for i in range(1, 255)]
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                # O list() força a espera, envolvemos em try/except para sair rápido
                results = list(executor.map(ping_host, ips))
                
                for res in results:
                    if res:
                        print(f"   [+] Host encontrado: {res[0]} - Status: {res[1]}")
                        found_count += 1
    except KeyboardInterrupt:
        print("\n\n🛑 Varredura interrompida pelo usuário.")
        return

    print("-" * 50)
    print(f"🏁 Varredura concluída. {found_count} máquinas respondendo na rede.")
    print("Dica: Se as máquinas estão ativas mas não aparecem no monitor, verifique o Firewall (Porta 5000).")

if __name__ == "__main__":
    # Loop de teste para manter o feedback visual constante
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        scan_network()
        print("\nPróxima varredura em 30 segundos... (Ctrl+C para sair)")
        time.sleep(30)