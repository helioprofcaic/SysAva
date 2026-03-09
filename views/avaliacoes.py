import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from services import database as db
from datetime import datetime
import re

def markdown_to_html(text):
    if not text: return ""
    text = str(text)
    # Bold **text**
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Italic *text*
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    # Code `text`
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    return text

def generate_printable_view(school_name, subject_name, class_name, student_name, ra, score, questions, answers_map):
    date_str = datetime.now().strftime("%d/%m/%Y")
    
    html = f"""
    <html>
    <head>
        <style>
            @media print {{
                @page {{ 
                    size: A4;
                    margin: 13mm 20mm 20mm 20mm;
                }}
                body {{ margin: 0; }}
                .no-print {{ display: none; }}
                .print-container {{ 
                    border: none !important; 
                    padding: 0 !important; 
                    max-width: 100% !important; 
                    margin: 0 !important;
                }}
            }}
        </style>
    </head>
    <body>
    <div class="no-print" style="text-align: right; margin-bottom: 10px;">
        <button onclick="window.print()" style="padding: 10px 20px; font-size: 16px; cursor: pointer; background-color: #4CAF50; color: white; border: none; border-radius: 5px;">🖨️ Imprimir Agora</button>
    </div>
    <div class="print-container" style="font-family: Arial, sans-serif; padding: 40px; border: 1px solid #ccc; background-color: white; color: black; max-width: 800px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="margin: 0;">{school_name}</h2>
            <p style="margin: 5px 0;"><strong>Disciplina:</strong> {subject_name} | <strong>Turma:</strong> {class_name}</p>
            <p style="margin: 5px 0;"><strong>Data:</strong> {date_str} | <strong>Cidade:</strong> Teresina - PI</p>
        </div>
        
        <div style="border: 1px solid #000; padding: 10px; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between;">
                <span><strong>Aluno(a):</strong> {student_name}</span>
                <span><strong>Nota Final:</strong> {score if score is not None else 'Pendente'}</span>
            </div>
            <p style="margin: 5px 0 0 0;"><strong>RA:</strong> {ra}</p>
        </div>
        
        <h3 style="border-bottom: 2px solid #000; padding-bottom: 5px;">Relatório de Avaliação</h3>
    """
    
    for i, q in enumerate(questions):
        ans = answers_map.get(q['id'])
        
        q_text = markdown_to_html(q['question_text'])
        user_resp = "Não respondeu"
        correct_resp = ""
        is_correct = False
        
        if q['question_type'] == 'objective':
            options = q.get('options', [])
            correct_idx = q.get('correct_option_index', 0)
            correct_resp = markdown_to_html(options[correct_idx]) if 0 <= correct_idx < len(options) else "?"
            
            if ans:
                user_idx = ans.get('selected_option_index', -1)
                if 0 <= user_idx < len(options):
                    user_resp = markdown_to_html(options[user_idx])
                is_correct = (user_idx == correct_idx)
        else:
            user_resp = ans.get('answer_text', '') if ans else ""
            link = ans.get('answer_link', '') if ans else ""
            if link:
                user_resp += f" <br>(Link: {link})"
            correct_resp = "(Questão Subjetiva)"
        
        color = "green" if is_correct else "red" if q['question_type'] == 'objective' else "black"
        icon = "✅" if is_correct else "❌" if q['question_type'] == 'objective' else "📝"
        
        html += f"""
        <div style="margin-bottom: 10px; border-bottom: 1px dotted #ccc; padding-bottom: 5px;">
            <p style="margin: 0 0 5px 0;"><strong>{i+1}. {q_text}</strong></p>
            <p style="margin: 0; color: {color};">Sua Resposta: {icon} {user_resp}</p>
            {f'<p style="margin: 0; font-size: 0.9em; color: #555;">Gabarito: {correct_resp}</p>' if not is_correct and q['question_type'] == 'objective' else ''}
        </div>
        """
        
    html += """
        <br><br><br><br>
        <div style="display: flex; justify-content: space-between; margin-top: 50px;">
           
        </div>
    </div>
    </body>
    </html>
    """
    return html

def generate_blank_printable_view(school_name, subject_name, class_name, assessment_title, questions):
    """Gera uma visualização de impressão para uma prova em branco."""
    
    html = f"""
    <html>
    <head>
        <style>
            @media print {{
                @page {{ 
                    size: A4;
                    margin: 13mm 20mm 20mm 20mm;
                }}
                body {{ margin: 0; }}
                .no-print {{ display: none; }}
                .print-container {{ 
                    border: none !important; 
                    padding: 0 !important; 
                    max-width: 100% !important; 
                    margin: 0 !important;
                }}
            }}
        </style>
    </head>
    <body>
    <div class="no-print" style="text-align: right; margin-bottom: 10px;">
        <button onclick="window.print()" style="padding: 10px 20px; font-size: 16px; cursor: pointer; background-color: #4CAF50; color: white; border: none; border-radius: 5px;">🖨️ Imprimir Agora</button>
    </div>
    <div class="print-container" style="font-family: Arial, sans-serif; padding: 40px; border: 1px solid #ccc; background-color: white; color: black; max-width: 800px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="margin: 0;">{school_name}</h2>
            <p style="margin: 5px 0;"><strong>Disciplina:</strong> {subject_name} | <strong>Turma:</strong> {class_name}</p>
            
            <p style="margin: 5px 0;"><strong>Data:</strong> ___/___/______ | <strong>Cidade:</strong> Teresina - PI</p>
        </div>
        
        <div style="border: 1px solid #000; padding: 10px; margin-bottom: 15px; display: flex; justify-content: space-between;">
            <span><strong>Aluno(a):</strong> ___________________________________________________</span>
            <span><strong>Nota Final:</strong> _________</span>
        </div>
        
        <p style="margin: 5px 0;"><strong>Avaliação:</strong> {assessment_title}</p>
    """
    
    for i, q in enumerate(questions):
        q_text = markdown_to_html(q['question_text'])
        html += f"""
        <div style="margin-bottom: 15px; padding-bottom: 5px; border-bottom: 1px dotted #ccc;">
            <p style="margin: 0 0 5px 0;"><strong>{i+1}. {q_text}</strong></p>
        """
        if q['question_type'] == 'objective':
            options = q.get('options', [])
            for opt in options:
                opt_html = markdown_to_html(opt)
                html += f'<p style="margin: 5px 0 5px 20px;">( &nbsp; ) {opt_html}</p>'
        else: # subjective
            if q.get('options') and "LINK_REQUIRED" in q['options']:
                 html += '<p style="margin: 5px 0 5px 20px;">Link para envio: ________________________________________________</p>'
            html += '<div style="border: 1px solid #ddd; height: 120px; margin-top: 10px; padding: 5px;"></div>'
            
        html += "</div>"
        
    html += """
        <br><br>
        <div style="text-align: center; margin-top: 35px; font-style: italic; font-size: 1.1em;">
            Boa sorte! 🍀
        </div>
    </div>
    </body>
    </html>
    """
    return html

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

                if st.button("🖨️ Imprimir Prova em Branco"):
                    school_info = db.get_school()
                    school_name = school_info['name'] if school_info else "Escola Técnica"
                    questions = db.get_assessment_questions(assessment['id'])
                    
                    blank_html = generate_blank_printable_view(
                        school_name,
                        selected_subject,
                        selected_class,
                        assessment['title'],
                        questions
                    )
                    components.html(blank_html, height=600, scrolling=True)
                    # Para a execução para não mostrar o resto da página, focando na impressão
                    st.stop()
                
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
                    
                    if st.button("🖨️ Visualizar Impressão"):
                        school_info = db.get_school()
                        school_name = school_info['name'] if school_info else "Escola Técnica"
                        
                        questions = db.get_assessment_questions(assessment['id'])
                        answers = db.get_submission_answers(student_sub['id'])
                        answers_map = {a['question_id']: a for a in answers}
                        
                        html_content = generate_printable_view(
                            school_name, 
                            selected_subject, 
                            selected_class, 
                            student_sub['app_users']['name'], 
                            student_sub['app_users']['ra'], 
                            student_sub['score'], 
                            questions, 
                            answers_map
                        )
                        components.html(html_content, height=600, scrolling=True)

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
                    score = submission.get('score')
                    with col2:
                        if score is not None:
                            st.success(f"Nota: {score}")
                        else:
                            st.success("✅ Concluída")
                    st.caption("Avaliação corrigida." if score is not None else "Você já realizou esta avaliação. Aguarde a correção.")
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
    if st.session_state.get('role') in ['admin', 'teacher']:
        show_admin_view()
    else:
        show_student_view()