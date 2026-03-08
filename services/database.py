# services/database.py
from supabase import create_client, Client
import streamlit as st
import httpx

@st.cache_resource
def init_connection():
    """Inicializa e armazena em cache a conexão com o Supabase."""
    try:
        supabase_url = st.secrets["SUPABASE_URL"]
        supabase_key = st.secrets["SUPABASE_KEY"]
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"Erro na conexão com Supabase: {e}")
        return None

supabase = init_connection()

def is_db_connected():
    """Verifica se a conexão com o banco de dados foi estabelecida."""
    return supabase is not None

# --- Funções de Usuário ---
def get_user(username: str):
    if not is_db_connected(): return None
    response = supabase.table("app_users").select("username, password, name, role").eq("username", username).execute()
    return response.data[0] if response.data else None

def create_user(username: str, hashed_password: str, name: str, ra: str, role: str = 'student'):
    if not is_db_connected(): return None, "Banco de dados não conectado"
    try:
        response = supabase.table("app_users").insert({
            "username": username, "password": hashed_password, "name": name, "ra": ra, "role": role
        }).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

def delete_user(username: str):
    """Remove um usuário do banco de dados."""
    if not is_db_connected(): return None, "Banco de dados não conectado"
    try:
        response = supabase.table("app_users").delete().eq("username", username).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

# --- Funções de Histórico do Usuário ---
def add_user_history(username: str, activity: str):
    """Adiciona uma entrada ao histórico do usuário."""
    if not is_db_connected(): return None, "Banco de dados não conectado"
    try:
        response = supabase.table("user_history").insert({
            "username": username, "activity": activity
        }).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

def get_user_history(username: str):
    """Busca o histórico de um usuário."""
    if not is_db_connected(): return []
    try:
        response = supabase.table("user_history").select("*").eq("username", username).order("timestamp", desc=True).execute()
        return response.data
    except Exception as e:
        return []

def get_all_history(limit: int = 200):
    """Busca o histórico global de atividades (para relatórios)."""
    if not is_db_connected(): return []
    try:
        response = supabase.table("user_history").select("*").order("timestamp", desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        return []

def upsert_user(username: str, hashed_password: str, name: str, ra: str):
    """Cria ou atualiza um usuário (útil para scripts de importação em massa)."""
    if not is_db_connected(): return None, "Banco de dados não conectado"
    try:
        response = supabase.table("app_users").upsert({
            "username": username, "password": hashed_password, "name": name, "ra": ra, "role": "student"
        }).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

def get_all_users():
    if not is_db_connected(): return []
    response = supabase.table("app_users").select("username, name, role").execute()
    return response.data

# --- Funções do Fórum ---
def get_forum_posts(lesson_id: int = None):
    if not is_db_connected(): return []
    try:
        query = supabase.table("forum_posts").select("*").order("created_at", desc=True)
        if lesson_id:
            query = query.eq("lesson_id", lesson_id)
        else:
            # Fórum geral mostra posts sem aula associada
            query = query.is_("lesson_id", "null")
        response = query.execute()
        return response.data
    except Exception as e:
        print(f"Erro ao buscar posts do fórum: {e}")
        return []

def add_forum_post(user_name: str, message: str, lesson_id: int = None):
    if not is_db_connected(): return None, "Banco de dados não conectado"
    try:
        post_data = {"user_name": user_name, "message": message}
        if lesson_id:
            post_data['lesson_id'] = lesson_id
        response = supabase.table("forum_posts").insert(post_data).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

def delete_forum_post(post_id: int):
    if not is_db_connected(): return None, "Banco de dados não conectado"
    response, error = supabase.table("forum_posts").delete().eq("id", post_id).execute()
    return response, error

# --- Funções da Estrutura Acadêmica ---

def upsert_school(name: str, gre: str):
    """Insere ou atualiza uma escola. Retorna o ID da escola."""
    if not is_db_connected(): return None
    try:
        # A cláusula 'on_conflict' e 'update' é específica do PostgreSQL. Usamos um select/insert para simplicidade.
        res = supabase.table("schools").select("id").eq("name", name).execute()
        if res.data:
            return res.data[0]['id']
        res = supabase.table("schools").insert({"name": name, "gre": gre}).execute()
        return res.data[0]['id']
    except Exception as e:
        print(f"Erro ao acessar tabela 'schools': {e}")
        return None

def upsert_class(name: str, code: str, school_id: int):
    """Insere ou atualiza uma turma. Retorna o ID da turma."""
    if not is_db_connected(): return None
    res = supabase.table("classes").select("id").eq("code", code).execute()
    if res.data:
        return res.data[0]['id']
    res = supabase.table("classes").insert({"name": name, "code": code, "school_id": school_id}).execute()
    return res.data[0]['id']

def get_classes():
    """Busca todas as turmas cadastradas."""
    if not is_db_connected(): return []
    try:
        response = supabase.table("classes").select("*").order("name").execute()
        return response.data
    except Exception as e:
        print(f"Erro ao buscar turmas: {e}")
        return []

def get_class_by_code(code: str):
    if not is_db_connected(): return None
    res = supabase.table("classes").select("id").eq("code", code).execute()
    return res.data[0] if res.data else None

def upsert_subject(name: str):
    """Insere ou atualiza uma disciplina. Retorna o ID da disciplina."""
    if not is_db_connected(): return None
    res = supabase.table("subjects").select("id").eq("name", name).execute()
    if res.data:
        return res.data[0]['id']
    res = supabase.table("subjects").insert({"name": name}).execute()
    return res.data[0]['id']

def link_subject_to_class(class_id: int, subject_id: int):
    """Associa uma disciplina a uma turma, ignorando se já existir."""
    if not is_db_connected(): return
    # A API do supabase-py não suporta 'ON CONFLICT DO NOTHING' diretamente na inserção.
    # Verificamos antes de inserir para evitar erros de duplicidade.
    res = supabase.table("class_subjects").select("*").eq("class_id", class_id).eq("subject_id", subject_id).execute()
    if not res.data:
        supabase.table("class_subjects").insert({"class_id": class_id, "subject_id": subject_id}).execute()

def get_subjects():
    """Busca todas as disciplinas."""
    if not is_db_connected(): return []
    try:
        response = supabase.table("subjects").select("*").execute()
        return response.data
    except Exception:
        return []

def enroll_student(username: str, class_id: int):
    """Matricula um aluno em uma turma."""
    if not is_db_connected(): return None, "Banco de dados não conectado"
    try:
        response = supabase.table("student_enrollments").upsert({
            "user_username": username, "class_id": class_id
        }).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

def get_subject_by_name(name: str):
    if not is_db_connected(): return None
    # Tenta busca exata
    res = supabase.table("subjects").select("id").eq("name", name).execute()
    if res.data:
        return res.data[0]
    
    # Tenta busca case-insensitive (ignora maiúsculas/minúsculas)
    res = supabase.table("subjects").select("id").ilike("name", name).execute()
    return res.data[0] if res.data else None

def get_user_enrollment(username: str):
    """Busca a matrícula (turma) de um usuário."""
    if not is_db_connected(): return None
    try:
        # O username do app é o user_username na tabela de matrículas
        response = supabase.table("student_enrollments").select("class_id").eq("user_username", username).limit(1).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Erro ao buscar matrícula do usuário '{username}': {e}")
        return None

def get_subjects_for_class(class_id: int):
    """Busca todas as disciplinas associadas a uma turma."""
    if not is_db_connected(): return []
    try:
        # 1. Buscar os subject_ids da tabela de junção
        response = supabase.table("class_subjects").select("subject_id").eq("class_id", class_id).execute()
        if not response.data:
            return []
        
        subject_ids = [item['subject_id'] for item in response.data]
        
        # 2. Buscar os detalhes das disciplinas com base nos IDs
        subjects_response = supabase.table("subjects").select("*").in_("id", subject_ids).order("name").execute()
        return subjects_response.data
    except Exception as e:
        print(f"Erro ao buscar disciplinas da turma {class_id}: {e}")
        return []

# --- Funções de Aulas e Conteúdo ---
def get_lessons():
    if not is_db_connected(): return []
    try:
        response = supabase.table("lessons").select("*").order("id").execute()
        return response.data
    except Exception as e:
        print(f"Erro ao buscar aulas (verifique se a tabela 'lessons' existe): {e}")
        return []

def get_lessons_for_subject(subject_id: int):
    """Busca todas as aulas de uma disciplina específica."""
    if not is_db_connected(): return []
    try:
        response = supabase.table("lessons").select("*").eq("subject_id", subject_id).order("id").execute()
        return response.data
    except Exception as e:
        print(f"Erro ao buscar aulas da disciplina {subject_id}: {e}")
        return []

def get_lesson_by_id(lesson_id: int):
    if not is_db_connected(): return None
    try:
        response = supabase.table("lessons").select("*").eq("id", lesson_id).execute()
        return response.data[0] if response.data else None
    except Exception:
        return None

def get_quiz_for_lesson(lesson_id: int):
    if not is_db_connected(): return None
    try:
        response = supabase.table("quizzes").select("id, title").eq("lesson_id", lesson_id).limit(1).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Erro ao buscar quiz da aula {lesson_id}: {e}")
        return None

def get_quiz_by_id(quiz_id: int):
    if not is_db_connected(): return None
    try:
        response = supabase.table("quizzes").select("*").eq("id", quiz_id).limit(1).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Erro ao buscar quiz por ID {quiz_id}: {e}")
        return None

def get_quiz_questions(quiz_id: int):
    if not is_db_connected(): return []
    try:
        response = supabase.table("quiz_questions").select("*").eq("quiz_id", quiz_id).execute()
        return response.data
    except Exception as e:
        print(f"Erro ao buscar questões do quiz {quiz_id}: {e}")
        return []

def create_lesson(title: str, subject_id: int, description: str, video_url: str):
    """Cria uma nova aula no banco."""
    if not is_db_connected(): return None, "Banco de dados não conectado"
    try:
        response = supabase.table("lessons").insert({
            "title": title, "subject_id": subject_id, "description": description, "video_url": video_url
        }).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

def upsert_lesson(title: str, subject_id: int, description: str, video_url: str):
    """Cria ou atualiza uma aula. Retorna o ID da aula."""
    if not is_db_connected(): return None
    try:
        lesson_data = {
            "title": title,
            "subject_id": subject_id,
            "description": description,
            "video_url": video_url
        }
        # on_conflict usa as colunas com a constraint UNIQUE para fazer o upsert
        response = supabase.table("lessons").upsert(lesson_data, on_conflict="subject_id,title").execute()
        return response.data[0]['id']
    except Exception as e:
        print(f"Erro ao fazer upsert da aula '{title}': {e}")
        return None

def create_quiz(lesson_id: int, title: str):
    """Cria um novo quiz associado a uma aula."""
    if not is_db_connected(): return None, "Banco de dados não conectado"
    try:
        response = supabase.table("quizzes").insert({"lesson_id": lesson_id, "title": title}).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

def create_quiz_question(quiz_id: int, question_text: str, options: list, correct_index: int):
    """Cria uma nova questão para um quiz."""
    if not is_db_connected(): return None, "Banco de dados não conectado"
    try:
        response = supabase.table("quiz_questions").insert({
            "quiz_id": quiz_id, "question_text": question_text, "options": options, "correct_option_index": correct_index
        }).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

# --- Funções de Avaliações (MN1, MN2, MN3, RM) ---

def get_assessments_by_subject(subject_id: int):
    """Busca todas as avaliações de uma disciplina."""
    if not is_db_connected(): return []
    try:
        response = supabase.table("assessments").select("*").eq("subject_id", subject_id).order("type").execute()
        return response.data
    except Exception as e:
        print(f"Erro ao buscar avaliações: {e}")
        return []

def create_assessment(subject_id: int, type: str, title: str):
    """Cria uma nova avaliação (MN1, MN2, MN3, RM)."""
    if not is_db_connected(): return None, "Banco de dados não conectado"
    try:
        response = supabase.table("assessments").insert({
            "subject_id": subject_id, "type": type, "title": title
        }).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

def get_assessment_questions(assessment_id: int):
    """Busca as questões de uma avaliação."""
    if not is_db_connected(): return []
    try:
        response = supabase.table("assessment_questions").select("*").eq("assessment_id", assessment_id).order("id").execute()
        return response.data
    except Exception as e:
        return []

def create_assessment_question(assessment_id: int, question_text: str, question_type: str, options: list, correct_index: int):
    """Cria uma questão para avaliação (Objetiva ou Subjetiva)."""
    try:
        data = {
            "assessment_id": assessment_id,
            "question_text": question_text,
            "question_type": question_type, # 'objective' ou 'subjective'
            "options": options,
            "correct_option_index": correct_index
        }
        response = supabase.table("assessment_questions").insert(data).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

def get_all_quiz_questions_for_subject(subject_id: int, assessment_type: str = None, workload: int = 40):
    """Busca questões de quizzes filtradas pelo tipo de avaliação (MN1, MN2, etc)."""
    if not is_db_connected(): return []
    try:
        # 1. Buscar IDs das aulas da disciplina ordenadas por ID (assumindo ordem de criação/semanas)
        lessons_res = supabase.table("lessons").select("id").eq("subject_id", subject_id).order("id").execute()
        all_lessons = lessons_res.data
        
        if not all_lessons: return []

        # Filtragem por tipo de avaliação (baseado em semanas/blocos de aulas)
        # 40h: 8 aulas/semana | 80h: 10 aulas/semana
        lessons_per_week = 10 if workload == 80 else 8
        
        # MN1: Semanas 1 e 2
        mn1_limit = lessons_per_week * 2
        
        # MN2: Semanas 3 e 4
        mn2_start = mn1_limit
        mn2_limit = mn2_start + (lessons_per_week * 2)
        
        # MN3/RM: Todas (Cumulativo, pois MN3 foca na S05 mas pode conter anteriores)
        target_lessons = []
        if assessment_type == 'MN1':
            target_lessons = all_lessons[:mn1_limit]
        elif assessment_type == 'MN2':
            target_lessons = all_lessons[mn2_start:mn2_limit]
        else:
            target_lessons = all_lessons

        if not target_lessons: return []

        lesson_ids = [l['id'] for l in target_lessons]

        # 2. Buscar IDs dos quizzes dessas aulas
        quizzes_res = supabase.table("quizzes").select("id").in_("lesson_id", lesson_ids).execute()
        quiz_ids = [q['id'] for q in quizzes_res.data]
        
        if not quiz_ids: return []

        # 3. Buscar questões desses quizzes
        questions_res = supabase.table("quiz_questions").select("*").in_("quiz_id", quiz_ids).execute()
        return questions_res.data
    except Exception as e:
        print(f"Erro ao buscar banco de questões: {e}")
        return []

# --- Funções de Submissão e Controle de Avaliações ---

def get_user_progress_stats(username: str):
    """Calcula estatísticas de progresso baseadas no histórico para liberar provas."""
    if not is_db_connected(): return {"lessons": 0, "quizzes": 0, "forum": 0}
    
    # Busca todo o histórico do usuário
    # Nota: Em produção, seria ideal fazer count direto no banco, mas user_history é genérico.
    history = get_user_history(username)
    
    unique_lessons = set()
    unique_quizzes = set()
    forum_posts = 0
    
    for item in history:
        act = item.get('activity', '')
        if act.startswith("Acessou a aula:"):
            unique_lessons.add(act) # Conta títulos de aulas únicos
        elif act.startswith("Concluiu Quiz:"):
            unique_quizzes.add(act) # Conta quizzes únicos
        elif "mensagem no fórum" in act:
            forum_posts += 1 # Conta total de posts
            
    return {
        "lessons": len(unique_lessons),
        "quizzes": len(unique_quizzes),
        "forum": forum_posts
    }

def get_student_submission(username: str, assessment_id: int):
    """Verifica se o aluno já realizou a avaliação."""
    if not is_db_connected(): return None
    try:
        res = supabase.table("student_assessments").select("*").eq("user_username", username).eq("assessment_id", assessment_id).execute()
        return res.data[0] if res.data else None
    except Exception:
        return None

def submit_assessment(username: str, assessment_id: int, answers: list):
    """
    Salva a submissão da prova.
    answers: lista de dicts {'question_id': int, 'type': str, 'value': ...}
    """
    if not is_db_connected(): return None, "Offline"
    try:
        # 1. Criar a submissão pai
        sub_res = supabase.table("student_assessments").insert({
            "user_username": username,
            "assessment_id": assessment_id,
            "status": "submitted"
        }).execute()
        
        if not sub_res.data:
            return None, "Erro ao criar registro de submissão."
            
        submission_id = sub_res.data[0]['id']
        
        # 2. Inserir as respostas
        answers_data = []
        for ans in answers:
            entry = {
                "submission_id": submission_id,
                "question_id": ans['question_id'],
                "selected_option_index": ans.get('value'), # Para objetivas
                "answer_text": ans.get('text'),            # Para subjetivas
                "answer_link": ans.get('link')             # Para subjetivas
            }
            answers_data.append(entry)
            
        supabase.table("student_assessment_answers").insert(answers_data).execute()
        return True, None
    except Exception as e:
        return None, str(e)

def simulate_student_activities(username: str):
    """Simula a conclusão de todas as aulas e quizzes para um usuário."""
    if not is_db_connected(): return None, "Offline"
    try:
        lessons = get_lessons()
        if not lessons:
            return None, "Nenhuma aula encontrada para simular."

        history_entries = []
        # Simula acesso a todas as aulas e quizzes
        for lesson in lessons:
            history_entries.append({"username": username, "activity": f"Acessou a aula: {lesson['title']}"})
            quiz = get_quiz_for_lesson(lesson['id'])
            if quiz:
                history_entries.append({"username": username, "activity": f"Concluiu Quiz: {quiz['title']} (2/2)"})
        
        # Simula 15 posts no fórum para garantir liberação
        for _ in range(15):
            history_entries.append({"username": username, "activity": "Enviou mensagem no fórum"})

        supabase.table("user_history").insert(history_entries).execute()
        return True, None
    except Exception as e:
        return None, str(e)

def reset_student_data(username: str):
    """Zera o histórico, submissões e respostas de avaliações de um aluno."""
    if not is_db_connected(): return None, "Offline"
    try:
        supabase.table("user_history").delete().eq("username", username).execute()

        submissions_res = supabase.table("student_assessments").select("id").eq("user_username", username).execute()
        if submissions_res.data:
            submission_ids = [s['id'] for s in submissions_res.data]
            supabase.table("student_assessment_answers").delete().in_("submission_id", submission_ids).execute()
            supabase.table("student_assessments").delete().in_("id", submission_ids).execute()
        
        return True, None
    except Exception as e:
        return None, str(e)

def get_assessment_submissions_with_users(assessment_id: int):
    """Busca todas as submissões de uma avaliação incluindo dados do usuário."""
    if not is_db_connected(): return []
    try:
        # Supabase permite join na query se as chaves estrangeiras estiverem certas
        # Sintaxe: tabela!fk(colunas)
        response = supabase.table("student_assessments")\
            .select("*, app_users!inner(name, ra)")\
            .eq("assessment_id", assessment_id)\
            .execute()
        return response.data
    except Exception as e:
        print(f"Erro ao buscar submissões: {e}")
        return []

def get_submission_answers(submission_id: int):
    """Busca as respostas de uma submissão específica."""
    if not is_db_connected(): return []
    try:
        response = supabase.table("student_assessment_answers").select("*").eq("submission_id", submission_id).execute()
        return response.data
    except Exception:
        return []

def update_submission_score(submission_id: int, new_score: float):
    """Atualiza a nota final de uma submissão."""
    if not is_db_connected(): return None, "Offline"
    try:
        response = supabase.table("student_assessments").update({"score": new_score}).eq("id", submission_id).execute()
        return response.data, None
    except Exception as e:
        return None, str(e)

def get_students_by_class(class_id: int):
    """Busca todos os alunos matriculados em uma turma específica."""
    if not is_db_connected(): return []
    try:
        # 1. Buscar os usernames dos alunos na turma
        enrollments_res = supabase.table("student_enrollments").select("user_username").eq("class_id", class_id).execute()
        if not enrollments_res.data:
            return []
        
        usernames = [e['user_username'] for e in enrollments_res.data]
        
        # 2. Buscar os detalhes desses alunos
        users_res = supabase.table("app_users").select("username, name, ra, role").in_("username", usernames).execute()
        return users_res.data
    except Exception as e:
        print(f"Erro ao buscar alunos da turma {class_id}: {e}")
        return []
