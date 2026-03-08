import streamlit as st
import argparse

# Importa as funções que renderizam cada página
from views import home, aulas, forum, quiz, avaliacoes, admin, login, register
from services import database, auth

# Configuração da Página (deve ser o primeiro comando Streamlit)
st.set_page_config(page_title="Plataforma de Ensino", layout="wide", page_icon="🎓")

# Define o tema da aplicação
st.markdown(
    """
    <style>
    /* Força o fundo escuro e a cor do texto branca para todo o app */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #333333;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)


# --- Lógica Principal (Roteamento) ---
def parse_arguments():
    parser = argparse.ArgumentParser(description="Streamlit App with Command-Line Arguments")
    parser.add_argument("--port", type=int, default=8501, help="Port to run the Streamlit app on")
    parser.add_argument("--theme", type=str, default="default", help="Theme for the Streamlit app")
    return parser.parse_args()

args = parse_arguments()

# Now you can use args.port, args.theme, etc. in your Streamlit app

# # Mock function to simulate fetching user history
def get_mock_user_history(username):
    # Replace this with actual database or data source retrieval
    return [f"Aula 1 concluída em 2024-01-01", f"Participou do fórum em 2024-01-05"]

def main():
    # Tenta recuperar a sessão via URL se o usuário não estiver logado
    if 'logado' not in st.session_state or not st.session_state['logado']:
        try:
            session_id = st.query_params.get("session_id")
            if session_id:
                user_session = auth.get_session(session_id)
                if user_session:
                    st.session_state['logado'] = True
                    st.session_state['usuario'] = user_session['name']
                    st.session_state['username'] = user_session['username']
                    st.session_state['role'] = user_session['role']
                    st.session_state.page = 'Home'
        except Exception:
            pass

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
        # Sidebar de Navegação
        with st.sidebar:
            st.image("https://cdn-icons-png.flaticon.com/512/2991/2991148.png", width=100)
            st.title(f"Olá, {st.session_state['usuario']}")

            # O Quiz agora é acessado via Aulas, então removemos do menu principal
            opcoes_menu = ["Home", "Aulas", "Fórum", "Avaliações"]
            if st.session_state.get('role') in ['admin', 'teacher']:
                opcoes_menu.append("Admin")
            
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
                st.session_state['logado'] = False

                st.session_state['usuario'] = ''
                st.session_state['role'] = 'student'
                st.session_state['page'] = 'login'
                st.rerun()
                
        page_to_show = st.session_state.get('page', 'Home')

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
        elif page_to_show == "Admin":
            admin.show_page()


if __name__ == "__main__":
    main()
