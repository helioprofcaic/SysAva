import os
import sys
import time
import re
from services.generate_lessons_gemini import GeradorAulaGemini, DATA_DIR
from services.ai_generation import generate_content_local_lm_studio, generate_content_with_fallback, configure_api

# Configuração Visual Simples
def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*60)
    print("🎓 GERADOR DE AULAS SYSAVA - MODO TERMINAL (LEVE)")
    print("="*60)
    print("Este modo economiza RAM ao não usar o navegador.")
    print("-" * 60)

def select_from_list(options, prompt_text):
    print(f"\n{prompt_text}")
    for i, opt in enumerate(options):
        print(f"[{i+1}] {opt}")
    
    while True:
        try:
            choice = int(input("\nDigite o número da opção: "))
            if 1 <= choice <= len(options):
                return options[choice-1]
            print("Opção inválida.")
        except ValueError:
            print("Digite apenas números.")

def select_multiple_from_list(options, prompt_text, suggested_options=[]):
    """Permite que o usuário selecione múltiplos itens de uma lista."""
    print(f"\n{prompt_text}")
    # Cria um mapa de nomes base para opções sugeridas para fácil verificação
    suggested_basenames = {os.path.basename(p) for p in suggested_options}

    for i, opt in enumerate(options):
        is_suggested = " (sugerido)" if os.path.basename(opt) in suggested_basenames else ""
        print(f"[{i+1}] {os.path.basename(opt)}{is_suggested}")
    
    print("\nDigite os números dos arquivos, separados por vírgula (ex: 1,3,5).")
    default_selection = "sugeridos" if suggested_options else "todos"
    print(f"Pressione Enter para usar os {default_selection}.")
    
    while True:
        try:
            choice_str = input("Sua seleção: ").strip()
            if not choice_str:
                return suggested_options if suggested_options else options

            indices = [int(i.strip()) - 1 for i in choice_str.split(',')]
            
            if all(0 <= i < len(options) for i in indices):
                return [options[i] for i in indices]
            print("Seleção inválida. Pelo menos um número está fora do intervalo.")
        except ValueError:
            print("Formato inválido. Use apenas números separados por vírgula.")

def main():
    gerador = GeradorAulaGemini()
    print_header()

    # 1. Configuração do Modelo
    print("\n[CONFIGURAÇÃO DE IA]")
    tipo_ia = select_from_list(["Modelo Local (LM Studio)", "Google Gemini (Nuvem)"], "Qual IA você quer usar?")
    
    api_key = None
    if "Gemini" in tipo_ia:
        api_key = input("Cole sua API Key do Gemini (ou Enter para tentar variável de ambiente): ").strip()
        if api_key:
            configure_api(api_key)
    else:
        print("\nCertifique-se que o LM Studio está rodando em http://localhost:1234")
        print("DICA: Para ser rápido com 16GB RAM, use modelos como 'Phi-3-mini' ou 'Gemma-2b'.")

    # 2. Seleção de Turma e Disciplina
    path_turmas = os.path.join(DATA_DIR, "Turmas")
    if not os.path.exists(path_turmas):
        print(f"Erro: Pasta {path_turmas} não encontrada.")
        return

    school_name = gerador.obter_nome_escola()

    turmas = [d for d in os.listdir(path_turmas) if os.path.isdir(os.path.join(path_turmas, d))]
    if not turmas:
        print("Nenhuma turma encontrada.")
        return
    
    turma = select_from_list(turmas, "Selecione a Turma:")
    
    path_disciplinas = os.path.join(path_turmas, turma)
    disciplinas = [d for d in os.listdir(path_disciplinas) if os.path.isdir(os.path.join(path_disciplinas, d))]
    if not disciplinas:
        print("Nenhuma disciplina encontrada nesta turma.")
        return
        
    disciplina = select_from_list(disciplinas, "Selecione a Disciplina:")
    
    # 3. Definição da Aula
    try:
        semana = int(input("\nDigite o número da Semana/Aula (ex: 1, 2...): "))
    except:
        semana = 1

    # 4. Modo de Contexto
    modo = select_from_list(["Ler Arquivos da Pasta (Rota 2)", "Ler Cronograma (Rota 1)"], "Fonte de Contexto:")
    usar_arquivos = "Rota 2" in modo

    contexto = ""

    print("\n🔄 Buscando contexto...")
    
    if usar_arquivos:
        # Listar arquivos primeiro
        arquivos_data, erro = gerador.listar_arquivos_aula(turma, disciplina, semana)
        if erro:
            print(f"Erro: {erro}")
            input("Pressione Enter para sair...")
            return
        
        todos = arquivos_data.get('todos', [])
        if not todos:
            print("Pasta vazia.")
            return

        sugeridos = arquivos_data.get('sugeridos', [])
        arquivos_para_ler = select_multiple_from_list(todos, "Selecione os arquivos para usar como contexto:", sugeridos)

        if not arquivos_para_ler:
            print("Nenhum arquivo selecionado. Abortando.")
            return
            
        print(f"\nLendo {len(arquivos_para_ler)} arquivo(s) selecionado(s)...")
        contexto = gerador.processar_arquivos_selecionados(arquivos_para_ler)
    else:
        contexto = gerador.obter_contexto_aula(turma, disciplina, semana, usar_arquivos=False)

    if not contexto or len(contexto) < 10:
        print("⚠️ Pouco ou nenhum contexto encontrado. A aula pode ficar genérica.")
    else:
        print(f"✅ Contexto carregado ({len(contexto)} caracteres).")

    # 5. Geração
    print("\n" + "="*60)
    print("🚀 INICIANDO GERAÇÃO DA AULA...")
    print("Isso pode demorar dependendo do seu computador.")
    print("="*60)

    # Truncamento preventivo para CLI
    if "Local" in tipo_ia and len(contexto) > 8000:
        print("⚠️ Contexto muito grande para IA Local. Truncando para 8000 caracteres...")
        contexto = contexto[:8000] + "\n[...truncado...]"

    prompt = gerador.gerar_prompt_aula(turma, disciplina, semana, contexto, school_name=school_name)
    
    start_time = time.time()
    response = None
    
    if "Local" in tipo_ia:
        response = generate_content_local_lm_studio(prompt)
    else:
        response = generate_content_with_fallback(prompt)
    
    elapsed = time.time() - start_time
    
    if response and hasattr(response, 'text'):
        # 1. Extrair o título do conteúdo gerado para nomear o arquivo
        # Usa (?m) para procurar em qualquer linha, não apenas na primeira
        titulo_match = re.search(r'(?m)^#\s+(.+)', response.text)
        
        if titulo_match:
            raw_title = titulo_match.group(1).strip()
            # Remove emojis e caracteres inválidos para nomes de arquivo
            emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
            clean_title = emoji_pattern.sub('', raw_title).strip()
            safe_title = re.sub(r'[\\/*?:"<>|]', "", clean_title).strip().rstrip('.')
            nome_arquivo = f"{safe_title}.md"
        else:
            # Fallback se não encontrar o título
            nome_arquivo = f"Aula_{semana:02d}_{disciplina.replace(' ', '_')}.md"

        # 2. Construir o caminho correto para salvar o arquivo
        semana_str = f"S{int(semana):02d}"
        pasta_semana = os.path.join(DATA_DIR, "Turmas", turma, disciplina, semana_str)
        os.makedirs(pasta_semana, exist_ok=True) # Cria a pasta se não existir
        caminho_saida = os.path.join(pasta_semana, nome_arquivo)
        
        with open(caminho_saida, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"\n✅ SUCESSO! Aula gerada em {elapsed:.1f} segundos.")
        print(f"📄 Arquivo salvo em: {caminho_saida}")
    else:
        print("\n❌ Falha na geração. Verifique o servidor do LM Studio.")

if __name__ == "__main__":
    main()
    input("\nPressione Enter para fechar...")