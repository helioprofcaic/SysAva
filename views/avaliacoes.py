import streamlit as st

def show_page():
    st.header("📊 Minhas Avaliações")
    
    col1, col2 = st.columns(2)
    
    quiz_score = st.session_state.get('quiz_score', 0)
    
    with col1:
        st.metric(label="Média Geral", value="8.5", delta="0.5")
    with col2:
        st.metric(label="Último Quiz", value=f"{quiz_score}/2")
        
    st.table({
        "Matéria": ["Python", "Data Science", "Web Dev"],
        "Nota": [9.0, 8.5, "Pendente"],
        "Status": ["Aprovado", "Aprovado", "Cursando"]
    })