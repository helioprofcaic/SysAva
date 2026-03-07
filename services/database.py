# services/database.py
from supabase import create_client, Client
import streamlit as st

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

def create_user(username: str, hashed_password: str, name: str, ra: str):
    if not is_db_connected(): return None, "Banco de dados não conectado"
    try:
        response = supabase.table("app_users").insert({
            "username": username, "password": hashed_password, "name": name, "ra": ra, "role": "student"
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
def get_forum_posts():
    if not is_db_connected(): return []
    response = supabase.table("forum_posts").select("*").order("created_at", desc=True).execute()
    return response.data

def add_forum_post(user_name: str, message: str):
    if not is_db_connected(): return None, "Banco de dados não conectado"
    response, error = supabase.table("forum_posts").insert({"user_name": user_name, "message": message}).execute()
    return response, error

def delete_forum_post(post_id: int):
    if not is_db_connected(): return None, "Banco de dados não conectado"
    response, error = supabase.table("forum_posts").delete().eq("id", post_id).execute()
    return response, error

# --- Funções da Estrutura Acadêmica ---

def upsert_school(name: str, gre: str):
    """Insere ou atualiza uma escola. Retorna o ID da escola."""
    if not is_db_connected(): return None
    # A cláusula 'on_conflict' e 'update' é específica do PostgreSQL. Usamos um select/insert para simplicidade.
    res = supabase.table("schools").select("id").eq("name", name).execute()
    if res.data:
        return res.data[0]['id']
    res = supabase.table("schools").insert({"name": name, "gre": gre}).execute()
    return res.data[0]['id']

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
