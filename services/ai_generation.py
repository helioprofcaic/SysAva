# import google.generativeai as genai
import google.generativeai as genai
from google.api_core.exceptions import PermissionDenied
import sys
import json
import re
import time
import os
import openai
import requests # Adicionamos a biblioteca requests

# NOTA: Para usar o modelo local, a biblioteca 'openai' é necessária.
# Adicione 'openai' ao seu arquivo requirements.txt.
# Ex: pip install openai

# Classe mock para compatibilidade de resposta entre diferentes modelos
class MockResponse:
    def __init__(self, text):
        self.text = text

def configure_api(api_key):
    """Configura a API do Gemini."""
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        return False

# Modelos prioritários para CPU (ordenados por desempenho em hardware sem GPU dedicada)
PRIORITY_MODELS = [
    "jan-v3.5-4b",           # 4B — equilíbrio velocidade/qualidade
    "jan-v3_5-4b",
    "qwen3-4b-instruct-2507",
    "qwen3-4b-instruct",
    "phi-4-mini-reasoning",
    "gemma-3n-e4b-it-text",
    "gemma-4-e4b",
]

def _select_best_model(available_models):
    """Seleciona o melhor modelo disponível baseado em prioridade de desempenho."""
    model_ids = [m["id"] for m in available_models]
    # Prioriza modelos da lista de prioridade
    for priority in PRIORITY_MODELS:
        for model_id in model_ids:
            if priority in model_id:
                return model_id
    # Fallback: primeiro modelo da lista
    return model_ids[0] if model_ids else "local-model"


def generate_content_local_openai_compatible(prompt: str, port: int, server_name: str):
    """
    Gera conteúdo usando um servidor local compatível com a API da OpenAI (Jan, LM Studio, Llama Serve).
    Otimizado para modelos 4B em CPU (Jan 3.5 4B é o padrão recomendado).
    """
    try:
        # Descobre e seleciona o melhor modelo disponível
        model_name = "local-model"
        try:
            models_response = requests.get(f"http://localhost:{port}/v1/models")
            if models_response.status_code == 200:
                models_data = models_response.json()
                if models_data.get("data"):
                    model_name = _select_best_model(models_data["data"])
        except requests.RequestException:
            pass

        client = openai.OpenAI(base_url=f"http://localhost:{port}/v1", api_key="local-key")
        
        # System message para instruções, User message para conteúdo
        # Otimizado para modelos 4B (Jan 3.5, Qwen3, etc.)
        
        system_message = """Você é um assistente especialista em criar planos de aula.
Responda APENAS com o plano de aula em Markdown, sem explicações adicionais."""
        
        # Remove as instruções críticas do prompt (já estão no system)
        user_content = prompt
        if "INSTRUÇÕES CRÍTICAS" in prompt:
            # Pega tudo depois de "Você é"
            idx = prompt.find("Você é")
            if idx > 0:
                user_content = prompt[idx:]
            else:
                # Remove linhas de instrução e pega o resto
                lines = prompt.split('\n')
                user_lines = [l for l in lines if not any(x in l for x in ["NUNCA inclua", "NUNCA mostre", "Responda DIRETAMENTE", "Sua resposta deve"])]
                user_content = '\n'.join(user_lines)
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_content}
        ]

        # Parâmetros otimizados para DeepSeek R1
        extra_params = {
            "temperature": 0.7,
            "top_p": 0.9,
            "frequency_penalty": 0.3,
            "presence_penalty": 0.3,
        }

        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=False,
            **extra_params
        )
        
        response_text = completion.choices[0].message.content
        
        # Remove tags de thinking que possam vazar
        response_text = re.sub(r'<think>.*?</think>', '', response_text, flags=re.DOTALL | re.IGNORECASE)
        response_text = re.sub(r'<think>.*$', '', response_text, flags=re.MULTILINE | re.IGNORECASE)
        response_text = re.sub(r'^(Okay|Let me|Hmm|Alright|So|Now|First).*?\n', '', response_text, flags=re.MULTILINE | re.IGNORECASE)
        response_text = re.sub(r'\n{3,}', '\n\n', response_text).strip()
        
        return MockResponse(response_text)

    except openai.APIConnectionError as e:
        error_message = (
            f"**ERRO: Não foi possível conectar ao {server_name} em http://localhost:{port}.**\n\n"
            f"Verifique se o servidor local está rodando e ativo na porta {port}.\n\n"
            f"*Detalhes técnicos: {e}*"
        )
        return MockResponse(error_message)
    except openai.APIStatusError as e: # Captura o erro específico de status da API (ex: 500)
        if e.status_code == 500 and 'failed to load' in str(e.response.text):
            error_message = (
                f"**ERRO: O servidor {server_name} falhou ao carregar o modelo.**\n\n"
                f"O servidor reportou que não conseguiu carregar o modelo `{model_name}`. Verifique no aplicativo se:\n"
                f"1. O modelo está completamente baixado e não está corrompido.\n"
                f"2. Seu computador tem memória RAM e VRAM suficientes para carregar este modelo.\n"
                f"3. Tente reiniciar o servidor do Jan ou recarregar o modelo.\n\n"
                f"*Detalhes técnicos: {e}*"
            )
        else:
            error_message = (
                f"**ERRO inesperado do servidor {server_name}.**\n\n"
                f"*Detalhes técnicos: {e}*"
            )
        return MockResponse(error_message)
    except Exception as e:
        error_message = (
            f"**ERRO inesperado ao chamar o modelo local ({server_name}).**\n\n"
            f"*Detalhes técnicos: {e}*"
        )
        return MockResponse(error_message)
# def generate_content_with_fallback(prompt, model_names=["gemini-3.1-flash-lite-preview",
#                                                         "gemini-2.5-flash", 
#                                                         "gemini-2.5-pro", 
#                                                         "gemini-2.0-flash",
#                                                         "gemini-2.5-flash-lite",
#                                                         "gemini-flash-latest", 
#                                                         "gemini-3-flash-preview"]):
def generate_content_with_mimo(prompt: str):
    """
    Gera conteúdo usando o MiMo (assistente de IA).
    Tenta chamar via script Python/PowerShell; fallback: salva prompt para uso manual.
    """
    import subprocess
    import tempfile

    # Instrução crítica: MiMo deve retornar APENAS o conteúdo, sem salvar arquivos
    mimo_prompt = (
        "INSTRUÇÃO OBRIGATÓRIA: Responda APENAS com o conteúdo solicitado em Markdown. "
        "NÃO salve arquivos. NÃO crie relatórios. NÃO descreva o que fez. "
        "Apenas retorne o texto final.\n\n"
        f"{prompt}"
    )

    script_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")
    call_mimo_script = os.path.join(script_dir, "call_mimo.py")

    # Salva prompt em arquivo temporário
    tmp_file = os.path.join(tempfile.gettempdir(), "mimo_prompt.txt")
    with open(tmp_file, "w", encoding="utf-8") as f:
        f.write(mimo_prompt)

    # Tenta via script Python wrapper
    if os.path.isfile(call_mimo_script):
        try:
            result = subprocess.run(
                [sys.executable, call_mimo_script, "--file", tmp_file],
                capture_output=True, text=True, timeout=180,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            if result.returncode == 0 and result.stdout.strip():
                response = result.stdout.strip()
                # Remove possíveis cabeçalhos de agente
                response = _clean_mimo_response(response)
                return MockResponse(response)
        except Exception:
            pass

    return MockResponse(
        f"**MiMo não pôde ser chamado automaticamente.**\n\n"
        f"Prompt salvo em: `{tmp_file}`\n\n"
        f"Execute no terminal:\n```\npython scripts/call_mimo.py --file \"{tmp_file}\"\n```"
    )


def _clean_mimo_response(text: str) -> str:
    """Limpa a resposta do MiMo, removendo metadados de agente."""
    import re
    # Remove linhas que são apenas status de agente
    lines = text.split('\n')
    cleaned = []
    skip_patterns = [
        r'^>?\s*(build|model|agent|tool|file|write|read|edit)',
        r'^\[0m',
        r'^\s*$',
    ]
    for line in lines:
        skip = False
        for pattern in skip_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                skip = True
                break
        if not skip:
            cleaned.append(line)
    return '\n'.join(cleaned).strip()


def generate_content_with_fallback(prompt, model_names=None):
    """Tenta gerar conteúdo usando uma lista de modelos em sequência."""
    if model_names is None:
        # Prioriza modelos com janelas de contexto maiores se o prompt for grande
        if len(prompt) > 15000:
             model_names = [ "gemini-2.5-flash-lite","gemini-1.5-pro-latest", "gemini-1.5-flash-latest", "gemini-pro"]
        else:
             model_names = ["gemini-3-flash-preview","gemini-1.5-flash-latest", "gemini-pro", "gemini-1.0-pro"]

    last_error = None
    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response
        except PermissionDenied as e: # Captura o erro de autenticação primeiro
            error_message = (
                "**ERRO DE AUTENTICAÇÃO COM O GEMINI**\n\n"
                "A API Key do Google Gemini configurada é inválida ou não tem permissão.\n\n"
                "**Ação Necessária:**\n"
                "1. Verifique se a chave foi copiada corretamente no arquivo `.streamlit/secrets.toml`.\n"
                "2. Acesse o Google AI Studio e gere uma nova chave se necessário.\n\n"
                f"*Detalhes técnicos: {e.__class__.__name__}*"
            )
            return MockResponse(error_message)
        except Exception as e:
            last_error = e
            if "429" in str(e):
                time.sleep(2) # Pequena pausa se der rate limit, mas no UI o ideal é avisar
            # Continua para o próximo modelo da lista
            continue
    
    return MockResponse(f"**ERRO GERAL DO GEMINI**\n\nFalha ao gerar conteúdo após tentar todos os modelos.\n\n*Último erro: {last_error}*")

def _extract_text_from_file(filepath):
    """Extrai texto de arquivos .txt, .md e tenta extrair de .pdf."""
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()
    
    try:
        if ext == '.pdf':
            try:
                import pypdf
                reader = pypdf.PdfReader(filepath)
                return "\n".join([page.extract_text() for page in reader.pages])
            except ImportError:
                return f"[PDF detectado ({os.path.basename(filepath)}), mas a biblioteca 'pypdf' não está instalada.]"
            except Exception as e:
                return f"[Erro ao ler PDF: {e}]"
        else:
            # Tenta ler como texto (md, txt, etc)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
    except Exception as e:
        return f"[Erro ao ler arquivo {os.path.basename(filepath)}: {e}]"

def get_repo_context(subject_name):
    """Busca arquivos relevantes na pasta data/repo baseados no nome da disciplina."""
    repo_path = os.path.join("data", "repo")
    if not os.path.exists(repo_path):
        return ""

    context_parts = []
    # Palavras-chave simples para filtrar arquivos (ignora palavras curtas)
    keywords = [w.lower() for w in subject_name.split() if len(w) > 3]
    
    # Lista de pastas para buscar contexto (Repo oficial e Exemplos práticos)
    search_paths = [repo_path, os.path.join("data", "examples")]
    
    for base_path in search_paths:
        if not os.path.exists(base_path):
            continue
            
        for root, _, files in os.walk(base_path):
            for file in files:
                # Filtra arquivos relevantes: código python, markdown, feature files
                if any(k in file.lower() for k in keywords) or file.endswith(('.py', '.feature', '.md', '.java')):
                    # Se a palavra chave estiver no nome ou se for um arquivo de exemplo da semana
                    # (Refinamento: se for .py/.feature, incluímos para dar contexto prático)
                    if any(k in file.lower() for k in keywords) or "src_" in file or "test_" in file or "spec_" in file or file.endswith('.java'):
                        filepath = os.path.join(root, file)
                        content = _extract_text_from_file(filepath)
                        if content.strip():
                            context_parts.append(f"--- CONTEXTO ({os.path.basename(base_path)}): {file} ---\n{content}\n")
    
    return "\n".join(context_parts)

def parse_cronograma(cronograma_text):
    """
    Usa o Gemini para ler o texto do cronograma e estruturar os dados.
    """
    prompt = f"""
    Analise o seguinte texto de um cronograma de aulas e extraia a estrutura de aulas.
    - Sua tarefa é identificar cada aula individualmente.
    - Se encontrar um intervalo de aulas (ex: "Aulas 3-6: Tema X"), você deve expandi-lo para aulas individuais (Aula 3: Tema X, Aula 4: Tema X, etc.).
    - Ignore completamente linhas que são apenas comentários, anúncios de recesso, feriados, ou títulos de seção que não definem uma aula.
    - Para cada aula, extraia o NÚMERO da aula e o TEMA.
    - Identifique a SEMANA (week) de cada aula. Se o texto fornecer datas, use-as para agrupar as aulas por semana. Se não houver datas, infira a semana: considere que disciplinas de 40h tem 8 aulas/semana e as de 80h tem 10 aulas/semana. Use o número da aula para agrupar sequencialmente (ex: Aulas 1-8 são semana 1, 9-16 semana 2, etc., para um ritmo de 8 aulas/semana).

    Retorne APENAS um JSON (sem markdown, sem aspas triplas) com uma lista de objetos. Cada objeto representa UMA aula e deve ter o seguinte formato:
    [
        {{
            "week": int,
            "lesson_number": int,
            "topic": "string"
        }}
    ]

    Texto do Cronograma a ser analisado:
    {cronograma_text}
    """
    
    response = generate_content_with_fallback(prompt)
    
    if not response:
        return []

    try:
        text_resp = response.text.strip()
        if text_resp.startswith("```"):
            text_resp = re.sub(r"^```json|^```", "", text_resp).strip()
            text_resp = re.sub(r"```$", "", text_resp).strip()
        return json.loads(text_resp)
    except Exception:
        return []

def generate_lesson_markdown(subject, class_name, topic, lesson_num, school_name, professor_name):
    """
    Gera o conteúdo da aula em Markdown usando o Gemini.
    """
    
    # Carrega contexto do repositório se disponível
    repo_context = get_repo_context(subject)
    context_instruction = ""
    if repo_context:
        context_instruction = f"\n\nCONTEXTO ADICIONAL (Ementas/Materiais encontrados no repositório):\n{repo_context}\nUse estas informações para garantir que o conteúdo esteja alinhado com a ementa oficial."

    prompt = f"""
    Atue como o Professor {professor_name} de Desenvolvimento de Sistemas - Curso Técnico.
    Público-Alvo: Estudantes adolescentes de escola pública (Ensino Médio Integrado). Use uma linguagem acessível, motivadora, com analogias do cotidiano e cultura pop, evitando termos excessivamente acadêmicos sem explicação.
    
    Crie o conteúdo de uma aula em formato Markdown seguindo ESTRITAMENTE o modelo abaixo.

    Variáveis:
    - Número da Aula: {lesson_num}
    - Tema: {topic}
    - Turma: {class_name}
    - Disciplina: {subject}
    {context_instruction}

    Instruções Visuais (Importante para engajamento):
    1. Use Emojis (🚀, 💡, 💻, ⚠️) generosamente para estruturar tópicos e quebrar blocos de texto.
    2. **ILUSTRAÇÕES VETORIAIS (SVG)**: 
       - Para explicar conceitos visuais (fluxogramas, arquiteturas, esquemas elétricos), **GERE O CÓDIGO SVG** (<svg>...</svg>) diretamente no corpo do texto.
       - O SVG deve ser responsivo (use `viewBox`), com cores vibrantes e estilo didático/lúdico.
       - **IMPORTANTE:** O código SVG deve ser inserido como HTML puro, SEM blocos de código markdown (sem ``` ou `).
       - Certifique-se de que há uma linha em branco ANTES e DEPOIS da tag <svg> para garantir a renderização correta e evitar conflitos de formatação.
    3. Use formatação Markdown (negrito, listas, code blocks) para tornar a leitura dinâmica.
    4. **TABELAS**: Use tabelas em Markdown para comparar conceitos ou listar dados de forma estruturada.

    Modelo de Saída (Markdown):
    # 🎨 Aula {lesson_num}: {topic}

    **🏫 Escola:** {school_name}  
    **👨‍🏫 Professor:** {professor_name}  
    **🎓 Turma:** {class_name}
    **📚 Componente:** {subject}  

    ---

    ## 📑 Sumário
    1. 🏁 Introdução
    2. 🎯 Objetivos
    3. 💡 Conteúdo
    4. 📖 Glossário
    5. 🛠️ Atividade Prática
    6. 🎬 Para Pesquisar (Vídeos)
    7. 📝 Quiz

    ---

    ## 🏁 Introdução
    (Breve introdução ao tema)

    ## 🎯 Objetivos
    (Liste 3 objetivos claros)
    
    ## 💡 Conteúdo
    (Explicação detalhada, didática, com exemplos práticos ou de código se for programação)
    
    ## 📖 Glossário
    (Definição de termos chave)

    ## 🛠️ Atividade Prática
    (Exercícios ou exemplos práticos)

    ## 🎬 Para Pesquisar (Vídeos)
    (Sugira 3 vídeos do YouTube sobre o tema, com título e link. Ex: - [Título do Vídeo](https://youtube.com/watch?v=...))

    ---
    ## 📝 Quiz Aula: {lesson_num} - {topic}

    (Crie 4 perguntas de múltipla escolha, cada uma com 4 alternativas. Para cada pergunta, marque a resposta correta com um [x] e as incorretas com [ ]. Exemplo: - [x] Opção correta)
    
    ---
    ## Gabarito Comentado
    (Breve explicação da resposta correta)
    """
    
    response = generate_content_with_fallback(prompt)
    
    if response:
        content = str(response.text)
        
        # Limpeza profunda de SVGs para evitar "envenenamento" do banco de dados
        content = content.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#x27;', "'")
        
        # Remove linkificação de namespace (xmlns="url")
        content = re.sub(r'xmlns\s*=\s*["\']?\[(http.*?)\]\(.*?\)\s*["\']?', r'xmlns="\1"', content, flags=re.IGNORECASE)
        
        # Remove blocos de código markdown residuais e isola o SVG
        content = re.sub(r'```(?:html|xml|svg)?\s*(<svg.*?</svg>)\s*```', r'\1', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'(<svg.*?</svg>)', r'\n\n\1\n\n', content, flags=re.DOTALL | re.IGNORECASE)

        content = re.sub(r'\n{3,}', '\n\n', content)
        return content
    
    return None