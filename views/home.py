import streamlit as st
from services import database as db
import pandas as pd

def show_student_home():
    """Exibe a home page padrao para o aluno, com seu historico de atividades."""

    username = st.session_state.get('username')
    if not username:
        st.warning("Por favor, faca login para ver seu historico.")
        return

    # --- Seletor de Disciplina para o Score ---
    enrollment = db.get_user_enrollment(username)
    subjects = []
    if enrollment:
        subjects = db.get_subjects_for_class(enrollment['class_id'])
        subjects = [s for s in subjects if s.get('is_active', True)]

    subject_options = {"Visao Geral (Todas)": None}
    if subjects:
        subject_options.update({s['name']: s['id'] for s in subjects})

    selected_subject_name = st.selectbox("Filtrar progresso por disciplina:", list(subject_options.keys()))
    selected_subject_id = subject_options[selected_subject_name]

    # --- Score do Aluno ---
    st.subheader("Seu Progresso (Score)")
    score = db.get_student_score(username, filter_subject_id=selected_subject_id)

    c1, c2, c3, c4 = st.columns(4)
    total_label = "Pontuacao Total" if selected_subject_id is None else f"Score em {selected_subject_name}"
    c1.metric(total_label, score['total'])
    c2.metric("Aulas Vistas (+1)", score['lesson'])
    c3.metric("Pontos em Quizzes", score['quiz'])
    c4.metric("Forum por Aula (+1)", score['forum'])

    st.caption("Criterio: 1 ponto por aula visualizada + Nota dos Quizzes + 1 ponto por participacao no forum da aula.")
    st.divider()

    # ========================================================================
    # NOTAS DAS AVALIACOES POR DISCIPLINA
    # ========================================================================
    st.subheader("Notas das Avaliacoes")

    if not subjects:
        st.info("Voce ainda nao esta matriculado em nenhuma disciplina.")
    else:
        subject_ids = [s['id'] for s in subjects]
        assessment_results = db.get_student_assessment_results(username, subject_ids)

        if not assessment_results:
            st.info("Nenhuma avaliacao cadastrada para suas disciplinas.")
        else:
            # Agrupa por disciplina
            subject_map = {s['id']: s['name'] for s in subjects}

            # Filtra por disciplina selecionada (se houver)
            if selected_subject_id:
                assessment_results = [r for r in assessment_results if r['subject_id'] == selected_subject_id]

            # Agrupa resultados por disciplina
            by_subject = {}
            for r in assessment_results:
                sid = r['subject_id']
                if sid not in by_subject:
                    by_subject[sid] = []
                by_subject[sid].append(r)

            for sid, results in by_subject.items():
                sname = subject_map.get(sid, f"Disciplina {sid}")
                total = len(results)
                done = len([r for r in results if r['status'] == 'submitted' and r['score'] is not None])
                pending = total - done

                with st.expander(f"{sname} — {done}/{total} avaliadas", expanded=(selected_subject_id is not None)):
                    # Tabela de notas
                    rows = []
                    for r in sorted(results, key=lambda x: x['type']):
                        nota = f"{r['score']:.1f}" if r['score'] is not None else "-"
                        status = "Realizada" if r['status'] == 'submitted' and r['score'] is not None else "Pendente"
                        data = ""
                        if r['submitted_at']:
                            ts = str(r['submitted_at'])
                            if 'T' in ts:
                                data = ts.split('T')[0]
                        rows.append({
                            "Avaliacao": r['type'],
                            "Titulo": r['title'],
                            "Nota": nota,
                            "Status": status,
                            "Data": data
                        })

                    df = pd.DataFrame(rows)
                    st.dataframe(df, hide_index=True, width="stretch", column_config={
                        "Avaliacao": st.column_config.TextColumn("Tipo", width="small"),
                        "Titulo": st.column_config.TextColumn("Titulo", width="large"),
                        "Nota": st.column_config.TextColumn("Nota", width="small"),
                        "Status": st.column_config.TextColumn("Status", width="small"),
                        "Data": st.column_config.TextColumn("Data", width="medium")
                    })

                    # Resumo
                    if done > 0:
                        scores = [r['score'] for r in results if r['score'] is not None]
                        media = sum(scores) / len(scores)
                        st.caption(f"Media: {media:.1f} | Melhor nota: {max(scores):.1f} | Pior nota: {min(scores):.1f}")
                    if pending > 0:
                        st.warning(f"{pending} avaliacao(oes) pendente(s).")

    st.divider()

    # ========================================================================
    # HISTORICO DE ATIVIDADES
    # ========================================================================
    st.subheader("Seu Historico de Atividades")

    user_history = db.get_user_history(username)

    if user_history:
        with st.container():
            for item in user_history:
                col1, col2 = st.columns([0.7, 0.3])
                with col1:
                    st.markdown(f"**{item.get('activity', 'Atividade')}**")
                with col2:
                    ts = str(item.get('timestamp', ''))
                    if 'T' in ts:
                        data, hora = ts.split('T')
                        st.caption(f"{data} {hora[:5]}")
                    else:
                        st.caption(ts)
                st.divider()
    else:
        st.info("Nenhuma atividade registrada recentemente.")

def show_teacher_dashboard():
    """Exibe um painel com métricas da plataforma e atalhos para professor/admin."""
    role = st.session_state.get('role')
    is_admin = role == 'admin'

    if is_admin:
        st.subheader("🛡️ Central de Comando")
        st.markdown("Visao geral da plataforma e ferramentas de gestao.")
    else:
        st.subheader("👨‍🏫 Painel do Professor")
        st.markdown("Visao geral das turmas e ferramentas rapidas.")

    # ========================================================================
    # SECAO 1: Saude da Plataforma (Metricas)
    # ========================================================================
    st.markdown("#### Status da Plataforma")

    all_users = db.get_all_users() if db.is_db_connected() else []
    all_classes = db.get_classes() if db.is_db_connected() else []
    all_subjects = db.get_subjects() if db.is_db_connected() else []
    all_lessons = db.get_lessons() if db.is_db_connected() else []

    total_users = len(all_users)
    total_students = len([u for u in all_users if u.get('role') == 'student'])
    total_teachers = len([u for u in all_users if u.get('role') in ('teacher', 'admin')])
    total_classes = len(all_classes)
    total_subjects = len(all_subjects)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Usuarios", total_users)
    m2.metric("Alunos", total_students)
    m3.metric("Professores", total_teachers)
    m4.metric("Turmas", total_classes)
    m5.metric("Disciplinas", total_subjects)

    # ========================================================================
    # SECAO 2: Visao do Conteudo
    # ========================================================================
    st.divider()
    st.markdown("#### Conteudo da Plataforma")

    col_lessons, col_assessments = st.columns(2)

    with col_lessons:
        st.markdown("**Aulas e Quizzes**")
        total_lessons = len(all_lessons)

        # Conta quizzes associados a aulas
        lessons_with_quiz = 0
        for lesson in all_lessons:
            quiz = db.get_quiz_for_lesson(lesson['id'])
            if quiz:
                lessons_with_quiz += 1

        lessons_without_quiz = total_lessons - lessons_without_quiz if total_lessons > 0 else 0

        c_a, c_b, c_c = st.columns(3)
        c_a.metric("Aulas", total_lessons)
        c_b.metric("Com Quiz", lessons_with_quiz)
        c_c.metric("Sem Quiz", total_lessons - lessons_with_quiz)

        if total_lessons > 0 and lessons_with_quiz < total_lessons:
            pct = lessons_with_quiz / total_lessons
            st.progress(pct, text=f"Cobertura de Quizzes: {pct:.0%}")

    with col_assessments:
        st.markdown("**Avaliacoes**")
        all_assessments = db.get_all_assessments() if db.is_db_connected() else []
        total_assessments = len(all_assessments)

        # Conta questoes totais
        total_questions = 0
        assessments_empty = 0
        for a in all_assessments:
            questions = db.get_assessment_questions(a['id'])
            total_questions += len(questions)
            if len(questions) == 0:
                assessments_empty += 1

        c_x, c_y, c_z = st.columns(3)
        c_x.metric("Provas", total_assessments)
        c_y.metric("Questoes", total_questions)
        c_z.metric("Sem Questoes", assessments_empty)

        if total_assessments > 0 and assessments_empty > 0:
            st.warning(f"{assessments_empty} prova(s) sem questoes cadastradas.")

    # ========================================================================
    # SECAO 3: Atividade Recente
    # ========================================================================
    st.divider()
    st.markdown("#### Atividade Recente")

    recent_history = db.get_all_history(limit=10) if db.is_db_connected() else []

    if recent_history:
        df_history = pd.DataFrame(recent_history)
        # Renomeia colunas para exibicao
        col_config = {
            "username": st.column_config.TextColumn("Usuario", width="medium"),
            "activity": st.column_config.TextColumn("Atividade", width="large"),
            "timestamp": st.column_config.TextColumn("Data/Hora", width="medium")
        }
        # Formata timestamp
        if 'timestamp' in df_history.columns:
            df_history['timestamp'] = pd.to_datetime(df_history['timestamp']).dt.strftime('%d/%m/%Y %H:%M')
        st.dataframe(df_history, column_config=col_config, hide_index=True, width="stretch")
    else:
        st.info("Nenhuma atividade registrada recentemente.")

    # ========================================================================
    # SECAO 4: Acoes Rapidas
    # ========================================================================
    st.divider()
    st.markdown("#### Acoes Rapidas")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("📝 Gerenciar Avaliacoes", width="stretch"):
            st.session_state.page = "Avaliacoes"
            st.rerun()
    with col_b:
        if st.button("📚 Gerenciar Conteudo", width="stretch"):
            st.session_state.page = "Admin"
            st.rerun()
    with col_c:
        if st.button("🧩 Central de Plugins", width="stretch"):
            st.session_state.page = "Plugins"
            st.rerun()

    # ========================================================================
    # SECAO 5: Consulta de Score Individual
    # ========================================================================
    st.divider()
    st.markdown("#### Consulta de Score Individual")

    class_options = {c['name']: c['id'] for c in all_classes}
    selected_class_score = st.selectbox("1. Selecione a Turma:", ["-- Selecione --"] + list(class_options.keys()), key="score_class_sel")

    if selected_class_score != "-- Selecione --":
        class_id_score = class_options[selected_class_score]

        subjects = db.get_subjects_for_class(class_id_score)
        subjects = [s for s in subjects if s.get('is_active', True)]

        subject_options_teacher = {"Visao Geral (Todas)": None}
        if subjects:
            subject_options_teacher.update({s['name']: s['id'] for s in subjects})

        selected_subject_name_teacher = st.selectbox(
            "2. Selecione a Disciplina (Score):",
            list(subject_options_teacher.keys()),
            key="score_subject_sel"
        )
        selected_subject_id_teacher = subject_options_teacher[selected_subject_name_teacher]

        if db.is_db_connected():
            students = db.get_students_by_class(class_id_score)
        else:
            students = [
                {'id': 'mock-1', 'name': 'Aluno Teste 1', 'username': 'aluno1', 'role': 'student'},
                {'id': 'mock-2', 'name': 'Aluno Teste 2', 'username': 'aluno2', 'role': 'student'}
            ]
            st.info("Exibindo alunos de teste (Modo Offline)")

        if not students:
            st.warning("Nenhum aluno encontrado nesta turma.")
        else:
            student_options = {f"{s['name']} ({s['username']})": s['username'] for s in students}
            selected_student_key = st.selectbox("3. Selecione o Aluno:", ["-- Selecione --"] + list(student_options.keys()), key="score_student_sel")

            if selected_student_key != "-- Selecione --":
                target_username = student_options[selected_student_key]
                st_score = db.get_student_score(target_username, filter_subject_id=selected_subject_id_teacher)

                st.info(f"**Score Detalhado de {selected_student_key}:**")
                sc1, sc2, sc3, sc4 = st.columns(4)
                total_label_teacher = "Total" if selected_subject_id_teacher is None else f"Score em {selected_subject_name_teacher}"
                sc1.metric(total_label_teacher, st_score['total'])
                sc2.metric("Aulas", st_score['lesson'])
                sc3.metric("Quizzes", st_score['quiz'])
                sc4.metric("Forum", st_score['forum'])

    # ========================================================================
    # SECAO 6: Dashboard de Participacao da Turma
    # ========================================================================
    st.divider()
    st.markdown("#### Participacao da Turma")

    if not all_classes:
        st.warning("Nenhuma turma cadastrada no sistema.")
        return

    class_map = {c['name']: c['id'] for c in all_classes}
    selected_class_name = st.selectbox("Selecione uma turma para analisar:", ["-- Selecione --"] + list(class_map.keys()), key="participation_class_sel")

    if selected_class_name != "-- Selecione --":
        class_id = class_map[selected_class_name]

        with st.spinner(f"Analisando dados da turma {selected_class_name}..."):
            students = db.get_students_by_class(class_id)
            if not students:
                st.info("Esta turma nao possui alunos matriculados.")
                return

            combined_data = []
            for s in students:
                progress = db.get_user_progress_stats(s['username'])
                progress['Aluno'] = s['name']
                combined_data.append(progress)

            df = pd.DataFrame(combined_data)

            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric("Nº de Alunos", len(students))
            m_col2.metric("Media de Aulas Vistas", f"{df['lessons'].mean():.1f}")
            m_col3.metric("Media de Quizzes Feitos", f"{df['quizzes'].mean():.1f}")

            st.markdown("##### Engajamento por Aluno")
            st.dataframe(df[['Aluno', 'lessons', 'quizzes', 'forum']].rename(columns={'lessons': 'Aulas', 'quizzes': 'Quizzes', 'forum': 'Fórum'}), width="stretch")

def show_page():
    school_info = db.get_school()
    school_name = school_info.get('name') if school_info else None
    user_name = st.session_state.get('usuario', 'Usuário')
    st.title(f"Bem-vindo, {user_name}!")
    if school_name:
        st.caption(f"Instituição: **{school_name}**")
    st.markdown("---")

    role = st.session_state.get('role')

    if role in ['teacher', 'admin']:
        show_teacher_dashboard()
    else: # student or default
        show_student_home()