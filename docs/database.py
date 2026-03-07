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
    except Exception:
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

def create_user(username: str, hashed_password: str, name: str):
    if not is_db_connected(): return None, "Banco de dados não conectado"
    try:
        response = supabase.table("app_users").insert({
            "username": username, "password": hashed_password, "name": name, "role": "student"
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