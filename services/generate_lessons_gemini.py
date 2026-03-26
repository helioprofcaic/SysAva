import os
import json
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
        Busca o nome da escola no arquivo Escola.txt dentro da pasta data/Turmas.
        """
        path_escola = os.path.join(DATA_DIR, "Turmas", "Escola.txt")
        if os.path.exists(path_escola):
            try:
                with open(path_escola, 'r', encoding='utf-8') as f:
                    nome = f.readline().strip()
                    if nome:
                        return nome
            except Exception as e:
                print(f"[Aviso] Erro ao ler Escola.txt: {e}")
        return "Escola Técnica Estadual"

    def _carregar_competencias_curriculo(self, disciplina):
        """
        Tenta carregar as competências e habilidades do arquivo curriculo_db.json.
        """
        path_json = os.path.join(REPO_DIR, "ementas_cronogramas", "curriculo_db.json")
        dados_disciplina = {}

        if os.path.exists(path_json):
            try:
                with open(path_json, 'r', encoding='utf-8') as f:
                    db = json.load(f)
                    # Busca em todos os segmentos (BASICO, EPT, etc.)
                    term_busca = disciplina.upper()
                    for segmento, conteudos in db.items():
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
            # Tenta inferir o caminho do txt: data/repo/<Disciplina>/lista de aulas.txt
            print(f">>> [DEBUG] Gerando via ROTA 1 (Cronograma) para {disciplina} - Aula {numero_aula}")
            
            # Ajuste de caminho: repo/<Turma>/<Disciplina>/lista de aulas.txt
            caminho_lista = os.path.join(REPO_DIR, turma, disciplina, "lista de aulas.txt")
            
            if not os.path.exists(caminho_lista):
                # Tenta fallback para estrutura antiga (sem turma)
                caminho_lista_antigo = os.path.join(REPO_DIR, disciplina, "lista de aulas.txt")
                if os.path.exists(caminho_lista_antigo):
                    caminho_lista = caminho_lista_antigo
                else:
                    # Tentativa de fallback para nome capitalizado se não achar
                    caminho_lista = os.path.join(REPO_DIR, disciplina.capitalize(), "lista de aulas.txt")

            contexto_str = self.contexto_mgr.obter_contexto_geracao(
                usar_arquivos=False,
                arquivo_lista_path=caminho_lista,
                numero_aula=numero_aula
            )
        return contexto_str

    def gerar_prompt_aula(self, turma, disciplina, semana, contexto_str: str, school_name: str = "Escola Técnica Estadual", professor_name: str = "Professor(a) Assistente", numero_aula: int = None, titulo_personalizado: str = None):
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

        # 3. Montagem do Prompt
        prompt = f"""
Atue como um Professor Assistente de {disciplina}.
Público-Alvo: Estudantes adolescentes de escola pública ({turma}). Use uma linguagem acessível, motivadora, com analogias do cotidiano e cultura pop.

Crie o conteúdo de uma aula em formato Markdown seguindo ESTRITAMENTE o modelo abaixo.

DADOS DA AULA:
- Semana: {semana}
- Número da Aula: {numero_aula}
- Instrução Importante: Identifique o NÚMERO REAL DA AULA lendo o CONTEÚDO BASE (ex: se o texto diz 'Aula 32', use 32). Se não achar, use {numero_aula}.
- Tema: {topic_instruction}
Turma: {turma}
Disciplina: {disciplina}

{texto_curriculo}

CONTEÚDO BASE (Material de apoio para você criar a aula):
---
{contexto_str}
---

Instruções de Formatação:
1. Use Emojis (🚀, 💡, 💻, ⚠️) para estruturar tópicos.
2. Use formatação Markdown (negrito, listas, blocos de código) para tornar a leitura dinâmica.

Modelo de Saída (Siga este formato):
# 🎨 Aula [NÚMERO IDENTIFICADO]: {titulo_personalizado if titulo_personalizado else "[TEMA INFERIDO AQUI]"}

**🏫 Escola:** {school_name}
**👨‍🏫 Professor:** {professor_name}
**🎓 Turma:** {turma}
**📚 Componente:** {disciplina}

---

## 📑 Sumário
1. 🏁 Introdução
2. 🎯 Objetivos
3. 💡 Conteúdo
4. 📖 Glossário
5. 🛠️ Atividade Prática
6. 🧰 Recursos e Ferramentas
7. 📝 Quiz

---

## 🎯 Objetivos de Aprendizagem
(Liste 3 objetivos claros, alinhados com a Referência Curricular e o Conteúdo Base)

## 💡 Conteúdo
(Explicação detalhada e didática do tema, baseada no CONTEÚDO BASE. Se houver código, use blocos de código.)

## 📖 Glossário
(Definição de 3 a 5 termos chave mencionados no conteúdo.)

## 🛠️ Atividade Prática
(Crie um exercício ou uma dinâmica relacionada ao conteúdo. Se o CONTEÚDO BASE for um exercício, adapte-o e formate-o aqui.)

---

## 🧰 Recursos e Ferramentas
(Liste as ferramentas de software ou hardware mencionadas no CONTEÚDO BASE. Se encontrar links de vídeos do YouTube no CONTEÚDO BASE, liste-os aqui também com título e link. Ex: - [Título do Vídeo](https://youtube.com/watch?v=...))

---

## 📝 Quiz Aula: [NÚMERO IDENTIFICADO] - {titulo_personalizado if titulo_personalizado else "[TEMA INFERIDO AQUI]"}

(Crie 3 perguntas de múltipla escolha com 4 alternativas cada. Marque a resposta correta com um [x] e as incorretas com [ ].)

**1. Pergunta 1?**
- [ ] Opção A
- [ ] Opção B
- [x] Opção C
- [ ] Opção D

**2. Pergunta 2?**
- [x] Opção A
- [ ] Opção B
- [ ] Opção C
- [ ] Opção D

**3. Pergunta 3?**
- [ ] Opção A
- [x] Opção B
- [ ] Opção C
- [ ] Opção D

---
### ✅ Gabarito
(Liste o gabarito de forma simples. Ex: 1. C, 2. A, 3. B)
"""
        return prompt