"""Aba Portal iSeduc: planejamento, registro de aulas e notas.

Separa a responsabilidade de lidar com o Portal iSeduc (onde se registra aula
com plano, frequência e atividades, e onde se lançam as notas) das funções do
portal do aluno.

Arquitetura (híbrida):
- Dados de leitura/visão geral vêm do Supabase.
- As ações que dependem do ambiente local (gerar planos, registrar, raspar,
  editar grade, configurações) usam a API local (`services.portal_api`),
  disponível apenas quando a automação está rodando na máquina.

Os recursos espelham o app `apps/planejamento_registro` (porta 8510), agora
acessíveis de dentro do portal principal.
"""

import pandas as pd
import streamlit as st

from services import database as db
from services import portal_api

SECOES = [
    "📝 Planejar aulas",
    "🚀 Registrar no Portal",
    "🔄 Sincronizar",
    "📊 Painel / Consolidadas",
    "📊 Notas",
    "⚙️ Config",
]


# ===========================================================================
# Helpers de API / Supabase
# ===========================================================================
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


def _select(table: str, columns: str, order_by: str = None, desc: bool = False,
            limit: int = 20, **filters):
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
            "As ações do robô ficam indisponíveis até a API local "
            "(`apps/api/api_service.py`, porta 8002) estar rodando."
        )


def _erro_api(err, contexto="a operação"):
    st.error(f"Falha ao executar {contexto}: {err}")
    st.caption("Confirme que a API local está rodando (`python apps/api/api_service.py`).")


# ===========================================================================
# Contexto (turma × disciplina)
# ===========================================================================
@st.cache_data(ttl=60, show_spinner=False)
def _carregar_turmas():
    dados, _err = portal_api.turmas_completo()
    if isinstance(dados, dict) and dados.get("turmas"):
        return dados["turmas"]
    try:
        return [{"id": c["id"], "name": c["name"], "code": c["code"]}
                for c in db.get_classes()]
    except Exception:
        return []


@st.cache_data(ttl=60, show_spinner=False)
def _carregar_disciplinas(class_id, class_code):
    dados, _err = portal_api.subjects_for_class(class_id)
    if isinstance(dados, list) and dados:
        return dados
    try:
        return [{"id": s["id"], "name": s["name"], "max_hours": s.get("max_hours"),
                 "duration_type": s.get("duration_type"), "is_active": s.get("is_active")}
                for s in db.get_subjects_for_class(int(class_id))]
    except Exception:
        return []


def _sidebar_contexto():
    with st.sidebar:
        st.divider()
        st.markdown("### 🌐 Portal iSeduc")
        turmas = _carregar_turmas()
        if not turmas:
            st.error("Nenhuma turma encontrada (API local offline e Supabase indisponível).")
            return None, None
        nomes = [f"{t['name']} ({t['code']})" for t in turmas]
        sel = st.selectbox("Turma (contexto)", nomes, key="portal_turma")
        turma = turmas[nomes.index(sel)]

        subs = _carregar_disciplinas(turma["id"], turma["code"])
        smap = {s["name"]: s for s in subs}
        if smap:
            ssel = st.selectbox("Disciplina (contexto)", list(smap.keys()),
                                key="portal_subject")
            subject = smap[ssel]
        else:
            subject = None
            st.caption("Sem disciplinas para esta turma.")
    return turma, subject


# ===========================================================================
# 📝 Planejar aulas
# ===========================================================================
def _metricas_contexto(turma, subject, online):
    if online and subject:
        dados, _err = portal_api.painel(turma["code"], subject["id"])
        if isinstance(dados, dict):
            return (dados.get("planejadas"), dados.get("registradas"),
                    dados.get("carga"), dados.get("faltantes"), dados.get("ultima_data"))
    pend = _count("planejamento", status="pendente")
    reg = _count("planejamento", status="registrada")
    return (pend, reg, None, None, None)


def _planejar(turma, subject, online):
    st.subheader("📝 Planejar aulas")
    st.caption("Fila de aulas planejadas para registrar no portal, por turma e disciplina.")

    plan, reg, carga, falt, ultima = _metricas_contexto(turma, subject, online)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pendentes (fila)", plan if plan is not None else "—")
    c2.metric("Registradas (portal)", reg if reg is not None else "—")
    c3.metric("Carga prevista", f"{carga} aulas" if carga else "—")
    c4.metric("Faltantes", falt if falt is not None else "—")
    if ultima:
        st.info(f"📅 Última aula registrada no portal: **{ultima}**")

    st.divider()
    st.markdown("**Próximas aulas a planejar**")
    fila = _fila_contexto(turma, subject, online)
    if fila:
        st.dataframe(pd.DataFrame(fila), width="stretch", hide_index=True)
    else:
        st.info("Nenhum plano na fila (ou API/banco indisponível).")

    if not online:
        st.divider()
        st.info("🚧 Geração e edição de planos exigem a API local online.")
        return

    st.divider()
    _gerar_planos_ui(turma, subject)
    st.divider()
    _gerenciar_planos_ui(turma, subject)


def _fila_contexto(turma, subject, online):
    rows = []
    if online:
        dados, _err = portal_api.planejamento_pendente()
        if isinstance(dados, list):
            ids = set(_disc_ids(turma["code"], subject["id"])) if subject else set()
            for r in dados:
                if str(r.get("turma_id")) != str(turma["code"]):
                    continue
                if subject and str(r.get("disciplina_id")) not in ids:
                    continue
                rows.append({
                    "data_planejada": r.get("data_planejada"),
                    "horario": r.get("horario"),
                    "numero_aula": r.get("numero_aula"),
                    "disciplina": subject["name"] if subject else r.get("disciplina"),
                    "status": r.get("status"),
                })
            return rows
    return _select(
        "planejamento",
        "data_planejada,horario,turma,disciplina,numero_aula,status",
        order_by="data_planejada",
        limit=50,
    )


def _disc_ids(turma_code, disciplina_id):
    try:
        from apps.planejamento_registro.core import banco as core_banco
        return core_banco.disc_ids(turma_code, disciplina_id)
    except Exception:
        return [str(disciplina_id)]


def _gerar_planos_ui(turma, subject):
    st.markdown("#### ⚙️ Gerar planos (grade/calendário)")
    if not subject:
        st.info("Selecione uma disciplina no contexto.")
        return
    c1, c2, c3 = st.columns(3)
    with c1:
        out_dir = st.radio("Destino:", ["pendentes", "prontas"], key="p_gerar_out")
    with c2:
        force = st.checkbox("Sobrescrever existentes", value=False, key="p_gerar_force")
    with c3:
        st.write("")
        gerar = st.button("🚀 Gerar planos", type="primary", width="stretch",
                          key="p_btn_gerar")

    c4, c5, c6, c7 = st.columns(4)
    estrategia = c4.text_input("Estratégia da aula",
                               value="Aula expositiva e prática.", key="p_estrategia")
    range_on = c5.checkbox("Limitar intervalo", value=False, key="p_range_on")
    a_min = c6.number_input("De (aula nº)", min_value=1, value=1, key="p_aula_min",
                            disabled=not range_on)
    a_max = c7.number_input("Até (aula nº)", min_value=1, value=40, key="p_aula_max",
                            disabled=not range_on)

    if gerar:
        with st.spinner("Gerando planos..."):
            dados, err = portal_api.gerar_planos(
                output_dir=out_dir,
                force_overwrite=force,
                turma_id=turma["code"],
                disciplina_id=subject["id"],
                estrategia=estrategia or None,
                aula_min=(int(a_min) if range_on else None),
                aula_max=(int(a_max) if range_on else None),
            )
        if err:
            _erro_api(err, "a geração de planos")
        elif isinstance(dados, dict):
            n = dados.get("generated", 0)
            if n:
                st.success(f"✅ {n} plano(s) gerado(s) em `{dados.get('path', out_dir)}`.")
            else:
                st.warning("Nenhum plano gerado. Verifique janela/calendário, "
                           "data de corte e se o slot já está ocupado.")
            st.caption(f"Frequência: {dados.get('com_frequencia', 0)} plano(s) com lista "
                       f"• pulados: {dados.get('skipped', 0)} "
                       f"• antigos removidos: {dados.get('deleted_old', 0)}")
            st.cache_data.clear()
        else:
            st.info(str(dados))


def _gerenciar_planos_ui(turma, subject):
    st.markdown("#### 📄 Planos (.txt)")
    if not subject:
        st.info("Selecione uma disciplina no contexto.")
        return
    c1, c2 = st.columns([0.4, 0.6])
    with c1:
        pasta = st.radio("Pasta:", ["pendentes", "prontas", "registradas"],
                         horizontal=True, key="p_planos_pasta")
    dados, err = portal_api.listar_aulas(pasta, turma["code"], subject["id"])
    if err:
        _erro_api(err, "a listagem de planos")
        return
    aulas = (dados or {}).get("aulas", [])
    c2.caption(f"{len(aulas)} arquivo(s) em `aulas/{pasta}/`.")
    if not aulas:
        st.info("Nenhum plano nesta pasta com o contexto atual.")
        return

    opcoes = {a["arquivo"]: a for a in aulas}
    sel = st.selectbox("Visualizar plano:", list(opcoes.keys()), key="p_planos_sel")
    info = opcoes[sel]
    if info.get("feriado"):
        st.warning(f"⚠️ **Feriado/recesso**: `{info.get('data')}` — {info['feriado']}. "
                   "O registro no portal está bloqueado para esta data.")
    conteudo, cerr = portal_api.ler_plano(sel)
    if cerr:
        _erro_api(cerr, "a leitura do plano")
    else:
        st.text_area("Conteúdo", conteudo or "", height=300, key="p_planos_conteudo")

    st.download_button("📥 Baixar este plano (.txt)",
                       data=(conteudo or "").encode("utf-8"),
                       file_name=sel, mime="text/plain", width="stretch",
                       key="p_dl_plano")

    with st.expander("🗑️ Excluir este plano"):
        st.caption("Remove o arquivo `.txt` e a linha correspondente em `planejamento`.")
        conf = st.checkbox("Confirmo a exclusão deste plano", key="p_del_conf")
        if st.button("🗑️ Excluir este plano", disabled=not conf, width="stretch",
                     key="p_btn_del"):
            resp, err = portal_api.excluir_plano(pasta, sel)
            if err:
                _erro_api(err, "a exclusão")
            else:
                st.success(f"🗑️ Removido: arquivo={'sim' if resp.get('arquivo_removido') else 'não'} "
                           f"• planejamento={resp.get('planejamento_removido', 0)} linha(s).")
                st.cache_data.clear()
                st.rerun()

    with st.expander("🗑️ Excluir vários planos"):
        sel_lote = st.multiselect("Selecione os planos:", list(opcoes.keys()),
                                  key="p_del_lote_sel")
        conf_lote = st.checkbox("Confirmo a exclusão dos selecionados", key="p_del_lote_conf")
        if st.button("🗑️ Excluir selecionados", type="primary",
                     disabled=not (sel_lote and conf_lote), key="p_btn_del_lote"):
            n_arq = n_linhas = 0
            for arq in sel_lote:
                resp, err = portal_api.excluir_plano(pasta, arq)
                if not err and resp:
                    n_arq += 1 if resp.get("arquivo_removido") else 0
                    n_linhas += int(resp.get("planejamento_removido", 0) or 0)
            st.success(f"🗑️ {n_arq} arquivo(s) e {n_linhas} linha(s) removidos.")
            st.cache_data.clear()
            st.rerun()


# ===========================================================================
# 🚀 Registrar no Portal
# ===========================================================================
def _registrar(turma, subject, online):
    st.subheader("🚀 Registrar no Portal")
    st.caption("Dispara o robô de registro das aulas prontas e acompanha o progresso.")

    total = _count("historico_aulas")
    c1, c2 = st.columns(2)
    c1.metric("Aulas no histórico", total if total is not None else "—")
    c2.metric("API local", "online" if online else "offline")

    if not online:
        st.divider()
        st.markdown("**Registros mais recentes**")
        rows = _select("historico_aulas", "data_aula,horario,turma,disciplina,status",
                       order_by="created_at", desc=True, limit=15)
        if rows:
            st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
        else:
            st.info("Nenhum registro encontrado (ou banco indisponível).")
        st.divider()
        st.info("🚧 O disparo e o acompanhamento do registro exigem a API local online.")
        return

    st.divider()
    st.markdown("**Planos prontos para registrar**")
    dados, err = portal_api.listar_aulas("prontas", turma["code"], subject["id"] if subject else "")
    if err:
        _erro_api(err, "a listagem de planos prontos")
        return
    prontas = (dados or {}).get("aulas", [])
    bloqueadas = [a for a in prontas if a.get("feriado")]
    livres = [a for a in prontas if not a.get("feriado")]
    if bloqueadas:
        st.warning("⚠️ " + f"{len(bloqueadas)} plano(s) em data de feriado — registro "
                   "bloqueado: " + ", ".join(f"`{a['arquivo']}`" for a in bloqueadas))
    if not prontas:
        st.info("Nenhum plano em `aulas/prontas/` para o contexto atual.")
    opts = [a["arquivo"] for a in livres]
    selecionados = st.multiselect("Planos prontos:", opts, key="p_reg_sel")
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("▶️ Registrar selecionados", type="primary", width="stretch",
                     disabled=not selecionados, key="p_reg_sel_btn"):
            resp, err = portal_api.registrar_lote(files=selecionados)
            (st.success if not err else st.error)(
                resp.get("message") if isinstance(resp, dict) else err)
    with b2:
        if st.button("▶️ Registrar TODOS os prontos", width="stretch",
                     disabled=not livres, key="p_reg_all_btn"):
            resp, err = portal_api.registrar_lote(files=[a["arquivo"] for a in livres])
            (st.success if not err else st.error)(
                resp.get("message") if isinstance(resp, dict) else err)
    with b3:
        if st.button("🔄 Atualizar status", width="stretch", key="p_reg_status_btn"):
            st.rerun()

    _progresso_registro()
    st.caption("Pré-requisitos: `pip install selenium webdriver-manager` e "
               "`data/credentials.json`.")


def _progresso_registro():
    st.markdown("#### 📈 Progresso do robô")
    s, _err = portal_api.registrar_status()
    if not isinstance(s, dict) or s.get("status") in (None, "parado"):
        st.caption("Sem registro em andamento. O robô escreve em "
                   "`data/logs/registro_status.json`.")
        return
    total = int(s.get("total", 0) or 0)
    proc = int(s.get("processados", 0) or 0)
    st.progress((proc / total) if total else 0.0)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Status", s.get("status", "-"))
    c2.metric("Processados", f"{proc}/{total}")
    c3.metric("Sucessos", s.get("sucessos", 0))
    c4.metric("Falhas", s.get("falhas", 0))
    if s.get("aula_atual"):
        st.caption(f"Aula atual: `{s['aula_atual']}`")
    det = s.get("detalhes") or []
    if det:
        st.dataframe(pd.DataFrame(det), width="stretch", hide_index=True)


# ===========================================================================
# 🔄 Sincronizar (raspagem)
# ===========================================================================
def _sincronizar(turma, subject, online):
    st.subheader("🔄 Sincronizar (raspagem do portal)")
    st.caption("Lê o portal iSeduc e reconcilia com o histórico local de aulas.")

    if not online:
        st.warning("A raspagem exige a API local online.")
        return

    modo = st.radio(
        "Escopo da raspagem:",
        ["🌐 Tudo (todas as turmas/disciplinas)", "🔎 Filtrar (turma × disciplina)"],
        horizontal=True, key="p_rasp_modo")
    filtrar = modo.startswith("🔎")
    turma_arg = disciplina_arg = None
    if filtrar:
        c_t, c_d = st.columns(2)
        turmas_opts = [t["name"] for t in _carregar_turmas()]
        default_turmas = [turma["name"]] if turma and turma["name"] in turmas_opts else []
        turmas_sel = c_t.multiselect(
            "Turmas (vazio = todas)", turmas_opts, default=default_turmas,
            key="p_rasp_turmas")
        disc_opts = ([s["name"] for s in _carregar_disciplinas(turma["id"], turma["code"])]
                     if turma else [])
        disc_sel = c_d.multiselect(
            "Disciplinas (vazio = todas)", disc_opts, default=[], key="p_rasp_discs",
            help="Disciplinas da turma do contexto. Com várias turmas selecionadas, "
                 "o filtro vale para todas.")
        turma_arg = ", ".join(turmas_sel) if turmas_sel else None
        disciplina_arg = ", ".join(disc_sel) if disc_sel else None
        if not turma_arg and not disciplina_arg:
            st.warning("Selecione ao menos uma turma ou disciplina, ou use o escopo **Tudo**.")
        st.caption("Raspagens filtradas não reconciliam o histórico "
                   "(a comparação ficaria parcial).")

    reconciliar = st.checkbox(
        "🧹 Reconciliar histórico", value=False, key="p_rasp_recon",
        disabled=filtrar,
        help="Apaga do histórico as linhas que o portal não mostra. Exige raspagem "
             "completa (sem filtro).")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 Sincronizar (raspagem)", type="primary", width="stretch",
                     key="p_rasp_btn"):
            resp, err = portal_api.raspagem_executar(
                turma_arg, disciplina_arg, reconciliar=(reconciliar and not filtrar))
            if err:
                _erro_api(err, "a raspagem")
            else:
                st.success((resp or {}).get("message", "Raspagem iniciada."))
    with c2:
        if st.button("🔄 Atualizar status/relatório", width="stretch", key="p_rasp_rel_btn"):
            st.rerun()

    st.divider()
    st.markdown("#### 📈 Status")
    s, err = portal_api.raspagem_status()
    if err:
        st.caption("Nenhuma raspagem executada ainda.")
    elif isinstance(s, dict):
        st.json(s.get("resumo") or s)

    st.markdown("#### 📄 Último relatório")
    rel, err = portal_api.raspagem_relatorio()
    if err or not isinstance(rel, dict):
        st.caption("Sem relatório de raspagem.")
        return
    st.caption(f"Gerado em {rel.get('timestamp', '—')}")
    st.json(rel.get("resumo") or {})
    rec = rel.get("reconciliacao") or {}
    if rec.get("removidos") and not rec.get("aplicado"):
        motivos = ", ".join(f"{v} {k}" for k, v in (rec.get("motivos") or {}).items()) or "órfãs"
        st.warning(f"🧹 {rec['removidos']} linha(s) do histórico não existem no portal "
                   f"({motivos}). Rode a raspagem com reconciliação pelo app 8510.")


# ===========================================================================
# 📊 Painel / Consolidadas
# ===========================================================================
def _painel_consolidadas(turma, subject, online):
    st.subheader("📊 Painel / Consolidadas")
    if not online:
        st.warning("As métricas consolidadas exigem a API local online.")
        return

    if subject:
        st.markdown("#### 🎯 Contexto atual")
        dados, _err = portal_api.painel(turma["code"], subject["id"])
        if isinstance(dados, dict):
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Carga prevista", f"{dados.get('carga', '—')} aulas")
            m2.metric("Registradas", dados.get("registradas", "—"))
            m3.metric("Planejadas", dados.get("planejadas", "—"))
            m4.metric("Faltantes", dados.get("faltantes", "—"))

    st.divider()
    st.markdown("#### 📈 Carga anual por turma × disciplina")
    dados, err = portal_api.consolidadas("")
    if err:
        _erro_api(err, "as consolidadas")
        return
    linhas = (dados or {}).get("linhas", [])
    if not linhas:
        st.info("Nenhuma disciplina encontrada.")
        return

    tot_carga = sum(d["carga"] for d in linhas)
    tot_reg = sum(d["registradas"] for d in linhas)
    tot_pront = sum(d["prontas"] for d in linhas)
    tot_pend = sum(d["pendentes"] for d in linhas)
    tot_falt = sum(d["faltantes"] for d in linhas)
    avanco = round(100 * tot_reg / tot_carga) if tot_carga else 0
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Disciplinas", len(linhas))
    c2.metric("Carga anual", f"{tot_carga} aulas")
    c3.metric("Registradas", tot_reg)
    c4.metric("Prontas + pendentes", tot_pront + tot_pend)
    c5.metric("Faltantes", tot_falt)
    st.progress(min(100, avanco), text=f"Avanço anual: **{avanco}%** da carga registrada")

    filtro = st.multiselect("Filtrar por turma:", sorted({d["turma"] for d in linhas}),
                            key="p_cons_turmas")
    base = [d for d in linhas if not filtro or d["turma"] in filtro]

    fluxo = []
    for d in base:
        disc = f"{d['disciplina']} ({d['turma_curta']})"
        for etapa, qtd in (("Registradas", d["registradas"]), ("Prontas", d["prontas"]),
                           ("Pendentes", d["pendentes"]), ("Faltantes", d["faltantes"])):
            fluxo.append({"Disciplina": disc, "Etapa": etapa, "Aulas": qtd})
    if fluxo:
        st.bar_chart(pd.DataFrame(fluxo), x="Disciplina", y="Aulas", color="Etapa",
                     horizontal=True, stack=True, height=420)

    tabela = [{
        "Turma": d["turma_curta"], "Disciplina": d["disciplina"],
        "Carga": d["carga"], "Registradas": d["registradas"], "Prontas": d["prontas"],
        "Pendentes": d["pendentes"], "Fila": d["fila"], "Faltantes": d["faltantes"],
        "%": f"{round(100 * d['registradas'] / d['carga'])}%" if d["carga"] else "-",
    } for d in base]
    st.dataframe(pd.DataFrame(tabela), width="stretch", hide_index=True)


# ===========================================================================
# 📊 Notas (existente)
# ===========================================================================
def _notas(online):
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
    rows = _select("assessments", "subject_id,type,title,created_at",
                   order_by="created_at", desc=True, limit=20)
    if rows:
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    else:
        st.info("Nenhuma avaliação encontrada (ou banco indisponível).")


# ===========================================================================
# ⚙️ Config
# ===========================================================================
def _config_map():
    dados, _err = portal_api.config_all()
    mapa = {}
    if isinstance(dados, list):
        for row in dados:
            chave = row.get("key") or row.get("chave")
            mapa[chave] = row.get("value", row.get("valor"))
    return mapa


def _config(turma, subject, online):
    st.subheader("⚙️ Configurações e manutenção")
    if not online:
        st.warning("As configurações exigem a API local online.")
        return

    cfg = _config_map()

    st.markdown("#### 📅 Feriados (`master_config` → `feriados.json`)")
    fer, err = portal_api.feriados()
    linhas = []
    cats = (("feriados_e_datas_importantes", "Feriados"),
            ("ferias_e_recessos", "Férias/Recessos"),
            ("planejamento_e_formacao", "Planejamento/Formação"),
            ("exames", "Exames"))
    if err:
        _erro_api(err, "a leitura dos feriados")
    else:
        fer = (fer or {}).get("feriados", {})
        for cat, rotulo in cats:
            for item in fer.get(cat, []) or []:
                if not isinstance(item, dict):
                    continue
                if item.get("data"):
                    linhas.append({"Categoria": rotulo, "Início": item["data"],
                                   "Fim": item["data"],
                                   "Descrição": item.get("descricao", "")})
                elif item.get("inicio") and item.get("fim"):
                    linhas.append({"Categoria": rotulo, "Início": item["inicio"],
                                   "Fim": item["fim"],
                                   "Descrição": item.get("descricao", "")})
    if linhas:
        st.dataframe(pd.DataFrame(linhas), width="stretch", hide_index=True, height=240)
    else:
        st.caption("Calendário sem períodos cadastrados.")

    st.divider()
    st.markdown("#### 📅 Data de corte do planejamento")
    corte = str(cfg.get("data_corte_planejamento") or "2026-05-01").strip('"')
    st.caption(f"Atual: `{corte}` — o gerador ignora aulas anteriores a esta data.")
    nova = st.date_input("Nova data de corte", key="p_cfg_corte")
    if st.button("💾 Salvar data de corte", key="p_cfg_corte_btn"):
        resp, err = portal_api.config_set("data_corte_planejamento", nova.isoformat())
        if err:
            _erro_api(err, "salvar a data de corte")
        else:
            st.success(f"Data de corte atualizada para {nova.isoformat()}.")
            st.cache_data.clear()

    st.divider()
    st.markdown("#### 🚫 Bloquear sábados letivos (geração automática)")
    sab, _err = portal_api.sabados()
    n_sab = len((sab or {}).get("sabados_letivos", []))
    bloq_val = str(cfg.get("bloquear_sabados_letivos", "false")).strip().lower()
    bloq_atual = bloq_val in ("true", "1", "sim", "yes")
    st.caption(f"Atual: `{'bloqueado' if bloq_atual else 'liberado'}` — "
               f"{n_sab} sábado(s) configurado(s).")
    novo_bloq = st.checkbox("Bloquear sábados letivos na geração automática",
                            value=bloq_atual, key="p_cfg_bloq")
    if st.button("💾 Salvar bloqueio", key="p_cfg_bloq_btn"):
        resp, err = portal_api.config_set("bloquear_sabados_letivos", bool(novo_bloq))
        if err:
            _erro_api(err, "salvar o bloqueio")
        else:
            st.success(f"Bloqueio de sábados {'ativado' if novo_bloq else 'desativado'}.")
            st.cache_data.clear()

    st.divider()
    _grade_ui()

    st.divider()
    st.markdown("#### 🧹 Resetar tabela `planejamento`")
    st.warning("Ação destrutiva. Não remove os arquivos `.txt` em `aulas/`.")
    escopo = st.radio("Escopo:", ["Tudo", "Somente esta turma",
                                  "Somente esta turma/disciplina"], key="p_cfg_escopo")
    conf = st.checkbox("Confirmo que quero apagar", key="p_cfg_conf")
    if st.button("🗑️ Apagar planejamento", disabled=not conf, key="p_cfg_reset_btn"):
        if escopo == "Tudo":
            resp, err = portal_api.planejamento_reset()
        elif escopo == "Somente esta turma":
            resp, err = portal_api.planejamento_reset(turma["code"])
        else:
            resp, err = portal_api.planejamento_reset(
                turma["code"], subject["id"] if subject else None)
        if err:
            _erro_api(err, "o reset")
        else:
            st.success(f"{resp.get('removidos', 0)} registro(s) removido(s).")
            st.cache_data.clear()
            st.rerun()


def _grade_ui():
    st.markdown("#### 🗓️ Grade horária")
    dados, err = portal_api.grade_turmas()
    if err:
        _erro_api(err, "a leitura da grade")
        return
    turmas = (dados or {}).get("turmas", [])
    if not turmas:
        st.info("Nenhuma turma com grade horária.")
        return
    g_turma = st.selectbox("Turma da grade", turmas, key="p_grade_turma")
    detalhe, err = portal_api.grade_ver(g_turma)
    if err:
        _erro_api(err, "a leitura da grade")
        return
    grade = (detalhe or {}).get("grade", {})
    dias = (detalhe or {}).get("dias", [])
    horarios = sorted({h for d in grade.values() for h in d})
    df = pd.DataFrame({"Horário": horarios})
    for dia in dias:
        df[dia] = [grade.get(dia, {}).get(h, "") for h in horarios]
    st.dataframe(df, width="stretch", hide_index=True)

    with st.expander("✏️ Editar grade (grava nos 3 espelhos)"):
        op = st.radio("Operação", ["🔄 Mover slot", "➕ Adicionar slot", "➖ Remover slot"],
                      horizontal=True, key="p_grade_op")
        dias_com = [d for d in dias if grade.get(d)]
        if op == "🔄 Mover slot":
            if not dias_com:
                st.info("Turma sem slots na grade.")
                return
            c1, c2 = st.columns(2)
            dia_o = c1.selectbox("Dia origem", dias_com, key="p_g_dia_o")
            slot_o = c2.selectbox("Horário origem", sorted(grade[dia_o]), key="p_g_slot_o")
            c3, c4 = st.columns(2)
            dia_d = c3.selectbox("Dia destino", dias, key="p_g_dia_d")
            slot_d = c4.selectbox("Horário destino", horarios or ["07:10"], key="p_g_slot_d")
            conf = st.checkbox("Confirmo a alteração", key="p_g_conf1")
            if st.button("💾 Mover slot", disabled=not conf, key="p_g_btn1"):
                rel, err = portal_api.grade_editar("mover", g_turma, dia_origem=dia_o,
                                                   slot_origem=slot_o, dia_destino=dia_d,
                                                   slot_destino=slot_d)
                _resultado_grade(rel, err, g_turma)
        elif op == "➕ Adicionar slot":
            c5, c6 = st.columns(2)
            dia_a = c5.selectbox("Dia", dias, key="p_g_a_dia")
            slot_a = c6.selectbox("Horário", horarios or ["07:10"], key="p_g_a_slot")
            comp = st.text_input("Componente", key="p_g_a_comp")
            conf = st.checkbox("Confirmo a alteração", key="p_g_conf2")
            if st.button("💾 Adicionar slot", disabled=not (conf and comp.strip()),
                         key="p_g_btn2"):
                rel, err = portal_api.grade_editar("adicionar", g_turma, dia=dia_a,
                                                   slot=slot_a, componente=comp.strip())
                _resultado_grade(rel, err, g_turma)
        else:
            if not dias_com:
                st.info("Turma sem slots na grade.")
                return
            c7, c8 = st.columns(2)
            dia_r = c7.selectbox("Dia", dias_com, key="p_g_r_dia")
            slot_r = c8.selectbox("Horário", sorted(grade[dia_r]), key="p_g_r_slot")
            conf = st.checkbox("Confirmo a alteração", key="p_g_conf3")
            if st.button("➖ Remover slot", disabled=not conf, key="p_g_btn3"):
                rel, err = portal_api.grade_editar("remover", g_turma, dia=dia_r,
                                                   slot=slot_r)
                _resultado_grade(rel, err, g_turma)


def _resultado_grade(rel, err, turma):
    if err:
        _erro_api(err, "a edição da grade")
        return
    for linha in (rel or {}).get("ok", []):
        st.write(f"`{linha.get('Ação')}` — SQLite: {linha.get('SQLite')} • "
                 f"JSON: {linha.get('JSON')} • Nuvem: **{linha.get('Nuvem')}**")
    st.cache_data.clear()


# ===========================================================================
# Render
# ===========================================================================
def show_page():
    st.header("🌐 Portal iSeduc")
    st.caption("Planejamento, registro de aulas e notas — separado do portal do aluno.")

    online, detail = portal_api.status()
    _api_badge(online, detail)

    turma, subject = _sidebar_contexto()

    st.divider()
    try:
        secao = st.segmented_control("Seção", SECOES, default=SECOES[0])
    except Exception:
        secao = st.radio("Seção", SECOES, horizontal=True)
    secao = secao or SECOES[0]

    if turma is None:
        st.info("Nenhuma turma disponível para montar o contexto.")
        return

    if secao == SECOES[0]:
        _planejar(turma, subject, online)
    elif secao == SECOES[1]:
        _registrar(turma, subject, online)
    elif secao == SECOES[2]:
        _sincronizar(turma, subject, online)
    elif secao == SECOES[3]:
        _painel_consolidadas(turma, subject, online)
    elif secao == SECOES[4]:
        _notas(online)
    else:
        _config(turma, subject, online)
