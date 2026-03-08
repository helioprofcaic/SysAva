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

def create_lesson(title: str, description: str, video_url: str):
    """Cria uma nova aula no banco."""
    if not is_db_connected(): return None, "Banco de dados não conectado"
    try:
        response = supabase.table("lessons").insert({
            "title": title, "description": description, "video_url": video_url
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
