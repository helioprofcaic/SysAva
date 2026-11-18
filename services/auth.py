# services/auth.py
import bcrypt
import streamlit as st
import uuid

def hash_password(password: str) -> str:
    """Criptografa uma senha para armazenamento."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# --- Gerenciamento de Sessão ---
@st.cache_resource
def get_active_sessions():
    """Retorna um dicionário compartilhado para gerenciar sessões ativas."""
    return {}

def create_session(username, role, name):
    session_id = str(uuid.uuid4())
    sessions = get_active_sessions()
    sessions[session_id] = {
        "username": username,
        "role": role,
        "name": name
    }
    return session_id

def get_session(session_id):
    sessions = get_active_sessions()
    return sessions.get(session_id)

def logout_session(session_id):
    sessions = get_active_sessions()
    if session_id in sessions:
        del sessions[session_id]

@st.cache_resource
def get_revoked_users():
    """Usuarios cujo acesso foi bloqueado neste processo (checagem barata)."""
    return set()

def logout_user_sessions(username):
    """Encerra as sessoes ativas de um usuario neste processo."""
    alvo = str(username or "").strip().lower()
    if not alvo:
        return 0
    sessions = get_active_sessions()
    alvos = [sid for sid, dados in sessions.items()
             if str((dados or {}).get("username") or "").strip().lower() == alvo]
    for sid in alvos:
        sessions.pop(sid, None)
    get_revoked_users().add(alvo)
    return len(alvos)

def allow_user_sessions(username):
    """Libera o usuario apos reativar o acesso."""
    alvo = str(username or "").strip().lower()
    if alvo:
        get_revoked_users().discard(alvo)

def is_session_revoked(username):
    alvo = str(username or "").strip().lower()
    return bool(alvo) and alvo in get_revoked_users()