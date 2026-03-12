import streamlit as st
from services import database as db
import json

def show_page():
    quiz_id = st.session_state.get('context_quiz_id')

    if not quiz_id:
        st.error("Nenhum quiz selecionado. Volte para a página de aulas e escolha um.")
        if st.button("⬅️ Voltar para as Aulas"):
            st.session_state.page = 'Aulas'
            if 'context_quiz_id' in st.session_state: del st.session_state['context_quiz_id']
            st.rerun()
        return

    # Busca os dados do quiz e da aula para dar mais contexto ao aluno
    quiz_data = db.get_quiz_by_id(quiz_id)
    lesson_data = db.get_lesson_by_id(quiz_data['lesson_id']) if quiz_data else None

    if not quiz_data or not lesson_data:
        st.error("Não foi possível carregar os dados do quiz ou da aula associada.")
        if st.button("⬅️ Voltar para as Aulas"):
            st.session_state.page = 'Aulas'
            if 'context_quiz_id' in st.session_state: del st.session_state['context_quiz_id']
            st.rerun()
        return

    st.header(f"📝 Quiz: {quiz_data['title']}")
    st.subheader(f"Referente à aula: {lesson_data['title']}")
    st.divider()

    questions = db.get_quiz_questions(quiz_id)

    if not questions:
        st.warning("Este quiz ainda não tem perguntas.")
        if st.button("⬅️ Voltar para a Aula"):
            st.session_state.page = 'Aulas'
            if 'context_quiz_id' in st.session_state: del st.session_state['context_quiz_id']
            st.rerun()
        return

    # Verifica se o usuário já respondeu a este quiz nesta sessão
    session_key_submitted = f"quiz_{quiz_id}_submitted"
    if session_key_submitted in st.session_state:
        score = st.session_state.get(f"quiz_{quiz_id}_score", 0)
        total = st.session_state.get(f"quiz_{quiz_id}_total", len(questions))
        st.success(f"Você já concluiu este quiz. Sua pontuação foi: {score}/{total}")
        if st.button("⬅️ Voltar para a Aula"):
            st.session_state.page = 'Aulas'
            if 'context_quiz_id' in st.session_state: del st.session_state['context_quiz_id']
            st.rerun()
        return

    with st.form("quiz_form"):
        responses = {}
        for i, q in enumerate(questions):
            st.write(f"**{i+1}. {q['question_text']}**")
            # O cliente Supabase já converte JSONB para lista/dicionário Python
            options = q['options']
            responses[q['id']] = st.radio(f"Resposta {i+1}:", options, key=f"q_{q['id']}", label_visibility="collapsed")
        
        submitted = st.form_submit_button("Enviar Respostas")
        
        if submitted:
            score = 0
            total = len(questions)
            for q in questions:
                user_answer = responses[q['id']]
                options = q['options']
                correct_answer = options[q['correct_option_index']]
                if user_answer == correct_answer:
                    score += 1
            
            subject_id = lesson_data['subject_id'] if lesson_data else 0
            # Registra no histórico
            db.add_user_history(st.session_state.get('username'), f"Concluiu Quiz: {quiz_data['title']} ({score}/{total}) | subject_id:{subject_id}")

            # Salva o resultado na sessão para evitar que o aluno refaça o teste
            st.session_state[session_key_submitted] = True
            st.session_state[f"quiz_{quiz_id}_score"] = score
            st.session_state[f"quiz_{quiz_id}_total"] = total
            
            # Reroda a página para mostrar o resultado final de forma limpa
            st.rerun()

    if st.button("⬅️ Voltar para a Aula"):
        st.session_state.page = 'Aulas'
        if 'context_quiz_id' in st.session_state: del st.session_state['context_quiz_id']
        st.rerun()
