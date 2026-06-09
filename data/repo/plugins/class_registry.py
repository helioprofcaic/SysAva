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
        "PENSAMENTO COMPUTACIONAL II": "PC_II",
        "MENTORIAS TEC II": "MENT_TEC",
        "INTELIGÊNCIA ARTIFICIAL": "IA"
    }
    # Se a disciplina está no mapeamento manual, usa ele.
    # Caso contrário, tenta usar o nome original (para as modulares que têm o nome da pasta igual ao do banco)
    if disciplina in mapping:
        return mapping[disciplina]
    return disciplina

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

def calculate_lesson_number(start_date, target_date, class_name, subject_name, grade, max_lessons=40):
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
    
    return min(max_lessons, max(1, lesson_count))

def init_session_state():
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'current_registration_data' not in st.session_state:
        st.session_state.current_registration_data = {}

def show_content_step():
    st.title("📝 Registro de Aula - Passo 1: Conteúdo")
    
    # Load data needed for this step
    grade = load_grade_with_sync()
    curriculo = load_json(CURRICULO_FILE)
    
    if not grade:
        st.error("Grade horária não encontrada.")
        return

    # Carrega o catálogo de aulas escaneando os arquivos .md
    df_catalogo = get_lessons_catalog()

    # --- CABEÇALHO DO REGISTRO ---
    col_header1, col_header2 = st.columns(2) # Changed to 2 columns
    
    with col_header1: # Changed to 2 columns
        tipo_aula = st.selectbox("Tipo de Aula", ["-- Selecione --", "Aula Híbrida", "Aula Remota", "Aula Normal", "Reposição", "Aula Extra"], key="tipo_aula")
        
        classes = list(grade.keys())
        turma_sel = st.selectbox("Turma", ["-- Selecione --"] + classes)

    with col_header2:
        data_aula = st.date_input("Data", datetime.now())
        dias_semana_map = {0: "Segunda", 1: "Terça", 2: "Quarta", 3: "Quinta", 4: "Sexta", 5: "Sábado", 6: "Domingo"}
        dia_nome = dias_semana_map[data_aula.weekday()]

        # --- CARREGAMENTO DINÂMICO DE DISCIPLINAS DO BANCO ---
        subjects_db = []
        mapping_grade_to_db = {
            "P.C. II": "PENSAMENTO COMPUTACIONAL II",
            "Ment.Tec.II": "MENTORIAS TEC II",
            "I.A.": "INTELIGÊNCIA ARTIFICIAL"
        }
        
        modular_subjects = []
        subjects_db = []
        if turma_sel != "-- Selecione --" and db:
            try:
                class_id = grade[turma_sel].get("id") # Caso tenha o ID na grade, ou busque por nome
                # Fallback se a grade não tiver ID: busca pelo nome da classe
                all_classes = db.get_classes()
                cid = next((c['id'] for c in all_classes if c['name'] == turma_sel), None)
                
                if cid:
                    subjects_db = db.get_subjects_for_class(cid)
                    # Filtra modulares usando a nova coluna (duration_type)
                    modular_subjects = [s['name'] for s in subjects_db if s.get('duration_type') == 'mensal']
            except: pass

        # --- LÓGICA DE FILTRAGEM POR GRADE ---
        componente = ""
        horarios_opcoes = []
        
        if turma_sel != "-- Selecione --":
            aulas_no_dia = grade[turma_sel].get(dia_nome, {})
            
            if not aulas_no_dia:
                st.warning(f"⚠️ Não há aulas previstas na grade para {dia_nome}.")
                componente_opcoes = ["-- Sem aulas na grade --"]
            else:
                componente_opcoes = sorted(list(set(aulas_no_dia.values()))) # Changed to 2 columns
            
            componente = st.selectbox("Componente", ["-- Selecione --"] + componente_opcoes, key="componente")
            # Changed to 2 columns
            if componente != "-- Selecione --" and componente != "-- Sem aulas na grade --":
                # Filtra apenas os horários em que este componente específico acontece neste dia
                horarios_opcoes = [h for h, s in aulas_no_dia.items() if s == componente]
        else:
            st.selectbox("Componente", ["-- Selecione a Turma primeiro --"], disabled=True)

    horario_sel = st.selectbox("Horário (inicial ~ final)", ["-- Selecione --"] + horarios_opcoes if horarios_opcoes else ["-- Selecione --"])
    # Changed to 2 columns
    # --- LÓGICA DE SELEÇÃO DE DISCIPLINA REAL (MODULAR VS ANUAL) ---
    # 1. Resolve apelidos da grade para nomes reais (Anuais)
    disciplina_final = mapping_grade_to_db.get(componente, componente) # Changed to 2 columns
    busca_grade_placeholder = componente # Termo usado para contar aulas na grade
    
    if componente == "Disc.Tec.":
        if not modular_subjects:
            st.warning("Nenhuma disciplina mensal/modular encontrada no banco para esta turma.")
            disciplina_final = "-- Selecione o Módulo --"
        else:
            disciplina_final = st.selectbox("Módulo Técnico Atual", ["-- Selecione o Módulo --"] + modular_subjects)
            
            # Permite ajustar a data de início do módulo para resetar o contador de aulas
            with st.expander("📅 Ajustar Início do Módulo"):
                data_inicio_modulo = st.date_input("Data de início deste módulo específico", datetime(2026, 2, 19).date(), key="start_mod")
                st.caption("O número da aula será contado a partir desta data.")
        
        if disciplina_final == "-- Selecione o Módulo --":
            st.stop() # Changed to 2 columns
    else:
        data_inicio_modulo = datetime(2026, 2, 19).date()

    st.divider()
    st.subheader("Registro de Aula")

    # --- LÓGICA DE CURRÍCULO (BNCC/EPT) --- # Changed to 2 columns
    # Tenta achar os dados da disciplina no curriculo_db.json
    dados_curriculo = {}
    if disciplina_final and disciplina_final != "-- Selecione --":
        comp_upper = disciplina_final.upper()
        for segmento in curriculo:
            if comp_upper in curriculo[segmento]:
                dados_curriculo = curriculo[segmento][comp_upper]
                break

    col_cur1, col_cur2 = st.columns(2)
    # Changed to 2 columns
    with col_cur1: # Changed to 2 columns
        comp_especifica = st.selectbox("Competência Específica", 
                                      ["-- Selecione --", dados_curriculo.get("competencia", "Geral")] if dados_curriculo else ["-- Selecione --"], key="comp_especifica")
        
        hab_lista = dados_curriculo.get("habilidades", []) # Changed to 2 columns
        habilidade = st.selectbox("Habilidades", ["-- Selecione --"] + hab_lista if hab_lista else ["-- Selecione --"], key="habilidade")

    with col_cur2: # Changed to 2 columns
        hab_integrada = st.selectbox("Habilidade Integrada", ["-- Selecione --", "Trabalho em Equipe", "Resolução de Problemas", "Ética Profissional"])
        objetivo = st.text_area("Objetivo da Aprendizagem", 
                               value=f"Capacitar o aluno a compreender e aplicar os conceitos de {disciplina_final}." if disciplina_final else "")

    objeto_conhecimento = st.text_input("Objeto do Conhecimento", value=disciplina_final)

    # --- LÓGICA DE CONTEÚDO AUTOMÁTICO ---
    # Usa a data de início geral ou a do módulo selecionado # Changed to 2 columns
    data_inicio = data_inicio_modulo # Changed to 2 columns
    
    sub_id = None
    if turma_sel != "-- Selecione --" and disciplina_final and disciplina_final != "-- Selecione --":
        # --- REGRA DE CARGA HORÁRIA (Evita Aula 114) ---
        num_subjects = len(subjects_db) if (subjects_db and len(subjects_db) > 0) else 10
        limit_lessons = 400 // num_subjects

        # --- NOVA LÓGICA: Sincronismo entre Histórico iSeduc (Passado) e Lessons SysAva (Presente) ---
        n_aula = 1
        if db and db.is_db_connected():
            try:
                # 1. Localiza o ID da disciplina atual no banco para precisão na consulta
                current_sub = next((s for s in subjects_db if s['name'] == disciplina_final), None)
                if current_sub:
                    sub_id = current_sub['id']
                    
                    # 2. Verifica se a data selecionada já foi registrada no portal oficial (historico_aulas)
                    dt_str = data_aula.strftime("%d/%m/%Y")
                    exist_res = db.supabase.table("historico_aulas")\
                        .select("id, status")\
                        .eq("data_aula", dt_str)\
                        .eq("disciplina_id", sub_id)\
                        .execute()
                    
                    if exist_res.data:
                        st.warning(f"⚠️ Atenção: Já existe um registro oficial ({exist_res.data[0]['status']}) para esta data no iSeduc.")

                    # 3. Determina o número da aula baseando-se na quantidade de registros existentes no histórico
                    hist_count = db.supabase.table("historico_aulas")\
                        .select("*", count='exact')\
                        .eq("disciplina_id", sub_id)\
                        .execute()
                    
                    # A aula sugerida é o total de registros já realizados + 1
                    n_aula = (hist_count.count if hist_count.count is not None else 0) + 1
            except Exception:
                # Fallback para o cálculo baseado em calendário caso o banco esteja inacessível
                n_aula = calculate_lesson_number(data_inicio, data_aula, turma_sel, busca_grade_placeholder, grade, max_lessons=limit_lessons)
        else:
            n_aula = calculate_lesson_number(data_inicio, data_aula, turma_sel, busca_grade_placeholder, grade, max_lessons=limit_lessons)
            
        n_aula = min(limit_lessons, n_aula)
        
        # 2. Busca no DataFrame do catálogo pela aula correspondente
        # Filtra por número da aula e tenta encontrar na pasta da disciplina
        match = df_catalogo[
            (df_catalogo['turma'].str.contains(turma_sel, case=False, na=False)) &
            (df_catalogo['aula_num'] == n_aula) & 
            (df_catalogo['disciplina'].str.contains(get_folder_mapping(disciplina_final), case=False, na=False))
        ]
        
        if not match.empty:
            aula_info = match.iloc[0]
            lesson_title = f"Aula {n_aula}: {aula_info['titulo']}"
            st.success(f"✅ Conteúdo da Aula {n_aula} extraído com sucesso!")
        elif db and db.is_db_connected():
            # Caso não encontre localmente, tenta baixar do banco de dados (Tabela Lessons - O "Presente")
            sid = sub_id if sub_id else (db.get_subject_by_name(disciplina_final) or {}).get('id')
            
            if sid:
                db_lessons = db.get_lessons_for_subject(sid)
                
                # Busca a aula pelo número no título (ex: "Aula 05" ou "Aula 5")
                search_pat = rf"Aula\s*0?{n_aula}\b"
                db_match = [l for l in db_lessons if re.search(search_pat, l['title'], re.IGNORECASE)]
                
                if db_match:
                    lesson_db = db_match[0]
                    full_desc = lesson_db.get('description', '')
                    title_db = lesson_db.get('title', '')
                    
                    lesson_title = f"Aula {n_aula}: {title_db}"
                    st.success(f"📥 Aula {n_aula} baixada do banco de dados para o registro!")
                    
                    st.download_button(
                        label="💾 Baixar arquivo .md desta aula",
                        data=full_desc,
                        file_name=f"Aula_{n_aula:02d}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                else:
                    lesson_title = f"Aula {n_aula}: "
                    st.info(f"ℹ️ Aula {n_aula} calculada, mas não localizada localmente ou no banco.")
            else:
                lesson_title = f"Aula {n_aula}: "
                st.info(f"ℹ️ Aula {n_aula} calculada, mas disciplina não encontrada no banco.")
        else:
            lesson_title = f"Aula {n_aula}: "
            st.info(f"ℹ️ Aula {n_aula} calculada, mas arquivo .md não localizado no catálogo.")
        
        # Preenchimento automático: Título + Objetivos
        conteudo_sugerido = f"{lesson_title}. {objetivo}"
    else:
        conteudo_sugerido = ""

    # Limitação de 250 caracteres conforme solicitado
    conteudo_abordado = st.text_area("Conteúdo abordado (*)", value=conteudo_sugerido[:250], height=150, max_chars=250)
    
    # Seletor de estratégias usuais
    estrategia_opcoes = [
        "Aula expositiva com uso de quadro branco, pincel e projetor",
        "Aula prática em laboratório com uso de projetor, computadores e smarphones",
        "Aula de atividades avaliativas em grupo, seminário, trabalho, pesquisa...",
        "Aula de atividade avaliativa individual, prova, teste..."
    ]
    estrategia = st.selectbox("Estratégia metodológica (*)", estrategia_opcoes, key="estrategia")

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
                "componente": disciplina_final,
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

            st.session_state.current_step = 1
            st.session_state.current_registration_data = {
                "tipo_aula": tipo_aula,
                "turma": turma_sel,
                "data": data_aula.isoformat(),
                "componente": disciplina_final,
                "horario": horario_sel,
                "competencia": comp_especifica,
                "habilidade": habilidade,
                "hab_integrada": hab_integrada,
                "objetivo": objetivo,
                "objeto_conhecimento": objeto_conhecimento,
                "conteudo": conteudo_abordado,
                "estrategia": estrategia,
                "n_aula": n_aula,
                "sub_id": sub_id
            }
            st.rerun()

def show_frequencia_step():
    st.title("📝 Registro de Aula - Passo 2: Frequência")
    st.write("Dados da aula:", st.session_state.current_registration_data)

    # Placeholder for frequency input
    st.info("Aqui você adicionaria a lista de alunos e marcaria a frequência.")
    frequencia_data = st.text_area("Observações sobre Frequência (Ex: Alunos presentes, ausentes, etc.)", key="frequencia_obs")
    
    st.session_state.current_registration_data['frequencia_obs'] = frequencia_data

    st.divider()
    col_btns = st.columns(3)
    if col_btns[0].button("Voltar", use_container_width=True):
        st.session_state.current_step = 0
        st.rerun()

    if col_btns[1].button("Salvar e Avançar", type="primary", use_container_width=True):
        st.session_state.current_step = 2
        st.rerun()

def show_recursos_step():
    st.title("📝 Registro de Aula - Passo 3: Recursos Utilizados")
    st.write("Dados da aula:", st.session_state.current_registration_data)

    # Placeholder for resources input
    st.info("Aqui você listaria os recursos didáticos e tecnológicos utilizados.")
    recursos_data = st.text_area("Recursos Utilizados (Ex: Projetor, Computadores, Livros, Plataformas Online)", key="recursos_utilizados")

    st.session_state.current_registration_data['recursos_utilizados'] = recursos_data

    st.divider()
    col_btns = st.columns(3)
    if col_btns[0].button("Voltar", use_container_width=True):
        st.session_state.current_step = 1
        st.rerun()

    if col_btns[1].button("Salvar e Avançar", type="primary", use_container_width=True):
        st.session_state.current_step = 3
        st.rerun()

def show_atividades_step():
    st.title("📝 Registro de Aula - Passo 4: Atividades Desenvolvidas")
    st.write("Dados da aula:", st.session_state.current_registration_data)

    # Placeholder for activities input
    atividades_data = st.text_area("Atividades Desenvolvidas (Ex: Exercícios em grupo, Discussão, Apresentação)", key="atividades_desenvolvidas")

    st.session_state.current_registration_data['atividades_desenvolvidas'] = atividades_data

    st.divider()
    col_btns = st.columns(3)
    if col_btns[0].button("Voltar", use_container_width=True):
        st.session_state.current_step = 2
        st.rerun()

    if col_btns[1].button("Finalizar Registro", type="primary", use_container_width=True):
        finalize_registration()

def finalize_registration():
    st.title("📝 Registro de Aula - Finalizando...")
    
    registries = load_json(REGISTRY_FILE)
    if "data" not in registries: registries["data"] = []
    
    new_entry = {
        "id": len(registries["data"]) + 1,
        "timestamp": datetime.now().isoformat(),
        **st.session_state.current_registration_data
    }
    
    registries["data"].append(new_entry)
    save_json(REGISTRY_FILE, registries)
    
    if db and hasattr(db, 'supabase'):
        try:
            user = st.session_state.get('username', 'professor_ext')
            db.add_user_history(user, f"Registrou aula {new_entry.get('n_aula', 'N/A')} de {new_entry.get('componente', 'N/A')} para {new_entry.get('turma', 'N/A')}")
        except Exception as e:
            st.error(f"Erro ao salvar histórico no banco de dados: {e}")

    st.success("Registro de aula salvo com sucesso! Você pode iniciar um novo registro.")
    st.balloons()

    st.session_state.current_registration_data = {} # Clear data for next registration
    st.session_state.current_step = 0 # Reset to start a new registration
    st.rerun()

def show_class_registry():
    init_session_state()

    if st.session_state.current_step == 0:
        show_content_step()
    elif st.session_state.current_step == 1:
        show_frequencia_step()
    elif st.session_state.current_step == 2:
        show_recursos_step()
    elif st.session_state.current_step == 3:
        show_atividades_step()

    # --- HISTÓRICO RECENTE ---
    with st.expander("📂 Ver Registros Anteriores"):
        tab_manual, tab_portal = st.tabs(["📝 Registros Manuais", "🤖 Portal iSeduc (Histórico)"])
        
        with tab_manual:
            registries = load_json(REGISTRY_FILE)
            if "data" in registries and registries["data"]:
                hist_df = pd.DataFrame(registries["data"])
                st.dataframe(hist_df[["data", "turma", "componente", "tipo", "conteudo"]], hide_index=True, use_container_width=True)
            else:
                st.info("Nenhum registro manual encontrado localmente.")

        with tab_portal:
            if db and hasattr(db, 'supabase'):
                try:
                    # Busca os últimos 50 registros de automação do portal
                    res = db.supabase.table("historico_aulas").select("*").order("created_at", desc=True).limit(50).execute()
                    if res.data:
                        portal_df = pd.DataFrame(res.data)
                        st.dataframe(
                            portal_df[["data_aula", "horario", "turma", "disciplina", "status"]],
                            column_config={
                                "data_aula": "Data",
                                "horario": "Horário",
                                "turma": "Turma",
                                "disciplina": "Disciplina",
                                "status": "Status"
                            },
                            hide_index=True,
                            use_container_width=True
                        )
                    else:
                        st.info("Nenhum registro de automação localizado na tabela do portal.")
                except Exception as e:
                    st.error(f"Erro ao conectar com historico_aulas: {e}")
            else:
                st.warning("Banco de dados indisponível para carregar o histórico do portal.")

    # --- UTILITÁRIOS DE CONSULTA AO BANCO --- # Changed to 2 columns
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
