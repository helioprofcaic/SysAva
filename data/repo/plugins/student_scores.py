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
from datetime import datetime

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

    # Carrega os dados existentes
    all_scores_data = load_json(SCORES_FILE)
    
    # Garante que a estrutura básica existe
    if "students_data" not in all_scores_data:
        all_scores_data["students_data"] = {}

    students = []

    # Carrega a lista de alunos do Supabase ou usa Mock se offline
    if db.is_db_connected():
        try:
            # Assumindo que db.get_all_users() retorna uma lista de dicionários com 'id', 'name', 'username', 'role'
            all_users = db.get_all_users() 
            students = [u for u in all_users if u.get('role') == 'student']
        except Exception as e:
            st.error(f"Erro ao carregar alunos do banco de dados: {e}")
    else:
        st.info("💡 Modo Offline: Carregando alunos de demonstração para teste.")
        students = [
            {'id': 'mock-1', 'name': 'Aluno de Teste 1', 'username': 'aluno1', 'role': 'student'},
            {'id': 'mock-2', 'name': 'Aluno de Teste 2', 'username': 'aluno2', 'role': 'student'}
        ]

    if not students:
        st.warning("Nenhum aluno encontrado no banco de dados.")
        return

    # Sidebar para seleção de aluno
    with st.sidebar:
        st.header("Aluno")
        student_names = [s['name'] for s in students]
        selected_student_name = st.selectbox("Selecione um aluno", student_names)
        
        selected_student = next((s for s in students if s['name'] == selected_student_name), None)
        
        if selected_student:
            st.write(f"**Usuário:** {selected_student['username']}")
            st.write(f"**ID:** {selected_student.get('id', 'N/A')}")
        else:
            st.warning("Aluno não encontrado.")
            return

    # Inicializa dados do aluno selecionado se não existirem no JSON
    student_username = selected_student['username']
    if student_username not in all_scores_data["students_data"]:
        all_scores_data["students_data"][student_username] = {
            "name": selected_student['name'],
            "overall_score": None,
            "overall_grade": None,
            "daily_qualitative_points": []
        }
        save_json(SCORES_FILE, all_scores_data) # Salva a estrutura inicial

    student_data = all_scores_data["students_data"][student_username]

    st.subheader(f"Detalhes para {student_data['name']}")

    # Exibir e editar Score e Grade Geral
    col1, col2 = st.columns(2)
    with col1:
        current_score = student_data.get("overall_score")
        # Garante que o valor inicial seja um float para o number_input
        new_score = st.number_input("Score Geral", value=float(current_score) if current_score is not None else 0.0, format="%.2f")
    with col2:
        current_grade = student_data.get("overall_grade", "")
        new_grade = st.text_input("Grade Geral", value=current_grade)

    # Verifica se houve alteração para salvar
    if new_score != current_score or new_grade != current_grade:
        student_data["overall_score"] = new_score
        student_data["overall_grade"] = new_grade
        save_json(SCORES_FILE, all_scores_data)
        st.success("Score e Grade atualizados!")
        st.rerun() # Recarrega a página para refletir as mudanças imediatamente

    st.markdown("---")

    # Adicionar Pontos Qualitativos Diários
    st.subheader("Adicionar Pontos Qualitativos Diários")
    with st.form("add_qualitative_points"):
        col_date, col_points = st.columns([0.4, 0.6])
        with col_date:
            point_date = st.date_input("Data", datetime.now())
        with col_points:
            point_value = st.number_input("Pontos", min_value=0, max_value=10, value=1, step=1)
        
        point_notes = st.text_area("Observações", placeholder="Ex: Participação ativa, colaboração, melhoria contínua...")
        
        if st.form_submit_button("Adicionar Ponto"):
            if point_notes:
                new_point = {
                    "date": point_date.isoformat(),
                    "points": point_value,
                    "notes": point_notes
                }
                student_data["daily_qualitative_points"].append(new_point)
                save_json(SCORES_FILE, all_scores_data)
                st.success("Ponto qualitativo adicionado com sucesso!")
                st.rerun()
            else:
                st.warning("Por favor, adicione uma observação para o ponto qualitativo.")

    st.markdown("---")

    # Visualizar Pontos Qualitativos Existentes
    st.subheader("Histórico de Pontos Qualitativos")
    if student_data["daily_qualitative_points"]:
        # Ordena por data decrescente
        sorted_points = sorted(student_data["daily_qualitative_points"], key=lambda x: x['date'], reverse=True)
        for i, point in enumerate(sorted_points):
            col_p_date, col_p_val, col_p_notes, col_p_del = st.columns([0.2, 0.1, 0.6, 0.1])
            col_p_date.write(f"**{point['date']}**")
            col_p_val.write(f"**{point['points']} pts**")
            col_p_notes.write(point['notes'])
            if col_p_del.button("🗑️", key=f"del_point_{student_username}_{i}"):
                student_data["daily_qualitative_points"].remove(point)
                save_json(SCORES_FILE, all_scores_data)
                st.success("Ponto removido.")
                st.rerun()
            st.markdown("---")
    else:
        st.info("Nenhum ponto qualitativo registrado para este aluno ainda.")

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