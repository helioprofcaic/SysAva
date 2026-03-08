import streamlit as st
from services import database as db

def show_page():
    st.title(f"Bem-vindo, {st.session_state.get('usuario', 'Aluno')}!")
    st.markdown("---")

    st.subheader("📅 Seu Histórico de Atividades")
    
    # Busca o histórico do usuário logado usando o username (RA/ID)
    username = st.session_state.get('username')
    
    if username:
        user_history = db.get_user_history(username)
        
        if user_history:
            with st.container():
                for item in user_history:
                    col1, col2 = st.columns([0.7, 0.3])
                    with col1:
                        st.markdown(f"**{item.get('activity', 'Atividade')}**")
                    with col2:
                        # Formatação simples da data/hora se vier no formato ISO
                        ts = str(item.get('timestamp', ''))
                        if 'T' in ts:
                            data, hora = ts.split('T')
                            st.caption(f"{data} {hora[:5]}")
                        else:
                            st.caption(ts)
                    st.divider()
        else:
            st.info("Nenhuma atividade registrada recentemente.")
    else:
        st.warning("Por favor, faça login para ver seu histórico.")