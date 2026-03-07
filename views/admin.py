import streamlit as st
from services import database as db

def show_page():
    st.header("🛡️ Painel Administrativo")
    st.info("Área restrita para gerenciamento de usuários.")
    
    if db.is_db_connected():
        st.subheader("Usuários Cadastrados")
        users = db.get_all_users()
        if users:
            st.dataframe(users, use_container_width=True)
    else:
        st.warning("Funcionalidade disponível apenas com banco de dados conectado.")