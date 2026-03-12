import google.generativeai as genai
import json
import re
import time
import os

def configure_api(api_key):
    """Configura a API do Gemini."""
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        return False

def generate_content_with_fallback(prompt, model_names=["gemini-3.1-flash-lite-preview",
                                                        "gemini-2.5-flash", 
                                                        "gemini-2.5-pro", 
                                                        "gemini-2.0-flash",
                                                        "gemini-2.5-flash-lite",
                                                        "gemini-flash-latest", 
                                                        "gemini-3-flash-preview"]):
    """Tenta gerar conteúdo usando uma lista de modelos em sequência."""
    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response
        except Exception as e:
            if "429" in str(e):
                time.sleep(2) # Pequena pausa se der rate limit, mas no UI o ideal é avisar
                continue
            continue
    return None

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
    
    for root, _, files in os.walk(repo_path):
        for file in files:
            if any(k in file.lower() for k in keywords):
                filepath = os.path.join(root, file)
                content = _extract_text_from_file(filepath)
                if content.strip():
                    context_parts.append(f"--- CONTEXTO DO ARQUIVO: {file} ---\n{content}\n")
    
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
        return response.text
    
    return None