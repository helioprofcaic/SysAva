import streamlit as st
from services import database as db
import streamlit.components.v1 as components
import re


def clean_svg_content(text):
    """Limpa e restaura o código SVG que pode ter sido corrompido pela IA ou markdown e remove invólucros globais de código."""
    if not text: return ""
    text = str(text).strip()

    # 1. Remove invólucros globais de bloco de código markdown (```markdown ... ```) produzidos pela IA
    if text.startswith('```'):
        m = re.match(r'^```(?:markdown|md)?\s*\n(.*?)\n```\s*$', text, flags=re.DOTALL | re.IGNORECASE)
        if m:
            text = m.group(1).strip()
        else:
            text = re.sub(r'^```(?:markdown|md)?\s*\n?', '', text, flags=re.IGNORECASE)
            text = re.sub(r'\n?```\s*$', '', text)

    # 2. Converte tags de imagem Markdown (![alt](path)) em SVGs autocontidos com base64
    if "![" in text:
        try:
            from services.pdf_extractor import convert_markdown_images_to_svg
            text = convert_markdown_images_to_svg(text)
        except Exception:
            pass

    # 3. Converte entidades escapadas (inclusive aspas e caracteres que quebram o XML)
    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#x27;', "'").replace('&nbsp;', ' ')
    
    # 4. Corrige a linkificação de namespaces (IA transforma URLs em links markdown dentro de atributos)
    text = re.sub(r'xmlns\s*=\s*["\']?\[(http.*?)\]\(.*?\)\s*["\']?', r'xmlns="\1"', text, flags=re.IGNORECASE)
    text = re.sub(r'xmlns\s*=\s*"(http.*?)"', r'xmlns="\1"', text, flags=re.IGNORECASE)

    # 5. Remove blocos de código markdown residuais que envolvem o SVG (```xml ... ```)
    text = re.sub(r'```(?:html|xml|svg)?\s*(<svg.*?</svg>)\s*```', r'\1', text, flags=re.DOTALL | re.IGNORECASE)

    # 6. Remove repetições acidentais de cabeçalho como "Escola: Escola:"
    text = re.sub(r'(\*\*🏫\s*Escola:\*\*\s*)(?:(?:Escola|Institui[cç][aã]o)\s*:\s*)+', r'\1', text, flags=re.IGNORECASE)

    # 7. CONVERSÃO DE SVG COM IMAGEM BASE64 PARA TAG HTML <img /> (Resolve sanitização do Streamlit)
    def svg_to_img_repl(match):
        svg_block = match.group(0)
        
        # Extrai a URL do base64 (href ou src da tag <image>)
        img_match = re.search(r'<image\s+[^>]*?href=["\'](data:image/.*?;base64,.*?)["\']', svg_block, flags=re.DOTALL | re.IGNORECASE)
        if not img_match:
            img_match = re.search(r'<image\s+[^>]*?src=["\'](data:image/.*?;base64,.*?)["\']', svg_block, flags=re.DOTALL | re.IGNORECASE)
            
        if img_match:
            base64_src = img_match.group(1).strip()
            # Remove quebras de linha/espaços em branco residuais no base64
            base64_src = re.sub(r'\s+', '', base64_src)
            
            # Extrai atributos de estilo, largura e altura do <svg>
            style_match = re.search(r'<svg\s+[^>]*?style=["\'](.*?)["\']', svg_block, flags=re.DOTALL | re.IGNORECASE)
            width_match = re.search(r'<svg\s+[^>]*?width=["\'](.*?)["\']', svg_block, flags=re.DOTALL | re.IGNORECASE)
            height_match = re.search(r'<svg\s+[^>]*?height=["\'](.*?)["\']', svg_block, flags=re.DOTALL | re.IGNORECASE)
            
            style_str = style_match.group(1) if style_match else "max-width: 100%; height: auto; border-radius: 8px;"
            width_str = width_match.group(1) if width_match else ""
            height_str = height_match.group(1) if height_match else ""
            
            # Reconstrói como tag <img /> HTML compatível
            attrs = []
            if width_str: attrs.append(f'width="{width_str}"')
            if height_str: attrs.append(f'height="{height_str}"')
            if style_str: attrs.append(f'style="{style_str}"')
            
            return f'<img src="{base64_src}" {" ".join(attrs)} />'
            
        return svg_block

    # Substitui tags <svg>...</svg> contendo imagens base64 por tags <img> normais
    text = re.sub(r'<svg\b[^>]*?>.*?</svg>', svg_to_img_repl, text, flags=re.DOTALL | re.IGNORECASE)
    
    return text.strip()

def markdown_to_html(text):
    """Converte texto markdown simples para HTML para impressão."""
    text = clean_svg_content(text)

    # 1. Protege blocos SVG: extrai e substitui por um placeholder 
    # para evitar que os replaces de newline e markdown quebrem o XML do SVG.
    svg_blocks = re.findall(r'<svg.*?</svg>', text, flags=re.DOTALL | re.IGNORECASE)
    for i, svg in enumerate(svg_blocks):
        text = text.replace(svg, f"<!--SVG_BLOCK_{i}-->")

    # Escapa tags HTML soltas (como <section>, <nav>, <div>, etc.) para não quebrarem o layout
    text = re.sub(r'<(/?[a-zA-Z][a-zA-Z0-9_\-]*(\s+[^>]*)?)>', r'&lt;\1&gt;', text)

    # Markdown Images: ![alt](src)
    text = re.sub(
        r'!\[(.*?)\]\((.*?)\)',
        r'<div style="text-align: center; margin: 15px 0;"><img src="\2" alt="\1" style="max-width: 85%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);"><p style="font-size: 0.85em; color: #666; margin-top: 4px;"><em>\1</em></p></div>',
        text
    )

    # Headers
    text = re.sub(r'^# (.*$)', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*$)', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.*$)', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    # Bold, Italic, Code
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    # Lists (simples)
    text = re.sub(r'^\s*[\*\-]\s+(.*)', r'<li>\1</li>', text, flags=re.M)
    # Envolve listas em tags <ul>
    if '<li>' in text:
        text = f"<ul>{text}</ul>".replace('</ul><br><ul>', '')
    # Newlines para <br>
    text = text.replace('\n', '<br>')
    text = re.sub(r'<br>\s*(<(?:li|ul|/ul)>)', r'\1', text)
    text = re.sub(r'(<(?:/li|ul|/ul)>)\s*<br>', r'\1', text)
    
    # 2. Restaura os blocos SVG originais sem as tags <br> extras
    for i, svg in enumerate(svg_blocks):
        text = text.replace(f"<!--SVG_BLOCK_{i}-->", svg)
        
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
            options_html += f'<div style="margin: 5px 0 5px 20px;">( &nbsp; ) {markdown_to_html(opt)}</div>'
        
        questions_html += f"""
        <div style="margin-bottom: 20px; page-break-inside: avoid;">
            <p><strong>{i+1}. {markdown_to_html(q['question_text'])}</strong></p>
            {options_html}
        </div>
        """
        
        # Gabarito
        correct_idx = q.get('correct_option_index', 0)
        correct_letter = chr(65 + correct_idx) # A=0, B=1...
        correct_text = options[correct_idx] if 0 <= correct_idx < len(options) else "?"
        answers_html += f"<tr><td style='padding: 4px; border-bottom: 1px solid #eee;'><strong>{i+1}.</strong> {correct_letter} - {markdown_to_html(correct_text)}</td></tr>"

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
    selected = st.session_state.selected_lesson
    # A listagem leve não traz o conteúdo; busca os campos completos apenas ao abrir a aula.
    lesson = db.get_lesson_by_id(selected['id']) or selected

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
            if st.button("🖨️ Imprimir Aula com Gabarito", width="stretch"):
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
                width="stretch"
            )
            
        st.divider()

    # Conteúdo da aula
    if lesson.get('video_url'):
        st.video(lesson['video_url'])
    if lesson.get('description'):
        desc = clean_svg_content(lesson['description'])
        
        st.markdown(desc, unsafe_allow_html=True)

    st.divider()
    col1, col2 = st.columns(2)

    # Botão para o Fórum
    with col1:
        if st.button("💬 Acessar Fórum da Aula", width="stretch"):
            st.session_state.context_lesson_id = lesson['id']
            st.session_state.page = 'Fórum'
            st.rerun()

    # Botão para o Quiz
    with col2:
        quiz = db.get_quiz_for_lesson(lesson['id'])
        if quiz:
            if st.button("📝 Fazer Quiz da Aula", width="stretch"):
                st.session_state.context_quiz_id = quiz['id']
                st.session_state.page = 'Quiz'
                st.rerun()
        else:
            st.button("📝 Sem quiz para esta aula", width="stretch", disabled=True)

def show_student_view(class_id):
    """Renderiza a view do aluno, com disciplinas e aulas filtradas por sua turma."""
    subjects = db.get_subjects_for_class(class_id)
    # Filtra apenas as disciplinas marcadas como ativas para reduzir a carga visual do aluno
    subjects = [s for s in subjects if s.get('is_active', True)]

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

        # --- SCORE DO ALUNO NESTA DISCIPLINA ---
        username = st.session_state.get('username')
        score = db.get_student_score(username, filter_subject_id=subject_id)
        with st.container():
            sc1, sc2, sc3, sc4 = st.columns(4)
            sc1.metric("🏆 Score", score['total'])
            sc2.metric("📺 Aulas", score['lesson'])
            sc3.metric("📝 Quizzes", score['quiz'])
            sc4.metric("💬 Fórum", score['forum'])

        st.divider()

        # --- VISTA DA LISTA DE AULAS ---
        if st.session_state.get('view_mode') == 'list':
            show_lesson_list(subject_id, selected_subject_name)
        
        # --- VISTA DETALHADA DA AULA ---
        else: # view_mode == 'detail'
            show_lesson_detail()


def get_lesson_number(title):
    """Extrai o número da aula do título."""
    match = re.search(r'Aula\s*(\d+)', title, re.IGNORECASE)
    return int(match.group(1)) if match else None

def group_lessons(lessons, subject_name, class_name, subject_id=None):
    """
    Agrupa as aulas por semana, unidade ou anual de forma agnóstica,
    lendo as configurações diretamente dos metadados da disciplina no banco de dados.
    """
    subj_data = db.get_subject_by_id(subject_id) if subject_id else None

    # 1. Tipo de agrupamento ('anual', 'semana', 'unidade', 'modulo', 'livre')
    group_type = 'semana'
    if subj_data and subj_data.get('group_type'):
        group_type = str(subj_data['group_type']).lower()
    else:
        # Fallback suave por nome
        safe_subject_name = (subject_name or "").upper()
        if any(exc in safe_subject_name for exc in ["MENTORIA", "PCII", "PROJETO DE VIDA"]):
            group_type = 'anual'

    if group_type == 'anual':
        return {"Anual": lessons}
    elif group_type == 'livre':
        return {"Aulas": lessons}

    # 2. Aulas por grupo / semana (lessons_per_week ou inferido de max_hours)
    group_size = None
    if subj_data:
        if subj_data.get('lessons_per_week'):
            group_size = int(subj_data['lessons_per_week'])
        elif subj_data.get('max_hours'):
            max_h = int(subj_data['max_hours'])
            group_size = 10 if max_h >= 80 else 8
        elif subj_data.get('duration_type') == 'mensal':
            group_size = 8

    if not group_size:
        safe_class_name = (class_name or "").upper()
        safe_subject_name = (subject_name or "").upper()
        modular_keywords = [
            "UI", "UX", "IHC", "INTELIGÊNCIA ARTIFICIAL", "INTELIGENCIA ARTIFICIAL",
            "ROBÓTICA", "ROBOTICA", "MICROSSERVIÇOS", "MICROSSERVICOS", 
            "ORIENTAÇÃO PROFISSIONAL", "ORIENTACAO PROFISSIONAL", "EMPREENDEDORISMO",
            "ATIVIDADES INTEGRADORAS"
        ]
        if any(kw in safe_subject_name for kw in modular_keywords):
            group_size = 8
        elif "DS" in safe_class_name or "DESENVOLVIMENTO DE SISTEMAS" in safe_class_name:
            group_size = 10
        else:
            group_size = 8

    # Prefixo de exibição ('Semana', 'Unidade', 'Módulo', etc.)
    if group_type == 'unidade':
        group_prefix = "Unidade"
    elif group_type == 'modulo':
        group_prefix = "Módulo"
    else:
        group_prefix = "Semana"

    # Adiciona número da aula para ordenação
    for lesson in lessons:
        lesson['number'] = get_lesson_number(lesson['title'])

    # Filtra aulas sem número e ordena
    numbered_lessons = sorted([l for l in lessons if l['number'] is not None], key=lambda x: x['number'])

    grouped = {}
    for lesson in numbered_lessons:
        group_index = (lesson['number'] - 1) // group_size + 1
        start_lesson = (group_index - 1) * group_size + 1
        end_lesson = start_lesson + group_size - 1

        group_key = f"{group_prefix} {group_index:02d} (Aulas {start_lesson:02d}-{end_lesson:02d})"
        
        if group_key not in grouped:
            grouped[group_key] = []
        grouped[group_key].append(lesson)

    return grouped

def show_lesson_list(subject_id, subject_name):
    """Exibe a lista de aulas, possivelmente agrupada."""
    lessons = db.get_lessons_for_subject(subject_id)
    if not lessons:
        st.info("Esta disciplina ainda não possui aulas cadastradas.")
        return

    # Carrega dados para os indicadores de status
    username = st.session_state.get('username')
    history = db.get_user_history(username)
    quizzes = db.get_quizzes_for_subject(subject_id)
    quiz_map = {q['lesson_id']: q for q in quizzes}
    
    visited_lesson_titles = set()
    completed_quiz_titles = set()
    completed_quiz_ids = set()
    
    for h in history:
        act = h.get('activity', '')
        if "Acessou a aula:" in act:
            title = act.split(':', 1)[1].split('|')[0].strip()
            visited_lesson_titles.add(title)
        elif "Concluiu Quiz:" in act:
            match_qid = re.search(r'\| quiz_id:(\d+)', act)
            if match_qid:
                completed_quiz_ids.add(int(match_qid.group(1)))
            else:
                raw_title = act.split(':', 1)[1].split('|')[0].strip()
                title = re.sub(r'\s*\(\d+/\d+\)$', '', raw_title).strip()
                # Títulos genéricos não identificam a aula: ignorados para evitar falsos positivos
                if not db.is_generic_quiz_title(title):
                    completed_quiz_titles.add(title)

    st.subheader(f"Aulas de {subject_name}")

    # Lógica de agrupamento
    enrollment = db.get_user_enrollment(username)
    
    # Temporarily define the missing function here. 
    # TODO: Move this function to the services/database.py module.
    def get_class_by_id(class_id):
        classes = db.get_classes()
        return next((c for c in classes if c['id'] == class_id), None)

    class_info = get_class_by_id(enrollment['class_id']) if enrollment else {}
    class_name = class_info.get('name', '')

    grouped_lessons = group_lessons(lessons, subject_name, class_name, subject_id=subject_id)

    for group_title, lessons_in_group in grouped_lessons.items():
        # Se houver apenas um grupo chamado "Aulas", não usa o expander
        if len(grouped_lessons) == 1 and group_title == "Aulas":
            render_lessons(lessons_in_group, visited_lesson_titles, completed_quiz_titles, completed_quiz_ids, quiz_map, subject_id)
        else:
            with st.expander(f"**{group_title}**", expanded=True):
                render_lessons(lessons_in_group, visited_lesson_titles, completed_quiz_titles, completed_quiz_ids, quiz_map, subject_id)

def render_lessons(lessons, visited_lesson_titles, completed_quiz_titles, completed_quiz_ids, quiz_map, subject_id):
    """Função auxiliar para renderizar uma lista de botões de aula."""
    for lesson in lessons:
        is_visited = lesson['title'] in visited_lesson_titles
        has_quiz = lesson['id'] in quiz_map
        is_concluded = False
        
        if is_visited:
            if not has_quiz:
                is_concluded = True
            else:
                quiz = quiz_map.get(lesson['id'])
                if quiz and (quiz['id'] in completed_quiz_ids or quiz['title'] in completed_quiz_titles):
                    is_concluded = True
        
        if is_concluded:
            status_class = "circle-green"
            tooltip = "Concluída"
        elif is_visited:
            status_class = "circle-orange"
            tooltip = "Visitada (Quiz pendente)"
        else:
            status_class = "circle-gray"
            tooltip = "Não visitada"

        col_btn, col_status = st.columns([0.92, 0.08])
        with col_btn:
            if st.button(lesson['title'], key=f"lesson_{lesson['id']}", width="stretch"):
                db.add_user_history(st.session_state.get('username'), f"Acessou a aula: {lesson['title']} | subject_id:{subject_id}")
                st.session_state.selected_lesson = lesson
                st.session_state.view_mode = 'detail'
                st.rerun()
        with col_status:
            st.markdown(f'<div class="circle {status_class}" title="{tooltip}"></div>', unsafe_allow_html=True)


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
        # Também filtra para o professor/admin para manter a consistência visual no seletor
        subjects = [s for s in subjects if s.get('is_active', True)]

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
            grouped_lessons = group_lessons(lessons, selected_subject_name, selected_class_name, subject_id=subject_id)
            for group_title, lessons_in_group in grouped_lessons.items():
                with st.expander(f"**{group_title}**", expanded=True):
                    for lesson in lessons_in_group:
                        if st.button(lesson['title'], key=f"admin_lesson_{lesson['id']}", width="stretch"):
                            st.session_state.selected_lesson = lesson
                            st.session_state.view_mode = 'detail'
                            st.rerun()

def show_page():
    st.header("📺 Sala de Aula Virtual")
    st.markdown("""<style>.circle {height: 12px;width: 12px;border-radius: 50%;display: inline-block;margin-top: 12px;border: 1px solid rgba(0,0,0,0.2);}.circle-green { background-color: #28a745; box-shadow: 0 0 5px #28a745; }.circle-orange { background-color: #fd7e14; box-shadow: 0 0 5px #fd7e14; }.circle-gray { background-color: #6c757d; }</style>""", unsafe_allow_html=True)
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