import streamlit as st
from services import database as db
import pandas as pd
import re
import html

def format_display_text(text):
    """
    Formata texto para exibição correta no Markdown do Streamlit:
    1. Desfaz entidades HTML literais (&lt; -> <, &gt; -> >).
    2. Tags HTML soltas (como <section>, <div>) são automaticamente envolvidas em crases `<tag>`.
    3. Tags já dentro de crases são mantidas como código inline.
    Isso evita quebras de linha e exibe a tag formatada sem mostrar texto '&lt;'.
    """
    if not text:
        return ""
    text = html.unescape(str(text))

    parts = text.split('`')
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(?<!`)(</?[a-zA-Z][a-zA-Z0-9_\-]*(\s+[^>]*)?>)(?!`)', r'`\1`', parts[i])
    
    result = '`'.join(parts)
    result = re.sub(r'``+', r'`', result)
    return result

def show_page():
    quiz_id = st.session_state.get('context_quiz_id')

    if not quiz_id:
        st.error("Nenhum quiz selecionado. Volte para a página de aulas e escolha um.")
        if st.button("⬅️ Voltar para as Aulas"):
            st.session_state.page = 'Aulas'
            if 'context_quiz_id' in st.session_state: del st.session_state['context_quiz_id']
            st.rerun()
        return

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

    # --- LÓGICA DE TENTATIVAS E HISTÓRICO ---
    username = st.session_state.get('username')
    history = db.get_user_history(username)
    
    # Filtra tentativas deste quiz no histórico do usuário
    quiz_attempts = []
    quiz_title = quiz_data['title']
    for h in history:
        act = h.get('activity', '')
        if not act.startswith("Concluiu Quiz:"):
            continue

        # Identifica a tentativa pelo ID do quiz (logs novos). Em logs antigos,
        # usa o título apenas quando ele é específico (títulos genéricos colidem).
        match_qid = re.search(r'\| quiz_id:(\d+)', act)
        if match_qid:
            if int(match_qid.group(1)) != int(quiz_id):
                continue
        else:
            if db.is_generic_quiz_title(quiz_title):
                continue
            if not act.startswith(f"Concluiu Quiz: {quiz_title}"):
                continue

        match = re.search(r'\((\d+/\d+)\)', act)
        score_str = match.group(1) if match else "N/A"
        quiz_attempts.append({
            "Data": h.get('timestamp'),
            "Resultado (Acertos)": score_str
        })

    # Exibe a tabela de tentativas logo abaixo do cabeçalho
    if quiz_attempts:
        st.markdown("### 📊 Suas Tentativas Anteriores")
        df_attempts = pd.DataFrame(quiz_attempts)
        try:
            df_attempts['Data'] = pd.to_datetime(df_attempts['Data']).dt.strftime('%d/%m/%Y %H:%M')
        except:
            pass
        st.table(df_attempts)
    else:
        st.info("Você ainda não realizou este quiz.")

    questions = db.get_quiz_questions(quiz_id)
    if not questions:
        st.warning("Este quiz ainda não tem perguntas.")
        if st.button("⬅️ Voltar para a Aula"):
            st.session_state.page = 'Aulas'
            if 'context_quiz_id' in st.session_state: del st.session_state['context_quiz_id']
            st.rerun()
        return

    num_attempts = len(quiz_attempts)
    max_attempts = 3
    session_key_submitted = f"quiz_{quiz_id}_submitted"

    # --- VERIFICAÇÃO DE ESTADO ---
    
    # Se o usuário acabou de submeter o formulário nesta sessão
    if session_key_submitted in st.session_state:
        score = st.session_state.get(f"quiz_{quiz_id}_score", 0)
        total = st.session_state.get(f"quiz_{quiz_id}_total", len(questions))
        st.success(f"Concluído! Sua pontuação nesta tentativa: {score}/{total}")
        
        st.markdown("### Revisão das Respostas:")
        responses = st.session_state.get(f"quiz_{quiz_id}_responses", {})
        
        for i, q in enumerate(questions):
            st.markdown(f"**{i+1}. {format_display_text(q['question_text'])}**")
            correct_answer = q['options'][q['correct_option_index']]
            user_answer = responses.get(q['id'])
            
            for opt in q['options']:
                if opt == correct_answer:
                    st.success(f"✓ {format_display_text(opt)}")
                elif opt == user_answer:
                    st.error(f"✗ {format_display_text(opt)}")
                else:
                    st.markdown(f"&nbsp;&nbsp;&nbsp; ( ) {format_display_text(opt)}")
            
            with st.expander("⚠️ Reportar Problema", expanded=False):
                reason = st.text_input("Qual o problema com esta questão?", key=f"req_{q['id']}")
                if st.button("Enviar Reporte", key=f"btn_req_{q['id']}"):
                    if reason:
                        report_text = f"🚨 REPORTE DE ERRO (Quiz {quiz_id}): Questão {q['id']} - {reason}"
                        db.add_user_history(username, report_text)
                        st.success("Problema reportado!")
                    else:
                        st.warning("Descreva o problema.")
            st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Voltar para a Aula", use_container_width=True):
                st.session_state.page = 'Aulas'
                if 'context_quiz_id' in st.session_state: del st.session_state['context_quiz_id']
                st.rerun()
        with col2:
            if num_attempts < max_attempts:
                if st.button("🔄 Tentar Novamente", use_container_width=True):
                    if session_key_submitted in st.session_state: del st.session_state[session_key_submitted]
                    st.rerun()
            else:
                st.warning("Limite de tentativas atingido.")
        return

    # Se já atingiu o limite de tentativas e não está visualizando um resultado recém-enviado
    if num_attempts >= max_attempts:
        st.error(f"Você já utilizou suas {max_attempts} tentativas permitidas.")
        if st.button("⬅️ Voltar para a Aula"):
            st.session_state.page = 'Aulas'
            if 'context_quiz_id' in st.session_state: del st.session_state['context_quiz_id']
            st.rerun()
        return

    # --- FORMULÁRIO PARA REALIZAR O QUIZ ---
    st.subheader("📝 Responder Quiz")
    st.info(f"Tentativa {num_attempts + 1} de {max_attempts}")

    with st.form("quiz_form"):
        responses = {}
        for i, q in enumerate(questions):
            st.write(f"**{i+1}. {format_display_text(q['question_text'])}**")
            options = q['options']
            responses[q['id']] = st.radio(
                f"Opções para a questão {i+1}:", 
                options, 
                key=f"q_{q['id']}", 
                label_visibility="collapsed",
                format_func=format_display_text
            )
        
        submitted = st.form_submit_button("Enviar Respostas")
        
        if submitted:
            score = 0
            for q in questions:
                user_answer = responses[q['id']]
                correct_answer = q['options'][q['correct_option_index']]
                if user_answer == correct_answer:
                    score += 1
            
            subject_id = lesson_data['subject_id'] if lesson_data else 0
            db.add_user_history(username, f"Concluiu Quiz: {quiz_data['title']} ({score}/{len(questions)}) | subject_id:{subject_id} | quiz_id:{quiz_id}")

            st.session_state[session_key_submitted] = True
            st.session_state[f"quiz_{quiz_id}_score"] = score
            st.session_state[f"quiz_{quiz_id}_total"] = len(questions)
            st.session_state[f"quiz_{quiz_id}_responses"] = responses
            st.rerun()

    if st.button("⬅️ Voltar para a Aula"):
        st.session_state.page = 'Aulas'
        if 'context_quiz_id' in st.session_state: del st.session_state['context_quiz_id']
        st.rerun()
