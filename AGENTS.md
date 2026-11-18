# 🤖 Instruções para Agentes (AGENTS.md)

Este arquivo contém orientações e restrições críticas para agentes que forem realizar manutenções, otimizações ou correções neste repositório. **Leia antes de fazer qualquer modificação.**

---

## 🏗️ Estrutura e Arquitetura

O SysAva é um portal de apoio educacional construído em **Streamlit** integrado ao **Supabase (PostgreSQL)** em nuvem, rodando sob o ambiente virtual local **`.sysenv`**.

### 📱 Aplicações Streamlit Disponíveis:
* **`app.py`**: Plataforma principal do portal (Aulas, Fóruns, Quizzes, Boletim).
* **`apps/duplicate_checker/duplicate_checker_streamlit.py`**: Utilitário seguro para auditar e limpar registros duplicados exatos na tabela `historico_aulas`.
* **`apps/supabase_monitor/supabase_monitor_streamlit.py`**: Diagnóstico de tamanho de tabelas, auditoria de código e simulador de tráfego/egress.
* **`apps/planejamento_registro/planejamento_registro_streamlit.py`**: Acompanhamento de planejamento e registro de aulas (porta 8510).
* **`apps/down_seductec/down_seductec_streamlit.py`**: Download de PDFs e links de vídeo do portal SeducTec para `data/repo/<turma>/<disciplina>/S0X/seductec/` (porta 8504).

### 📦 Repositório aninhado `syava-apps`:
* A pasta **`apps/`** é um **repositório Git próprio** (<https://github.com/hiseg10/syava-apps>), versionando os apps Streamlit, a pasta **`apps/bots/`** (autômatos Selenium do iSeduc: `registrar_aulas`, `registrar_notas`, `grade_scraper`, `bot_raspagem`, `inspector_*` — antes em `apps/api/tools/`) e docs (`README.md`, `ISSUES.md` com IDs `AP-NNN`, `AGENTS.md`, `run_apps.bat`).
* O `.gitignore` do SysAva ignora `apps/` por completo — os dois repositórios não conflitam. **Nunca** tente versionar `apps/` a partir da raiz do SysAva.
* Fora de escopo do repo novo (e bloqueados pelo `.gitignore` dele): `apps/api/`, `apps/apis_gemini_key/`, `apps/data/`, backups `.db`, `.csv`, `html/`, logs. Detalhes em `apps/AGENTS.md`.

### 🔌 Inicialização:
* **Atalho Unificado (`run.bat`):** Sempre execute este arquivo bat na raiz. Ele abre um menu interativo que gerencia o ambiente virtual, atualiza dependências e permite escolher qual dos apps Streamlit iniciar (portas: 8501 principal, 8502 duplicatas, 8503 monitor, 8504 Down SeducTec, 8510 planejamento).
* **Bootloader dos apps (`apps/run_apps.bat`):** menu próprio do repositório syava-apps, que detecta/cria o mesmo venv `.sysenv`.

### 🖥️ Runtime do Monitor:
* Todos os arquivos do servidor/agente/tela/bandejas do monitor ficam em **`data/repo/plugins/monitor/`** (receiver, `lab_agent`, `sysava_lock`, trays, diagnóstico, `emails.json`, `lab_users.json`, `acesso_coletivos.json`, logs, `.atividades/`, `.relatorios/`, assets).
* O código versionado do plugin Streamlit continua em `plugins/monitor_rede/`; `views/plugins.py` carrega de lá e o plugin resolve o runtime em `data/repo/plugins/monitor/` (`SYSAVA_PLUGIN_DIR` sobrescreve).
* Scripts dentro de `monitor/` sobem **quatro níveis** até a raiz (`..\..\..\..`) para achar `.sysenv`/`.env`/`data/Turmas`.
* **Bandejas:** `tray_servidor.ps1` mostra/atualiza o IP, abre o **2º servidor** (peer via `/api/peer/state`) e traz **Abrir SysAva (8501)** + **Apps** (Streamlit local ou portal na nuvem) + **Parar todos os apps**. `tray_aluno.ps1` mostra **nome + RA** e copia o RA (API/cache ou `%LOCALAPPDATA%\SysAva\ultimo_ra.txt`), abre o **SysAva com o RA** e tem **Sair da conta** (limpa `tela_ok.json`/`ultimo_ra.txt`, chama `POST /api/logout_ra` e reabre o `sysava_lock.ps1`), **Abrir tela de bloqueio**, **Atualizar meus dados** e **Sair do Windows (logoff)**. O logout remove a associação do PC em `lab_users.json` e propaga aos peers (`/api/peer/logout`), liberando o RA na hora. **Atualizar Bandeja do Aluno** (Controle) baixa os arquivos e reinicia a instância antiga; para mudanças manuais no script, feche e reabra o `tray_aluno.bat`.
* **Usuários no painel web:** a aba **Usuários** (porta 5000) cria contas, desativa/reativa o acesso (`app_users.status='blocked'`) e remove cadastros. Professor gerencia apenas alunos; administrador gerencia qualquer função. O bloqueio não altera `is_active`/`is_portal` (frequência) e o login do painel também recusa contas bloqueadas.
* **Ferramentas → Texto e Comando:** painel web e plugin Streamlit têm campos para enviar **texto/alerta** e **comando digitado** aos PCs marcados. No web, a rota é `POST /ferramenta_texto_comando`; o texto dispara `Enviar Alerta Visual` e, ao executar um comando, também é enviado antes como alerta (quando não é o próprio alerta).
* **Preferência de servidor:** o **PC01 do laboratório** (`PC01*`) tem prioridade. O `/health` publica `hostname`/`preferred`; `lab_agent.py`, `sysava_lock.ps1`, `sysava_tray.ps1`, `tray_aluno.ps1` e `tray_servidor.ps1` escolhem primeiro o PC01 e, no cluster, ele fica **primário** mesmo subindo depois do notebook. Sem o PC01, vale quem iniciou primeiro. Ajuste com `SYSAVA_PREFERRED_SERVERS` (ex.: `PC01*,PC02*`; vazio desliga). O agente subiu para **build 20** (alerta maior, texto selecionável e botão Copiar).

---

## ⚠️ Restrição Crítica: Cota do Supabase (5GB Egress)

O projeto opera no **plano gratuito do Supabase**, que possui uma cota rígida de **5GB de saída de banda (Egress) mensal**. Devido à arquitetura "Rerun" do Streamlit, é extremamente fácil estourar esse limite caso as regras abaixo não sejam seguidas:

### 1. Caching Obrigatório (`services/local_cache.py`)
* **Qualquer consulta de leitura repetitiva** no arquivo `services/database.py` (ex: `get_lessons()`, `get_classes()`, `get_subjects()`) **DEVE** passar por `local_cache.get_or_fetch(chave, fetch_fn, ttl=...)` para evitar chamadas duplicadas ao Supabase a cada rerun do Streamlit.
* O cache SQLite é **ligado por padrão** (`services/local_cache.py`) e funciona também no Streamlit Cloud (arquivo efêmero por instância). Para desligar, use `DISABLE_LOCAL_CACHE = true` ou `ENABLE_LOCAL_CACHE = false` em `.streamlit/secrets.toml`/variável de ambiente.
* **Toda escrita deve invalidar o cache correspondente.** Ex.: ao gravar histórico, chamar `local_cache.invalidate(f"user_history:{username}")`; ao mexer em quizzes, usar `_invalidate_quizzes_cache()`. Sem invalidação, dados ficam desatualizados até o TTL expirar.
* TTLs disponíveis: `TTL_SHORT` (120s, histórico/score), `TTL_FORUM` (300s), `TTL_SCORE` (600s, cache de score em lote), `TTL_MEDIUM` (1h), `TTL_BASE` (6h). Nunca quebra: em erro de SQLite cai no Supabase.

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

### 3. Identificação por `quiz_id` (nunca só pelo título)
* O título do quiz **deve ser único por aula** (`Quiz: {título da aula}`). O template da IA gera cabeçalhos genéricos repetidos (ex: `## 📝 Quiz: Teste seu Conhecimento!`) que **não** podem virar título do quiz, sob pena de um quiz respondido marcar vários outros como concluídos.
* Conclusão, tentativas e pontuação devem ser identificadas por **`quiz_id`** (gravado no histórico como `| quiz_id:X`). Nunca volte a comparar apenas por título.
* Ao salvar uma aula, remova os quizzes anteriores daquela aula antes de criar os novos (evita duplicatas). Use `db.delete_quizzes_for_lesson(lesson_id)`.
* Migração e reset de tentativas: `scripts/migrate_quiz_titles.py` e `scripts/reset_quiz_attempts.py` (ver `docs/ISSUES_LOCAIS.md`).

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

---

## 🔐 Regras de Acesso do Laboratório (tela de bloqueio)

Arquivos principais: `data/repo/plugins/monitor/sysava_lock.ps1` (tela), `data/repo/plugins/monitor/lab_receiver.py` (`/api/auth_ra`, `/api/alunos`), `data/repo/plugins/monitor/acesso_coletivos.json` e `data/repo/plugins/monitor/lab_users.json`.

* **RA único:** um RA comum não pode estar logado em dois PCs ao mesmo tempo. O `/api/auth_ra` responde **400** com o PC onde ele já está; ao deslogar/desligar a origem (~60s sem ping) o RA é liberado. Não remova essa checagem em `_autorizar_login_ra` sem prever uma forma de liberação.
* **Contas coletivas:** `7anoA`, `7anoB`, `8ano`, `9ano`, `1alunoEja`, `Alunos_EJA_Noite` ficam fora da regra de RA único. A lista fica em `acesso_coletivos.json` (`coletivos`). Novas contas coletivas devem ser adicionadas lá **e** criadas em `app_users` (Supabase) com `role=student`.
* **Janela EJA:** contas em `acesso_coletivos.json` → `eja.contas` só entram das **17h às 23h** (hora do servidor). A checagem existe no receiver (`_eja_pode_entrar`) e no `sysava_lock.ps1` (offline). A janela vale para **novos logins**.
* **PC mestre:** a senha administrativa (`unlock_secret.txt`/`SYSAVA_ADMIN_UNLOCK`, padrão `labadmin`) e o bypass da lista só valem em hostnames configurados (padrão `PC01*`) via `SYSAVA_MASTER_HOSTS` ou `C:\ProgramData\SysAva\master_hosts.txt`. Nos demais PCs apenas nome/RA da lista libera.
* **Professores na tela:** `acesso_coletivos.json` → `professores` (ex.: `["adriana"]`) libera docentes por login, RA ou nome **apenas nos PCs mestres** (`PC01*`). O `/api/auth_ra` aceita o professor e associa ao PC; `/api/alunos?maquina=...` inclui esses professores no seletor somente no mestre. Professores não entram na regra de RA único. Nos demais PCs a tela continua exigindo nome/RA de aluno ou a senha admin.
* **Tela reaberta (agente build 15+):** ao validar o RA, `sysava_lock.ps1` grava `%LOCALAPPDATA%\SysAva\tela_ok.json` (RA + epoch). O `lab_agent.py` relança a tela quando o processo desaparece **sem** token válido para a sessão atual do Windows (`psutil.users().started`); não relança se o professor liberou (`tela_liberada.json`) ou se o aluno já validou. Mantenha essa distinção ao mexer na tela/agente.
* **Jogos:** o watchdog fecha jogos (Roblox, Fortnite/Epic, League of Legends) e janelas de sites de jogos (Loki, Poki, Friv, Temple Run...) **quando o bloqueio persistente (`block_state.json`) está ativo**. Com **Desbloquear Sites/Jogos**, esses processos ficam livres (`WATCHDOG_EXCLUDE_KEYWORDS`); o comando manual **Bloquear Jogos** fecha uma vez, sem manter bloqueio. Fortnite precisa continuar em `BLOCKED_PROCESS_KEYWORDS`, `BLOCKED_SITE_KEYWORDS`, `JOGO_KEYWORDS` (receiver) e `bloquear_hosts.ps1`.
* **Backup de atividades:** solicitado pela aba Ferramentas (Streamlit e painel web). O agente procura `%USERPROFILE%\Documents\SysAva` e alternativas (perfis/OneDrive/Public); se não achar, devolve erro claro. Os ZIPs ficam em `data/repo/plugins/monitor/.atividades/` e são servidos em `/atividades`.
* **Ações do Controle:** o painel web aceita **várias ações** por envio (`name="acao"` repetido). O receiver enfileira em `pending_queue` no `lab_status.json` e entrega **uma por ping** (~10 s, na ordem marcada); não volte a sobrescrever `pending_command` sem preservar a fila. O Streamlit usa `st.multiselect` + presets e envia um POST por ação.
* **Ferramentas e Portal com RA:** a aba Ferramentas do painel web é dividida em sub-abas (Atividades, Sites e RA, Tela, Manutenção). **Ferramentas → Sites e RA → Abrir SysAva com RA** (`POST /abrir_sysava`) associa o RA ao PC, propaga aos peers e envia **"Abrir SysAva (RA)"** com `{url, browser, ra}`; o agente **build 16+** abre `?ra=...` no navegador escolhido (Chrome/Edge/Firefox/Brave/Opera) e usa o padrão do Windows se não achar. Mantenha `AGENT_BUILD_MIN_SYSAVA=16` e o `lab_agent.ps1` sincronizado com o `.py`.
* Ao mexer nesses fluxos, atualize este `AGENTS.md`, o `plugins/monitor_rede/README.md` e registre em `docs/ISSUES_LOCAIS.md`.

---

## 🗂️ Registro de Issues Locais (obrigatório)

* Toda correção/melhoria relevante deve ser registrada em **`docs/ISSUES_LOCAIS.md`** (índice com ID `IS-NNN`, status, arquivos afetados e como validar).
* Ao concluir uma tarefa, **atualize o registro** antes de finalizar: adicione/edite a entrada, o status e o commit relacionado.
* Mantenha o formato existente (símbolos 🟢/🟡/🔴/⚪ e a seção "Comandos úteis").
