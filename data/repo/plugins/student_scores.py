"""
Plugin de Gerenciamento de Notas e Pontos Qualitativos (SysAva)

Este plugin permite que administradores e professores gerenciem as notas gerais
dos alunos e adicionem pontos qualitativos diários, salvando os dados em um
arquivo JSON local.

Uso: Acessível via menu 'Plugins' no painel administrativo do SysAva.
"""

import streamlit as st
import json
import os
import sys
import pandas as pd
from datetime import datetime
from io import BytesIO

# Tenta importar Matplotlib para geração de PNG
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# --- Configurações de Caminho ---
PLUGIN_DIR = os.path.dirname(__file__)
SCORES_FILE = os.path.join(PLUGIN_DIR, "student_scores.json")

# Adiciona o diretório raiz do projeto ao sys.path para garantir que os módulos sejam encontrados.
# O script está em 'data/repo/plugins', então subimos 3 níveis para chegar à raiz.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def log_message(message, type="info"):
    """Exibe mensagens no Streamlit ou no Console dependendo do contexto."""
    try:
        if type == "error": st.error(message)
        elif type == "warning": st.warning(message)
        else: st.info(message)
    except:
        print(f"[{type.upper()}] {message}")

try:
    from services import database as db
except ImportError:
    db = None
    log_message("Erro: Não foi possível importar o serviço de banco de dados.", "error")

@st.cache_data(ttl=600)
def load_json(file_path):
    """Carrega dados de um arquivo JSON. Retorna um dicionário vazio se o arquivo não existir ou estiver corrompido."""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            log_message(f"Arquivo '{file_path}' corrompido. Criando novo.", "warning")
            return {"students_data": {}}
        except Exception as e:
            log_message(f"Erro ao carregar JSON: {e}", "error")
            return {"students_data": {}}
    return {"students_data": {}}

@st.cache_data(ttl=300)
def get_cached_student_score(username, subject_id):
    """Wrapper para cachear a consulta de scores do banco de dados e evitar 431/timeouts."""
    if db:
        return db.get_student_score(username, filter_subject_id=subject_id)
    return {'total': 0.0}

def save_json(file_path, data):
    """Salva dados em um arquivo JSON."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        log_message(f"Erro ao salvar JSON: {e}", "error")

def create_scores_png(df, class_name, subject_name, school_name, prof_name):
    """Gera uma imagem PNG da lista de notas usando Matplotlib."""
    # Ajusta o tamanho da figura baseado na quantidade de alunos
    fig, ax = plt.subplots(figsize=(16, len(df) * 0.4 + 3))
    ax.axis('off')

    # Cabeçalho da Imagem
    plt.text(0.5, 0.97, school_name, fontsize=18, fontweight='bold', ha='center', va='top', transform=fig.transFigure)
    plt.text(0.5, 0.93, f"Relatório de Notas - {class_name}", fontsize=14, ha='center', va='top', transform=fig.transFigure)
    plt.text(0.5, 0.90, f"Disciplina: {subject_name} | Professor: {prof_name}", fontsize=11, ha='center', va='top', transform=fig.transFigure)

    header_bg = '#e9ecef'
    
    # Cria a tabela no plot (Removemos colunas internas como username para a foto)
    export_df = df.drop(columns=['Username']) if 'Username' in df.columns else df

    the_table = ax.table(
        cellText=export_df.values, 
        colLabels=export_df.columns, 
        cellLoc='center', 
        loc='center',
        bbox=[0, 0, 1, 0.88]
    )

    # Estilização das células
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(9)
    the_table.scale(1.2, 1.5)

    for (row, col), cell in the_table.get_celld().items():
        if row == 0:
            cell.set_facecolor(header_bg)
            cell.get_text().set_weight('bold')
        
        # Alinha a coluna do Nome (0) à esquerda para evitar cortes e melhorar leitura
        if col == 0 and row > 0:
            cell.get_text().set_horizontalalignment('left')

    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight', dpi=200)
    plt.close(fig)
    return buf.getvalue()

def run_cli_report():
    """Executa um relatório no terminal quando o plugin é chamado como script externo."""
    print("\n" + "="*50)
    print("📊 RELATÓRIO DE ESCORES E PONTOS QUALITATIVOS")
    print("="*50)
    
    data = load_json(SCORES_FILE)
    students = data.get("students_data", {})
    
    if not students:
        print("Nenhum dado de aluno encontrado no arquivo JSON.")
        return

    for username, info in students.items():
        score = info.get("overall_score", 0)
        grade = info.get("overall_grade", "N/A")
        q_points = len(info.get("daily_qualitative_points", []))
        print(f"Estudante: {info['name']} ({username})")
        print(f"  - Score: {score} | Grade: {grade}")
        print(f"  - Registros Qualitativos: {q_points}")
        print("-" * 30)
    print("="*50 + "\n")

def show_student_scores():
    """Renderiza a interface para gerenciar escores e pontos qualitativos dos alunos."""
    st.title("📊 Gerenciador de Notas e Pontos Qualitativos")

    if db is None:
        st.error("Serviço de banco de dados não disponível.")
        return

    # Busca informações da instituição e professor para os labels do PNG
    school_info = db.get_school()
    school_name = school_info.get('name', 'SysAva') if school_info else "SysAva"
    prof_name = st.session_state.get('usuario', 'Professor')

    # Carrega os dados existentes
    all_scores_data = load_json(SCORES_FILE)
    if "students_data" not in all_scores_data:
        all_scores_data["students_data"] = {}

    # --- SIDEBAR: Seleção de Turma e Disciplina ---
    with st.sidebar:
        st.header("Filtros")
        classes = db.get_classes()
        # Mapeia ID para objeto completo para facilitar exibição composta
        class_options = {c['name']: c['id'] for c in classes}
        # Cria um mapeamento de exibição: "Nome Amigável (Nome Oficial)"
        class_display = {c['name']: f"{c['name']} ({c.get('official_name', 'S/N Oficial')})" for c in classes}
        
        selected_class_name = st.selectbox(
            "Selecione a Turma", 
            ["-- Selecione --"] + list(class_options.keys()),
            format_func=lambda x: class_display.get(x, x)
        )

        selected_subject_id = None
        selected_subject_name = "Visão Geral"

        if selected_class_name != "-- Selecione --":
            class_id = class_options[selected_class_name]
            subjects = db.get_subjects_for_class(class_id)
            subject_options = {"Visão Geral (Todas)": None}
            subject_options.update({s['name']: s['id'] for s in subjects})
            selected_subject_name = st.selectbox("Selecione a Disciplina", list(subject_options.keys()))
            selected_subject_id = subject_options[selected_subject_name]
        else:
            st.info("Selecione uma turma para carregar o quadro de notas.")
            return

        st.divider()
        st.session_state['selected_trimester'] = st.radio(
            "Filtrar por Período",
            ["Visão Geral", "1º Trimestre", "2º Trimestre", "3º Trimestre"],
            horizontal=True,
            key="trim_selector"
        )

    if selected_class_name == "-- Selecione --":
            st.info("Selecione uma turma para carregar o quadro de notas.")
            return

    # --- CARREGAMENTO DE ALUNOS ---
    students = db.get_students_by_class(class_id)
    if not students:
        st.warning(f"Nenhum aluno encontrado na turma {selected_class_name}.")
        return

    st.subheader(f"📋 Quadro de Notas: {selected_class_name}")
    st.caption(f"Disciplina: {selected_subject_name}")

    # --- CARREGAMENTO DE AVALIAÇÕES DO BANCO ---
    asmt_lookup = {k: {} for k in ["MN1", "MN2", "MN3", "Outros1", "Outros2", "Outros3", "Outros4"]}
    
    if selected_subject_id is not None:
        try:
            assessments = db.get_assessments_by_subject(selected_subject_id)
            assessments = sorted(assessments, key=lambda x: x.get('created_at', x['id']))
            
            outros_found = 0
            for a in assessments:
                a_type = str(a.get('type', ''))
                target_key = None
                
                if a_type in ["MN1", "MN2", "MN3"]:
                    target_key = a_type
                elif a_type == "Outros":
                    outros_found += 1
                    target_key = f"Outros{outros_found}" if outros_found <= 4 else None
                
                if target_key and target_key in asmt_lookup:
                    subs = db.get_assessment_submissions_with_users(a['id'])
                    for s in subs:
                        user_info = s.get('app_users') or {}
                        u_name = user_info.get('username')
                        u_real_name = user_info.get('name')
                        u_score = s.get('score')
                        
                        if u_score is not None:
                            if u_name:
                                if u_name not in asmt_lookup[target_key] or u_score > asmt_lookup[target_key][u_name]:
                                    asmt_lookup[target_key][u_name] = u_score
                            if u_real_name:
                                if u_real_name not in asmt_lookup[target_key] or u_score > asmt_lookup[target_key][u_real_name]:
                                    asmt_lookup[target_key][u_real_name] = u_score
        except Exception:
            pass

    # Prepara a lista de dados para o Dataframe (Quadro da Turma)
    table_rows = []
    for s in students:
        username = s['username']
        
        # Inicializa aluno no JSON se não existir
        if username not in all_scores_data["students_data"]:
            all_scores_data["students_data"][username] = {
                "name": s['name'], "overall_score": 0, "overall_grade": None, "subjects": {}, "daily_qualitative_points": [],
                "overall_nm1": 0.0, "overall_nm2": 0.0, "overall_nm3": 0.0, "overall_outros1": 0.0, "overall_outros2": 0.0
            }

        student_json = all_scores_data["students_data"][username]
        if "subjects" not in student_json: student_json["subjects"] = {}
        if "daily_qualitative_points" not in student_json: student_json["daily_qualitative_points"] = []

        # Garante que as chaves de notas gerais existam para todos os alunos (correção de inconsistência)
        for key in ["overall_nm1", "overall_nm2", "overall_nm3", "overall_outros1", "overall_outros2"]:
            if key not in student_json:
                # Inicializa todas as 9 notas e as gerais
                student_json.update({f"overall_nm{i}": 0.0 for i in range(1, 10)})
        
        
        # Inicializa variáveis locais para evitar NameError
        nm1, nm2, nm3, outros1, outros2 = 0.0, 0.0, 0.0, 0.0, 0.0
        manual_score, manual_grade = 0.0, ""

        # Busca score calculado pelo sistema
        calc = get_cached_student_score(username, selected_subject_id)
        
        # Busca dados salvos manualmente
        if selected_subject_id is None:
            manual_score = student_json.get("overall_score", 0)
            manual_grade = student_json.get("overall_grade", "")
            nm1 = student_json.get("overall_nm1", 0.0)
            nm2 = student_json.get("overall_nm2", 0.0)
            nm3 = student_json.get("overall_nm3", 0.0)            
            outros1 = student_json.get("overall_outros1", 0.0)
            outros2 = student_json.get("overall_outros2", 0.0)
        else:
            sid_str = str(selected_subject_id)
            if "subjects" not in student_json:
                student_json["subjects"] = {}
            
            if sid_str not in student_json["subjects"]:
                student_json["subjects"][sid_str] = {
                    "score": calc.get('total', 0.0), "grade": "",
                    "T1": {"N1": 0.0, "N2": 0.0, "N3": 0.0},
                    "T2": {"N1": 0.0, "N2": 0.0, "N3": 0.0},
                    "T3": {"N1": 0.0, "N2": 0.0, "N3": 0.0}
                }
            
            sub_data = student_json["subjects"].get(sid_str, {})
            manual_score = sub_data.get("score", 0)
            manual_grade = sub_data.get("grade", "")

            # Carrega as notas da estrutura aninhada
            t1_data = sub_data.get("T1", {})
            t2_data = sub_data.get("T2", {})
            t3_data = sub_data.get("T3", {})

            # Lógica de retrocompatibilidade: Tenta ler a nova estrutura aninhada.
            # Se falhar, lê a estrutura antiga (nm1, nm2, etc.) para não perder dados.
            nm1 = t1_data.get("N1", sub_data.get("nm1", 0.0))
            nm2 = t1_data.get("N2", sub_data.get("nm2", 0.0))
            nm3 = t1_data.get("N3", sub_data.get("nm3", 0.0))
            nm4 = t2_data.get("N1", sub_data.get("nm4", 0.0))
            nm5 = t2_data.get("N2", sub_data.get("nm5", 0.0))
            nm6 = t2_data.get("N3", sub_data.get("nm6", 0.0))
            nm7 = t3_data.get("N1", sub_data.get("nm7", 0.0))
            nm8 = t3_data.get("N2", sub_data.get("nm8", 0.0))
            nm9 = t3_data.get("N3", sub_data.get("nm9", 0.0))

        # --- LÓGICA DE FORMAÇÃO DE NOTAS (Simplificada) ---
        system_score = round(float(calc['total']), 2)

        # Busca bases de notas (Prioriza Avaliações Específicas > Outros > Manual)
        db_mn1 = asmt_lookup["MN1"].get(username, asmt_lookup["MN1"].get(s['name']))
        db_mn2 = asmt_lookup["MN2"].get(username, asmt_lookup["MN2"].get(s['name']))
        db_mn3 = asmt_lookup["MN3"].get(username, asmt_lookup["MN3"].get(s['name']))
        db_ot1 = asmt_lookup["Outros1"].get(username, asmt_lookup["Outros1"].get(s['name']))
        db_ot2 = asmt_lookup["Outros2"].get(username, asmt_lookup["Outros2"].get(s['name']))
        db_ot3 = asmt_lookup["Outros3"].get(username, asmt_lookup["Outros3"].get(s['name']))
        db_ot4 = asmt_lookup["Outros4"].get(username, asmt_lookup["Outros4"].get(s['name']))

        val_ot1 = db_ot1 if db_ot1 is not None else db_ot3
        base_nm1 = round(float(db_mn1 if db_mn1 is not None else (val_ot1 if val_ot1 is not None else nm1)), 2)
        
        val_ot2 = db_ot2 if db_ot2 is not None else db_ot4
        base_nm2 = round(float(db_mn2 if db_mn2 is not None else (val_ot2 if val_ot2 is not None else nm2)), 2)

        base_nm3 = round(float(db_mn3 if db_mn3 is not None else nm3), 2)
        
        # Soma pontos qualitativos manuais filtrando pela disciplina selecionada
        all_points = student_json.get("daily_qualitative_points", [])
        if selected_subject_id is not None:
            sid_str = str(selected_subject_id)
            qual_manual = round(sum(p.get('points', 0) for p in all_points if str(p.get('subject_id')) == sid_str), 2)
        else:
            qual_manual = round(sum(p.get('points', 0) for p in all_points), 2)
        
        # Lógica simplificada: As notas são o que foi digitado ou o que veio do banco.
        f_nm1 = base_nm1
        f_nm2 = base_nm2
        f_nm3 = base_nm3
        
        # Lógica de Média por Trimestre
        t1_notes = [nm1, nm2, nm3]
        t2_notes = [nm4, nm5, nm6]
        t3_notes = [nm7, nm8, nm9]

        # Conta apenas notas > 0 para a média, para não penalizar notas não lançadas
        media_t1 = sum(t1_notes) / len([n for n in t1_notes if n > 0]) if any(n > 0 for n in t1_notes) else 0.0
        media_t2 = sum(t2_notes) / len([n for n in t2_notes if n > 0]) if any(n > 0 for n in t2_notes) else 0.0
        media_t3 = sum(t3_notes) / len([n for n in t3_notes if n > 0]) if any(n > 0 for n in t3_notes) else 0.0

        # Média Final Geral
        all_trim_means = [media_t1, media_t2, media_t3]
        final_media = sum(all_trim_means) / len([m for m in all_trim_means if m > 0]) if any(m > 0 for m in all_trim_means) else 0.0

        table_rows.append({
            "Username": username,
            "Nome": s['name'],
            "🌐 Engaj.": system_score,
            # T1
            "NM1": t1_notes[0],
            "NM2": t1_notes[1],
            "NM3": t1_notes[2],
            # T2
            "NM4": t2_notes[0],
            "NM5": t2_notes[1],
            "NM6": t2_notes[2],
            # T3
            "NM7": t3_notes[0],
            "NM8": t3_notes[1],
            "NM9": t3_notes[2],
            "Média": round(final_media, 2),
            "📝 Final": float(manual_score) if manual_score is not None else 0.0,
            "🎓 Conc.": manual_grade if manual_grade is not None else "",
            "⭐ Qualit.": qual_manual,
        })

    df_scores = pd.DataFrame(table_rows)

    # --- EDITOR DE DADOS (PLANILHA) ---
    selected_trim = st.session_state.get('selected_trimester', "Visão Geral")

    # Define quais colunas de nota devem ser visíveis
    visible_notes = []
    if selected_trim == "1º Trimestre":
        visible_notes = ["NM1", "NM2", "NM3"]
    elif selected_trim == "2º Trimestre":
        visible_notes = ["NM4", "NM5", "NM6"]
    elif selected_trim == "3º Trimestre":
        visible_notes = ["NM7", "NM8", "NM9"]
    else: # Visão Geral
        visible_notes = [f"NM{i}" for i in range(1, 10)]

    edited_df = st.data_editor(
        df_scores,
        column_config={
            "Username": None,
            "Nome": st.column_config.TextColumn("Estudante", width="large", disabled=True),
            "🌐 Engaj.": st.column_config.NumberColumn("Engaj.", help="Score do Sistema (influencia NM1, NM2 e NM3)", disabled=True, format="%.2f"),
            # T1
            "NM1": st.column_config.NumberColumn("N1 (T1)", help="Nota 1 do 1º Trimestre", min_value=0.0, max_value=10.0, format="%.2f") if "NM1" in visible_notes else None,
            "NM2": st.column_config.NumberColumn("N2 (T1)", help="Nota 2 do 1º Trimestre", min_value=0.0, max_value=10.0, format="%.2f") if "NM2" in visible_notes else None,
            "NM3": st.column_config.NumberColumn("N3 (T1)", help="Nota 3 do 1º Trimestre", min_value=0.0, max_value=10.0, format="%.2f") if "NM3" in visible_notes else None,
            # T2
            "NM4": st.column_config.NumberColumn("N1 (T2)", help="Nota 1 do 2º Trimestre", min_value=0.0, max_value=10.0, format="%.2f") if "NM4" in visible_notes else None,
            "NM5": st.column_config.NumberColumn("N2 (T2)", help="Nota 2 do 2º Trimestre", min_value=0.0, max_value=10.0, format="%.2f") if "NM5" in visible_notes else None,
            "NM6": st.column_config.NumberColumn("N3 (T2)", help="Nota 3 do 2º Trimestre", min_value=0.0, max_value=10.0, format="%.2f") if "NM6" in visible_notes else None,
            # T3
            "NM7": st.column_config.NumberColumn("N1 (T3)", help="Nota 1 do 3º Trimestre", min_value=0.0, max_value=10.0, format="%.2f") if "NM7" in visible_notes else None,
            "NM8": st.column_config.NumberColumn("N2 (T3)", help="Nota 2 do 3º Trimestre", min_value=0.0, max_value=10.0, format="%.2f") if "NM8" in visible_notes else None,
            "NM9": st.column_config.NumberColumn("N3 (T3)", help="Nota 3 do 3º Trimestre", min_value=0.0, max_value=10.0, format="%.2f") if "NM9" in visible_notes else None,

            "Média": st.column_config.NumberColumn("Média Final", disabled=True, format="%.2f"),
            "📝 Final": st.column_config.NumberColumn("Nota Final", help="Nota final manual, se necessário", min_value=0.0, step=0.1, format="%.2f"),
            "🎓 Conc.": st.column_config.TextColumn("Conceito", help="Ex: A, B, C..."),
            "⭐ Qualit.": st.column_config.NumberColumn("Qualitativo", help="Pontos qualitativos acumulados (não altera a média)", disabled=True, format="%.1f"),
        },
        column_order=[
            "Nome", "🌐 Engaj.", 
            "NM1", "NM2", "NM3", 
            "NM4", "NM5", "NM6",
            "NM7", "NM8", "NM9",
            "Média", "📝 Final", "🎓 Conc.", "⭐ Qualit."
        ],
        hide_index=True,
        use_container_width=True,
        key=f"ed_scr_{class_id}" # Chave curta para reduzir o tamanho do header/state
    )

    if st.button("💾 Salvar Alterações da Turma", type="primary", use_container_width=True):
        for _, row in edited_df.iterrows():
            uname = row['Username']
            s_json = all_scores_data["students_data"][uname]
            
            # Lógica de salvamento simplificada
            if selected_subject_id is None:
                s_json["overall_score"] = row["📝 Final"]
                s_json["overall_grade"] = row["🎓 Conc."]
                for i in range(1, 10):
                    s_json[f"overall_nm{i}"] = round(row[f"NM{i}"], 2)
            else:
                sid_str = str(selected_subject_id)
                if "subjects" not in s_json: s_json["subjects"] = {}
                if sid_str not in s_json["subjects"]: s_json["subjects"][sid_str] = {}
                
                s_json["subjects"][sid_str]["score"] = row["📝 Final"]
                s_json["subjects"][sid_str]["grade"] = row["🎓 Conc."]
                s_json["subjects"][sid_str]["T1"] = {"N1": round(row["NM1"], 2), "N2": round(row["NM2"], 2), "N3": round(row["NM3"], 2)}
                s_json["subjects"][sid_str]["T2"] = {"N1": round(row["NM4"], 2), "N2": round(row["NM5"], 2), "N3": round(row["NM6"], 2)}
                s_json["subjects"][sid_str]["T3"] = {"N1": round(row["NM7"], 2), "N2": round(row["NM8"], 2), "N3": round(row["NM9"], 2)}
        
        save_json(SCORES_FILE, all_scores_data)
        st.cache_data.clear() # Limpa o cache para mostrar os novos dados após salvar
        st.success("Quadro de notas atualizado!")
        st.rerun()

    st.divider()

    # --- PAINEL INDIVIDUAL DO ALUNO ---
    st.subheader("👤 Análise Individual e Pontos Qualitativos")

    student_names = edited_df['Nome'].tolist()
    selected_student_name = st.selectbox(
        "Selecione um aluno para ver detalhes",
        ["-- Selecione --"] + student_names,
        key="student_detail_selector"
    )

    if selected_student_name != "-- Selecione --":
        student_row = edited_df[edited_df['Nome'] == selected_student_name].iloc[0]
        username = student_row['Username']
        student_json = all_scores_data["students_data"][username]

        st.markdown(f"#### Detalhes de **{selected_student_name}**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Média Final (Calculada)", f"{student_row['Média']:.2f}")
        with col2:
            st.metric("Score de Engajamento", f"{student_row['🌐 Engaj.']:.2f}")
        with col3:
            st.metric("Pontos Qualitativos", f"{student_row['⭐ Qualit.']:.1f}")

        with st.expander("➕ Adicionar Pontos Qualitativos"):
            with st.form(key=f"form_qual_{username}"):
                points_to_add = st.number_input("Pontos a adicionar", min_value=0.0, max_value=5.0, step=0.5, value=1.0)
                reason = st.text_input("Motivo/Atividade", placeholder="Ex: Participação em aula, projeto extra...")
                submitted = st.form_submit_button("Adicionar Ponto")

                if submitted:
                    if reason:
                        entry = {
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "points": points_to_add,
                            "notes": reason
                        }
                        if selected_subject_id is not None:
                            entry["subject_id"] = selected_subject_id
                        
                        student_json.setdefault("daily_qualitative_points", []).append(entry)
                        save_json(SCORES_FILE, all_scores_data)
                        st.success(f"{points_to_add} ponto(s) adicionado(s) para {selected_student_name}!")
                        st.rerun()
                    else:
                        st.warning("Por favor, informe o motivo da pontuação.")

        st.markdown("##### 📜 Histórico de Pontos Qualitativos")
        qual_history = student_json.get("daily_qualitative_points", [])
        
        if qual_history:
            if selected_subject_id:
                sid_str = str(selected_subject_id)
                qual_history = [p for p in qual_history if str(p.get('subject_id')) == sid_str]

            if qual_history:
                df_qual = pd.DataFrame(qual_history).sort_values(by="date", ascending=False)
                df_qual = df_qual.rename(columns={"date": "Data", "points": "Pontos", "notes": "Motivo"})
                st.dataframe(df_qual[['Data', 'Pontos', 'Motivo']], hide_index=True, use_container_width=True)
            else:
                st.info(f"Nenhum ponto qualitativo registrado para esta disciplina.")
        else:
            st.info("Nenhum ponto qualitativo registrado para este aluno.")

    # --- EXPORTAÇÃO PARA PNG ---
    with st.expander("📸 Exportar Relatório de Notas"):
        if not MATPLOTLIB_AVAILABLE:
            st.error("Matplotlib não disponível.")
        else:
            if st.button("🖼️ Gerar Imagem das Notas", use_container_width=True):
                with st.spinner("Renderizando imagem..."):
                    df_export = edited_df.drop(columns=['Username'])
                    png_data = create_scores_png(df_export, selected_class_name, selected_subject_name, school_name, prof_name)
                    st.download_button(
                        label="💾 Download Imagem (PNG)",
                        data=png_data,
                        file_name=f"notas_{selected_class_name}_{datetime.now().strftime('%Y%m%d')}.png",
                        mime="image/png",
                        use_container_width=True
                    )

# Se o script for executado diretamente (para testes)
if __name__ == "__main__":
    # Detecta se está rodando dentro do Streamlit ou via Terminal (External Plugin)
    is_streamlit = False
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx(): is_streamlit = True
    except: pass

    if is_streamlit:
        show_student_scores()
    else:
        # Se rodar via "Executar" na aba de Plugins Externos
        run_cli_report()