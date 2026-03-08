import streamlit as st
from services import database as db
import json

def show_page():
    st.header("📝 Quiz da Aula")

    quiz_id = st.session_state.get('context_quiz_id')

    if not quiz_id:
        st.error("Nenhum quiz selecionado. Volte para a página de aulas e escolha um.")
        if st.button("⬅️ Voltar para as Aulas"):
            st.session_state.page = 'Aulas'
            st.rerun()
        return

    questions = db.get_quiz_questions(quiz_id)

    if not questions:
        st.warning("Este quiz ainda não tem perguntas.")
        if st.button("⬅️ Voltar para as Aulas"):
            st.session_state.page = 'Aulas'
            st.rerun()
        return

    with st.form("quiz_form"):
        responses = {}
        for i, q in enumerate(questions):
            st.write(f"**{i+1}. {q['question_text']}**")
            # As opções estão em JSON, precisamos carregar
            options = json.loads(q['options']) if isinstance(q['options'], str) else q['options']
            responses[q['id']] = st.radio(f"Resposta {i+1}:", options, key=f"q_{q['id']}", label_visibility="collapsed")
        
        submitted = st.form_submit_button("Enviar Respostas")
        
        if submitted:
            score = 0
            total = len(questions)
            for q in questions:
                user_answer = responses[q['id']]
                options = json.loads(q['options']) if isinstance(q['options'], str) else q['options']
                correct_answer = options[q['correct_option_index']]
                if user_answer == correct_answer:
                    score += 1
            
            st.session_state['quiz_score'] = score
            
            if score == total:
                st.balloons()
                st.success(f"Parabéns! Você acertou {score}/{total}.")
            else:
                st.warning(f"Você acertou {score}/{total}. Continue estudando!")
            
            st.info("Você pode fechar esta aba ou voltar para as aulas.")

    if st.button("⬅️ Voltar para as Aulas"):
        st.session_state.page = 'Aulas'
        st.rerun()
