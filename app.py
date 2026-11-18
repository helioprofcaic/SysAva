import streamlit as st
import argparse
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path para garantir que os módulos sejam encontrados.
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

APP_LOGO = os.path.join(project_root, "assets", "logo_sysava.png")

# Importa as funções que renderizam cada página

from views import home, aulas, forum, quiz, avaliacoes, admin, login, register, gerador_aulas, plugins, portal, usuarios
from services import database, auth
import config

# Título e ícone da aba do navegador (deve ser o primeiro comando st.*)
st.set_page_config(
    page_title="SysAva",
    page_icon=APP_LOGO if os.path.exists(APP_LOGO) else "🎓",
)

# Define o tema da aplicação
st.markdown(
    """
    <style>
        /* Escala de leitura: o navegador a 100% fica confortável em telas grandes */
        html { font-size: 112.5% !important; } /* 18px (padrão Streamlit: 16px) */

        /* Tema azul SysAva (mesma paleta do logo) */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0B1E3F 0%, #070D18 100%);
            color: #E5E7EB;
        }
        [data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0A1730 0%, #081020 100%);
            border-right: 1px solid rgba(37, 99, 235, 0.35);
        }
        /* Card Style para seções */
        div.stButton > button {
            border-radius: 8px;
            transition: all 0.3s ease;
            border: 1px solid #2563EB;
        }
        div.stButton > button:hover {
            border-color: #60A5FA;
            color: #60A5FA;
            box-shadow: 0 0 10px rgba(37, 99, 235, 0.35);
        }
        /* Melhora a visibilidade de inputs */
        .stTextInput input, .stTextArea textarea {
            background-color: #0F1B2E !important;
            color: #ffffff !important;
        }
        a { color: #60A5FA !important; }

        /* Boxes de código: azul mais claro que o fundo, sem branco */
        pre, code, [data-testid="stCodeBlock"], [data-testid="stCodeBlock"] pre {
            background-color: #152C52 !important;
            color: #E5E7EB !important;
            border: 1px solid #2E4F7A !important;
        }
    </style>
    """, unsafe_allow_html=True)


# --- Lógica Principal (Roteamento) ---
def parse_arguments():
    parser = argparse.ArgumentParser(description="Streamlit App with Command-Line Arguments")
    parser.add_argument("--port", type=int, default=8501, help="Port to run the Streamlit app on")
    parser.add_argument("--theme", type=str, default="default", help="Theme for the Streamlit app")
    return parser.parse_args()

@st.cache_resource(show_spinner="Sincronizando arquivos do Google Drive...")
def _drive_bootstrap():
    """Uma vez por processo: baixa plugins/repo e o banco (se faltar)."""
    try:
        from services import drive_storage
        if not drive_storage.credentials_available():
            return False
        drive_storage.sync_repo_down()
        db_path = os.path.join(project_root, "data", "escola_ativa.db")
        if not os.path.exists(db_path):
            drive_storage.sync_db_down(db_path)
        return True
    except Exception:
        return False


def main():
    args = parse_arguments()
    # Tenta recuperar a sessão via URL se o usuário não estiver logado
    if 'logado' not in st.session_state or not st.session_state['logado']:
        try:
            session_id = st.query_params.get("session_id") or args.port # Fallback para porta se necessário ou apenas ignorar
            if session_id:
                user_session = auth.get_session(session_id)
                if user_session:
                    usuario_atual = None
                    if database.is_db_connected():
                        usuario_atual = database.get_user(user_session['username'])
                    if usuario_atual and database.is_user_blocked(usuario_atual):
                        auth.logout_session(session_id)
                    else:
                        st.session_state['logado'] = True
                        st.session_state['usuario'] = user_session['name']
                        st.session_state['username'] = user_session['username']
                        st.session_state['role'] = user_session['role']
                        st.session_state.page = 'Home'
        except Exception:
            pass

    # Conta desativada pelo professor: derruba a sessao na hora (sem consultar
    # o banco a cada rerun; usa a lista em memoria compartilhada do processo).
    if st.session_state.get('logado') and auth.is_session_revoked(
            st.session_state.get('username')):
        try:
            from services import audit_log
            audit_log.registrar(
                "Sessão encerrada (conta desativada)",
                username=st.session_state.get('username', ''),
                name=st.session_state.get('usuario', ''),
                role=st.session_state.get('role', ''),
                pagina='Sessão',
            )
        except Exception:
            pass
        st.session_state['logado'] = False
        st.session_state['usuario'] = ''
        st.session_state['role'] = 'student'
        st.session_state['page'] = 'login'
        try:
            st.query_params.clear()
        except Exception:
            pass
        st.rerun()

    if 'page' not in st.session_state:
        st.session_state.page = 'login'

    # Roteador de páginas de autenticação
    if not st.session_state.get('logado', False):
        if st.session_state.page == 'login':
            login.show_page()
        elif st.session_state.page == 'register':
            register.show_page()
        else:
            # Se o usuário não está logado e tentou acessar uma página protegida,
            # força o redirecionamento para a página de login.
            st.session_state.page = 'login'  # Se não logado, volta para a página de login
            st.rerun()
    else:
        _drive_bootstrap()

        # Sidebar de Navegação
        with st.sidebar:
            if os.path.exists(APP_LOGO):
                st.image(APP_LOGO, width=100)
            else:
                st.markdown("## 🎓 SysAva")
            st.title(f"Olá, {st.session_state['usuario']}")
            try:
                from services import database as _db
                st.caption(f"🗄️ Banco: {_db.get_backend_label()}")

                # Disciplina atual + progresso do aluno (quizzes e fóruns)
                if st.session_state.get('role') == 'student':
                    _page = st.session_state.get('page', 'Home')
                    if _page in ('Home', 'Avaliações'):
                        _sname = st.session_state.get('home_subject_filter') or st.session_state.get('home_subject_name')
                        _sid = st.session_state.get('home_subject_id')
                        if _sname and 'Visao Geral' not in str(_sname):
                            _match = next((s for s in (_db.get_subjects() or []) if s.get('name') == _sname), None)
                            _sid = _match['id'] if _match else _sid
                    elif _page == 'Aulas':
                        _sname = st.session_state.get('aulas_subject_filter') or st.session_state.get('selected_subject_name')
                        _sid = st.session_state.get('selected_subject_id')
                        if _sname and _sname != "-- Selecione uma disciplina --":
                            _match = next((s for s in (_db.get_subjects() or []) if s.get('name') == _sname), None)
                            _sid = _match['id'] if _match else _sid
                    else:
                        _sid = st.session_state.get('selected_subject_id') or st.session_state.get('home_subject_id')
                        _sname = st.session_state.get('selected_subject_name') or st.session_state.get('home_subject_name')

                    if _sid:
                        _label = _sname or f"Disciplina {_sid}"
                    elif _sname and 'Visao Geral' in str(_sname):
                        _label = 'Visão Geral (todas)'
                    elif _page in ('Home', 'Avaliações'):
                        _label = 'Visão Geral (todas)'
                    else:
                        _label = 'Nenhuma selecionada'

                    st.markdown(f"📚 **Disciplina atual:** {_label}")
                    _username = st.session_state.get('username') or st.session_state.get('usuario')
                    _stats = _db.get_student_completion_stats(_username, _sid)
                    st.progress(
                        _stats['quiz_pct'] / 100.0,
                        text=f"📝 Quizzes: {_stats['quiz_done']}/{_stats['quiz_total']} ({_stats['quiz_pct']}%)",
                    )
                    st.progress(
                        _stats['forum_pct'] / 100.0,
                        text=f"💬 Fóruns: {_stats['forum_done']}/{_stats['forum_total']} ({_stats['forum_pct']}%)",
                    )
            except Exception:
                pass

            # Menu base (O Fórum agora é condicional à visualização de uma aula)
            opcoes_menu = ["Home", "Aulas"]
            
            # Só mostra o Fórum se houver uma aula selecionada ou se o usuário já estiver nele
            if st.session_state.get('view_mode') == 'detail' or st.session_state.get('page') == 'Fórum' or st.session_state.get('context_lesson_id'):
                opcoes_menu.append("Fórum")
                
            opcoes_menu.append("Avaliações")

            if st.session_state.get('role') in ['admin', 'teacher']:
                opcoes_menu.append("Portal")
                opcoes_menu.append("Gestão de Usuários")
                opcoes_menu.append("Admin")
                opcoes_menu.append("Plugins")
                opcoes_menu.append("Gerador de Aulas")
            
            # Identifica qual opção deve estar marcada no menu
            current_page = st.session_state.get('page', 'Home')

            # Se a página atual (ex: Quiz) não está no menu padrão,
            # adicionamos ela temporariamente.
            # Isso impede que o st.radio force a seleção para o índice 0 ('Aulas') e cause redirect.
            if current_page not in opcoes_menu and current_page != "Sair":
                opcoes_menu.append(current_page)

            opcoes_menu.append("Sair")
            
            try:
                index_menu = opcoes_menu.index(current_page)
            except ValueError:
                # Se a página atual não está no menu (ex: Quiz), marca a primeira opção (Aulas)
                index_menu = 0
            
            menu_selection = st.radio(
                "Menu", opcoes_menu, index=index_menu
            )


            # Se a seleção do menu mudou, atualiza a página e limpa contextos antigos
            if menu_selection != current_page:
                st.session_state.page = menu_selection
                
                # Limpa contextos específicos ao navegar pelo menu principal
                keys_to_clear = ['context_lesson_id', 'context_quiz_id', 'view_mode', 'selected_lesson']
                for key in keys_to_clear:
                    if key in st.session_state: del st.session_state[key]
                
                st.rerun()
            
            if st.session_state.page == "Sair":
                # Limpa a sessão persistente
                try:
                    sid = st.query_params.get("session_id")
                    if sid:
                        auth.logout_session(sid)
                    st.query_params.clear()
                except:
                    pass

                # Limpa a sessão para fazer logout
                try:
                    from services import audit_log
                    audit_log.registrar("Logout", username=st.session_state.get('username', ''),
                                        name=st.session_state.get('usuario', ''),
                                        role=st.session_state.get('role', ''), pagina='Sair')
                except Exception:
                    pass
                st.session_state['logado'] = False

                st.session_state['usuario'] = ''
                st.session_state['role'] = 'student'
                st.session_state['page'] = 'login'
                st.rerun()
                
        page_to_show = st.session_state.get('page', 'Home')

        # --- Auditoria (IS-071): registra a navegação (1x por troca de página) ---
        try:
            from services import audit_log
            if st.session_state.get('_audit_ultima_pagina') != page_to_show:
                st.session_state['_audit_ultima_pagina'] = page_to_show
                _ip = "local"
                try:
                    _ip = (st.context.headers.get("X-Forwarded-For", "") or "").split(",")[0].strip() or "local"
                except Exception:
                    pass
                audit_log.registrar(
                    "Navegou",
                    username=st.session_state.get('username', ''),
                    name=st.session_state.get('usuario', ''),
                    role=st.session_state.get('role', ''),
                    pagina=page_to_show, ip=_ip)
        except Exception:
            pass

        # Renderização das Páginas
        if page_to_show == "Home":
            home.show_page()
        elif page_to_show == "Aulas":
            aulas.show_page()
        elif page_to_show == "Fórum":
            forum.show_page()
        elif page_to_show == "Quiz":
            quiz.show_page()
        elif page_to_show == "Avaliações":
            avaliacoes.show_page()
        elif page_to_show == "Gestão de Usuários":
            usuarios.show_page()
        elif page_to_show == "Admin":
            admin.show_page()
        elif page_to_show == "Plugins":
            plugins.show_page()
        elif page_to_show == "Gerador de Aulas":
            gerador_aulas.show_page()
        elif page_to_show == "Portal":
            portal.show_page()


if __name__ == "__main__":
    main()
