# 🤖 Instruções para Agentes (AGENTS.md)

Este arquivo contém orientações e restrições críticas para agentes que forem realizar manutenções, otimizações ou correções neste repositório. **Leia antes de fazer qualquer modificação.**

---

## 🏗️ Estrutura e Arquitetura

O SysAva é um portal de apoio educacional construído em **Streamlit** integrado ao **Supabase (PostgreSQL)** em nuvem, rodando sob o ambiente virtual local **`.sysenv`**.

### 📱 Aplicações Streamlit Disponíveis:
* **`app.py`**: Plataforma principal do portal (Aulas, Fóruns, Quizzes, Boletim).
* **`apps/duplicate_checker/duplicate_checker_streamlit.py`**: Utilitário seguro para auditar e limpar registros duplicados exatos na tabela `historico_aulas`.
* **`apps/supabase_monitor/supabase_monitor_streamlit.py`**: Diagnóstico de tamanho de tabelas, auditoria de código e simulador de tráfego/egress.

### 🔌 Inicialização:
* **Atalho Unificado (`run.bat`):** Sempre execute este arquivo bat na raiz. Ele abre um menu interativo que gerencia o ambiente virtual, atualiza dependências e permite escolher qual dos 3 apps Streamlit iniciar.

---

## ⚠️ Restrição Crítica: Cota do Supabase (5GB Egress)

O projeto opera no **plano gratuito do Supabase**, que possui uma cota rígida de **5GB de saída de banda (Egress) mensal**. Devido à arquitetura "Rerun" do Streamlit, é extremamente fácil estourar esse limite caso as regras abaixo não sejam seguidas:

### 1. Caching Obrigatório (`@st.cache_data`)
* **Qualquer consulta de leitura repetitiva** no arquivo `services/database.py` (ex: `get_lessons()`, `get_classes()`, `get_subjects()`) **DEVE** utilizar o decorador `@st.cache_data(ttl=300)` para evitar chamadas duplicadas ao Supabase a cada clique do usuário.

### 2. Evite `select("*")` para Listagens
* Nunca use `select("*")` para listar aulas em menus ou páginas de seleção. A coluna `full_content` na tabela `lessons` contém resumos de texto longos.
* **Prática Correta:** Faça duas funções. Uma leve para a listagem (`select("id, title, week, subject_id")`) e outra pesada para carregar o conteúdo da aula (`select("id, full_content")`) **apenas** quando o aluno abrir aquela página específica.

### 3. Proibido Imagens inline em Base64 no Banco
* Nunca faça upload, armazene ou gere ilustrações embutidas em Base64 dentro das colunas `description` ou `full_content` das tabelas `lessons` e `forum_posts`. Uma única imagem em Base64 adiciona 2MB à linha do banco, estourando a cota de tráfego em dias.
* No Gerador de Aulas (`views/gerador_aulas.py`), mantenha a opção **"Bloquear imagens Base64"** como `True` por padrão. As imagens devem ser tratadas como links normais locais (ex: `![alt](assets/img.png)`).

---

## 📝 Padrões de Geração e Parsing de Quizzes

### 1. Estrutura do Quiz (4x4)
* Todos os quizzes gerados pela IA devem ter obrigatoriamente **4 perguntas** de múltipla escolha com **4 alternativas** cada.
* As alternativas corretas devem ser identificadas por `[x]` e as incorretas por `[ ]`.

### 2. Resiliência do Parser (`services/quiz_parser.py`)
* O separador de quizzes procura pelo cabeçalho `## Quiz` de forma resiliente usando expressões regulares. **Nunca modifique o padrão regex para algo rígido** que dependa do emoji `📝`, pois variações da IA farão a aula ser salva sem nenhum quiz associado.
* O parser traduz as variações de perguntas (`Pergunta 1`, `Questão 01`) de forma flexível e compara os números do gabarito como inteiros (`int`) para evitar falhas de matching com zeros à esquerda.

---

## 🎨 Modelos de IA e Prompting

No Gerador de Aulas (`views/gerador_aulas.py`):
* **Modelos em Nuvem (Gemini e ChatGPT/OpenAI):** Devem ser identificados por `is_local_model=False`. Eles utilizam o prompt completo de alta qualidade e são limitados inteligentemente a **`MAX_CHARS_CONTEXTO_NUVEM = 32000`** para conter gastos desnecessários com tokens de entrada da API.
* **Modelos Locais (LM Studio, Jan, Llama Serve):** Usam prompts compactos, têm truncamento de contexto rígido (`MAX_CHARS_CONTEXTO_LOCAL = 9000`) para não sobrecarregar a memória RAM do computador do usuário, e não suportam processamento massivo.

---

## 📁 Paths e Importações em Scripts Secundários

Ao criar ou editar scripts que ficam dentro de subpastas (como `apps/` ou `scripts/`), as importações do módulo `services` falharão caso o diretório raiz não esteja no path do Python. Sempre insira o seguinte trecho no início do arquivo:

```python
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Ajuste o nível de dirname conforme a profundidade da subpasta
if project_root not in sys.path:
    sys.path.insert(0, project_root)
```
