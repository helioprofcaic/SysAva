import streamlit as st

def get_supabase_client():
    """Obtém o cliente do banco (Supabase ou SQLite local)."""
    # O backend já é resolvido por services.database (SYSAVA_DB_MODE).
    from services.database import get_supabase
    return get_supabase()

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