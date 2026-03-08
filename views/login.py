import streamlit as st
from services import database as db
from services import auth

def show_page():
    st.title("🔐 Login do Aluno")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        user = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        
        if st.button("Entrar"):
            if db.is_db_connected():
                # Remove espaços extras que podem causar erro
                user = user.strip()

                user_data = db.get_user(user)
                if user_data:
                    if auth.check_password(password, user_data['password']):
                        st.session_state['logado'] = True
                        st.session_state['usuario'] = user_data.get('name', user)
                        # Armazena o username (RA) para consultas de matrícula
                        st.session_state['username'] = user
                        st.session_state['role'] = user_data.get('role', 'student')
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos.")
                else:
                    st.error("Usuário ou senha incorretos.")
            else:
                # Fallback offline
                if user == "admin" and password == "admin":
                    st.session_state['logado'] = True
                    st.session_state['usuario'] = "Administrador (Offline)"
                    # Armazena o username para consistência
                    st.session_state['username'] = "admin"
                    st.session_state['role'] = "admin"
                    st.rerun()
                else:
                    st.error("Login offline: use admin/admin")
        
        st.divider()
        if st.button("Não tem uma conta? Registre-se"):
            st.session_state.page = 'register'
            st.rerun()