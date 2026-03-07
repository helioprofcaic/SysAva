import streamlit as st
import time
from services import database as db
from services import auth

def show_page():
    st.title("📝 Cadastro de Novo Aluno")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("registration_form"):
            name = st.text_input("Nome Completo")
            username = st.text_input("Usuário (para login)")
            ra = st.text_input("RA (Registro do Aluno)")
            password = st.text_input("Senha", type="password")
            password_confirm = st.text_input("Confirme a Senha", type="password")
            
            submitted = st.form_submit_button("Cadastrar")

            if submitted:
                if not all([name, username, password, password_confirm, ra]):
                    st.warning("Por favor, preencha todos os campos.")
                elif password != password_confirm:
                    st.error("As senhas não coincidem.")
                elif not db.is_db_connected():
                    st.error("Modo offline. Não é possível registrar novos usuários.")
                else:
                    # Verifica se o usuário já existe
                    if db.get_user(username):
                        st.error("Este nome de usuário já existe.")
                    else:
                        hashed = auth.hash_password(password)
                        data, error = db.create_user(username, hashed, name, ra)
                        if error:
                            st.error(f"Erro no cadastro: {error}")
                        else:
                            st.success("Usuário cadastrado com sucesso! Redirecionando...")
                            time.sleep(2)
                            st.session_state.page = 'login'
                            st.rerun()
        
        st.divider()
        if st.button("Já tem uma conta? Faça o login"):
            st.session_state.page = 'login'
            st.rerun()