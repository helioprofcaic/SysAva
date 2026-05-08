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
        class_options = {c['name']: c['id'] for c in classes}
        selected_class_name = st.selectbox("Selecione a Turma", ["-- Selecione --"] + list(class_options.keys()))

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

    # --- CARREGAMENTO DE ALUNOS ---
    students = db.get_students_by_class(class_id)
    if not students:
        st.warning(f"Nenhum aluno encontrado na turma {selected_class_name}.")
        return

    st.subheader(f"📋 Quadro de Notas: {selected_class_name}")
    st.caption(f"Disciplina: {selected_subject_name}")

    # Prepara a lista de dados para o Dataframe (Quadro da Turma)
    table_rows = []
    for s in students:
        username = s['username']
        
        # Inicializa aluno no JSON se não existir
        if username not in all_scores_data["students_data"]:
            all_scores_data["students_data"][username] = {
                "name": s['name'], "overall_score": 0, "overall_grade": None, "subjects": {}, "daily_qualitative_points": []
            }

        student_json = all_scores_data["students_data"][username]
        if "subjects" not in student_json: student_json["subjects"] = {}
        
        # Busca score calculado pelo sistema
        calc = db.get_student_score(username, filter_subject_id=selected_subject_id)
        
        # Busca dados salvos manualmente
        if selected_subject_id is None:
            manual_score = student_json.get("overall_score", 0)
            manual_grade = student_json.get("overall_grade", "")
            nm1 = student_json.get("overall_nm1", 0.0)
            nm2 = student_json.get("overall_nm2", 0.0)
            nm3 = student_json.get("overall_nm3", 0.0)
        else:
            sid_str = str(selected_subject_id)
            if "subjects" not in student_json:
                student_json["subjects"] = {}
            
            if sid_str not in student_json["subjects"]:
                student_json["subjects"][sid_str] = {
                    "score": calc['total'], "grade": "", "nm1": 0.0, "nm2": 0.0, "nm3": 0.0
                }
            
            sub_data = student_json["subjects"].get(sid_str, {})
            manual_score = sub_data.get("score", 0)
            manual_grade = sub_data.get("grade", "")
            nm1 = sub_data.get("nm1", 0.0)
            nm2 = sub_data.get("nm2", 0.0)
            nm3 = sub_data.get("nm3", 0.0)

        # Cálculo da Média das Mensais
        v_nm1 = float(nm1) if nm1 is not None else 0.0
        v_nm2 = float(nm2) if nm2 is not None else 0.0
        v_nm3 = float(nm3) if nm3 is not None else 0.0
        media = (v_nm1 + v_nm2 + v_nm3) / 3
        
        # Soma pontos qualitativos totais
        qual_total = sum(p.get('points', 0) for p in student_json.get("daily_qualitative_points", []))

        table_rows.append({
            "Username": username,
            "Nome": s['name'],
            "🌐 Sis": calc['total'],
            "NM1": v_nm1,
            "NM2": v_nm2,
            "NM3": v_nm3,
            "Média": round(media, 2),
            "📝 Final": float(manual_score) if manual_score is not None else 0.0,
            "🎓 Conc.": manual_grade if manual_grade is not None else "",
            "⭐ Qualit.": qual_total,
            "➕ Add hoje": 0 # Campo para entrada rápida
        })

    df_scores = pd.DataFrame(table_rows)

    # --- EDITOR DE DADOS (PLANILHA) ---
    edited_df = st.data_editor(
        df_scores,
        column_config={
            "Username": None, # Oculto
            "Nome": st.column_config.TextColumn("Estudante", width="large", disabled=True),
            "🌐 Sis": st.column_config.NumberColumn("Score Sis.", help="Calculado pelo sistema", disabled=True, format="%.2f"),
            "NM1": st.column_config.NumberColumn("NM1", min_value=0.0, max_value=10.0, step=0.1, format="%.2f"),
            "NM2": st.column_config.NumberColumn("NM2", min_value=0.0, max_value=10.0, step=0.1, format="%.2f"),
            "NM3": st.column_config.NumberColumn("NM3", min_value=0.0, max_value=10.0, step=0.1, format="%.2f"),
            "Média": st.column_config.NumberColumn("Média", disabled=True, format="%.2f"),
            "📝 Final": st.column_config.NumberColumn("Nota Final", min_value=0.0, step=0.1, format="%.2f"),
            "🎓 Conc.": st.column_config.TextColumn("Conceito", help="Ex: A, B, C..."),
            "⭐ Qualit.": st.column_config.NumberColumn("Total Qualit.", disabled=True),
            "➕ Add hoje": st.column_config.NumberColumn("Ponto Extra", min_value=0, max_value=10, step=1)
        },
        hide_index=True,
        use_container_width=True,
        key=f"editor_scores_{class_id}_{selected_subject_id}"
    )

    if st.button("💾 Salvar Alterações da Turma", type="primary", use_container_width=True):
        for _, row in edited_df.iterrows():
            uname = row['Username']
            s_json = all_scores_data["students_data"][uname]
            
            # Atualiza Notas e Conceitos no JSON
            if selected_subject_id is None:
                s_json["overall_score"] = row["📝 Final"]
                s_json["overall_grade"] = row["🎓 Conc."]
                s_json["overall_nm1"] = row["NM1"]
                s_json["overall_nm2"] = row["NM2"]
                s_json["overall_nm3"] = row["NM3"]
            else:
                sid_str = str(selected_subject_id)
                if "subjects" not in s_json: s_json["subjects"] = {}
                if sid_str not in s_json["subjects"]: s_json["subjects"][sid_str] = {}
                
                s_json["subjects"][sid_str]["nm1"] = row["NM1"]
                s_json["subjects"][sid_str]["nm2"] = row["NM2"]
                s_json["subjects"][sid_str]["nm3"] = row["NM3"]
                s_json["subjects"][sid_str]["score"] = row["📝 Final"]
                s_json["subjects"][sid_str]["grade"] = row["🎓 Conc."]

            # Registra novos pontos qualitativos
            if row["➕ Add hoje"] > 0:
                s_json["daily_qualitative_points"].append({
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "points": row["➕ Add hoje"],
                    "notes": f"Lançamento via Quadro de Notas ({selected_subject_name})"
                })
        
        save_json(SCORES_FILE, all_scores_data)
        st.success("Quadro de notas atualizado!")
        st.rerun()

    st.divider()

    # --- EXPORTAÇÃO PARA PNG ---
    with st.expander("📸 Exportar Relatório de Notas"):
        if not MATPLOTLIB_AVAILABLE:
            st.error("Matplotlib não disponível.")
        else:
            if st.button("🖼️ Gerar Imagem das Notas", use_container_width=True):
                with st.spinner("Renderizando imagem..."):
                    # Remove colunas de edição e IDs para a imagem oficial
                    df_export = edited_df.drop(columns=['Username', '➕ Add hoje'])
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