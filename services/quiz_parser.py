import re
from services import database as db

def split_lesson_and_quiz(full_content: str):
    """
    Separa o conteúdo da aula do conteúdo do quiz.
    Retorna (lesson_content, quiz_content)
    """
    # 1. Tenta encontrar o início do Quiz pelo cabeçalho contendo "Quiz" de forma resiliente
    # Aceita qualquer nível de cabeçalho (#, ##, ###), com ou sem emojis (ex: ## 📝 Quiz, ## Quiz)
    quiz_match = re.search(r'(?:^|\n)(#+\s*(?:📝\s*)?Quiz\b)', full_content, re.IGNORECASE)
    
    if quiz_match:
        split_index = quiz_match.start(1)
        lesson_content = full_content[:split_index].strip()
        quiz_content = full_content[split_index:].strip()
        return lesson_content, quiz_content
    
    return full_content, None

def process_quiz_content(lesson_id: int, quiz_content: str, lesson_title: str):
    """Parseia o conteudo de um quiz e o insere no banco de dados."""

    # Título único por aula. O template da IA gera cabeçalhos genéricos
    # (ex: "## 📝 Quiz: Teste seu Conhecimento!") que, se usados como título,
    # fazem quizzes de aulas diferentes colidirem e serem marcados como
    # concluídos em conjunto.
    quiz_title = f"Quiz: {lesson_title}".strip() if lesson_title else "Quiz"

    # Remove quizzes anteriores desta aula para não acumular duplicatas a cada salvamento.
    try:
        db.delete_quizzes_for_lesson(lesson_id)
    except Exception:
        pass

    # Cria o Quiz no banco
    quiz_data, error = db.create_quiz(lesson_id, quiz_title)
    if error or not quiz_data:
        return False, f"Erro ao criar quiz: {error}"

    quiz_id = quiz_data[0]['id']

    # Pre-processamento agressivo para quebrar tudo corretamente

    # 1. Substitui Pergunta/Questão por "1." de forma resiliente e remove zeros à esquerda
    content = re.sub(r'(?:Pergunta|Quest[aã]o|Question)\s+0*(\d+)', r'\1.', quiz_content, flags=re.IGNORECASE)
    content = re.sub(r'(\d+)\.', r'\1.', content) # normaliza o número da pergunta

    # 2. Quebra antes de numeros de questao (1. 2. 3.)
    content = re.sub(r'(\S)\s+(\d+[\.\)])', r'\1\n\n\2', content)

    # 3. Quebra entre alternativas coladas "a) X b) Y c) Z d) W"
    content = re.sub(r'([a-dA-D][\.\)])\s+([a-dA-D][\.\)])', r'\1\n\2', content)

    # 4. Quebra apos letra antes de proximo numero "d) texto 2." -> "d) texto\n\n2."
    content = re.sub(r'([a-dA-D][\.\)])\s+([^a-dA-D\n]{5,})\s+(\d+[\.\)])', r'\1 \2\n\n\3', content)

    # 5. Fallback: quebra espacos duplos
    content = re.sub(r'([a-dA-D][\.\)])\s{2,}', r'\1\n', content)

    lines = content.split('\n')
    questions_buffer = []

    current_question = None
    current_options = []
    current_correct_index = -1
    current_question_number = None

    parsing_gabarito = False

    def flush_current_question():
        nonlocal current_question, current_options, current_correct_index, current_question_number
        if current_question and current_options:
            questions_buffer.append({
                'question_text': current_question,
                'options': current_options,
                'correct_option_index': current_correct_index,
                'number': current_question_number
            })

        current_question = None
        current_options = []
        current_correct_index = -1
        current_question_number = None

    for line in lines:
        line = line.strip()
        if not line: continue

        clean_line = re.sub(r'^>\s*', '', line)

        # Detecta inicio da secao de Gabarito
        if re.search(r'(\*\*|##).*Gabarito', clean_line, re.IGNORECASE):
            flush_current_question()
            parsing_gabarito = True
            continue

        if parsing_gabarito:
            all_answers = re.findall(r'(\d+)\s*[\-\.\)]\s*([a-eA-E])', clean_line)
            if all_answers:
                for q_num, ans_char in all_answers:
                    ans_idx = ord(ans_char.lower()) - ord('a')
                    for q in questions_buffer:
                        try:
                            # Comparação numérica resiliente (ignora zeros à esquerda)
                            if q['number'] is not None and int(q['number']) == int(q_num):
                                q['correct_option_index'] = ans_idx
                                break
                        except ValueError:
                            if q['number'] == q_num:
                                q['correct_option_index'] = ans_idx
                                break
            continue

        question_regex_str = r'^(?:###\s*)?[\*]*(\d+)[\*]*[\.\)\-]\s+(.*)'

        # Ignora titulos
        if clean_line.startswith('#') and not re.match(question_regex_str, clean_line):
            continue

        # Identifica resposta na linha
        answer_match = re.search(r'(?:Resposta|Gabarito|Correct|Solucao).*?([a-eA-E])', clean_line, re.IGNORECASE)
        if answer_match and current_options:
            correct_char = answer_match.group(1).upper()
            idx = ord(correct_char) - ord('A')
            if 0 <= idx < len(current_options):
                current_correct_index = idx
            continue

        # Nova pergunta
        question_match = re.match(question_regex_str, clean_line)
        if question_match:
            flush_current_question()
            current_question_number = question_match.group(1)
            current_question = question_match.group(2)
            current_options = []
            current_correct_index = -1
            continue

        # Opcao checkbox [x]
        checkbox_match = re.match(r'^[-*+]?\s*[\[\(]\s*([xX\s]?)\s*[\]\)]\s*(.*)', clean_line)
        if checkbox_match:
            is_correct = checkbox_match.group(1).strip().lower() == 'x'
            opt_text = checkbox_match.group(2).strip()
            
            # Limpa prefixos de letras residuais (ex: "[ ] a) Opção" -> "Opção")
            opt_text = re.sub(r'^(?:\*\*)?[a-eA-E][\.\)]\s*(?:\*\*)?', '', opt_text).strip()
            
            if is_correct:
                current_correct_index = len(current_options)
            current_options.append(opt_text)
            continue

        # Opcao letra a)
        letter_match = re.match(r'^[-*+]?\s*(?:\*\*)?([a-eA-E])(?:\*\*)?[\.\)]\s+(.*)', clean_line)
        if letter_match:
            opt_text = letter_match.group(2).strip()
            # Detecta marcador (RESPOSTA) e marca como correta
            if re.search(r'\(RESPOSTA\)', opt_text, re.IGNORECASE):
                opt_text = re.sub(r'\s*\(RESPOSTA\)', '', opt_text, flags=re.IGNORECASE).strip()
                current_correct_index = len(current_options)
            current_options.append(opt_text)
            continue

        # Continuacao da pergunta
        if current_question is not None and not current_options:
            if current_question == "":
                current_question = clean_line
            else:
                current_question += " " + clean_line

    if not parsing_gabarito:
        flush_current_question()

    saved_count = 0
    for q in questions_buffer:
        if q['correct_option_index'] == -1:
             continue

        _, q_error = db.create_quiz_question(quiz_id, q['question_text'], q['options'], q['correct_option_index'])
        if not q_error:
             saved_count += 1

    return True, f"Quiz criado com {saved_count} questoes."