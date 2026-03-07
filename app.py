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
            
            opcoes_menu = ["Aulas", "Fórum", "Quiz", "Avaliações"]
            if st.session_state.get('role') == 'admin':
                opcoes_menu.append("Admin")
            opcoes_menu.append("Sair")
            
            menu = st.radio(
                "Menu", opcoes_menu
            )
            
            if menu == "Sair":
                # Limpa a sessão para fazer logout
                st.session_state['logado'] = False
                st.session_state['usuario'] = ''
                st.session_state['role'] = 'student'
                st.session_state['page'] = 'login'
                st.rerun()

        # Renderização das Páginas
        if menu == "Aulas":
            aulas.show_page()
        elif menu == "Fórum":
            forum.show_page()
        elif menu == "Quiz":
            quiz.show_page()
        elif menu == "Avaliações":
            avaliacoes.show_page()
        elif menu == "Admin":
            admin.show_page()

if __name__ == "__main__":
    main()
