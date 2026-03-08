import streamlit as st
from services import database as db
from services import auth
from services import ai_generation as ai
import re
import json
import pandas as pd
import time

def show_page():
    st.header("🛡️ Painel Administrativo")

    if not db.is_db_connected():
        st.warning("Funcionalidade disponível apenas com banco de dados conectado.")
        return

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Gerenciar Usuários", "Gerenciar Aulas", "Gerenciar Quizzes", "Gerenciar Avaliações", "🤖 Simulador", "📊 Relatórios", "🤖 Gerador de Aulas"])

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
                    new_role = st.selectbox("Função", ["student", "teacher", "admin"], format_func=lambda x: {"student": "Aluno", "teacher": "Professor", "admin": "Administrador"}.get(x, x))
                
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

        st.divider()
        st.subheader("Filtros de Usuários")

        # --- FILTROS ---
        col_f1, col_f2 = st.columns(2)
        
        role_map_filter = {"Todos": None, "Alunos": "student", "Professores": "teacher", "Administradores": "admin"}
        selected_role_key = col_f1.selectbox("Filtrar por Função", list(role_map_filter.keys()))
        
        selected_class_id = None
        if selected_role_key == "Alunos":
            classes = db.get_classes()
            class_options = {"Todas as Turmas": None}
            class_options.update({c['name']: c['id'] for c in classes})
            
            selected_class_name = col_f2.selectbox("Filtrar por Turma", list(class_options.keys()))
            selected_class_id = class_options[selected_class_name]

        # --- LÓGICA DE BUSCA E EXIBIÇÃO ---
        st.subheader("Usuários Cadastrados")
        users = []
        if selected_role_key == "Alunos" and selected_class_id is not None:
            # Caso específico: Alunos de uma turma
            users = db.get_students_by_class(selected_class_id)
        else:
            # Outros casos: buscar todos e filtrar em memória
            all_users = db.get_all_users()
            target_role = role_map_filter[selected_role_key]
            if target_role:
                users = [u for u in all_users if u.get('role') == target_role]
            else:
                users = all_users

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
                role_map = {"student": "Aluno", "teacher": "Professor", "admin": "Administrador"}
                c3.write(role_map.get(u['role'], u['role']))
                
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
        else:
            st.info("Nenhum usuário encontrado com os filtros selecionados.")

    with tab2:
        st.subheader("Aulas")
        
        with st.expander("➕ Criar Nova Turma"):
            with st.form("new_class_form", clear_on_submit=True):
                class_name = st.text_input("Nome da Turma (ex: 3º Ano A - 2024)")
                class_code = st.text_input("Código Único da Turma (ex: 3A2024)")
                submitted_class = st.form_submit_button("Criar Turma")
                if submitted_class and class_name and class_code:
                    # Use a default school for simplicity, as school management is not a primary UI feature
                    school_id = db.upsert_school("Escola Padrão", "N/A")
                    if school_id:
                        new_class_id = db.upsert_class(class_name, class_code, school_id)
                        if new_class_id:
                            st.success(f"Turma '{class_name}' criada com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao criar a turma. O código pode já existir.")
                    else:
                        st.error("Erro ao acessar a escola padrão.")
        
        # Seletor de Turma
        classes = db.get_classes()
        class_options = {c['name']: c['id'] for c in classes}
        selected_class_name = st.selectbox("Selecione a Turma para gerenciar", options=["-- Selecione --"] + list(class_options.keys()))

        if selected_class_name != "-- Selecione --":
            class_id = class_options[selected_class_name]
            
            with st.expander("➕ Criar Nova Disciplina e Vincular a esta Turma"):
                with st.form("new_subject_form", clear_on_submit=True):
                    subject_name = st.text_input("Nome da Disciplina (ex: Programação com Python)")
                    submitted_subject = st.form_submit_button("Criar e Vincular Disciplina")
                    if submitted_subject and subject_name:
                        subject_id = db.upsert_subject(subject_name)
                        if subject_id:
                            db.link_subject_to_class(class_id, subject_id)
                            st.success(f"Disciplina '{subject_name}' vinculada à turma '{selected_class_name}'!")
                            st.rerun()
                        else:
                            st.error("Erro ao criar a disciplina.")
            
            # Seletor de Disciplina (baseado na turma)
            subjects = db.get_subjects_for_class(class_id)
            subject_options = {s['name']: s['id'] for s in subjects}
            
            if not subjects:
                st.warning("Esta turma não possui disciplinas vinculadas. Crie e vincule uma no formulário acima.")
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
                            st.caption(f"Questões disponíveis para {assessment['type']} (filtradas por semana/conteúdo).")
                            
                            # Seletor de Carga Horária para definir o filtro de aulas
                            workload_opt = st.radio("Carga Horária da Disciplina:", ["40h (8 aulas/sem)", "80h (10 aulas/sem)"], horizontal=True, key=f"wl_{assessment['id']}")
                            workload_val = 80 if "80h" in workload_opt else 40
                            
                            quiz_questions = db.get_all_quiz_questions_for_subject(subject_id_av, assessment['type'], workload_val)
                            
                            if not quiz_questions:
                                st.info(f"Nenhuma questão encontrada nos quizzes correspondentes à {assessment['type']}.")
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

    with tab6:
        st.subheader("📊 Relatórios de Atividades")
        st.markdown("Visualize as ações recentes dos usuários na plataforma.")

        # Filtros
        users = db.get_all_users()
        user_options = ["Todos"] + [u['username'] for u in users]
        selected_user_filter = st.selectbox("Filtrar por Usuário", user_options)

        # Busca dados
        if selected_user_filter != "Todos":
            history_data = db.get_user_history(selected_user_filter)
        else:
            history_data = db.get_all_history(limit=500)

        if history_data:
            # Exibe tabela
            st.dataframe(history_data, use_container_width=True, column_config={
                "username": "Usuário",
                "activity": "Ação Realizada",
                "timestamp": "Data/Hora"
            })

            # Botão de Exportação
            df = pd.DataFrame(history_data)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Baixar Relatório Completo (CSV)", data=csv, file_name="relatorio_atividades.csv", mime="text/csv")
        else:
            st.info("Nenhuma atividade registrada com os filtros atuais.")

    with tab7:
        st.subheader("🤖 Gerador de Aulas com IA (Gemini)")
        st.markdown("Cole o cronograma, analise a estrutura e gere as aulas automaticamente no banco de dados.")

        # 1. Seleção de Contexto
        classes = db.get_classes()
        class_options = {c['name']: c['id'] for c in classes}
        sel_class_name = st.selectbox("1. Selecione a Turma", ["-- Selecione --"] + list(class_options.keys()), key="gen_class")

        if sel_class_name != "-- Selecione --":
            class_id = class_options[sel_class_name]
            subjects = db.get_subjects_for_class(class_id)
            subject_options = {s['name']: s['id'] for s in subjects}
            
            sel_subject_name = st.selectbox("2. Selecione a Disciplina", ["-- Selecione --"] + list(subject_options.keys()), key="gen_subj")

            if sel_subject_name != "-- Selecione --":
                subject_id = subject_options[sel_subject_name]
                
                # Recupera último cronograma salvo
                last_schedule = db.get_latest_schedule(subject_id)
                
                cronograma_text = st.text_area("3. Cole o texto do Cronograma aqui:", value=last_schedule if last_schedule else "", height=200)
                
                api_key = st.text_input("4. Chave de API do Google Gemini", type="password", help="Necessária para gerar o conteúdo.")

                if st.button("🔍 Analisar Cronograma"):
                    if not api_key:
                        st.error("Por favor, insira a Chave de API.")
                    elif not cronograma_text:
                        st.warning("Cole o texto do cronograma.")
                    else:
                        ai.configure_api(api_key)
                        with st.spinner("Interpretando cronograma..."):
                            # Salva cronograma no banco
                            db.create_schedule(subject_id, cronograma_text)
                            
                            # Analisa estrutura
                            plan = ai.parse_cronograma(cronograma_text)
                            
                            if plan:
                                st.session_state['lesson_plan'] = plan
                                st.success(f"Identificadas {len(plan)} aulas no cronograma.")
                            else:
                                st.error("Não foi possível extrair aulas do texto. Verifique o formato.")

                # Exibe plano e permite geração
                if 'lesson_plan' in st.session_state and st.session_state.get('lesson_plan'):
                    plan = st.session_state['lesson_plan']
                    
                    # Verifica conflitos com aulas existentes no banco
                    existing_lessons = db.get_lessons_for_subject(subject_id)
                    existing_titles = [l['title'] for l in existing_lessons]
                    
                    st.divider()
                    st.write("### 📋 Plano de Aulas Identificado")
                    
                    lessons_to_generate = []
                    conflicting_ids = []
                    
                    for lesson in plan:
                        # Lógica simples de conflito: verifica se o tema está contido em algum título existente
                        # ou se existe uma aula com o mesmo número (se conseguíssemos extrair o numero do titulo)
                        found_lesson = next((l for l in existing_lessons if lesson['topic'] in l['title']), None)
                        is_conflict = found_lesson is not None
                        if is_conflict:
                            conflicting_ids.append(found_lesson['id'])

                        status = "✅ Já existe (Pular)" if is_conflict else "🆕 Será gerada"
                        
                        col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
                        col1.write(f"**#{lesson['lesson_number']}**")
                        col2.write(lesson['topic'])
                        col3.caption(status)
                        
                        if not is_conflict:
                            lessons_to_generate.append(lesson)

                    if conflicting_ids:
                        if st.button(f"🗑️ Excluir {len(set(conflicting_ids))} aulas conflitantes deste cronograma"):
                            for lid in set(conflicting_ids):
                                db.delete_lesson(lid)
                            st.success("Aulas excluídas com sucesso! Clique em 'Analizar Cronograma' novamente para atualizar.")
                            del st.session_state['lesson_plan']
                            st.rerun()

                    if lessons_to_generate:
                        st.info(f"Serão geradas {len(lessons_to_generate)} novas aulas.")
                        
                        if st.button("🚀 Iniciar Geração Automática"):
                            ai.configure_api(api_key)
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            for i, lesson in enumerate(lessons_to_generate):
                                status_text.text(f"Gerando aula {lesson['lesson_number']}: {lesson['topic']}...")
                                
                                # Gera conteúdo
                                content = ai.generate_lesson_markdown(sel_subject_name, sel_class_name, lesson['topic'], lesson['lesson_number'])
                                
                                if content:
                                    # Popula no banco (Aula + Quiz se houver)
                                    # Aqui usamos uma lógica simplificada de inserção direta
                                    # Extrai titulo do markdown gerado
                                    title_match = re.search(r'^#\s+.*Aula\s*\d+:\s*(.*)', content, re.IGNORECASE)
                                    final_title = f"Aula {lesson['lesson_number']}: {lesson['topic']}"
                                    
                                    # Insere aula
                                    lesson_id = db.upsert_lesson(final_title, subject_id, content, "")
                                    
                                    # Tenta extrair e inserir Quiz (reutilizando lógica simplificada)
                                    quiz_match = re.search(r'(?:^|\n)(##\s*📝\s*Quiz)', content, re.IGNORECASE)
                                    if quiz_match and lesson_id:
                                        split_index = quiz_match.start(1)
                                        quiz_content = content[split_index:].strip()
                                        # Para simplificar, criamos o quiz básico. 
                                        # A lógica completa de parsing de quiz do seed_lessons é complexa para replicar aqui inline,
                                        # mas podemos criar o quiz vazio ou tentar um parse simples.
                                        db.create_quiz(lesson_id, f"Quiz: {final_title}")
                                
                                progress_bar.progress((i + 1) / len(lessons_to_generate))
                                time.sleep(1) # Rate limit preventivo
                            
                            status_text.text("✅ Processo concluído!")
                            st.success("Todas as aulas foram geradas e salvas no banco de dados!")
                            # Limpa o plano para evitar re-cliques acidentais
                            del st.session_state['lesson_plan']
                            st.rerun()
                    else:
                        st.success("Todas as aulas do cronograma já parecem estar cadastradas!")