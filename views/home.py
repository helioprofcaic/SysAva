import streamlit as st
from services import database as db
import pandas as pd

def show_student_home():
    """Exibe a home page padrão para o aluno, com seu histórico de atividades."""
    st.subheader("📅 Seu Histórico de Atividades")
    
    username = st.session_state.get('username')
    if not username:
        st.warning("Por favor, faça login para ver seu histórico.")
        return

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
    """Exibe um painel com atalhos e métricas para o professor."""
    st.subheader("👨‍🏫 Painel do Professor")
    st.markdown("Acesso rápido e visão geral do engajamento das turmas.")

    # 1. Atalhos
    st.markdown("#### Ações Rápidas")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Gerenciar Avaliações", use_container_width=True):
            st.session_state.page = "Avaliações"
            st.rerun()
    with col2:
        if st.button("📚 Gerenciar Conteúdo (Aulas, Quizzes)", use_container_width=True):
            st.session_state.page = "Admin"
            st.rerun()
    
    st.divider()

    # 2. Dashboard de Participação
    st.markdown("#### 📈 Dashboard de Participação da Turma")
    classes = db.get_classes()
    if not classes:
        st.warning("Nenhuma turma cadastrada no sistema.")
        return

    class_map = {c['name']: c['id'] for c in classes}
    selected_class_name = st.selectbox("Selecione uma turma para analisar:", ["-- Selecione --"] + list(class_map.keys()))

    if selected_class_name != "-- Selecione --":
        class_id = class_map[selected_class_name]
        
        with st.spinner(f"Analisando dados da turma {selected_class_name}..."):
            students = db.get_students_by_class(class_id)
            if not students:
                st.info("Esta turma não possui alunos matriculados.")
                return

            progress_data = [db.get_user_progress_stats(s['username']) for s in students]
            df = pd.DataFrame(progress_data)
            df['Aluno'] = [s['name'] for s in students]

            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric("Nº de Alunos", len(students))
            m_col2.metric("Média de Aulas Vistas", f"{df['lessons'].mean():.1f}")
            m_col3.metric("Média de Quizzes Feitos", f"{df['quizzes'].mean():.1f}")

            st.markdown("##### Engajamento por Aluno")
            st.dataframe(df[['Aluno', 'lessons', 'quizzes', 'forum']].rename(columns={'lessons': 'Aulas', 'quizzes': 'Quizzes', 'forum': 'Fórum'}), use_container_width=True)

def show_page():
    st.title(f"Bem-vindo, {st.session_state.get('usuario', 'Usuário')}!")
    st.markdown("---")

    role = st.session_state.get('role')

    if role in ['teacher', 'admin']:
        show_teacher_dashboard()
    else: # student or default
        show_student_home()