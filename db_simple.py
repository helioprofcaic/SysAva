import streamlit as st

def get_supabase_client():
    """Obtém o cliente Supabase a partir dos segredos do Streamlit."""
    try:
        # Acessa o cliente Supabase que já foi inicializado em database.py
        # e armazenado no estado da sessão pelo hack nos scripts de seed.
        return st.session_state.supabase_client
    except (AttributeError, KeyError):
        # Fallback se o cliente não estiver no estado da sessão
        from services.database import init_connection
        return init_connection()

def simple_upsert_subject(name: str):
    """
    Cria ou atualiza uma disciplina apenas pelo nome, sem usar a coluna 'type'.
    """
    supabase = get_supabase_client()
    try:
        # Verifica se a disciplina já existe
        existing = supabase.table("subjects").select("id").eq("name", name).limit(1).execute()
        if existing.data:
            return existing.data[0]['id']
        
        # Se não existe, insere
        new_subject = supabase.table("subjects").insert({"name": name}).execute()
        return new_subject.data[0]['id']
    except Exception as e:
        print(f"    ERRO ao fazer upsert simples da disciplina '{name}': {e}")
        return None