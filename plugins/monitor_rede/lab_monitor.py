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
# O código-fonte deste plugin fica em plugins/monitor_rede; o runtime do
# monitor (receiver, status, usuários, tela, agente...) fica em
# data/repo/plugins/monitor. SYSAVA_PLUGIN_DIR sobrescreve.
_PASTA_ARQUIVO = os.path.dirname(os.path.abspath(__file__))


def _achar_raiz_projeto():
    """Sobe a partir do arquivo até achar app.py ou data/repo/plugins."""
    atual = _PASTA_ARQUIVO
    for _ in range(8):
        if (os.path.exists(os.path.join(atual, "app.py"))
                or os.path.isdir(os.path.join(atual, "data", "repo", "plugins"))):
            return atual
        pai = os.path.dirname(atual)
        if pai == atual:
            break
        atual = pai
    return _PASTA_ARQUIVO


_PROJETO_RAIZ = _achar_raiz_projeto()


def _resolver_plugin_dir():
    candidatos = [
        os.environ.get("SYSAVA_PLUGIN_DIR", ""),
        os.path.join(_PROJETO_RAIZ, "data", "repo", "plugins", "monitor"),
        os.path.join(_PROJETO_RAIZ, "data", "repo", "plugins"),
        _PASTA_ARQUIVO,
    ]
    for c in candidatos:
        if not c:
            continue
        if (os.path.exists(os.path.join(c, "lab_receiver.py"))
                or os.path.exists(os.path.join(c, "lab_status.json"))):
            return os.path.abspath(c)
    return _PASTA_ARQUIVO


PLUGIN_DIR = _resolver_plugin_dir()
MONITOR_DATA_FILE = os.path.join(PLUGIN_DIR, "lab_status.json")
LABELS_FILE = os.path.join(PLUGIN_DIR, "lab_labels.json")
USERS_MAP_FILE = os.path.join(PLUGIN_DIR, "lab_users.json")

# Se você está usando um Receiver público, configure aqui:
# PUBLIC_RECEIVER_URL = "https://sysava.streamlit.app" # Comentado para forçar o uso local
PUBLIC_RECEIVER_URL = None
AUTH_TOKEN = None  # Se o receiver exigir Bearer token, defina aqui
LOCAL_RECEIVER_URL = "http://127.0.0.1:5000"
OFFLINE_SECONDS = 60  # sem sinal por mais que isso, some do radar
# Validade do comando pendente (evita desligar/reiniciar horas depois).
try:
    COMMAND_TTL_SECONDS = int(os.environ.get("COMMAND_TTL_SECONDS") or 1800)
except ValueError:
    COMMAND_TTL_SECONDS = 1800
# Tempo maximo para exibir o aluno associado pela tela de bloqueio.
try:
    USER_MAP_TTL_SECONDS = int(os.environ.get("USER_MAP_TTL_SECONDS") or 57600)
except ValueError:
    USER_MAP_TTL_SECONDS = 57600

# Espelha a lista de bloqueio do agente (lab_agent.py) apenas para exibição na UI.
BLOCKED_PLATFORMS_INFO = (
    "Roblox, Fortnite/Epic, League of Legends e sites/proxies de jogos no "
    "navegador (Loki, Poki, Friv, Y8, ClickJogos, Gartic...), fechados sempre."
)

# --- Detecção de Ambiente (Local vs. Nuvem) ---
IS_CLOUD_ENVIRONMENT = "STREAMLIT_SERVER_RUN_ON_SAVE" in os.environ or "PROJECT_GIT_HASH" in os.environ

def get_receiver_base_url():
    """Retorna a URL base do receiver, priorizando a pública se configurada e não em ambiente de nuvem."""
    if PUBLIC_RECEIVER_URL and not IS_CLOUD_ENVIRONMENT:
        return PUBLIC_RECEIVER_URL.rstrip('/')
    return LOCAL_RECEIVER_URL

def get_local_ip():
    """Obtém o IP real da interface de rede ativa (evita 127.0.0.1)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Não precisa ser alcançável; serve só para o SO escolher a interface correta.
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_dashboard_base_url():
    """URL do painel web acessível pela rede (IP real, nunca loopback).

    Sobrescreva com a variável de ambiente SYSAVA_SERVER_URL quando o IP
    precisar ser fixo (ex.: http://192.168.0.10:5000).
    """
    override = os.environ.get("SYSAVA_SERVER_URL", "").strip()
    if override:
        return override.rstrip('/')
    if PUBLIC_RECEIVER_URL and not IS_CLOUD_ENVIRONMENT:
        return PUBLIC_RECEIVER_URL.rstrip('/')
    return f"http://{get_local_ip()}:5000"

if _PROJETO_RAIZ not in sys.path:
    sys.path.insert(0, _PROJETO_RAIZ)

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
        response = requests.get(f"{get_receiver_base_url()}/api/status", timeout=0.5, headers=headers)
        if response.status_code == 200:
            return response.json()
    except:
        pass

    # Fallback para o registro em disco (Histórico/Vigilância)
    if os.path.exists(MONITOR_DATA_FILE):
        try:
            with open(MONITOR_DATA_FILE, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            agora = time.time()
            return {
                k: v for k, v in dados.items()
                if isinstance(v, dict) and (agora - v.get('timestamp', 0)) < OFFLINE_SECONDS
            }
        except: return {}
    return {}

def save_monitor_data(data):
    # Nao grava no JSON local as maquinas que pertencem ao outro servidor (peer).
    limpo = {
        k: v for k, v in data.items()
        if isinstance(v, dict) and v.get('_owner') in (None, 'local')
    }
    # Preserva comandos enfileirados pelo receiver (/api/command) que o estado
    # em memoria do Streamlit pode nao ter visto (evita perder a fila).
    atual = {}
    try:
        if os.path.exists(MONITOR_DATA_FILE):
            with open(MONITOR_DATA_FILE, 'r', encoding='utf-8') as f:
                atual = json.load(f)
    except Exception:
        atual = {}
    for nome, info in limpo.items():
        antigo = atual.get(nome) if isinstance(atual.get(nome), dict) else {}
        fila = antigo.get('pending_queue')
        if isinstance(fila, list) and fila:
            info['pending_queue'] = fila
        if antigo.get('pending_command') and not info.get('pending_queue'):
            info['pending_command'] = antigo['pending_command']
            for chave in ('command_msg', 'command_ts', 'command_created_at', 'command_expires_at'):
                if chave in antigo:
                    info[chave] = antigo[chave]
    with open(MONITOR_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(limpo, f, indent=4, ensure_ascii=False)

def _local_api_token():
    """Token local do receiver (mesma pasta); protege /api/command."""
    p = os.path.join(PLUGIN_DIR, "receiver_secret.key")
    try:
        with open(p, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""

def _enviar_comando_receiver(maquinas, action, msg=""):
    """Envia o comando ao receiver local; ele encaminha ao peer se a maquina for dele."""
    try:
        base = get_receiver_base_url().rstrip('/')
        headers = {}
        tok = _local_api_token()
        if tok:
            headers["X-SysAva-Token"] = tok
        r = requests.post(base + "/api/command",
                          json={"maquinas": maquinas, "acao": action, "msg": msg},
                          headers=headers, timeout=5)
        return r.status_code == 200
    except Exception:
        return False

def _enfileirar_comando(lab_data, targets, action, msg=""):
    """Envia o comando pelo receiver; so grava localmente se o receiver falhar."""
    if _enviar_comando_receiver(targets, action, msg):
        return
    ts = datetime.now().strftime("%H:%M:%S")
    agora = time.time()
    for t in targets:
        if t in lab_data:
            fila = lab_data[t].get('pending_queue')
            if not isinstance(fila, list):
                fila = []
            igual = (action, msg or "")
            if not any(isinstance(c, dict) and (c.get('cmd'), c.get('msg') or '') == igual for c in fila):
                fila.append({
                    'cmd': action,
                    'msg': msg,
                    'ts': ts,
                    'created_at': agora,
                    'expires_at': agora + COMMAND_TTL_SECONDS,
                })
            lab_data[t]['pending_queue'] = fila[-50:]

def load_labels():
    """Lê o mapa máquina (hostname) -> rótulo amigável (ex.: PC1-Fila1)."""
    if os.path.exists(LABELS_FILE):
        try:
            with open(LABELS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_labels(labels):
    with open(LABELS_FILE, 'w', encoding='utf-8') as f:
        json.dump(labels, f, indent=4, ensure_ascii=False)

def load_users_map():
    """Lê o mapa máquina -> aluno (RA/nome) associado pela tela de bloqueio."""
    if os.path.exists(USERS_MAP_FILE):
        try:
            with open(USERS_MAP_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _lookup_ci(mapa, chave):
    """Busca em dict sem diferenciar maiusculas/minusculas (hostnames)."""
    if not isinstance(mapa, dict) or not chave:
        return None
    if chave in mapa:
        return mapa[chave]
    alvo = str(chave).strip().lower()
    for k, v in mapa.items():
        if str(k).strip().lower() == alvo:
            return v
    return None

def _data_curta(u, ts):
    """Data dd/mm da ultima associacao (logged_date ou timestamp)."""
    logged = str(u.get('logged_date') or '').strip()
    if logged:
        try:
            return datetime.strptime(logged[:10], '%Y-%m-%d').strftime('%d/%m')
        except ValueError:
            return logged[:10]
    if ts:
        try:
            return datetime.fromtimestamp(ts).strftime('%d/%m')
        except (OSError, ValueError, OverflowError):
            return ''
    return ''

def _fmt_aluno(u):
    """Nome (RA) do aluno associado; associacao vencida mostra a data."""
    if not u:
        return ""
    try:
        ts = float(u.get('ts') or 0)
    except (TypeError, ValueError):
        ts = 0
    name = (u.get('name') or '').strip()
    ra = (u.get('ra') or '').strip()
    if not name and not ra:
        return ""
    texto = f"{name} ({ra})" if name and ra else (name or ra)
    if ts and (time.time() - ts) > USER_MAP_TTL_SECONDS:
        data = _data_curta(u, ts)
        if data:
            return f"{texto} — último em {data}"
    return texto

def _dt_local(ts):
    """Converte um timestamp (ISO, possivelmente UTC) para datetime local."""
    try:
        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        if dt.tzinfo is not None:
            dt = dt.astimezone()
        return dt
    except Exception:
        return None

def _render_diagnostico_servidor():
    """Diagnóstico do receiver (uptime + scanner de rede) — aba Diagnóstico."""
    st.subheader("🔍 Diagnóstico do Servidor")
    if IS_CLOUD_ENVIRONMENT:
        st.info("O diagnóstico de rede só está disponível ao rodar o SysAva localmente.")
        return

    diagnostic_url = f"{get_receiver_base_url()}/api/diagnostics"
    try:
        with st.spinner("Buscando dados do servidor..."):
            response = requests.get(diagnostic_url, timeout=2)
            response.raise_for_status()
            data = response.json()

            st.metric("Uptime do Servidor", f"{data.get('uptime', 0)} segundos")

            st.markdown("---")
            st.markdown("### 🌐 Scanner de Rede")

            scan_url = f"{get_receiver_base_url()}/scan"
            if st.button("Iniciar Varredura de Rede", disabled=data.get('is_scanning', False)):
                requests.post(scan_url, timeout=1)
                st.toast("Comando de varredura enviado!")
                time.sleep(1)
                st.rerun()

            if data.get('is_scanning'):
                st.info("Varredura de rede em andamento...")

            scan_results = data.get('scan_results', [])
            if scan_results:
                df_scan = pd.DataFrame(scan_results, columns=['ip', 'status', 'mac'])
                df_scan['ip'] = df_scan['ip'].fillna('N/A')
                df_scan['status'] = df_scan['status'].fillna('Desconhecido')
                df_scan['mac'] = df_scan['mac'].fillna('N/A')
                st.dataframe(df_scan, use_container_width=True)
            elif not data.get('is_scanning'):
                st.info("Nenhum resultado de varredura disponível.")

    except requests.exceptions.RequestException as e:
        st.error(f"Não foi possível conectar ao servidor de diagnóstico: {e}")

def _render_baixar_pacote(dash_url):
    """Card de download do pacote de atualização (servidor.zip)."""
    st.markdown("### ⬇️ Pacote de atualização")
    st.caption(
        "Scripts do servidor (receiver, watchdog, bandeja/tray e diagnóstico) para "
        "atualizar outro PC ou restaurar esta pasta."
    )
    st.link_button("⬇️ Baixar servidor.zip", dash_url.rstrip('/') + "/servidor.zip")
    st.caption("Copie por cima da pasta `plugins` do PC de destino e rode `reiniciar_servidor.bat`.")


def build_estrutura_payload(base, turma, disciplina, aulas, aluno=None):
    """Payload (JSON) do comando 'Estruturar Pastas' enviado ao agente.

    Contrato com `_criar_estrutura_atividades` (lab_agent.py): o agente cria
    `<base>/<turma>/<disciplina>/<aluno>/Aula_NN` (espaços viram `_`).
    """
    return json.dumps({
        "base": base,
        "turma": turma,
        "disciplina": disciplina,
        "aluno": str(aluno or ""),
        "aulas": str(aulas or ""),
    }, ensure_ascii=False)


def show_lab_monitor():
    st.title("🖥️ Radar de Atividade do Laboratório")

    if db is None:
        st.error("Banco de dados não disponível.")
        return

    _base = get_receiver_base_url().rstrip('/')
    try:
        _health = requests.get(_base + "/health", timeout=1.5).json()
        _peers = requests.get(_base + "/api/peer/state", timeout=1.5).json().get("peers") or []
        _papel = _health.get("role", "?")
        _rotulo = "primário" if _papel == "primary" else "auxiliar"
        st.caption(
            f"Servidor local: **online** ({_rotulo}) | peers: {len(_peers)} | "
            f"máquinas: {_health.get('machines_connected', 0)} | v{_health.get('version', '?')}"
        )
        if not _peers:
            st.info(
                "Nenhum **servidor auxiliar** conectado. No PC do laboratório (ex.: PC01-LAB02) "
                "rode `tray_servidor.bat` (ícone na bandeja, inicia no logon) ou "
                "`instalar_servidor_auto.bat`; se não aparecer, rode `diagnostico_servidor.bat`."
            )
    except Exception:
        st.warning(
            "Servidor auxiliar local **offline** — o radar está lendo o último arquivo salvo. "
            "Inicie-o com `tray_servidor.bat` ou `INICIAR_SERVIDOR.bat` na pasta do servidor."
        )

    _dash_url = get_dashboard_base_url().rstrip('/') + "/"
    st.link_button("🌐 Abrir Dashboard Web do Monitor", _dash_url)
    st.caption(f"Dashboard completo (login do professor): {_dash_url}")

    # Pasta padrão (token expandido no PC do aluno pelo agente), usada em Ferramentas.
    base_pastas_padrao = "%USERPROFILE%\\Documents\\SysAva"
    prof = st.session_state.get('usuario', 'Professor')

    # --- BARRA LATERAL: servidor/utilitários (as funções ficam nas abas) ---
    with st.sidebar:
        st.header("⚙️ Servidor")
        if st.button("🔄 Forçar Atualização do Radar", use_container_width=True):
            st.rerun()
        st.link_button("🌐 Abrir Dashboard Web", _dash_url, use_container_width=True)
        st.caption(f"Painel web (login do professor): {_dash_url}")

        st.divider()
        st.link_button("⬇️ Pacote de atualização (servidor.zip)",
                       _dash_url.rstrip('/') + "/servidor.zip",
                       use_container_width=True)

        st.divider()
        with st.expander("🛡️ Modo não invasivo (Hosts)"):
            st.caption(
                "Para PCs sem o agente instalado: rode o script **bloquear_hosts.bat** "
                "em cada máquina (duplo-clique, requer Administrador). Ele bloqueia o "
                "Roblox pelo arquivo `hosts` do Windows, sem instalar nada, e pode ser "
                "removido a qualquer momento."
            )
            st.code(os.path.join(PLUGIN_DIR, "bloquear_hosts.bat"), language="text")

        if st.button("🗑️ Limpar Todos os Dados", type="secondary", use_container_width=True):
            save_monitor_data({})
            st.success("Radar resetado!")
            st.rerun()

        st.caption("Dica: o agente local deve enviar o IP da máquina para rastreamento preciso.")

    lab_data = load_monitor_data()

    tabs = st.tabs([
        "📊 Radar",
        "🕹️ Controle",
        "🧰 Ferramentas",
        "⚡ Ações em Massa",
        "📜 Histórico",
        "🔍 Diagnóstico",
    ])
    tab_radar, tab_controle, tab_ferramentas, tab_massa, tab_hist, tab_diag = tabs

    with tab_diag:
        _render_diagnostico_servidor()

    if not lab_data:
        with tab_radar:
            st.info("📡 Aguardando sinal dos computadores ou registros manuais de alunos...")
            st.info("Com o servidor online e sem agentes, use a aba **Diagnóstico**.")
        with tab_controle:
            st.info("Nenhuma máquina no radar. Inicie o agente (`lab_agent`) nos PCs do laboratório.")
        with tab_ferramentas:
            _render_baixar_pacote(_dash_url)
        with tab_massa:
            st.info("Nenhuma máquina no radar.")
        with tab_hist:
            st.info("Nenhuma atividade registrada ainda.")
        return

    # --- DADOS E RÓTULOS (usados por todas as abas) ---
    df = pd.DataFrame.from_dict(lab_data, orient='index').reset_index().rename(columns={'index': 'Maquina'})
    for col in [c for c in df.columns if str(c).startswith('_')]:
        df = df.drop(columns=[col])

    labels = load_labels()
    users_map = load_users_map()
    df['Rotulo'] = df['Maquina'].map(lambda m: _lookup_ci(labels, m) or m)
    df['Aluno'] = df['Maquina'].map(lambda m: _fmt_aluno(_lookup_ci(users_map, m)) or 'Não logado')
    for col in ('maquina', 'timestamp'):
        if col in df.columns:
            df = df.drop(columns=[col])
    df = df[['Rotulo', 'Aluno'] + [c for c in df.columns if c not in ('Rotulo', 'Aluno')]]

    def _tela_label(info):
        try:
            exp = int((info or {}).get('lock_released_until') or 0)
        except (TypeError, ValueError):
            exp = 0
        if exp > int(time.time()):
            return 'liberada ' + datetime.fromtimestamp(exp).strftime('%H:%M')
        if (info or {}).get('lock_running'):
            return 'bloqueada'
        if (info or {}).get('lock_ok'):
            return 'liberada (aluno)'
        if 'lock_running' in (info or {}):
            return 'sem tela de bloqueio'
        return '-'

    df['Tela'] = df['Maquina'].map(lambda m: _tela_label(lab_data.get(m, {})))

    maquinas = df['Maquina'].tolist()
    opcoes_maquinas = {f"{labels.get(m, m)} · {m}": m for m in maquinas}

    def _style_category(val):
        colors = {
            'Roblox': 'background-color: #ff4b4b; color: white; font-weight: bold',
            'Games': 'background-color: #ffa500; color: white; font-weight: bold',
            'Social': 'background-color: #1c83e1; color: white; font-weight: bold',
            'Anônimo': 'background-color: #111111; color: #ff4b4b; font-weight: bold',
            'Produtivo': 'background-color: #28a745; color: white; font-weight: bold',
            'Celular (Proibido)': 'background-color: #7030a0; color: white; font-weight: bold'
        }
        return colors.get(val, 'color: white')

    # ============================ ABA RADAR ============================
    with tab_radar:
        st.subheader("📊 Estatísticas de Uso")

        c1, c2, c3, c4 = st.columns(4)
        total = len(df)
        roblox_count = len(df[df['category'] == 'Roblox'])
        games_count = len(df[df['category'] == 'Games'])
        social_count = len(df[df['category'] == 'Social'])
        produtivo_count = len(df[df['category'] == 'Produtivo'])

        c1.metric("Online", total)
        c2.metric("No Roblox 🎮", roblox_count,
                  delta=f"{roblox_count/total*100:.0f}%" if total else None,
                  delta_color="inverse")
        c3.metric("Em Games/Redes 🌐", games_count + social_count, delta_color="inverse")
        c4.metric("Produtivos ✅", produtivo_count)

        st.write("Distribuição de Atividade:")
        contagem = df['category'].value_counts()
        ordem = ["Produtivo", "Games", "Roblox", "Social", "Anônimo", "Celular (Proibido)"]
        categorias = [c for c in ordem if c in contagem.index] + \
                     [c for c in contagem.index if c not in ordem]
        dist_data = pd.DataFrame({
            "Categoria": categorias,
            "Máquinas": [int(contagem[c]) for c in categorias],
        })
        st.bar_chart(dist_data, x="Categoria", y="Máquinas", horizontal=True, color="#1a73e8")

        st.divider()
        st.subheader("👁️ Monitoramento ao Vivo")
        st.dataframe(
            df.style.map(_style_category, subset=['category']),
            hide_index=True,
            use_container_width=True,
            column_config={
                "Rotulo": st.column_config.TextColumn("Rótulo", width="small"),
                "Aluno": st.column_config.TextColumn("Aluno (RA)", width="medium"),
                "Maquina": st.column_config.TextColumn("Máquina (host)", width="small"),
                "user": st.column_config.TextColumn("Conta Win", width="small"),
                "activity": st.column_config.TextColumn("Janela Ativa", width="large"),
                "category": st.column_config.TextColumn("Categoria"),
                "Tela": st.column_config.TextColumn("Tela", width="small"),
                "last_seen": st.column_config.TextColumn("Última Atualização"),
                "ip": st.column_config.TextColumn("IP Identificado"),
                "ports": st.column_config.ListColumn("Portas Abertas")
            }
        )

        with st.expander("🏷️ Rótulos das máquinas"):
            st.caption("Dê um nome amigável a cada PC (ex.: PC1-Fila1). Salvo em `lab_labels.json`.")
            with st.form("form_labels"):
                novos = {}
                alvos_labels = list(dict.fromkeys(maquinas + list(labels.keys())))
                for m in alvos_labels:
                    novos[m] = st.text_input(m, value=labels.get(m, ""), key=f"lbl_{m}")
                if st.form_submit_button("💾 Salvar rótulos"):
                    save_labels({k: v.strip() for k, v in novos.items() if v.strip()})
                    st.success("Rótulos salvos!")
                    st.rerun()

        st.divider()
        with st.expander("📱 Monitorar Alunos Externos (Celular/BYOD)"):
            classes_ext = db.get_classes()
            if not classes_ext:
                st.info("Nenhuma turma cadastrada.")
            else:
                nomes_ext = [c['name'] for c in classes_ext]
                turma_ext = st.selectbox("Turma", nomes_ext, key="mon_ext_class")
                class_id_ext = next(c['id'] for c in classes_ext if c['name'] == turma_ext)
                st.markdown("Alunos desta turma que ainda não estão nas máquinas do laboratório:")

                all_students = db.get_students_by_class(class_id_ext)
                monitored_users = df['user'].tolist()
                external_candidates = [s for s in all_students if s['username'] not in monitored_users]

                if not external_candidates:
                    st.success("Todos os alunos desta turma já estão sendo monitorados automaticamente.")
                else:
                    col_ext1, col_ext2, col_ext3 = st.columns([0.4, 0.3, 0.3])
                    student_options = {f"{s['name']} ({s['username']})": s['username'] for s in external_candidates}
                    targets_ext = col_ext1.multiselect("Selecionar Alunos", list(student_options.keys()),
                                                       key="mon_ext_alunos")
                    status_ext = col_ext2.selectbox(
                        "Status Manual",
                        ["Produtivo", "Celular (Proibido)", "Roblox", "Games", "Social"],
                        key="man_status",
                    )

                    if col_ext3.button("➕ Adicionar ao Radar", use_container_width=True):
                        for label in targets_ext:
                            uname = student_options[label]
                            real_name = label.split(" (")[0]

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

    # =========================== ABA CONTROLE ===========================
    with tab_controle:
        st.subheader("🕹️ Central de Intervenção")
        st.caption("Ações de vigilância e controle nas máquinas do laboratório.")

        selecionar_todas = st.checkbox("Selecionar TODAS as máquinas", key="mon_sel_all")
        if selecionar_todas:
            target = maquinas
            st.caption(f"✅ {len(target)} máquina(s) selecionada(s).")
        else:
            escolhidas = st.multiselect("Selecionar Máquinas", list(opcoes_maquinas.keys()),
                                        placeholder="Escolha os alvos...", key="mon_targets")
            target = [opcoes_maquinas[e] for e in escolhidas]

        ACOES_CONTROLE = [
            "Enviar Alerta Visual",
            "Abrir Prova Motriz (jovensgenios)",
            "Faxina (limpeza)",
            "Definir Volume em 30%",
            "Restaurar Volume (100%)",
            "Fechar Sites/Jogos (YouTube/Roblox/Loki/Games/Redes)",
            "Bloquear Sites/Jogos (YouTube/Roblox/Loki/Games/Redes)",
            "Desbloquear Sites/Jogos (YouTube/Roblox/Loki/Games/Redes)",
            "Bloquear Jogos (Fechar Roblox/Loki/Games)",
            "Limpar Inicialização do Roblox (bandeja)",
            "Limpar Inicialização do Opera (bandeja)",
            "Limpar Inicialização do Chrome (bandeja)",
            "Limpar Inicialização do WPS (bandeja)",
            "Liberar Telas (desativar bloqueio)",
            "Reativar Telas (bloqueio)",
            "Desativar Copilot (Windows)",
            "Desativar Apps em Segundo Plano (WPS/Chrome/Microsoft/Opera)",
            "Limpar Inicialização de Apps Microsoft (bandeja)",
            "Bloquear Sites (YouTube/Instagram/TikTok/Facebook)",
            "Bloquear Anônimos (Tor)",
            "Atualizar Monitor (rápido, sem UAC)",
            "Reinstalar Monitor (com UAC)",
            "Atualizar Tela de Bloqueio (sem UAC)",
            "Bloquear Navegador",
            "Registrar Uso Indevido de Celular",
            "Forçar Logoff (Deslogar PC)",
            "Desligar PC (Shutdown)",
            "Reiniciar PC (Restart)",
        ]
        PRESETS = {
            "🛑 Anti-jogo": [
                "Fechar Sites/Jogos (YouTube/Roblox/Loki/Games/Redes)",
                "Bloquear Sites/Jogos (YouTube/Roblox/Loki/Games/Redes)",
            ],
            "🎯 Aula focada": [
                "Enviar Alerta Visual",
                "Bloquear Sites/Jogos (YouTube/Roblox/Loki/Games/Redes)",
            ],
            "🔓 Liberar aula": [
                "Desbloquear Sites/Jogos (YouTube/Roblox/Loki/Games/Redes)",
                "Restaurar Volume (100%)",
            ],
            "🧹 Faxina": ["Faxina (limpeza)"],
            "💤 Desligar": ["Desligar PC (Shutdown)"],
        }

        def _aplicar_preset_acoes(lista):
            st.session_state["mon_actions"] = list(lista)

        cols_preset = st.columns(len(PRESETS))
        for i, ((nome_preset, lista_preset), col_preset) in enumerate(zip(PRESETS.items(), cols_preset)):
            col_preset.button(nome_preset, use_container_width=True,
                              key=f"mon_preset_{i}",
                              on_click=_aplicar_preset_acoes, args=(lista_preset,))

        actions = st.multiselect(
            "Ações de Controle (marque uma ou várias)",
            ACOES_CONTROLE,
            placeholder="Escolha uma ou mais ações...",
            key="mon_actions",
        )

        msg = ""
        if any("Alerta" in a for a in actions):
            msg = st.text_input("Mensagem do Alerta",
                                value="Foco na atividade! Feche o jogo imediatamente.",
                                key="mon_msg")
        st.caption(f"🎮 Jogos: {BLOCKED_PLATFORMS_INFO}")

        if st.button("🚀 Executar Comando Remoto", type="primary", use_container_width=True):
            if not target or not actions:
                st.warning("Selecione pelo menos uma máquina e uma ação.")
            else:
                for t in target:
                    for action in actions:
                        if action == "Registrar Uso Indevido de Celular":
                            u_name = lab_data.get(t, {}).get('user', 'desconhecido')
                            lab_data[t]['category'] = "Celular (Proibido)"
                            lab_data[t]['activity'] = "📱 Celular flagrado pelo professor"
                            db.add_user_history(
                                u_name,
                                f"🚩 INFRAÇÃO: Uso de celular sem permissão (Registrado por {prof})",
                            )
                        _enfileirar_comando(lab_data, [t], action,
                                            msg if "Alerta" in action else "")

                save_monitor_data(lab_data)
                st.success(f"{len(actions)} ação(ões) enviada(s) para: {', '.join(labels.get(t, t) for t in target)}")
                db.add_user_history(prof, f"Enviou {len(actions)} ação(ões) para {len(target)} máquinas no laboratório.")
                st.rerun()

    # ========================= ABA FERRAMENTAS =========================
    with tab_ferramentas:
        st.subheader("🧰 Ferramentas")
        # Base padrao tambem usada pelo backup; o bloco de estrutura pode
        # sobrescrever com o valor digitado.
        base_pastas = base_pastas_padrao

        st.markdown("#### 💬 Texto e comando")
        st.caption(
            "Envie uma mensagem/alerta e/ou digite um comando do monitor para os "
            "PCs selecionados. O comando usa o mesmo nome das ações da aba Controle."
        )
        alvo_texto_rotulos = st.multiselect(
            "Aplicar nos PCs (texto/comando)",
            list(opcoes_maquinas.keys()),
            key="fer_texto_alvo",
        )
        texto_msg = st.text_area(
            "Texto / mensagem",
            key="fer_texto_msg",
            placeholder="Ex.: Foco na atividade! Feche o jogo imediatamente.",
        )
        comando_txt = st.text_input(
            "Comando (opcional)",
            key="fer_texto_cmd",
            placeholder="Ex.: Desligar PC (Shutdown)",
            help="Exemplos: Enviar Alerta Visual, Bloquear Sites/Jogos (...), Desligar PC (Shutdown).",
        )
        st.caption(
            "Exemplos: `Enviar Alerta Visual` · `Bloquear Sites/Jogos (YouTube/Roblox/Loki/Games/Redes)` "
            "· `Desligar PC (Shutdown)` · `Reiniciar PC (Restart)`."
        )
        col_texto1, col_texto2 = st.columns(2)
        if col_texto1.button("💬 Enviar texto", type="primary", use_container_width=True):
            alvo_texto = [opcoes_maquinas[r] for r in alvo_texto_rotulos]
            if not alvo_texto:
                st.warning("Selecione pelo menos um PC.")
            elif not texto_msg.strip():
                st.warning("Digite o texto da mensagem.")
            else:
                for maquina in alvo_texto:
                    _enfileirar_comando(lab_data, [maquina], "Enviar Alerta Visual", texto_msg.strip())
                save_monitor_data(lab_data)
                db.add_user_history(prof, f"Enviou texto/alerta para {len(alvo_texto)} PC(s).")
                st.success(f"Texto enviado para {len(alvo_texto)} PC(s).")
                st.rerun()
        if col_texto2.button("🚀 Executar comando", use_container_width=True):
            alvo_texto = [opcoes_maquinas[r] for r in alvo_texto_rotulos]
            comando = comando_txt.strip()
            if not alvo_texto:
                st.warning("Selecione pelo menos um PC.")
            elif not comando:
                st.warning("Digite o comando a executar.")
            else:
                for maquina in alvo_texto:
                    if texto_msg.strip() and "Alerta" not in comando:
                        _enfileirar_comando(lab_data, [maquina], "Enviar Alerta Visual", texto_msg.strip())
                    _enfileirar_comando(
                        lab_data, [maquina], comando,
                        texto_msg.strip() if "Alerta" in comando else "",
                    )
                save_monitor_data(lab_data)
                db.add_user_history(prof, f"Executou '{comando}' em {len(alvo_texto)} PC(s).")
                st.success(f"Comando enviado para {len(alvo_texto)} PC(s).")
                st.rerun()

        st.divider()
        st.markdown("#### 🗂️ Estrutura de pastas de atividades")
        st.caption(
            "Cria **`<base>\\<turma>\\<disciplina>\\<aluno>\\Aula_NN`** nos PCs selecionados "
            "(cada aluno tem a própria pasta). Espaços viram `_` e `%USERPROFILE%` é expandido "
            "no PC do aluno (sem Administrador)."
        )
        st.warning(
            "Requer **agente atualizado**: rode `Controle → Atualizar Monitor (rápido, sem UAC)` "
            "nos PCs antes. Agentes antigos ignoram este comando sem mostrar erro."
        )

        classes = db.get_classes()
        if not classes:
            st.warning("Nenhuma turma cadastrada no sistema.")
        else:
            nomes_turmas = [c['name'] for c in classes]
            turma_nome = st.selectbox("Turma", nomes_turmas, key="fer_turma")
            st.session_state['last_lab_class'] = turma_nome
            class_id = next(c['id'] for c in classes if c['name'] == turma_nome)

            disciplinas = []
            try:
                disciplinas = [s['name'] for s in db.get_subjects_for_class(class_id)
                               if s.get('is_active', True)]
            except Exception:
                try:
                    disciplinas = [d['name'] for d in db.get_disciplines_by_class(class_id)]
                except Exception:
                    disciplinas = []

            if disciplinas:
                disc_nome = st.selectbox("Disciplina", disciplinas, key="fer_disc")
            else:
                st.info("Esta turma não tem disciplinas vinculadas; digite o nome abaixo.")
                disc_nome = st.text_input("Disciplina", key="fer_disc_manual")

            col_a, col_b = st.columns(2)
            aulas = col_a.text_input("Aulas (ex.: 1-32 ou 32)", value="1-32", key="fer_aulas")
            base_pastas = col_b.text_input("Pasta base nos PCs", value=base_pastas_padrao,
                                           key="fer_base")

            alvo_rotulos = st.multiselect(
                "Aplicar nos PCs",
                list(opcoes_maquinas.keys()),
                default=list(opcoes_maquinas.keys()),
                key="fer_alvo",
            )
            alvo = [opcoes_maquinas[r] for r in alvo_rotulos]

            if disc_nome:
                st.caption(
                    f"Prévia: `{base_pastas}\\{turma_nome}\\{disc_nome}\\<aluno>\\Aula_01` "
                    f"... `Aula_NN` ({aulas or 'sem aulas'})"
                )

            if st.button("📁 Criar estrutura de pastas", type="primary"):
                if not disc_nome:
                    st.error("Escolha (ou digite) a disciplina.")
                elif not alvo:
                    st.warning("Selecione pelo menos um PC.")
                else:
                    sem_aluno = 0
                    for maquina in alvo:
                        u = _lookup_ci(users_map, maquina) or {}
                        aluno = (u.get('name') or '').strip() or \
                                lab_data.get(maquina, {}).get('user', '')
                        if not aluno:
                            aluno = maquina
                            sem_aluno += 1
                        payload = build_estrutura_payload(
                            base_pastas, turma_nome, disc_nome, aulas, aluno
                        )
                        _enfileirar_comando(lab_data, [maquina], "Estruturar Pastas", payload)
                    save_monitor_data(lab_data)
                    db.add_user_history(
                        prof,
                        f"Estruturou pastas ({turma_nome} / {disc_nome}) em {len(alvo)} PC(s).",
                    )
                    st.success(f"Comando enviado para {len(alvo)} PC(s). As pastas aparecem em instantes.")
                    if sem_aluno:
                        st.caption(f"{sem_aluno} PC(s) sem aluno associado — usei a conta Windows.")
                    st.caption("Se o PC estava desligado, a ação expira em 30 min (segurança).")

        st.divider()
        st.markdown("#### 📦 Backup de atividades")
        st.caption(
            "Pede aos PCs selecionados um ZIP da pasta de atividades "
            f"(`{base_pastas}`, expandida no PC do aluno). Os ZIPs ficam no servidor em "
            "`.atividades` e podem ser baixados em **Backups de atividades (recebidos)**."
        )
        alvo_backup_rotulos = st.multiselect(
            "Enviar backup destes PCs",
            list(opcoes_maquinas.keys()),
            default=list(opcoes_maquinas.keys()),
            key="fer_backup_alvo",
        )
        if st.button("📦 Solicitar ZIP das atividades", type="primary"):
            if not alvo_backup_rotulos:
                st.warning("Selecione pelo menos um PC.")
            else:
                alvo_backup = [opcoes_maquinas[r] for r in alvo_backup_rotulos]
                payload = json.dumps({"base": base_pastas}, ensure_ascii=False)
                for maquina in alvo_backup:
                    _enfileirar_comando(lab_data, [maquina], "Enviar Atividades", payload)
                save_monitor_data(lab_data)
                db.add_user_history(
                    prof,
                    f"Solicitou backup de atividades de {len(alvo_backup)} PC(s).",
                )
                st.success(
                    f"Backup solicitado a {len(alvo_backup)} PC(s). "
                    "Aguarde e confira em **Backups de atividades (recebidos)**."
                )
                st.caption("Se o PC estava desligado, a ação expira em 30 min (segurança).")

        st.divider()
        st.markdown("#### 🛠️ Instalar Kit Lab DS (winget)")
        st.caption("VS Code, JDK 17, Node.js LTS e NetBeans. Pede UAC no PC do aluno.")
        alvo_kit_rotulos = st.multiselect(
            "Aplicar nos PCs (Kit)",
            list(opcoes_maquinas.keys()),
            key="fer_kit_alvo",
        )
        if st.button("📦 Instalar Kit nos PCs selecionados"):
            if not alvo_kit_rotulos:
                st.warning("Selecione pelo menos um PC.")
            else:
                alvo_kit = [opcoes_maquinas[r] for r in alvo_kit_rotulos]
                _enfileirar_comando(lab_data, alvo_kit, "Instalar Kit Lab DS (Winget)")
                save_monitor_data(lab_data)
                db.add_user_history(prof, f"Instalou Kit Lab DS em {len(alvo_kit)} PC(s).")
                st.success(f"Instalação agendada em {len(alvo_kit)} PC(s).")

        st.divider()
        _render_baixar_pacote(_dash_url)
        st.link_button("📦 Backups de atividades (recebidos)",
                       _dash_url.rstrip('/') + "/atividades")

    # ========================= ABA AÇÕES EM MASSA =========================
    with tab_massa:
        st.subheader("⚡ Ações em Massa (todo o laboratório)")
        st.caption("Aplica o comando selecionado a TODAS as máquinas visíveis no radar.")
        confirmar = st.checkbox("Confirmo aplicar em todas as máquinas do radar", key="mon_conf_massa")
        todas = maquinas
        col_m1, col_m2, col_m3 = st.columns(3)
        acao_massa = None
        if col_m1.button("🔌 Desligar TODAS", disabled=not confirmar, use_container_width=True):
            acao_massa = "Desligar PC (Shutdown)"
        if col_m2.button("♻️ Reiniciar TODAS", disabled=not confirmar, use_container_width=True):
            acao_massa = "Reiniciar PC (Restart)"
        if col_m3.button("🚫 Bloquear Sites em TODAS", disabled=not confirmar, use_container_width=True):
            acao_massa = "Bloquear Sites (YouTube/Instagram/TikTok/Facebook)"
        if st.button("🧹 Limpar Inicialização do Roblox em TODAS", disabled=not confirmar, use_container_width=True):
            acao_massa = "Limpar Inicialização do Roblox (bandeja)"
        if st.button("🧹 Limpar Inicialização do Opera em TODAS", disabled=not confirmar, use_container_width=True):
            acao_massa = "Limpar Inicialização do Opera (bandeja)"
        if st.button("🧹 Limpar Inicialização de Apps Microsoft em TODAS", disabled=not confirmar, use_container_width=True):
            acao_massa = "Limpar Inicialização de Apps Microsoft (bandeja)"
        if st.button("⛔ Bloquear Sites/Jogos em TODAS", disabled=not confirmar, use_container_width=True):
            acao_massa = "Bloquear Sites/Jogos (YouTube/Roblox/Loki/Games/Redes)"
        if st.button("✅ Desbloquear Sites/Jogos em TODAS", disabled=not confirmar, use_container_width=True):
            acao_massa = "Desbloquear Sites/Jogos (YouTube/Roblox/Loki/Games/Redes)"
        if st.button("🔊 Volume 30% em TODAS", disabled=not confirmar, use_container_width=True):
            acao_massa = "Definir Volume em 30%"
        if st.button("🔊 Volume 100% em TODAS", disabled=not confirmar, use_container_width=True):
            acao_massa = "Restaurar Volume (100%)"
        if st.button("🌐 Abrir Prova Motriz em TODAS", disabled=not confirmar, use_container_width=True):
            acao_massa = "Abrir Prova Motriz (jovensgenios)"
        if st.button("🧹 Faxina em TODAS", disabled=not confirmar, use_container_width=True):
            acao_massa = "Faxina (limpeza)"

        if acao_massa:
            _enfileirar_comando(lab_data, todas, acao_massa)
            save_monitor_data(lab_data)
            db.add_user_history(prof, f"Enviou '{acao_massa}' para TODAS as {len(todas)} máquinas do laboratório.")
            st.success(f"'{acao_massa}' enviado para {len(todas)} máquina(s).")
            st.rerun()

    # ============================ ABA HISTÓRICO ============================
    with tab_hist:
        st.subheader("📜 Histórico de Hoje")
        st.caption("Entradas, ações do professor e infrações registradas hoje.")
        all_hist = db.get_all_history(limit=300)
        hoje = datetime.now().date()
        linhas = []
        for h in all_hist:
            dt = _dt_local(h.get('timestamp'))
            if not dt or dt.date() != hoje:
                continue
            act = h.get('activity', '')
            baixo = act.lower()
            if "infração" in baixo or "celular" in baixo:
                tipo = "Infração"
            elif "enviou" in baixo:
                tipo = "Ação do professor"
            elif "entrou" in baixo or "login" in baixo:
                tipo = "Entrada"
            else:
                tipo = "Registro"
            linhas.append({
                "Hora": dt.strftime("%H:%M"),
                "Usuário/RA": h.get('username', ''),
                "Tipo": tipo,
                "Ocorrência": act.replace("🚩 INFRAÇÃO: ", ""),
            })
        linhas.sort(key=lambda x: x["Hora"], reverse=True)
        if linhas:
            st.dataframe(linhas, hide_index=True, use_container_width=True)
            infr = sum(1 for l in linhas if l["Tipo"] == "Infração")
            st.caption(f"{len(linhas)} registro(s) hoje · {infr} infração(ões).")
        else:
            st.info("Nenhuma atividade registrada hoje até o momento.")

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
