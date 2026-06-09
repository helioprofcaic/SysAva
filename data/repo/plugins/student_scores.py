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
                    "score": calc['total'], "grade": "", "nm1": 0.0, "nm2": 0.0, "nm3": 0.0, "outros1": 0.0, "outros2": 0.0
                }
            
            sub_data = student_json["subjects"].get(sid_str, {})
            manual_score = sub_data.get("score", 0)
            manual_grade = sub_data.get("grade", "")
            nm1 = sub_data.get("nm1", 0.0)
            nm2 = sub_data.get("nm2", 0.0)
            nm3 = sub_data.get("nm3", 0.0)            
            outros1 = sub_data.get("outros1", 0.0)
            outros2 = sub_data.get("outros2", 0.0)

        # --- LÓGICA DE FORMAÇÃO DE NOTAS (Engajamento e Qualitativos) ---
        system_score = round(float(calc['total']), 2)
        # Penalidade: se engajamento < 3, o aluno perde a diferença (máximo 3 pontos) em NM1 e NM2
        engaj_penalty = round(max(0.0, 3.0 - system_score), 2)
        # Bônus: engajamento adiciona até 3 pontos em NM3
        engaj_bonus = round(min(3.0, system_score), 2)
        
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
        
        # Regra NM3: Ou Nota de Avaliação (Base) ou Qualitativo (Engajamento + Extras)
        f_nm1 = round(min(10.0, max(0.0, base_nm1 - engaj_penalty)), 2)
        f_nm2 = round(min(10.0, max(0.0, base_nm2 - engaj_penalty)), 2)
        
        qual_total = round(min(10.0, engaj_bonus + qual_manual), 2)
        # Se o aluno tem nota na avaliação NM3, prioriza ela. Senão, usa o qualitativo.
        f_nm3 = base_nm3 if base_nm3 > 0 else qual_total
        
        media = (f_nm1 + f_nm2 + f_nm3) / 3

        table_rows.append({
            "Username": username,
            "Nome": s['name'],
            "🌐 Engaj.": system_score,
            "NM1": f_nm1,
            "NM2": f_nm2,
            "NM3": f_nm3,
            "Média": round(media, 2),
            "📝 Final": float(manual_score) if manual_score is not None else 0.0,
            "🎓 Conc.": manual_grade if manual_grade is not None else "",
            "⭐ Qualit.": qual_manual,
            "➕ Add hoje": 0,
            "_orig_qual": qual_manual, # Campo oculto para detecção de alteração
            "_eng_pen": engaj_penalty,  # Auxiliar para o save não duplicar pontos
            "_eng_bon": engaj_bonus,    # Auxiliar para o save não duplicar pontos
            "_base_nm3": base_nm3       # Base original para saber se era AV ou Qualitativo
        })

    df_scores = pd.DataFrame(table_rows)

    # --- EDITOR DE DADOS (PLANILHA) ---
    edited_df = st.data_editor(
        df_scores,
        column_config={
            "Username": None,
            "_orig_qual": None,
            "_eng_pen": None,
            "_eng_bon": None,
            "_base_nm3": None,
            "Nome": st.column_config.TextColumn("Estudante", width="large", disabled=True),
            "🌐 Engaj.": st.column_config.NumberColumn("Engaj.", help="Score do Sistema (influencia NM1, NM2 e NM3)", disabled=True, format="%.2f"),
            "NM1": st.column_config.NumberColumn("NM1", help="Base da Avaliação 1", min_value=0.0, max_value=10.0, format="%.2f"),
            "NM2": st.column_config.NumberColumn("NM2", help="Base da Avaliação 2", min_value=0.0, max_value=10.0, format="%.2f"),
            "NM3": st.column_config.NumberColumn("NM3", help="Base da Avaliação 3", min_value=0.0, max_value=10.0, format="%.2f"),
            "Média": st.column_config.NumberColumn("Média Final", disabled=True, format="%.2f"),
            "📝 Final": st.column_config.NumberColumn("Nota Final", min_value=0.0, step=0.1, format="%.2f"),
            "🎓 Conc.": st.column_config.TextColumn("Conceito", help="Ex: A, B, C..."),
            "⭐ Qualit.": st.column_config.NumberColumn("Qualitativo", help="Pontos qualitativos acumulados", min_value=0.0, max_value=10.0, format="%.1f"),
            "➕ Add hoje": st.column_config.NumberColumn("Ponto Extra", min_value=0, max_value=10, step=1)
        },
        hide_index=True,
        use_container_width=True,
        key=f"ed_scr_{class_id}" # Chave curta para reduzir o tamanho do header/state
    )

    if st.button("💾 Salvar Alterações da Turma", type="primary", use_container_width=True):
        for _, row in edited_df.iterrows():
            uname = row['Username']
            s_json = all_scores_data["students_data"][uname]
            
            # Reverte penalidade de NM1 e NM2
            res_nm1 = round(row["NM1"] + row["_eng_pen"], 2)
            res_nm2 = round(row["NM2"] + row["_eng_pen"], 2)
            
            # Lógica para NM3: Zerar se houver ponto extra ou se o valor for o calculado automaticamente
            # Isso evita "resquícios" no JSON e garante que o NM3 reflita sempre Engajamento + Qualitativo
            current_qual_calc = round(min(10.0, row["⭐ Qualit."] + row["_eng_bon"]), 2)
            
            if row["➕ Add hoje"] > 0:
                res_nm3 = 0.0
            elif abs(row["NM3"] - current_qual_calc) < 0.01:
                res_nm3 = 0.0
            else:
                res_nm3 = row["NM3"]

            # Salva no JSON
            if selected_subject_id is None:
                s_json["overall_score"] = row["📝 Final"]
                s_json["overall_grade"] = row["🎓 Conc."]
                s_json["overall_nm1"] = res_nm1
                s_json["overall_nm2"] = res_nm2
                s_json["overall_nm3"] = res_nm3
            else:
                sid_str = str(selected_subject_id)
                if "subjects" not in s_json: s_json["subjects"] = {}
                if sid_str not in s_json["subjects"]: s_json["subjects"][sid_str] = {}
                
                s_json["subjects"][sid_str]["nm1"] = res_nm1
                s_json["subjects"][sid_str]["nm2"] = res_nm2
                s_json["subjects"][sid_str]["nm3"] = res_nm3
                s_json["subjects"][sid_str]["score"] = row["📝 Final"]
                s_json["subjects"][sid_str]["grade"] = row["🎓 Conc."]

            # Verifica se o qualitativo foi alterado manualmente no editor
            diff_qual = row["⭐ Qualit."] - row["_orig_qual"]
            if abs(diff_qual) > 0.01:
                entry = {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "points": round(diff_qual, 1),
                    "notes": "Ajuste manual via Quadro de Notas"
                }
                if selected_subject_id is not None:
                    entry["subject_id"] = selected_subject_id
                s_json["daily_qualitative_points"].append(entry)

            # Registra novos pontos qualitativos
            if row["➕ Add hoje"] > 0:
                entry = {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "points": row["➕ Add hoje"],
                    "notes": f"Lançamento via Quadro de Notas ({selected_subject_name})"
                }
                if selected_subject_id is not None:
                    entry["subject_id"] = selected_subject_id
                s_json["daily_qualitative_points"].append(entry)
        
        save_json(SCORES_FILE, all_scores_data)
        st.cache_data.clear() # Limpa o cache para mostrar os novos dados após salvar
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