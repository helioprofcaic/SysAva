import streamlit as st
from services import database as db
import json

def show_page():
    st.header("🛡️ Painel Administrativo")

    if not db.is_db_connected():
        st.warning("Funcionalidade disponível apenas com banco de dados conectado.")
        return

    tab1, tab2, tab3 = st.tabs(["Gerenciar Usuários", "Gerenciar Aulas", "Gerenciar Quizzes"])

    with tab1:
        st.subheader("Usuários Cadastrados")
        users = db.get_all_users()
        if users:
            st.dataframe(users, use_container_width=True)

    with tab2:
        st.subheader("Aulas")
        with st.expander("Adicionar Nova Aula", expanded=False):
            with st.form("new_lesson_form", clear_on_submit=True):
                title = st.text_input("Título da Aula")
                description = st.text_area("Descrição")
                video_url = st.text_input("URL do Vídeo (YouTube)")
                submitted = st.form_submit_button("Salvar Aula")
                if submitted and title:
                    _, error = db.create_lesson(title, description, video_url)
                    if error:
                        st.error(f"Erro ao criar aula: {error}")
                    else:
                        st.success("Aula criada com sucesso!")
        
        st.write("Aulas existentes:")
        lessons = db.get_lessons()
        st.dataframe(lessons, use_container_width=True)

    with tab3:
        st.subheader("Quizzes e Questões")
        lessons = db.get_lessons()
        if not lessons:
            st.warning("Cadastre uma aula primeiro para poder criar um quiz.")
            return

        with st.expander("Adicionar Novo Quiz a uma Aula", expanded=False):
            with st.form("new_quiz_form", clear_on_submit=True):
                lesson_map = {lesson['title']: lesson['id'] for lesson in lessons}
                selected_lesson_title = st.selectbox("Selecione a Aula", options=lesson_map.keys())
                quiz_title = st.text_input("Título do Quiz")
                submitted = st.form_submit_button("Salvar Quiz")
                if submitted and quiz_title and selected_lesson_title:
                    lesson_id = lesson_map[selected_lesson_title]
                    _, error = db.create_quiz(lesson_id, quiz_title)
                    if error:
                        st.error(f"Erro ao criar quiz: {error}")
                    else:
                        st.success(f"Quiz '{quiz_title}' criado para a aula '{selected_lesson_title}'!")

        st.divider()

        with st.expander("Adicionar Questão a um Quiz Existente", expanded=False):
            quizzes = [q for lesson in lessons if (q := db.get_quiz_for_lesson(lesson['id']))]
            if not quizzes:
                st.warning("Nenhum quiz cadastrado. Crie um quiz primeiro.")
            else:
                with st.form("new_question_form", clear_on_submit=True):
                    quiz_map = {quiz['title']: quiz['id'] for quiz in quizzes}
                    selected_quiz_title = st.selectbox("Selecione o Quiz", options=quiz_map.keys())
                    question_text = st.text_input("Texto da Questão")
                    options_str = st.text_input('Opções (separadas por vírgula)', help='Ex: Opção A, Opção B, Opção C')
                    correct_option_index = st.number_input("Índice da Opção Correta (começando em 0)", min_value=0, step=1)
                    submitted = st.form_submit_button("Salvar Questão")
                    if submitted and question_text and options_str:
                        quiz_id = quiz_map[selected_quiz_title]
                        options = [opt.strip() for opt in options_str.split(',')]
                        _, error = db.create_quiz_question(quiz_id, question_text, options, correct_option_index)
                        if error:
                            st.error(f"Erro ao criar questão: {error}")
                        else:
                            st.success("Questão adicionada com sucesso!")