import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from services import database as db
from datetime import datetime
import re

# Tenta importar o componente de JS, se não existir, a funcionalidade ficará desabilitada.
try:
    from streamlit_javascript import st_javascript
except ImportError:
    st_javascript = None
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

def generate_assessment_print_html(school_name, subject_name, class_name, assessment_title, questions, assessment_type):
    """Gera HTML formatado para impressao da prova completa."""
    date_str = datetime.now().strftime("%d/%m/%Y")

    rows_html = ""
    for i, q in enumerate(questions):
        q_text = markdown_to_html(q['question_text'])
        options_html = ""
        if q['question_type'] == 'objective':
            for opt in q.get('options', []):
                opt_html = markdown_to_html(opt)
                options_html += f'<p style="margin: 5px 0 5px 20px;">( &nbsp; ) {opt_html}</p>'
        else:
            if q.get('options') and "LINK_REQUIRED" in q['options']:
                options_html += '<p style="margin: 5px 0 5px 20px;">Link para envio: ________________________________________________</p>'
            options_html += '<div style="border: 1px solid #ddd; height: 100px; margin-top: 10px; padding: 5px;"></div>'

        rows_html += f"""
        <div style="margin-bottom: 15px; padding-bottom: 5px; border-bottom: 1px dotted #ccc;">
            <p style="margin: 0 0 5px 0;"><strong>{i+1}. {q_text}</strong></p>
            {options_html}
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Avaliação - {assessment_title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
            .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }}
            .header h1 {{ margin: 0; font-size: 20px; }}
            .header p {{ margin: 5px 0; color: #666; }}
            .student-info {{ border: 1px solid #000; padding: 10px; margin-bottom: 15px; display: flex; justify-content: space-between; }}
            @media print {{
                .no-print {{ display: none !important; }}
                body {{ margin: 0; padding: 15mm; }}
                @page {{ size: A4; margin: 15mm; }}
            }}
        </style>
    </head>
    <body>
        <div class="no-print" style="text-align: center; margin-bottom: 15px;">
            <button onclick="window.print()" style="background-color: #4CAF50; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; font-size: 14px;">IMPRIMIR / SALVAR PDF</button>
        </div>
        <div class="header">
            <h1>{school_name}</h1>
            <p><strong>Disciplina:</strong> {subject_name} | <strong>Turma:</strong> {class_name}</p>
            <p><strong>Avaliação:</strong> {assessment_title} ({assessment_type}) | <strong>Data:</strong> {date_str}</p>
        </div>
        <div class="student-info">
            <span><strong>Aluno(a):</strong> _________________________________________________</span>
            <span><strong>Nota Final:</strong> _________</span>
        </div>
        <p><strong>RA:</strong> ___________________</p>
        <hr style="margin: 15px 0;">
        {rows_html}
        <br>
        <div style="text-align: center; margin-top: 30px; font-style: italic;">
            Boa prova!
        </div>
    </body>
    </html>
    """
    return html

def show_admin_view():
    st.subheader("Area do Professor - Correcao e Notas")

    # 1. Seletores de Contexto
    classes = db.get_classes()
    class_options = {c['name']: c['id'] for c in classes}
    selected_class = st.selectbox("Turma", ["-- Selecione --"] + list(class_options.keys()))

    if selected_class != "-- Selecione --":
        class_id = class_options[selected_class]
        subjects = db.get_subjects_for_class(class_id)
        subjects = [s for s in subjects if s.get('is_active', True)]

        subject_options = {s['name']: s['id'] for s in subjects}

        selected_subject = st.selectbox("Disciplina", ["-- Selecione --"] + list(subject_options.keys()))

        if selected_subject != "-- Selecione --":
            subject_id = subject_options[selected_subject]

            # 3. Seletor de Trimestre/Tipo
            trimester_options = {
                "Todos": "Todos",
                "1 Trimestre": "T1",
                "2 Trimestre": "T2",
                "3 Trimestre": "T3",
                "Recuperacao": "RM",
                "Outros": "Outros"
            }
            selected_trimester_label = st.selectbox("Trimestre", list(trimester_options.keys()))
            selected_type_prefix = trimester_options[selected_trimester_label]

            # 4. Seletor de Avaliacao (filtrado)
            all_assessments = db.get_assessments_by_subject(subject_id)
            if selected_type_prefix == "Todos":
                filtered_assessments = all_assessments
            elif selected_type_prefix in ["RM", "Outros"]:
                filtered_assessments = [a for a in all_assessments if a['type'] == selected_type_prefix]
            else:
                filtered_assessments = [a for a in all_assessments if a['type'] and a['type'].startswith(selected_type_prefix)]

            assessment_map = {f"{a['type']} - {a['title']}": a for a in filtered_assessments}
            selected_assessment_key = st.selectbox("Avaliacao", ["-- Selecione --"] + list(assessment_map.keys()))

            if selected_assessment_key != "-- Selecione --":
                assessment = assessment_map[selected_assessment_key]
                st.divider()

                # ====================================================================
                # EMISSAO / IMPRESSAO DE PROVAS
                # ====================================================================
                st.markdown("#### Emissao / Impressao de Prova")

                col_print, col_save, col_email = st.columns(3)

                # Prepara dados para impressao
                school_info = db.get_school()
                school_name = school_info['name'] if school_info else "Escola Tecnica"
                questions = db.get_assessment_questions(assessment['id'])

                # Gera HTML da prova (com campos para aluno preencher)
                blank_html = generate_assessment_print_html(
                    school_name,
                    selected_subject,
                    selected_class,
                    assessment['title'],
                    questions,
                    assessment['type']
                )

                with col_print:
                    if st.button("Imprimir Prova", width="stretch", key="btn_print_assessment"):
                        components.html(blank_html, height=600, scrolling=True)
                        st.stop()

                with col_save:
                    st.download_button(
                        label="Salvar PDF",
                        data=blank_html.encode('utf-8'),
                        file_name=f"prova_{assessment['type']}_{selected_subject.replace(' ', '_')}.html",
                        mime="text/html",
                        width="stretch",
                        key="btn_save_assessment"
                    )

                with col_email:
                    # Campo de email para envio
                    email_to = st.text_input("Email do destinatario:", placeholder="professor@escola.edu.br", key="email_to_assessment")
                    if st.button("Enviar por Email", width="stretch", key="btn_email_assessment", disabled=not email_to):
                        with st.spinner("Enviando email..."):
                            filename = f"prova_{assessment['type']}_{selected_subject.replace(' ', '_')}.html"
                            success, err = db.send_email_with_attachment(
                                to_email=email_to,
                                subject=f"Prova: {assessment['title']} - {selected_subject}",
                                html_content=blank_html,
                                filename=filename
                            )
                            if success:
                                st.success(f"Email enviado com sucesso para {email_to}!")
                            else:
                                st.error(f"Erro ao enviar email: {err}")

                if st.button("Visualizar Prova", key="btn_preview_assessment"):
                    components.html(blank_html, height=700, scrolling=True)
                    st.stop()

                st.divider()
                
                # 2. Lista de Submissões
                submissions = db.get_assessment_submissions_with_users(assessment['id'])
                original_data_key = f"original_data_{assessment['id']}"

                # --- LÓGICA PARA COPIAR NOTAS DO 1º TRIMESTRE (Disciplinas Técnicas) ---
                # Aparece se for uma avaliação do 2º ou 3º trimestre e houver submissões
                current_type = assessment['type']
                # Condição para não exibir em disciplinas da base comum como IA
                is_common_base_subject = "INTELIGÊNCIA ARTIFICIAL" in selected_subject.upper()

                if current_type and (current_type.startswith('T2_') or current_type.startswith('T3_')) and submissions and not is_common_base_subject:

                    # Determina o tipo de avaliação correspondente no 1º trimestre
                    source_type = current_type.replace('T2_', 'T1_').replace('T3_', 'T1_')
                    
                    st.info(f"💡 **Dica:** Para disciplinas técnicas, você pode replicar as notas da avaliação do 1º Trimestre.")
                    if st.button(f"➡️ Copiar Notas de '{source_type}' para esta avaliação ({current_type})"):
                        with st.spinner(f"Buscando notas de '{source_type}'..."):
                            # 1. Encontrar a avaliação correspondente do 1º trimestre
                            source_assessment = next((a for a in all_assessments if a['type'] == source_type), None)
                            
                            if not source_assessment:
                                st.error(f"Nenhuma avaliação do tipo '{source_type}' encontrada para esta disciplina.")
                            else:
                                # 2. Obter as notas da avaliação de origem
                                source_submissions = db.get_assessment_submissions_with_users(source_assessment['id'])
                                source_scores = {
                                    sub.get('app_users', {}).get('username'): sub.get('score')
                                    for sub in source_submissions if sub.get('score') is not None
                                }

                                # 3. Atualizar o cache (st.session_state) com as notas da MN1
                                if original_data_key in st.session_state:
                                    cached_data = st.session_state[original_data_key]
                                    for student_row in cached_data:
                                        username = student_row['_user_info'].get('username')
                                        if username in source_scores:
                                            student_row['Nota'] = source_scores[username]
                                    st.success(f"Notas de '{source_type}' copiadas para a tabela abaixo. Clique em 'Salvar' para confirmar.")
                                    st.rerun()
                                else:
                                    st.warning("A tabela de dados ainda não foi carregada. Tente novamente.")
                
                if not submissions:
                    st.info("Nenhum aluno realizou esta prova ainda.")
                else:
                    # --- Montagem dos dados para exibição e exportação ---
                    with st.spinner("Buscando scores dos alunos..."):

                        # 1. Pega todas as questões da avaliação para montar as colunas
                        questions = db.get_assessment_questions(assessment['id'])
                        
                        # 2. Prepara o cabeçalho dinâmico para as questões
                        question_headers = {f"Q{i+1}": q for i, q in enumerate(questions)}

                        table_data = []
                        for sub in sorted(submissions, key=lambda x: x.get('app_users', {}).get('name', '')):
                            user_info = sub.get('app_users', {})
                            
                            # Busca as respostas do aluno para esta submissão
                            answers = db.get_submission_answers(sub['id'])
                            answers_map = {a['question_id']: a for a in answers}

                            # Monta a linha do aluno
                            student_row = {
                                "Nome": user_info.get('name'),
                                "Nota": sub['score'] if sub['score'] is not None else None,
                                "Visualizar": False,
                                "_submission": sub, # hidden column
                                "_user_info": user_info # hidden column
                            }

                            # Preenche as colunas de questão (Q1, Q2, ...)
                            for header, question in question_headers.items():
                                answer_text = "---" # Padrão
                                ans = answers_map.get(question['id'])
                                if ans:
                                    if question['question_type'] == 'objective':
                                        idx = ans.get('selected_option_index')
                                        opts = question.get('options', [])
                                        if idx is not None and 0 <= idx < len(opts):
                                            answer_text = opts[idx]
                                    else:
                                        answer_text = ans.get('answer_text', '')
                                student_row[header] = answer_text
                            table_data.append(student_row)

                        # Limpa o cache se a avaliação mudar
                        if st.session_state.get('last_assessment_id_for_cache') != assessment['id']:
                            if original_data_key in st.session_state:
                                del st.session_state[original_data_key]
                        st.session_state['last_assessment_id_for_cache'] = assessment['id']

                        # Força a atualização se o cache estiver vazio ou se o número de submissões divergir do banco
                        if original_data_key not in st.session_state or not st.session_state[original_data_key] or len(st.session_state[original_data_key]) != len(table_data):
                            st.session_state[original_data_key] = table_data
                        
                        df = pd.DataFrame(st.session_state[original_data_key]).reset_index()
                    
                    # --- Métricas e Exportação ---
                    df_display = df.drop(columns=['index', '_submission', '_user_info'], errors='ignore')
                    csv = df_display.to_csv(index=False).encode('utf-8')

                    col_metrics, col_export = st.columns([0.7, 0.3])
                    col_metrics.metric("Total de Envios", len(submissions))
                    col_export.download_button(
                        label="📥 Exportar Notas (CSV)",
                        data=csv,
                        file_name=f"notas_{assessment['type']}_{selected_class}.csv",
                        mime="text/csv"
                    )
                    
                    st.markdown("### 📝 Submissões dos Alunos")
                    # Mantendo apenas a versão moderna (Batch Editor)
                    column_config = {"Nome": st.column_config.TextColumn("Nome do Aluno", width="large", disabled=True), "Nota": st.column_config.NumberColumn("Nota Final", min_value=0.0, max_value=10.0, step=0.5, format="%.2f"), "Visualizar": st.column_config.CheckboxColumn("👁️"), "index": None, "_submission": None, "_user_info": None}
                    for h in question_headers.keys(): column_config[h] = st.column_config.TextColumn(h, width="small", disabled=True)
                    edited_df = st.data_editor(df, column_config=column_config, width="stretch", hide_index=True)
                    if st.button("💾 Salvar Todas as Notas Alteradas", type="primary", width="stretch"):
                        for idx, row in edited_df.iterrows():
                            orig = df.loc[df['index'] == row['index']].iloc[0]
                            if row['Nota'] is not None and (pd.isna(orig['Nota']) or orig['Nota'] != row['Nota']):
                                db.update_submission_score(orig['_submission'].get('id'), row['Nota'])
                        st.success("Notas atualizadas!"); st.rerun()

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
    # Filtra as disciplinas ativas para a visão do aluno
    subjects = [s for s in subjects if s.get('is_active', True)]
    
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

                submissions = db.get_student_submissions(username, assessment['id'])
                attempts = len(submissions)

                if attempts > 0:
                    best_score = -1
                    is_corrected = False
                    for sub in submissions: 
                        s = sub.get('score')
                        if s is not None: 
                            is_corrected = True
                            if s > best_score: best_score = s
                    
                    if is_corrected: st.success(f"**Melhor Nota: {best_score}**")
                    else: st.caption("Aguardando correção.")

                if attempts < 2:
                    st.caption("Você ainda não realizou esta avaliação.")
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

                            label = f"Iniciar {'Nova ' if attempts > 0 else ''}Tentativa ({attempts + 1}/2)"
                            if st.button(label, key=f"start_{assessment['id']}_{attempts}"):
                                st.session_state.active_assessment = assessment
                                st.rerun()

                    # Botao para imprimir a prova (disponivel antes de iniciar)
                    if not is_locked and attempts < 2:
                        with st.expander("Imprimir Prova (responder no papel)", expanded=False):
                            school_info = db.get_school()
                            school_name = school_info['name'] if school_info else "Escola Tecnica"
                            questions_print = db.get_assessment_questions(assessment['id'])

                            # Busca nome da turma
                            enrollment = db.get_user_enrollment(username)
                            class_name = "Turma"
                            if enrollment:
                                classes_all = db.get_classes()
                                for c in classes_all:
                                    if c['id'] == enrollment['class_id']:
                                        class_name = c['name']
                                        break

                            blank_html = generate_blank_printable_view(
                                school_name,
                                selected_subject_name,
                                class_name,
                                assessment['title'],
                                questions_print
                            )

                            col_prev, col_dl = st.columns(2)
                            with col_prev:
                                if st.button("Visualizar Prova", key=f"preview_std_{assessment['id']}"):
                                    components.html(blank_html, height=700, scrolling=True)
                                    st.stop()
                            with col_dl:
                                st.download_button(
                                    label="Salvar Prova (HTML)",
                                    data=blank_html.encode('utf-8'),
                                    file_name=f"prova_{assessment['type']}.html",
                                    mime="text/html",
                                    key=f"dl_std_{assessment['id']}"
                                )
                else: # attempts >= 2
                    with col2:
                        st.success("✅ Concluído")
                    st.caption("Você já utilizou todas as suas tentativas para esta avaliação.")
                st.divider()

    # --- ÁREA DE REALIZAÇÃO DA PROVA ---
    else:
        assessment = st.session_state.active_assessment
        st.markdown(f"## ✍️ Realizando: {assessment['title']}")
        if st.button("Cancelar / Voltar"):
            del st.session_state.active_assessment
            st.rerun()


        # --- NOVO: Detector de Perda de Foco ---
        if st_javascript is None:
            st.warning("A biblioteca 'streamlit-javascript' não está instalada. O monitoramento de foco está desativado.")
        else:
            # Este JS escuta eventos de perda de foco e retorna 'true' para o Python
            js_code = """
                (function() {
                    if (!window.focusListenerAdded) {
                        window.addEventListener('blur', () => {
                            window.parent.postMessage({ type: 'streamlit:setComponentValue', value: true }, '*');
                        });
                        window.focusListenerAdded = true;
                    }
                })();
            """
            focus_lost = st_javascript(js_code, key=f"focus_detector_{assessment['id']}")
            if focus_lost:
                st.error("⚠️ **Atenção:** Detectamos que você saiu da tela da prova. Esta ação foi registrada.")
                db.add_user_history(username, f"Perdeu o foco durante a avaliação: {assessment['title']}")

        
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

                    with st.spinner("Corrigindo e enviando sua avaliação..."):
                        # --- LÓGICA DE AUTOCORREÇÃO ---
                        objective_score = 0
                        has_subjective = False
                        total_questions = len(questions)
                        points_per_question = 10 / total_questions if total_questions > 0 else 0

                        question_map = {q['id']: q for q in questions}

                        for ans in answers:
                            if ans['type'] == 'objective':
                                question = question_map.get(ans['question_id'])
                                if question and question.get('correct_option_index') == ans.get('value'):
                                    objective_score += points_per_question
                            elif ans['type'] == 'subjective':
                                has_subjective = True
                        
                        # Se não houver subjetivas, a nota final é a nota objetiva. Senão, é nula para correção manual.
                        final_score = round(objective_score, 2) if not has_subjective else None
                        
                        success, err = db.submit_assessment(username, assessment['id'], answers, final_score)
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