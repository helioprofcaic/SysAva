import google.generativeai as genai
import json
import re
import time

def configure_api(api_key):
    """Configura a API do Gemini."""
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        return False

def generate_content_with_fallback(prompt, model_names=["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash", "gemini-flash-latest"]):
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

def parse_cronograma(cronograma_text):
    """
    Usa o Gemini para ler o texto do cronograma e estruturar os dados.
    """
    prompt = f"""
    Analise o seguinte texto de um cronograma de aulas.
    Extraia a estrutura de aulas.
    Regra de inferência de Semanas: Geralmente as disciplinas possuem blocos de 8 ou 10 aulas por semana.
    Se as semanas não estiverem explicitamente numeradas no texto, deduza a semana (week) baseando-se nessa contagem sequencial.
    Retorne APENAS um JSON (sem markdown, sem aspas triplas) com o seguinte formato para cada aula identificada:
    [
        {{
            "week": int,
            "lesson_number": int,
            "topic": "string"
        }}
    ]

    Texto do Cronograma:
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

def generate_lesson_markdown(subject, class_name, topic, lesson_num):
    """
    Gera o conteúdo da aula em Markdown usando o Gemini.
    """
    prompt = f"""
    Atue como o Professor Helio Lima do CETI PROFESSOR RALDIR CAVALCANTE BASTOS.
    Crie o conteúdo de uma aula em formato Markdown seguindo ESTRITAMENTE o modelo abaixo.

    Variáveis:
    - Número da Aula: {lesson_num}
    - Tema: {topic}
    - Turma: {class_name}
    - Disciplina: {subject}

    Modelo de Saída (Markdown):
    # 🎨 Aula {lesson_num}: {topic}

    **🏫 Escola:** CETI PROFESSOR RALDIR CAVALCANTE BASTOS  
    **👨‍🏫 Professor:** Helio Lima  
    **🎓 Turma:** {class_name}
    **📚 Componente:** {subject}  

    ---

    ## 📑 Sumário
    1. 🏁 Introdução
    2. 🎯 Objetivos
    3. 💡 Conteúdo
    4. 📖 Glossário
    5. 🛠️ Atividade Prática
    6. 📝 Quiz

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
    
    ## 📝 Quiz de Fixação
    (Crie 4 perguntas de múltipla escolha. Para cada pergunta, marque a resposta correta com um [x] e as incorretas com [ ]. Exemplo: - [x] Opção correta)
    
    ## Gabarito Comentado
    (Breve explicação da resposta correta)
    """
    
    response = generate_content_with_fallback(prompt)
    
    if response:
        return response.text
    
    return None