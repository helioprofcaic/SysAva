import streamlit as st
import pandas as pd
from services import database as db

def show_admin_view():
    st.subheader("👨‍🏫 Área do Professor - Correção e Notas")
    
    # 1. Seletores de Contexto
    classes = db.get_classes()
    class_options = {c['name']: c['id'] for c in classes}
    selected_class = st.selectbox("Turma", ["-- Selecione --"] + list(class_options.keys()))

    if selected_class != "-- Selecione --":
        class_id = class_options[selected_class]
        subjects = db.get_subjects_for_class(class_id)
        subject_options = {s['name']: s['id'] for s in subjects}
        
        selected_subject = st.selectbox("Disciplina", ["-- Selecione --"] + list(subject_options.keys()))
        
        if selected_subject != "-- Selecione --":
            subject_id = subject_options[selected_subject]
            assessments = db.get_assessments_by_subject(subject_id)
            assessment_map = {f"{a['type']} - {a['title']}": a for a in assessments}
            
            selected_assessment_key = st.selectbox("Avaliação", ["-- Selecione --"] + list(assessment_map.keys()))
            
            if selected_assessment_key != "-- Selecione --":
                assessment = assessment_map[selected_assessment_key]
                st.divider()
                
                # 2. Lista de Submissões
                submissions = db.get_assessment_submissions_with_users(assessment['id'])
                
                if not submissions:
                    st.info("Nenhum aluno realizou esta prova ainda.")
                else:
                    # --- Exportação CSV ---
                    df_export = []
                    for sub in submissions:
                        user_info = sub.get('app_users', {})
                        df_export.append({
                            "Nome": user_info.get('name'),
                            "RA": user_info.get('ra'),
                            "Data Envio": sub['submitted_at'],
                            "Nota Atual": sub['score'] if sub['score'] is not None else "Não avaliado"
                        })
                    
                    df = pd.DataFrame(df_export)
                    csv = df.to_csv(index=False).encode('utf-8')
                    
                    col_metrics, col_export = st.columns([0.7, 0.3])
                    col_metrics.metric("Total de Envios", len(submissions))
                    col_export.download_button(
                        label="📥 Exportar CSV",
                        data=csv,
                        file_name=f"notas_{assessment['type']}_{selected_class}.csv",
                        mime="text/csv"
                    )
                    
                    st.markdown("### 📝 Corrigir Provas")
                    
                    # Seletor de Aluno para Correção
                    student_options = {f"{s['app_users']['name']} ({s['app_users']['ra']})": s for s in submissions}
                    selected_student_key = st.selectbox("Selecione o Aluno para corrigir:", list(student_options.keys()))
                    
                    student_sub = student_options[selected_student_key]
                    
                    with st.form("grading_form"):
                        st.markdown(f"**Aluno:** {student_sub['app_users']['name']}")
                        st.markdown(f"**Nota Atual:** {student_sub['score'] if student_sub['score'] is not None else 'N/A'}")
                        st.divider()
                        
                        # Busca perguntas e respostas
                        questions = db.get_assessment_questions(assessment['id'])
                        answers = db.get_submission_answers(student_sub['id'])
                        answers_map = {a['question_id']: a for a in answers}
                        
                        # Exibe a prova respondida
                        for i, q in enumerate(questions):
                            ans = answers_map.get(q['id'])
                            st.markdown(f"**Questão {i+1}:** {q['question_text']}")
                            
                            if q['question_type'] == 'objective':
                                user_idx = ans['selected_option_index'] if ans else -1
                                correct_idx = q['correct_option_index']
                                options = q.get('options', [])
                                
                                user_text = options[user_idx] if 0 <= user_idx < len(options) else "Não respondeu"
                                correct_text = options[correct_idx] if 0 <= correct_idx < len(options) else "Erro"
                                
                                if user_idx == correct_idx:
                                    st.success(f"Resposta do Aluno: {user_text} (Correta)")
                                else:
                                    st.error(f"Resposta do Aluno: {user_text}")
                                    st.caption(f"Resposta Correta: {correct_text}")
                                    
                            elif q['question_type'] == 'subjective':
                                st.info(f"✍️ Resposta Subjetiva:")
                                st.text_area("Texto:", value=ans['answer_text'] if ans else "", disabled=True)
                                if ans and ans.get('answer_link'):
                                    st.markdown(f"🔗 **Link enviado:** [{ans['answer_link']}]({ans['answer_link']})")
                                else:
                                    st.caption("Nenhum link enviado.")
                            
                            st.divider()
                        
                        new_grade = st.number_input("Nota Final", min_value=0.0, max_value=10.0, value=float(student_sub['score'] or 0.0), step=0.5)
                        
                        if st.form_submit_button("💾 Salvar Nota"):
                            _, err = db.update_submission_score(student_sub['id'], new_grade)
                            if err: st.error(f"Erro: {err}")
                            else: 
                                st.success("Nota atualizada com sucesso!")
                                st.rerun()

def show_student_view():
    username = st.session_state.get('username')
    if not username:
        st.warning("Faça login para acessar suas avaliações.")
        return

    # 1. Identificar Turma e Disciplinas do Aluno
    enrollment = db.get_user_enrollment(username)
    if not enrollment:
        st.info("Você não está matriculado em nenhuma turma.")
        return
        
    class_id = enrollment['class_id']
    subjects = db.get_subjects_for_class(class_id)
    
    if not subjects:
        st.warning("Nenhuma disciplina encontrada para sua turma.")
        return
        
    # Seletor de Disciplina
    subject_map = {s['name']: s['id'] for s in subjects}
    selected_subject_name = st.selectbox("Selecione a Disciplina", list(subject_map.keys()))
    subject_id = subject_map[selected_subject_name]
    
    st.divider()
    
    # 2. Listar Avaliações Disponíveis
    assessments = db.get_assessments_by_subject(subject_id)
    
    if not assessments:
        st.info(f"Nenhuma avaliação agendada para {selected_subject_name}.")
        return
        
    # 3. Verificar Progresso (Critério MN1)
    stats = db.get_user_progress_stats(username)
    
    # Se não estiver fazendo uma prova, mostra a lista
    if 'active_assessment' not in st.session_state:
        for assessment in assessments:
            with st.container():
                col1, col2 = st.columns([0.7, 0.3])
                with col1:
                    st.subheader(f"{assessment['type']} - {assessment['title']}")
                
                # Verifica se já foi feita
                submission = db.get_student_submission(username, assessment['id'])
                
                if submission:
                    with col2:
                        st.success("✅ Concluída")
                    st.caption("Você já realizou esta avaliação. Aguarde a correção.")
                else:
                    # Lógica de Bloqueio MN1
                    is_locked = False
                    lock_reason = []
                    
                    if assessment['type'] == 'MN1':
                        if stats['lessons'] < 15: lock_reason.append(f"Aulas: {stats['lessons']}/15")
                        if stats['quizzes'] < 15: lock_reason.append(f"Quizzes: {stats['quizzes']}/15")
                        if stats['forum'] < 15: lock_reason.append(f"Fórum: {stats['forum']}/15")
                        
                        if lock_reason: is_locked = True
                    
                    elif assessment['type'] == 'MN2':
                        # Verifica se MN1 foi concluída
                        mn1_done = False
                        for a in assessments:
                            if a['type'] == 'MN1':
                                if db.get_student_submission(username, a['id']):
                                    mn1_done = True
                                break
                        
                        if not mn1_done: lock_reason.append("Pré-requisito: MN1 concluída")
                        if stats['lessons'] < 30: lock_reason.append(f"Aulas: {stats['lessons']}/30 (+15 novas)")
                        
                        if lock_reason: is_locked = True
                    
                    elif assessment['type'] == 'MN3':
                        # Verifica se MN2 foi concluída
                        mn2_done = False
                        for a in assessments:
                            if a['type'] == 'MN2':
                                if db.get_student_submission(username, a['id']):
                                    mn2_done = True
                                break
                        
                        if not mn2_done: lock_reason.append("Pré-requisito: MN2 concluída")
                        
                        if lock_reason: is_locked = True
                    
                    if is_locked:
                        with col2:
                            st.error("🔒 Bloqueada")
                        st.warning(f"Requisitos pendentes: {', '.join(lock_reason)}")
                        st.progress(min(stats['lessons']/15, 1.0), text="Progresso de Aulas")
                    else:
                        with col2:
                            if st.button("Iniciar Prova", key=f"start_{assessment['id']}"):
                                st.session_state.active_assessment = assessment
                                st.rerun()
                st.divider()

    # --- ÁREA DE REALIZAÇÃO DA PROVA ---
    else:
        assessment = st.session_state.active_assessment
        st.markdown(f"## ✍️ Realizando: {assessment['title']}")
        if st.button("Cancelar / Voltar"):
            del st.session_state.active_assessment
            st.rerun()
        
        questions = db.get_assessment_questions(assessment['id'])
        
        with st.form(key=f"assessment_form_{assessment['id']}"):
            answers = []
            for i, q in enumerate(questions):
                st.markdown(f"**Questão {i+1}:** {q['question_text']}")
                
                if q['question_type'] == 'objective':
                    opts = q.get('options', [])
                    val = st.radio("Selecione a alternativa:", opts, key=f"q_{q['id']}", index=None)
                    idx = opts.index(val) if val in opts else -1
                    answers.append({'question_id': q['id'], 'type': 'objective', 'value': idx})
                    
                elif q['question_type'] == 'subjective':
                    text_resp = st.text_area("Sua resposta:", key=f"txt_{q['id']}")
                    link_resp = ""
                    if q.get('options') and "LINK_REQUIRED" in q['options']:
                        link_resp = st.text_input("Link do projeto (GitHub/Drive):", key=f"lnk_{q['id']}")
                    answers.append({'question_id': q['id'], 'type': 'subjective', 'text': text_resp, 'link': link_resp})
                st.markdown("---")
            
            if st.form_submit_button("Finalizar e Enviar Avaliação"):
                # Validação simples
                if any((a['type'] == 'objective' and a['value'] == -1) for a in answers):
                    st.error("Responda todas as questões objetivas.")
                else:
                    success, err = db.submit_assessment(username, assessment['id'], answers)
                    if success:
                        st.success("Avaliação enviada com sucesso!")
                        del st.session_state.active_assessment
                        st.rerun()
                    else:
                        st.error(f"Erro ao enviar: {err}")

def show_page():
    st.header("📊 Avaliações e Provas")
    if st.session_state.get('role') == 'admin':
        show_admin_view()
    else:
        show_student_view()