import os
import json
from services import database as db
from dotenv import load_dotenv
from services.contexto_aulas import GerenciadorContextoAula

# Configurações de Diretório
# Assume que este script está em b:\Dev\SysAva\services
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Tenta localizar a pasta data, seja rodando do services ou da raiz
if os.path.exists(os.path.join(BASE_DIR, "data")):
    DATA_DIR = os.path.join(BASE_DIR, "data")
else:
    # Fallback caso a estrutura seja diferente
    DATA_DIR = os.path.join(os.getcwd(), "data")

REPO_DIR = os.path.join(DATA_DIR, "repo")
ENV_PATH = os.path.join(BASE_DIR, '.env')

# Carrega variáveis de ambiente
load_dotenv(ENV_PATH)

class GeradorAulaGemini:
    def __init__(self, api_key=None):
        """
        Inicializa o gerador de aulas.
        :param api_key: Chave de API (opcional, pois o serviço de IA lida com isso na interface).
        """
        self.contexto_mgr = GerenciadorContextoAula(DATA_DIR)
        self.api_key = api_key

    def obter_nome_escola(self):
        """
        Busca o nome da escola, priorizando o banco de dados e usando o arquivo
        Escola.txt como fallback.
        """
        # 1. Tenta buscar do banco de dados primeiro
        school_data = db.get_school()
        if school_data and school_data.get('name'):
            return school_data['name']

        # 2. Fallback para o arquivo Escola.txt se não encontrar no banco
        path_escola = os.path.join(DATA_DIR, "Turmas", "Escola.txt")
        if os.path.exists(path_escola):
            try:
                with open(path_escola, 'r', encoding='utf-8') as f:
                    return f.readline().strip()
            except Exception as e:
                print(f"[Aviso] Erro ao ler Escola.txt: {e}")
        return "Escola Técnica Estadual" # Valor padrão final

    def _carregar_competencias_curriculo(self, disciplina):
        """
        Tenta carregar as competências e habilidades do arquivo curriculo_db.json.
        """
        path_json = os.path.join(REPO_DIR, "ementas_cronogramas", "curriculo_db.json")
        dados_disciplina = {}

        if os.path.exists(path_json):
            try:
                with open(path_json, 'r', encoding='utf-8') as f:
                    curriculo_data = json.load(f)
                    # Busca em todos os segmentos (BASICO, EPT, etc.)
                    term_busca = disciplina.upper()
                    for segmento, conteudos in curriculo_data.items():
                        if term_busca in conteudos:
                            dados_disciplina = conteudos[term_busca]
                            break
            except Exception as e:
                print(f"[Aviso] Erro ao ler banco de currículo: {e}")
        
        return dados_disciplina

    def listar_arquivos_aula(self, turma, disciplina, semana):
        """
        Retorna estrutura com arquivos 'todos' e 'sugeridos'.
        """
        resultado, erro = self.contexto_mgr.listar_arquivos_rota_2(turma, disciplina, semana)
        if erro:
            return None, erro
        return resultado, None

    def processar_arquivos_selecionados(self, lista_arquivos):
        """
        Lê o conteúdo dos arquivos escolhidos.
        """
        return self.contexto_mgr.ler_arquivos_especificos(lista_arquivos)

    def obter_contexto_aula(self, turma, disciplina, semana, numero_aula=None, usar_arquivos=True):
        """
        Obtém o contexto da aula (Rota 1 ou Rota 2).
        """
        if numero_aula is None:
            numero_aula = semana

        if usar_arquivos:
            # ROTA 2: Busca automática na pasta data/Turmas/...
            print(f">>> [DEBUG] Gerando via ROTA 2 (Arquivos) para {turma} - {disciplina} - Semana {semana}")
            contexto_str = self.contexto_mgr.obter_contexto_geracao(
                usar_arquivos=True,
                turma=turma,
                disciplina=disciplina,
                semana=semana
            )
        else:
            # ROTA 1: Busca no arquivo de lista (Cronograma)

            print(f">>> [DEBUG] Gerando via ROTA 1 (Cronograma) para {disciplina} - Aula {numero_aula}")
            
            semana_str = f"S{int(semana):02d}"
            
            # Tenta encontrar o arquivo .txt (cronograma) em diversas vias possíveis
            opcoes_caminho = [
                # Nova recomendação: Caminho específico da semana (Turmas ou Repo)
                os.path.join(DATA_DIR, "Turmas", turma, disciplina, semana_str, "lista de aulas.txt"),
                os.path.join(REPO_DIR, turma, disciplina, semana_str, "lista de aulas.txt"),
                # Caminho padrão por Disciplina (com e sem turma)
                os.path.join(REPO_DIR, turma, disciplina, "lista de aulas.txt"),
                os.path.join(REPO_DIR, disciplina, "lista de aulas.txt"),
                os.path.join(REPO_DIR, disciplina.capitalize(), "lista de aulas.txt")
            ]
            
            caminho_lista = None
            for opt in opcoes_caminho:
                if os.path.exists(opt):
                    caminho_lista = opt
                    print(f"    🔎 Arquivo de cronograma encontrado em: {opt}")
                    break
            
            if not caminho_lista:
                # Fallback final: se nada foi encontrado, usa o primeiro da lista para o erro ser informativo
                caminho_lista = opcoes_caminho[0]
            contexto_str = self.contexto_mgr.obter_contexto_geracao(
                usar_arquivos=False,
                arquivo_lista_path=caminho_lista,
                numero_aula=numero_aula
            )
        return contexto_str

    def gerar_prompt_aula(self, turma, disciplina, semana, contexto_str: str, school_name: str = "Escola Técnica Estadual", professor_name: str = "Professor(a) Assistente", numero_aula: int = None, titulo_personalizado: str = None, persona: str = None, metodologia: str = None, estrutura: str = None, is_local_model: bool = False):
        """
        Gera o prompt final para o LLM a partir de um contexto já fornecido,
        usando o template estruturado que gera um plano de aula completo com quiz.
        """
        if numero_aula is None:
            numero_aula = semana

        # Instrução para a IA inferir o tópico ou usar o personalizado
        if titulo_personalizado:
            topic_instruction = f"TEMA DEFINIDO: {titulo_personalizado}"
        else:
            topic_instruction = "Inferir o TEMA principal a partir do CONTEÚDO BASE fornecido."

        # 2. Dados do Currículo
        info_curriculo = self._carregar_competencias_curriculo(disciplina)
        texto_curriculo = ""
        if info_curriculo:
            habilidades = ", ".join(info_curriculo.get('habilidades', []))
            texto_curriculo = (
                f"REFERÊNCIA CURRICULAR (Use para guiar os objetivos):\n"
                f"Competência: {info_curriculo.get('competencia', '')}\n"
                f"Habilidades: {habilidades}\n"
            )

        # 3. Adaptação de Nível Pedagógico (Ex: 9º ano vs Ensino Médio/Técnico)
        nivel_pedagogico = "Ensino Médio/Técnico"
        instrucao_nivel = "Pode usar termos técnicos padrão e referências em inglês, mas sempre com breve explicação."
        
        if "9ano" in turma.lower() or "9º" in turma:
            nivel_pedagogico = "Ensino Fundamental (9º Ano)"
            instrucao_nivel = (
                "IMPORTANTE: Alunos com pouco contato com inglês. EVITE termos em inglês sem tradução. "
                "Sempre que usar um termo técnico (ex: 'Array', 'Loop'), coloque a tradução ou um apelido em português ao lado. "
                "Use uma didática muito simples, focada em conceitos básicos e analogias lúdicas."
            )

        # 4.1 Geração de Prompt Simplificado para Modelos Locais (OTIMIZADO)
        if is_local_model:
            titulo = titulo_personalizado if titulo_personalizado else 'a ser inferido'

            # Trunca contexto — modelos locais têm janela limitada
            max_context_chars = 3000
            if len(contexto_str) > max_context_chars:
                contexto_str = contexto_str[:max_context_chars] + "\n[CONTEÚDO TRUNCADO]"

            # Prompt compacto — quebras de linha mínimas para não desperdiçar tokens
            prompt = (
                f'Crie um plano de aula Markdown sobre "{titulo}".\n\n'
                f'CABEÇALHO (use EXATAMENTE este formato, sem alterar):\n'
                f'**📚 Disciplina:** {disciplina}\n'
                f'**🎓 Turma:** {turma}\n'
                f'**🏫 Escola:** {school_name}\n'
                f'**👨‍🏫 Professor:** {professor_name}\n\n'
                f'CONTEÚDO BASE:\n{contexto_str}\n\n'
                f'Estrutura obrigatória:\n'
                f'# Aula {numero_aula}: {titulo}\n'
                f'## 🎯 Objetivos (3 itens)\n'
                f'## 💡 Conteúdo Teórico (explicação didática)\n'
                f'## 🛠️ Atividade Prática\n'
                f'(Crie um EXERCÍCIO DE CÓDIGO para o aluno copiar e testar no VS Code ou IDE online. '
                f'Inclua: 1) Objetivo do exercício, 2) Código completo e funcional, 3) Instruções de como rodar. '
                f'Use blocos de código ```python ``` ou ```html ``` conforme a disciplina.)\n'
                f'## 📝 Quiz (3 perguntas múltipla escolha com [x])\n'
                f'### ✅ Gabarito'
            )
            return prompt


        # 4. Montagem do Prompt
        prompt = f"""# MISSÃO
Sua missão é criar um plano de aula completo em formato Markdown.

# PERSONA
{persona if persona else f"Atue como um Professor Assistente de {disciplina}, especialista em criação de materiais didáticos para o {nivel_pedagogico}."}

# DIRETRIZES GERAIS
- **Público-Alvo:** {nivel_pedagogico} de escola pública ({turma}).
- **Adaptação Pedagógica:** {instrucao_nivel}
- **Metodologia:** {metodologia if metodologia else "Aula Expositiva Dialogada"}.
- **Linguagem:** Use uma linguagem acessível, motivadora, com analogias do cotidiano e cultura pop.
- **Estilo Visual:** Use Emojis para estruturar e ilustrações via `!descrição` para conceitos complexos.

# DADOS DE ENTRADA (OBRIGATÓRIOS)
- **Escola:** {school_name}
- **Professor:** {professor_name}
- **Turma:** {turma}
- **Disciplina:** {disciplina}
- **Semana:** {semana}
- **Aula Nº:** {numero_aula}
- **Tema da Aula:** {topic_instruction}
{texto_curriculo}

# MATERIAL DE APOIO (CONTEÚDO BASE)
Use o texto abaixo como fonte principal e obrigatória para o conteúdo da aula.
---
{contexto_str}
---

# ESTRUTURA DE SAÍDA (SIGA ESTRITAMENTE ESTA ORDEM E FORMATAÇÃO)
A estrutura da aula DEVE seguir a ordem definida em `{estrutura if estrutura else "1. Título; 2. Objetivos; 3. Introdução; 4. Conteúdo Teórico; 5. Exemplo Prático; 6. Desafio Prático (Script); 7. Conclusão; 8. Quiz."}`.
O resultado final deve ser um único arquivo Markdown.

--- INÍCIO DO TEMPLATE DE SAÍDA ---
# Aula {numero_aula}: {titulo_personalizado if titulo_personalizado else "[TEMA INFERIDO A PARTIR DO CONTEÚDO BASE]"}

**📚 Disciplina:** {disciplina}
**🎓 Turma:** {turma}
**🏫 Escola:** {school_name}
**👨‍🏫 Professor:** {professor_name}

---

## 🎯 Objetivos de Aprendizagem
*Liste 3 objetivos claros e mensuráveis, alinhados com a Referência Curricular, se disponível.*

## 🏁 Introdução
*Faça uma introdução cativante sobre o tema, conectando com o universo dos alunos.*

##  Conteúdo Teórico
*Desenvolva o conteúdo principal de forma didática, extraindo e explicando os conceitos do MATERIAL DE APOIO. Insira ilustrações onde for pertinente.*

## 🛠️ Exemplo Prático / Atividade
*Crie um EXERCÍCIO DE CÓDIGO para o aluno copiar e testar. Obrigatoriamente inclua:*
*1. Objetivo do exercício (o que o aluno vai praticar)*
*2. Código completo e funcional em blocos ```python ``` ou ```html ```*
*3. Instruções de como rodar (VS Code, Replit, OnlineGDB)*
*O código deve ser FUNCIONAL e prontinho para copiar e colar.*

## 🏁 Conclusão
*Faça um resumo dos pontos principais e reforce a importância do aprendizado.*

## 🧰 Recursos e Links
*EXTRAÇÃO OBRIGATÓRIA: Localize e liste aqui todos os links (YouTube, artigos, etc.) encontrados no MATERIAL DE APOIO. Se não houver links, sugira termos de busca para pesquisa.*

---

## 📝 Quiz: Teste seu Conhecimento!
*Crie 3 perguntas de múltipla escolha com 4 alternativas cada. Marque a resposta correta com `[x]` e as incorretas com `[ ]`.*

### ✅ Gabarito
*Liste o gabarito de forma simples. Ex: 1. C, 2. A, 3. B*
--- FIM DO TEMPLATE DE SAÍDA ---
"""
        return prompt