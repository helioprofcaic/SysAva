import streamlit as st
from services import database as db
import streamlit.components.v1 as components
import re


def markdown_to_html(text):
    """Converte texto markdown simples para HTML para impressão."""
    if not text: return ""
    text = str(text)
    # Headers
    text = re.sub(r'^# (.*$)', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*$)', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.*$)', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    # Bold, Italic, Code
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    # Lists (simples)
    text = re.sub(r'^\s*[\*\-]\s+(.*)', r'<li>\1</li>', text, flags=re.MULTILINE)
    # Envolve listas em tags <ul>
    if '<li>' in text:
        text = f"<ul>{text}</ul>".replace('</ul><br><ul>', '')
    # Newlines para <br>
    text = text.replace('\n', '<br>')
    # Limpeza de <br> extras
    text = re.sub(r'<br>\s*(<(?:li|ul|/ul)>)', r'\1', text)
    text = re.sub(r'(<(?:/li|ul|/ul)>)\s*<br>', r'\1', text)
    return text

def generate_printable_lesson_view(school_name, subject_name, class_name, lesson, quiz, questions):
    """Gera uma visualização de impressão para uma aula e seu quiz com gabarito."""
    
    lesson_content_html = markdown_to_html(lesson.get('description', ''))
    
    # Preparar título seguro para JS
    safe_title = lesson['title'].replace('"', '\\"').replace("'", "\\'")
    
    # 1. Gera HTML das Questões
    questions_html = ""
    answers_html = ""
    
    for i, q in enumerate(questions):
        # Questões para o aluno
        options_html = ""
        options = q.get('options', [])
        for opt in options:
            options_html += f'<div style="margin: 5px 0 5px 20px;">( &nbsp; ) {opt}</div>'
        
        questions_html += f"""
        <div style="margin-bottom: 20px; page-break-inside: avoid;">
            <p><strong>{i+1}. {q['question_text']}</strong></p>
            {options_html}
        </div>
        """
        
        # Gabarito
        correct_idx = q.get('correct_option_index', 0)
        correct_letter = chr(65 + correct_idx) # A=0, B=1...
        correct_text = options[correct_idx] if 0 <= correct_idx < len(options) else "?"
        answers_html += f"<tr><td style='padding: 4px; border-bottom: 1px solid #eee;'><strong>{i+1}.</strong> {correct_letter} - {correct_text}</td></tr>"

    # 2. Monta o HTML Completo
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{lesson['title']}</title>
        <script>
            function triggerPrint() {{
                document.title = "{safe_title}";
                window.print();
            }}
        </script>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; background: white; }}
            .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }}
            .header h1 {{ margin: 0; font-size: 24px; }}
            .header p {{ margin: 5px 0; color: #666; font-size: 14px; }}
            .content {{ text-align: justify; margin-bottom: 40px; }}
            .quiz-section {{ border-top: 2px dashed #ccc; padding-top: 20px; margin-top: 30px; page-break-before: always; }}
            .answer-key {{ border-top: 2px solid #333; margin-top: 40px; padding-top: 10px; page-break-before: always; }}
            
            /* Botão de Impressão (Só aparece na tela) */
            .no-print {{ text-align: center; margin-bottom: 20px; }}
            .btn-print {{ background-color: #4CAF50; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; font-weight: bold; }}
            .btn-print:hover {{ background-color: #45a049; }}

            @media print {{
                .no-print {{ display: none !important; }}
                body {{ padding: 0; margin: 1.5cm; }}
                a {{ text-decoration: none; color: black; }}
            }}
        </style>
    </head>
    <body>
        <div class="no-print">
            <button class="btn-print" onclick="triggerPrint()">🖨️ CLIQUE AQUI PARA IMPRIMIR</button>
        </div>

        <div class="header">
            <h1>{school_name}</h1>
            <p><strong>Disciplina:</strong> {subject_name} | <strong>Turma:</strong> {class_name}</p>
            <p><strong>Conteúdo:</strong> {lesson['title']}</p>
        </div>

        <div class="content">{lesson_content_html}</div>

        <div class="quiz-section">
            <h2>📝 Exercícios de Fixação</h2>
            {questions_html}
        </div>

        <div class="answer-key">
            <h3>🔑 Gabarito Oficial</h3>
            <table style="width: 100%; font-size: 0.9em;">
                {answers_html}
            </table>
        </div>
    </body>
    </html>
    """
    return html

def show_lesson_detail():
    """Renderiza a view de detalhe de uma aula selecionada."""
    lesson = st.session_state.selected_lesson

    st.title(lesson['title'])

    if st.button("⬅️ Voltar para a lista de aulas"):
        st.session_state.view_mode = 'list'
        del st.session_state.selected_lesson
        # Limpa contextos para não interferir na próxima navegação
        if 'context_lesson_id' in st.session_state: del st.session_state.context_lesson_id
        if 'context_quiz_id' in st.session_state: del st.session_state.context_quiz_id
        st.rerun()

    st.divider()

    # Botão de Impressão para Admin/Professor
    if st.session_state.get('role') in ['admin', 'teacher']:
        # Prepara dados da aula e quiz (necessário para montar o arquivo de download)
        quiz = db.get_quiz_for_lesson(lesson['id'])
        questions = db.get_quiz_questions(quiz['id']) if quiz else []
        
        # Gera conteúdo formatado em Markdown
        md_content = f"# {lesson['title']}\n\n"
        if lesson.get('video_url'):
            md_content += f"**Vídeo:** {lesson['video_url']}\n\n"
        md_content += lesson.get('description', '') + "\n\n"
        
        if quiz and questions:
            md_content += "---\n\n"
            md_content += f"## 📝 Quiz: {quiz['title']}\n\n"
            for i, q in enumerate(questions):
                md_content += f"**{i+1}. {q['question_text']}**\n"
                for opt in q.get('options', []):
                    md_content += f"- [ ] {opt}\n"
                md_content += "\n"
            
            md_content += "---\n\n### 🔑 Gabarito\n"
            for i, q in enumerate(questions):
                correct_idx = q.get('correct_option_index', 0)
                correct_letter = chr(65 + correct_idx)
                options = q.get('options', [])
                correct_text = options[correct_idx] if 0 <= correct_idx < len(options) else "?"
                md_content += f"- **{i+1}.** {correct_letter} - {correct_text}\n"

        col_print, col_save = st.columns(2)
        
        with col_print:
            if st.button("🖨️ Imprimir Aula com Gabarito", use_container_width=True):
                if not quiz or not questions:
                    st.warning("Esta aula não tem quiz para imprimir.")
                else:
                    with st.spinner("Gerando visualização..."):
                        c_name = st.session_state.get('admin_selected_class_name', 'N/A')
                        s_name = st.session_state.get('admin_selected_subject_name', 'N/A')
                        sch_info = db.get_school()
                        sch_name = sch_info['name'] if sch_info else "Escola Técnica"
                        
                        html = generate_printable_lesson_view(sch_name, s_name, c_name, lesson, quiz, questions)
                        components.html(html, height=600, scrolling=True)
                        st.stop()
        
        with col_save:
            safe_filename = re.sub(r'[\\/*?:"<>|]', "", lesson['title']).strip().replace(" ", "_")
            st.download_button(
                label="💾 Salvar em Markdown",
                data=md_content,
                file_name=f"{safe_filename}.md",
                mime="text/markdown",
                use_container_width=True
            )
            
        st.divider()

    # Conteúdo da aula
    if lesson.get('video_url'):
        st.video(lesson['video_url'])
    if lesson.get('description'):
        st.markdown(lesson['description'], unsafe_allow_html=True)

    st.divider()
    col1, col2 = st.columns(2)

    # Botão para o Fórum
    with col1:
        if st.button("💬 Acessar Fórum da Aula", use_container_width=True):
            st.session_state.context_lesson_id = lesson['id']
            st.session_state.page = 'Fórum'
            st.rerun()

    # Botão para o Quiz
    with col2:
        quiz = db.get_quiz_for_lesson(lesson['id'])
        if quiz:
            if st.button("📝 Fazer Quiz da Aula", use_container_width=True):
                st.session_state.context_quiz_id = quiz['id']
                st.session_state.page = 'Quiz'
                st.rerun()
        else:
            st.button("📝 Sem quiz para esta aula", use_container_width=True, disabled=True)

def show_student_view(class_id):
    """Renderiza a view do aluno, com disciplinas e aulas filtradas por sua turma."""
    subjects = db.get_subjects_for_class(class_id)
    if not subjects:
        st.info("Sua turma ainda não tem disciplinas cadastradas. Fale com a secretaria.")
        return

    subject_map = {s['name']: s['id'] for s in subjects}
    subject_names = ["-- Selecione uma disciplina --"] + sorted(list(subject_map.keys()))
    
    # Usar session_state para lembrar a disciplina selecionada
    if 'selected_subject_name' not in st.session_state:
        st.session_state.selected_subject_name = subject_names[0]

    # Validação extra: se a disciplina salva não estiver na lista (ex: erro de carga), reseta
    if st.session_state.selected_subject_name not in subject_names:
        st.session_state.selected_subject_name = subject_names[0]

    selected_subject_name = st.selectbox(
        "Disciplinas da sua turma:", 
        subject_names,
        index=subject_names.index(st.session_state.selected_subject_name)
    )
    st.session_state.selected_subject_name = selected_subject_name

    # Se uma disciplina for selecionada, mostrar as aulas
    if selected_subject_name != "-- Selecione uma disciplina --":
        subject_id = subject_map[selected_subject_name]

        # Se a disciplina mudar, volta para a lista de aulas
        if 'selected_subject_id' in st.session_state and st.session_state.selected_subject_id != subject_id:
            st.session_state.view_mode = 'list'
            if 'selected_lesson' in st.session_state:
                del st.session_state.selected_lesson
        
        st.session_state.selected_subject_id = subject_id

        # --- VISTA DA LISTA DE AULAS ---
        if st.session_state.get('view_mode') == 'list':
            lessons = db.get_lessons_for_subject(subject_id)
            if not lessons:
                st.info("Esta disciplina ainda não possui aulas cadastradas.")
                return
            
            st.subheader(f"Aulas de {selected_subject_name}")
            for lesson in lessons:
                if st.button(lesson['title'], key=f"lesson_{lesson['id']}", use_container_width=True):
                    db.add_user_history(st.session_state.get('username'), f"Acessou a aula: {lesson['title']} | subject_id:{subject_id}")
                    st.session_state.selected_lesson = lesson
                    st.session_state.view_mode = 'detail'
                    st.rerun()
        
        # --- VISTA DETALHADA DA AULA ---
        else: # view_mode == 'detail'
            show_lesson_detail()

def show_admin_view():
    """Renderiza a view de admin, com seletores de turma e disciplina."""
    if st.session_state.get('view_mode') == 'detail':
        show_lesson_detail()
        return

    st.subheader("Gerenciamento de Aulas (Visão de Admin/Professor)")

    # 1. Seletor de Turma
    classes = db.get_classes()
    if not classes:
        st.warning("Nenhuma turma cadastrada no sistema. Crie uma no Painel Administrativo.")
        return
    
    class_options = {"-- Selecione uma turma --": None}
    class_options.update({c['name']: c['id'] for c in classes})
    
    # Manter seleção entre reruns
    if 'admin_selected_class_name' not in st.session_state or st.session_state.admin_selected_class_name not in class_options:
        st.session_state.admin_selected_class_name = list(class_options.keys())[0]

    selected_class_name = st.selectbox(
        "Turma:", list(class_options.keys()),
        index=list(class_options.keys()).index(st.session_state.admin_selected_class_name)
    )
    st.session_state.admin_selected_class_name = selected_class_name

    if selected_class_name != "-- Selecione uma turma --":
        class_id = class_options[selected_class_name]
        
        # 2. Seletor de Disciplina
        subjects = db.get_subjects_for_class(class_id)
        subject_options = {"-- Selecione uma disciplina --": None}
        subject_options.update({s['name']: s['id'] for s in subjects})

        if 'admin_selected_subject_name' not in st.session_state or st.session_state.admin_selected_subject_name not in subject_options:
             st.session_state.admin_selected_subject_name = list(subject_options.keys())[0]

        selected_subject_name = st.selectbox(
            "Disciplina:", list(subject_options.keys()),
            index=list(subject_options.keys()).index(st.session_state.admin_selected_subject_name)
        )
        st.session_state.admin_selected_subject_name = selected_subject_name

        if selected_subject_name != "-- Selecione uma disciplina --":
            subject_id = subject_options[selected_subject_name]
            st.divider()

            lessons = db.get_lessons_for_subject(subject_id)
            st.subheader(f"Aulas de {selected_subject_name}")
            for lesson in lessons:
                if st.button(lesson['title'], key=f"lesson_{lesson['id']}", use_container_width=True):
                    st.session_state.selected_lesson = lesson
                    st.session_state.view_mode = 'detail'
                    st.rerun()

def show_page():
    st.header("📺 Sala de Aula Virtual")

    # Gerencia a visualização entre lista e detalhe da aula
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = 'list'

    # Identifica o usuário e seu papel
    username = st.session_state.get('username')
    is_privileged = st.session_state.get('role') in ['admin', 'teacher']

    if not username:
        st.error("Não foi possível identificar o usuário. Por favor, faça o login novamente.")
        if st.button("Ir para Login"):
            st.session_state.page = 'login'
            st.rerun()
        return

    # Admin vê tudo, aluno vê apenas o conteúdo da sua turma
    if is_privileged:
        show_admin_view()
    else:
        enrollment = db.get_user_enrollment(username)
        if not enrollment:
            st.warning("Você não está matriculado em nenhuma turma. Fale com a secretaria para regularizar seu acesso.")
            return
        
        class_id = enrollment['class_id']
        show_student_view(class_id)