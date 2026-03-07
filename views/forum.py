import streamlit as st
import time
from services import database as db

def show_page():
    st.header("💬 Fórum de Dúvidas")
    
    with st.form("novo_post"):
        nova_msg = st.text_area("Escreva sua dúvida ou comentário:")
        submit_btn = st.form_submit_button("Enviar")
        
        if submit_btn and nova_msg:
            if db.is_db_connected():
                _, error = db.add_forum_post(st.session_state['usuario'], nova_msg)
                if error:
                    st.error(f"Erro: {error}")
                else:
                    st.success("Mensagem enviada!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning("Fórum indisponível offline.")

    st.divider()
    st.subheader("Últimas Discussões")
    
    posts = db.get_forum_posts()
    
    for post in posts:
        col_msg, col_action = st.columns([0.9, 0.1])
        with col_msg:
            # Formata a hora simples para exibição
            ts = post.get("created_at", "")
            hora = ts.split("T")[1][:5] if "T" in ts else ts
            
            with st.chat_message("user" if post['user_name'] == st.session_state['usuario'] else "assistant"):
                st.write(f"**{post['user_name']}** ({hora}):")
                st.write(post['message'])
        
        if st.session_state.get('role') == 'admin':
            with col_action:
                if st.button("🗑️", key=f"del_{post['id']}", help="Excluir post"):
                    db.delete_forum_post(post['id'])
                    st.rerun()