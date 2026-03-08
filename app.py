import streamlit as st

# Importa as funções que renderizam cada página
from views import aulas, forum, quiz, avaliacoes, admin, login, register

# Configuração da Página
st.set_page_config(page_title="Plataforma de Ensino", layout="wide", page_icon="🎓")


# --- Lógica Principal (Roteamento) ---

def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

    # Roteador de páginas de autenticação
    if not st.session_state.get('logado', False):
        if st.session_state.page == 'login':
            login.show_page()
        elif st.session_state.page == 'register':
            register.show_page()
    else:
        # Sidebar de Navegação
        with st.sidebar:
            st.image("https://cdn-icons-png.flaticon.com/512/2991/2991148.png", width=100)
            st.title(f"Olá, {st.session_state['usuario']}")
            
            # O Quiz agora é acessado via Aulas, então removemos do menu principal
            opcoes_menu = ["Aulas", "Fórum", "Avaliações"]
            if st.session_state.get('role') == 'admin':
                opcoes_menu.append("Admin")
            opcoes_menu.append("Sair")
            
            # O radio do sidebar agora controla o st.session_state.page
            current_page = st.session_state.get('page', 'Aulas')
            menu_selection = st.radio(
                "Menu", opcoes_menu
            )
            
            # Se a seleção do menu mudou, atualiza a página e limpa contextos antigos
            if menu_selection != current_page:
                st.session_state.page = menu_selection
                st.rerun()
            
            if st.session_state.page == "Sair":
                # Limpa a sessão para fazer logout
                st.session_state['logado'] = False
                st.session_state['usuario'] = ''
                st.session_state['role'] = 'student'
                st.session_state['page'] = 'login'
                st.rerun()

        page_to_show = st.session_state.get('page', 'Aulas')

        # Renderização das Páginas
        if page_to_show == "Aulas":
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
