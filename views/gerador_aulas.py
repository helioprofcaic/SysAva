import streamlit as st
import os
import re
from services.generate_lessons_gemini import GeradorAulaGemini, DATA_DIR
from services.ai_generation import generate_content_with_fallback, generate_content_local_lm_studio, configure_api

def show_page():
    st.header("🎓 Gerador de Planos de Aula (Gemini)")
    st.markdown("---")

    # --- SIDEBAR: Configurações ---
    with st.sidebar:
        st.divider()
        st.header("⚙️ Configuração do Gerador")
        
        modo_operacao = st.radio(
            "Fonte de Contexto:",
            ("📂 Arquivos da Pasta (Rota 2)", "📝 Lista de Cronograma (Rota 1)"),
            help="Rota 2 lê PDFs e Links da pasta da turma. Rota 1 lê o arquivo 'lista de aulas.txt'."
        )
        
        usar_arquivos = "Rota 2" in modo_operacao

        st.divider()
        st.header("🤖 Modelo de IA")
        
        ia_source_option = st.radio(
            "Escolha o modelo de IA:",
            ("Google Gemini (Nuvem)", "Modelo Local (LM Studio)"),
            help="Use o Gemini para maior qualidade ou um modelo local para privacidade e uso offline (requer LM Studio rodando em localhost:1234)."
        )
        
        ia_source = "local" if "Modelo Local" in ia_source_option else "gemini"
        
        api_key_gemini = None
        if ia_source == "gemini":
            api_key_gemini = st.text_input("Chave de API do Google Gemini", type="password", help="Necessária para usar o Gemini.")

        st.subheader("Seleção")
        
        # Tenta listar as Turmas disponíveis na pasta data/Turmas
        path_turmas = os.path.join(DATA_DIR, "Turmas")
        turmas_disponiveis = []
        if os.path.exists(path_turmas):
            turmas_disponiveis = [d for d in os.listdir(path_turmas) if os.path.isdir(os.path.join(path_turmas, d))]
        
        turma_selecionada = st.selectbox("Turma", ["Selecione..."] + turmas_disponiveis)
        
        # Tenta listar Disciplinas dentro da Turma
        disciplinas_disponiveis = []
        if turma_selecionada and turma_selecionada != "Selecione...":
            path_disciplinas = os.path.join(path_turmas, turma_selecionada)
            if os.path.exists(path_disciplinas):
                disciplinas_disponiveis = [d for d in os.listdir(path_disciplinas) if os.path.isdir(os.path.join(path_disciplinas, d))]
        
        disciplina_selecionada = st.selectbox("Disciplina", ["Selecione..."] + disciplinas_disponiveis)
        
        c_sem, c_aula = st.columns(2)
        with c_sem:
            semana = st.number_input("Semana (Pasta)", min_value=1, max_value=50, value=1)
        with c_aula:
            numero_aula = st.number_input("Nº Aula", min_value=0, max_value=200, value=1, help="Defina 0 para listar arquivos da pasta da semana manualmente.")

    # --- ÁREA PRINCIPAL ---
    # Removido o st.columns para um layout de coluna única, melhorando a legibilidade.

    # Inicializa o estado para armazenar o contexto
    if 'gerador_contexto' not in st.session_state:
        st.session_state.gerador_contexto = None

    # Novo estado para armazenar arquivos encontrados antes de ler
    if 'arquivos_encontrados' not in st.session_state:
        st.session_state.arquivos_encontrados = None

    st.info("ℹ️ **Como funciona:**\n\n1. Selecione os filtros e clique em **Buscar Contexto**.\n2. Selecione os arquivos desejados (Rota 2).\n3. Clique em **Gerar Plano de Aula**.")
    
    # Sobrescrita de modo para Aula 0
    if numero_aula == 0:
        usar_arquivos = True
        st.caption("📂 **Modo Manual Ativado:** Aula 0 selecionada. O sistema listará todos os arquivos da semana para seleção.")

    # Validação Básica
    pode_buscar = True
    if turma_selecionada == "Selecione..." or disciplina_selecionada == "Selecione...":
        st.warning("Selecione Turma e Disciplina para continuar.")
        pode_buscar = False

    # Etapa 1: Buscar o contexto
    label_botao = "1. Listar Arquivos Disponíveis" if usar_arquivos else "1. Buscar Contexto (Cronograma)"
    
    if st.button(label_botao, disabled=not pode_buscar, use_container_width=True):
        # Limpa estados anteriores
        st.session_state.gerador_contexto = None
        st.session_state.arquivos_encontrados = None
        if 'aula_gerada' in st.session_state: del st.session_state['aula_gerada']

        with st.spinner("Buscando..."):
            gerador = GeradorAulaGemini()
            
            if usar_arquivos:
                # ROTA 2: Apenas lista primeiro
                arquivos_data, erro = gerador.listar_arquivos_aula(turma_selecionada, disciplina_selecionada, semana)
                if erro:
                    st.error(erro)
                else:
                    st.session_state.arquivos_encontrados = arquivos_data
            else:
                # ROTA 1: Carrega direto do txt
                contexto = gerador.obter_contexto_aula(
                    turma=turma_selecionada,
                    disciplina=disciplina_selecionada,
                    semana=semana,
                    numero_aula=numero_aula,
                    usar_arquivos=False
                )
                st.session_state.gerador_contexto = contexto

    # Etapa Intermediária (Apenas Rota 2): Seleção de Arquivos
    if usar_arquivos and st.session_state.arquivos_encontrados:
        data_arq = st.session_state.arquivos_encontrados
        todos = data_arq.get('todos', [])
        sugeridos = data_arq.get('sugeridos', [])

        if not todos:
            st.warning("Pasta encontrada, mas vazia.")
        else:
            st.markdown("### 📂 Selecione os arquivos para a aula:")
            
            # Cria um multiselect com os sugeridos pré-selecionados
            # Exibe apenas o nome do arquivo, mas retorna o caminho completo
            mapa_nomes = {os.path.basename(p): p for p in todos}
            default_nomes = [os.path.basename(p) for p in sugeridos]
            
            selecionados_nomes = st.multiselect(
                "Arquivos disponíveis na pasta da semana:",
                options=list(mapa_nomes.keys()),
                default=default_nomes
            )
            
            caminhos_finais = [mapa_nomes[nome] for nome in selecionados_nomes]

            if st.button("Confirmar Seleção e Ler Conteúdo", use_container_width=True):
                with st.spinner("Lendo arquivos..."):
                    gerador = GeradorAulaGemini()
                    st.session_state.gerador_contexto = gerador.processar_arquivos_selecionados(caminhos_finais)

    # Exibe o contexto encontrado
    if st.session_state.gerador_contexto is not None:
        with st.expander("🔍 Contexto Encontrado (Material Base para a IA)", expanded=True):
            st.text_area("Conteúdo extraído dos arquivos:", st.session_state.gerador_contexto, height=250)

        # Etapa 2: Gerar a aula com base no contexto
        if st.button("2. Gerar Plano de Aula com IA", disabled=(st.session_state.gerador_contexto is None), use_container_width=True):
            if ia_source == "gemini" and not api_key_gemini:
                st.error("Por favor, insira sua Chave de API do Google Gemini na barra lateral.")
            else:
                spinner_text = "Conectando ao modelo local e gerando aula..." if ia_source == "local" else "Analisando contexto e gerando aula com Gemini..."
                with st.spinner(spinner_text):
                    try:
                        gerador = GeradorAulaGemini()
                        school_name_ui = gerador.obter_nome_escola()

                        # Pega o nome do professor logado na sessão (ou usa padrão se offline/não logado)
                        professor_name_ui = st.session_state.get('usuario', "Professor(a) Assistente")
                        
                        contexto_para_ia = st.session_state.gerador_contexto

                        # Adiciona lógica de truncamento para modelos locais
                        if ia_source == "local":
                            # Modelos locais geralmente têm janelas de contexto menores (ex: 4096 tokens).
                            # O prompt em si consome tokens, então limitamos o contexto para evitar erros.
                            # 1 token ~ 3-4 caracteres. 2500 tokens de contexto ~ 9000 caracteres.
                            MAX_CHARS_CONTEXTO_LOCAL = 9000
                            if len(contexto_para_ia) > MAX_CHARS_CONTEXTO_LOCAL:
                                st.warning(f"⚠️ O contexto era muito longo para o modelo local e foi truncado para {MAX_CHARS_CONTEXTO_LOCAL} caracteres para evitar erros.")
                                contexto_para_ia = contexto_para_ia[:MAX_CHARS_CONTEXTO_LOCAL] + "\n\n[... CONTEÚDO TRUNCADO ...]"
                        
                        prompt = gerador.gerar_prompt_aula(
                            turma=turma_selecionada,
                            disciplina=disciplina_selecionada,
                            semana=semana,
                            contexto_str=contexto_para_ia,
                            school_name=school_name_ui,
                            professor_name=professor_name_ui,
                            numero_aula=numero_aula
                        )
                        
                        st.session_state['last_prompt'] = prompt
                        
                        if ia_source == "local":
                            response = generate_content_local_lm_studio(prompt)
                        else: # Gemini
                            configure_api(api_key_gemini)
                            response = generate_content_with_fallback(prompt)
                        
                        if response and hasattr(response, 'text'):
                            st.session_state['aula_gerada'] = response.text
                            st.success("Aula gerada com sucesso!")
                        else:
                            st.error("Falha ao receber resposta da IA. Verifique a API Key, cotas ou a conexão com o servidor local.")
                            
                    except Exception as e:
                        st.error(f"Ocorreu um erro: {str(e)}")

    st.divider()

    # Abas para Visualização do resultado final
    if 'aula_gerada' in st.session_state or ('last_prompt' in st.session_state and st.session_state.gerador_contexto is not None):
        tab_aula, tab_debug = st.tabs(["📄 Plano de Aula", "🔍 Contexto (Debug)"])
        
        with tab_aula:
            if 'aula_gerada' in st.session_state:
                conteudo_aula = st.session_state['aula_gerada']
                st.markdown(conteudo_aula)
                
                # Lógica para extrair nome do arquivo
                nome_arquivo = f"Aula_{numero_aula:02d}_{disciplina_selecionada}.md" # Default
                
                # Tenta extrair o título H1 (# Título)
                titulo_match = re.search(r'(?m)^#\s+(.+)', conteudo_aula)
                if titulo_match:
                    raw_title = titulo_match.group(1).strip()
                    # Remove emojis
                    emoji_pattern = re.compile("["
                                           u"\U0001F600-\U0001F64F"
                                           u"\U0001F300-\U0001F5FF"
                                           u"\U0001F680-\U0001F6FF"
                                           u"\U0001F1E0-\U0001F1FF"
                                           "]+", flags=re.UNICODE)
                    clean_title = emoji_pattern.sub('', raw_title).strip()
                    # Remove caracteres inválidos de arquivo
                    safe_title = re.sub(r'[\\/*?:"<>|]', "", clean_title).strip().rstrip('.')
                    if safe_title:
                        nome_arquivo = f"{safe_title}.md"
                
                st.download_button(
                    label="💾 Baixar Plano (.md)",
                    data=conteudo_aula,
                    file_name=nome_arquivo,
                    mime="text/markdown"
                )
            else:
                st.info("Clique em 'Gerar Plano de Aula com IA' para ver o resultado aqui.")
        
        with tab_debug:
            st.caption("Aqui você vê o prompt exato enviado para a IA, incluindo o contexto recuperado dos arquivos.")
            if 'last_prompt' in st.session_state:
                st.text_area("Prompt Enviado", st.session_state['last_prompt'], height=600)
            else:
                st.write("Nenhum prompt gerado ainda.")

    # Rodapé com verificação de pastas
    st.markdown("---")
    if usar_arquivos and disciplina_selecionada != "Selecione...":
        caminho_esp = os.path.join(DATA_DIR, "Turmas", turma_selecionada, disciplina_selecionada, f"S{semana:02d}", "seductec")
        if os.path.exists(caminho_esp):
            st.caption(f"✅ Pasta encontrada: `{caminho_esp}`")
        else:
            st.caption(f"❌ Pasta não encontrada: `{caminho_esp}` (Certifique-se que ela existe para a Rota 2)")

        
    