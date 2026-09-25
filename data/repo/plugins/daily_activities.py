"""
Plugin de Atividades Diárias e Engajamento (SysAva)

Permite criar atividades vinculadas a aulas, postar automaticamente no fórum
e atribuir pontos qualitativos com limite de 6 pontos por bloco de 20 aulas.
"""

import streamlit as st
import json
import os
import sys
import pandas as pd
import re
from datetime import datetime

# --- Configurações de Caminho ---
PLUGIN_DIR = os.path.dirname(__file__)
SCORES_FILE = os.path.join(PLUGIN_DIR, "student_scores.json")

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from services import database as db
    from services import local_cache as lc
except ImportError:
    db = None
    lc = None

def load_json(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return {}
    return {}

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def _empty_score():
    return {'total': 0.0, 'lesson': 0, 'quiz': 0, 'forum': 0}

def get_scores_for_students(students, subject_id, force_refresh=False):
    """
    Carrega os scores da turma usando o cache SQLite local ANTES de ir ao Supabase.
    Só consulta o Supabase para os alunos sem entrada fresca no cache (evita o N+1).
    """
    usernames = [s['username'] for s in students]

    cached = {} if (force_refresh or lc is None) else lc.get_scores_bulk(subject_id, usernames)
    result = dict(cached)

    missing = [u for u in usernames if u not in result]
    if missing and db is not None:
        fetched = {}
        for u in missing:
            try:
                fetched[u] = db.get_student_score(u, filter_subject_id=subject_id)
            except Exception:
                fetched[u] = _empty_score()
        if lc is not None:
            lc.set_scores_bulk(subject_id, fetched)
        result.update(fetched)

    for u in usernames:
        result.setdefault(u, _empty_score())
    return result

def get_lesson_number(title):
    match = re.search(r'Aula\s*(\d+)', title, re.IGNORECASE)
    return int(match.group(1)) if match else 0

def _lesson_display(title):
    match = re.match(r'^Aula\s*\d+\s*[:.\-]?\s*', title, flags=re.IGNORECASE)
    return title[match.end():].strip() if match else title

APRESENTACAO_QTD = 8

def _bloco_regular(aula_num):
    grupo = max(1, (aula_num - 1) // 20 + 1)
    ini = (grupo - 1) * 20 + 1
    fim = grupo * 20
    return f"{ini}-{fim}"

def _bloco_info(aula_num, ultima_aula):
    if ultima_aula >= APRESENTACAO_QTD and aula_num > ultima_aula - APRESENTACAO_QTD:
        return f"Apresentação ({ultima_aula - APRESENTACAO_QTD + 1}-{ultima_aula})", False
    return _bloco_regular(aula_num), True

def show_daily_activities():
    st.title("🎯 Gestor de Atividades Diárias")
    
    if db is None:
        st.error("Banco de dados não disponível.")
        return

    # --- SIDEBAR: Filtros ---
    with st.sidebar:
        st.header("Filtros")
        classes = db.get_classes()
        class_options = {c['name']: c['id'] for c in classes}
        class_display = {c['name']: f"{c['name']} ({c.get('official_name', 'S/N')})" for c in classes}

        sel_class_name = st.selectbox(
            "Turma", 
            ["-- Selecione --"] + list(class_options.keys()),
            format_func=lambda x: class_display.get(x, x)
        )

        if sel_class_name == "-- Selecione --":
            st.stop()

        class_id = class_options[sel_class_name]
        subjects = db.get_subjects_for_class(class_id)
        subjects = [s for s in subjects if s.get('is_active', True)]
        subject_options = {}
        for s in subjects:
            s_name = s['name'].strip()
            if s_name not in subject_options:
                subject_options[s_name] = s['id']
        sel_subject_name = st.selectbox("Disciplina", list(subject_options.keys()))
        subject_id = subject_options[sel_subject_name]

    # --- CARREGAMENTO DE DADOS ---
    lessons = db.get_lessons_for_subject(subject_id)
    if not lessons:
        st.warning("Nenhuma aula encontrada para esta disciplina.")
        return

    ultima_aula = max([get_lesson_number(l['title']) for l in lessons] + [0])
    apres_ini = max(1, ultima_aula - APRESENTACAO_QTD + 1)

    # --- LANÇAMENTO DE SEMINÁRIO COMO AVALIAÇÃO ---
    st.divider()
    st.subheader("🎤 Lançamento de Seminário (Avaliação)")
    st.caption("Selecione o intervalo de aulas, dê um nome ao seminário e ele será lançado nas Avaliações da disciplina (visível para professor e alunos).")

    lesson_num_map = {}
    for l in lessons:
        n = get_lesson_number(l['title'])
        if n:
            lesson_num_map.setdefault(n, l)
    aula_ordenadas = sorted(lesson_num_map.keys())

    if not aula_ordenadas:
        st.info("Esta disciplina não possui aulas numeradas (padrão 'Aula XX'), então não é possível montar o intervalo.")
    else:
        intervalo = st.select_slider(
            "Intervalo de aulas para o seminário",
            options=aula_ordenadas,
            value=(aula_ordenadas[0], aula_ordenadas[-1]),
            key="sem_intervalo"
        )
        aula_min, aula_max = intervalo
        interval_lessons = [lesson_num_map[n] for n in range(aula_min, aula_max + 1) if n in lesson_num_map]

        if interval_lessons:
            st.markdown("#### 📚 Lista de Aulas para Pesquisar")
            st.dataframe(
                pd.DataFrame([
                    {"Aula": n, "Título": _lesson_display(lesson_num_map[n]['title'])}
                    for n in range(aula_min, aula_max + 1) if n in lesson_num_map
                ]),
                hide_index=True,
                use_container_width=True
            )

        sem_nome = st.text_input(
            "Nome do Seminário",
            placeholder="Ex: Seminário de IA na Educação",
            key="sem_nome"
        )

        sem_students = db.get_students_by_class(class_id)
        student_options = {}
        for s in sem_students:
            key = f"{s.get('name', s['username'])} ({s['username']})"
            if s['username'] not in student_options:
                student_options[key] = s['username']
        sem_membros = st.multiselect(
            "👥 Integrantes do grupo do seminário",
            sorted(student_options.keys()),
            key="sem_membros"
        )
        if sem_membros:
            st.caption(f"{len(sem_membros)} integrante(s) selecionado(s).")

        if st.button("🚀 Lançar Seminário como Avaliação", type="primary", use_container_width=True, key="btn_lancar_seminario"):
            sem_nome = (sem_nome or "").strip()
            if not sem_nome:
                st.warning("Informe o nome do seminário antes de lançar.")
            elif not interval_lessons:
                st.warning("O intervalo selecionado não contém aulas numeradas.")
            elif not sem_membros:
                st.warning("Selecione ao menos um integrante do grupo.")
            else:
                av_title = f"{sem_nome} · Aulas {aula_min}–{aula_max}"
                existing = db.get_assessments_by_subject(subject_id)
                if any(str(a.get('title', '')).strip() == av_title for a in existing):
                    st.warning(f"Já existe um seminário com este nome/intervalo: **{av_title}**.")
                else:
                    data, err = db.create_assessment(subject_id, "Seminário", av_title)
                    if err:
                        st.error(f"Erro ao lançar o seminário: {err}")
                    elif not data or not isinstance(data, list) or not data:
                        st.error("O Supabase não retornou a avaliação criada.")
                    else:
                        aid = data[0]['id']
                        lista_pesquisa = "\n".join(
                            f"- Aula {n}: {_lesson_display(lesson_num_map[n]['title'])}"
                            for n in range(aula_min, aula_max + 1) if n in lesson_num_map
                        )
                        lista_integrantes = "\n".join(f"- {membro}" for membro in sem_membros)
                        _, qerr = db.create_assessment_question(
                            aid,
                            f"SEMINÁRIO — {sem_nome}\n\n"
                            f"👥 Integrantes do grupo:\n{lista_integrantes}\n\n"
                            f"📚 Pesquise e apresente as aulas abaixo:\n{lista_pesquisa}",
                            'subjective', [], 0
                        )
                        if qerr:
                            st.warning(f"Seminário criado, mas não foi possível anexar a lista: {qerr}")
                        st.success(f"Seminário lançado como avaliação: **{av_title}** (id {aid}). "
                                   f"{len(interval_lessons)} aula(s) compõem a pesquisa e "
                                   f"{len(sem_membros)} integrante(s) no grupo.")
                        st.rerun()

    st.divider()

    lesson_map = {f"{l['title']}": l for l in lessons}
    selected_lesson_title = st.selectbox("Escolha a Aula para a Atividade:", list(lesson_map.keys()))
    selected_lesson = lesson_map[selected_lesson_title]
    lesson_num = get_lesson_number(selected_lesson_title)

    # Identifica o bloco — as últimas 8 aulas da disciplina são Apresentação de Seminários (sem teto)
    bloco, capped = _bloco_info(lesson_num, ultima_aula)
    if not capped:
        st.info(f"📍 Aula de **Apresentação ({apres_ini}-{ultima_aula})** — apresentações de seminários. **Sem limite de 6 pontos** (nota pode chegar a 10).")
    else:
        st.info(f"📍 Aula selecionada pertence ao **Bloco {bloco}**. (Limite: 6 pontos acumulados)")

    # --- CRIAÇÃO DA ATIVIDADE ---
    st.subheader("📝 Descrição da Atividade")
    activity_text = st.text_area("O que os alunos devem fazer?", 
                                placeholder="Ex: Resolver os exercícios da página 50 e enviar o print do código...")
    
    col1, col2 = st.columns(2)
    if col1.button("📢 Publicar no Fórum como EduBot", use_container_width=True):
        if activity_text:
            msg = (
                f"🚀 **ATIVIDADE PRÁTICA: {selected_lesson_title}**\n\n"
                f"{activity_text}\n\n"
                "--- \n"
                "💡 **Dica do EduBot:** Se a atividade envolver código, você pode testar no [Replit](https://replit.com) ou [OnlineGDB](https://www.onlinegdb.com). Poste sua dúvida abaixo!"
            )
            _, error = db.add_forum_post("EduBot 🤖", msg, lesson_id=selected_lesson['id'])
            if error:
                st.error(f"Erro ao publicar: {error}")
            else:
                st.success("Atividade publicada no fórum da aula!")
        else:
            st.warning("Escreva a atividade antes de publicar.")

    st.divider()

    # --- LANÇAMENTO DE PONTOS ---
    col_titulo, col_refresh = st.columns([4, 1])
    col_titulo.subheader("⭐ Atribuir Pontos para esta Aula")
    if col_refresh.button("🔄 Atualizar notas", use_container_width=True,
                          help="Ignora o cache local e rebusca os scores no Supabase"):
        if lc is not None:
            lc.invalidate_scores(subject_id)
        st.rerun()

    students = db.get_students_by_class(class_id)
    all_scores_data = load_json(SCORES_FILE)
    if "students_data" not in all_scores_data: all_scores_data["students_data"] = {}

    # Carrega todos os scores de uma vez (cache SQLite local antes do Supabase)
    scores_map = get_scores_for_students(students, subject_id)

    # Otimização: Criamos um mapa de blocos para todas as aulas da disciplina de uma vez só
    lesson_block_map = {}
    for l in lessons:
        bloco_l, _ = _bloco_info(get_lesson_number(l['title']), ultima_aula)
        lesson_block_map[l['id']] = bloco_l

    table_data = []
    for s in students:
        uname = s['username']
        if uname not in all_scores_data["students_data"]:
            all_scores_data["students_data"][uname] = {"name": s['name'], "daily_qualitative_points": []}
        
        student_json = all_scores_data["students_data"][uname]
        if "daily_qualitative_points" not in student_json:
            student_json["daily_qualitative_points"] = []
        
        # Cálculo de engajamento do sistema (conforme home.py), já vindo do cache local
        calc = scores_map.get(uname, _empty_score())
        system_score = calc.get('total', 0.0)
        
        # Filtra pontos qualitativos JÁ ATRIBUÍDOS no bloco atual (1-20, 21-40, ... ou Apresentação) com limite de 6.0
        qual_points_bloco = 0.0
        for p in student_json.get("daily_qualitative_points", []):
            p_lesson_id = p.get('lesson_id')
            p_bloco = lesson_block_map.get(p_lesson_id)
            if p_bloco == bloco:
                qual_points_bloco += float(p.get('points', 0))

        if capped:
            qual_points_bloco = min(6.0, qual_points_bloco)
            total_atual = min(6.0, system_score + qual_points_bloco)
            restante = max(0.0, 6.0 - total_atual)
        else:
            total_atual = system_score + qual_points_bloco
            restante = 999.0

        table_data.append({
            "Username": uname,
            "Nome": s['name'],
            "Nota de Hoje": 0.0,
            "🌐 Sis": system_score,
            "⭐ Qualit": round(qual_points_bloco, 1),
            "📈 Total": round(total_atual, 2),
            "Limite": round(restante, 1)
            # "Nota de Hoje": 0.0
        })

    df_atividades = pd.DataFrame(table_data)
    
    max_nota_hoje = 10.0 if not capped else 2.0
    passo_nota = 0.5 if not capped else 0.1
    help_limite = (f"Aulas de apresentação ({apres_ini}-{ultima_aula}): sem teto de 6 pontos" if not capped
                   else "Quanto o aluno ainda pode ganhar neste bloco")

    edited_df = st.data_editor(
        df_atividades,
        column_config={
            "Username": None,
            "Nome": st.column_config.TextColumn("Estudante", disabled=True, width="large"),
            "Nota de Hoje": st.column_config.NumberColumn("Pontuar", min_value=0.0, max_value=max_nota_hoje, step=passo_nota),
            "🌐 Sis": st.column_config.NumberColumn(disabled=True, format="%.2f"),
            "⭐ Qualit": st.column_config.NumberColumn(disabled=True, format="%.1f"),
            "📈 Total": st.column_config.NumberColumn(disabled=True, format="%.2f"),
            "Limite": st.column_config.NumberColumn("Disponível", help=help_limite, disabled=True, format="%.1f")
        },
        hide_index=True,
        use_container_width=True,
        key=f"editor_atividades_{selected_lesson['id']}"
    )

    if st.button("💾 Salvar Pontos de Hoje", type="primary", use_container_width=True):
        saved_count = 0
        for _, row in edited_df.iterrows():
            if row["Nota de Hoje"] > 0:
                uname = row['Username']
                s_json = all_scores_data["students_data"][uname]
                
                # Garante que os novos pontos não ultrapassem o teto de 6.0 do bloco (exceto Apresentação)
                pontos_novos = row["Nota de Hoje"]
                if capped and row["📈 Total"] + pontos_novos > 6.0:
                    pontos_novos = max(0.0, 6.0 - row["📈 Total"])
                
                if pontos_novos > 0:
                    s_json["daily_qualitative_points"].append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "points": round(pontos_novos, 1),
                        "lesson_id": selected_lesson['id'],
                        "subject_id": subject_id,
                        "subject_name": sel_subject_name,
                        "notes": f"Atividade Aula {lesson_num}: {selected_lesson_title}"
                    })
                    saved_count += 1
        
        if saved_count > 0:
            save_json(SCORES_FILE, all_scores_data)
            st.success(f"Pontuação de {saved_count} alunos registrada com sucesso!")
            st.rerun()
        else:
            st.info("Nenhuma pontuação nova para salvar.")

    # --- VISUALIZAÇÃO: PONTUAÇÃO DISTRIBUÍDA POR ATIVIDADES ---
    st.divider()
    st.subheader("📊 Pontuação Distribuída por Atividades")

    lesson_title_map = {l['id']: l['title'] for l in lessons}
    student_name_map = {s['username']: s['name'] for s in students}

    detail_rows = []
    for uname, s_data in all_scores_data.get("students_data", {}).items():
        if uname not in student_name_map:
            continue
        for p in s_data.get("daily_qualitative_points", []):
            p_lesson_id = p.get('lesson_id')
            p_subject_id = p.get('subject_id')
            # Entradas antigas não possuem subject_id: infere pela aula da disciplina
            pertence = (str(p_subject_id) == str(subject_id)) or (
                p_subject_id is None and p_lesson_id in lesson_title_map
            )
            if not pertence:
                continue
            detail_rows.append({
                "Data": p.get('date', ''),
                "Estudante": student_name_map[uname],
                "Aula": lesson_title_map.get(p_lesson_id, p.get('notes', '—')),
                "Bloco": lesson_block_map.get(p_lesson_id, '—'),
                "Pontos": round(float(p.get('points', 0)), 1)
            })

    if detail_rows:
        bloco_filtro = st.selectbox("Filtrar por bloco", ["Todos"] + sorted({b for b in lesson_block_map.values() if b}), key="filtro_bloco_detalhe")
        df_detalhe = pd.DataFrame(detail_rows)
        if bloco_filtro != "Todos":
            df_detalhe = df_detalhe[df_detalhe["Bloco"] == bloco_filtro]
        df_detalhe = df_detalhe.sort_values("Data", ascending=False)

        if not df_detalhe.empty:
            col_a, col_b, col_c, col_d = st.columns([2, 2, 2, 2])
            col_a.metric("Total distribuído", f"{df_detalhe['Pontos'].sum():.1f} pts")
            col_b.metric("Lançamentos", len(df_detalhe))

            # Exporta TODAS as aulas da disciplina (ignora o filtro de bloco da tela)
            df_export = pd.DataFrame(detail_rows).sort_values("Data", ascending=False)
            base_name = f"relatorio_atividades_{sel_class_name}_{sel_subject_name}"
            csv_bytes = df_export.to_csv(index=False).encode('utf-8-sig')

            html_doc = (
                "<!DOCTYPE html><html lang='pt-BR'><head><meta charset='utf-8'>"
                f"<title>Relatório de Atividades — {sel_subject_name}</title>"
                "<style>body{font-family:Arial,sans-serif;margin:24px;color:#222}"
                "h1{font-size:20px}table{border-collapse:collapse;width:100%}"
                "th,td{border:1px solid #ccc;padding:6px 10px;font-size:13px;text-align:left}"
                "th{background:#f0f2f6}tr:nth-child(even){background:#fafafa}</style>"
                "</head><body>"
                f"<h1>Relatório de Pontuação por Atividades</h1>"
                f"<p><strong>Turma:</strong> {sel_class_name} &nbsp;|&nbsp; "
                f"<strong>Disciplina:</strong> {sel_subject_name}</p>"
                + df_export.to_html(index=False, border=0)
                + "</body></html>"
            )

            col_c.download_button(
                "📥 Baixar CSV",
                data=csv_bytes,
                file_name=f"{base_name}.csv",
                mime="text/csv",
                use_container_width=True,
                key="download_relatorio_atividades_csv"
            )
            col_d.download_button(
                "🌐 Baixar HTML",
                data=html_doc.encode('utf-8'),
                file_name=f"{base_name}.html",
                mime="text/html",
                use_container_width=True,
                key="download_relatorio_atividades_html"
            )
            st.dataframe(df_detalhe, hide_index=True, use_container_width=True)
        else:
            st.info("Nenhum ponto distribuído no bloco selecionado.")
    else:
        st.info("Nenhum ponto distribuído para esta disciplina até o momento.")

if __name__ == "__main__":
    is_streamlit = False
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx(): is_streamlit = True
    except: pass

    if is_streamlit:
        show_daily_activities()