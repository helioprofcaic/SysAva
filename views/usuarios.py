"""Gestão de contas (professores e administradores).

Aba dedicada para adicionar contas, bloquear/reativar o acesso ao portal,
redefinir senha e remover cadastros. O bloqueio usa `app_users.status =
'blocked'`; os flags de frequência (`is_active`/`is_portal`) não são alterados.
"""

import streamlit as st
import pandas as pd

from services import database as db
from services import auth

ROLE_LABELS = {
    "student": "Aluno",
    "teacher": "Professor",
    "admin": "Administrador",
}


def _label_role(role: str) -> str:
    return ROLE_LABELS.get((role or "").strip().lower(), role or "-")


def _status_label(user: dict) -> str:
    return "Desativado" if db.is_user_blocked(user) else "Ativo"


def _pode_gerenciar(meu_role: str, alvo_role: str) -> bool:
    if meu_role == "admin":
        return True
    if meu_role == "teacher":
        return (alvo_role or "").strip().lower() == "student"
    return False


def _admins_ativos(users) -> int:
    return sum(
        1 for u in users
        if (u.get("role") or "").strip().lower() == "admin"
        and not db.is_user_blocked(u)
    )


def _mapa_turmas(users) -> dict:
    """username -> nome da turma (usa o cache de get_students_by_class)."""
    mapa = {}
    try:
        for classe in db.get_classes():
            for aluno in db.get_students_by_class(classe["id"]):
                mapa[aluno.get("username")] = classe.get("name") or ""
    except Exception:
        pass
    return mapa


def _turma_label(user, turmas) -> str:
    turma = turmas.get((user or {}).get("username")) or ""
    if turma:
        return turma
    if (user or {}).get("role") == "student":
        return "Sem turma"
    return "-"


def _flash():
    msg = st.session_state.pop("usuarios_flash", None)
    if not msg:
        return
    tipo, texto = msg
    if tipo == "ok":
        st.success(texto)
    elif tipo == "erro":
        st.error(texto)
    else:
        st.warning(texto)


def _definir_flash(tipo: str, texto: str):
    st.session_state["usuarios_flash"] = (tipo, texto)


def _registrar_auditoria(acao: str, username: str, name: str, role: str):
    try:
        from services import audit_log
        audit_log.registrar(
            acao,
            username=username,
            name=name,
            role=role,
            pagina="Gestão de Usuários",
        )
    except Exception:
        pass


def _mostrar_formulario(meu_role: str, users, classes):
    if meu_role == "teacher":
        st.caption(
            "Professor cria apenas contas de aluno. Contas de professor e "
            "administrador são gerenciadas por um administrador."
        )
        roles = ["student"]
    else:
        roles = ["student", "teacher", "admin"]

    ids_turmas = {"Sem turma": None}
    for c in classes:
        nome_classe = (c.get("name") or "").strip()
        if nome_classe and nome_classe not in ids_turmas:
            ids_turmas[nome_classe] = c.get("id")
    nomes_turmas = ["Sem turma"] + sorted(k for k in ids_turmas if k != "Sem turma")

    with st.form("usuarios_nova_conta", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            nome = st.text_input("Nome completo", key="usuarios_novo_nome")
            usuario = st.text_input("Usuário (login)", key="usuarios_novo_usuario")
            ra = st.text_input("RA", key="usuarios_novo_ra")
        with c2:
            role = st.selectbox(
                "Função", roles,
                format_func=_label_role,
                key="usuarios_novo_role",
            )
            turma = st.selectbox(
                "Turma (opcional, para alunos)",
                nomes_turmas,
                key="usuarios_novo_turma",
            )
            senha = st.text_input("Senha", type="password", key="usuarios_novo_senha")
            senha2 = st.text_input("Confirmar senha", type="password", key="usuarios_novo_senha2")

        enviar = st.form_submit_button("Cadastrar conta", type="primary")

    if not enviar:
        return

    nome = (nome or "").strip()
    usuario = (usuario or "").strip()
    ra = (ra or "").strip()

    if not nome or not usuario or not ra or not senha:
        st.warning("Preencha nome, usuário, RA e senha.")
        return
    if any(ch.isspace() for ch in usuario):
        st.error("O usuário (login) não pode conter espaços.")
        return
    if senha != senha2:
        st.error("As senhas não coincidem.")
        return
    if len(senha) < 6:
        st.error("A senha precisa ter pelo menos 6 caracteres.")
        return
    if role not in roles:
        st.error("Você não tem permissão para criar esta função.")
        return

    existentes = {(u.get("username") or "").strip().lower() for u in users}
    if usuario.lower() in existentes:
        st.error(f"O usuário {usuario} já existe.")
        return
    if any((u.get("ra") or "").strip() == ra for u in users):
        st.error(f"O RA {ra} já está cadastrado.")
        return

    hashed = auth.hash_password(senha)
    _, erro = db.create_user(usuario, hashed, nome, ra, role=role)
    if erro:
        st.error(f"Não foi possível criar a conta: {erro}")
        return

    if role == "student":
        turma_id = ids_turmas.get(turma)
        if turma_id:
            _, erro_turma = db.enroll_student_in_class(usuario, turma_id)
            if erro_turma:
                _definir_flash(
                    "aviso",
                    f"Conta {usuario} criada, mas não foi possível matricular na turma: {erro_turma}",
                )
                st.rerun()
    _definir_flash("ok", f"Conta {nome} ({usuario}) criada.")
    st.rerun()


def _mostrar_acoes(meu_username: str, meu_role: str, users, visiveis, turmas):
    st.subheader("Gerenciar conta")
    if not visiveis:
        st.info("Nenhuma conta disponível para gerenciar.")
        return

    opcoes = []
    por_rotulo = {}
    for u in sorted(visiveis, key=lambda x: ((x.get("name") or "").lower(), x.get("username") or "")):
        rotulo = f"{u.get('name') or '-'} - {u.get('username') or '-'} ({_label_role(u.get('role'))})"
        if db.is_user_blocked(u):
            rotulo += " [desativado]"
        opcoes.append(rotulo)
        por_rotulo[rotulo] = u

    escolha = st.selectbox("Selecione a conta", opcoes, key="usuarios_acao_conta")
    alvo = por_rotulo.get(escolha) or {}
    username = (alvo.get("username") or "").strip()
    alvo_role = (alvo.get("role") or "").strip().lower()
    blocked = db.is_user_blocked(alvo)

    c1, c2, c3 = st.columns(3)
    c1.metric("Função", _label_role(alvo_role))
    c2.metric("Acesso", "Desativado" if blocked else "Ativo")
    c3.metric("Turma", _turma_label(alvo, turmas))

    if username == meu_username:
        st.info("Esta é a sua conta. Por segurança, ela não pode ser desativada nem removida por aqui.")
        return
    if not _pode_gerenciar(meu_role, alvo_role):
        st.warning("Seu perfil pode gerenciar apenas contas de aluno.")
        return

    ultimo_admin = (
        alvo_role == "admin"
        and not blocked
        and _admins_ativos(users) <= 1
    )
    if ultimo_admin:
        st.warning(
            "Esta é a última conta de administrador ativa. Crie ou reative outro "
            "administrador antes de desativar/remover esta conta."
        )

    b1, b2 = st.columns(2)
    if blocked:
        if b1.button("Reativar acesso", type="primary", key=f"usuarios_reativar_{username}"):
            _, erro = db.set_user_access_blocked(username, False)
            if erro:
                st.error(f"Não foi possível reativar: {erro}")
            else:
                auth.allow_user_sessions(username)
                _registrar_auditoria(
                    "Usuário reativado", meu_username,
                    st.session_state.get("usuario", ""), meu_role,
                )
                _definir_flash("ok", f"Acesso de {username} reativado.")
                st.rerun()
    else:
        if b1.button("Desativar acesso", disabled=ultimo_admin, key=f"usuarios_desativar_{username}"):
            _, erro = db.set_user_access_blocked(username, True)
            if erro:
                st.error(f"Não foi possível desativar: {erro}")
            else:
                auth.logout_user_sessions(username)
                _registrar_auditoria(
                    "Usuário desativado", meu_username,
                    st.session_state.get("usuario", ""), meu_role,
                )
                _definir_flash("ok", f"Acesso de {username} desativado. A conta não consegue mais entrar no portal.")
                st.rerun()

    b2.caption("Desativar bloqueia o login no portal, sem alterar a frequência.")

    with st.expander("Redefinir senha"):
        with st.form(f"usuarios_reset_{username}"):
            p1 = st.text_input("Nova senha", type="password", key=f"usuarios_reset_p1_{username}")
            p2 = st.text_input("Confirmar nova senha", type="password", key=f"usuarios_reset_p2_{username}")
            trocar = st.form_submit_button("Salvar nova senha")
        if trocar:
            if not p1 or len(p1) < 6:
                st.error("A senha precisa ter pelo menos 6 caracteres.")
            elif p1 != p2:
                st.error("As senhas não coincidem.")
            else:
                _, erro = db.update_user_password(username, auth.hash_password(p1))
                if erro:
                    st.error(f"Não foi possível trocar a senha: {erro}")
                else:
                    _registrar_auditoria(
                        "Senha redefinida", meu_username,
                        st.session_state.get("usuario", ""), meu_role,
                    )
                    _definir_flash("ok", f"Senha de {username} atualizada.")
                    st.rerun()

    with st.expander("Remover conta"):
        st.warning(
            "A remoção apaga o cadastro e a matrícula. O histórico e as notas já "
            "registradas permanecem. O RA fica livre para um novo cadastro."
        )
        confirmar = st.checkbox(
            f"Confirmo remover permanentemente {username}",
            key=f"usuarios_remover_conf_{username}",
        )
        if st.button(
            "Remover conta",
            disabled=(not confirmar) or ultimo_admin,
            key=f"usuarios_remover_{username}",
        ):
            _, erro = db.delete_user(username)
            if erro:
                st.error(f"Não foi possível remover: {erro}")
            else:
                auth.logout_user_sessions(username)
                _registrar_auditoria(
                    "Usuário removido", meu_username,
                    st.session_state.get("usuario", ""), meu_role,
                )
                _definir_flash("ok", f"Conta {username} removida.")
                st.rerun()


def show_page():
    st.header("Gestão de Usuários")

    meu_username = (st.session_state.get("username") or "").strip()
    meu_role = (st.session_state.get("role") or "student").strip().lower()

    if meu_role not in ("admin", "teacher"):
        st.error("Acesso restrito a professores e administradores.")
        return

    st.caption(
        "Adicione contas, desative o acesso ao portal e remova cadastros. "
        "A frequência (Falta/Inativo) continua sendo gerenciada em Admin > Usuários."
    )
    _flash()

    if not db.is_db_connected():
        st.warning("Banco de dados desconectado. A gestão de contas precisa do Supabase.")
        return

    users = db.get_all_users()
    turmas = _mapa_turmas(users)

    if meu_role == "teacher":
        visiveis = [u for u in users if (u.get("role") or "").strip().lower() == "student"]
    else:
        visiveis = list(users)

    total = len(visiveis)
    ativos = sum(1 for u in visiveis if not db.is_user_blocked(u))
    desativados = total - ativos
    alunos = sum(1 for u in visiveis if (u.get("role") or "").strip().lower() == "student")
    equipe = sum(1 for u in visiveis if (u.get("role") or "").strip().lower() in ("teacher", "admin"))

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Contas", total)
    m2.metric("Ativas", ativos)
    m3.metric("Desativadas", desativados)
    m4.metric("Alunos", alunos)
    if meu_role == "admin":
        st.caption(f"Equipe (professores + administradores): {equipe}")

    aba_contas, aba_nova = st.tabs(["Contas cadastradas", "Adicionar conta"])

    with aba_contas:
        f1, f2, f3 = st.columns([2, 1, 1])
        busca = f1.text_input("Buscar por nome, usuário ou RA", key="usuarios_busca")
        filtro_role = f2.selectbox(
            "Função", ["Todas", "Alunos", "Professores", "Administradores"],
            key="usuarios_filtro_role",
        )
        filtro_status = f3.selectbox(
            "Acesso", ["Todos", "Ativos", "Desativados"], key="usuarios_filtro_status",
        )

        filtro_turma = "Todas"
        if meu_role == "admin" or filtro_role == "Alunos":
            nomes_turmas = ["Todas", "Sem turma"] + sorted(set(v for v in turmas.values() if v))
            filtro_turma = st.selectbox(
                "Turma", nomes_turmas, key="usuarios_filtro_turma")

        role_alvo = {
            "Alunos": "student",
            "Professores": "teacher",
            "Administradores": "admin",
        }.get(filtro_role)

        def _bate(u):
            if role_alvo and (u.get("role") or "").strip().lower() != role_alvo:
                return False
            if filtro_status == "Ativos" and db.is_user_blocked(u):
                return False
            if filtro_status == "Desativados" and not db.is_user_blocked(u):
                return False
            if filtro_turma != "Todas":
                turma_u = turmas.get(u.get("username")) or ""
                if filtro_turma == "Sem turma":
                    if turma_u:
                        return False
                elif turma_u != filtro_turma:
                    return False
            if busca:
                alvo = busca.strip().lower()
                texto = " ".join([
                    str(u.get("name") or ""), str(u.get("username") or ""),
                    str(u.get("ra") or ""),
                ]).lower()
                if alvo not in texto:
                    return False
            return True

        lista = [u for u in visiveis if _bate(u)]
        lista.sort(key=lambda u: ((u.get("name") or "").lower(), u.get("username") or ""))

        if lista:
            df = pd.DataFrame([
                {
                    "Nome": u.get("name") or "",
                    "Usuário": u.get("username") or "",
                    "RA": str(u.get("ra") or ""),
                    "Função": _label_role(u.get("role")),
                    "Turma": _turma_label(u, turmas),
                    "Acesso": _status_label(u),
                }
                for u in lista
            ])
            st.dataframe(
                df,
                hide_index=True,
                width="stretch",
                column_config={
                    "Nome": st.column_config.TextColumn(width="large"),
                    "Usuário": st.column_config.TextColumn(width="medium"),
                    "RA": st.column_config.TextColumn(width="medium"),
                    "Função": st.column_config.TextColumn(width="small"),
                    "Turma": st.column_config.TextColumn(width="medium"),
                    "Acesso": st.column_config.TextColumn(width="small"),
                },
            )
            st.caption(f"{len(lista)} conta(s) exibida(s).")
        else:
            st.info("Nenhuma conta encontrada com os filtros selecionados.")

        st.divider()
        _mostrar_acoes(meu_username, meu_role, users, lista, turmas)

    with aba_nova:
        _mostrar_formulario(meu_role, users, db.get_classes())
