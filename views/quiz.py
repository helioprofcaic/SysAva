import streamlit as st

def show_page():
    st.header("📝 Quiz de Conhecimento")
    
    with st.form("quiz_form"):
        st.write("1. Qual comando usamos para exibir texto no Streamlit?")
        q1 = st.radio("Resposta 1:", ["print()", "st.write()", "console.log()"], key="q1")
        
        st.write("2. O Streamlit é baseado em qual linguagem?")
        q2 = st.radio("Resposta 2:", ["Java", "Python", "C++"], key="q2")
        
        submitted = st.form_submit_button("Enviar Respostas")
        
        if submitted:
            score = 0
            if q1 == "st.write()": score += 1
            if q2 == "Python": score += 1
            
            if 'quiz_score' not in st.session_state:
                st.session_state['quiz_score'] = 0
            st.session_state['quiz_score'] = score
            
            if score == 2:
                st.balloons()
                st.success(f"Parabéns! Você acertou {score}/2.")
            else:
                st.warning(f"Você acertou {score}/2. Tente novamente!")