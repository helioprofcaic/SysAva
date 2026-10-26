import streamlit as st
from services import database as db
from services import auth

def show_page():
    st.title("🔐 Login do Aluno/Professor")
    # A tela de bloqueio abre o portal com ?ra=...; preenche o campo para o
    # aluno nao precisar digitar de novo (a senha continua obrigatoria).
    try:
        ra_prefill = (st.query_params.get("ra") or "").strip()
    except Exception:
        ra_prefill = ""
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        user = st.text_input("Usuário", value=ra_prefill)
        password = st.text_input("Senha", type="password")
        
        if st.button("Entrar"):
            if db.is_db_connected():
                # Remove espaços extras que podem causar erro
                user = user.strip()

                # Tenta capturar o IP do dispositivo do aluno
                try:
                    remote_ip = st.context.headers.get("X-Forwarded-For", "127.0.0.1").split(",")[0]
                except:
                    remote_ip = "127.0.0.1"

                user_data = db.get_user(user)
                if not user_data:
                    # Permite entrar tambem com o RA/CPF (o username real e assumido depois)
                    user_data = db.get_user_by_ra(user)
                if not user_data:
                    # Ignora maiusculas/minusculas no login
                    user_data = db.get_user_ci(user)
                if user_data:
                    if auth.check_password(password, user_data['password']):
                        st.session_state['logado'] = True
                        st.session_state['usuario'] = user_data.get('name', user)
                        # Armazena o username (RA) para consultas de matrícula
                        st.session_state['username'] = user_data.get('username', user)
                        st.session_state['role'] = user_data.get('role', 'student')
                        db.add_user_history(user, f"Realizou login (IP: {remote_ip})")
                        try:
                            from services import audit_log
                            audit_log.registrar("Login", username=st.session_state['username'],
                                                name=st.session_state['usuario'],
                                                role=st.session_state['role'], pagina='Login', ip=remote_ip)
                        except Exception:
                            pass
                        session_id = auth.create_session(user, st.session_state['role'], st.session_state['usuario'])
                        st.query_params["session_id"] = session_id
                        st.session_state.page = 'Home'
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos.")
                else:
                    st.error("Usuário ou senha incorretos.")
            else:
                # Fallback offline
                if user == "admin" and password == "admin":
                    st.session_state['logado'] = True
                    st.session_state['usuario'] = "Administrador (Offline)"
                    # Armazena o username para consistência
                    st.session_state['username'] = "admin"
                    st.session_state['role'] = "admin"
                    session_id = auth.create_session("admin", "admin", "Administrador (Offline)")
                    st.query_params["session_id"] = session_id
                    st.session_state.page = 'Home'
                    st.rerun()
                else:
                    st.error("Login offline: use admin/admin")
        
        st.divider()
        if st.button("Não tem uma conta? Registre-se"):
            st.session_state.page = 'register'
            st.rerun()