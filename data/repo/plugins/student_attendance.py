"""
Plugin de Gerenciamento de Frequência (SysAva)

Este plugin permite registrar a presença diária dos alunos por turma,
salvando os dados em um arquivo JSON local.
"""

import streamlit as st
import json
import os
import sys
import pandas as pd
from datetime import datetime

# --- Configurações de Caminho ---
PLUGIN_DIR = os.path.dirname(__file__)
ATTENDANCE_FILE = os.path.join(PLUGIN_DIR, "student_attendance.json")

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from services import database as db
except ImportError:
    db = None

def load_json(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_json(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

def show_attendance_plugin():
    st.title("📅 Diário de Frequência")

    if db is None:
        st.error("Serviço de banco de dados não disponível.")
        return

    # 1. Seleção de Turma e Data na Sidebar
    with st.sidebar:
        st.header("Configurações")
        classes = db.get_classes()
        class_options = {c['name']: c['id'] for c in classes}
        
        selected_class_name = st.selectbox("Selecione a Turma", ["-- Selecione --"] + list(class_options.keys()))
        selected_date = st.date_input("Data da Aula", datetime.now())
        date_key = selected_date.isoformat()

    if selected_class_name == "-- Selecione --":
        st.info("Selecione uma turma na barra lateral para iniciar a chamada.")
        return

    class_id = class_options[selected_class_name]
    students = db.get_students_by_class(class_id)

    if not students:
        st.warning(f"Nenhum aluno encontrado na turma {selected_class_name}.")
        return

    # 2. Carregar Dados de Frequência
    attendance_data = load_json(ATTENDANCE_FILE)
    
    # Estrutura: { "class_id": { "date": { "username": "status" } } }
    class_key = str(class_id)
    if class_key not in attendance_data:
        attendance_data[class_key] = {}
    if date_key not in attendance_data[class_key]:
        attendance_data[class_key][date_key] = {}

    day_attendance = attendance_data[class_key][date_key]

    st.subheader(f"Lista de Presença: {selected_class_name}")
    st.caption(f"Registro para o dia {selected_date.strftime('%d/%m/%Y')}")

    # 3. Interface da Chamada (Tabela Condensada)
    # Preparamos um DataFrame para o editor
    df_attendance = pd.DataFrame([
        {
            "Username": s['username'], 
            "Nome": s['name'], 
            "Status": day_attendance.get(s['username'], "Presente")
        }
        for s in students
    ])

    # O data_editor permite editar o status como um dropdown em uma tabela compacta
    edited_df = st.data_editor(
        df_attendance,
        column_config={
            "Username": None, # Oculta a coluna de ID técnico
            "Nome": st.column_config.TextColumn("Estudante", disabled=True, width="large"),
            "Status": st.column_config.SelectboxColumn(
                "Presença",
                options=["Presente", "Falta", "Atraso"],
                required=True,
                width="medium"
            )
        },
        hide_index=True,
        use_container_width=True,
        key=f"editor_{class_key}_{date_key}"
    )

    new_entries = {row['Username']: row['Status'] for _, row in edited_df.iterrows()}

    if st.button("💾 Salvar Chamada do Dia", use_container_width=True, type="primary"):
        attendance_data[class_key][date_key] = new_entries
        save_json(ATTENDANCE_FILE, attendance_data)
        st.success(f"Chamada de {selected_date.strftime('%d/%m/%Y')} salva com sucesso!")
        st.rerun()

    # 4. Resumo rápido
    presencas = list(new_entries.values()).count("Presente")
    faltas = list(new_entries.values()).count("Falta")
    atrasos = list(new_entries.values()).count("Atraso")

    c1, c2, c3 = st.columns(3)
    c1.metric("Presenças", presencas)
    c2.metric("Faltas", faltas)
    c3.metric("Atrasos", atrasos)

    # 5. Tabela Geral de Histórico (Acumulado)
    st.divider()
    st.subheader("📊 Relatório Geral de Faltas e Presenças")
    
    class_history = attendance_data.get(class_key, {})
    if not class_history:
        st.info("Nenhum histórico acumulado para esta turma ainda.")
    else:
        summary_list = []
        all_dates = class_history.keys()
        
        for s in students:
            u = s['username']
            p_count = 0
            f_count = 0
            a_count = 0
            for d_key in all_dates:
                stat = class_history[d_key].get(u)
                if stat == "Presente": p_count += 1
                elif stat == "Falta": f_count += 1
                elif stat == "Atraso": a_count += 1
            
            total_days = p_count + f_count + a_count
            freq_val = (p_count + a_count) / total_days * 100 if total_days > 0 else 0
            
            summary_list.append({
                "Nome": s['name'],
                "Presenças ✅": p_count,
                "Faltas ❌": f_count,
                "Atrasos 🕒": a_count,
                "% Freq.": f"{freq_val:.1f}%"
            })
        
        # Ordenamos por quem tem mais faltas para facilitar a atenção do professor
        df_summary = pd.DataFrame(summary_list).sort_values(by="Faltas ❌", ascending=False)
        st.dataframe(df_summary, hide_index=True, use_container_width=True)

if __name__ == "__main__":
    is_streamlit = False
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx(): is_streamlit = True
    except: pass

    if is_streamlit:
        show_attendance_plugin()
    else:
        print("Este plugin deve ser executado dentro do SysAva.")