"""
Plugin de Monitoramento de Laboratório (SysAva)

Monitora a atividade dos computadores em tempo real, categorizando o uso
em Produtivo, Roblox, Games ou Redes Sociais.
"""

import streamlit as st
import pandas as pd
import json
import os
import sys
import subprocess
import requests
import time
import socket
from datetime import datetime

# --- Configurações de Caminho ---
PLUGIN_DIR = os.path.dirname(__file__)
MONITOR_DATA_FILE = os.path.join(PLUGIN_DIR, "lab_status.json")

# Se você está usando um Receiver público, configure aqui:
# PUBLIC_RECEIVER_URL = "https://sysava.streamlit.app" # Comentado para forçar o uso local
PUBLIC_RECEIVER_URL = None
AUTH_TOKEN = None  # Se o receiver exigir Bearer token, defina aqui
LOCAL_RECEIVER_URL = "http://127.0.0.1:5000"

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from services import database as db
except ImportError:
    db = None
    
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

@st.cache_resource
def start_receiver():
    # Se o receiver remoto estiver configurado, não inicia o local.
    if PUBLIC_RECEIVER_URL:
        return None

    # Evita abrir múltiplos processos se a porta 5000 (do receiver) já estiver ocupada
    if is_port_in_use(5000):
        return None
        
    receiver_path = os.path.join(PLUGIN_DIR, "lab_receiver.py")
    if os.path.exists(receiver_path):
        # Starts the Flask receiver in the background without blocking Streamlit
        log_path = os.path.join(PLUGIN_DIR, "receiver_errors.log")
        with open(log_path, "a") as f:
            f.write(f"\n--- Início do Log: {datetime.now()} ---\n")
            return subprocess.Popen([sys.executable, receiver_path], cwd=PLUGIN_DIR, stdout=f, stderr=f)
    return None

start_receiver()

def load_monitor_data():
    """
    Carrega o status priorizando a RAM (via API do Receiver).
    Caminho: Publico > Local > JSON (Registros/Vigilância)
    """
    headers = {}
    if AUTH_TOKEN:
        headers['Authorization'] = f"Bearer {AUTH_TOKEN}"

    data = {}
    if PUBLIC_RECEIVER_URL:
        try:
            response = requests.get(f"{PUBLIC_RECEIVER_URL.rstrip('/')}/api/status", timeout=1, headers=headers)
            if response.status_code == 200:
                return response.json()
        except:
            pass

    try:
        # Tenta buscar o estado ultra-latente na RAM do Receiver local
        response = requests.get(f"{LOCAL_RECEIVER_URL}/api/status", timeout=0.5, headers=headers)
        if response.status_code == 200:
            return response.json()
    except:
        pass

    # Fallback para o registro em disco (Histórico/Vigilância)
    if os.path.exists(MONITOR_DATA_FILE):
        try:
            with open(MONITOR_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return {}
    return {}

def save_monitor_data(data):
    with open(MONITOR_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def show_lab_monitor():
    st.title("🖥️ Radar de Atividade do Laboratório")

    if db is None:
        st.error("Banco de dados não disponível.")
        return

    # Carrega nome da escola (conforme run.bat) para a estrutura de pastas
    school_name = "SysAva"
    school_file = os.path.join(project_root, "data", "Turmas", "Escola.txt")
    if os.path.exists(school_file):
        try:
            with open(school_file, 'r', encoding='utf-8') as f:
                school_name = f.read().strip()
        except: pass

    # --- BARRA LATERAL: Configurações e Filtros ---
    with st.sidebar:
        st.header("🔍 Filtros de Monitoramento")
        classes = db.get_classes()
        class_options = {c['name']: c['id'] for c in classes}
        sel_class_name = st.selectbox("Selecione a Turma Atual", ["-- Selecione --"] + list(class_options.keys()))
        st.session_state['last_lab_class'] = sel_class_name
        
        # Seleção de Disciplina e Alunos para estruturação de pastas
        sel_disc_name = "-- Selecione --"
        all_students = []
        if sel_class_name != "-- Selecione --":
            class_id = class_options[sel_class_name]
            all_students = db.get_students_by_class(class_id)
            try:
                disciplines = db.get_disciplines_by_class(class_id)
                disc_options = [d['name'] for d in disciplines]
                sel_disc_name = st.selectbox("Selecione a Disciplina", ["-- Selecione --"] + disc_options)
            except:
                sel_disc_name = st.text_input("Disciplina (Nome Manual)")

        st.divider()
        if st.button("🔄 Forçar Atualização do Radar", use_container_width=True):
            st.rerun()
        
        st.divider()
        st.markdown("### 🛠️ Depuração")
        
        with st.expander("🔍 Ver Diagnóstico do Servidor"):
            if st.button("Carregar Diagnóstico na Página Principal", use_container_width=True):
                st.session_state['monitor_view'] = 'diagnostics'
                st.rerun()

        if st.button("🗑️ Limpar Todos os Dados", type="secondary", use_container_width=True):
            save_monitor_data({})
            st.success("Radar resetado!")
            st.rerun()

        st.caption("Dica: O Agente local deve enviar o IP da máquina para rastreamento preciso.")

    # --- ROTEADOR DE VISUALIZAÇÃO (DENTRO DO PLUGIN) ---
    if st.session_state.get('monitor_view') == 'diagnostics':
        st.subheader("🔍 Diagnóstico do Servidor")

        # Aponta para o novo endpoint de dados JSON
        diagnostic_url = f"{PUBLIC_RECEIVER_URL.rstrip('/') if PUBLIC_RECEIVER_URL else LOCAL_RECEIVER_URL}/api/diagnostics"
        try:
            with st.spinner("Buscando dados do servidor..."):
                response = requests.get(diagnostic_url, timeout=2)
                response.raise_for_status()
                data = response.json()

                # Renderiza os dados usando componentes do Streamlit
                st.metric("Uptime do Servidor", f"{data.get('uptime', 0)} segundos")

                st.markdown("---")
                st.markdown("### 🌐 Scanner de Rede")

                # Botão para iniciar a varredura (agora aciona o endpoint /scan)
                scan_url = f"{PUBLIC_RECEIVER_URL.rstrip('/') if PUBLIC_RECEIVER_URL else LOCAL_RECEIVER_URL}/scan"
                if st.button("Iniciar Varredura de Rede", disabled=data.get('is_scanning', False)):
                    requests.post(scan_url, timeout=1)
                    st.toast("Comando de varredura enviado!")
                    time.sleep(1) # Pequena pausa para o servidor processar
                    st.rerun()

                if data.get('is_scanning'):
                    st.info("Varredura de rede em andamento...")

                scan_results = data.get('scan_results', [])
                if scan_results:
                    # Garante que as colunas principais sempre existam
                    df_scan = pd.DataFrame(scan_results, columns=['ip', 'status', 'mac'])
                    # Preenche valores nulos para evitar erros de renderização
                    df_scan['ip'] = df_scan['ip'].fillna('N/A')
                    df_scan['status'] = df_scan['status'].fillna('Desconhecido')
                    df_scan['mac'] = df_scan['mac'].fillna('N/A')
                    st.dataframe(df_scan, use_container_width=True)
                else:
                    st.info("Nenhum resultado de varredura disponível.")

        except requests.exceptions.RequestException as e:
            st.error(f"Não foi possível conectar ao servidor de diagnóstico: {e}")
        
        if st.button("⬅️ Voltar ao Radar"):
            st.session_state['monitor_view'] = 'radar'
            st.rerun()
        return

    # --- VISUALIZAÇÃO PADRÃO (RADAR) ---
    # Carrega dados simulando o que viria dos computadores do laboratório
    lab_data = load_monitor_data()
    
    if not lab_data:
        st.info("📡 Aguardando sinal dos computadores ou registros manuais de alunos...")
        # Adiciona um botão para permitir o acesso ao diagnóstico mesmo sem dados
        st.info("Se o servidor estiver online mas sem agentes, você ainda pode acessar o diagnóstico pela barra lateral.")
        return

    # --- SEÇÃO 1: ESTATÍSTICAS ---
    st.subheader("📊 Estatísticas de Uso")
    
    df = pd.DataFrame.from_dict(lab_data, orient='index').reset_index().rename(columns={'index': 'Maquina'})
    
    c1, c2, c3, c4 = st.columns(4)
    total = len(df)
    roblox_count = len(df[df['category'] == 'Roblox'])
    games_count = len(df[df['category'] == 'Games'])
    social_count = len(df[df['category'] == 'Social'])
    produtivo_count = len(df[df['category'] == 'Produtivo'])

    c1.metric("Online", total)
    c2.metric("No Roblox 🎮", roblox_count, delta=f"{roblox_count/total*100:.0f}%", delta_color="inverse")
    c3.metric("Em Games/Redes 🌐", games_count + social_count, delta_color="inverse")
    c4.metric("Produtivos ✅", produtivo_count)

    # Gráfico de pizza simples usando Streamlit
    st.write("Distribuição de Atividade:")
    chart_data = df['category'].value_counts()
    st.bar_chart(chart_data)

    st.divider()

    # --- SEÇÃO 2: MONITOR AO VIVO E CONTROLE ---
    st.subheader("👁️ Monitoramento e Controle Direto")

    # Formatação de cores para a tabela
    def style_category(val):
        colors = {
            'Roblox': 'background-color: #ff4b4b; color: white; font-weight: bold',
            'Games': 'background-color: #ffa500; color: white; font-weight: bold',
            'Social': 'background-color: #1c83e1; color: white; font-weight: bold',
            'Produtivo': 'background-color: #28a745; color: white; font-weight: bold',
            'Celular (Proibido)': 'background-color: #7030a0; color: white; font-weight: bold'
        }
        return colors.get(val, 'color: white')

    # Exibe a tabela com o status
    st.dataframe(
        df.style.map(style_category, subset=['category']),
        hide_index=True,
        use_container_width=True,
        column_config={
            "Maquina": st.column_config.TextColumn("Máquina", width="small"),
            "user": st.column_config.TextColumn("Usuário", width="medium"),
            "activity": st.column_config.TextColumn("Janela Ativa", width="large"),
            "category": st.column_config.TextColumn("Categoria"),
            "last_seen": st.column_config.TextColumn("Última Atualização"),
            "ip": st.column_config.TextColumn("IP Identificado"),
            "ports": st.column_config.ListColumn("Portas Abertas")
        }
    )

    st.divider()

    # --- SEÇÃO 3: RASTREAMENTO MANUAL (CELULAR OU PCs EXTERNOS) ---
    if sel_class_name != "-- Selecione --":
        with st.expander("📱 Monitorar Alunos Externos (Celular/BYOD)"):
            st.markdown("Alunos nesta turma que não estão nas máquinas do laboratório:")
            
            class_id = class_options[sel_class_name]
            all_students = db.get_students_by_class(class_id)
            
            # Alunos que NÃO estão na lista de monitoramento automático do radar
            monitored_users = df['user'].tolist()
            external_candidates = [s for s in all_students if s['username'] not in monitored_users]
            
            if not external_candidates:
                st.success("Todos os alunos desta turma já estão sendo monitorados automaticamente.")
            else:
                col_ext1, col_ext2, col_ext3 = st.columns([0.4, 0.3, 0.3])
                
                student_options = {f"{s['name']} ({s['username']})": s['username'] for s in external_candidates}
                targets = col_ext1.multiselect("Selecionar Alunos", list(student_options.keys()))
                status_ext = col_ext2.selectbox("Status Manual", ["Produtivo", "Celular (Proibido)", "Roblox", "Games", "Social"], key="man_status")
                
                if col_ext3.button("➕ Adicionar ao Radar", use_container_width=True):
                    for label in targets:
                        uname = student_options[label]
                        real_name = label.split(" (")[0]
                        
                        # Recupera o último IP registrado no histórico de login desse usuário
                        hist = db.get_user_history(uname)
                        detected_ip = "N/A"
                        for h in hist:
                            if "IP:" in h['activity']:
                                detected_ip = h['activity'].split("IP: ")[1].split(")")[0]
                                break

                        lab_data[f"EXT-{uname[-4:]}"] = {
                            "user": uname,
                            "activity": f"Acesso Externo ({real_name})",
                            "category": status_ext,
                            "last_seen": datetime.now().strftime("%H:%M:%S"),
                            "ip": detected_ip,
                            "manual": True
                        }
                    save_monitor_data(lab_data)
                    st.rerun()

    st.divider()
    
    # --- PAINEL DE COMANDO ---
    st.subheader("🕹️ Central de Intervenção")
    
    col_ctrl1, col_ctrl2 = st.columns([0.4, 0.6])
    
    with col_ctrl1:
        target = st.multiselect("Selecionar Máquinas", df['Maquina'].tolist(), placeholder="Escolha os alvos...")
        action = st.selectbox("Ação de Controle", [
            "Enviar Alerta Visual", 
            "Bloquear Processo (Fechar Roblox/Game)", 
            "Bloquear Navegador",
            "Registrar Uso Indevido de Celular",
            "Forçar Logoff (Deslogar PC)",
            "Desligar PC (Shutdown)",
            "Reiniciar PC (Restart)",
            "Instalar Kit Lab DS (Winget)",
            "Estruturar Pastas de Projetos"
        ])

    with col_ctrl2:
        msg = ""
        if "Alerta" in action:
            msg = st.text_input("Mensagem do Alerta", value="Foco na atividade! Feche o jogo imediatamente.")
        
        if st.button("🚀 Executar Comando Remoto", type="primary", use_container_width=True):
            if not target:
                st.warning("Selecione pelo menos uma máquina alvo.")
            else:
                prof = st.session_state.get('usuario', 'Professor')
                for t in target:
                    if t in lab_data:
                        u_name = lab_data[t].get('user', 'desconhecido')
                        
                        # Se for celular, muda a categoria no radar visual imediatamente
                        if action == "Registrar Uso Indevido de Celular":
                            lab_data[t]['category'] = "Celular (Proibido)"
                            lab_data[t]['activity'] = "📱 Celular flagrado pelo professor"
                            if db:
                                db.add_user_history(u_name, f"🚩 INFRAÇÃO: Uso de celular sem permissão (Registrado por {prof})")
                        
                        # Lógica para Estruturar Pastas
                        current_msg = msg
                        if action == "Estruturar Pastas de Projetos":
                            if sel_disc_name in ["-- Selecione --", ""]:
                                st.error("Selecione uma disciplina na barra lateral primeiro.")
                                break
                            
                            # Identifica o nome real do aluno para a pasta
                            student_info = next((s for s in all_students if s['username'] == u_name), None)
                            real_name = student_info['name'] if student_info else u_name
                            current_msg = f"{school_name}|{sel_class_name}|{sel_disc_name}|{real_name}"

                        # Registra o comando no JSON para o Agente ler (caso seja PC)
                        lab_data[t]['pending_command'] = action
                        lab_data[t]['command_msg'] = current_msg
                        lab_data[t]['command_ts'] = datetime.now().strftime("%H:%M:%S")
                
                save_monitor_data(lab_data)
                st.success(f"Comando '{action}' enviado para: {', '.join(target)}")

                # Registra no histórico de auditoria do SysAva
                if db:
                    db.add_user_history(prof, f"Enviou '{action}' para {len(target)} máquinas no laboratório.")
                st.rerun()

    # Histórico de infrações (Dinâmico do Banco)
    with st.expander("📜 Histórico de Desvios e Infrações (Hoje)"):
        if db:
            all_hist = db.get_all_history(limit=100)
            today_str = datetime.now().strftime("%Y-%m-%d")
            
            infractions = []
            for h in all_hist:
                # Filtra apenas registros de hoje que contenham termos de controle ou infração
                if today_str in h.get('timestamp', ''):
                    act = h.get('activity', '')
                    if any(term in act for term in ["INFRAÇÃO", "Enviou '", "Bloqueio", "Celular"]):
                        infractions.append({
                            "Hora": h['timestamp'].split('T')[-1][:5] if 'T' in h['timestamp'] else h['timestamp'],
                            "Usuário/RA": h['username'],
                            "Ocorrência": act.replace("🚩 INFRAÇÃO: ", "")
                        })
            
            if infractions:
                st.dataframe(infractions, hide_index=True, use_container_width=True)
            else:
                st.info("Nenhuma infração registrada hoje até o momento.")
        else:
            st.info("Conecte ao banco de dados para ver o histórico real.")

if __name__ == "__main__":
    # Detecção de contexto Streamlit
    is_streamlit = False
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx(): is_streamlit = True
    except: pass

    if is_streamlit:
        show_lab_monitor()
    else:
        print("Este plugin deve ser executado dentro do ambiente Streamlit do SysAva.")