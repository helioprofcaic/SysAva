import streamlit as st
from services import database as db


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

    # Conteúdo da aula
    if lesson.get('video_url'):
        st.video(lesson['video_url'])
    if lesson.get('description'):
        st.markdown(f"**Resumo da Aula:**\n{lesson['description']}")

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
                    st.session_state.selected_lesson = lesson
                    st.session_state.view_mode = 'detail'
                    st.rerun()
        
        # --- VISTA DETALHADA DA AULA ---
        else: # view_mode == 'detail'
            show_lesson_detail()

def show_admin_view():
    """Renderiza a view de admin, que mostra todas as aulas de todas as disciplinas."""
    if st.session_state.get('view_mode') == 'detail':
        show_lesson_detail()
        return

    st.subheader("Selecione uma aula para começar (Visão de Admin)")
    
    lessons = db.get_lessons()
    if not lessons:
        st.warning("Nenhuma aula cadastrada no sistema.")
        return

    subjects = db.get_subjects()
    subject_map = {s['id']: s['name'] for s in subjects}
    
    lessons_by_subject = {}
    for lesson in lessons:
        subject_id = lesson.get('subject_id')
        if subject_id not in lessons_by_subject:
            lessons_by_subject[subject_id] = []
        lessons_by_subject[subject_id].append(lesson)

    for subject_id, subject_lessons in lessons_by_subject.items():
        subject_name = subject_map.get(subject_id, "Outras Aulas")
        with st.expander(f"**{subject_name}**", expanded=True):
            for lesson in subject_lessons:
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
    is_admin = st.session_state.get('role') == 'admin'

    if not username:
        st.error("Não foi possível identificar o usuário. Por favor, faça o login novamente.")
        if st.button("Ir para Login"):
            st.session_state.page = 'login'
            st.rerun()
        return

    # Admin vê tudo, aluno vê apenas o conteúdo da sua turma
    if is_admin:
        show_admin_view()
    else:
        enrollment = db.get_user_enrollment(username)
        if not enrollment:
            st.warning("Você não está matriculado em nenhuma turma. Fale com a secretaria para regularizar seu acesso.")
            return
        
        class_id = enrollment['class_id']
        show_student_view(class_id)