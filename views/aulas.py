import streamlit as st
from services import database as db


def show_page():
    st.header("📺 Sala de Aula Virtual")

    # Gerencia a visualização entre lista e detalhe da aula
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = 'list'

    lessons = db.get_lessons()
    if not lessons:
        st.warning("Nenhuma aula cadastrada.")
        return

    # Agrupa as aulas por disciplina para exibição
    subjects = db.get_subjects()
    subject_map = {s['id']: s['name'] for s in subjects}
    
    lessons_by_subject = {}
    for lesson in lessons:
        subject_id = lesson.get('subject_id')
        if subject_id not in lessons_by_subject:
            lessons_by_subject[subject_id] = []
        lessons_by_subject[subject_id].append(lesson)

    # --- VISTA DA LISTA DE AULAS ---
    if st.session_state.view_mode == 'list':
        st.subheader("Selecione uma aula para começar")
        
        # Exibe um expander para cada disciplina que tem aulas
        for subject_id, subject_lessons in lessons_by_subject.items():
            subject_name = subject_map.get(subject_id, "Outras Aulas")
            with st.expander(f"**{subject_name}**"):
                for lesson in subject_lessons:
                    if st.button(lesson['title'], key=f"lesson_{lesson['id']}", use_container_width=True):
                        st.session_state.selected_lesson = lesson
                        st.session_state.view_mode = 'detail'
                        st.rerun()

    # --- VISTA DETALHADA DA AULA ---
    elif st.session_state.view_mode == 'detail':
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
                st.info("Esta aula não possui um quiz associado.")