"""Aba Portal iSeduc: planejamento, registro de aulas e notas.

Separa a responsabilidade de lidar com o Portal iSeduc (onde se registra aula
com plano, frequência e atividades, e onde se lançam as notas) das funções do
portal do aluno.

Arquitetura (híbrida):
- Dados de leitura vêm do Supabase.
- Ações do robô (registrar no portal, raspagem) usam a API local (`services.portal_api`),
  disponível apenas quando a automação está rodando na máquina.
"""

import streamlit as st

from services import database as db
from services import portal_api

SECOES = ["📝 Planejar aulas", "🚀 Registrar no Portal", "📊 Notas"]


def _count(table: str, **filters):
    if not db.is_db_connected():
        return None
    try:
        q = db.supabase.table(table).select("id", count="exact").limit(0)
        for key, value in filters.items():
            q = q.eq(key, value)
        return q.execute().count
    except Exception:
        return None


def _select(table: str, columns: str, order_by: str = None, desc: bool = False, limit: int = 20, **filters):
    if not db.is_db_connected():
        return []
    try:
        q = db.supabase.table(table).select(columns)
        for key, value in filters.items():
            q = q.eq(key, value)
        if order_by:
            q = q.order(order_by, desc=desc)
        return q.limit(limit).execute().data or []
    except Exception:
        return []


def _api_badge(online: bool, detail: str):
    if online:
        st.success(f"🤖 Automação local: **{detail}** (`{portal_api.get_api_url()}`)")
    else:
        st.warning(
            f"🤖 Automação local: **{detail}** (`{portal_api.get_api_url()}`). "
            "As ações do robô ficam indisponíveis até a API local (`apps/api`) estar rodando."
        )


def _planejar(online: bool):
    st.subheader("📝 Planejar aulas")
    st.caption("Fila de aulas planejadas para registrar no portal, por turma e disciplina.")

    pendentes = _count("planejamento", status="pendente")
    registradas = _count("planejamento", status="registrada")
    c1, c2, c3 = st.columns(3)
    c1.metric("Pendentes", pendentes if pendentes is not None else "—")
    c2.metric("Registradas", registradas if registradas is not None else "—")
    c3.metric("API local", "online" if online else "offline")

    st.divider()
    st.markdown("**Próximas aulas a planejar**")
    rows = _select(
        "planejamento",
        "data_planejada,horario,turma,disciplina,numero_aula,status",
        order_by="data_planejada",
        limit=25,
    )
    if rows:
        st.dataframe(rows, width="stretch", hide_index=True)
    else:
        st.info("Nenhum plano na fila (ou banco indisponível).")

    st.divider()
    st.info("🚧 Em construção: geração e edição de planos de aula serão movidas para cá.")


def _registrar(online: bool):
    st.subheader("🚀 Registrar no Portal")
    st.caption("Acompanhamento dos registros de aula feitos no Portal iSeduc pelo robô.")

    total = _count("historico_aulas")
    c1, c2 = st.columns(2)
    c1.metric("Aulas no histórico", total if total is not None else "—")
    c2.metric("API local", "online" if online else "offline")

    st.divider()
    st.markdown("**Registros mais recentes**")
    rows = _select(
        "historico_aulas",
        "data_aula,horario,turma,disciplina,status",
        order_by="created_at",
        desc=True,
        limit=15,
    )
    if rows:
        st.dataframe(rows, width="stretch", hide_index=True)
    else:
        st.info("Nenhum registro encontrado (ou banco indisponível).")

    st.divider()
    st.info("🚧 Em construção: disparo e acompanhamento do registro (raspagem/registrar_lote) entram aqui.")


def _notas(online: bool):
    st.subheader("📊 Notas")
    st.caption("Lançamento e consulta das notas das avaliações no Portal iSeduc.")

    avaliacoes = _count("assessments")
    submissoes = _count("student_assessments")
    c1, c2, c3 = st.columns(3)
    c1.metric("Avaliações", avaliacoes if avaliacoes is not None else "—")
    c2.metric("Submissões", submissoes if submissoes is not None else "—")
    c3.metric("API local", "online" if online else "offline")

    st.divider()
    st.markdown("**Avaliações cadastradas**")
    rows = _select("assessments", "subject_id,type,title,created_at", order_by="created_at", desc=True, limit=20)
    if rows:
        st.dataframe(rows, width="stretch", hide_index=True)
    else:
        st.info("Nenhuma avaliação encontrada (ou banco indisponível).")

    st.divider()
    st.info("🚧 Em construção: lançamento/sincronização de notas no portal entram aqui.")


def show_page():
    st.header("🌐 Portal iSeduc")
    st.caption("Planejamento, registro de aulas e notas — separado do portal do aluno.")

    online, detail = portal_api.status()
    _api_badge(online, detail)
    st.divider()

    try:
        secao = st.segmented_control("Seção", SECOES, default=SECOES[0])
    except Exception:
        secao = st.radio("Seção", SECOES, horizontal=True)
    secao = secao or SECOES[0]

    if secao == SECOES[0]:
        _planejar(online)
    elif secao == SECOES[1]:
        _registrar(online)
    else:
        _notas(online)
