"""
Plugin de Registro de Aula (SysAva)

Este plugin automatiza o registro de diários de classe, integrando a grade horária,
o currículo (BNCC/EPT) e o conteúdo das aulas para preenchimento automático.
"""

import streamlit as st
import json
import os
import sys
import re
import pandas as pd
from datetime import datetime, timedelta

# --- Configurações de Caminho ---
PLUGIN_DIR = os.path.dirname(__file__)
REGISTRY_FILE = os.path.join(PLUGIN_DIR, "class_registries.json")
GRADE_FILE = os.path.join(PLUGIN_DIR, "grade_horaria.json")
CURRICULO_FILE = os.path.join(os.path.dirname(PLUGIN_DIR), "ementas_cronogramas", "curriculo_db.json")
REPO_DIR = os.path.dirname(PLUGIN_DIR)

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
        except: return {}
    return {}

@st.cache_data(show_spinner="Sincronizando catálogo de aulas...")
def get_lessons_catalog():
    """
    Escaneia a pasta data/Turmas (lógica similar ao seed_lessons.py)
    e retorna um DataFrame com todas as aulas encontradas.
    """
    base_path = os.path.join(project_root, 'data', 'Turmas')
    lessons_list = []
    
    if not os.path.exists(base_path):
        return pd.DataFrame()

    # Percorre a estrutura: Turma / Disciplina / Semana / Aula_XX.md
    for root, dirs, files in os.walk(base_path):
        md_files = [f for f in files if f.lower().endswith(".md")]
        if not md_files:
            continue
            
        relative_path = os.path.relpath(root, base_path)
        path_parts = relative_path.split(os.sep)
        
        # Identifica Turma e Disciplina pelos nomes das pastas
        # Estrutura esperada: data/Turmas/{Turma}/{Disciplina}/...
        if len(path_parts) >= 2:
            turma_folder = path_parts[0]
            disc_folder = path_parts[1]
            
            for lesson_file in md_files:
                # Tenta extrair o número da aula do nome do arquivo (ex: Aula_05.md)
                num_match = re.search(r'Aula_(\d+)', lesson_file, re.IGNORECASE)
                if not num_match:
                    num_match = re.search(r'(\d+)', lesson_file) # Fallback para qualquer número
                
                lesson_num = int(num_match.group(1)) if num_match else 0
                
                try:
                    with open(os.path.join(root, lesson_file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
                    title = title_match.group(1).strip() if title_match else lesson_file.replace(".md", "")
                    
                    intro_match = re.search(r'##\s+(?:🏁\s+)?Introdução\n+(.*?)\n(?:#|---)', content, re.DOTALL | re.IGNORECASE)
                    intro = intro_match.group(1).strip() if intro_match else "Conteúdo da aula teórica e prática."
                    
                    lessons_list.append({
                        "turma": turma_folder,
                        "disciplina": disc_folder,
                        "aula_num": lesson_num,
                        "titulo": title,
                        "intro": intro
                    })
                except: continue
                
    return pd.DataFrame(lessons_list)

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_folder_mapping(disciplina):
    """Mapeia o nome da disciplina na grade para o nome da pasta no repositório."""
    mapping = {
        "Disc.Tec.": "PROG_ESTRUCT",
        "I.A.": "IA",
        "P.C. II": "PC_II",
        "Ment.Tec.II": "MENT_TEC"
    }
    return mapping.get(disciplina, disciplina.upper().replace(" ", "_")[:12])

def load_grade_with_sync():
    """Carrega a grade horária do JSON. Se não existir, baixa do Supabase."""
    grade = load_json(GRADE_FILE)
    
    # Se o arquivo não existe ou está vazio, tenta recuperar do banco de dados
    if not grade and db and hasattr(db, 'supabase'):
        try:
            with st.spinner("Grade local não encontrada. Sincronizando com o servidor..."):
                response = db.supabase.table("weekly_schedule").select("*").execute()
                if response.data:
                    new_grade = {}
                    for row in response.data:
                        turma = row['class_name']
                        dia = row['day_of_week']
                        horario = row['time_slot']
                        disc = row['subject_name']
                        
                        if turma not in new_grade:
                            new_grade[turma] = {
                                "config_horarios": ["07:10", "08:10", "09:10", "10:10", "10:30", "11:30", "12:30", "13:30", "14:30", "14:50", "15:50", "16:50"]
                            }
                        
                        if dia not in new_grade[turma]:
                            new_grade[turma][dia] = {}
                        
                        new_grade[turma][dia][horario] = disc
                    
                    if new_grade:
                        save_json(GRADE_FILE, new_grade)
                        st.toast("✅ Grade horária sincronizada e salva localmente.")
                        return new_grade
        except Exception: pass
            
    return grade

def calculate_lesson_number(start_date, target_date, class_name, subject_name, grade):
    """Calcula o número da aula baseado na grade horária e data inicial."""
    if class_name not in grade: return 1
    
    dias_semana_map = {0: "Segunda", 1: "Terça", 2: "Quarta", 3: "Quinta", 4: "Sexta", 5: "Sábado", 6: "Domingo"}
    
    current = start_date
    lesson_count = 0
    
    while current <= target_date:
        dia_nome = dias_semana_map[current.weekday()]
        aulas_dia = grade[class_name].get(dia_nome, {})
        
        # Conta quantas vezes a disciplina aparece naquele dia
        for h, sub in aulas_dia.items():
            if subject_name.lower() in sub.lower() or sub.lower() in subject_name.lower():
                lesson_count += 1
        current += timedelta(days=1)
    
    return max(1, lesson_count)

def show_class_registry():
    st.title("📝 Registro de Aula")
    
    grade = load_grade_with_sync()
    curriculo = load_json(CURRICULO_FILE)
    
    if not grade:
        st.error("Grade horária não encontrada.")
        return

    # Carrega o catálogo de aulas escaneando os arquivos .md
    df_catalogo = get_lessons_catalog()

    # --- CABEÇALHO DO REGISTRO ---
    col_header1, col_header2 = st.columns(2)
    
    with col_header1:
        tipo_aula = st.selectbox("Tipo de Aula", ["-- Selecione --", "Teórica", "Prática", "Avaliação", "Laboratório", "Extraordinária"])
        
        classes = list(grade.keys())
        turma_sel = st.selectbox("Turma", ["-- Selecione --"] + classes)

    with col_header2:
        data_aula = st.date_input("Data", datetime.now())
        dias_semana_map = {0: "Segunda", 1: "Terça", 2: "Quarta", 3: "Quinta", 4: "Sexta", 5: "Sábado", 6: "Domingo"}
        dia_nome = dias_semana_map[data_aula.weekday()]

        # --- LÓGICA DE FILTRAGEM POR GRADE ---
        componente = ""
        horarios_opcoes = []
        
        if turma_sel != "-- Selecione --":
            aulas_no_dia = grade[turma_sel].get(dia_nome, {})
            
            if not aulas_no_dia:
                st.warning(f"⚠️ Não há aulas previstas na grade para {dia_nome}.")
                componente_opcoes = ["-- Sem aulas na grade --"]
            else:
                componente_opcoes = sorted(list(set(aulas_no_dia.values())))
            
            componente = st.selectbox("Componente", ["-- Selecione --"] + componente_opcoes)
            
            if componente != "-- Selecione --" and componente != "-- Sem aulas na grade --":
                # Filtra apenas os horários em que este componente específico acontece neste dia
                horarios_opcoes = [h for h, s in aulas_no_dia.items() if s == componente]
        else:
            st.selectbox("Componente", ["-- Selecione a Turma primeiro --"], disabled=True)

    horario_sel = st.selectbox("Horário (inicial ~ final)", ["-- Selecione --"] + horarios_opcoes if horarios_opcoes else ["-- Selecione --"])
        
    st.divider()
    st.subheader("Registro de Aula")

    # --- LÓGICA DE CURRÍCULO (BNCC/EPT) ---
    # Tenta achar os dados da disciplina no curriculo_db.json
    dados_curriculo = {}
    if componente:
        comp_upper = componente.upper()
        for segmento in curriculo:
            if comp_upper in curriculo[segmento]:
                dados_curriculo = curriculo[segmento][comp_upper]
                break

    col_cur1, col_cur2 = st.columns(2)
    
    with col_cur1:
        comp_especifica = st.selectbox("Competência Específica", 
                                      ["-- Selecione --", dados_curriculo.get("competencia", "Geral")] if dados_curriculo else ["-- Selecione --"])
        
        hab_lista = dados_curriculo.get("habilidades", [])
        habilidade = st.selectbox("Habilidades", ["-- Selecione --"] + hab_lista if hab_lista else ["-- Selecione --"])

    with col_cur2:
        hab_integrada = st.selectbox("Habilidade Integrada", ["-- Selecione --", "Trabalho em Equipe", "Resolução de Problemas", "Ética Profissional"])
        objetivo = st.text_area("Objetivo da Aprendizagem", 
                               value=f"Capacitar o aluno a compreender e aplicar os conceitos de {componente}." if componente else "")

    objeto_conhecimento = st.text_input("Objeto do Conhecimento", value=componente)

    # --- LÓGICA DE CONTEÚDO AUTOMÁTICO ---
    # Data de início do ano letivo fornecida: 19/02/2026
    data_inicio = datetime(2026, 2, 19).date()
    
    if turma_sel != "-- Selecione --" and componente:
        # 1. Calcula qual o número da aula no cronograma
        n_aula = calculate_lesson_number(data_inicio, data_aula, turma_sel, componente, grade)
        
        # 2. Busca no DataFrame do catálogo pela aula correspondente
        # Filtra por número da aula e tenta encontrar na pasta da disciplina
        match = df_catalogo[
            (df_catalogo['turma'].str.contains(turma_sel, case=False, na=False)) &
            (df_catalogo['aula_num'] == n_aula) & 
            (df_catalogo['disciplina'].str.contains(get_folder_mapping(componente), case=False, na=False))
        ]
        
        if not match.empty:
            aula_info = match.iloc[0]
            conteudo_sugerido = f"Aula {n_aula}: {aula_info['titulo']}\n\n{aula_info['intro']}"
            st.success(f"✅ Conteúdo da Aula {n_aula} extraído com sucesso!")
        elif db and db.is_db_connected():
            # Caso não encontre localmente, tenta baixar do banco de dados
            sub_info = db.get_subject_by_name(componente)
            if sub_info:
                sid = sub_info['id']
                db_lessons = db.get_lessons_for_subject(sid)
                
                # Busca a aula pelo número no título (ex: "Aula 05" ou "Aula 5")
                search_pat = rf"Aula\s*0?{n_aula}\b"
                db_match = [l for l in db_lessons if re.search(search_pat, l['title'], re.IGNORECASE)]
                
                if db_match:
                    lesson_db = db_match[0]
                    full_desc = lesson_db.get('description', '')
                    title_db = lesson_db.get('title', '')
                    
                    # Extrai introdução para o diário
                    intro_m = re.search(r'##\s+(?:🏁\s+)?Introdução\n+(.*?)\n(?:#|---)', full_desc, re.DOTALL | re.IGNORECASE)
                    intro_db = intro_m.group(1).strip() if intro_m else "Conteúdo recuperado do banco de dados."
                    
                    conteudo_sugerido = f"Aula {n_aula}: {title_db}\n\n{intro_db}"
                    st.success(f"📥 Aula {n_aula} baixada do banco de dados para o registro!")
                    
                    # Opção para baixar o arquivo .md completo recuperado
                    st.download_button(
                        label="💾 Baixar arquivo .md desta aula",
                        data=full_desc,
                        file_name=f"Aula_{n_aula:02d}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                else:
                    conteudo_sugerido = f"Aula {n_aula}: "
                    st.info(f"ℹ️ Aula {n_aula} calculada, mas não localizada localmente ou no banco.")
            else:
                conteudo_sugerido = f"Aula {n_aula}: "
                st.info(f"ℹ️ Aula {n_aula} calculada, mas disciplina não encontrada no banco.")
        else:
            conteudo_sugerido = f"Aula {n_aula}: "
            st.info(f"ℹ️ Aula {n_aula} calculada, mas arquivo .md não localizado no catálogo.")
            
    else:
        conteudo_sugerido = ""

    conteudo_abordado = st.text_area("Conteúdo abordado (*)", value=conteudo_sugerido, height=150)
    
    estrategia = st.text_area("Estratégia metodológica (*)", 
                             placeholder="Informe as estratégias metodológica (ex: Aula expositiva, prática em laboratório...)")

    # --- BOTÕES DE AÇÃO ---
    st.divider()
    c_btn1, c_btn2, c_btn3 = st.columns([0.2, 0.2, 0.6])
    
    if c_btn1.button("Cancelar", use_container_width=True):
        st.rerun()

    if c_btn2.button("Salvar e Avançar", type="primary", use_container_width=True):
        # Validação simples
        if not conteudo_abordado or not estrategia:
            st.error("Por favor, preencha todos os campos obrigatórios (*)")
        else:
            # Salva no JSON local
            registries = load_json(REGISTRY_FILE)
            if "data" not in registries: registries["data"] = []
            
            new_entry = {
                "id": len(registries["data"]) + 1,
                "timestamp": datetime.now().isoformat(),
                "tipo": tipo_aula,
                "turma": turma_sel,
                "componente": componente,
                "data": data_aula.isoformat(),
                "horario": horario_sel,
                "competencia": comp_especifica,
                "habilidade": habilidade,
                "objetivo": objetivo,
                "conteudo": conteudo_abordado,
                "estrategia": estrategia
            }
            
            registries["data"].append(new_entry)
            save_json(REGISTRY_FILE, registries)
            
            # Integração com o banco de dados (opcional)
            if db and hasattr(db, 'supabase'):
                try:
                    # Exemplo de salvamento no histórico do usuário
                    user = st.session_state.get('username', 'professor_ext')
                    db.add_user_history(user, f"Registrou aula {n_aula} de {componente} para {turma_sel}")
                except: pass

            st.success("Registro de aula salvo com sucesso!")
            st.balloons()

    # --- HISTÓRICO RECENTE ---
    with st.expander("📂 Ver Registros Anteriores"):
        registries = load_json(REGISTRY_FILE)
        if "data" in registries and registries["data"]:
            hist_df = pd.DataFrame(registries["data"])
            st.dataframe(hist_df[["data", "turma", "componente", "tipo", "conteudo"]], hide_index=True)
        else:
            st.info("Nenhum registro encontrado.")

    # --- UTILITÁRIOS DE CONSULTA AO BANCO ---
    st.divider()
    with st.expander("🔍 Utilitários do Banco de Dados"):
        if db and db.is_db_connected():
            if st.button("📋 Gerar Lista de Aulas do Banco", use_container_width=True):
                lessons_db = db.get_lessons()
                if lessons_db:
                    log_content = "LISTA DE AULAS NO BANCO DE DADOS (SUPABASE)\n"
                    log_content += f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                    log_content += "="*60 + "\n"
                    for l in lessons_db:
                        log_content += f"ID: {l['id']:<5} | Disciplina ID: {l['subject_id']:<5} | Título: {l['title']}\n"
                    
                    st.download_button(
                        label="📥 Baixar lessons_db.log",
                        data=log_content,
                        file_name="lessons_db.log",
                        mime="text/plain",
                        use_container_width=True
                    )
                else:
                    st.warning("Nenhuma aula encontrada no banco de dados.")
        else:
            st.error("Banco de dados não conectado para consulta.")

if __name__ == "__main__":
    # Configura a página se rodar sozinho
    try:
        st.set_page_config(page_title="Registro de Aula - SysAva", layout="wide")
    except: pass
    show_class_registry()


### Principais Funcionalidades Implementadas:

# 1.  **Cálculo Automático do Cronograma**: O script utiliza a data de `19/02/2026` como marco zero. Ele percorre os dias entre o início e a data selecionada no calendário, consultando a `grade_horaria.json` para contar quantas vezes aquela disciplina ocorreu, determinando o **Número da Aula** exato.
# 2.  **Extração de Conteúdo (Smart-Fill)**: Ao identificar o número da aula, o plugin varre a pasta `data/repo` em busca do arquivo Markdown correspondente. Ele extrai o título principal e o parágrafo da "Introdução" para preencher o campo **Conteúdo Abordado** automaticamente.
# 3.  **Integração Curricular**: O plugin tenta carregar Competências e Habilidades do arquivo `curriculo_db.json` (usado pelo motor do Gemini no SysAva), facilitando o preenchimento pedagógico.
# 4.  **Interface Fiel ao Requisito**: Incluí todos os campos solicitados, respeitando a obrigatoriedade (*) e a estrutura de colunas para uma melhor experiência de usuário no Streamlit.
# 5.  **Persistência**: Os registros são salvos em `class_registries.json` na pasta do plugin, permitindo auditoria e exportação futura.

# Para que o plugin apareça na sua central, certifique-se de que ele está listado no seu arquivo principal de visualização de plugins ou chame-o diretamente via Streamlit.

# <!--
# [PROMPT_SUGGESTION]Adicionar um botão para gerar um relatório PDF formatado do Registro de Aula selecionado.[/PROMPT_SUGGESTION]
# [PROMPT_SUGGESTION]Sincronizar os registros de aula salvos no JSON com uma tabela 'class_logs' no Supabase.[/PROMPT_SUGGESTION]
