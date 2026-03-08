import streamlit as st
from services import database as db
from services import auth
import json

def show_page():
    st.header("🛡️ Painel Administrativo")

    if not db.is_db_connected():
        st.warning("Funcionalidade disponível apenas com banco de dados conectado.")
        return

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Gerenciar Usuários", "Gerenciar Aulas", "Gerenciar Quizzes", "Gerenciar Avaliações", "🤖 Simulador"])

    with tab1:
        with st.expander("➕ Cadastrar Novo Usuário", expanded=False):
            with st.form("register_user_form", clear_on_submit=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    new_name = st.text_input("Nome Completo")
                    new_user = st.text_input("Usuário (Login)")
                    new_ra = st.text_input("RA (Registro Acadêmico)")
                with col_b:
                    new_pass = st.text_input("Senha", type="password")
                    new_role = st.selectbox("Função", ["student", "admin"], format_func=lambda x: "Aluno" if x == "student" else "Administrador")
                
                if st.form_submit_button("Cadastrar"):
                    if new_name and new_user and new_pass and new_ra:
                        hashed = auth.hash_password(new_pass)
                        _, error = db.create_user(new_user, hashed, new_name, new_ra, new_role)
                        if error:
                            st.error(f"Erro: {error}")
                        else:
                            st.success("Usuário cadastrado com sucesso!")
                            st.rerun()
                    else:
                        st.warning("Preencha todos os campos.")

        st.subheader("Usuários Cadastrados")
        users = db.get_all_users()
        if users:
            # Cabeçalho da tabela customizada
            col_h1, col_h2, col_h3, col_h4 = st.columns([0.3, 0.3, 0.2, 0.2])
            col_h1.markdown("**Nome**")
            col_h2.markdown("**Usuário**")
            col_h3.markdown("**Função**")
            col_h4.markdown("**Ação**")
            st.divider()

            for u in users:
                c1, c2, c3, c4 = st.columns([0.3, 0.3, 0.2, 0.2])
                c1.write(u['name'])
                c2.write(u['username'])
                c3.write("Admin" if u['role'] == 'admin' else "Aluno")
                
                # Impede que o usuário exclua a si mesmo
                if u['username'] != st.session_state.get('username'):
                    if c4.button("🗑️ Excluir", key=f"del_user_{u['username']}"):
                        _, err = db.delete_user(u['username'])
                        if err:
                            st.error(f"Erro: {err}")
                        else:
                            st.success(f"Usuário {u['username']} removido.")
                            st.rerun()
                else:
                    c4.caption("Atual")
                st.divider()

    with tab2:
        st.subheader("Aulas")
        
        # Seletor de Turma
        classes = db.get_classes()
        class_options = {c['name']: c['id'] for c in classes}
        selected_class_name = st.selectbox("Selecione a Turma", options=["-- Selecione --"] + list(class_options.keys()))

        if selected_class_name != "-- Selecione --":
            class_id = class_options[selected_class_name]
            
            # Seletor de Disciplina (baseado na turma)
            subjects = db.get_subjects_for_class(class_id)
            subject_options = {s['name']: s['id'] for s in subjects}
            
            if not subjects:
                st.warning("Esta turma não possui disciplinas vinculadas.")
            else:
                selected_subject_name = st.selectbox("Selecione a Disciplina", options=list(subject_options.keys()))
                subject_id = subject_options[selected_subject_name]

                st.divider()
                
                # Formulário de Criação (Agora vinculado à disciplina selecionada)
                with st.expander(f"Adicionar Nova Aula em {selected_subject_name}", expanded=False):
                    with st.form("new_lesson_form", clear_on_submit=True):
                        title = st.text_input("Título da Aula")
                        description = st.text_area("Descrição")
                        video_url = st.text_input("URL do Vídeo (YouTube)")
                        submitted = st.form_submit_button("Salvar Aula")
                        
                        if submitted and title:
                            _, error = db.create_lesson(title, subject_id, description, video_url)
                            if error:
                                st.error(f"Erro ao criar aula: {error}")
                            else:
                                st.success(f"Aula criada com sucesso na disciplina {selected_subject_name}!")
                                st.rerun()
                
                st.write(f"Aulas de **{selected_subject_name}** ({selected_class_name}):")
                lessons = db.get_lessons_for_subject(subject_id)
                st.dataframe(lessons, use_container_width=True, column_config={"id": "ID", "title": "Título", "video_url": "Link", "created_at": "Criado em"})

    with tab3:
        st.subheader("Gerenciar Quizzes")
        lessons = db.get_lessons()
        if not lessons:
            st.warning("Cadastre uma aula primeiro para poder criar um quiz.")
            return

        # Mapeamento de aulas para seleção
        lesson_map = {lesson['title']: lesson['id'] for lesson in lessons}
        selected_lesson_title = st.selectbox("Selecione a Aula", options=["-- Selecione --"] + list(lesson_map.keys()))

        if selected_lesson_title != "-- Selecione --":
            lesson_id = lesson_map[selected_lesson_title]
            
            # Verifica se já existe quiz para esta aula
            quiz = db.get_quiz_for_lesson(lesson_id)
            
            if not quiz:
                st.info("Nenhum quiz encontrado para esta aula.")
                with st.form("create_quiz_form"):
                    st.write("Criar Novo Quiz")
                    quiz_title = st.text_input("Título do Quiz")
                    submitted = st.form_submit_button("Criar Quiz")
                    if submitted and quiz_title:
                        _, error = db.create_quiz(lesson_id, quiz_title)
                        if error:
                            st.error(f"Erro ao criar quiz: {error}")
                        else:
                            st.success("Quiz criado com sucesso! Agora você pode adicionar questões.")
                            st.rerun()
            else:
                st.markdown(f"### Editando Quiz: {quiz['title']}")
                
                # Exibir questões existentes
                questions = db.get_quiz_questions(quiz['id'])
                if questions:
                    with st.expander(f"Ver {len(questions)} questões cadastradas", expanded=False):
                        for i, q in enumerate(questions):
                            st.markdown(f"**{i+1}. {q['question_text']}**")
                            st.caption(f"Opções: {', '.join(q['options'])} | Correta: {q['options'][q['correct_option_index']]}")
                            st.divider()
                
                st.markdown("#### Adicionar Nova Questão")
                with st.form("add_question_form", clear_on_submit=True):
                    question_text = st.text_input("Enunciado da Questão")
                    options_str = st.text_area("Opções (separadas por vírgula)", help="Ex: Azul, Vermelho, Verde")
                    correct_option_index = st.number_input("Índice da Opção Correta (0 = 1ª opção)", min_value=0, step=1)
                    
                    submitted = st.form_submit_button("Adicionar Questão")
                    
                    if submitted and question_text and options_str:
                        options = [opt.strip() for opt in options_str.split(',') if opt.strip()]
                        if len(options) < 2:
                            st.error("Adicione pelo menos 2 opções.")
                        elif correct_option_index >= len(options):
                            st.error(f"Índice inválido. Máximo: {len(options)-1}")
                        else:
                            _, error = db.create_quiz_question(quiz['id'], question_text, options, correct_option_index)
                            if error:
                                st.error(f"Erro ao adicionar questão: {error}")
                            else:
                                st.success("Questão adicionada com sucesso!")
                                st.rerun()

    with tab4:
        st.subheader("Gerenciar Avaliações (Provas)")
        
        # --- Seletor de Contexto (Igual ao de Aulas) ---
        classes = db.get_classes()
        class_options = {c['name']: c['id'] for c in classes}
        selected_class_name_av = st.selectbox("Selecione a Turma", options=["-- Selecione --"] + list(class_options.keys()), key="sel_class_av")

        if selected_class_name_av != "-- Selecione --":
            class_id_av = class_options[selected_class_name_av]
            subjects = db.get_subjects_for_class(class_id_av)
            subject_options = {s['name']: s['id'] for s in subjects}
            
            if not subjects:
                st.warning("Turma sem disciplinas.")
            else:
                selected_subject_name_av = st.selectbox("Selecione a Disciplina", options=["-- Selecione --"] + list(subject_options.keys()), key="sel_subj_av")
                
                if selected_subject_name_av != "-- Selecione --":
                    subject_id_av = subject_options[selected_subject_name_av]
                    
                    st.divider()
                    
                    # --- Listagem e Criação de Avaliações ---
                    assessments = db.get_assessments_by_subject(subject_id_av)
                    
                    col_list, col_create = st.columns([0.6, 0.4])
                    
                    with col_create:
                        st.markdown("#### Nova Avaliação")
                        with st.form("create_assessment_form"):
                            av_type = st.selectbox("Tipo", ["MN1", "MN2", "MN3", "RM"])
                            av_title = st.text_input("Título (ex: Prova de Python Básico)")
                            if st.form_submit_button("Criar Avaliação"):
                                # Verifica se já existe esse tipo para a disciplina (opcional, mas recomendado)
                                existing = [a for a in assessments if a['type'] == av_type]
                                if existing:
                                    st.warning(f"Já existe uma avaliação {av_type} para esta disciplina.")
                                else:
                                    _, err = db.create_assessment(subject_id_av, av_type, av_title)
                                    if err: st.error(err)
                                    else: st.rerun()

                    with col_list:
                        st.markdown("#### Avaliações Existentes")
                        if not assessments:
                            st.info("Nenhuma avaliação criada.")
                        
                        # Seletor para editar uma avaliação específica
                        assessment_map = {f"{a['type']} - {a['title']}": a for a in assessments}
                        selected_assessment_key = st.selectbox("Selecione para editar questões:", options=["-- Selecione --"] + list(assessment_map.keys()))

                    # --- Gerenciamento de Questões da Avaliação Selecionada ---
                    if selected_assessment_key != "-- Selecione --":
                        assessment = assessment_map[selected_assessment_key]
                        st.divider()
                        st.markdown(f"### Editando: {assessment['title']} ({assessment['type']})")
                        
                        # Lista questões atuais
                        questions = db.get_assessment_questions(assessment['id'])
                        st.write(f"Questões cadastradas: {len(questions)}/10")
                        for i, q in enumerate(questions):
                            tipo_icon = "📝" if q.get('question_type') == 'subjective' else "🔘"
                            st.text(f"{i+1}. {tipo_icon} {q['question_text']}")
                            if q.get('question_type') == 'subjective' and q.get('options') and "LINK_REQUIRED" in q['options']:
                                st.caption("   ↳ 🔗 Solicita link externo (GitHub/Drive)")

                        st.divider()
                        
                        # --- Importação de Questões de Quizzes ---
                        with st.expander("📂 Importar do Banco de Questões (Quizzes)", expanded=False):
                            st.caption("Abaixo estão listadas todas as questões cadastradas nos Quizzes das aulas desta disciplina.")
                            quiz_questions = db.get_all_quiz_questions_for_subject(subject_id_av)
                            
                            if not quiz_questions:
                                st.info("Nenhuma questão encontrada nos quizzes desta disciplina.")
                            else:
                                for q in quiz_questions:
                                    col_q, col_btn = st.columns([0.8, 0.2])
                                    with col_q:
                                        st.markdown(f"**{q['question_text']}**")
                                        # Mostra opções de forma compacta se existirem
                                        opts = q.get('options', [])
                                        if isinstance(opts, list):
                                            st.caption(f"Opções: {', '.join(map(str, opts))}")
                                    with col_btn:
                                        if st.button("Importar", key=f"imp_q_{q['id']}"):
                                            # Importa como questão objetiva
                                            _, err = db.create_assessment_question(
                                                assessment['id'],
                                                q['question_text'],
                                                'objective',
                                                q.get('options', []),
                                                q.get('correct_option_index', 0)
                                            )
                                            if err: st.error("Erro ao importar.")
                                            else: st.rerun()
                                    st.divider()

                        st.markdown("#### Adicionar Questão")
                        with st.form("add_assessment_question"):
                            q_type = st.radio("Tipo da Questão", ["Objetiva", "Subjetiva"], horizontal=True)
                            q_text = st.text_area("Enunciado da Questão")
                            
                            options = []
                            correct_idx = 0
                            
                            if q_type == "Objetiva":
                                opts_str = st.text_input("Opções (separadas por vírgula)", help="Ex: A, B, C, D")
                                correct_idx = st.number_input("Índice da Correta (0 = 1ª opção)", min_value=0, step=1)
                                if opts_str:
                                    options = [o.strip() for o in opts_str.split(',') if o.strip()]
                            else:
                                st.info("ℹ️ O aluno terá um campo de texto para a resposta.")
                                require_link = st.checkbox("Adicionar campo para envio de Link (GitHub/Drive)?", value=True)
                                options = ["LINK_REQUIRED"] if require_link else []
                                correct_idx = 0 # Padrão 0 conforme solicitado

                            if st.form_submit_button("Salvar Questão"):
                                type_db = 'subjective' if q_type == "Subjetiva" else 'objective'
                                _, err = db.create_assessment_question(assessment['id'], q_text, type_db, options, correct_idx)
                                if err: st.error(err)
                                else: 
                                    st.success("Questão adicionada!")
                                    st.rerun()

    with tab5:
        st.subheader("🤖 Simulador de Atividades de Aluno")
        st.info("Esta ferramenta preenche o histórico de um aluno com todas as aulas e quizzes para fins de teste. A ação de 'Zerar' apaga permanentemente o histórico e as provas realizadas pelo aluno.")

        users = db.get_all_users()
        students = {u['username']: u['name'] for u in users if u['role'] == 'student'}
        
        if not students:
            st.warning("Nenhum aluno cadastrado para simular.")
        else:
            selected_student_username = st.selectbox(
                "Selecione o Aluno (por login/RA) para gerenciar:", 
                options=list(students.keys()),
                format_func=lambda username: f"{students[username]} ({username})"
            )

            if selected_student_username:
                st.markdown("---")
                st.markdown(f"#### Progresso Atual de **{students[selected_student_username]}**")
                
                progress = db.get_user_progress_stats(selected_student_username)
                col1, col2, col3 = st.columns(3)
                col1.metric("Aulas Vistas", progress.get('lessons', 0))
                col2.metric("Quizzes Feitos", progress.get('quizzes', 0))
                col3.metric("Posts no Fórum", progress.get('forum', 0))

                st.markdown("---")

                col_sim, col_reset = st.columns(2)

                with col_sim:
                    st.markdown("#### ✅ Simular Conclusão Total")
                    if st.button("🚀 Simular Todas as Atividades"):
                        with st.spinner("Simulando..."):
                            _, err = db.simulate_student_activities(selected_student_username)
                            if err: st.error(f"Erro na simulação: {err}")
                            else: st.rerun()
                
                with col_reset:
                    st.markdown("#### ⚠️ Zerar Dados do Aluno")
                    st.warning("Apaga histórico e provas. Use para liberar o RA para um aluno real.")
                    
                    confirm_reset = st.checkbox(f"Confirmo que desejo zerar todos os dados de {students[selected_student_username]}")

                    if st.button("🗑️ Zerar Dados Agora", disabled=not confirm_reset):
                        with st.spinner("Apagando dados..."):
                            _, err = db.reset_student_data(selected_student_username)
                            if err: st.error(f"Erro ao zerar dados: {err}")
                            else: st.rerun()