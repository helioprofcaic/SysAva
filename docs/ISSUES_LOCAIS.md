# 🗂️ Registro de Issues Locais — SysAva

Documento de acompanhamento **local** das correções e melhorias feitas no projeto.
Serve para não perder o fio das alterações entre sessões de manutenção.

**Regra:** toda alteração relevante deve virar uma entrada aqui (com ID, status,
arquivos afetados e como validar). Agentes devem atualizar este arquivo ao
concluir uma tarefa.

## Convenções

| Símbolo | Significado |
| ------- | ----------- |
| 🔴 | Aberto |
| 🟡 | Em andamento |
| 🟢 | Resolvido |
| ⚪ | Backlog / ideia |

Formato de ID: `IS-NNN`.

---

## Índice

| ID | Título | Status | Data |
| -- | ------ | ------ | ---- |
| IS-001 | Plugin de Atividades — dataset de pontuação por atividades | 🟢 | 2026-09-17 |
| IS-002 | Quizzes marcados como respondidos sem responder | 🟢 | 2026-09-17 |
| IS-003 | Egress do Supabase estourando a cota de 5 GB | 🟢 | 2026-09-17 |
| IS-004 | Lentidão no dataframe do plugin de qualitativo | 🟢 | 2026-09-17 |
| IS-005 | Configurar cache no Streamlit Cloud | ⚪ | 2026-09-17 |
| IS-006 | Cachear avaliações/submissões (admin) | ⚪ | 2026-09-17 |
| IS-007 | Quizzes feitos não contabilizados no score (regressão do IS-002) | 🟢 | 2026-09-17 |
| IS-008 | Lista negra de faltosos inicia a chamada como "Falta" (Frequência) | 🟢 | 2026-09-17 |
| IS-009 | Base64/SVG inflando aulas — backup limpo e migração para novo banco | 🟢 | 2026-09-22 |
| IS-010 | Auditoria e limpeza de duplicatas de bot no fórum | 🟢 | 2026-09-22 |
| IS-011 | Aba Portal (iSeduc): esqueleto Planejar/Registrar/Notas | 🟡 | 2026-09-22 |
| IS-012 | Gerador de aulas salvando opções com marcador "[x]/[ ]" no texto | 🟢 | 2026-09-24 |
| IS-013 | Plugin Atividades: exportar relatório CSV de pontos por aula | 🟢 | 2026-09-24 |
| IS-014 | Qualitativo vazando entre disciplinas (pontos órfãos sem subject_id) | 🟢 | 2026-09-24 |
| IS-015 | Planejamento/Registro: contagem da disciplina IA 51/40 vs 28/27 no portal | 🟢 | 2026-09-24 |
| IS-016 | Gerador de planos: Mentoria Tech II não gerava datas novas com lições | 🟢 | 2026-09-24 |
| IS-017 | Gerador de planos: lições fora do padrão de título "Aula XX" quebravam a fila de planejamento | 🟢 | 2026-09-25 |
| IS-018 | Frequência dos planos só consultava a lista negra — tabela `attendance` e JSON de plugins não eram lidos | 🟢 | 2026-09-25 |
| IS-019 | Gerador de planos: tipos de estratégia configuráveis + filtro de intervalo de aulas a gerar | 🟢 | 2026-09-25 |
| IS-020 | Numeração de planos pulava os pares (grade duplicada) + "Sobrescrever" agora limpa `planejamento` | 🟢 | 2026-09-25 |
| IS-021 | Frequência diária não persistia no `escola_ativa.db` e a leitura ignorava disciplina (estrutura data → turma → disciplina) | 🟢 | 2026-09-25 |
| IS-022 | Plugins Notas/Frequência: `escola_ativa` como 1ª persistência e Supabase como redundância (sem travar na conexão) | ⚪ | 2026-09-25 |
| IS-023 | Plugin Atividades: lançamento de Seminário como avaliação (intervalo de aulas + nome + lista de pesquisa) | 🟡 | 2026-09-25 |
| IS-024 | Admin/Gerenciar Avaliações: opção de excluir avaliação (com respostas, questões e notas) | 🟢 | 2026-09-25 |
| IS-025 | Plugin Atividades: últimas 8 aulas da disciplina fora do teto de 6 pts (40h→33-40, 80h→73-80) + aulas de apresentação criadas | 🟢 | 2026-09-25 |
| IS-026 | Prova impressa/salva: separar lista de integrantes e lista de aulas do seminário (quebras de linha e listas) | 🟢 | 2026-09-25 |
| IS-027 | Visualizar/Imprimir Prova: prova cortada à direita (overflow do container 800px) | 🟢 | 2026-09-25 |
| IS-028 | Imprimir Prova/Visualizar Prova exibiam a prova dentro de coluna estreita (1/3 da largura), cortada à direita | 🟢 | 2026-09-25 |
| IS-029 | Planos individual: feedback explícito da origem da frequência | 🟢 | 2026-09-28 |
| IS-030 | Gerar planos: ampliar lista de presença para visualizar 15 alunos | 🟢 | 2026-09-28 |
| IS-031 | Frequência: incluir alunos inativos da lista negra | 🟢 | 2026-09-29 |
| IS-032 | Planos: não sugerir datas cadastradas como feriado | 🟢 | 2026-09-29 |
| IS-033 | Planos: diagnóstico contava linhas duplicadas de `historico_aulas` | 🟢 | 2026-09-29 |
| IS-034 | Planos: lista negra misturava alunos de turmas diferentes | 🟢 | 2026-09-29 |
| IS-035 | Planos: associar abreviações de disciplina ao rótulo da grade | 🟢 | 2026-09-29 |
| IS-036 | Repo syava-apps aninhado em `apps/` + app Down SeducTec (8504) + menu do `run.bat` | 🟢 | 2026-09-29 |
| IS-037 | Planejamento: feriados bloqueiam geração/registro; configs migram para `master_config`; frequência ao vivo | 🟢 | 2026-09-29 |
| IS-038 | Planejamento: aba Consolidadas no app 8510 + `disciplina_ids`/sync do calendário (`data/calendario_letivo.json` → `master_config`) | 🟢 | 2026-09-29 |
| IS-039 | Disciplina oculta no local: cache de disciplinas obsoleto, toggle sem invalidação, fetch que cacheava lista vazia e `.env` em projeto Supabase antigo | 🟢 | 2026-09-30 |
| IS-040 | Lista negra não funcionava no Cloud: fonte única em JSON não versionado → mecanismo de inativos via `app_users`/`user_profiles` | 🟢 | 2026-09-30 |
| IS-041 | `historico_aulas` não refletia o portal: 189 órfãs com rótulo antigo de turma (local 601 × portal 418) + sync do Supabase | 🟢 | 2026-10-01 |
| IS-042 | Gerador de planos: geração "Sobrescrever"+intervalo pulou 24/09 (P.C.II I-B) e duplicou o nº 30 (17/09 × 01/10) — base hist+pend instável e descartes invisíveis na UI | 🟡 | 2026-10-01 |
| IS-043 | Fila Disc.Tec.: plano modular (Fundamentos UI I-A) gerado antes da última aula modular registrada no portal (18/05 × Front-End até 03/06) — piso do portal agora precede o calendário | 🟢 | 2026-10-01 |
| IS-044 | Grade horária: slot fantasma 09:10 (I-A segundas × I-B quintas; portal registra 09:30) — 3 espelhos divergentes e 2 planos gerados em horário inexistente | 🟢 | 2026-10-02 |
| IS-045 | Aulas especiais via "livro-caixa": estrutura `{01-08}{09-16}{LIVRE}{17-24}{25-32}{LIVRE}` (fechamento por horas), model' de leitura em `master_config`, planos 8510 consultam o livro — fase 1 (model' + fila + aba 8510) implementada e validada | 🟢 | 2026-10-02 |
| IS-046 | Transição disciplina→disciplina: piso IS-043 (`ult+1 dia`) descartava os slots livres do dia da última aula (03/06 08:10 da I-A ficava ocioso) — piso agora vale o próprio dia; ocupação/feriado/`inicio_disciplina` seguem protegendo | 🟢 | 2026-10-02 |
| IS-047 | Grade horária na ⚙️ Config do 8510: monitor dos 3 espelhos (SQLite/JSON/Supabase) + edição mover/adicionar/remover — mudança real Sex 11:30/13:30 → Qua (I-A, Disc.Tec.) aplicada e planos disc 8 renumerados | 🟢 | 2026-10-02 |
| IS-048 | Caderno de notas `student_scores.json` era JSON inválido (`NaN` gravado pelo plugin) e a opção [5] do `run_apps.bat` apontava para um README inexistente — app novo de Análise de Notas (8511) + sanitização dos plugins | 🟢 | 2026-10-03 |
| IS-049 | Investigação das notas no portal iSeduc (aba 🔍 do 8511 + `POST /notas/investigar` na API local) e centralização dos 6 bots ativos em `apps/bots/` — só repo syava-apps, nenhum arquivo do núcleo alterado | 🟢 | 2026-10-03 |
| IS-050 | Análise de Notas: lançamento direto do caderno destruía nota de aluno transferido/fora do portal e não permitia editar notas antes de enviar — tabela editável na aba 🤖 + 5ª aba ⚙️ Config com status de envio por aluno, incluindo **piso 6** para AEE/Licença | 🟢 | 2026-10-03 |
| IS-051 | Aba 🌐 Portal do app principal: recursos do app 8510 trazidos para o Portal (Planejar/gerar planos, Registrar lote + status, Sincronizar/raspagem, Painel/Consolidadas e Config), via API local | 🟢 | 2026-10-05 |
| IS-052 | Grade semanal duplicada (`weekly_schedule` com 18 slots repetidos / "COLISÃO!"): `/pull-from-cloud` recriava a tabela como TEXT e destruía a UNIQUE — script de correção + schema canônico restaurado | 🟢 | 2026-10-05 |
| IS-053 | Auditoria das demais tabelas afetadas pelo mesmo `/pull-from-cloud`: `attendance` (835 linhas repetidas) e `assessments` (11) deduplicadas e constraints restauradas via `scripts/repair_local_db.py` | 🟢 | 2026-10-05 |
| IS-054 | Raspagem do Portal coletava 0 cards: filtro de turma recebia o `code` (309197) mas o bot casa pelo texto do card — bot resolve code/nome/sigla; Portal agora sincroniza completo por padrão com reconciliação opcional | 🟢 | 2026-10-07 |
| IS-078 | `lessons` local desatualizado vs Supabase (ex.: PROGRAMAÇÃO PARA DISPOSITIVOS MÓVEIS com 0 no local e 17 na nuvem): script `sync_lessons_from_supabase.py` faz upsert por `id` | 🟢 | 2026-10-14 |
| IS-079 | Gerador de planos: piso modular excluía os slots livres do **próprio dia** da última aula registrada (Fundamentos UI perdeu 10/06 08:10/11:30/13:30) — piso agora é inclusivo (intenção do IS-046) | 🟢 | 2026-10-15 |
| IS-080 | Cesta de chamadas (rateio proporcional da frequência real → planos compensados): `core/cesta.py` expande as chamadas pelo peso da **grade real** (backup), duplica semana se faltar chamada e fecha a carga | 🟡 | 2026-10-15 |
| IS-055 | Monitor de laboratório: bloqueio manual expandido de jogos (Roblox/League of Legends + sites/proxies no navegador, ex. Loki) | 🟢 | 2026-10-09 |
| IS-056 | Monitor: modo não invasivo — bloqueio do Roblox via arquivo `hosts` (sem instalação do agente) | 🟢 | 2026-10-09 |
| IS-057 | Monitor: descoberta robusta do servidor (cache local + broadcast UDP 5001) para rede com IP dinâmico | 🟢 | 2026-10-09 |
| IS-058 | Monitor: servidor de instalação/atualização pela rede (`/setup`) — sem pendrive | 🟢 | 2026-10-09 |
| IS-059 | Monitor: agente em SYSTEM (sessão 0) relança na sessão ativa do aluno (janela correta) | 🟢 | 2026-10-09 |
| IS-060 | Monitor: selecionar todas, ações em massa (desligar/reiniciar), Bloquear Sites (YouTube/Instagram) e hosts com redes sociais | 🟢 | 2026-10-09 |
| IS-061 | Monitor: rótulos amigáveis por máquina (ex.: PC1-Fila1) em `lab_labels.json` | 🟢 | 2026-10-09 |
| IS-062 | Tela de bloqueio + papel de parede do SysAva (login por RA no logon) | 🟢 | 2026-10-09 |
| IS-063 | Associar o aluno ao PC pelo RA da tela de bloqueio (`lab_users.json` + coluna "Aluno (RA)") | 🟢 | 2026-10-09 |
| IS-064 | Agente não voltava após reboot (sem auto-start) — tarefa "SysAva Agent" no logon | 🟢 | 2026-10-09 |
| IS-065 | Curso Técnico de Marketing: professora + turma + 6 disciplinas + 25 alunos (script `criar_turma_professor.py`) | 🟢 | 2026-10-13 |
| IS-066 | Filtro por professor: cada docente vê só as turmas dele (mapa `professores_turmas.json`; admin vê tudo) | 🟢 | 2026-10-13 |
| IS-067 | Login tolerante: aceitar login por RA/CPF e ignorar maiúsculas (`get_user_by_ra`/`get_user_ci`) | 🟢 | 2026-10-13 |
| IS-068 | Tela de bloqueio não travava no logon — autostart via Startup comum (VBS) + fallback tarefa | 🟢 | 2026-10-13 |
| IS-069 | Estrutura de pastas turma/disciplina/aluno/**aula XX** (comando do agente, intervalo fixo) | 🟢 | 2026-10-14 |
| IS-073 | Painel web do receiver: login do professor + controles via HTTP (sem Streamlit) | 🟢 | 2026-10-14 |
| IS-074 | Receiver fora do Streamlit não carregava `.env` — login do painel e `/api/auth_ra` sempre falhavam | 🟢 | 2026-10-14 |
| IS-075 | Monitor: seção "Histórico de Hoje" aparecia vazia (filtro só de infração + fuso UTC) | 🟢 | 2026-10-14 |
| IS-076 | Desligar/Reiniciar não concluía: `shutdown` com `/t 10` → trocado por `/t 0` (imediato) | 🟢 | 2026-10-14 |
| IS-077 | (Estudo/Backlog) Monitor "online" no Streamlit Cloud: relay via Supabase (A) + túnel p/ tempo real/DNS (B) | ⚪ | 2026-10-14 |
| IS-078 | Bloqueio persistente: watchdog que derruba jogos sozinho + tela reforçada (IFEO pendente) | 🟢 | 2026-10-14 |
| IS-079 | Relatório detalhado por PC no dashboard (navegadores, jogos e apps em atividade) | 🟢 | 2026-10-14 |
| IS-080 | Autostart: `GroupId "BUILTIN\Users"` falha em Windows pt-BR — trocar por pasta Startup (VBS) | 🟢 | 2026-10-14 |
| IS-081 | Ação "Atualizar Monitor": agente baixa o lab do servidor e reexecuta elevado (UAC pede a senha admin) | 🟢 | 2026-10-14 |
| IS-082 | Plugin Monitor: botão/link para abrir o dashboard web do receiver | 🟢 | 2026-10-14 |
| IS-083 | Tela de bloqueio: memorizar o último RA (preenche no próximo logon) | 🟢 | 2026-10-14 |
| IS-084 | Relatório/dashboard: mostrar o aluno da tela de bloqueio (RA) em vez da conta Windows "ALUNO" | 🟢 | 2026-10-14 |
| IS-085 | Ao iniciar: fechar navegadores e bootloaders de jogos e abrir 1 janela só do SysAva | 🟢 | 2026-10-14 |
| IS-086 | Servidor portátil: receiver autônomo (auth via REST/bcrypt) + `INICIAR_SERVIDOR` (Python embutido) | 🟢 | 2026-10-16 |
| IS-087 | Servidor portátil: bootstrap baixa tudo sozinho (`/servidor.zip`) — resolve "não encontrou lab_receiver" | 🟢 | 2026-10-16 |
| IS-070 | (Backlog) Instaladores de ferramentas/pacotes por disciplina (kit dev mobile etc.) | ⚪ | 2026-10-13 |
| IS-071 | Log de atividade dos usuários + histórico do navegador + relatório HTML em pasta oculta (`.relatorios/`) | 🟢 | 2026-10-14 |
| IS-072 | (Em andamento) Proteção do aluno: conteúdo adulto, sites perigosos e Tor/dark web — bloqueio por categoria + alerta | 🟡 | 2026-10-13 |
| IS-088 | Planejamento 8510: sábado recomeçava em 13 depois da aula 23 registrada, o gerador automático (base 21) pulava 07:10/08:10/11:30 com o filtro “De 24” e planejava 10/06 — numeração/ocupação agora leem os `.txt` (inclui `aulas/registradas/`) e a ⚙️ Config ganhou o **sábado alvo** (`sabado_alvo_planejamento`, marcado em 20/06) para planejar só o dia demarcado | 🟢 | 2026-10-19 |
| IS-089 | SysAva principal: aba mostrava “Streamlit” e a sidebar exibia o **logo do Google** (a URL do flaticon era o “G”) — `app.py` não chamava `st.set_page_config`; agora título **SysAva** + logo próprio em `assets/logo_sysava.png` | 🟢 | 2026-10-19 |
| IS-090 | Tema azul do SysAva: paleta do logo (#2563EB) no tema do Streamlit e no CSS global (fundo navy, sidebar, botões e links azuis) | 🟢 | 2026-10-19 |
| IS-091 | Visualização da prova: texto escuro sobre fundo navy (ilegível) — agora renderiza como folha A4 branca sobre fundo claro, com sombra e botão de impressão azul | 🟢 | 2026-10-19 |
| IS-092 | Legibilidade em telas grandes: fontes/elementos pequenos com o navegador a 100% — base do Streamlit elevada de 16px para 18px | 🟢 | 2026-10-19 |
| IS-093 | Boxes de código/conteúdo em azul mais claro (principal e 8510): `pre/code/stCodeBlock`, textarea do plano e dropdown de planos com fundo `#152C52` e texto `#E5E7EB` | 🟢 | 2026-10-19 |
| IS-094 | Google Drive (conta bot/service account): sync de `data/repo` (plugins/Turmas) para o Cloud, download do `escola_ativa.db`, aba ☁️ Drive no Plugins e `scripts/drive_check.py`; upload limitado pela cota do service account | 🟢 | 2026-10-19 |
| IS-095 | Gerenciador de Notas: `float(None)` em nota do `student_scores.json` (Drive) derrubava o plugin — `_to_float` e notas saneadas | 🟢 | 2026-10-19 |
| IS-096 | Monitor do laboratório: links do painel web usavam `127.0.0.1:5000` (inacessível de outros PCs) — agora usam o IP real da LAN, com override por `SYSAVA_SERVER_URL` | 🟢 | 2026-10-20 |
| IS-097 | Roblox na bandeja/inicialização: agente limpa Run/RunOnce, Startup, StartupApproved e tarefas agendadas em todos os PCs e expõe comando no Monitor | 🟢 | 2026-10-20 |
| IS-098 | Tela de bloqueio liberava com qualquer palavra quando o servidor falhava; agora só RA válido no servidor ou senha secreta do admin (padrão `labadmin`) | 🟢 | 2026-10-20 |
| IS-099 | Tela de bloqueio aceita primeiro nome do aluno (sem caixa/acentos) e exige nome completo quando há homônimos (`ana` → `Ana Roberta`/`anaroberta`/`ANA ROBERTA`) | 🟢 | 2026-10-20 |
| IS-100 | `labadmin` não fica pré-preenchido/memorizado na tela de bloqueio nem entra na lista de máquinas (`/api/auth_ra` só aceita `role=student`) | 🟢 | 2026-10-20 |
| IS-101 | Desligar/Reiniciar remotos fecham a tela de bloqueio, restauram o Gerenciador de Tarefas e não ficam presos no `FormClosing` | 🟢 | 2026-10-20 |
| IS-102 | Atualização do agente sem UAC (`/download/lab_agent.py` + auto-restart) e tela de bloqueio auto-atualizável via `%LOCALAPPDATA%\SysAva` | 🟢 | 2026-10-20 |
| IS-103 | Dashboard: campo de tempo de liberação do Roblox (padrão 20 min); agente libera, fecha ao fim e mantém bloqueado até nova liberação — **substituído pelo IS-104** | ⚪ | 2026-10-20 |
| IS-104 | Roblox deixou de ser fechado automaticamente: o watchdog o ignora e só o comando manual **Bloquear Jogos** o encerra | 🟢 | 2026-10-20 |
| IS-105 | Servidor em conjunto (notebook + PC do laboratório): descoberta de peers, máquinas/comandos compartilhados, papel primário/assistente e auto-start no Windows | 🟢 | 2026-10-20 |
| IS-106 | Atualizar arquivos do servidor não recarregava o código em execução: `reiniciar_servidor.ps1`, `/health` com versão e detecção de tarefa apontando para outra pasta | 🟢 | 2026-10-20 |
| IS-107 | Novo guia rápido de Flutter (baixar/instalar/testar) em `plugins/atividades/flutter-instalar-e-testar.md`, com links nos tutoriais existentes | 🟢 | 2026-10-22 |
| IS-108 | Tela de bloqueio: RA falhava quando a URL salva (notebook) estava offline; agora valida `/health` e cai para cache/UDP, achando o PC do laboratório | 🟢 | 2026-10-22 |
| IS-109 | Comando **Atualizar Tela de Bloqueio (sem UAC)**: baixa a tela nova para `%LOCALAPPDATA%`, reinicia, cria Startup por usuário se preciso e evita duas telas | 🟢 | 2026-10-22 |
| IS-110 | Dashboard: PC desligado continuava aparecendo por 5 min e a página não se atualizava; agora some em 60 s, auto-refresh de 15 s e `Cache-Control: no-store` | 🟢 | 2026-10-22 |
| IS-111 | Servidor do monitor no PC do laboratório: auto-start no **boot** (SYSTEM) por padrão, watchdog que reinicia o receiver e grava `servidor.log`, checagem de dependências e `-Logon`/`-Remover` | 🟢 | 2026-10-23 |
| IS-112 | Tela de bloqueio presa em “Servidor indisponível (1/5)” quando as máquinas ligam antes do PC01: agora **aguarda até 3 min** redescoberto o servidor, com contagem e sem precisar redigitar o RA | 🟢 | 2026-10-23 |
| IS-113 | Comandos pendentes para PCs desligados executavam horas depois: **validade de 30 min** (`command_expires_at`, configurável por `COMMAND_TTL_SECONDS`), descartando Desligar/Reiniciar vencidos | 🟢 | 2026-10-23 |
| IS-114 | Identificação frágil no painel: hostname cru e conta Windows “ALUNO” apareciam como aluno — agora mostra **rótulo da máquina** (com host abaixo), **nome completo (RA)** do lock, conta Windows só como secundária, “sem RA” quando não identificado e validade de 16 h | 🟢 | 2026-10-23 |
| IS-115 | Tela de bloqueio: **seletor de aluno (nome + RA)** em vez de digitar, lista via `/api/alunos` com cache local, e abre o SysAva com `?ra=` para já preencher o login | 🟢 | 2026-10-23 |
| IS-116 | Opera subindo com o Windows: agente remove o auto-start (Run/RunOnce/Startup/tarefas) sem fechar o Opera aberto manualmente e novo comando **Limpar Inicialização do Opera** | 🟢 | 2026-10-23 |
| IS-117 | Apps Microsoft subindo com o Windows (Outlook, OneDrive, Teams, OneNote, Skype, Copilot, Office Hub, Xbox/Game Bar, Widgets): agente remove só o auto-start e novo comando **Limpar Inicialização de Apps Microsoft** | 🟢 | 2026-10-23 |
| IS-118 | Ações **Fechar / Bloquear / Desbloquear Sites/Jogos** (YouTube, Roblox, Loki, games e redes sociais): bloqueio persistente via watchdog (fecha janelas e derruba processes) até desbloquear | 🟢 | 2026-10-23 |
| IS-125 | Comando **Definir Volume em 30%** (e restaurar 100%) nos PCs: script Core Audio, sem UAC, roda na sessão do aluno e desmuta | 🟢 | 2026-10-23 |
| IS-119 | Admin/Avaliações: **editar o nome (título)** de uma avaliação existente e manter a seleção após renomear | 🟢 | 2026-10-26 |
| IS-120 | Prog. Dispositivos Móveis: aulas **33–40** do seminário (Grupo1 25–28 / Grupo2 29–32) criadas no `subject_id=5` em versão neutra (sem nomes de turma) | 🟢 | 2026-10-26 |
| IS-121 | Aulas criadas com título fora do padrão "Aula N" apareciam no Admin mas **sumiam da página Aulas**; agora entram em "Outras aulas (sem número)" | 🟢 | 2026-10-26 |
| IS-122 | IA: duas aulas de seminário (Aulas 36 e 37) para 2A e 2B — temas 20–24 e 25–28, grupos do seminário anterior | 🟢 | 2026-10-26 |
| IS-123 | DevOps: 3 aulas geradas dos PDFs da S01 para a turma I-A e versão própria para a I-B (nova disciplina) | 🟢 | 2026-10-26 |
| IS-124 | Gerador de Aulas: opção DeepSeek Cloud com pré-preenchimento de `DEEPSEEK_API_KEY` em modo local | 🟢 | 2026-10-26 |
| IS-126 | Gerador de Aulas: vídeo da aula (`links_aulas.md`) não entrava no contexto nem no plano gerado | 🟢 | 2026-10-28 |
| IS-127 | Replicação para a turma B caía na disciplina compartilhada; aulas 4–8 importadas na disciplina própria da I-B | 🟢 | 2026-10-28 |
| IS-128 | "Nenhuma turma cadastrada" com todas as turmas no banco: cache local gravava lista vazia de uma falha de rede | 🟢 | 2026-10-28 |
| IS-129 | Servidor auxiliar (PC01-LAB02) não sobe no boot e não aparece no monitor: bandeja (tray) + diagnóstico | 🟢 | 2026-10-28 |
| IS-130 | Monitor em abas (Radar/Controle/Ferramentas/Massa/Histórico/Diagnóstico) + estrutura `turma\disciplina\aluno\Aula_NN` (espaços → `_`) + pacote de atualização | 🟢 | 2026-10-28 |
| IS-131 | Baixar as atividades dos alunos zipadas no notebook (ZIP por PC em `.atividades`, lista e "baixar todos" no painel) | 🟢 | 2026-10-28 |
| IS-132 | Designar o aluno (RA) de um PC pelo painel do notebook (associação igual à da tela de bloqueio) | 🟢 | 2026-10-28 |
| IS-133 | Bandeja (tray) do SysAva e apps no notebook, estilo LM Studio, com status e "Iniciar com o Windows" | 🟢 | 2026-10-28 |
| IS-134 | Organização dos plugins: monitor movido para `plugins/monitor_rede/` (código separado do runtime) | 🟢 | 2026-10-28 |
| IS-135 | Tela de bloqueio: modo offline (lista local/Drive + carência de 15 min + fila de sincronização) | 🟢 | 2026-10-28 |
| IS-136 | Guia de acesso remoto ao laboratório com Tailscale (subnet router; substitui a ideia de DDNS) | 🟢 | 2026-10-28 |
| IS-138 | Post da Aula 01 de DevOps no fórum: Tailscale com a conta institucional (passo a passo) | 🟢 | 2026-10-28 |
| IS-139 | Abrir site (Prova Motriz) no navegador dos PCs: ação no painel, URL livre e build 7 do agente | 🟢 | 2026-10-28 |
| IS-140 | Bandeja do aluno nos PCs + copiar e-mail institucional (`emails.json` das pastas da turma) | 🟢 | 2026-10-29 |
| IS-141 | Faxina (limpeza segura) nos PCs pelo painel: temporários, restos do SysAva, logs e caches opcionais | 🟢 | 2026-10-29 |
| IS-142 | WPS Office e apps de segundo plano: remover da inicialização, encerrar helpers e desativar widgets/Copilot/Game Bar | 🟢 | 2026-10-29 |
| IS-143 | Copilot vem habilitado na inicialização: desativar por política (HKCU) + startup + processo | 🟢 | 2026-10-29 |
| IS-144 | Tela de bloqueio: status do servidor (conectado/desconectado) e aviso para ligar o PC01 | 🟢 | 2026-10-29 |
| IS-145 | Tela de bloqueio: aviso em destaque e seta para baixo/Page Down abrindo a lista de alunos | 🟢 | 2026-10-29 |
| IS-146 | Chrome: remover da inicialização e desligar o modo segundo plano (não fecha o navegador do aluno) | 🟢 | 2026-10-29 |
| IS-147 | Conta compartilhada `Alunos_EJA_Noite` (aluno) criada no Supabase e disponível na tela de bloqueio | 🟢 | 2026-10-29 |
| IS-148 | Liberar a tela de bloqueio remotamente (caso excepcional) com expiração automática | 🟢 | 2026-10-29 |
| IS-149 | Dashboard do servidor mostra o status da tela de bloqueio por PC (liberada/bloqueada/sem tela) | 🟢 | 2026-10-29 |
| IS-150 | "Abrir site": a última URL usada fica salva no servidor (`site_padrao.json`) | 🟢 | 2026-10-29 |
| IS-151 | Aluno (RA) vencido não some mais: mostra “último em dd/mm” / “Não logado” no painel e no Streamlit | 🟢 | 2026-11-03 |
| IS-152 | DevOps (Aulas 07/08): 3 projetos de CI/CD por aula publicados no fórum (I-A e I-B) | 🟢 | 2026-11-03 |
| IS-153 | DevOps (Aula 09): atividade de automação com pipeline — chatbot FAQ + execução agendada (I-A e I-B) | 🟢 | 2026-11-03 |
| IS-154 | Monitor: “Designar aluno” vale na hora nos peers e prévia mostra aluno/pasta (2 primeiros nomes) por PC | 🟢 | 2026-11-04 |
| IS-155 | Monitor: bot?o de backup de atividades no plugin + comandos n?o se perdem mais (concorr?ncia) | 🟢 | 2026-11-04 |
| IS-156 | Tela de bloqueio: so nome/RA da lista libera; senha admin apenas no PC mestre (PC01) | 🟢 | 2026-11-05 |
| IS-157 | Tela de bloqueio: RA unico (nao pode estar logado em dois PCs ao mesmo tempo) | 🟢 | 2026-11-05 |
| IS-158 | Contas coletivas (8ano, 9ano, 1alunoEja) + janela EJA 17h-23h | 🟢 | 2026-11-05 |
| IS-159 | MENTORIAS TEC II: deduplicar Aulas 21–35 (arquivar cópias) e ordenar por "Aula N" | 🟢 | 2026-11-09 |
| IS-160 | DevOps 2º ano: arquivar duplicatas do I-A e criar Aulas 17–20 nas duas turmas | 🟢 | 2026-11-09 |
| IS-161 | iSeduc: gerar/validar planos de outubro/2026 de IA, Mentorias Tech II e PC II (I-A e I-B) | 🟢 | 2026-11-09 |
| IS-162 | iSeduc: lançar notas de Programação Web Front-End (I-B T1/T2/T3 e I-A T2/T3) com T2/T3 = T1 e Alice (licença) 6,0 | 🟢 | 2026-11-10 |
| IS-163 | Bandeja: painel do servidor busca o servidor atual na rede (porta local, cache, peers.txt e UDP 5001) e abre | 🟢 | 2026-11-12 |
| IS-164 | Bloqueio rígido: Fortnite/Epic + Roblox/Loki fechados sempre; tela de bloqueio reaberta sem login (token `tela_ok.json`) | 🟢 | 2026-11-12 |
| IS-165 | Controle: várias ações por envio (chips agrupados, presets, fila `pending_queue` de 1 ação por ping) | 🟢 | 2026-11-12 |
| IS-169 | Monitor: runtime movido para `data/repo/plugins/monitor/` (receiver, agente, tela, bandejas, dados) e paths corrigidos | 🟢 | 2026-11-12 |
| IS-170 | Ferramentas: abas internas (Atividades/Sites e RA/Tela/Manutenção) + "Abrir SysAva com RA" no navegador escolhido (agente build 16) | 🟢 | 2026-11-12 |
| IS-171 | Bandejas: servidor mostra/atualiza IP e abre 2º servidor (peer); aluno mostra e copia o RA | 🟢 | 2026-11-12 |
| IS-172 | Roblox não desbloqueava: watchdog fechava jogos sempre; agora só com "Bloquear Sites/Jogos" ativo (agente build 17) | 🟢 | 2026-11-12 |
| IS-173 | Gerador de aulas: "Pasta não encontrada" em Microsserviços I-A (pasta no disco sem o "V": `MICROSSERIÇOS`) | 🟢 | 2026-11-13 |
| IS-174 | Monitor: preferencia de servidor pelo PC01 do laboratorio (agente build 18) | 🟢 | 2026-11-16 |
| IS-175 | Arquitetura de Microsserviços: PDFs do S01 tratam de testes; 8 aulas corretas geradas (I-A e I-B) | 🟢 | 2026-11-16 |
| IS-176 | Monitor: aba Ferramentas ganhou "Texto e Comando" (alerta + comando digitado) no painel web e no Streamlit | 🟢 | 2026-11-16 |
| IS-177 | PC01: ATUALIZAR_PC01.bat sem IP fixo (descoberta por UDP/cache + `descobrir_servidor.ps1`) | 🟢 | 2026-11-16 |
| IS-178 | PC01: `CORRIGIR_ACESSO_PC01.bat` (firewall 5000/8501/5001, Tailscale Private, relatório de acesso) | 🟢 | 2026-11-16 |
| IS-179 | PC01 autônomo sem notebook: RA valida pelo `alunos_cache.json` e cache incluído no `servidor.zip` | 🟢 | 2026-11-16 |
| IS-180 | Tela de bloqueio: letras de mensagem/status maiores, aviso de servidor sem resposta e descoberta UDP do PC01 no status | 🟢 | 2026-11-16 |
| IS-181 | Bandeja: "Iniciar servidor neste PC" volta a funcionar mesmo com o notebook online (regressão do buscador de servidores) | 🟢 | 2026-11-16 |
| IS-182 | Bandeja: busca de servidores inclui peers do Tailscale (PC01 acessível de casa/4G) | 🟢 | 2026-11-16 |
| IS-183 | Arquitetura de Microsserviços: aulas 09-10 de laboratório (projeto SysLoja em FastAPI) | 🟢 | 2026-11-16 |
| IS-184 | Arquitetura de Microsserviços: aulas 11-13 de laboratório (Docker, Compose e CI/CD) | 🟢 | 2026-11-16 |
| IS-185 | Arquitetura de Microsserviços: bloco 1 fechado (aulas 14-19 + AV1 na 20) e `plano.txt` | 🟢 | 2026-11-16 |
| IS-186 | Alerta do Monitor: janela com texto selecionável e botão Copiar (agente build 19) | 🟢 | 2026-11-16 |
| IS-187 | Monitor: página `/instrucoes` com comandos copiáveis e alerta Tk com texto selecionável/maior | 🟢 | 2026-11-16 |
| IS-188 | Notas iSeduc: replicação T1 → T2/T3 lendo o próprio portal (Fundamentos UI/UX I-A) | 🟢 | 2026-11-17 |
| IS-189 | Notas iSeduc: recuperações RPT (RM do SysAva) em UI/UX I-A e I-B | 🟢 | 2026-11-17 |
| IS-190 | Notas iSeduc: Programação Mobile I-A — T1/T2/T3 do plugin Notas lançados e ficha | 🟢 | 2026-11-17 |
| IS-191 | Registro de aulas: Mobile I-B — 10 aulas de 23/07 a 30/07 (Aulas 13–22) | 🟢 | 2026-11-17 |
| IS-192 | Registro de aulas: Mobile 40/40 (I-A/I-B) + sync do histórico e limpeza da fila | 🟢 | 2026-11-17 |
| IS-137 | Projeto Feira das Profissões: 6 aulas em `plugins/atividades/Atividades_florestan/` | 🟢 | 2026-10-29 |
| IS-193 | Bandeja do aluno: sair da conta, reabrir a tela de bloqueio e liberar o RA | 🟢 | 2026-11-18 |
| IS-194 | Monitor: Atualizar Bandeja do Aluno reinicia a instância antiga | 🟢 | 2026-11-18 |
| IS-195 | Gestão de Usuários: adicionar, desativar acesso e remover contas | 🟢 | 2026-11-18 |
| IS-196 | Painel do monitor: aba Usuários (criar, desativar, remover contas) | 🟢 | 2026-11-18 |
| IS-197 | Tela de bloqueio: professora Adriana liberada no PC01 | 🟢 | 2026-11-18 |
| IS-198 | Aulas: status não ficava verde por quizzes duplicados (Microsserviços) | 🟢 | 2026-11-18 |

---

## IS-001 — Plugin de Atividades: dataset de pontuação por atividades 🟢

**Pedido:** visualizar a pontuação distribuída por atividades no plugin de
qualitativo (aba **Atividades**).

**Solução:** nova seção **📊 Pontuação Distribuída por Atividades**, detalhada
por lançamento (`Data`, `Estudante`, `Aula`, `Bloco`, `Pontos`), filtro por bloco
(1-20 / 21-40) e métricas de total distribuído e nº de lançamentos. Filtra pela
disciplina selecionada na sidebar; entradas antigas sem `subject_id` são
inferidas pela aula.

**Arquivos:** `data/repo/plugins/daily_activities.py`

**Validar:** abrir Plugins → Atividades, escolher turma/disciplina e conferir a
tabela abaixo do botão de salvar.

---

## IS-002 — Quizzes marcados como respondidos sem responder 🟢

**Sintoma:** alunos relataram quizzes aparecendo como "Concluída" (círculo
verde) sem terem respondido; tentativas e nota compartilhadas entre aulas.

**Causa raiz:** o gerador criava todos os quizzes com o **mesmo título
genérico** (`📝 Quiz: Teste seu Conhecimento!`) e o sistema identificava a
conclusão/tentativa **pelo título**. Responder um quiz marcava vários outros.

**Evidência:** 378 quizzes com apenas 164 títulos distintos; 93x o título
genérico; na disciplina `FUNDAMENTOS DE UI / UX OU IHC`, 17 de 17 quizzes com o
mesmo título.

**Solução:**
- `services/quiz_parser.py`: título único `Quiz: {título da aula}` e remoção dos
  quizzes anteriores da aula antes de recriar (fim das duplicatas).
- `views/quiz.py`: grava `| quiz_id:X` no histórico e filtra tentativas por ID.
- `views/aulas.py`: conclusão por `quiz_id` (títulos genéricos antigos ignorados).
- `services/database.py`: `get_student_score` e `get_user_progress_stats`
  deduplicam por `quiz_id`.

**Migração/limpeza executada:**
- `scripts/migrate_quiz_titles.py --apply` → 336 quizzes renomeados, 68
  duplicatas removidas.
- `scripts/reset_quiz_attempts.py --apply` → 2666 tentativas remapeadas com
  `quiz_id` (notas preservadas), 364 ambíguas/genéricas removidas.

**Arquivos:** `services/quiz_parser.py`, `views/quiz.py`, `views/aulas.py`,
`services/database.py`, `scripts/migrate_quiz_titles.py`,
`scripts/reset_quiz_attempts.py`

**Validar:** abrir uma aula, responder o quiz e confirmar que apenas aquela aula
fica verde; conferir tentativas em `views/quiz.py`.

---

## IS-003 — Egress do Supabase estourando a cota de 5 GB 🟢

**Sintoma:** consumo mensal de saída de banda acima do limite do plano gratuito.

**Diagnóstico:** não é conteúdo grande — 344 aulas somam ~1,6 MB de
`full_content` e **não há Base64**. O problema é **volume de queries repetidas**
a cada rerun do Streamlit e laços N+1 por aluno.

**Solução:**
- `services/local_cache.py`: cache SQLite **ligado por padrão** (opt-out via
  `DISABLE_LOCAL_CACHE = true` / `ENABLE_LOCAL_CACHE = false`). Fallback seguro
  se o disco não for gravável.
- `services/database.py`: cache + invalidação nas consultas quentes:
  `get_user_history` (120s), `get_student_score` (120s),
  `get_user_enrollment` (1h), `get_user_forum_lessons_by_subject` (5min),
  `get_lesson_by_id` (1h), `get_quiz_for_lesson`/`get_quiz_by_id`/
  `get_quiz_questions`/`get_quizzes_for_subject`/`get_all_quizzes_summary` (1h),
  `get_school` (6h).
- `get_all_users` deixou de baixar o **hash de senha**.
- `_compute_student_score` usa `get_all_quizzes_summary()` (cacheado) em vez de
  consultar quizzes a cada chamada.

**Arquivos:** `services/local_cache.py`, `services/database.py`

**Validar:** `python -c "from services import local_cache as lc; print(lc.cache_enabled())"`
deve imprimir `True`; acompanhar o egress no app **Supabase Monitor**.

---

## IS-004 — Lentidão no dataframe do plugin de qualitativo 🟢

**Sintoma:** demora para exibir a tabela de pontos (uma consulta de score por
aluno).

**Solução:**
- `services/local_cache.py`: nova tabela `_score_cache` + `get_scores_bulk`,
  `set_scores_bulk`, `invalidate_scores` (TTL 600s).
- `data/repo/plugins/daily_activities.py`: `get_scores_for_students()` carrega a
  turma em lote (cache antes do Supabase) e botão **🔄 Atualizar notas**.

**Arquivos:** `services/local_cache.py`,
`data/repo/plugins/daily_activities.py`

**Validar:** abrir a aba Atividades; a segunda carga não deve consultar o
Supabase (3 alunos: 3 queries → 0 na recarga).

---

## IS-005 — Configurar cache no Streamlit Cloud ⚪

O cache agora é **ligado por padrão**, então o Cloud já se beneficia. Se for
necessário desligar em algum ambiente, definir nos secrets:

```toml
DISABLE_LOCAL_CACHE = true
```

**Pendente:** decidir se o Cloud deve usar TTLs maiores para economizar ainda
mais, ou menores para dados mais frescos.

---

## IS-006 — Cachear avaliações/submissões (admin) ⚪

`get_assessments_by_subject`, `get_assessment_questions`,
`get_submission_answers` e afins ainda não têm cache. São usados
principalmente em telas de admin/avaliação. Avaliar custo/benefício.

---

## IS-007 — Quizzes feitos não contabilizados no score 🟢

**Sintoma:** aluna com vários quizzes respondidos aparecia com **Quizzes = 0**
no painel do professor (ex.: `MARIA CRYSTHIELY DA SILVA`, disciplina 8).

**Causa:** o app em execução ainda usava o código antigo (sem `| quiz_id:`).
As tentativas foram gravadas com o **título novo** (já renomeado pela migração),
mas **sem `quiz_id`**. Como o IS-002 passou a exigir `quiz_id` no
`get_student_score`, esses pontos zeraram.

**Solução:** em `_compute_student_score` e `get_user_progress_stats`, quando o
log não tem `quiz_id`, resolve-se o quiz pelo **título** (que agora é único por
aula) via mapa `quiz_title_to_id`. Assim a tentativa antiga e a nova caem na
mesma chave `id:X` — não perde ponto nem conta em dobro.

**Arquivos:** `services/database.py`

**Validar:**
```powershell
python -c "from services import database as db; print(db.get_student_score('[RA]', filter_subject_id=8))"
```
Deve retornar `quiz` > 0 (no caso, 41).

---

## IS-008 — Lista negra de faltosos inicia a chamada como "Falta" 🟢

**Pedido:** no plugin **Frequência**, os alunos da lista negra de faltosos devem
já aparecer com status **Falta** (em vez do padrão "Presente").

**Solução:** `student_attendance.py` lê `data/excecoes_alunos.json`
(`blacklist` de RAs + `blacklist_names`, com nomes normalizados) e usa "Falta"
como status inicial desses alunos. Mostra um aviso com os nomes encontrados na
turma. Valores já salvos **não** são sobrescritos.

**Arquivos:** `data/repo/plugins/student_attendance.py`

**Validar:** Plugins → Frequência → turma `2ª SÉRIE - Turma I-B (Técnico DS)`:
`GUSTAVO RAFAEL FRIGERI`, `ISADORA FERNANDA DA SILVA`, `[ALUNO] DE SOUSA SILVA`
e `JANAYRA SOARES BRANDÃO` devem iniciar como **Falta**.

**Observação:** `data/excecoes_alunos.json` está no `.gitignore` (é local). Se o
arquivo não existir, a lista fica vazia e o comportamento volta ao padrão
(todos "Presente").

---

## IS-009 — Base64/SVG inflando aulas — backup limpo e migração para novo banco 🟢

**Sintoma:** o Supabase restringiu o serviço (`Services restricted` — organização
estourou a cota). O app quebrava com `pydantic ValidationError` do `postgrest`
(que mascara a mensagem real `{"message": ...}`).

**Causa raiz:** `services/pdf_extractor.py::convert_markdown_images_to_svg`
embutia imagens em **Base64** (`<image href="data:image/...;base64,...">`) dentro
de `lessons.description`, e `views/aulas.py::clean_svg_content` re-embutia Base64
tanto na renderização quanto **antes de gravar** (`views/admin.py`,
`views/gerador_aulas.py`). O cache do Supabase confirmou: 37 blocos Base64 em
`lessons`, ~1 MB de texto inflado (linha de descrição chegava a 237 KB).

**Solução:**
- `services/pdf_extractor.py`: nova barreira `strip_base64_images()` (remove só o
  Base64, **preserva SVG vetorial puro** e links locais). O
  `convert_markdown_images_to_svg` deixou de codificar raster em Base64 — imagens
  viram link para o arquivo local (padrão do AGENTS.md).
- `views/aulas.py`: `clean_svg_content` agora remove Base64 em vez de re-embutir.
- `views/gerador_aulas.py` / `views/admin.py`: barreira final antes de salvar.
- `services/database.py`: `_sanitize_text()` aplicado em `create_lesson`,
  `upsert_lesson`, `update_lesson_plan_fields` e `add_forum_post` (choke point).
- `scripts/backup_clean.py`: backup limpo a partir de `data/escola_ativa.db`
  (SQLite + JSONL + manifesto), removendo Base64.
- `docs/NOVO_BANCO_SCHEMA.sql`: DDL idempotente do novo projeto Supabase
  (modelo canônico + tabelas de automação + funções de resolução de disciplinas).
- `scripts/restore_new_supabase.py`: restaura o backup limpo no novo projeto.

**Evidência:** backup gerado em `data/backup_clean_2026-09-22_0757/` — 37 blocos
Base64 removidos, ~1,01 MB de Base64 eliminados; `description` máxima caiu de
237 KB para 20,7 KB; 60 linhas com SVG vetorial preservadas; 0 Base64 restante.

**Auditoria e redução (ver `docs/AUDITORIA_BANCO.md`):** o portal usa o Supabase
(21 tabelas) e a automação usa o SQLite `escola_ativa.db` (34 tabelas). As 13
tabelas de automação **não** vão para o novo Supabase; as vazias/abandonadas
(`qualitative_points`, `grade_milestones`, `user_reminders`, `user_profiles`) e a
inexistente `student_scores` não serão recriadas. O novo projeto nasce com 21
tabelas (25.228 linhas no restore). Consolidações de config/plugins ficam para
depois da migração.

**Arquivos:** `services/pdf_extractor.py`, `services/database.py`,
`views/aulas.py`, `views/gerador_aulas.py`, `views/admin.py`,
`views/home.py`, `views/quiz.py`,
`scripts/backup_clean.py`, `scripts/prepare_restore.py`,
`scripts/restore_new_supabase.py`,
`docs/NOVO_BANCO_SCHEMA.sql`, `docs/AUDITORIA_BANCO.md`

**Migração concluída (2026-09-22):** novo projeto Supabase com as 21 tabelas
essenciais; 24.087 linhas restauradas e sequências reajustadas. Verificação
origem × Supabase: **21/21 tabelas com contagem idêntica**. Cache local limpo e
smoke test do portal OK (2 turmas, 16 disciplinas, 364 aulas, sem Base64).

Tratamentos aplicados na preparação (`scripts/prepare_restore.py`):
- `historico_aulas.data_aula` mantido em `dd/mm/aaaa` (o Supabase guarda como
  TEXTO, igual ao bot do iSeduc). No projeto novo, ajustar o tipo com
  `ALTER TABLE public.historico_aulas ALTER COLUMN data_aula TYPE text USING to_char(data_aula,'DD/MM/YYYY');`
- `attendance`: 107 linhas de teste corrompidas removidas + 835 duplicatas
  idênticas; 1 `student_number` fora do INTEGER normalizado.
- Duplicatas removidas respeitando as UNIQUE: `historico_aulas` 167,
  `weekly_schedule` 20, `assessments` 11 (PK).
- 1 aula de teste com `id` UUID removida; 214 ids nulos preenchidos.
- **Pós-migração:** o Supabase devolve `timestamptz` misturando com e sem
  microssegundos; `pd.to_datetime` estourava em `views/home.py` e `views/quiz.py`.
  Corrigido com `format='ISO8601', errors='coerce'`.
- **Pós-migração:** `get_user` deixou de estourar quando o banco falha (ex.: cota
  ou secret incorreta no Cloud): o fallback agora é protegido, registra o erro no
  log e retorna `None` (login mostra "usuário ou senha incorretos" em vez de
  traceback).

**Observação:** o `historico_aulas` local tinha 566 linhas contra 1.234 no
Supabase antigo (inacessível durante o bloqueio) — a diferença não pôde ser
recuperada.

**Validar:**
```powershell
python scripts/backup_clean.py
python scripts/prepare_restore.py
python scripts/restore_new_supabase.py --dry-run
```

---

## IS-010 — Auditoria e limpeza de duplicatas de bot no fórum 🟢

**Sintoma:** o EduBot/SysAva Bot aparecia com mensagens repetidas nos fóruns,
aumentando o fluxo de dados.

**Diagnóstico:** posts de bot eram republicados a cada ação:
- `views/gerador_aulas.py` postava o desafio do EduBot **toda vez** que a aula era
  salva/gerada/replicada (sem checar se já existia).
- `scripts/seed_lessons.py` postava o SysAva Bot a cada execução (não idempotente).

**Evidência:** 243 posts de bot; 27 grupos duplicados (mesmo texto na mesma aula),
29 cópias extras (~14,5 KB). Ex.: `SysAva Bot` 3× na aula 273; `EduBot 🤖` 2–3× em
27 aulas.

**Solução:**
- `services/database.py`: novo `has_bot_post(lesson_id, bot_name)`.
- `views/gerador_aulas.py`: só posta o desafio se a aula ainda não tiver post do
  EduBot (2 pontos: geração e replicação).
- `scripts/seed_lessons.py`: pula o post do SysAva Bot se já existir.
- `scripts/cleanup_forum_duplicates.py`: remove duplicatas (dry-run por padrão;
  `--apply` para remover). Só mexe em posts de bot.
- `views/gerador_aulas.py`: nova opção na sidebar **💬 Fórum → "Publicar desafio
  do EduBot no fórum"** (marcada por padrão). Desmarcada, gera/salva a aula sem
  criar o post do EduBot (geração e replicação).

**Resultado:** 29 posts removidos; 243 → 214 posts de bot, 0 duplicatas.

**Arquivos:** `services/database.py`, `views/gerador_aulas.py`,
`scripts/seed_lessons.py`, `scripts/cleanup_forum_duplicates.py`

**Validar:**
```powershell
python scripts/cleanup_forum_duplicates.py          # deve mostrar 0 a remover
```

**Nota (backlog):** o Fórum Geral (`get_forum_posts()` sem aula) ainda baixa
**todos** os posts (~1 MB) com cache só de `st.cache_data` (120 s), sem o
`local_cache` SQLite. É o maior ofensor de egress restante no fórum.

---

## IS-011 — Aba Portal (iSeduc): esqueleto Planejar/Registrar/Notas 🟡

**Objetivo:** separar no app principal a responsabilidade de lidar com o **Portal
iSeduc** (planejar aula, registrar aula com plano/frequência/atividades e lançar
notas), hoje espalhada em `apps/api` e `apps/planejamento_registro`.

**Decisões:**
- Página **Portal** no menu principal (visível a `admin`/`teacher`), com submenu
  interno: **Planejar aulas**, **Registrar no Portal**, **Notas**.
- Arquitetura **híbrida**: leitura de dados no **Supabase**; ações de robô
  (registrar/raspagem) via **API local** (`apps/api`), que só existe rodando
  localmente — no Cloud a UI mostra aviso e desabilita as ações.
- Construção incremental: primeiro o esqueleto (feito), depois cada subpágina.

**Entregue (esqueleto):**
- `services/portal_api.py`: cliente da API local com falha graciosa
  (`PORTAL_API_URL`, padrão `http://127.0.0.1:8000`).
- `views/portal.py`: página com as 3 subpáginas, status da automação local e
  resumos de leitura (planejamento pendente, histórico recente, avaliações).
- `app.py`: item **Portal** no menu (admin/teacher) e roteamento.

**Observação:** `apps/` está no `.gitignore` (não vai ao Cloud), por isso o Portal
mora em `views/`/`services/` e não importa módulos de `apps/`.

**Arquivos:** `services/portal_api.py`, `views/portal.py`, `app.py`

**Próximos passos:** definir e implementar as ações de cada subpágina
(gerar/editar plano; disparar `registrar_lote`/`raspagem`; lançar/sincronizar
notas).

**Validar:** logar como admin/professor → menu **Portal** → alternar as 3 seções.

---

## IS-012 — Gerador de aulas salvando opções com marcador "[x]/[ ]" no texto 🟢

**Pedido:** ao gerar uma aula, o quiz salvo apresentava alternativas com o marcador
`[x]`/`[ ]` impresso no texto da opção, além de nem sempre marcar a resposta
correta.

**Causa:** a IA produz variações do formato de alternativas (`A) [x] Opção`,
`**A) [x]**`, `**[x]**`, `A. Opção (x)`), mas o parser (`services/quiz_parser.py`)
só reconhecia o marcador `[x]` quando ele iniciava a linha (checkbox). Quando vinha
combinado com letra (`a) [x] ...`), a opção era salva com o `[x]` literal no texto e
o índice da correta ficava errado.

**Correção:** em `services/quiz_parser.py`:
- Normaliza marcadores em negrito: `**[x]**` → `[x]`, `**b)**` → `b)`, `**(x)**` → `(x)`.
- Reconhece `[x]`/`(x)` embutido em opções com letra e marca a alternativa correta.
- Remove marcadores residuais `[x]`/`[ ]`/`(x)` (e `*` de negrito) do texto salvo.

**Arquivos:** `services/quiz_parser.py`, `docs/ISSUES_LOCAIS.md`

**Validar:** gerar uma aula com quiz (`A) [ ] … B) [x] …`) e conferir no banco/
painel que as opções saem sem o `[x]` e com a correta marcada.

---

## IS-013 — Plugin Atividades: exportar relatório CSV de pontos por aula 🟢

**Pedido:** após um erro na pontuação dos qualitativos, precisar exportar um
relatório para conferir os pontos de atividade de **todas as aulas** de uma
disciplina.

**Solução:** a seção **📊 Pontuação Distribuída por Atividades** ganhou dois
botões de exportação — **📥 Baixar CSV** e **🌐 Baixar HTML** — sempre com
**todas as aulas** da disciplina (ignorando o filtro de bloco da tela), com as
colunas `Data, Estudante, Aula, Bloco, Pontos`.

**Arquivos:** `data/repo/plugins/daily_activities.py`

**Validar:** Plugins → Atividades → escolher turma/disciplina → tabela de
detalhe → botões CSV/HTML geram `relatorio_atividades_{turma}_{disciplina}.(csv|html)`.

---

## IS-014 — Qualitativo vazando entre disciplinas (pontos órfãos sem subject_id) 🟢

**Sintoma:** aluna sem atividades em **FUNDAMENTOS DE UI / UX OU IHC** aparecia
com **Qualitativo 6.0**. Exemplo: `MARIA FERNANDA DOS SANTOS LIMA` → 6.0 no
quadro de notas, embora não tivesse nenhuma atividade/lesson daquela disciplina.

**Causa raiz:** no plugin `student_scores.py`, `get_student_qualitative_points`
somava **qualquer ponto sem `subject_id`** ao total de **todas** as disciplinas
(`elif p_sid is None: total_pts += pts`). A aluna tinha 4 lançamentos órfãos de
27/05/2025 (2 + 4 − 6 + 6 = 6.0), lançados via Quadro de Notas da disciplina
**INTELIGÊNCIA ARTIFICIAL** sem preencher `subject_id`/`lesson_id` — e eles
inflavam o qualitativo de toda disciplina.

**Correção:** pontos sem `subject_id` (ex: lançados na "Visão Geral") só são
atribuídos à disciplina atual se o nome dela (normalizado) aparecer no campo
`notes` do lançamento. Pontos com `lesson_id` continuam resolvidos pelo mapa
de aulas.

**Resultado validado (dados reais da aluna):** UI/UX=IHC → 0.0, IA → 6.0,
POO → 2.5, Web Front-end 2026B → 0.5, Visão Geral → 6.0.

**Arquivos:** `data/repo/plugins/student_scores.py`

**Validar:** Plugins → Notas → Fundamentos UI → qualitativo da aluna agora 0.0;
Inteligência Artificial mantém 6.0.

---

## IS-015 — Planejamento/Registro: IA com 51/40 registros local vs 28/27 no portal 🟢

**Sintoma:** no app de Planejamento e Registro, a disciplina **INTELIGÊNCIA
ARTIFICIAL** mostrava **51** registros na Turma I-A (309197) e **40** na I-B
(314114), mas o portal iSeduc exibia **28** e **27**.

**Causa raiz:** `historico_aulas` tinha **duplicatas das mesmas aulas**. A
raspagem grava o histórico com o **nome atual da turma** (ex.: `2ª SÉRIE -
Turma I-A (Técnico DS)`), mas o robô de registro antigo gravou as mesmas aulas
com o rótulo antigo do portal (`EMTPDES-SIS-2ª SERIE - INTEGRAL-I-A`) e, nos
meses de fev-mar/2026, também no horário antigo `09:10 às 10:10` (aulas depois
movidas para `10:30 às 11:30`). Como o UNIQUE de `historico_aulas` é sobre o
**texto** `(data_aula, horario, turma, disciplina)`, o `INSERT OR REPLACE` da
raspagem **não** substituiu essas linhas — gerando 2-3 linhas por aula. O app
contava **linhas**; o portal conta **aulas**.

**Evidência:** Turma A = 28 linhas com o nome atual da turma (status `Aula
confirmada`) = exatamente o que o portal mostra; o restante (09:10 antigos,
duplicatas `10:30` e `Aguardando confirmação`) é resíduo. Turma B: a aula
excluída usa o rótulo antigo, então some com o filtro (27 = 28 datas − 1 excluída).

**Correção:** todas as consultas de histórico do app
(`apps/planejamento_registro/planejamento_registro_streamlit.py`) agora filtram
`turma = <nome atual da turma>` (via `_nome_turma_atual()`) e ignoram status
`Aula Excluída`: `panel_data`, `listar_historico`, `proximo_numero`,
`renumerar_planejamento`, `reconciliar` e `status_sabado`. Dados **não** foram
apagados — as linhas residuais continuam no banco.

**Arquivos:** `apps/planejamento_registro/planejamento_registro_streamlit.py`

**Validar:** app Planejamento e Registro → Turma A/B → IA → Painel mostra
**28/27** "Registradas (portal)" e Reconciliação bate com o portal.

---

## IS-016 — Gerador de planos: Mentoria Tech II não gerava datas novas com lições 🟢

**Sintoma:** em Planejamento e Registro → MENTORIAS TEC II, o Painel mostrava
"Última aula registrada no portal: 29/08/2026" (Turma A) / 28/08 (Turma B), mas
o botão "Gerar planos" não criava **nenhuma** data nova com lição até hoje
(24/09/2026).

**Causa raiz:** o contador `next_aula_num` do gerador
(`apps/planejamento_registro/core/gerador.py`) era inicializado com o **total
de linhas** de `historico_aulas` por turma/disciplina — incluindo o **resíduo
de bot antigo** (nome de turma/horário antigos, mesmo problema do IS-015). Na
Mentoria isso dava **45** (Turma A) e **38** (Turma B) vs. `max_hours = 40`
(subjects). Como toda aula gerada exige `seq_num = current_count + 1 ≤
max_hours`, o primeiro `seq = 46` já estourava o limite → **todos os slots eram
pulados** em `if seq_num > max_hours_disc: continue`.

**Evidência:** Turma A/B com `max_hours=40`; grade semanal tem slots reais
`Ment.Tec.II` (Terça 13:30 p/ 309197; Sexta 10:30 p/ 314114), sem bloqueios nem
feriados em set/2026; `planejamento` de disc 2 vazio. Linhas canônicas = 26 por
turma (set raspado do portal = 378 ao todo). Com a correção, o gerador produz
planos com lição de 01/09 a 22/09 (A) e 04/09 a 18/09 (B).

**Correção:** o gerador agora desconsidera linhas não-canônicas do histórico
(turma ≠ nome atual; fallback p/ turmas sem nenhuma linha canônica), tanto na
montagem de `historico_set` (bloqueio de slots) quanto na contagem
`hist_count` usada por `next_aula_num`. Removido o `GROUP BY` sobre todas as
linhas.

**Arquivos:** `apps/planejamento_registro/core/gerador.py`

**Validar:** app Planejamento e Registro → Turma A → MENTORIAS TEC II → "Gerar
planos" gera `plano_309197_2_2026-09-01_1330.txt` … `2026-09-22` (com lição) e
continua até 13/10; Turma B gera `plano_314114_2_2026-09-04_1030.txt` … 16/10.
Obs.: cada slot de Mentoria aparece 2× na grade (2h semanais) — o 2º passa a
ser reportado como `skipped` (arquivo já existe), comportamento pré-existente.

---

## IS-017 — Gerador de planos: lições fora do padrão de título "Aula XX" quebravam a fila de planejamento 🟢

**Sintoma:** ao revisar `aulas/prontas` de MENTORIAS TEC II da Turma A, os planos
de 22/09 a 06/10/2026 traziam conteúdo-lixo de lições que **não seguem** o padrão
de título `Aula XX`, p.ex.: "--- Configurações Iniciais ---", "Usamos o
$PSScriptRoot...", "Conta Pessoal (Padrão)" e "Setup PowerShell" (subject 2,
ids 69–72), "[Markdown] Estrutura para o seu Jupyter Notebook" (subject 11,
id 55) e "Documentação Técnica..."/"Jogo 2D simples com Pygame" (subject 1,
ids 1–2). Essas lições (fragmentos/placeholders) eram escolhidas normalmente
quando a sequência chegava às suas posições.

**Causa raiz:** a seleção de lição usava apenas a posição
`lessons_list[pedagogical_idx - 1]`, sem validar o formato do título; qualquer
registro solto na tabela `lessons` entrava na fila elegível ao planejamento.

**Correção:** adicionada a helper de módulo `_eh_lesson_planejavel(titulo)`
(regex `^\s*Aula\s+\d+`, `re.IGNORECASE`, contemplando acentos/variações como
"Aula 05", "Aula 27: ..."). Na seleção (`gerar_txt_planos`), a lição candidata
só é atribuída se o título passar no filtro; caso contrário `lesson = None` (o
plano não é gerado com conteúdo inválido e, no modo `prontas`, o arquivo não é
criado). **Não** se alterou o índice da lista / `sequence_map`.

**Ordenação (atualização 25/09):** a fila de lições planejáveis era montada com
`ORDER BY subject_id, id ASC`, o que fazia os títulos saírem **fora da ordem
crescente** (lições legadas da auditoria têm `id` alto, ex.: "Aula 11" com
`id=103` antes de "Aula 1" com `id=40`; a sequência gerada degradava para
"Aula 24/25" seguida de "Aula 11/12"). A fila agora é ordenada pelo **número
extraído do título** via `_numero_aula()`/`_ordenar_lessons_fila()` (None por
último; empates de mesmo número mantêm a ordem original — duplicatas legadas
ex.: Aula 11 id 103/50, Aula 24 id 478/498). O caminho manual do app
(`database_model.get_lesson_content_by_number`) já ordenava por número de
título e não precisou de mudança.

**Verificação:** regex validada contra todas as lições de subjects 1, 2, 3, 4,
6, 8, 11, 30, 33, 34, 35 (válidas por subject: 11=40, 3=21, 4=40, 2=33, 1=33,
30=38, 34=41, 33=44, 6=17, 8=31, 35=0). Teste end-to-end: rodada `pendentes`
p/ Turma A disc 2 e 11 com **zero** planos contendo conteúdo proibido; no modo
`prontas` p/ disc 2, nenhum arquivo novo é criado (as posições inválidas 34–37
caem como `Sem lição`, igual 38–40 p/ superfície de lições).

**Arquivos:** `apps/planejamento_registro/core/gerador.py`

**Validar:** Planejamento e Registro → Turma A → "Gerar planos" (pendentes):
nenhum `[CONTEUDO]` contém "--- Configurações Iniciais ---", "Setup PowerShell",
"Conta Pessoal (Padrão)" ou "Jupyter Notebook"; e os títulos das lições no
plano seguem ordem crescente de Aula (Mentoria A 01→22/09: Aula 24, 25, 26,
28 — a "27" só seria gravada no 2º passe do slot duplicado de 2h, que já cai
como `skipped`). Planos além da grade curricular continuam caindo no fallback
genérico "DISC - Aula N" (comportamento pré-existente no modo `pendentes`).
Planos já existentes em `aulas/prontas` com conteúdo-lixo permanecem no disco
(não são apagados nem regenerados automaticamente); para limpar, usar
"Sobrescrever existentes".

---

## IS-018 — Frequência dos planos só consultava a lista negra (tabela `attendance`/JSON não eram lidos) 🟢

**Sintoma:** os planos gerados traziam a chamada `[FREQUENCIA]` com **todos os
alunos como Presente**, exceto os da lista negra
(`data/excecoes_alunos.json` → `blacklist`/`blacklist_names`). A frequência
real (faltas registradas) não aparecia, mesmo existindo duas fontes:
a **tabela `attendance`** do banco local (sincronizada do Supabase, datas até
26/05/2026) e o **`data/repo/plugins/student_attendance.json`** (147KB).

**Causa raiz:** `banco.load_attendance_map_for()` lia os JSONs apenas em
`api/plugins/` (pasta que **não existe** no projeto) e esperava o formato
aninhado `{turma: {disc: {data: {ra}}}}` — mas o arquivo real usa o formato
plano `{turma: {data: {ra}}}` e vive em `data/repo/plugins/`. Resultado: o mapa
de frequência sempre voltava vazio e só restava a regra da lista negra. O
"Gerar plano" manual do app (`montar_conteudo_plano`) nem sequer consultava o
mapa de frequência (passava `attendance_map=None` ao `build_plan_txt`).

**Correção** em `apps/planejamento_registro/core/banco.py`:
- `load_attendance_json()` agora procura em `data/repo/plugins/` (atual) e
  depois em `api/plugins/` (compatibilidade).
- Novo `load_attendance_from_db(turma_id, data_iso)`: lê a tabela `attendance`
  por **data exata**, casando as linhas pelo **nome da turma normalizado**
  (a coluna `class_name` tem variações de escrita/acento; `student_number`
  guarda o nº de ordem, não o RA — o mapa sai por NOME em maiúsculas).
- `load_attendance_map_for()` prioriza: **1)** tabela `attendance`, **2)** JSONs
  (corrigido → normalizado → raw → planejado), e passou a reconhecer o
  **formato plano** do JSON.
- `montar_conteudo_plano()` (plano manual no app) agora também consulta
  `load_attendance_map_for` e repassa ao `build_plan_txt`.

**Arquivos:** `apps/planejamento_registro/core/banco.py`,
`apps/planejamento_registro/planejamento_registro_streamlit.py`

**Validar:** `load_attendance_map_for("309197", "2", "2026-05-12")` → origem
`tabela attendance`, 8 faltas reais (12 Presente / 8 Falta no plano manual);
datas sem chamada seguem com `Presente` + lista negra. A regra absoluta da
lista negra (`blacklist` SEMPRE `Falta`) foi mantida.

---

## IS-019 — Gerador de planos: tipos de estratégia configuráveis + filtro de intervalo de aulas a gerar 🟢

**Solicitação:** criar uma lista de tipos de estratégia ("Aula expositiva",
"Aula baseada em projetos", "Aula de atividades em laboratório") e um filtro
que permita gerar planos apenas dentro de um intervalo de número de aula (seq).

**Causa raiz:** a estratégia era um valor fixo `"Aula expositiva e prática."`
(no `'estrategia'` do plano e como default do `build_plan_txt`) e
`gerar_txt_planos` não tinha parâmetro de intervalo — a UI não oferecia escolha
de estratégia nem limites de aula.

**Correção:**
- `gerador.py`: novos parâmetros de `gerar_txt_planos`:
  `estrategia: str = None` (valor aplicado na seção `[ESTRATEGIA]` do TXT;
  `None`/omitido mantém o default `"Aula expositiva e prática."`) e
  `aula_min`/`aula_max: int = None` (limita o intervalo de `seq_num`/`AULA_NUM`
  gerado; `None` ou `0` = sem filtro). O filtro é aplicado logo após a checagem
  de `max_hours_disc`, **depois** de avançar os contadores (`next_aula_num`),
  então a numeração das aulas seguintes não muda e o modo `prontas`/existente
  continua sendo respeitado (não sobrescreve sem `force_overwrite`).
- `planejamento_registro_streamlit.py`: helper
  `_estrategias_disponiveis()`/`_salvar_estrategias()` persistindo a lista na
  chave `estrategias_disponiveis` de `planejamento_config` (JSON; default
  `["Aula expositiva", "Aula baseada em projetos", "Aula de atividades em
  laboratório"]`). Na seção "Gerar planos (grade/calendário)": `selectbox` de
  estratégia, checkbox "Limitar intervalo de aulas" com inputs "De/Até (aula nº)"
  e `expander` "Gerenciar lista de tipos de estratégia (uma por linha)". Os
  valores escolhidos são repassados ao `_gerar_txt_planos`.

**Verificação:** teste end-to-end (turma 309197, disc 1, numeração atual 30→31):
- sem estratégia → `[ESTRATEGIA] = Aula expositiva e prática.` (default preservado);
- `"Aula baseada em projetos"`, `"Aula de atividades em laboratório"`,
  `"Aula expositiva"` → aplicadas corretamente em todos os TXT gerados;
- `aula_min=32` → seq 31 NÃO gerada; `aula_min=29, aula_max=33` → apenas 31 e 33.
- Cleanup do teste confirmou que nada foi deixado no banco (1/6/24 pendentes
  originais) nem na pasta `aulas/padrao`.

**Arquivos:** `apps/planejamento_registro/core/gerador.py`,
`apps/planejamento_registro/planejamento_registro_streamlit.py`

**Validar:** Planejamento e Registro → "Gerar planos": escolher uma estratégia,
marcar "Limitar intervalo de aulas" (ex.: 30–33) e gerar; os TXT devem trazer
`[ESTRATEGIA]` com a opção escolhida e `AULA_NUM` dentro do intervalo. O
expander "Gerenciar lista de tipos de estratégia" salva a lista em
`planejamento_config` (persiste entre sessões).

---

## IS-020 — Numeração de planos pulava os pares (grade duplicada) + "Sobrescrever" agora limpa `planejamento` 🟢

**Sintoma (relatado):** "Não gerou planos do intervalo de 22 a 32"; IA da Turma A
tem 28 aulas canônicas e as pendentes saíram numeradas 29, 31, 33, 35, 37, 39 —
nunca pares; não era possível gerar 29–32 em sequência.

**Causa raiz:** a tabela `weekly_schedule` contém cada slot **duplicado**
("I.A.", "P.C. II"/"P.C.II", "Disc.Tec.", "Ment.Tec.II" — 22 linhas = 11 slots).
O gerador processava as duas linhas: a 1ª gera o plano (seq 29) e a 2ª **avançava
o contador de novo** antes de ser pulada pelo "arquivo já existe" → o `seq`/`AULA_NUM`
aumentava +2 por semana. Além disso, `force_overwrite` não regenerava slots já
existentes na tabela `planejamento` (pulados em `planejamento_set`) e não removia
linhas antigas com numeração divergente.

**Correção:**
- `gerador.py`: **deduplicação dos slots** da grade por `(class_name, day_of_week,
  time_slot)` no carregamento — cada slot gera UMA aula → numeração consecutiva.
- `gerador.py`: em modo `force_overwrite` (check "Sobrescrever existentes"):
  - o piso de contagem **não soma mais os pendentes** existentes (a numeração parte
    do histórico e é renumerada em ordem natural dentro da rodada);
  - o skip de `planejamento_set` é **ignorado** (slots já planejados são regenerados);
  - no save no banco, linhas antigas do mesmo slot com `numero_aula` divergente são
    **deletadas** antes do upsert (sem resíduos duplicados).

**Verificação:** force-regen com intervalo 29–34 na IA → 6 arquivos `AULA_NUM`
29,30,31,32,33,34 consecutivos e tabela `planejamento` atualizada (09-14 sai de 31
para 30, linha antiga 31 removida); depois do intervalo, continua 35,36,…40 nas
segundas livres. Pendentes IA existentes foram re-numerados no banco (29→34) em
ordem de data (aulas 29–32 atendem ao pedido). Estado do banco restaurado após os
testes (1 + 6 + 24 pendentes originais).

**Arquivos:** `apps/planejamento_registro/core/gerador.py`

**Validar:** Planejamento e Registro → Turma A → IA → "Gerar planos" marcando
"Sobrescrever existentes" com intervalo 29–32: os TXT/lista devem vir 29, 30, 31,
32 consecutivos e sem duplicar linhas em `planejamento`.

---

## IS-021 — Frequência diária não persistia no `escola_ativa.db` + leitura sem disciplina 🟢

**Sintoma:** em 25/09/2026, planos gerados (ex.: `plano_309197_11_2026-09-14_1030.txt`)
traziam a chamada `[FREQUENCIA]` sem a frequência real — só `Presente` e os alunos
da lista negra global (`data/excecoes_alunos.json`). O usuário registra a chamada
todo dia no plugin Frequência e esperava que ela persistisse nas **3 fontes**:
Supabase + `escola_ativa.db` + JSON.

**Causa raiz (2 frentes):**
1. **Persistência:** `data/repo/plugins/student_attendance.py` (plugin ativo do
   portal) gravava apenas o **JSON** (`turma → disciplina → data`) e o **Supabase**;
   a tabela `attendance` do **`escola_ativa.db` nunca era escrita** pelo plugin.
   Como a tabela local só era populada por restore/sync pontual, ela estava
   parada em 26/05/2026 com `subject_id` **NULL** em todas as 1431 linhas — sem
   nunca chegar as chamadas de junho em diante.
2. **Leitura:** `load_attendance_from_db` era "disciplina agnóstica" (filtrava por
   data + turma, ignorava `subject_id`), então a frequência de um dia caía em
   qualquer disciplina daquele dia.

**Correção:**
- `data/repo/plugins/student_attendance.py`: novo helper
  `_write_local_attendance(db_records)` grava a chamada também na tabela
  `attendance` do `escola_ativa.db`, **com `subject_id` preenchido**. Upsert
  **manual** por `(student_name, class_name, subject_id, date)` — a tabela local
  (restaurada do Supabase) **não tem UNIQUE**, então `ON CONFLICT` falharia. O
  botão "Salvar Chamada do Dia" agora redunda nas **3 fontes**: JSON + banco
  local + Supabase (o Supabase continua condicional a `db.supabase`).
- `apps/planejamento_registro/core/banco.py`: resolução da frequência estruturada
  como **DATA → TURMA → DISCIPLINA**:
  - `load_attendance_from_db(turma_id, data_iso, disc_id=None)`: filtra pela
    **data exata**, casa a turma por nome normalizado e separa as linhas por
    `subject_id` — as **exatas da disciplina** têm prioridade; linhas legadas
    **sem** `subject_id` servem de fallback; linhas de **outra** disciplina são
    ignoradas.
  - `load_attendance_map_for` passa a aceitar também o formato **data-first** no
    JSON `{data: {turma: {disciplina: {ra: status}}}}`, além do plano legado
    `{turma: {data: {ra}}}` e do canônico `{turma: {disciplina: {data: {ra}}}}`.

**Observação:** `apps/api/*` é apenas leitura/referência e **não** foi alterado
(conforme orientação). A tabela local `attendance` tem schema legado (id TEXT,
sem UNIQUE) — o upsert manual do plugin casa com esse schema.

**Validação executada:** escrita via `_write_local_attendance` → `load_attendance_map_for`,
retornando `{ANDRE…: Falta, BRUNA…: Presente}` somente para a disciplina 11 da
Turma A na data; outra disciplina na mesma data e a Turma B retornam **vazio**;
upsert reexecutado atualizou `is_present` sem duplicar. Formato data-first do JSON
validado em `data/repo/plugins/student_attendance_corrigido.json` temporário
(removido após o teste) para 309197/11 e 314114/11.

**Arquivos:** `data/repo/plugins/student_attendance.py`,
`apps/planejamento_registro/core/banco.py`

**Validar:** (a) no plugin Frequência, salvar a chamada de uma data → conferir
linhas novas com `subject_id` na tabela `attendance` de `data/escola_ativa.db`;
(b) `load_attendance_map_for("309197", "11", "<data>")` retorna a chamada daquele
(data, turma, disciplina); (c) gerar plano e conferir que `[FREQUENCIA]` reflete a
chamada real daquele dia/disciplina.

---

## IS-022 — Plugins Notas/Frequência: `escola_ativa` como 1ª persistência, Supabase como redundância ⚪

**Pedido (agenda):** "Sempre que vou colocar uma nota, fazer uma frequência fica
lento esperando conexão." Registrar **primeiro no `escola_ativa.db`** (rápido,
local) e usar o **Supabase como redundância** com um **tempo razoável de
redundância**, para não travar o trabalho do professor na chamada/nota.

**Situação atual:**
- `data/repo/plugins/student_attendance.py` (Diário de Frequência): após o
  IS-021 grava JSON + `escola_ativa.db` na hora, mas faz o **upsert no Supabase
  de forma síncrona** no próprio callback do botão — a latência/conexão do cloud
  bloqueia a interface até terminar (ou estourar o timeout).
- `data/repo/plugins/student_scores.py` / `daily_activities.py` (Notas e
  Atividades): gravação/leitura de pontos qualitativos passa pela nuvem na carga
  e no save (ex.: `db.supabase` / `get_student_score`), mesmo cenário de espera.

**Proposta (quando implementar):**
1. **Persistência primária local:** escrever instantâneo em `escola_ativa.db`
   (+ JSON de origem), sem depender de rede.
2. **Supabase = redundância em fila:** enfileirar o lote pendente localmente
   (ex.: tabela/arquivo `pendentes_sync`), enviar ao cloud em **lote com
   debounce** (ex.: a cada N minutos ou quando o app voltar ao foco), sem
   bloquear o botão "Salvar" (thread de fundo / timer).
3. Aplicar o mesmo padrão em Frequência, Notas e Atividades.
4. **Bônus (IS-003):** batching reduz o número de round-trips e ajuda a conter o
   egress.

**Arquivos (candidatos):** `data/repo/plugins/student_attendance.py`,
`data/repo/plugins/student_scores.py`, `data/repo/plugins/daily_activities.py`,
e um novo utilitário de fila de sincronização.

**Validar (quando implementar):** salvar chamada/nota com o Supabase
indisponível → operação conclui na hora; com nuvem disponível, o sync chega ao
Supabase no intervalo configurado.

---

## IS-023 — Plugin Atividades: Lançamento de Seminário como Avaliação 🟡

**Pedido:** no plugin de Atividades, lançar um **seminário** como avaliação — o
professor seleciona um **intervalo de aulas**, dá o **nome do seminário** e obtém
a **lista de aulas a pesquisar**; a avaliação deve aparecer na UI de professor e
alunos (mesmo mecanismo do admin de Avaliações).

**Implementação (IS-021/IS-022 não interferem):**
- Nova seção "🎤 Lançamento de Seminário (Avaliação)" em
  `data/repo/plugins/daily_activities.py`, logo após o carregamento das aulas da
  disciplina (turma/disciplina vêm da sidebar do plugin).
- `st.select_slider(range=True)` escolhe o intervalo entre as aulas numeradas
  (regex `Aula\s*(\d+)`); a "lista de aulas a pesquisar" é exibida em dataframe
  sem repetir o prefixo "Aula N" (helper `_lesson_display`).
- **Integrantes do grupo:** multiselect com os alunos da turma
  (`db.get_students_by_class(class_id)`, já cacheado) — obrigatório ao menos 1;
  a lista de integrantes é embutida na mesma questão subjetiva criada, ficando
  visível para professor e alunos ao abrir a avaliação.
- Lança via `db.create_assessment(subject_id, "Seminário", f"{nome} · Aulas {min}–{max}")`
  (tabela `assessments` do Supabase, reutilizada pelo admin/front) e anexa **1
  questão subjetiva** com a lista de pesquisa (1 único insert = menos round-trips
  que uma questão por aula). Guarda contra duplicidade por título e contra
  resposta vazia do Supabase.
- Visibilidade confirmada sem mudanças no front: professor vê em
  `views/avaliacoes.py` (filtro "Trimestre=Todos" inclui qualquer tipo) e aluno
  na mesma tela — apenas MN1/MN2/MN3 têm trava de bloqueio; "Seminário" cai no
  fluxo normal com botão "Iniciar Tentativa".

**Pendências:**
- (decisão) Correção da nota do seminário: hoje o professor corrige via UI de
  correção da avaliação (resposta subjetiva); não há fluxo específico de
  "nota de apresentação".

**Arquivos:** `data/repo/plugins/daily_activities.py`, `docs/ISSUES_LOCAIS.md`

**Validar:** no plugin Atividades (turma/disciplina), selecionar intervalo,
nomear e lançar → conferir em `views/avaliacoes.py` (professor e aluno logado)
que aparece "Seminário - {nome} · Aulas X–Y" e que, ao abrir, lista as aulas a
pesquisar.

---

## IS-024 — Admin/Gerenciar Avaliações: exclusão de avaliação 🟢

**Pedido:** "Em admin/Gerenciar Avaliações não tem a opção de excluir a
avaliação. Quero excluir e recriar os seminários."

**Implementação:**
- `services/database.py`: nova função `delete_assessment(assessment_id)` que
  remove na ordem **respostas → submissões → questões → avaliação** (apenas
  `assessment_questions` tem `ON DELETE CASCADE` no schema; `student_assessments`
  e `student_assessment_answers` não, então a exclusão manual evita violação de
  FK no Supabase).
- `views/admin.py` (aba "Avaliações"): botão "🗑️ Excluir ..." abaixo do seletor
  de avaliação, com **confirmação em duas etapas** via `session_state`
  (`confirm_del_av_{id}`) para evitar exclusão acidental; ao confirmar chama
  `db.delete_assessment` e faz `st.rerun()`.

**Arquivos:** `services/database.py`, `views/admin.py`

**Validar:** em Admin → Avaliações, selecionar a turma/disciplina, escolher uma
avaliação existente, clicar em Excluir, confirmar → a avaliação some da lista
(de Admin e da tela do aluno) e um seminário com o mesmo título pode ser
recriado pelo plugin sem "já existe".

---

## IS-025 — Plugin Atividades: últimas 8 aulas fora do teto de 6 pts + aulas de apresentação 🟢

**Pedido (após IS-023):** ao lançar seminários, o limite de 6 pontos por bloco
impede pontuar as apresentações. Regra definida pelo usuário: **deixar fora do
teto as últimas 8 aulas** da disciplina — 40h → **33-40**; 80h → **73-80**.

**Implementação (evita regra fixa "33-40", que quebraria em 80h):**
- `data/repo/plugins/daily_activities.py`:
  - `APRESENTACAO_QTD = 8`; `_bloco_regular(aula_num)` divide a disciplina em
    blocos de 20 (1-20, 21-40, 41-60, ...) — generalizado para 80h;
  - `_bloco_info(aula_num, ultima_aula)` retorna o bloco "Apresentação
    (X-última)" com `capped=False` para as **8 aulas finais**, tomando
    `ultima_aula` = maior número de aula da disciplina (`get_lessons_for_subject`);
  - UI dinâmica: mensagem "Apresentação (33-40)/(73-80)... sem limite de 6
    pontos", coluna Pontuar com passo 0.5 e teto 10, "Disponível" 999, e filtro
    de bloco no relatório montado a partir dos blocos reais;
  - guarda: disciplinas com menos de 8 aulas não têm bloco de apresentação.
- **Aulas criadas no Supabase** (`lessons`, subject 8 FUNDAMENTOS DE UI/UX
  ORA IHC, 40h — só ia até a Aula 32): "Aula 33..40 Apresentação de Seminários
  — Grupo 1..8" (ids 634-641) com título, descrição, objetivo, roteiro da
  apresentação, critérios de avaliação e recursos (sem Base64).

**Arquivos:** `data/repo/plugins/daily_activities.py`; dados em `lessons`
(Supabase, subject 8).

**Validar (40h):** plugin Atividades → Fundamentos de UI/UX → aula 33-40 mostra
"Apresentação (33-40)... sem limite de 6 pontos" e aceita nota até 10; aula 25
segue em Bloco 21-40 com teto 6. (80h: aula 73-80 mostra Apresentação 73-80.)

---

## IS-026 — Prova impressa: separar integrantes e lista de aulas do seminário 🟢

**Pedido:** "Ao salvar a prova falta formatar melhor o layout, pois a lista de
alunos e a lista das aulas estão juntas". A questão subjetiva do seminário
(1 único texto com integrantes + aulas) era impressa em uma única linha porque
`markdown_to_html` descarta `\n` e itens `- `.

**Implementação:** em `views/avaliacoes.py`, nova `text_block_to_html(text)` —
mantém `markdown_to_html` (bold/italic/code + escape) e adiciona:
- quebras de linha como `<br>` e linhas em branco como espaçador de 8px;
- itens iniciados com `- ` ou `• ` agrupados em `<ul><li>` (recuo 22px).

Aplicada no texto das questões nas 3 telas de prova: Prova corrigida
(`generate_printable_view`), Prova em branco (`generate_blank_printable_view`)
e Impressão/Salvar da avaliação (`generate_assessment_print_html`). Options,
código web e respostas continuam com `markdown_to_html`.

**Arquivos:** `views/avaliacoes.py`

**Validar:** admin/avaliações de um Seminário → "Imprimir Prova" ou "Salvar
Prova (HTML)" → integrantes e lista de aulas aparecem em listas separadas.

---

## IS-027 — Visualizar/Imprimir Prova cortada à direita 🟢

**Pedido:** "No campo Imprimir Prova/Visualizar Prova a prova aparece na metade
do layout cortando na metade do lado direito". O container de 800px (`max-width:
800px`, sem `width`/`box-sizing`) estourava em telas estreitas e a faixa
"Aluno(a)/Nota" (linhas de `_` longas em flex `space-between`) transbordava o
bloco, cortando o lado direito.

**Implementação:** em `views/avaliacoes.py`, nos 3 templates
(`generate_printable_view`, `generate_blank_printable_view` e
`generate_assessment_print_html`):
- container centralizado com `max-width: min(800px, 100%); box-sizing:
  border-box; overflow-wrap: break-word;` — nunca ultrapassa a largura da tela;
- faixas `Aluno(a)/Nota Final` com `flex-wrap: wrap;` (e `gap` no template de
  impressão da avaliação) para quebrar linha quando não houver espaço.

**Arquivos:** `views/avaliacoes.py`

**Validar:** Visualizar Prova / Imprimir Prova de uma avaliação (ex. Seminário)
em janela estreita e larga — a prova fica centralizada e sem corte à direita.

---

## IS-028 — Prova exibida dentro de coluna estreita, cortada à direita 🟢

**Causa raiz (a do IS-027 não era o overflow):** o `components.html(prova)` era
chamado **dentro** de `with st.columns(...)`, então o iframe ficava com apenas
1/3 (ou 1/2) da largura da tela e a prova de 800px era cortada no lado direito
("prova no lado esquerdo, layout cortado ao meio"). O `st.stop()` logo em
seguida congelava a página.

**Implementação:** o `components.html` foi movido para **fora** da coluna (largura
total), usando uma flag setada pelo botão dentro da coluna:
- `views/avaliacoes.py`: botão "Imprimir Prova" (aba Avaliações do admin, estava
  na 1ª de 3 colunas); "Visualizar Prova Corrigida" e "Visualizar Prova"
  (aluno, estavam na 1ª de 2 colunas).
- `views/admin.py`: botão "🖨️ PDF para Impressão" (estava na 2ª de 2 colunas).

Os botões continuam nas colunas; o iframe da prova é renderizado em largura
total abaixo delas, seguido de `st.stop()`.

**Arquivos:** `views/avaliacoes.py`, `views/admin.py`

**Validar:** aba Avaliações (admin) / área do aluno → "Imprimir Prova" e
"Visualizar Prova" → a prova ocupa a largura total e não é mais cortada.

---

## IS-029 — Planos individual: feedback explícito da origem da frequência 🟢

**Sintoma:** no Gerar Individual, a chamada aparentava conter apenas as faltas
da lista negra, sem deixar claro se uma frequência salva havia sido encontrada.

**Causa:** o gerador consultava Supabase e JSON, mas a consulta SQLite pedia a
coluna `subject_name`, inexistente na tabela local `attendance`; a exceção era
silenciada e nenhum registro local era carregado. A lista negra também era lida
de um caminho diferente do usado pelo Diário de Frequência (`data/excecoes_alunos.json`).
Além disso, o JSON podia estar no formato `data → turma → disciplina`, enquanto
a leitura não reconhecia todos os formatos legados e havia diferença potencial
de acentos/caixa nos nomes da turma e dos alunos.

**Correção:** `buscar_alunos_presenca` lê o schema real da tabela local
(`student_name`, `is_present`, `class_name`, `date`, `subject_id`), converte os
valores SQLite `0/1`, e reconhece os dois formatos JSON, respeitando turma,
disciplina e data. A turma e os nomes são comparados sem depender de acentos ou
caixa; registros legados sem `subject_id` só são usados quando não há registros
da disciplina exata. Sem chamada salva para a data selecionada, a interface
mantém apenas os status aceitos pelo portal (`Presente` e `Falta`): Presente é o
padrão, enquanto alunos da lista negra iniciam como Falta. O aviso informa que
nenhuma chamada foi encontrada. A lista negra passa a ser carregada de
`data/excecoes_alunos.json` e aplicada como falta inicial somente quando não há
chamada salva para o aluno. O painel mostra feedback de frequência encontrada
com o nome da tabela/arquivo; sem registros, informa as fontes consultadas e
esclarece que a lista começa como Presente, podendo faltas vir das exceções. O
feedback mostra também a quantidade de registros encontrados e é renderizado no
painel principal do Gerar Individual, acima das abas internas, sem exigir que o
usuário abra "Lista de Presença". O calendário em `master_config` (`key =
feriados.json`) é consultado com cache de 1 hora; para datas cadastradas, o
painel também exibe a descrição do feriado.

**Arquivos:** `data/repo/plugins/gerar_planos_txt.py`, `docs/ISSUES_LOCAIS.md`

**Validar:** em Planos → Operações → Gerar Individual → Lista de Presença,
selecionar uma data com chamada salva e conferir o feedback com a fonte. Em data
sem chamada, conferir o aviso com os caminhos consultados. Confirmar que chamada
de outra disciplina não altera os status.

---

## IS-030 — Gerar planos: lista de presença com 15 linhas 🟢

**Pedido:** aumentar a quantidade de alunos visíveis na tabela de presença
durante a geração individual do plano.

**Correção:** altura do editor da lista de presença ampliada para 680 px,
permitindo visualizar aproximadamente 15 linhas sem rolagem interna.

**Arquivos:** `data/repo/plugins/gerar_planos_txt.py`, `docs/ISSUES_LOCAIS.md`

**Validar:** Gerar Individual → Lista de Presença → conferir cerca de 15 alunos
visíveis simultaneamente.

---

## IS-031 — Frequência: incluir alunos inativos da lista negra 🟢

**Sintoma:** Luara e Guilherme constavam na lista negra, mas não apareciam na
frequência do plano.

**Causa:** para recuperar alunos inativos da lista negra, o gerador acrescentava
à turma selecionada todos os usuários globais que estivessem na lista. Isso
misturava alunos matriculados em outras turmas. Os cadastros de Luara e
Guilherme existem em `app_users`, com `is_active = false` e `is_portal = true`.

**Correção:** `app_users.is_portal` controla se o usuário ainda pertence ao
portal; `is_active` não é usado como sinal de transferência. A frequência agora
parte exclusivamente das matrículas da turma selecionada; a lista negra apenas
mantém nessa turma alunos `is_active = false` e define `Falta` quando não há
presença salva. Alunos de outras turmas não são adicionados globalmente e
transferidos marcados com `is_portal = false` são excluídos.

**Arquivos:** `services/database.py`, `data/repo/plugins/gerar_planos_txt.py`,
`data/repo/plugins/student_attendance.py`, `docs/ISSUES_LOCAIS.md`

**Validar:** em uma turma com alunos de outras turmas na lista negra, confirmar
que só aparecem alunos matriculados na turma selecionada. Luara e Guilherme,
matriculados na 2ª Série Turma I-A com `is_portal = true`, devem aparecer nela
com `Falta` se não houver frequência salva. Marcar um transferido com
`is_portal = false` e confirmar que não aparece.

---

## IS-032 — Planos: não sugerir datas cadastradas como feriado 🟢

**Sintoma:** a cadência semanal sugeria 07/09/2026 para Inteligência Artificial,
apesar da data estar cadastrada como feriado.

**Correção:** o cálculo da próxima aula agora pula datas presentes em
`master_config` → `feriados.json`. Para aulas semanais avança uma semana; para
disciplinas modulares busca o próximo dia previsto na grade que não seja feriado.
Feriados pulados são mostrados na tela. A sessão também troca uma sugestão
automática antiga que tenha ficado selecionada em feriado.

**Arquivos:** `data/repo/plugins/gerar_planos_txt.py`, `docs/ISSUES_LOCAIS.md`

**Validar:** com última aula em 31/08/2026 e cadência semanal, a sugestão pula
07/09/2026 (Independência do Brasil) e avança para 14/09/2026.

---

## IS-033 — Planos: diagnóstico contava linhas duplicadas de `historico_aulas` 🟢

**Sintoma:** IA da 2ª Série Turma I-A mostrava 38 aulas no diagnóstico, embora
o portal tenha 28.

**Diagnóstico:** para `turma_id = 309197` e `disciplina_id = 11`, a consulta
encontrou 38 linhas em `historico_aulas`, mas apenas 28 datas distintas. As
linhas extras repetiam datas usando rótulos/horários antigos.

**Correção:** `buscar_historico_aulas` mantém uma linha por data, prefere status
confirmado/registrado e ignora aulas excluídas/canceladas. Métricas, numeração e
data mais recente passam a usar as aulas distintas.

**Arquivos:** `data/repo/plugins/gerar_planos_txt.py`, `docs/ISSUES_LOCAIS.md`

**Validar:** selecionar IA na Turma I-A (ID 309197); o diagnóstico deve indicar
28 aulas registradas e a próxima aula como 29.

---

## IS-034 — Planos: lista negra misturava alunos de turmas diferentes 🟢

**Sintoma:** a lista de presença de uma turma mostrava alunos de outras turmas.

**Causa:** além da matrícula da turma selecionada, o gerador acrescentava
alunos da lista negra encontrados na consulta global de usuários.

**Correção:** a frequência usa exclusivamente `get_students_by_class(class_id)`.
A lista negra mantém como `Falta` alunos inativos que já pertencem àquela
matrícula, mas não importa usuários de outras turmas. `is_portal = false`
continua excluindo transferidos. A chave de estado da tabela acompanha turma,
disciplina, data e composição dos alunos, impedindo que o `data_editor` preserve
uma lista antiga após atualização da matrícula.

**Arquivos:** `data/repo/plugins/gerar_planos_txt.py`, `docs/ISSUES_LOCAIS.md`

**Validar:** selecionar uma turma e confirmar que a frequência contém apenas
seus matriculados, mesmo quando a lista negra contém alunos de outras turmas.
Na Turma I-A (ID 1), Luara e Guilherme devem aparecer com `Falta` se não houver
frequência salva; alternar turma/data deve atualizar as linhas da tabela.

---

## IS-035 — Planos: associar abreviações de disciplina ao rótulo da grade 🟢

**Sintoma:** em Planos, a disciplina `MENTORIAS TEC II` selecionada exibia um
aviso de divergência quando a grade mostrava `Ment.Tec.II` no horário de terça
às 13:30.

**Causa:** a verificação comparava o rótulo abreviado da grade diretamente com
o nome completo cadastrado da disciplina.

**Correção:** a comparação normaliza os dois nomes e resolve aliases conhecidos
da grade, incluindo `Ment.Tec.II` → `MENTORIAS TEC II`, `P.C.II` →
`PENSAMENTO COMPUTACIONAL II` e `I.A.` → `INTELIGÊNCIA ARTIFICIAL`. Divergências
reais continuam exibindo aviso.

**Arquivos:** `data/repo/plugins/gerar_planos_txt.py`, `docs/ISSUES_LOCAIS.md`

**Validar:** selecionar `MENTORIAS TEC II` na Turma I-A em uma terça às 13:30;
deve aparecer o feedback de disciplina associada à grade, sem aviso de
divergência.

---

## IS-036 — Repo syava-apps aninhado em `apps/` + Down SeducTec 🟢

**Pedido:** separar os apps Streamlit em um repositório GitHub próprio
(<https://github.com/hiseg10/syava-apps>) com README, ISSUES, AGENTS e
bootloader próprios, mantendo o `run.bat` do SysAva lançando-os por links;
e criar o app de download do portal SeducTec.

**Solução:**
- **Repo aninhado:** `git init` em `apps/` com remote `hiseg10/syava-apps`
  (histórias unificadas via merge `--allow-unrelated-histories -X ours`,
  mantendo o LICENSE MIT). O SysAva continua ignorando `apps/`
  (`.gitignore:34`) — os dois repositórios não conflitam.
- **Escopo versionado:** `duplicate_checker`, `supabase_monitor`,
  `planejamento_registro`, `analise_notas`, `down_seductec` + docs
  (`README.md`, `ISSUES.md` com IDs `AP-NNN`, `AGENTS.md`,
  `requirements.txt`, `run_apps.bat`, `.gitignore`).
  Excluído: `api/`, `apis_gemini_key/`, `data/`, backups `.db`, `.csv`,
  `html/`, logs e `__pycache__/`. Outputs do `analise_notas.ipynb` limpos
  (8 outputs com nomes de alunos removidos); scan de chaves limpo.
- **Bootloader `apps/run_apps.bat`:** detecta/cria o venv `.sysenv` do SysAva
  e oferece menu com portas fixas (8502/8503/8504/8510).
- **Novo app `apps/down_seductec/`** (porta **8504**): núcleo portado do
  script legado `Aulas_selenium/tools/utils/seductec_scraper.py` — login
  manual detectado por polling (sem `input()`), extração de tiles
  `S(\d+)-AULA\s*(\d+)`, download de PDFs resolvendo redirects do Moodle,
  coleta de links YouTube e `links_aulas.md` reescrito por execução
  (idempotente). Destino `data/repo/<turma>/<disciplina>/S0X/seductec/`,
  compatível com o `generate_lessons_gemini`.
- **`run.bat`:** menu ampliado para **1-8** — `[5] Down SeducTec`,
  `[6] README dos Apps`, `[7] Repo no GitHub`, `[8] Sair`.

**Arquivos:** `apps/down_seductec/*`, `apps/{README,ISSUES,AGENTS}.md`,
`apps/.gitignore`, `apps/requirements.txt`, `apps/run_apps.bat`, `run.bat`,
`apps/analise_notas/analise_notas.ipynb`, `docs/ISSUES_LOCAIS.md`.

**Validar:** `py_compile` dos arquivos novos; `streamlit run
apps/down_seductec/down_seductec_streamlit.py --server.port 8504` renderiza
(sidebar com turma, log ao vivo, botão Conectar); `git -C apps status` sem
dados sensíveis; `push` em `hiseg10/syava-apps` OK. Downloads reais dependem
de login manual no portal (validação manual).

---

## IS-037 — Planejamento: feriados bloqueiam geração/registro; configs migram para `master_config`; frequência ao vivo 🟢

**Sintoma:** o app `planejamento_registro` gerava/registrava aulas em feriados
(07/09, 12/10, 01/05...), sem nenhum sinal na UI; as configurações viviam na
tabela local `planejamento_config` (espelho sem sync, ausente do Supabase); e
a frequência do `.txt` caía em `Presente` silencioso quando não havia registro.

**Correções:**
1. **Feriados (AP-005):** `core/gerador.py` pula datas de
   `master_config` → `feriados.json` no loop de geração (log em
   `slots_pulados`); UI ganha helpers `_feriados_config()`/`feriado_na_data()`,
   bloqueio no 🤖 Registrar (multiselect e "Registrar TODOS" filtrados),
   badges `⚠️ Feriado/recesso` em 📄 Planos e 👁️ Plano Individual, coluna
   `Feriado` + aviso na fila do Painel, e seção 📅 de verificação na aba
   ⚙️ Config (tabela por categoria + verificador de data).
2. **Migração (AP-006):** chaves `data_corte_planejamento`, `ferias` e
   `estrategias_disponiveis` migraram para `master_config` (JSON);
   `database_model.set_config()` novo (UPDATE→INSERT, schemas `key/value` e
   legado); consumidores redirecionados (`banco.get/set_config`,
   `gerador.py`, `html_routes`, `bot_raspagem`, UI "Outros parâmetros");
   `DROP TABLE planejamento_config` após verificação (backup
   `data/escola_ativa_backup_antes_migracao_20260929_171123.db`).
3. **Frequência (AP-007):** `load_attendance_map_for` retorna
   `(mapa, fonte, diagnostico)` com `{encontrou, quantidade, fontes,
   outra_disciplina}`; fallback para a disciplina com mais registros da mesma
   turma/data (sinalizado); exceções manuais em `attendance_exceptions.json`
   (chave `{turma}|{data}|{disc}`, ações `ignorar` / `usar_disciplina`);
   aba 👁️ com banners ✅/⚠️ + tabela de frequência ao vivo + comparação
   `.txt` × banco; gerador reporta `freq_outra_disciplina`.
4. **Limpeza:** 3 linhas de `planejamento` e 4 `.txt` em feriado movidos para
   `data/backup_clean_feriados_20260929_172617/` (`historico_aulas` intocada).

**Arquivos:** `apps/planejamento_registro/{planejamento_registro_streamlit.py,
core/{banco,gerador,datas}.py}`, `apps/api/tools/{database_model,bot_raspagem}.py`,
`apps/api/html_routes.py`, `apps/ISSUES.md`, `docs/{ISSUES_LOCAIS.md,
AUDITORIA_BANCO.md,NOVO_BANCO_SCHEMA.sql}`.

**Validar:** QA Playwright no app 8510 (0 erros de console): badges/bloqueio,
aba Config com `Atual: 2026-04-01` e verificador ✅, banners da 👁️ (exata
22 alunos, feriado sem frequência, outra disciplina 22); geração de teste com
rollback pulou `2026-09-07` e `2026-10-12` (`RESULT: PASS`); fila do Painel
sem planos em feriado.

---

## IS-038 — Planejamento: aba Consolidadas + `disciplina_ids` no calendário 🟢

**Pedido:** visão anual (carga × fluxo por turma/disciplina) com filtro, e
expor o **fluxo letivo anual** para situar cada disciplina no seu escopo — o
fluxo por turma sozinho ficava "relativo".

**Correções:**
1. **Aba 📈 Consolidadas (AP-008):** `consolidadas_data()` + KPIs + gráficos
   (fluxo empilhado; carga × registradas por turma) + tabela Detalhamento,
   com seletor "Todas as turmas". Definições: registradas = `historico_aulas`
   (turma_id + nome canônico, status ≠ `Aula Exclu%`); prontas/pendentes =
   `.txt` em `aulas/prontas|pendentes`; faltantes = `carga − reg − prontas −
   pendentes`; carga = `subjects.max_hours`.
   **Carga corrigida para 880h** (11 × 40h × 2 turmas, base
   `data/Turmas/Escola.txt`): `_chave_disc()` agrupa aliases pelo nome
   canônico (remove `(…)`, `2026A/B`, acento, caixa) — POO `4+30` e WEB
   FRONT-END `6+31+33+34` viram 1 linha de 40h; **Caderno de Atividades**
   (subject 35) fora da carga; base = todas as 22 linhas (sem filtro
   `is_active`).
2. **`disciplina_ids` no calendário:** cada entrada de
   `restricoes_planejamento` ganhou a lista de `subjects.id` correspondentes
   (arquivo `data/calendario_letivo.json` **e** espelho
   `master_config['calendario_letivo.json']`, mantidos idênticos; typo
   histórico `INTRODUCAOAECOSSISTEMADEVOPS` → id 9). Backup
   `data/escola_ativa_backup_calendario_20260929_200449.db`.
3. **Gantt na aba:** `load_janelas_disciplinas()` lê o calendário (mesma
   fonte do gerador: `master_config` → fallback do arquivo), indexa
   `disciplina_id → {inicio, fim}` e desenha a janela de cada disciplina no
   ano (Altair, cor = Anual/Mensal, régua = hoje, altura dinâmica
   `max(420, 26n+90)`) + coluna **Janela** na tabela.
4. **Sync `data/calendario_letivo.json` → `master_config`** (fecha a
   divergência das 10 janelas): investigação mostrou que a direção correta é
   **a inversa** da inicialmente imaginada. O `master_config` foi escrito por
   um import de **14/06/2026** (`updated_at` em formato ISO, distinto do
   `datetime('now')` do `set_config`) e saiu **degradado**: `sabados_letivos`,
   `trimestres` e `ferias_e_recessos` ficaram `{}`. O arquivo é que tinha os
   dados vivos (18 sábados letivos, trimestres com `data_limite_iseduc`,
   `carga_horaria` por restrição, `disciplinas_config.mensais` 340B vs 124B).
   Consequência do bug: **`core/gerador.py:431` lia `sabados_letivos` do
   master e recebia `{}` → geração de sábados letivos quebrada**. Sincronizado
   com `database_model.set_config` (arquivo → master, `updated_at` renovado);
   cópia cega na direção contrária teria **destruído** os 18 sábados + 3
   trimestres. Backup do valor antigo do master:
   `data/backup_master_calendario_20260930_043908.json`. Datas resultantes
   (agora idênticas nas 2 fontes): anuais `19/02–17/12` = fim do 3º trimestre
   (antes `27/11` no master, sem respaldo). Evidência de decisão: o arquivo é
   superconjunto (`chaves só no master = ∅`) e interno consistente
   (`data_fim 17/12` = fim do 3º trimestre).

**Arquivos:** `apps/planejamento_registro/planejamento_registro_streamlit.py`
(`secao_consolidadas`, `consolidadas_data`, `load_janelas_disciplinas`,
`_SECOES`), `apps/ISSUES.md`, `docs/ISSUES_LOCAIS.md`, dados
`data/calendario_letivo.json` + `master_config` (não versionados).

**Validar:** abrir `http://localhost:8510` → 📈 Consolidadas → **22 disc /
880 carga / 378 registradas / 25 prontas+pendentes / 478 faltantes / 43%**;
filtro I-A → 11 / 440 / 204 / 2 / 235; Gantt com **22 barras**, régua em
hoje e rótulos sem truncar; coluna Janela na tabela; sem "Caderno"; ⚠️
esperado de `PROGRAMAÇÃO WEB FRONT-END (I-A)` (41 registros > 40 de carga).
Sync: `cmp_fontes.py` → 11/11 `OK` e `chaves só no arquivo/master = ∅`;
`get_config(...)['sabados_letivos']` → 18 entradas.

---

## IS-039 — Disciplina oculta no portal local (cache + `.env` em projeto antigo) 🟢

**Sintoma:** `PROGRAMAÇÃO PARA DISPOSITIVOS MÓVEIS` (subject 5) aparecia na
versão Cloud mas não no portal local.

**Causas (4, todas verificadas):**
1. **Cache obsoleto:** `data/cache/sysava_cache.db` tinha
   `subjects_for_class:1` (05:10) e `:2` (05:14 de 30/09) com
   `id 5 → is_active=False`, enquanto o Supabase vivo respondia `True` nas 2
   turmas. TTL de 6h (`local_cache.TTL_BASE`) mantinha a lista velha.
2. **Toggle sem invalidação:** `views/admin.py` gravava
   `class_subjects.is_active` direto no Supabase sem
   `local_cache.invalidate(f"subjects_for_class:{class_id}")` (só
   `link_subject_to_class` e `update_training_links` invalidavam).
3. **Fetch envenenava o cache:** `_fetch()` de `get_subjects_for_class`
   capturava a exceção de rede e devolvia `[]`, que era gravada como fresca
   por 6h (observado às 11:57 — `WinError 10060`, `row_count=0`).
4. **Dois projetos Supabase:** `.env` apontava o projeto antigo
   (`tsbx…`: disciplina inativa, 0 aulas) e `.streamlit/secrets.toml` o novo
   (`xfudd…`: ativa, 8 aulas). Portal local e Cloud usavam o novo; `apps/api`,
   plugins e seeds usavam `.env` (antigo).

**Correções:**
1. Invalidação do cache no toggle de visibilidade (`views/admin.py`).
2. `_fetch()` de `get_subjects_for_class`/`get_students_by_class` agora
   **propaga** a exceção: `get_or_fetch` cai no cache antigo em vez de gravar
   lista vazia (nenhuma lista vazia de erro é mais cacheada).
3. `get_students_by_class` deixou de usar `select("*")` (regra de egress do
   `AGENTS.md`) — passou a `username, name, ra, role, status, is_active,
   is_portal` com fallback para bancos sem as colunas novas; chave de cache
   `v2` → `v3` (descarta blobs antigos que continham hash de senha).
4. Bug extra: `create_user`/`delete_user`/`toggle_user_active`/`upsert_user`
   invalidavam a chave `"app_users"` mas a lista é cacheada como
   **`"app_users:v2"`** → invalidação era no-op; corrigido para a chave real.
5. `.env` alinhado ao projeto novo (`SUPABASE_URL`/`SUPABASE_KEY` copiados de
   `.streamlit/secrets.toml`; backup em
   `data/logs/env_backup_20260930_115615.env`). Demais chaves (Gemini/OpenAI/
   DeepSeek) mantidas.

**Arquivos:** `views/admin.py`, `services/database.py`, `.env` (não
versionado), `data/cache/sysava_cache.db` (chaves `subjects*` removidas).

**Validar:** `python -c "from services import database as db; print([(s['name'], s['is_active']) for s in db.get_subjects_for_class(1) if s['id']==5])"`
→ `[('PROGRAMAÇÃO PARA DISPOSITIVOS MÓVEIS', True)]`; portal → Home/Aulas
mostra a disciplina nas turmas I-A e I-B.

**⚠️ Pendência relacionada:** `data/escola_ativa.db` (365 aulas) ainda
espelha o projeto antigo (novo projeto: 409). **Não rodar
`audit_backup.sync_local_to_supabase()` (push)** antes de atualizar o SQLite
a partir do projeto novo, senão dados velhos sobrescrevem os novos.

---

## IS-040 — Lista negra fora do Cloud → mecanismo de inativos no banco 🟢

**Sintoma:** a lista negra de faltosos não funcionava na versão Cloud.

**Causa:** a lista era **apenas** `data/excecoes_alunos.json`, no
`.gitignore:26` — nunca vai ao GitHub, logo não existe no Streamlit Cloud.
O código dos plugins **é** versionado e rodava, mas degradava em silêncio
(`load_json` → `{}` em `student_attendance.py`; `try/except: pass` em
`gerar_planos_txt.py`) → todos iniciavam "Presente", sem nenhum aviso. Não
havia tabela Supabase, `st.secrets` nem Storage para esse dado (o arquivo não
tinha UI de edição: era mantido à mão).

**Semântica adotada (decisão do mantenedor):**
- `app_users.is_active = false` → aluno **fica** na chamada e **inicia como
  Falta** (também no bloco `[FREQUENCIA]` dos planos).
- `app_users.is_portal = false` → aluno é **excluído** da lista de chamada.
- Login **não** é bloqueado (`views/login.py` intocado).
- Banco = fonte de verdade (local e Cloud); o JSON local vira **espelho** para
  os robôs de `apps/`.

**Correções:**
1. **DDL (executado em 30/09):** `docs/ADD_USER_PROFILES_FREQUENCIA.sql`
   adiciona `user_profiles.frequencia_status` (`normal|falta|inativo`),
   `motivo` e `atualizado_em`. Sem o DDL o recurso também funciona: o status é
   derivado de `is_active`/`is_portal` (fallback explícito).
2. **`services/database.py`:** `get_frequency_flags()` (cache
   `app_users_flags:v1`, TTL_MEDIUM), `set_frequency_flag()` (único caminho de
   escrita: grava `app_users` + `user_profiles` e invalida
   `app_users:v2`/`app_users_flags:v1`/`students_by_class:*`) e
   `sync_blacklist_json_mirror()` (regrava o JSON preservando chaves extras
   como `ignored_names`; falha em silêncio no Cloud).
3. **Admin (`views/admin.py`):** seção "🚫 Frequência — status dos alunos"
   com `data_editor` (Normal/Falta/Inativo + motivo), resumo por status e
   gravação + regeneração do espelho.
4. **Migração (`scripts/migrar_excecoes_para_banco.py`, whitelist no
   `.gitignore`):** `--dry-run` mostrou [ALUNO] `[RA]` e [ALUNO]
   `[RA]` **ativos no banco mas na lista do JSON** → migrados para
   `falta`; [ALUNO] `[RA]` já `inativo`; ALUNO TESTE `[RA]`
   só no banco (mantido). Espelho regerado: **8 `blacklist`, 7
   `blacklist_names`, 1 `dropouts`**.
5. **Plugins:** `student_attendance.py` lê o banco primeiro e cai no JSON só
   se o aluno não estiver nas flags; conta e anuncia os excluídos
   (`is_portal=false`); `gerar_planos_txt.py`
   (`buscar_alunos_presenca`) passou a filtrar **somente** por `is_portal`
   (antes `is_active=false` fora da lista, salvo se estivesse no JSON) e o
   status inicial vem das flags do banco.

**Arquivos:** `services/database.py`, `views/admin.py`,
`data/repo/plugins/student_attendance.py`,
`data/repo/plugins/gerar_planos_txt.py`,
`scripts/migrar_excecoes_para_banco.py`, `docs/ADD_USER_PROFILES_FREQUENCIA.sql`,
`.gitignore`, `data/excecoes_alunos.json` (espelho, não versionado).

**Validar:** I-A → [ALUNO] fora da lista (22 → 20 no plano), Falta em
GUILHERME/LUARA/[ALUNO]; I-B → Falta em ISADORA/GUSTAVO/JANAYRA/[ALUNO];
`python scripts/migrar_excecoes_para_banco.py --dry-run` → sem alterações
pendentes; no Cloud (sem o JSON) a chamada e os planos repetem o mesmo
resultado; aluno com `is_active=false` ainda consegue logar.

**Concluído (30/09):** DDL executado no SQL Editor; migração reexecutada
→ `user_profiles` com **9 linhas** (8 `falta`, 1 `inativo`, todas com
`motivo='migracao do JSON'`); `get_frequency_flags()` lendo as colunas novas;
UI do Admin conferida pelo mantenedor.

---

## IS-041 — `historico_aulas` não refletia o portal: 189 órfãs com rótulo antigo de turma 🟢

**Sintoma:** a raspagem do portal iSeduc (`apps/api/tools/bot_raspagem.py`)
fechou com **Portal: 418 | Local: 601 | Órfãs no local: 189 | Faltantes: 0**
(e aviso `time data '13/07/2026' does not match format '%Y-%m-%d'`).

**Causa raiz:** **188 linhas** gravadas entre 28/05 e 15/06 com o **nome cru
da turma vindo do portal** (`EMTPDES-SIS-2ª SERIE - INTEGRAL-I-A/B`) em vez do
nome canônico de `classes.name` (`2ª SÉRIE - Turma I-A/B (Técnico DS)`) — com
`turma_id` correto, vindas de uma sincronização/restauração antiga e depois
replicadas para o Supabase. Como `save_history` usa `INSERT OR REPLACE`
(**nunca apaga**) e o relatório aplicava o `turma_map` só no lado do portal,
elas acumulavam como órfãs e o app principal (que filtra por `turma_id` em
`gerar_planos_txt.py`) as contava em dobro. Detalhes:
- **167** eram duplicata exata (`turma_id` + data + horário + disciplina) da
  linha canônica; **22** sem par (16 `Registrada`, 3 `Aula Excluída`, 2
  `Aguardando confirmação`, 1 `Aula confirmada`);
- **+1** linha canônica órfã (15/08, PCII) e **+1** variante de grafia de
  disciplina (`PROGRAMACAO WEB FRONT-END` sem Ç/Ã, status
  `Aguardando confirmação`) — escapava do relatório porque a comparação
  normaliza acentos e as duas linhas colapsavam na mesma chave;
- **15** linhas com status que o próprio `save_history` se recusa a gravar.

**Correções:**
1. **Backups:** `data/escola_ativa_backup_historico_orfas_20261001_164116.db`
   (SQLite) e `data/logs/historico_aulas_supabase_backup_20261001_164116.json`
   (399 linhas do Cloud).
2. **Limpeza local (`scripts/limpar_historico_orfas.py`, dry-run →
   `--aplicar`):** removeu **190 linhas** (189 órfãs do relatório + 1 status
   inválido) → **411 = 418 − 7 status excluídos do portal**.
3. **Cloud (`scripts/sync_historico_supabase.py`, dry-run → `--aplicar`):**
   removeu **189** do Supabase e enviou **201** → **411 no Cloud = 411 no
   local**. A comparação usa `(data_aula, horario, turma, disciplina)` (não só
   `turma_id`) para o rótulo antigo não passar batido.
4. **`bot_raspagem.py`:** `carregar_turma_map()` extraído e aplicado **também
   no lado local** da comparação (simetria); nova
   `reconciliar_historico(portal_data, root, aplicar=)` que remove linhas sem
   contraparte no portal **protegendo pares (turma, disciplina) que o portal
   devolveu 0 registros** (card vazio/portal congelado não apaga histórico) e
   deduplicando rótulos antigos; roda após cada raspagem completa em
   **dry-run** (`--reconciliar` ou o checkbox do app aplicam);
   `load_feriados()` aceita `DD/MM/AAAA` (fim do aviso de feriado).
5. **`database_model.save_history`:** grava `disciplina` com o nome canônico de
   `subjects.name` (elimina variantes de grafia) e **ignora** linhas com
   `turma_id`/`disciplina_id` não resolvidos (antes gravava invisível) — a
   raspagem as acusa como "faltante no local".
6. **App 8510:** checkbox "🧹 Reconciliar histórico ao sincronizar" na página
   Registro + aviso quando a última raspagem listou órfãs pendentes.

**Arquivos:** `apps/api/tools/bot_raspagem.py`, `apps/api/tools/database_model.py`,
`apps/planejamento_registro/planejamento_registro_streamlit.py`,
`scripts/limpar_historico_orfas.py`, `scripts/sync_historico_supabase.py`,
`apps/ISSUES.md` (AP-012).

**Validar:** `python scripts/limpar_historico_orfas.py` → "Nada a limpar";
`python scripts/sync_historico_supabase.py` → "Remover do cloud: 0 / Enviar: 0";
comparação 411 × 411 → 0 faltantes/0 órfãs; reconciliação em banco de teste
remove só a sujeira injetada (rótulo antigo + status excluído) e **protege** o
par inexistente no portal; `py_compile` OK nos 5 arquivos.

**Concluído (01/10):** local **601 → 411**, Supabase **399 → 411** (213 I-A +
198 I-B, todas "Aula confirmada", 0 rótulos `EMTPDES-*`, 0 duplicatas).

---

## IS-042 — Gerador: "Sobrescrever"+intervalo pulou 24/09 e duplicou o nº 30 🟡

**Sintoma:** em 01/10 a geração da turma **314114 (I-B)**, disciplina
**P.C.II** (slot Qui 15:50), não criou o plano de **24/09/2026** e criou
`01/10 = nº 30` (id 12328), **duplicando** o nº 30 do plano de 17/09
(id 12272). Estado atual: 04-11=26, 06-27=27, 09-03=28, 09-10=29,
09-17=30, **(24/09 ausente)**, 10-01=30 (dup), 10-08=31, 10-22=32 —
todos `pendente`.

**Causa raiz:** a numeração de partida é
`next = max(hist_efetivo, max_pos_seq_map) + Σ(linhas pendente/pronta)`
(`core/gerador.py` l.631-674, primeira data recebe `next+1`) — e em
**Sobrescrever** (`force_overwrite`) os pendentes **não** somam
(l.658-674, IS-019). Hist P.C.II = 25 (estável desde a limpeza IS-041 às
16:41:16) e o intervalo `De/Até` é digitado pelo usuário contra a
numeração **antiga**. Rodadas de 01/10 reconstituídas (todas com
`bloquear_sabados_letivos=true` já ativo — o save de 19:46:13 em
`master_config` foi re-save):

1. **00:29** — sem Sobrescrever, pend=0 → base 25 → 04-11=26 … 09-19=31;
   parou em `Até=31` → **24/09 (#32) ficou fora da janela e nunca surgiu**
   (12274-12283, criados numa rodada posterior e excluídos antes do backup
   das 16:41, são resquício da mesma tentativa).
2. **~16:42:52** — duas gerações sem Sobrescrever com `Até=32`:
   P.C.II (base 31 = 25+6 pend) → **24/09 = #32** (linha 12324 + arquivo);
   IA (base 31) → 29/09 = #32 (linha 12325, arquivo movido para
   `registradas` no Registrador das 16:54). A **linha 12324 — o único
   24/09 já gerado — foi depois excluída em lote**, junto com 12273
   (19/09), pela exclusão em lote adicionada na edição das 16:52.
3. **19:42:51** — **Sobrescrever** + `De=31 Até=32` + saída `pendentes` →
   base reseta para 25 → seqs 26-30 (09-03 … 01-10) **descartados sem
   aviso** (`_descarta('aula_menor_que_min')`, l.973-975) → sobraram só
   10-08=31 (12326) e 10-22=32 (12327). **24/09 recebeu seq 29 e morreu
   no intervalo.**
4. **19:48:12** — **Sobrescrever** + `De=30 Até=32` + saída `prontas` →
   base 25 → 24/09 = 29 descartado (fora do intervalo) → 01/10 = **30**
   (INSERT 12328 = duplicado), 10-08/10-22 regravados em `prontas`
   (`UPDATE`, ids preservados); 10-29 = 33 > 32 descartado.

**Provas:** rodadas 3/4 não podem ser sem Sobrescrever (pend 5-7 daria
seq ≥ 31 para datas que não existem nas saídas); sem sábados bloqueados
04-11/06-27/09-19 consumiriam seq e 09-19 geraria arquivo (não existe);
`Até=32` é obrigatório na rodada 4 (sem ele, 10-29 → seq 33 encontra
`lessons_list[32]='Aula 30'` e gravaria `prontas/10-29`).

**Defeitos:**
- **D1 (mecanismo direto):** Sobrescrever zera a base só com o histórico,
  mas o intervalo `De/Até` é digitado contra a numeração antiga → as
  datas "andam" e caem fora do intervalo sem nenhum aviso.
- **D2:** a base soma linhas com **status mutável** (`pendente`/`pronta` →
  `registrada` via `confirm-registration`) e sofre com exclusões → a
  numeração muda entre rodadas (daí o nº 30 duplicado). Hoje uma
  geração sem Sobrescrever partiria de **#34** para 24/09 (25 hist + 8
  pend + 1); cada raspagem que adicionar 03/09-10/09-17/09 ao histórico
  empurra a base ainda mais.
- **D3:** os descartes/`slots_pulados` só aparecem na UI quando **0**
  plano foi gerado (`planejamento_registro_streamlit.py` l.1314-1342);
  nas rodadas 3/4 a mensagem foi só "✅ 2 plano(s)" — motivo e datas
  descartadas ficaram invisíveis.

**Correções aplicadas (01/10):**
1. **Dados (produção):** backup `data/escola_ativa_backup_is042_20261001_222537.db`
   + os 5 `.txt` com numeracao antiga movidos para `aulas/_backup_is042/`;
   removidas as 3 linhas erradas (12326-12328) e os 4 planos **recriados pelo
   próprio gerador** (não-force, intervalo 31-34, saída `pendentes`):
   **24/09=31 (12379), 01/10=32 (12380), 10-08=33 (12381), 10-22=34
   (12382** — posição 34 sem lição "Aula XX" → título de fallback). Fila
   final com numeração **única 26…34** e conteúdo alinhado à posição da
   fila (`lessons_list[n-1]`: 24/09→Aula 28, 01/10→Aula 29, 10/08→Aula 30).
2. **D2:** base da numeração passou de `COUNT(*)` para
   `MAX(CAST(numero_aula AS INTEGER))` por (turma, disciplina) em modo
   normal (`core/gerador.py` l.658-680) — validado: PCII =
   `max(hist 25, max 34)` → próxima data nova = **35** (a fórmula antiga
   daria 33, colidindo com as existentes).
3. **D3:** `descartados`/`slots_pulados` agora são exibidos na UI **mesmo
   com planos gerados** (`planejamento_registro_streamlit.py` l.1314-1359;
   `st.info` com os descartes exceto `filtro_disciplina` + expander com os
   slots pulados).

**Pendente (D1):** `force_overwrite` continua zerando a base só no histórico
— intervalo `De/Até` digitado contra a numeração antiga ainda pode descartar
datas em silêncio (o efeito agora fica **visível** via D3). Sem alteração de
código por enquanto.

**Arquivos:** `apps/planejamento_registro/core/gerador.py`,
`apps/planejamento_registro/planejamento_registro_streamlit.py`
(registro em `apps/ISSUES.md` → **AP-013**).

**Validar:** fila P.C.II = 26,27,28,29,30,31,32,33,34 sem duplicatas e com
24/09 presente; geração não-force sem intervalo parte de 35 (não de 33/34);
rodada com planos gerados exibe "Descartes nesta geração: …" na 8510
(streamlit faz auto-reload no próximo rerun); `py_compile` OK nos 2 arquivos.

---

## IS-043 — Fila Disc.Tec.: plano modular gerado antes da última aula registrada no portal 🟢

**Sintoma:** na turma **309197 (I-A)**, a geração da disciplina
**Fundamentos de UI/UX** (fila Disc.Tec., slot genérico) criou planos a
partir de **18/05/2026** (ids 12276-12279: 18/05, 25/05, 01/06, 03/06)
enquanto o módulo anterior **Front-End** seguia registrado no portal até
**03/06/2026** (40 aulas, última em 03/06 07:10). O módulo seguinte só
deveria começar em **04/06**.

**Causa raiz:** o piso "após a última aula registrada" é calculado **por
turma/disciplina** (`inicio_geracao`/`inicio_disciplina`, `core/datas.py`) —
Fundamentos, sem histórico próprio, caía no fallback `base` = `data_corte`
(01/04). A janela de Fundamentos (02/06–03/07) com tolerância ±15 dias
(`tolerancia_janela_dias=15`) começa em **18/05**, e com a disciplina
filtrada a `janela_filtro` força a resolução dos slots genéricos para ela
(AP-011) → as datas de maio/junho foram geradas normalmente (o único gate
antes do calendário era o slot ocupado via `historico_set`). Em 314114 o
mesmo efeito criou 05-21 e 05-28 < última Front-End 29/05.

**Correção aplicada (01/10):**
1. `core/datas.py` → nova `ultima_aula_modular(ids_modulares)`: retorna
   `(ids_expandidos, {turma: data})` — a última aula registrada entre as
   disciplinas modulares da turma (ids vindos das janelas ≤300 dias,
   expandidos via `discipline_aliases` base↔aliases; anuais P.C.II/IA/
   Mentorias ficam de fora, como em `janelas_modulares`).
2. `core/gerador.py` → logo após montar `janelas`, calcula `ids_modulares`
   + `ultima_modular`; no gate de data, quando o slot é genérico ou a
   disciplina resolvida é modular, o limite passa a ser
   `max(inicio_disciplina, última_modular + 1 dia)` — **o portal manda
   sobre o calendário e a tolerância** (o slot ocupado já era o 1º gate via
   `historico_set`/`planejamento_set`). Debug da 8510 ganhou
   `piso_modular_turmas`.

**Validação (sandbox A/B — cópia do DB, linhas 309197/8 apagadas, mesmos
parâmetros):**
- Controle (código anterior): 4 linhas antes do piso (18/05…03/06),
  `descartados.antes_inicio_disciplina: 0` → bug reproduzido.
- Corrigido: `antes_inicio_disciplina: 4`, primeira linha **05/06 ≥
  04/06**, zero datas abaixo do piso (mesmo total de 40 linhas).
- Unit: 309197 → última modular 03/06 → piso 04/06; 314114 → 29/05 →
  piso 30/05. `py_compile` OK; banco de produção intocado (mtime
  22:25:37; 8 linhas 309197/8 e 10 em 314114/8).

**Dados (produção, 01/10, aprovado "Remover e renumerar"):** backup
`data/escola_ativa_backup_is043_20261001_225025.db` + os 6 `.txt` abaixo do
piso movidos para `aulas/_backup_is043/`; removidas as 6 linhas (12276-12279
em 309197/8 e 12369-12370 em 314114/8) e as restantes **renumeradas pelo
próprio gerador** (force + `aula_max`, estrategia "Aula de atividades em
laboratório"): **309197/8 = 4 linhas 1..4** (05/06×3, 06/08) e **314114/8 =
8 linhas 1..8** (01/06×2, 05/06, 06/08×2, 06/11×3), com `.txt`
regravados alinhados à nova posição (AULA_NUM ↔ conteúdo da lição) e o
piso bloqueando a recriação das datas antigas (`antes_inicio_disciplina:
4`/`2` nas rodadas de força). Verificado em sandbox antes em produção;
nenhuma linha/file abaixo do piso e nenhum número duplicado.

**Arquivos:** `apps/planejamento_registro/core/datas.py`,
`apps/planejamento_registro/core/gerador.py` (registro em `apps/ISSUES.md`
→ **AP-014**).

**Validar:** regenerar (não-force, filtro Fundamentos) para 309197 não
recria datas < 04/06; o debug da 8510 exibe `piso_modular_turmas`; slots
do histórico continuam pulados primeiro ("Ja existe no historico"); disciplinas
anuais (P.C.II etc.) sem histórico não são afetadas (piso continua `data_corte`).

---

## IS-044 — Grade horária com slot fantasma 09:10: plano gerado em horário que não existe no portal 🟢

**Sintoma (relatado):** a geração de Fundamentos (disc 8) criou
`plano_309197_8_2026-06-08_0910.txt` (AULA_NUM 05, 09:10–10:10) na segunda,
mas **no portal não existe esse horário** — lá é **09:30–10:30** e a turma
tem apenas **duas** aulas Disc.Tec. nas segundas (08:10 e 09:30). O mesmo
fantasma existia na I-B (quintas): linha #8 de 06-11 às 09:10.

**Causa raiz:** o `historico_aulas` tem **0 linhas com horário 09:10** (para
qualquer turma/disciplina) — o portal sempre registrou 09:30 — mas a
`weekly_schedule` tem os **dois** horários convivendo nos **3 espelhos**
(triplo espelho, `docs/AUDITORIA_BANCO.md`), e a deduplicação do IS-020 é
por `(class_name, day_of_week, time_slot)`: 09:10 e 09:30 são chaves
distintas, então **ambas sobrevivem** e a segunda da I-A virou 3 slots
Disc.Tec. (08:10, 09:10, 09:30):

| Espelho | I-A Seg 09:10 | I-B Qui 09:10 | 09:30 correto |
|---|---|---|---|
| SQLite local (lido pelo gerador da 8510) | linha `id=NULL` (geração antiga) | cópia `2569` | presente |
| Supabase (ao vivo) | `2578` | `2569` | `2559` / `2579` |
| `grade_horaria.json` | `09:10` rotulado `I.A.` | `09:10` | **faltava** |

O JSON trazia ainda I-A Sexta `12:30` (portal: 11:30) e I-A Seg `10:30`
rotulado `Disc.Tec.` (portal: `I.A.`). Como o `load_grade()` do plugin
"Grade Semanal" funde JSON+Supabase e o botão **"Sincronizar com Nuvem"**
reescreve o JSON a partir desse fusionado, corrigir só o SQLite não seria
durável — o 09:10 reapareceria (e o Supabase também o receberia).

**Correção (somente dados — nenhum código alterado; aprovada "Completo:
local + Supabase + JSON"; 02/10):**
1. **SQLite local:** `DELETE` dos 2 slots 09:10, com guard que exigia o
   09:30 correspondente já presente antes de apagar (1 linha cada).
2. **Supabase:** `DELETE` ids `2578` (I-A Seg) e `2569` (I-B Qui) com
   `eq(id)` + `eq(time_slot='09:10')` + `eq(day_of_week)` — `select`
   final confirmou nenhum 09:10 restante nas turmas da 2ª série.
3. **JSON:** I-A Seg → `{07:10 P.C.II, 08:10 Disc.Tec., 09:30 Disc.Tec.,
   10:30 I.A.}`; I-A Sex `12:30`→`11:30`; I-B Qui `09:10`→`09:30`
   (dias reordenados por horário).
4. **Planos:** linhas `12399` (I-A #509:10) e `12394` (I-B #8 09:10)
   removidas, os 2 `.txt` movidos para `aulas/_backup_is044/` e
   renumeração via **force + intervalo 1–8** (mesmo harness IS-043,
   **sandbox validado antes** da produção, estratégia "Aula de atividades
   em laboratório").

**Resultado (produção, 02/10 00:25, "TODAS AS VERIFICACOES OK"):**
`309197/8` = **8 linhas 1..8** (06-05×3; 06-08 08:10=4, **09:30=5**;
06-09=6; 06-10 07:10=7, **08:10=8**) e `314114/8` = **8 linhas 1..8**
(… **06-11 09:30=8**) — `.txt` regravados com `AULA_NUM` ↔ conteúdo da
posição; **0 linhas 09:10** em `planejamento`, grade local e Supabase;
JSON válido. Backups: `data/escola_ativa_backup_is044_20261002_002548.db`
e `aulas/_backup_is044/` (2 `.txt` + `grade_horaria_*.json`).

**Observação:** os 7 arquivos históricos `aulas/registradas/*0910*` da
disc 6 (Front-End, mai/jun) foram **mantidos** — dizem 09:10, mas não há
linhas correspondentes em `planejamento` (somente arquivo, sem impacto na
geração; fora de escopo aprovado).

**Arquivos:** nenhum código alterado (só dados + documentação); registro
cruzado em `apps/ISSUES.md` → **AP-015**.

**Validar:** gerar planos de Fundamentos na I-A sem force → nenhum slot
09:10 é considerado (grade limpa) e a segunda exibe exatamente 2 planos
Disc.Tec. (08:10 e 09:30); plugin 🗓️ Grade Semanal não mostra coluna
09:10 e "Sincronizar com Nuvem" não a reintroduz; arquivo
`plano_309197_8_2026-06-08_0930.txt` = AULA_NUM 05 / 09:30 - 10:30.

---

## IS-045 — Aulas especiais via "livro-caixa" (estrutura em blocos + zonas livres) 🟢

**Status: fase 1 CONCLUÍDA e validada em 02/10** (model' + integração na fila
do gerador + aba "📚 Livro-Caixa" no 8510). As decisões da conversa de 02/10
ficam registradas abaixo; o que foi implementado e validado está no fim.

**Motivação:** 40h = 32 aulas de conteúdo + 8 especiais (Avaliação,
Seminário, Pesquisa...). O problema da solução atual é a **numeração linear
monolítica 01→40** — não há onde encaixar as especiais sem renumerar o
conteúdo.

**Estrutura aprovada:** fechar conjuntos semanais de 8 aulas com zonas
livres: **`{01-08} {09-16} [LIVRE] {17-24} {25-32} [LIVRE]`**, com
fechamento por **horas** (40h = concluído, não "40 linhas"). Conteúdo segue
linear 01→32 dentro dos blocos; o que entra nas zonas (após o 16 e após o
32), quantos e de que tipo é **livre, decidido no model**. Essa estrutura
responde as 4 perguntas de projeto (distribuição, numeração, tipos, escopo)
sem decisões extras.

**Arquitetura (decidida):**
1. **`lessons` e suas relações: intocadas.** Zero migração, zero mudança em
   portal/quizzes/fórum/Atividades — verificado que **não existe join
   posição↔título** no código: tudo que lê "número da aula" lê do **título**
   (`get_lesson_number(title)` em `views/aulas.py:386` e
   `daily_activities.py:72`, que ignora quem não tem número: `if n:` e
   `max(...+[0])`), enquanto `planejamento.numero_aula` só vira
   agenda/posição (portal `views/portal.py:72`, registro, histórico).
2. **model' (somente leitura):** camada nova que consulta o relacionamento
   banco↔front-end Streamlit e resolve a estrutura por disciplina; tipos e
   escopo livre são definidos nele. Não escreve em `lessons`.
3. **Livro-caixa em `master_config`** (decisão "Ponto 1"): JSON por
   disciplina (chave nova, mesmo padrão de `feriados.json`). Leitura direta
   no SQLite local — sem egress, logo **sem `local_cache`** (a regra de
   cache do AGENTS.md vale para leituras repetitivas do Supabase, não do
   banco local). Espelhado automaticamente pelo `audit_backup`.
4. **App gerador de planos (8510) passa a "escutar a conversa":** consulta
   o model, **persiste a resolução no livro-caixa** e gera os planos a
   partir dele. **Único ponto de integração** com código existente: a fila
   que hoje ordena por número do título (`apps/planejamento_registro/core/gerador.py`
   `_ordenar_lessons_fila` 73-84, montagem 449-461, lookup
   `lessons_list[pedagogical_idx-1]` 1027-1030) passa a consultar o
   livro-caixa. O resto é aditivo.
5. **Numeração (decisão "Ponto 2"):** `AULA_NUM` é **figurante** — guarda a
   **posição para o portal**; pode ficar fora de ordem em relação ao título
   (título 17 na posição 20 sem problema). O título da posição vem do que
   for escrito no **plugin Atividades**:
   `AULA_NUM: 17 -> {titulo = <o que vier do Atividades>}`.
6. **Exibição:** aula especial **não aparece na página Aulas** — não é
   conteúdo, é **avaliação**. Aparece na página **Avaliações**, como o
   Seminário (via `create_assessment`, fluxo de `daily_activities.py:136-229`).
   Diferença-chave: lançar o seminário **das aulas 01–16** e **registrar na
   posição 17/18 do portal**; título = o da avaliação; **frequência
   editável no portal**.
7. **Legado:** disciplinas já geradas com 40 lineares ficam como estrutura
   "linear legada" aceita pelo model — sem reescrever conteúdo existente.

**Implementado em 02/10 (fase 1 — único ponto de integração com código
existente):**
* `services/livro_caixa.py` (novo): model' somente leitura — CRUD do doc em
  `master_config` (chave `livro_caixa:<subject_id>`, schema duplo
  `chave/valor`↔`key/value`), `estrutura_padrao`/`estrutura_linear`,
  `resolver` (fila posicional `entradas` com `tipo: conteudo|especial`),
  `conferir` (erros/avisos: blocos fora de ordem, especial sem título,
  meta≠cobertura, aulas ausentes em `lessons`), `resolver_e_marcar`.
  Aponta para a cópia do banco no sandbox via `DB_PATH_OVERRIDE`/env
  `SYSAVA_DB_PATH`.
* `apps/planejamento_registro/core/gerador.py`: build de `filas_livro`
  {key: (entradas, num_map)} após a ordenação legada; consumo **posicional**
  por `seq_num` (`item_lc`/`lesson`/`especial_lc` — a especial vira
  pseudo-lesson e NÃO conta como "sem lição"); fallback para a fila legada
  quando a posição está fora da cobertura ou não há doc; `estrategia_plano`
  + objetivos/recursos/atividade vindos do item; counter `especiais` no
  retorno.
* `apps/planejamento_registro/planejamento_registro_streamlit.py`: função
  `secao_livro_caixa(turma, subject)` + entrada "📚 Livro-Caixa" no rádio de
  navegação (criar estrutura padrão/linear, recalcular+salvar resolução,
  métricas e conferência, tabela da fila resolvida com coluna "Nº título",
  editor de zonas livres, blocos JSON, remover livro-caixa).

**Validação (02/10):**
* Unitário do model' (`_lc_unit.py`, 25+ asserções; harnesses em
  `%TEMP%\opencode`): resolver, zonas,
  conferir (erros/avisos), linear, CRUD local nos dois schemas de
  `master_config`.
* Sandbox (`_lc_sandbox.py`, cópia em `%TEMP%\lc_sandbox`, harness padrão
  IS-043/044): disciplina 8 (Fundamentos, turma 309197), doc de teste
  `blocos [[1,4],[5,6]]` + 2 zonas com 1 especial cada → 8 planos:
  posições 1-4 = Aula 1-4, **posição 5 = especial**, **posições 6/7 com
  `AULA_NUM` 06/07 divergindo do título (Aula 5/Aula 6 — figurante
  confirmado)**, posição 8 = especial; estratégias vindas do item especial
  vs. a passada no gerador; `especiais=2`, `sem_licao=0`; doc removido →
  **regressão legada** idêntica ao comportamento pré-IS-045 (posição N =
  N-ésima aula por título, `especiais=0`).
* Smoke da UI (8511 headless, browser-automation): navegação → "📚
  Livro-Caixa" renderiza subheader/legenda/aviso "sem livro-caixa" e os 2
  botões de criação, **0 erros de console, 0 requests falhos** (nenhum botão
  de escrita clicado — leitura apenas).

**Observação:** o app 8510 precisa ser **reiniciado/recarregado** para
mostrar a nova aba.

**Pendências (fases 2/3):** Atividades (lançamento por tipo nas posições e
título da posição vindo do plugin) e abertura de zonas/especiais no
gerador. Registro da frente do app: **AP-016** em `apps/ISSUES.md`.

**Arquivos:** `services/livro_caixa.py` (novo), `master_config` (chaves
`livro_caixa:<subject_id>`), `apps/planejamento_registro/core/gerador.py`
(fila), `apps/planejamento_registro/planejamento_registro_streamlit.py`
(aba), `data/repo/plugins/daily_activities.py` (fase 2, ainda não tocado).

---

## IS-046 — Transição de disciplina: slots livres do dia da última aula ficavam ociosos 🟢

**Sintoma (relatado):** a turma **309197 (I-A)** encerrou o módulo
**Front-End** (disc 6) em **03/06/2026 07:10** (40ª aula) e o slot
**03/06 08:10** — o único DT livre de junho na grade I-A — ficou sem dono;
a geração de Fundamentos (disc 8) só começou em **05/06**. O relato citou
"5 slots na quarta", mas a grade I-A tem apenas 2 DTs na quarta
(07:10/08:10); os **5 slots da quinta 04/06 (I-B)** estão livres porque
**04/06 = Corpus Christi** (confirmado em `feriados.json`) — é o correto,
não é desperdício. Os slots de julho livres são apenas pendentes ainda não
gerados (planos param em 01/07 na I-A e 11/06 na I-B).

**Causa raiz:** o piso do IS-043 em `core/gerador.py` usava
`ultima_modular + 1 dia` → limite 04/06, e o gate
`antes_inicio_disciplina` descartava **todo o dia 03/06**, mesmo com
`janela_por_data(03/06)` já resolvendo **Fundamentos** (janela 02/06–03/07,
tol ±15, distância 0). O slot da aula registrada já era protegido pela
ocupação (`historico_set`), então o "+1 dia" só jogava fora os horários
livres restantes do dia da transição.

**Correção (02/10):** `core/gerador.py` (gate pós-IS-043):
`limite = max(limite, ult + timedelta(days=1))` →
`limite = max(limite, ult)` — o piso vale o **próprio dia** da última aula
modular. Continuam valendo: ocupação pula o slot já registrado;
`inicio_disciplina` da própria disciplina (+1) impede a seguinte de
reiniciar no mesmo dia; o bloqueio de datas **anteriores** a `ult` (IS-043)
permanece.

**Validação (02/10, `_trans_sandbox.py`, cópia do DB em `%TEMP%\tr_sandbox`):**
- Pré-condições: 39 linhas disc 8 (duas turmas) removidas; histórico do
  FE-I-A de 01/06–02/06 removido de propósito (libera 3 slots) mantendo o
  de 03/06 (piso = 03/06).
- **Fase A (I-A, força):** **0 linhas em 01/06–02/06** mesmo com slots
  livres (piso IS-043 preservado), **exatamente 1 linha em 03/06 08:10 =
  nº 1** (transição liberada), continuidade 05/06 07:10 nº 2, 40 aulas
  03/06–08/07, nums 1..40 monotônicos (`sem_licao=9` = posições 32-40 sem
  lição na fila legada, comportamento pré-existente).
- **Fase B (I-B, força):** primeira aula **01/06** (pós-29/05 do FE),
  **0 aulas em 04/06** (feriado), 40 aulas 01/06–09/07, nums monôtonos —
  regressão preservada (pré/pós-fix idêntico nesta turma).
- Regressão IS-045: `_lc_sandbox.py` reexecutado → OK. `py_compile` OK.

**Produção (02/10, aprovado):** backup
`data/escola_ativa_backup_is046_20261002_153325.db`; os 31 `.txt` atuais (30
em `prontas` + 1 em `registradas`) movidos para `aulas/_backup_is046/`;
regenerados com **force + intervalo 1..31** (31 lições reais, mesma
estratégia "Aula de atividades em laboratório", `output_dir='prontas'`):
**31 linhas 1..31, de 03/06 08:10 (Aula 1) a 06/30 07:10**, sem 01/07 — a
linha órfã de 01/07 (fora do novo conjunto de slots) foi removida.
Verificação: nums monotônicos, 31 `.txt` em `prontas` com AULA_NUM × DATA ×
DB consistentes, `sem_licao=0`. **I-B não regenerada** (não muda nada).
Efeito colateral: o dia 01/07 ficou sem plano — as 31 lições cabem nos 31
primeiros slots a partir da transição; se quiser cobrir 01/07, gerar
intervalo 1..32 (posição 32 = conteúdo genérico, sem lição correspondente).

**Arquivos:** `apps/planejamento_registro/core/gerador.py` (~l.981, gate
`antes_inicio_disciplina`; frente: `apps/ISSUES.md` → **AP-017**).

**Validar:** gerar disc 8 da I-A e conferir primeiro slot = 03/06 08:10 sem
nada anterior; I-B mantém início 01/06 e pula 04/06.

---

## IS-047 — Grade horária na ⚙️ Config: monitor dos 3 espelhos + edição (Sex 11:30/13:30 → Qua) 🟢

**Pedido:** as duas últimas aulas de Disc.Tec. da sexta da **I-A** passaram
para a quarta (print do sistema oficial, 03/06/2026, mostrando 4 horários
de Fundamentos na quarta: 07:10, 08:10, 11:30, 13:30). Criar na página de
Configurações um lugar para **monitorar e editar** esse tipo de mudança.

**Solução:**
1. Novo núcleo `apps/planejamento_registro/core/grade.py`: leitura dos 3
   espelhos (`weekly_schedule` SQLite do gerador, `grade_horaria.json` do
   Registro do portal, `weekly_schedule` Supabase), `divergencias()`
   (comparação slot a slot com status), `impacto()` (aulas registradas +
   planos por slot, com aviso "planos fora da grade") e edição
   `mover/adicionar/remover` que grava **nos 3 espelhos de uma vez**
   (SQLite delete+insert com dedup de duplicatas, JSON reescrito,
   Supabase delete+upsert `on_conflict=class_name,day_of_week,time_slot`).
2. Nova seção `#### 🗓️ Grade horária (monitor + edição)` na ⚙️ Config do
   8510 (logo após Feriados), com abas **📋 Grade** (pivot dia×horário),
   **🔀 Espelhos** (tabela de divergências + estado da nuvem), **⚖️
   Impacto** (planos/registradas por slot com flags) e **✏️ Editar**
   (mover/adicionar/remover, com confirmação antes de gravar).

**Dados aplicados (02/10):** backups `escola_ativa_backup_is047_20261002_171734.db`
e `aulas/_backup_is047/grade_horaria_*.json` (mais os 31 `.txt` movidos para
lá); grade I-A: **Sexta 11:30/13:30 removidos, Quarta 11:30/13:30 =
Disc.Tec.** nos 3 espelhos (Supabase: "ok"); planos disc 8 regenerados com
**force 1..31**: 31 linhas de 03/06 08:10 (nº1) a 06/30 07:10 (nº31), com
os **8 planos** que estavam em Sex 11:30/13:30 agora em Quarta 11:30/13:30.

**Validação:**
- `_grade_sandbox.py` (cópia DB+JSON em `%TEMP%\grade_sandbox`): baseline
  SQLite==JSON; mover os 2 slots com dedup (duplicata local removida, resta
  exatamente 1 linha); round-trip adicionar/remover; guards de slot
  inexistente — todas OK (nuvem leitura OK).
- `_grade_apply.py` (produção): 3 espelhos idênticos (divergências = 0), 8
  planos em Quarta 11:30/13:30, 0 em Sexta, 31 `.txt` com AULA_NUM × DATA ×
  DB consistente.
- Smoke UI (8511 headless, browser-automation): seção e as 4 abas renderizam,
  "Espelhos consistentes", "Nenhum plano fora da grade", editor operacional,
  **0 erros de console, 0 requests falhos**.

**Arquivos:** `apps/planejamento_registro/core/grade.py` (novo),
`apps/planejamento_registro/planejamento_registro_streamlit.py` (seção na
Config); frente do app: `apps/ISSUES.md` → **AP-018**.

---

## IS-048 — Caderno de notas com `NaN` (JSON inválido) + opção [5] do menu dos apps quebrada 🟢

**Sintomas:**
1. `data/repo/plugins/student_scores.json` continha `"N2": NaN` — **não é JSON
   válido**. O `JSON.parse` do `dashboard_dinamico.html` falhava com
   *"Unexpected token 'N'"* e o dashboard caía no modo demonstração.
2. `apps/run_apps.bat` opção `[5] Analise de Notas` testava a existência de
   `apps/analise_notas/README_DASHBOARD.md`, arquivo movido para
   `apps/docs/` no commit `046ee7c` — a opção caía no `else` e só imprimia
   `[INFO] Rode: export_student_scores.py`.

**Causa do `NaN`:** `student_scores.py` grava `round(row["NM1"], 2)` a partir
de uma média pandas sem valores válidos → `NaN`, e `json.dump` aceita `NaN`
por padrão (a leitura em Python também aceita, por isso ninguém notava).

**Solução:**
1. `data/repo/plugins/student_scores.py` e `data/repo/plugins/daily_activities.py`
   — `save_json()` agora passa os dados por `_sem_nan()` (recursivo) e grava
   com `allow_nan=False`: nada de `NaN`/`Infinity` chega ao disco.
2. `data/repo/plugins/student_scores.json` — reescrito uma vez com `NaN` →
   `null` (42 alunos preservados; `json.loads` estrito OK).
3. App novo **`apps/analise_notas/`** (porta **8511**): `core.py` saneia na
   leitura (`sanitizar_json`), `analise_notas_streamlit.py` com as abas
   Análise / Dashboard HTML / Registro iSeduc, `bot_lancar_notas.py` como
   subprocesso e `README.md` com o passo a passo do servidor HTTP local +
   dashboard. Ver **AP-019** no `apps/ISSUES.md`.
4. `run.bat` ganhou a opção `[6]` (8511) e `apps/run_apps.bat` a `[5]` agora
   inicia o app (antes abria o README sumido).

**Validação:** `py_compile` dos plugins e de todos os `.py` do app;
`pytest` em `apps/` → **36 testes OK** (22 novos em
`tests/test_analise_notas.py`); smoke do app 8511 com `streamlit.testing.v1.AppTest`
(0 exceções, 0 avisos de `use_container_width` deprecado, 6 KPIs); dashboard
via browser-automation servido em `http://127.0.0.1:8765/dashboard_dinamico.html`
(**"✅ Dados carregados: 42 alunos"**, 3 gráficos Plotly renderizados em SVG,
100 linhas de tabela, **0 erros de console e 0 requests falhos**).

**Arquivos:** `data/repo/plugins/student_scores.py`,
`data/repo/plugins/daily_activities.py`,
`data/repo/plugins/student_scores.json` (dado), `run.bat`,
`apps/run_apps.bat`, `apps/README.md`, `apps/AGENTS.md`,
`apps/requirements.txt`, `apps/analise_notas/*` (novo), `apps/tests/test_analise_notas.py`
(novo); frente do app: `apps/ISSUES.md` → **AP-019**.

**Validar:** ⚙️ Config → aba 🔀 Espelhos com os 3 espelhos iguais; o
Registro do portal (03/06, quarta) oferece os 4 horários de Fundamentos; o
plugin Grade Semanal não reintegra Sexta 11:30/13:30 (nuvem já corrigida);
gerar planos sem force não recria slots de sexta 11:30/13:30.

---

## IS-049 — Investigação das notas no portal iSeduc + pasta `apps/bots/` 🟢

**Pedido (2 problemas em um):** (1) criar uma página de investigação da
situação de notas **no portal** iSeduc a partir do scraper da API, e (2)
criar uma pasta `bots/` centralizando todos os bots do sistema.

**Decisões do mantenedor:** página em **modo Ambos** (endpoint na API local +
aba consumidora), pasta **`apps/bots/` versionada** e escopo **apenas os 6
bots ativos** (`registrar_aulas`, `registrar_notas`, `grade_scraper`,
`bot_raspagem`, `inspector_diagnostico`, `inspector_frequencia`); o legado
`api/tools/versão_aulas_selenium/` permanece onde está (só com o import
corrigido).

**Solução (tudo dentro do repo aninhado `apps/`, que o `.gitignore` da raiz
ignora — nenhum arquivo do núcleo do SysAva foi alterado):**
1. **`apps/bots/`** — 6 bots movidos de `apps/api/tools/`, cada um com
   bootstrap `PROJECT_ROOT` (raiz) + `apps/` + `apps/api` no `sys.path`;
   referências externas redirecionadas em `api/api_service.py`,
   `api/tools/agents/agent_router.py`,
   `planejamento_registro/planejamento_registro_streamlit.py` e
   `analise_notas/bot_lancar_notas.py`.
2. **`apps/bots/grade_scraper.py`** — modo investigação de **somente
   leitura**: descobre os cards da grade pelo nome (turma/disciplina),
   resolve os ids no SQLite local, lê os 3 trimestres, monta e grava
   `data/logs/investigacao_ultimo.json` (escrita atômica) e aceita CLI
   (`--turma-id --disciplina-id --trimestres --out`).
3. **`apps/api/api_service.py`** — `POST /notas/investigar` (subprocesso +
   `BackgroundTasks`, log `data/logs/investigacao_notas.log`, timeout 600s),
   `GET /notas/investigar/status` e `GET /notas/investigar/relatorio`.
4. **`apps/analise_notas/`** — `core.comparar_portal_vs_caderno()` puro
   (status `Divergente`/`Falta no portal`/`Só no portal`/`Só no caderno`/
   `Igual`/`Sem dado`) + 4ª aba **🔍 Investigação iSeduc** no app 8511
   (coleta via API 8002 se estiver de pé, senão subprocesso; KPIs, filtro,
   tabela, CSV).

**Validação:** `py_compile` OK; `pytest -q` em `apps/` → **41 testes OK**;
import smoke dos 6 bots e de `api_service` (96 rotas); API de pé →
`/health-check` 200, `/notas/investigar/status` `parado`, relatório 404 sem
coleta; `AppTest` do 8511 → **4 abas**, 0 exceções/erros, KPIs da investigação
renderizando com relatório sintético (23 linhas).

**Arquivos:** `apps/bots/*` (novo), `apps/api/api_service.py`,
`apps/api/tools/agents/agent_router.py`,
`apps/api/tools/versão_aulas_selenium/*`,
`apps/planejamento_registro/planejamento_registro_streamlit.py`,
`apps/analise_notas/{core,analise_notas_streamlit,bot_lancar_notas}.py`,
`apps/tests/test_analise_notas.py`, `apps/{README.md,AGENTS.md,.gitignore}`;
frente do repo: `apps/ISSUES.md` → **AP-020**.

**Validar:** subir a 8511 → aba **🔍 Investigação iSeduc** → escolher
turma/disciplina → **🔎 Coletar notas no portal** → KPIs e tabela por status;
`.sysenv\Scripts\python.exe apps\bots\grade_scraper.py --turma-id 1
--disciplina-id 11 --trimestres 1` imprime `RELATORIO: …`.

---

## IS-050 — Análise de Notas: notas editáveis + quem pode receber nota (⚙️ Config) 🟢

**Pedido:** (1) permitir **editar as notas livremente** numa tabela antes de
mandar para o portal iSeduc, e (2) garantir que alunos que não podem receber
nota **nunca tenham a nota destruída** pelo robô.

**Causa:** o robô montava o payload direto do caderno
(`student_scores.json`) e escrevia em todas as linhas da turma. O portal
**não tem** status "transferido" (lá quem saiu aparece como "Falta"), então
não havia como distinguir um transferido de um faltoso normal — e alunos
transferidos cuja linha continua no portal corriam o risco de ser zerados.

**Decisões do mantenedor (régua dos casos reais):**

| Aluno | Situação | Status |
|---|---|---|
| Luara | saiu da escola, continua no caderno com notas | **Transferido** → nunca escreve (notas preservadas) |
| Fabiano | fora da lista do portal (drop-out) | **Fora do portal** |
| Yasmin | na escola, nunca fez prova | **Zero sempre** |
| Cleison | AEE, não pode ser reprovado | **AEE** → piso 6 |
| Alice | licença maternidade, recuperação até o fim do ano | **Licença** → piso 6 |
| Lázaro | voltou a frequentar as aulas | **Voltou às aulas** → idêntico a *Normal* (rastreio) |

* **"Zero sempre" envia os `0,0` e mantém os valores não-zero** do caderno —
  nunca força `0,0`; quem quiser zerar tudo edita a célula na tabela.
* **"Zero sempre" só existe por marcação manual** (ninguém nasce assim).
* **Piso 6 (AEE e Licença)**: nota abaixo de 6, `0,0`, vazia ou inválida é
  enviada como `6,0` — inclusive o zero. A **tabela mostra a nota real do
  caderno**; quem eleva é o envio, e a aba 🤖 lista cada elevação
  (*ANA NM2: 4,00 → 6,00*). Rastreável pelo status, sem mexer no portal.
* **Balanço com o portal (decisão do mantenedor: "portal é a fonte da
  verdade")**: se o relatório da 🔍 Investigação mostra **≥ 6,0** naquela
  célula, **nada é escrito** — se lá tem 9, fica 9 (ele edita no portal se
  houver divergência). O piso só age onde o portal não protege: caderno
  ≥ 6,0 vai como está; abaixo dele (ou vazio) entra `6,0`. Fonte local
  (`data/logs/investigacao_ultimo.json`, 0 bytes de egress); sem relatório
  da seleção atual, o aviso da aba 🤖 diz que o balanço ficou só pelo
  caderno.
* **"Voltou às aulas"** = *Normal* (sem piso, zeros conforme a opção) —
  existe para rastrear quem saiu de "A classificar".
* Quem está no espelho da lista negra **ainda sem decisão** vira
  **"A classificar" = não envia** (proteção padrão: Luara é salva mesmo
  antes de alguém classificá-la).

**Solução (repo aninhado `apps/`, nenhum arquivo do núcleo do SysAva foi
alterado):**

1. **`apps/analise_notas/core.py`** — espelho da lista negra
   (`carregar_lista_negra()` lê `data/excecoes_alunos.json`, com fallback no
   SQLite local; `motivo_lista_negra()` casa por RA **ou** nome normalizado)
   + **status de envio** (`Normal`, `Zero sempre`, `AEE`, `Licença`,
   `Voltou às aulas`, `Transferido`, `Fora do portal`, `A classificar`)
   resolvidos por `status_do_aluno()` / `mapa_status_envio()` /
   `aplicar_lista_negra()`, com `valor_para_envio(bruto, status, portal=)`
   aplicando as regras de cada status (balanço do piso com o portal, piso 6,
   zeros, faixa 0..10), `balanco_piso()` listando o que foi elevado/preservado
   e `notas_do_portal()` lendo o relatório da 🔍 Investigação (`{RA: {NM1:
   8.0}}`, filtrado por turma/disciplina/trimestre). A classificação é gravada
   no **`master_config`** local
   (SQLite `key/value/updated_at`, fallback `data/master_config.json`) na
   chave **`notas_status_alunos.json`** — o espelho de frequência **não é
   alterado**. As três montagens de payload (`montar_payload_lancamento`,
   `montar_edicao_lancamento`, `payload_da_tabela`) aplicam as regras e aceitam
   `portal_notas=`; a
   investigação (`comparar_portal_vs_caderno`) passa `status_notas={},
   lista={}` para continuar comparando a **realidade**.
2. **`apps/analise_notas/analise_notas_streamlit.py`** — aba **🤖 Registro**
   virou `st.data_editor` (RA/Aluno/Status travados, notas 0..10), grava
   `data/logs/notas_payload.json` (escrita atômica) e passa `--payload` ao
   robô; **aviso do balanço AEE/Licença** (regras, contagem de
   elevadas/preservadas e expander com o detalhe por célula). Nova **5ª aba
   ⚙️ Config** com monitoramento das duas fontes
   (espelho × `master_config`, contagens e mtime), lista dos pendentes,
   explicação de cada status e a classificação por aluno (selectbox, por
   turma da sidebar) com merge que preserva quem está fora do filtro.
3. **`apps/analise_notas/bot_lancar_notas.py`** — `--payload ARQ` com
   validação (nota finita em 0..10), aviso se o arquivo foi gerado para
   outra turma/disciplina/trimestre, descarte de RAs de outra turma e
   **`aplicar_lista_negra()` de segurança** antes de qualquer envio
   (inclusive em payload escrito à mão); no modo caderno carrega
   `portal_notas=` e imprime a linha do **balanço** no cabeçalho.
4. **`apps/bots/registrar_notas.py`** — `lancar_notas_do_banco(..., payload=)`
   usa o JSON da UI **e reaplica as regras** (defesa em profundidade).

**Validação:** `py_compile` de 5 arquivos OK; `pytest -q` em `apps/` →
**69 testes OK** (27 do AP-021, sendo 5 do balanço piso × portal, roundtrip
do `master_config` nos dois schemas, payload editável e o arquivo
do robô); dados reais → espelho com 9 RAs e classificação manual gravada no
`master_config` (42 alunos: Luara `Transferido`, Fabiano `Fora do portal`,
Yasmin + 3 `Zero sempre`, resto `Normal`); `AppTest` do 8511 → **5 abas**, 0
exceções/erros, com o aviso do balanço renderizando **1 célula elevada · 2
preservadas** quando o relatório da 🔍 traz 8,0/7,5 para um AEE; dry-run do
robô com payload contendo a Luara com `0,0`
escritos à mão → `Filtro: 1 aluno(s) removido(s)` e exit 0.

**Arquivos:** `apps/analise_notas/{core,analise_notas_streamlit,bot_lancar_notas}.py`,
`apps/bots/registrar_notas.py`, `apps/tests/test_analise_notas.py`;
frente do repo: `apps/ISSUES.md` → **AP-021**.

**Validar:** subir a 8511 → aba **⚙️ Config** → conferir espelho e
`master_config` → classificar (ex.: Luara = *Transferido*, Yasmin =
*Zero sempre*) → **💾 Salvar classificação**; voltar à aba **🤖 Registro** →
conferir que os bloqueados saíram da tabela → **🧪 Dry-run** → verificar no
log `Origem: payload editado da UI` + `Filtro: N aluno(s) removido(s)`.

---

## IS-051 — Aba 🌐 Portal: recursos do app de Planejamento trazidos para o Portal 🟢

**Pedido:** estudar o app `apps/planejamento_registro` (porta 8510) e trazer
alguns recursos para a aba **🌐 Portal** do app principal (`views/portal.py`),
que era só um esqueleto com avisos "🚧 Em construção".

**Arquitetura:** o Portal **não** roda os bots nem lê a árvore local
diretamente — fala com a **API local** (`services/portal_api.py`), o que
mantém o app principal leve e seguro no Cloud (offline degrada com aviso).
Para isso a API ganhou endpoints de planejamento. Leitura de visão geral
continua no Supabase; as ações locais passam pela API (0 bytes de egress).

**Solução:**

1. **`apps/api/api_service.py`** (ambiente local, não versionado): estendeu
   `POST /gerar-txt-planos` (`estrategia`, `aula_min`, `aula_max`) e adicionou
   `GET /aulas/listar`, `POST /aulas/excluir`, `GET /painel`,
   `GET /consolidadas`, `POST /planejamento/reset`, `POST /config/set`,
   `GET /feriados`, `GET /sabados`, `GET /grade/turmas`, `GET /grade/ver` e
   `POST /grade/editar` (grade nos 3 espelhos via `core/grade.py`).
2. **`apps/api/tools/database_model.py`**: `get_all_configs` passou a aceitar
   os dois schemas da `master_config` (`key/value` novo e `chave/valor`
   legado) — o `/config/all` estava 500 no schema novo.
3. **`services/portal_api.py`**: cliente tipado para os endpoints acima e
   **correção da porta padrão** de `8000` para `8002` (a mesma do
   `api_service.py` e da Análise de Notas). `PORTAL_API_URL` continua
   sobrepondo.
4. **`views/portal.py`**: contexto turma×disciplina na sidebar e 6 seções —
   **📝 Planejar aulas** (métricas, fila, gerar planos e listar/visualizar/
   baixar/excluir `.txt`), **🚀 Registrar no Portal** (lote + progresso do
   robô), **🔄 Sincronizar** (raspagem, status e relatório/reconciliação),
   **📊 Painel / Consolidadas** (carga × registradas × faltantes + gráfico),
   **📊 Notas** (preservada) e **⚙️ Config** (feriados, data de corte,
   bloqueio de sábados, grade horária com edição e reset do planejamento).

**Validação:** `py_compile` dos 4 arquivos OK; `import views.portal` OK;
`api_service` carregou com **106 rotas** (as 13 novas presentes); endpoints
testados contra o banco real (`/aulas/listar` → 25 prontas/21 pendentes,
`/consolidadas` → 22 linhas, `/painel`, `/feriados`, `/sabados` → 18,
`/grade/turmas` → 2); `services.portal_api` callado via HTTP com a API
rodando (health, turmas, subjects, listar, consolidadas, painel, config_all,
grade) OK; `AppTest` das **6 seções** — **0 exceções** com a API **online e
offline**.

**Arquivos:** `views/portal.py`, `services/portal_api.py`; frente local (não
versionada): `apps/api/api_service.py`, `apps/api/tools/database_model.py`.

**Validar:** rodar a API local (`python apps/api/api_service.py`) → menu
**Portal** (admin/teacher) → conferir as 6 seções; com a API desligada, cada
seção mostra aviso em vez de quebrar.

---

## IS-052 — Grade semanal duplicada (`weekly_schedule`) e UNIQUE destruída 🟢

**Sintoma:** a "Grade Semanal" mostrava 2 cards por slot (o mesmo componente
repetido) marcados como *COLISÃO!*.

**Diagnóstico:** a tabela local `weekly_schedule` tinha **40 linhas / 22 slots**
(18 slots duplicados) e schema `id TEXT, ...` **sem PRIMARY KEY e sem
UNIQUE**. A nuvem (Supabase) estava correta: 22 slots, sem duplicatas, com os
mesmos horários. Causa raiz: o endpoint **`/pull-from-cloud`**
(`apps/api/backup_routes.py`) fazia `DROP TABLE` + `CREATE TABLE (... TEXT)`
para **toda** tabela sincronizada — recriava a grade sem as constraints, então
os syncs seguintes inseriam sem sobrescrever.

**Solução:**

1. **`scripts/fix_weekly_schedule.py`** (novo, versionado) — dry-run por
   padrão; com `--apply` faz backup de `data/escola_ativa.db`, reconstrói
   `weekly_schedule` com o schema canônico (`id INTEGER PRIMARY KEY
   AUTOINCREMENT`, `UNIQUE(class_name, day_of_week, time_slot)`) e reinsere a
   grade de-deduplicada. Fonte: **Supabase (soberano)** se acessível; senão,
   deduplica o local (preferindo a linha com `created_at`/`class_id`).
2. **`apps/api/backup_routes.py`** — `/pull-from-cloud` não faz mais
   `DROP TABLE`; cria só se não existir e preserva o schema existente
   (`DELETE` + insert), garantindo o índice único de `weekly_schedule`.
3. **`apps/planejamento_registro/core/grade.py`** — `_sqlite_apply` (3
   espelhos, usado pelo app 8510 e pela API) cria, de forma defensiva,
   `ux_weekly_schedule_slot` se ele não existir (auto-recuperação).

**Validação:** dry-run 40→22 (origem Supabase, 0 duplicatas na nuvem);
`--apply` gravou 22 linhas, schema com `UNIQUE` (autoindex), 0 duplicatas;
`py_compile` OK. Backup: `data/escola_ativa_backup_weekly_*.db`.

**Arquivos:** `scripts/fix_weekly_schedule.py`; frente local (não versionada):
`apps/api/backup_routes.py`. Frente do repo aninhado:
`apps/planejamento_registro/core/grade.py` → `apps/ISSUES.md` **AP-024**.

**Validar:** `python scripts/fix_weekly_schedule.py` (dry-run) → deve mostrar
0 duplicatas e schema com UNIQUE; reabrir a Grade Semanal (1 card por slot).

---

## IS-053 — Auditoria das demais tabelas afetadas por `/pull-from-cloud` 🟢

**Pedido:** o mesmo endpoint que duplicou a grade recriava **todas** as tabelas
sincronizadas como TEXT (sem PK/UNIQUE). Auditar e corrigir as demais.

**Auditoria (local × nuvem):** única tabela com dados duplicados além da grade
foi `attendance` — 2963 linhas / 2128 distintas (**835 repetições exatas**) e
`assessments` — 26 / 15 (**11 repetições**). Nuvem: `attendance` 3145 linhas
sem duplicatas; `weekly_schedule` 22 sem duplicatas. Várias tabelas perderam o
`UNIQUE`/PK sem ainda duplicar (`app_users`, `classes`, `subjects`,
`class_subjects`, `lessons`, `student_enrollments`).

**Solução — `scripts/repair_local_db.py`** (novo, versionado): dry-run por
padrão; `--apply` faz backup de `data/escola_ativa.db`, deduplica cada tabela
pela chave natural (mantendo a linha mais recente, via `ROW_NUMBER() OVER
PARTITION BY`) e (re)cria índice `UNIQUE` (`ux_<tabela>_key`), com `IFNULL` nas
colunas anuláveis. Idempotente.

**Resultado:** `attendance` 2963 → **2128** (0 dups); `assessments` 26 → **15**;
índices UNIQUE criados em `attendance`, `app_users`, `classes`, `subjects`,
`class_subjects`, `lessons`, `student_enrollments`, `historico_aulas`,
`weekly_schedule`, `turma_disciplina_config`, `assessments`,
`assessment_questions`, `quizzes`, `quiz_questions`. Backups:
`data/escola_ativa_backup_repair_*.db`.

**Pendências (não causadas por este endpoint, reportadas):**

* `student_grades` tem **schema diferente** do canônico
  (`student_name/class_name/subject/nm1..nm3`), sem as colunas
  `user_username/class_id/subject_id/trimester` — divergência anterior; as
  funções `database_model.get_students_with_grades` / `save_student_grades_batch`
  esperam o schema canônico.
* `attendance` local (2128) × nuvem (3145): divergência de conteúdo (local não
  tem ~1017 registros da nuvem) — não é duplicação; precisa de decisão de
  sincronização.

**Arquivos:** `scripts/repair_local_db.py`.

**Validar:** `python scripts/repair_local_db.py` (dry-run) → deve reportar 0
duplicatas em todas as tabelas.

---

## IS-054 — Raspagem do Portal retornava "0 cards" (filtro por turma) 🟢

**Sintoma:** em **Portal → 🔄 Sincronizar**, a raspagem logava
`Encontrados 0 cards para coletar` e `Portal: 0 registros coletados`.

**Causa:** o bot filtra os cards por **texto do `<h3>`** (`nf in
normalize_key(h3)`), esperando a sigla/nome da turma (`--turma "I-A"`). O
Portal passava o **`code`** (`turma["code"]` = `309197`), que não aparece no
nome do card → o filtro descartava todos. Além disso, o `code` como filtro
também **desabilitava a reconciliação** (`executar_raspagem` ignora
reconciliação quando há filtro de turma).

**Solução:**

1. **`apps/bots/bot_raspagem.py`** — novo `candidatos_turma()`: expande o
   filtro consultando `classes` (code ↔ name ↔ portal_name ↔ sigla) e o match
   passa a aceitar **qualquer** candidato. Passar `309197`, `I-A` ou o nome
   completo agora casa com o card. Adicionado **filtro de disciplina**
   (`candidatos_disciplina()` + `resolve_subject_alias`, match nos dois
   sentidos) e ambos os filtros aceitam **lista por vírgula** (`--turma "I-A,I-B"
   --disciplina "P.C. II,Disc.Tec."`). Sem filtro, raspa todos os cards.
2. **`views/portal.py`** (`_sincronizar`) **e** `apps/planejamento_registro`
   (`secao_registrar` / `rodar_raspagem`) — escopo **🌐 Tudo** (sem filtro,
   habilita **🧹 Reconciliar histórico**) ou **🔎 Filtrar (turma × disciplina)**,
   com `multiselect` de turmas (padrão: turma do contexto) e de disciplinas
   (padrão: contexto/todas); `rodar_raspagem` passou a montar `--turma`/
   `--disciplina`. O app 8510 era o que o usuário usava e não tinha filtros —
   por isso "raspava os 22 cards". Raspagens filtradas não reconciliam.
3. **`services/portal_api.py`** e **`apps/api/api_service.py`** (local) —
   `POST /raspagem/executar` passou a aceitar `reconciliar`, `turma` e
   `disciplina`.

**Validação:** `candidatos_turma("309197"|"I-A"|nome)` casa com o h3;
`candidatos_disciplina("P.C. II,Disc.Tec.")` filtra os cards certos; as 6
seções do Portal renderizam sem exceções (online e offline) e o modo **Filtrar**
exibe os dois `multiselect`; `py_compile` OK; 71 testes dos apps + 12 do SysAva.

**Arquivos:** `views/portal.py`, `services/portal_api.py`; frente local
(não versionada): `apps/api/api_service.py`. Frente do repo aninhado:
`apps/bots/bot_raspagem.py` → `apps/ISSUES.md` **AP-025**.

**Validar:** Portal → 🔄 Sincronizar → **Sincronizar (raspagem)** (sem marcar
"somente a turma") → log deve escanear os cards; com o filtro marcado, o log
mostra `Filtro de turma '309197' ... Candidatos: [...]` quando não casar.

---

## IS-078 — `lessons` local desatualizado vs Supabase 🟢

**Sintoma:** PROGRAMAÇÃO PARA DISPOSITIVOS MÓVEIS (subject `5`) tem **0 aulas**
no `lessons` local, mas **17** no Supabase → "🚀 Gerar planos" não produz nada
para ela, e a raspagem mostrou 0 registros no portal.

**Causa:** o gerador de planos e a API local leem `lessons` do
`data/escola_ativa.db`, que estava **desatualizado** em relação à nuvem (365
locais × 418 na nuvem; outras disciplinas também com lacunas: 8, 11, 1, 2).
O material da disciplina existe em `data/repo/.../PROGRAMAÇÃO PARA DISPOSITIVOS
MÓVEIS/S01–S04` (PDFs), mas não estava cadastrado como aula.

**Solução — `scripts/sync_lessons_from_supabase.py`** (novo, versionado):
busca as aulas no Supabase (por disciplina ou todas) e faz **upsert por `id`**
nas mesmas 14 colunas; dry-run por padrão, `--apply` faz backup.

```
python scripts/sync_lessons_from_supabase.py --subject 5          # dry-run
python scripts/sync_lessons_from_supabase.py --subject 5 --apply
python scripts/sync_lessons_from_supabase.py --all --apply        # todas
```

**Resultado:** subject `5` 0 → **17** aulas; `lessons` local 365 → **382**.
`get_lesson_content_by_number(5, n)` já resolve "Aula 1"…"Aula 17".
Depois, subject `8` (FUNDAMENTOS DE UI / UX OU IHC) 31 → **46** aulas
(Aula 26–40, incluindo os 8 seminários); `lessons` local 382 → **397**.

**Observação (subject 8):** a nuvem tem **números de Aula repetidos**
(7–12 aparecem 2×, com títulos diferentes — ex. "Protegendo sua Genialidade…"
× "A Importância dos Direitos Autorais…"). O `_ordenar_lessons_fila` do
gerador posiciona por número, então as duplicatas **desalinhavam o conteúdo**
(AULA_NUM 8 → "Aula 7", 9–10 → "Aula 8"…). O `created_at` mostrou que o
**Set B (ids 568–641, 09–25/09) é o novo**; o Set A (525–542, 28/08–03/09) é
antigo. **Correção aplicada:** removidas as 6 duplicatas antigas
(ids 530, 533, 534, 538, 540, 542) → subject 8 fica com **40 aulas (Aula
1–40) sem repetição**, e os planos foram **limpos e regenerados**:
I-A `prontas` (aulas 9–40) e I-B `pendentes` (aulas 1–40), agora **alinhados**.
Resta desalinhada só a **Aula 8 já registrada** (no histórico/portal — não
regenerável localmente). As 6 duplicatas **continuam no Supabase** (limpar
depois para não voltarem num `--all`).

**Pendências:** a janela de Programação Mobile no calendário é **06/07 a
21/08/2026** (já passou); os planos gerados sairão nessas datas. Demais
disciplinas (11, 1, 2) continuam com lacunas — usar `--all --apply`.

**Arquivos:** `scripts/sync_lessons_from_supabase.py`.

**Validar:** `python scripts/sync_lessons_from_supabase.py --subject 5`
(dry-run) → deve mostrar `novos: 0`; no app 8510, **📄 Planos → 🚀 Gerar
planos** com essa disciplina.

---

## IS-079 — Gerador: piso modular excluía os slots livres do próprio dia 🟢

**Sintoma:** em **FUNDAMENTOS DE UI / UX OU IHC** (I-A) a quarta **10/06**
ficou só com o 07:10 já registrado — os slots **08:10/11:30/13:30** não
viraram plano; a disciplina "empurrou" aulas para julho.

**Causa:** a regra do piso modular (IS-043/IS-046) usa
`limite = max(inicio_disciplina, ultima_modular)`. `inicio_disciplina` devolve
**última aula + 1 dia** (10/06 → 11/06). Como o subject 8 já tem histórico até
10/06, o piso virou 11/06 e os slots livres **do mesmo dia 10/06** foram
descartados (`antes_inicio_disciplina`). O IS-046 queria justamente esse dia
inclusivo (o caso clássico do Front-End 03/06 07:10 → Fundamentos 08:10), mas
a regra só funcionava para a disciplina *seguinte* (sem histórico), não para
uma que já tem registros.

**Solução (`core/gerador.py`):** para disciplinas modulares/genéricas, o piso
passa a ser **inclusivo**: recua 1 dia do `limite` (clamp no corte) e mantém o
maior com o piso modular da turma. Assim os slots livres do dia da última aula
voltam a ser usados.

**Resultado:** regenerados os planos de Fundamentos UI — I-A `prontas` (aulas
9–40, agora com **10/06 08:10/11:30/13:30**) e I-B `pendentes` (aulas 1–40),
todos alinhados (`AULA_NUM` = conteúdo). 71 + 12 testes OK.

**Arquivos:** `apps/planejamento_registro/core/gerador.py` (repo aninhado) →
`apps/ISSUES.md` **AP-026**.

**Validar:** regenerar a disciplina (`Sobrescrever`) e conferir que a quarta
da última aula registrada volta a receber os slots vagos.

---

## IS-080 — Cesta de chamadas (rateio proporcional da frequência) 🟡

**Contexto:** as disciplinas modulares foram ministradas em datas **reais**
(ago/set) sob uma grade que **mudou** (ex.: I-A Qua 2→4, Sex 3→1). Ao registrar
planos com datas **compensadas** (jun), a frequência real precisa ser redistribuída
sem beneficiar/prejudicar por causa da troca de grade — "peso da Falta = peso do
Presente".

**Solução (parcial — core pronto):** `apps/planejamento_registro/core/cesta.py`
(novo, compartilhado app+API):

* **Peso** de cada chamada = nº de aulas genéricas ("Disc.Tec.") do dia da semana
  na **grade real** — recuperada do backup mais antigo
  `aulas/_backup_is*/grade_horaria_*.json`; fallback: `weekly_schedule`.
* Expande as chamadas pelo peso real → **cesta**; se faltar chamada, **duplica a
  semana** até fechar a carga; se sobrar, corta.
* Lista negra (RA/nome em `data/excecoes_alunos.json`) sempre **Falta**.
* `montar_cesta(...)` e `revisao(...)` (resumo por aluno: faltas, presenças, %).

**Validação:** I-A → peso real `{Seg 2, Ter 1, Qua 2, Sex 3}` (fonte backup
IS-044), 17 chamadas + duplicação → cesta **40**; I-B → `{Seg 2, Qui 5, Sex 1}`,
10 chamadas + duplicação → cesta **40**. `py_compile` OK.

**Pendências (🟡):**
1. **Tela de revisão** no app (por aluno/semana) antes de gerar.
2. **Hook no gerador**: usar a cesta quando gerar **>2 planos** por disciplina
   (anuais seguem normal), gravando `[FREQUENCIA]`.
3. **Histórico de grades**: gravar a grade vigente a cada mudança (para a cesta
   achar a grade da época no futuro, sem depender de backup).
4. **Seminários**: 3 dias faltantes entram como presença (menos lista negra);
   decisão caso a caso no portal.

**Arquivos:** `apps/planejamento_registro/core/cesta.py` → `apps/ISSUES.md`
**AP-027**.

---

## IS-055 — Monitor de laboratório: bloqueio manual expandido de jogos 🟢

**Pedido:** ampliar o bloqueio do painel de intervenção para plataformas de jogos
além do Roblox — incluindo sites/proxies abertos no navegador (ex.: **Loki**).

**Solução:**
- `lab_agent.py` (e o agente embutido em `lab_agent.ps1`): listas
  `BLOCKED_PROCESS_KEYWORDS` (robôs instalados: Roblox, League of Legends),
  `BLOCKED_SITE_KEYWORDS` (sites/proxies: Loki, Poki, Friv, Y8, ClickJogos,
  Gartic...) e `BROWSER_PROCESS_KEYWORDS`. Novas funções `kill_game_processes`,
  `close_blocked_sites` (fecha a janela do navegador pelo título via
  `pygetwindow`), `close_browsers` e `block_games`.
- `get_category()` passou a reconhecer os sites bloqueados como **Games**.
- Comandos tratados: `Bloquear Jogos` (antes só `Bloquear Processo`/Roblox),
  `Bloquear Navegador` (existia no painel mas não no agente) e `Forçar Logoff`
  (idem).
- `lab_monitor.py`: ação renomeada para **Bloquear Jogos (Fechar
  Roblox/Loki/Games)**, aviso das plataformas-alvo e expander informativo do
  modo via `hosts`.

**Arquivos:** `data/repo/plugins/lab_agent.py`, `data/repo/plugins/lab_agent.ps1`,
`data/repo/plugins/lab_monitor.py`

**Validar:** `python -m py_compile` no agente e o gerado pelo `.ps1`; escolher
uma máquina com Roblox ou com o Loki aberto no navegador e acionar **Bloquear
Jogos** — o processo/aba deve fechar e o log registrar `Bloqueio de jogos -> ...`.

---

## IS-056 — Monitor: modo não invasivo (bloqueio via arquivo `hosts`) 🟢

**Pedido:** opção de bloqueio para PCs onde não é possível instalar o agente, sem
nenhuma instalação.

**Solução:** script standalone **`bloquear_hosts.ps1`** + atalho
**`bloquear_hosts.bat`** (duplo-clique, pede Administrador). Aplica/remove um
bloco marcado (`# === SysAva Bloqueio de Jogos ===`) no arquivo `hosts` do
Windows, redirecionando os domínios do Roblox para `0.0.0.0` e limpando o cache
DNS (`ipconfig /flushdns`). É **idempotente** (não duplica linhas) e
**reversível** (`-Revert`, ou opção **[2] Remover** no `.bat`). A lista fica em
`$Dominios` (padrão: somente Roblox); domínios extras podem ser adicionados por um
`dominios_extra.txt` (um por linha) — caminho pensado para incluir o Loki depois.

**Arquivos:** `data/repo/plugins/bloquear_hosts.ps1`,
`data/repo/plugins/bloquear_hosts.bat`

**Validar:** rodar o `.bat` → **[1] Aplicar**: `hosts` ganha o bloco e o Roblox
para de conectar; rodar de novo não duplica; **[2] Remover** devolve o arquivo
original. Teste de lógica (aplicar 3x / reverter) confirmou idempotência.

---

## IS-057 — Monitor: descoberta robusta do servidor (cache + UDP) 🟢

**Contexto:** a rede do laboratório tem "switch rigoroso" e IP dinâmico. A
investigação na rede real mostrou:
- Sub-rede real é **`192.168.10.0/23`** (máscara `255.255.254.0`), gateway/DHCP
  `192.168.10.1`; o servidor (notebook do professor) pegou **`192.168.11.253`**
  por DHCP (lease ~3h).
- O `KNOWN_SERVER_IP = 192.168.11.249` do agente estava **obsoleto**: `.249` agora
  é um PC do lab (ASRock); os desktops do lab são MACs `A8:A1:59` (ASRock).
- Firewall do servidor **libera `python.exe`** no perfil Público → TCP 5000 ok.
- Unicast cliente↔cliente funciona (SMB do `192.168.11.112` acessível).
- `netstat` confirmou o receiver **parado** no momento da coleta.

**Solução (descoberta em camadas, sem depender de IP fixo):**
1. **Cache local** `server_cache.txt` (ao lado do agente): a última URL que
   funcionou é tentada primeiro e revalidada por `/health`.
2. **Broadcast UDP** na porta **5001**: o agente envia `SYSAVA_DISCOVER` para
   `255.255.255.255`, broadcast da sub-rede e `192.168.10/11.255`; o receiver
   responde `SYSAVA_SERVER <ip>:5000` e o agente valida por HTTP.
3. Fallback mantido: MAC/ARP → IP conhecido → varredura da sub-rede.

**Arquivos:** `data/repo/plugins/lab_agent.py`,
`data/repo/plugins/lab_agent.ps1` (agente embutido),
`data/repo/plugins/lab_receiver.py` (thread `run_udp_discovery`)

**Validar:** subir o receiver e rodar o round-trip UDP — respondido
`SYSAVA_SERVER 192.168.11.253:5000` com o IP correto; `discover_server_udp()`
retornou a URL; `load/save_cached_server` idempotente. Se `netstat` não mostrar
UDP 5001 no servidor, verifique firewall (regra de programa do `python.exe`).
Substituir o IP fixo por **reserva DHCP** no roteador é recomendado como reforço.

---

## IS-058 — Monitor: servidor de instalação/atualização pela rede (sem pendrive) 🟢

**Pedido:** sem pendrive, digitar um endereço no cliente para baixar/atualizar o
agente e os utilitários.

**Solução:** rotas novas no `lab_receiver.py` (mesmo servidor do radar):
- `GET /setup` (e `/instalar`): página de instruções com o IP detectado e links.
- `GET /download/<arquivo>`: entrega **apenas** os arquivos de uma whitelist
  (`lab_agent.ps1`, `bloquear_hosts.ps1`, `bloquear_hosts.bat`) — protege contra
  path traversal.
- `GET /instalar_agente.bat` e `/instalar_hosts.bat`: geram na hora um `.bat` que
  baixa o script **deste** servidor (IP/porta do request) e o executa como
  Administrador. Como os arquivos vêm do disco a cada request, rebaixar = atualizar.
- Link para `/setup` adicionado ao dashboard (`/`).
- `lab_agent.ps1`: antes de iniciar, **encerra instâncias anteriores** do agente
  (`lab_agent.py`) para uma atualização limpa.
- `lab_receiver.bat`: passou a criar também a regra de firewall **UDP 5001**.

**Arquivos:** `data/repo/plugins/lab_receiver.py`,
`data/repo/plugins/lab_receiver.bat`, `data/repo/plugins/lab_agent.ps1`,
`servidor_instalacao.bat` (raiz — atalho que sobe o receiver, cria firewall
TCP 5000/UDP 5001, mostra o IP e a URL `/setup`, e não duplica se já estiver no ar)

**Validar:** com o receiver no ar, abrir `http://<ip>:5000/setup` no cliente e
usar os botões de download. Teste via Flask test client: `/setup`, `/download/*`,
`/instalar_agente.bat`, `/instalar_hosts.bat` retornam 200; o `.bat` gerado contém
a URL do servidor.

---

## IS-059 — Monitor: agente em SYSTEM relança na sessão ativa do aluno 🟢

**Sintoma:** máquinas apareciam no radar com `user: SYSTEM` e "Janela Ativa:
Administrador: Windows PowerShell". Como o agente rodava como **SYSTEM (sessão 0)**,
ele não enxergava a janela/aplicações do aluno — a atividade e a categoria saíam
distorcidas.

**Solução:** em `lab_agent.py` e no agente embutido do `lab_agent.ps1`:
- Detecção: `is_system_process()` + comparação da sessão atual (`ProcessIdToSessionId`)
  com a sessão de console ativa (`WTSGetActiveConsoleSessionId`).
- Se for SYSTEM fora da sessão ativa, `WTSQueryUserToken` → `DuplicateTokenEx` →
  `CreateEnvironmentBlock` → `CreateProcessAsUserW` inicia uma cópia do agente na
  **sessão do usuário** (`lpDesktop = winsta0\\default`), e a cópia de sistema encerra.
- Guarda `--session-agent` no argv evita relançamento em loop.

**Arquivos:** `data/repo/plugins/lab_agent.py`, `data/repo/plugins/lab_agent.ps1`

**Validar:** rodar o agente como SYSTEM numa máquina com usuário logado — o log deve
registrar `Agente relancado na sessao ativa N`; o radar deve passar a mostrar o
usuário real e a janela do aluno. Em sessão normal (não-SYSTEM) nada muda
(testado localmente: `is_system_process=False`, `relaunch=False`).
**Limite:** se o aluno não for admin, comandos privilegiados (desligar/reiniciar)
podem falhar — a cópia herda o token do usuário.

---

## IS-060 — Monitor: massa, Bloquear Sites e hosts com redes sociais 🟢

**Pedido:** ter "selecionar todas", desligar/reiniciar todas em um clique, e
bloquear YouTube/Instagram (que não eram cobertos).

**Solução:**
- `lab_monitor.py`: checkbox **Selecionar TODAS as máquinas** no painel de comando;
  novo expansor **⚡ Ações em Massa** com **Desligar TODAS**, **Reiniciar TODAS** e
  **Bloquear Sites em TODAS** (com confirmação); helper `_enfileirar_comando()`
  evita duplicar a lógica de comando; nova ação **Bloquear Sites
  (YouTube/Instagram/TikTok/Facebook)**.
- `lab_agent.py` (+ embutido no `.ps1`): `BLOCKED_SOCIAL_KEYWORDS` e
  `close_social_sites()` (generalização de `close_windows_by_keywords`); trata o
  comando **Bloquear Sites** fechando só as janelas desses sites.
- `bloquear_hosts.ps1`: `$DominiosSociais` + parâmetro **`-Sociais`**; `.bat` com
  menu **[1] Roblox / [2] Roblox + Redes Sociais / [3] Remover**.

**Arquivos:** `data/repo/plugins/lab_monitor.py`,
`data/repo/plugins/lab_agent.py`, `data/repo/plugins/lab_agent.ps1`,
`data/repo/plugins/bloquear_hosts.ps1`, `data/repo/plugins/bloquear_hosts.bat`

**Validar:** marcar "Selecionar TODAS" e enviar um Alerta; usar as Ações em Massa
(exige confirmação); "Bloquear Sites" fecha só abas de redes sociais; no hosts,
`-Sociais` inclui youtube/instagram (merge testado). `py_compile` + parse do `.ps1`
+ Python embutido OK.

---

## IS-061 — Monitor: rótulos amigáveis por máquina 🟢

**Pedido:** identificar facilmente os PCs (hostnames como `22139923-LAB-70006` são
difíceis). Atribuir nomes como `PC1-Fila1`, `PC4-Fila4`, `PC5-Fila3`.

**Solução:** novo `lab_labels.json` (mapa hostname → rótulo) e em `lab_monitor.py`:
- `load_labels()`/`save_labels()`; coluna **Rotulo** como 1ª da tabela ao vivo
  (`Máquina (host)` continua como coluna secundária).
- Expander **🏷️ Rótulos das máquinas** (form) edita os rótulos, inclusive de PCs
  offline (união das máquinas online + rótulos já salvos); campo vazio remove.
- As listas de seleção/target e a mensagem de sucesso passam a exibir o rótulo.

Rótulos já pré-carregados: `22139923-LAB-70006→PC4-Fila4`,
`22139923-LAB-80054→PC5-Fila3`, `DESKTOP-7H3URJE→PC1-Fila1`.

**Arquivos:** `data/repo/plugins/lab_monitor.py`,
`data/repo/plugins/lab_labels.json`

**Validar:** Plugins → Monitor: a tabela mostra a coluna **Rótulo** e o expander
permite editar/salvar; `py_compile` OK.

---

## IS-062 — Tela de bloqueio + papel de parede do SysAva 🟢

**Pedido:** PCs iniciarem com a marca do SysAva e uma tela de bloqueio que já abre
o `sysava.streamlit.app`, com desbloqueio pelo login do SysAva (RA).

**Solução:**
- **Marca**: `gerar_logo_sysava.py` (Pillow) gera `logo_sysava.png` (512×512) e
  `wallpaper_sysava.png` (1920×1080) com a identidade SysAva.
- **Papel de parede**: `aplicar_papel_parede.ps1` (HKCU + `PersonalizationCSP` p/
  tela de bloqueio com admin).
- **Tela de bloqueio**: `sysava_lock.ps1` (WinForms fullscreen, topmost) — fundo com
  a marca, abre o `sysava.streamlit.app` e pede o **RA**; valida em
  `/api/auth_ra` do receiver; libera em modo offline se o servidor não responder.
- **Receiver**: endpoint `GET /api/auth_ra?ra=...` (consulta `services.database.get_user`,
  login = RA, com cache em memória); whitelist de download ampliada; card **3** em
  `/setup`; rota `/instalar_tela.bat` (o `.bat` gerado passa `-Server`).
- **Instalador**: `instalar_tela_sysava.ps1` baixa os arquivos p/
  `C:\ProgramData\SysAva`, aplica o papel de parede e registra a tarefa
  **"SysAva Lock"** no logon (`BUILTIN\Users`); `-Remover` desinstala.

**Arquivos:** `data/repo/plugins/gerar_logo_sysava.py`,
`logo_sysava.png`, `wallpaper_sysava.png`, `aplicar_papel_parede.ps1`,
`sysava_lock.ps1`, `instalar_tela_sysava.ps1`, `lab_receiver.py`

**Validar:** `/api/auth_ra?ra=` → 400 e RA inexistente → 404 (test client);
descoberta em PowerShell retornou `http://192.168.10.161:5000`; `/setup` e
`/download/*` 200; `py_compile` + parse dos `.ps1` OK.

**Limite:** bloqueio leve (Alt+F4/Task Manager fecham); sem senha (só RA). Evolução
possível: kiosk rígido e/ou exigir senha.

---

## IS-063 — Associar o aluno ao PC pela tela de bloqueio 🟢

**Pedido:** aproveitar o RA digitado no desbloqueio para saber qual aluno está em
qual PC (o agente reporta `user: SYSTEM`, sem identificar o aluno).

**Solução:**
- `lab_receiver.py`: `_associar_usuario_maquina()` grava `lab_users.json`
  (`máquina → {ra, name, ts}`); `/api/auth_ra` passou a aceitar `&maquina=` e, ao
  validar o RA, registra a associação (sem custo extra no banco).
- `sysava_lock.ps1`: envia `$env:COMPUTERNAME` na validação.
- `lab_monitor.py`: `load_users_map()` + coluna **Aluno (RA)** (coluna `Conta Win`
  para o usuário do Windows do agente).

**Arquivos:** `data/repo/plugins/lab_receiver.py`,
`data/repo/plugins/sysava_lock.ps1`, `data/repo/plugins/lab_monitor.py`

**Validar:** chamar `/api/auth_ra?ra=<valido>&maquina=PC1` grava a associação em
`lab_users.json`; o radar mostra "Aluno (RA)". Teste da função de gravação OK e
`py_compile` OK.

**Histórico (IS-063, ampliação):** ao associar, grava
`db.add_user_history(ra, "Entrou no <Rótulo> (tela de bloqueio)")`, **deduplicado
por aluno/máquina/dia** (campo `logged_date` em `lab_users.json`) para não pesar no
egress. Teste com `db` simulado: 1ª vez grava, repetição no mesmo dia não grava,
RA diferente grava.

---

## IS-064 — Agente sumia do radar após reiniciar (auto-start) 🟢

**Sintoma:** "PC1-Fila1 está ligado e não aparece". `/api/debug` mostrou o
`ram_cache` vazio (nenhum agente reportando). As máquinas haviam sido
desligadas/reiniciadas nos testes.

**Causa:** o instalador **iniciava o agente uma única vez**, sem persistência — não
havia chave Run/pasta Startup/tarefa. Depois de reboot/shutdown o agente não voltava
(alguns scripts do projeto mexem em hosts/firewall, mas **nenhum** no autostart).

**Solução:** `lab_agent.ps1`, passo **5b**, registra a tarefa agendada
**“SysAva Agent”** (`AtLogOn`, `BUILTIN\Users`, `RunLevel Limited`) rodando
`pythonw.exe lab_agent.py` (fallback `python.exe`). `Register-ScheduledTask -Force`
torna idempotente.

**Bug encontrado na 1ª versão:** `New-ScheduledTaskPrincipal -GroupId ... -LogonType
Group` falha com *"O conjunto de parâmetros não pode ser resolvido"* (`-LogonType`
só existe no parameter set de `-UserId`). O instalador caía no `catch` e avisava que
**não** agendaria. **Correção:** remover `-LogonType Group` (idem em
`instalar_tela_sysava.ps1`); adicionado fallback via **pasta Startup comum**
(`SysAva Agent.vbs` com `WScript.Shell.Run ..., 0, False`) caso a tarefa falhe.

**Arquivos:** `data/repo/plugins/lab_agent.ps1`,
`data/repo/plugins/instalar_tela_sysava.ps1`

**Validar:** re-executar o instalador (`/setup` → `instalar_agente.bat`), reiniciar a
máquina e conferir que o agente volta e aparece no radar. `schtasks /query /tn "SysAva
Agent"` deve listar a tarefa. Parse do `.ps1` + Python embutido OK.

**Nota para o operador:** máquinas instaladas antes deste ajuste precisam
**re-rodar o instalador** para ganhar o autostart.

---

## IS-065 — Curso Técnico de Marketing (professora/turma/disciplinas/alunos) 🟢

**Pedido:** criar login da professora (Adriana), a turma e disciplinas de Marketing,
e matricular os alunos. Dúvida: o schema tem "curso"? (não) e onde ficam dados do
professor.

**Diagnóstico:** não há coluna de **curso** (o curso é implícito no
`classes.name`/`official_name`/`portal_name`); não há vínculo professor↔turma;
`get_classes()` retorna todas as turmas; dados do professor = só `app_users.name`/`ra`.

**Decisão:** rótulo de curso por **convenção de nome** (sem migração) + script de
criação. Novo `scripts/criar_turma_professor.py` (dry-run por padrão, `--apply`) —
espelha `seed_data.py`/`seed_students.py` (MockSecrets + `.env`).

**Executado (`--apply`):**
- Professora `adriana` (name=[PROFESSORA], ra=CPF `[RA]`,
  role=teacher, senha inicial = RA).
- Turma `312076` → `classes.id=3`: name `1ª SÉRIE - Turma I-B (Técnico Marketing)`,
  `official_name=EMTPMARK-DIG-1ª SERIE - INTEGRAL-I-B`, `portal_name=...1a SERIE...`.
- Disciplinas: E-COMMERCE(36), GESTÃO ESTRATÉGICA DE REDES SOCIAIS(37),
  PRODUÇÃO DE CONTEÚDO DIGITAL(38), FUNDAMENTOS DA ADMINISTRAÇÃO(39), FUNDAMENTOS
  DO MARKETING(40) e **INTELIGÊNCIA ARTIFICIAL(11, compartilhada com o DS)** — todas
  vinculadas à turma.
- 25 alunos criados (username=RA, senha=RA) e matriculados.

**Arquivos:** `scripts/criar_turma_professor.py`

**Validar:** `db.get_class_by_code("312076")` → id 3; `get_subjects_for_class(3)` → 6;
`get_students_by_class(3)` → 25; `get_user("adriana")` role=teacher. Dry-run confere
tudo antes de gravar.

**Pendente (combinado):** **filtro por professor** (novo) — criar vínculo
professor↔turma e fazer `get_classes()` respeitar o docente logado (admin vê tudo).

---

## IS-066 — Filtro por professor (isolamento de turmas) 🟢

**Pedido:** cada professor vê só as turmas dele; admin vê tudo.

**Limitação encontrada:** só existe a chave **anon** do Supabase no `.env` (PostgREST
não faz DDL) — **não é possível criar tabela** pela aplicação. Optou-se por um
**mapeamento local** `data/professores_turmas.json` (`username → [codigos de turma]`),
consistente com os demais espelhos JSON do projeto.

**Solução (centralizada, sem tocar em cada tela):**
- `services/database.py`: `_current_teacher_scope()` (lê `st.session_state` role/username;
  fora do Streamlit → `None`) e `_load_teacher_map()` (lê o JSON).
- `get_classes()` aplica o filtro **depois** do cache: se o professor logado está no
  mapa, retorna só as turmas dele; **admin/script** (`None`) e **professor sem mapa**
  continuam vendo tudo (sem regressão para `heliol`).
- Como plugins e telas chamam `db.get_classes()`, o filtro vale em todo o app.
- Conteúdo do mapa: `{ "adriana": ["312076"] }`.

**Arquivos:** `services/database.py`, `data/professores_turmas.json`

**Validar (com db real):** sem escopo → 3 turmas; `adriana` → só `312076`; `heliol`
(sem mapa) → 3 turmas. `py_compile` OK.

**Upgrade opcional (tabela no Supabase):** quando houver a chave de serviço/Editor SQL,
rodar e aí eu ligo o código na tabela:
```sql
CREATE TABLE IF NOT EXISTS class_teachers (
    id BIGSERIAL PRIMARY KEY,
    class_id BIGINT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    username TEXT NOT NULL REFERENCES app_users(username) ON DELETE CASCADE,
    UNIQUE (class_id, username)
);
INSERT INTO class_teachers (class_id, username)
SELECT id, 'adriana' FROM classes WHERE code = '312076'
ON CONFLICT DO NOTHING;
```

---

## IS-067 — Login tolerante (RA/CPF e maiúsculas) 🟢

**Sintoma:** a professora `adriana` não conseguia logar. Diagnóstico: a conta está
correta (`check_password("[RA]", hash)=True`, `is_active=True`, `role=teacher`);
`get_user` é case-sensitive e usa só `username` — o CPF (RA) não era aceito.

**Solução:** `views/login.py` passou a tentar, em ordem: `get_user(user)` →
`get_user_by_ra(user)` → `get_user_ci(user)`; o `username` real é assumido na sessão
(importante para o filtro por professor). Novas funções em `services/database.py`:
`get_user_by_ra` (coluna `ra`) e `get_user_ci` (`ilike`, sem diferenciar caixa).

**Arquivos:** `services/database.py`, `views/login.py`

**Validar:** login OK com `adriana`, `Adriana`, `ADRIANA` e `[RA]` (senha =
`[RA]`). `py_compile` OK.

**Atenção:** o fallback é código novo — só vale no app local (ou após redeploy no
Cloud). De todo modo, `adriana` + senha já funcionavam no banco.

---

## IS-068 — Tela de bloqueio não travava no logon (autostart) 🟢

**Sintoma:** depois de instalar a tela de bloqueio, o PC continuava **liberado** (só
o papel de parede mudava). A tela não aparecia no logon.

**Causa:** o `instalar_tela_sysava.ps1` registrava **só** uma tarefa agendada — e a
versão instalada ainda tinha o bug `New-ScheduledTaskPrincipal -GroupId ... -LogonType
Group` (IS‑064), que **falha** e aborta o registro. Resultado: nenhuma inicialização
no logon.

**Solução:** o instalador passou a registrar a tela via **pasta Startup comum**
(`C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\SysAva Lock.vbs`, que
roda no logon de qualquer usuário, oculto), com a **tarefa agendada como fallback**
(parâmetro corrigido). O `-Remover` limpa a tarefa e o VBS. Mensagem final mostra
como **testar agora** rodando o `sysava_lock.ps1` direto.

**Arquivos:** `data/repo/plugins/instalar_tela_sysava.ps1`

**Validar:** reinstalar (`/setup` → card 3 → `instalar_tela.bat`), fazer logoff e
confirmar a tela; ou rodar `powershell -File C:\ProgramData\SysAva\sysava_lock.ps1`
para ver na hora. Parse do `.ps1` OK.

---

## IS-069 — Estrutura de pastas turma/disciplina/aluno/aula XX 🟢

**Pedido:** gerar a árvore `Escola / Turma / Disciplina / Aluno / Aula XX` em cada
PC, com as aulas por **intervalo fixo** (via agente).

**Solução:** a ação **"Estruturar Pastas de Projetos"** do agente passou a aceitar um
**5º campo** com o intervalo de aulas:
- Monitor (`lab_monitor.py`): ao escolher a ação, aparece o campo **"Aulas (ex.: 1-32
  ou 32)"**; a mensagem vira `escola|turma|disciplina|aluno|<aulas>`.
- Agente (`lab_agent.py` + embutido no `lab_agent.ps1`): `_parse_aula_range("32"|"1-32")`
  e cria `C:\Projetos\<Escola>\<Turma>\<Disciplina>\<Aluno>\Aula 01..NN`
  (`os.makedirs(..., exist_ok=True)` — idempotente).

**Arquivos:** `data/repo/plugins/lab_agent.py`,
`data/repo/plugins/lab_agent.ps1`, `data/repo/plugins/lab_monitor.py`

**Validar:** `_parse_aula_range("32")` → 1..32; `"1-5"` → 1..5; `""` → []. `py_compile`
+ parse do `.ps1` + Python embutido OK. **Clientes precisam re-rodar o instalador**
para baixar o agente novo (o código é embutido no `lab_agent.ps1`).

---

## IS-073 — Painel web do receiver com login e controles 🟢

**Pedido:** melhorar a página `http://<ip>:5000/` com **login do professor** e
**controles via HTTP** (sem abrir o Streamlit).

**Solução (em `lab_receiver.py`):**
- **Login** (`/login`, `/logout`): valida contra o SysAva
  (`get_user`/`get_user_by_ra`/`get_user_ci` + `auth.check_password`) exigindo
  `role` teacher/admin; sessão por cookie assinado (`app.secret_key` persistida em
  `receiver_secret.key`). `/` e `/diagnostics` passam a exigir login (`login_required`).
- **Controles** (`POST /control`): o dashboard ganhou **checkboxes por máquina**,
  select de **ação** (as mesmas do plugin: alerta, bloquear jogos/sites/anônimos/
  navegador, deslogar, desligar, reiniciar) e campo de mensagem; grava
  `pending_command` no `lab_status.json` — o agente recebe no próximo `/ping`.
- Dashboard mostra o **usuário logado**, **Sair**, links para `/setup` e atualizar,
  e mensagens de sucesso/erro. As APIs do agente (`/ping`, `/health`, `/api/*`,
  `/scan`, `/download`, `/setup`) seguem **abertas** (não autenticáveis por máquina).

**Arquivos:** `data/repo/plugins/lab_receiver.py`

**Validar (test client):** `/` sem login → 302 → `/login`; senha errada → mensagem;
`adriana`/senha → 302 → `/`; logado → 200 com o form de controle. HTTP real: 302 e
`/login` 200. Receiver reiniciado OK.

---

## IS-074 — Receiver não carregava `.env` (login/`auth_ra` sempre falhavam) 🟢

**Sintoma:** o login do painel web (`/login`) sempre dizia "Usuário ou senha
inválidos"; a validação de RA da tela de bloqueio (`/api/auth_ra`) também não achava
ninguém.

**Diagnóstico:** o receiver roda **fora do Streamlit** (`lab_receiver.py`), e
`services.database` busca `SUPABASE_URL/KEY` em `st.secrets` e, na falta, em
variáveis de ambiente. Como o `.env` **não** era carregado e o processo inicia com
`cwd = data/repo/plugins`, as credenciais não existiam → `is_db_connected()` falso →
`get_user()` sempre `None`. (Nos testes via script o `cwd` era a raiz e o
`st.secrets`/`.env` era encontrado — daí parecer que funcionava.) O `/api/auth_ra`
retornava 404 "RA não encontrado" mesmo com RA válido (mesma resposta do
não-conectado), mascarando o problema.

**Solução:** no topo do `lab_receiver.py`, `load_dotenv(PROJECT_ROOT/.env)` (com
`python-dotenv`) + inserir `PROJECT_ROOT` no `sys.path`. Além disso, o login passou a
**registrar o motivo da falha** (`usuario nao encontrado` / `senha invalida` /
`sem permissao`).

**Arquivo:** `data/repo/plugins/lab_receiver.py`

**Validar:** `/api/auth_ra?ra=adriana` → `{"ok":true,...}`; `POST /login` com
`adriana`/senha → 302 e log `LOGIN PAINEL: adriana`. Reiniciar o receiver após
alterar credenciais.

---

## IS-070 — (Backlog) Instaladores de ferramentas por disciplina ⚪

Pacotes prontos instaláveis pelo agente (winget), por disciplina: ex. **kit dev
mobile** (Android SDK/emulador, Flutter, Node), design (Figma/Canva), marketing
(ferramentas de edição), etc. Já existe "Instalar Kit Lab DS" (VS Code, JDK, Node,
NetBeans) — generalizar para uma **lista por disciplina** escolhida no painel.

## IS-071 — Log de atividade dos usuários + relatório HTML 🟢

Registrar **o que cada usuário fez e quando** no sistema, com um local para consultar,
e — se possível — o **histórico do navegador**. Relatórios em `.log`/`.html` numa
**pasta oculta** na pasta do monitor.

Pontos a considerar (quando implementar):
- **Já existe** base para reaproveitar: `lab_receiver.log` (eventos/mudanças de
  estado), `lab_status.json`, `db.add_user_history` (login/entradas) e o "Histórico
  de Desvios" do plugin Monitor.
- **Servidor (Streamlit):** logar navegação/ações por usuário (página, timestamp,
  IP) — ex. middleware em `app.py` + persistência local.
- **Agente (PCs):** coletar o histórico do navegador (Chrome/Edge: `History` SQLite
  em `%LocalAppData%`, copiando o arquivo pois fica travado com o navegador aberto)
  e enviar esporadicamente (evitar egress em excesso).
- **Armazenamento:** pasta oculta na pasta do monitor (ex.:
  `data/repo/plugins/.relatorios/` — nome com `.` e/ou atributo *hidden* do Windows),
  com relatórios `.log` (texto) e `.html` (navegável).
- **Privacidade/legal:** histórico de navegador é dado sensível — precisa de
  finalidade/consentimento escolar; documentar e limitar o escopo.

**IMPLEMENTADO (completo):**
- Novo `audit_log` (em `services/` **e** cópia portátil em `data/repo/plugins/`): grava
  eventos em **JSON-lines diário** em pasta **oculta** `.relatorios/`
  (`atividade-AAAA-MM-DD.log` e `historico-AAAA-MM-DD.log`), com `registrar()`,
  `registrar_historico()`, `ler()`, `gerar_html()`. Sem rede (não afeta egress).
- **Ganchos:** `app.py` registra **navegação** (1x por troca de página, com IP) e
  **logout**; `views/login.py` registra **Login**.
- **Histórico do navegador:** o **agente** lê Chrome/Edge (`%LocalAppData%\...\History`,
  copiando o arquivo por estar travado) a cada ~180s e envia para **`POST /api/historico`**;
  o receiver grava via `audit_log.registrar_historico()`.
- **Consulta:** rota **`/relatorios`** (login) renderiza o HTML com **duas tabelas**
  (atividade + histórico do navegador); link **📋 Relatórios** no dashboard.

**Residual (opcional):** filtros por dia/usuário na tela e retenção/limpeza automática
dos logs (definir política).

**Validar:** `registrar()` cria a pasta **Hidden** e grava; `gerar_html()` monta as
tabelas; `/api/historico` recebe e grava; `/relatorios` sem login → 302, logado → 200.
`py_compile` OK. **Reinstalar o agente** para ele começar a enviar o histórico.

## IS-072 — (Backlog) Proteção do aluno: categorias perigosas + Tor/dark web ⚪

**Contexto:** preocupação de proteção (risco criminal/emocional). Além das redes
sociais (bloqueadas quando houver excesso), o foco é **conteúdo adulto, sites
perigosos, dark web e outros riscos**. Nas redes sociais há maior exposição e não dá
para acompanhar tudo manualmente — daí a automação de **detecção + alerta**.

**Abordagem em camadas (a definir):**
1. **Filtro de rede por categoria (recomendado):** trocar o DNS do laboratório por um
   DNS de família/filtro (ex.: família Cloudflare `1.1.1.3`/`1.1.1.2`, OpenDNS
   FamilyShield) ou um DNS local com listas de categorias (NextDNS/Pi‑hole + listas
   como StevenBlack/UT1). Pega adulto/malware/phishing **sem tocar em cada PC**.
2. **Bloqueio por hosts nas máquinas (complemento):** estender `bloquear_hosts.ps1`
   com **listas por categoria** (adulto, apostas, malware, proxy/VPN/anônimos).
3. **Dark web / Tor:** `.onion` exige Tor — inacessível na rede normal. O foco é
   **detectar/bloquear Tor** (`tor.exe`, bridges, I2P) e **alertar**.
4. **Detecção e alerta (safeguarding):** o agente sinaliza categorias de risco
   (adulto, automutilação/violência, Tor) e o painel **alerta o responsável** — não
   só bloqueio silencioso. Combina com IS‑071 (logs/relatórios).
5. **Ação humana:** alerta → pedagógico/apoio; manter registro discreto.

**Cuidados obrigatórios:** finalizar por **autorização da escola/responsáveis** e
**finalidade declarada**; guardar relatórios com acesso restrito; não é vigilância
genérica — é proteção. Definir retenção e quem vê.

**REGRA (decidida) — política de tiers (implementar amanhã, no laboratório):**

| Tipo | Ação | Alerta ao professor |
|---|---|---|
| Adulto/pornografia, malware/phishing, apostas, Tor/anônimos/VPN de evasão | **Bloqueia automático** (silencioso) | **Não** — só log |
| Redes sociais e jogos/streaming em **excesso** | **Sugere bloquear** (professor aciona) | Sim (agrupado por limiar) |
| Risco emocional (automutilação, violência) e criminal (aliciamento) | **Bloqueia + destaca** | **Prioritário e discreto** |
| Qualquer ocorrência | **Registra** (log/relatório) | — |

Regras de implementação:
- **Evitar fadiga de alerta:** Tier 1 **não** alerta por evento (só grava); Tiers 2/3
  agrupam por limiar (ex.: N acessos ou X min no período) antes de notificar.
- **Tier 1 (base técnica):** DNS de filtro (família Cloudflare `1.1.1.3`/`1.1.1.2`,
  OpenDNS FamilyShield) ou DNS local com categorias **+** `bloquear_hosts.ps1`
  estendido com listas por categoria (adulto/apostas/malware/anônimos).
- **Tor/dark web:** `.onion` não acessa na rede normal; **detectar/bloquear** `tor.exe`,
  bridges e I2P; alertar.
- **Tiers 2/3 (base técnica):** o **agente** classifica por janela ativa/histórico do
  navegador e sinaliza a categoria; o **painel do Monitor** mostra e permite a ação
  ("Bloquear Sites/Navegador"), com alerta destacado no Tier 3.
- **Log/registro:** o que/quando/quem/máquina/categoria; pasta **oculta** na pasta do
  monitor (ex.: `data/repo/plugins/.relatorios/`) em `.log` **e** `.html`; **acesso
  restrito**, retenção definida e quem pode ver.
- **Não bloquear "tudo" automaticamente** (evita bypass por VPN/celular e perda de
  visibilidade); o humano decide o ambíguo.

**IMPLEMENTADO (parcial — Tier 1/Tor):**
- `aplicar_dns_seguro.ps1` (+ `/instalar_dns.bat` e card **4** em `/setup`): DNS de
  família (Cloudflare for Families) — `family-adult` bloqueia **adulto + malware**
  por PC; `-Revert` desfaz. Recomendado aplicar também no **roteador/DHCP**.
- `bloquear_hosts.ps1 -Perigo`: lê todos os `.txt` de `categorias/` (adulto/apostas/
  malware/anônimos) e adiciona ao `hosts`; `.bat` ganhou a opção **[3] Proteção**.
  Pasta `categorias/` + `LEIA-ME.txt` (o arquivo `-Perigo` é o mecanismo; as listas
  ficam a critério da escola).
- **Tor/anonimizadores:** agente detecta (`BLOCKED_ANON_*`), categoria **"Anônimo"**
  no radar e ação **"Bloquear Anônimos (Tor)"** (encerra `tor.exe`/I2P e fecha o Tor
  Browser).

**Ainda pendente (próximas etapas):** alerta automático no painel (sugerir/bloquear
por limiar), categorias de risco emocional/criminal e o log/relatório (IS‑071).

---

## IS-075 — Monitor: "Histórico de Hoje" aparecia vazio 🟢

**Sintoma:** o expansor "Histórico de Desvios e Infrações (Hoje)" mostrava "Nenhuma
infração..." mesmo com atividade no dia.

**Causa:** a seção filtrava **apenas** termos de infração (`"INFRAÇÃO"`, `"Enviou '"`,
`"Bloqueio"` com B maiúsculo, `"Celular"`). As entradas do dia eram logins da tela de
bloqueio (`"Entrou no ... (tela de bloqueio)"`, com **b** minúsculo) → **nada casava**.
Além disso, o timestamp vem em **UTC** e o match era por string de data local.

**Solução (`lab_monitor.py`):** a seção virou **"Histórico de Hoje (entradas, ações e
infrações)"** — mostra **todos** os registros do dia, com coluna **Tipo**
(Entrada/Ação do professor/Infração/Registro) e contagem; conversão de fuso via
`_dt_local()` (ISO→local) e `datetime.now().date()`.

**Validar:** com dados reais, passou de **0** para **222** registros de hoje. `py_compile` OK.

---

## IS-076 — Desligar/Reiniciar não concluía (delay de 10s) 🟢

**Sintoma:** ao enviar "Desligar PC", a máquina ia para a tela **"Você escolheu
sair"** mas **não desligava**.

**Diagnóstico:** o comando **chegou** (o `activity` da máquina mostrava "Você escolheu
sair"); o problema era o `shutdown /s /f /t 10` — a contagem de 10s permite abortar
(`shutdown /a`) e deixa a tela pendurada.

**Solução:** trocado para **`/t 0`** (imediato, sem janela para abortar) em
`lab_agent.py` e no embutido do `lab_agent.ps1` (Shutdown e Restart).

**Arquivos:** `data/repo/plugins/lab_agent.py`, `data/repo/plugins/lab_agent.ps1`

**Ação:** **reinstalar o agente** nas máquinas (o código é embutido no `lab_agent.ps1`)
para valer. Se ainda assim não desligar, será questão de privilégio (agente na sessão
do aluno sem direito de desligar) — aí elevamos o agente.

---

## IS-077 — (Estudo/Backlog) Monitor online no Streamlit Cloud ⚪

**Problema:** o Streamlit Cloud **não recebe conexões de entrada** nem roda um Flask
persistente; o **receiver** (que escuta os agentes na porta 5000) **não pode morar no
Cloud**. O Cloud só lê um datastore alcançável (Supabase).

**Opções avaliadas:**
- **A) Relay via Supabase (recomendado):** o receiver no PC do professor **empurra**
  um snapshot agregado (throttle ~60s) para `lab_snapshot` e **puxa** comandos de
  `lab_commands`; a página **Monitor** no app Cloud lê o Supabase. Online, multiusuário,
  reaproveita login. Não é tempo real.
- **B) Túnel (Tailscale/Cloudflare Tunnel):** expõe o receiver por **nome fixo**
  (Tailscale já instalado) → tempo real + resolve IP/DNS. Exige túnel ativo.
- **C) Agentes enviando direto p/ Supabase:** rejeitado (egress/segurança/internet).
- **D) Receiver em VPS público:** custo/segurança/rede da escola.

**DNS:** professores usam a URL pública do Cloud (sem DNS); os **agentes** ganham nome
fixo via túnel (ou DDNS+port-forward, menos seguro).

**Recomendação:** fase 1 = **A) relay Supabase + página Monitor no Cloud**; fase 2
opcional = **B) Tailscale Funnel** para tempo real. App separado no repo `apps/` é
possível, mas **não necessário** (uma página no app principal resolve).

**Cuidados:** push a cada ~60s (não 10s), sem `select(*)`, cache `st.cache_data` no
Cloud; comandos só por tabela (latência de 1 ciclo); manter login teacher/admin.

---

## IS-078 — Bloqueio persistente: watchdog + tela reforçada 🟢

**Pedido:** "fechar o jogo" hoje não adianta (reabrem logo). Ter um rastreador que
**derruba o processo sozinho** e/ou **impede a inicialização**.

**IMPLEMENTADO:**
- **Watchdog no agente** (`lab_agent.py` + embutido no `.ps1`): thread daemon que a
  cada **4s** encerra processos cujo nome contenha alguma chave de `BLOCKED_PROCESS_KEYWORDS`
  ∪ `blocked_apps.json` (novo arquivo, editável — ex.: `tor.exe`, `i2prouter.exe`).
  Flag `AUTO_BLOCK` (default `True`). Cada kill é registrado no log.
- **`blocked_apps.json`**: lista extra de processos (reload dinâmico).
- **Tela de bloqueio reforçada** (`sysava_lock.ps1`): `ShowInTaskbar=false`, timer de
  **1s** que reafirma `TopMost`/`BringToFront` e **mata `taskmgr.exe`**; e
  **`DisableTaskMgr=1`** no HKCU enquanto bloqueado (restaurado ao desbloquear).

**Pendente (backlog):** **IFEO** (`Image File Execution Options`) para impedir de vez a
abertura dos `.exe` (requer Admin), e hook de teclado/quiosque se quiser bloquear
Alt+F4/Alt+Tab.

**Arquivos:** `data/repo/plugins/lab_agent.py`, `data/repo/plugins/lab_agent.ps1`,
`data/repo/plugins/sysava_lock.ps1`, `data/repo/plugins/blocked_apps.json`

**Ação:** **reinstalar o agente** (código embutido no `.ps1`) nas máquinas.

## IS-079 — Relatório detalhado por PC no dashboard 🟢

**Pedido:** selecionar um PC e ver **navegadores, jogos e apps** em atividade.

**IMPLEMENTADO:**
- Agente passa a enviar `procs` (lista compacta dos nomes de processos ativos,
  até 200) no payload do `/ping`.
- Nova rota **`/detalhes?maquina=X`** (login) no receiver: mostra usuário/IP, janela
  ativa, categoria, portas e **três colunas** — 🌐 Navegadores, 🎮 Jogos, ⚙️ Outros
  processos. Link **🔎** adicionado em cada linha do dashboard.

**Arquivos:** `data/repo/plugins/lab_receiver.py`, `data/repo/plugins/lab_agent.py`,
`data/repo/plugins/lab_agent.ps1`

**Validar:** `/detalhes` sem login → 302; logado e máquina existente → 200 com
"Navegadores". `py_compile` + parse dos `.ps1` + Python embutido OK.

---

## IS-080 — Autostart falhava no `GroupId` (nome de grupo localizado) 🟢

**Sintoma:** ao atualizar o agente, dava **erro no `GroupId`** na criação da tarefa.

**Causa:** `New-ScheduledTaskPrincipal -GroupId "BUILTIN\Users"` usa o **nome do grupo
local** — num Windows **pt-BR** o grupo é "Usuários", então `BUILTIN\Users` não
resolve e a tarefa falha.

**Solução:**
- `lab_agent.ps1` (passo 5b): o autostart passou a usar a **pasta Startup comum**
  (`SysAva Agent.vbs`, que roda no logon de qualquer usuário, oculto) como
  **método principal** — sem depender de nome de grupo. Fallback de tarefa agora usa
  **`-UserId "$env:USERDOMAIN\$env:USERNAME"`** (+ `-LogonType Interactive`), não GroupId.
- `instalar_tela_sysava.ps1`: o fallback da tarefa também trocado para `-UserId`.

**Arquivos:** `data/repo/plugins/lab_agent.ps1`,
`data/repo/plugins/instalar_tela_sysava.ps1`

**Validar:** parse OK e **nenhum `GroupId`** restou nos `.ps1`. Re-executar o
instalador deve mostrar **"[OK] ... via Startup"**.

---

## IS-081 — Ação "Atualizar Monitor" pelo painel 🟢

**Pedido:** uma opção de atualização que, na máquina, baixa o lab e roda o script
pedindo a senha de Administrador.

**Solução:**
- Agente (`lab_agent.py` + embutido no `.ps1`): nova função `atualizar_monitor()` —
  baixa `lab_agent.ps1` do servidor (`/download/lab_agent.ps1`) para o TEMP e o
  reexecuta com **`Start-Process -Verb RunAs`** (o **UAC pede a senha de
  Administrador**); o instalador atualiza o agente e reinicia. Trata o comando
  **"Atualizar"**.
- Ação **"Atualizar Monitor (baixar e reinstalar)"** adicionada ao painel do plugin
  (`lab_monitor.py`) e ao dashboard web (`ACOES_CONTROLE` no `lab_receiver.py`).

**Arquivos:** `data/repo/plugins/lab_agent.py`, `data/repo/plugins/lab_agent.ps1`,
`data/repo/plugins/lab_monitor.py`, `data/repo/plugins/lab_receiver.py`

**Bug de encoding corrigido junto:** o passo `/t 0` (IS-076) gravou os arquivos com
`Get-Content`/`Set-Content`, **duplo-codificando os acentos** ("Anônimos"→"AnÃ´nimos").
Corrigido por round-trip `cp1252→utf-8` em `lab_agent.py`/`lab_agent.ps1` (mesmo
padrão de `lab_agent.py`/`.ps1` recentes; usar **LF** foi mantido).

**Validar:** parse + `py_compile` + Python embutido OK; `"Anônimos"` presente e sem
resíduo `Ã`. **Reinstalar o agente** para receber a ação.

---

## IS-082 — Abrir o dashboard web pelo plugin Monitor 🟢

**Pedido:** no plugin Monitor, visualizar e clicar num link para abrir o dashboard
web do receiver.

**Solução (`lab_monitor.py`):** adicionado **`st.link_button`** para
`http://<ip>:5000/` (via `get_receiver_base_url()`), **em dois lugares**: no topo da
página e na barra lateral. Ao lado, um `st.caption` mostra a URL (com aviso de
"login do professor").

**Validar:** `py_compile` OK; `st.link_button` disponível no Streamlit instalado.

---

## IS-083 — Memorizar o RA na tela de bloqueio 🟢

**Pedido:** não ter que digitar o RA toda vez que logar.

**Solução (`sysava_lock.ps1`):** guarda o **último RA válido** em
`%LOCALAPPDATA%\SysAva\ultimo_ra.txt` (por usuário do Windows) e **preenche o campo**
no próximo logon (com o texto selecionado — basta teclar **Enter**). O RA é salvo ao
validar com sucesso (também no modo offline). Se não for o mesmo aluno, basta
sobrescrever o campo.

**Arquivos:** `data/repo/plugins/sysava_lock.ps1`

**Observação:** em PC com **conta Windows compartilhada**, o RA lembrado é o do
**último** aluno (o próximo confirma ou troca). Se cada aluno tem conta Windows
própria, cada um lembra o seu.

**Ação:** reinstalar a tela (`/setup` → card 3) para baixar o `sysava_lock.ps1` novo.

---

## IS-084 — Mostrar o aluno da tela de bloqueio no relatório 🟢

**Contexto:** a conta Windows do laboratório é **sempre "ALUNO"**, então o relatório
mostrava "ALUNO" em vez do aluno real.

**Solução (`lab_receiver.py`):** o **dashboard** e a página **`/detalhes`** passaram a
exibir **`Aluno (RA)`** a partir de `lab_users.json` (associação gravada pela tela de
bloqueio via `/api/auth_ra?ra=...&maquina=...`), com **fallback** para a conta Windows
quando não houver associação. Coluna do dashboard renomeada de "Usuário" para
**"Aluno (RA)"**.

**Arquivos:** `data/repo/plugins/lab_receiver.py`

**Validar:** com uma associação de teste, `GET /` mostrou **"Aluno Teste (12345)"** em
vez de "ALUNO"; `py_compile` OK. (No plugin Streamlit já existia a coluna "Aluno (RA)".)

---

## IS-085 — Início limpo: só o SysAva, sem navegadores/bootloaders 🟢

**Pedido:** ao iniciar, deixar **apenas uma janela do navegador na página do SysAva** e
**fechar outros navegadores e bootloaders de jogos**.

**Solução:**
- **Tela de bloqueio** (`sysava_lock.ps1`): nova função **`Fechar-Navegadores-E-Jogos`**
  (mata `chrome`, `msedge`, `firefox`, `brave`, `opera`, `iexplore` e launchers
  `steam`, `epicgameslauncher`, `battle.net`, `riotclientservices`, `origin`,
  `eadesktop`, `ubisoftconnect`, `gog`/`galaxyclient`). Chamada no **`Add_Shown`**
  **antes** de abrir a URL — assim abre **uma** instância já na página do SysAva.
- **Watchdog do agente** (`blocked_apps.json`): adicionados os **bootloaders** para
  não reabrirem (são derrubados a cada ~4s).

**Arquivos:** `data/repo/plugins/sysava_lock.ps1`,
`data/repo/plugins/blocked_apps.json`

**Validar:** parse do `.ps1` OK; `blocked_apps.json` válido. **Reinstalar a tela**
(`/setup` card 3) e o agente (card 1) para valer.

---

## IS-086 — Servidor portátil (sem depender do notebook) 🟢

**Pedido:** o receiver não pode depender do notebook (bateria/cair). Ter uma versão
para instalar num PC fixo.

**Limitação:** o Streamlit Cloud **não hospeda** o receiver (sem conexões de entrada).

**Solução — receiver autônomo + pacote portátil:**
- **Autonomia (`lab_receiver.py`):** removida a dependência do `services` na
  autenticação/relatório/histórico:
  - Login do painel e `/api/auth_ra` agora usam **REST do Supabase** (PostgREST, via
    `requests`) + **`bcrypt`** (`_rest_get`, `_buscar_usuario`, `_bcrypt_ok`).
  - Histórico do aluno via `_rest_insert("user_history", ...)`.
  - Relatório usa **`audit_log.py` local** (novo arquivo ao lado do servidor, pasta
    oculta `.relatorios/`), com fallback para o `services`.
  - Credenciais carregadas do `.env` local **e** da raiz.
  Deps do servidor: **flask, waitress, filelock, requests, bcrypt, python-dotenv**.
- **Pacote portátil:** `INICIAR_SERVIDOR.ps1` + `.bat` — baixa/instala um **Python
  embutido** (ou usa o do PATH), instala as dependências, **abre o firewall** (TCP 5000
  / UDP 5001) e sobe o `lab_receiver.py`. `config.env.example` para o `.env`.
- **Uso:** copiar a pasta **`plugins`** para o PC fixo, criar `.env`
  (`SUPABASE_URL`/`SUPABASE_KEY`) e rodar `INICIAR_SERVIDOR.bat`. Card **6** no `/setup`
  baixa os arquivos.

**Arquivos:** `data/repo/plugins/lab_receiver.py`, `data/repo/plugins/audit_log.py`,
`data/repo/plugins/INICIAR_SERVIDOR.ps1`, `data/repo/plugins/INICIAR_SERVIDOR.bat`,
`data/repo/plugins/config.env.example`

**Validar:** `/api/auth_ra?ra=adriana` → `ok:true` e `POST /login` OK (REST, sem o
`services`); `/download/INICIAR_SERVIDOR.*` → 200; card 6 no `/setup`; parse do `.ps1`
e `py_compile` OK.

**Observação:** o servidor precisa de **internet** (Supabase) para login/relatório;
agentes e downloads funcionam na **LAN**. Ainda é preciso um PC ligado (o fixo), mas
**não** o notebook.

---

## IS-087 — Bootstrap do servidor portátil baixa tudo sozinho 🟢

**Sintoma:** ao rodar o `INICIAR_SERVIDOR.bat` numa pasta nova, deu
**"lab_receiver.py nao encontrado"** — porque só o `.bat` havia sido baixado, sem os
demais arquivos.

**Solução:**
- `INICIAR_SERVIDOR.ps1` ganhou o parâmetro **`-Fonte`**: se o `lab_receiver.py` não
  estiver na pasta, ele **pergunta a URL de origem** (ex.: `http://<ip>:5000`), baixa
  **`/servidor.zip`** e extrai tudo (**`Expand-Archive -Force`**).
- Rota **`/servidor.zip`** no receiver: empacota os arquivos do servidor
  (`lab_receiver.py`, `audit_log.py`, `INICIAR_SERVIDOR.*`, `config.env.example`,
  agentes/scripts, `logo`/`wallpaper`, `blocked_apps.json`, `categorias/`).
- Card **6** no `/setup` ganhou o botão **📦 servidor.zip (tudo)**.

**Arquivos:** `data/repo/plugins/lab_receiver.py`,
`data/repo/plugins/INICIAR_SERVIDOR.ps1`

**Validar:** `/servidor.zip` → 126 KB com todos os itens; parse do `.ps1` +
`py_compile` OK. Uso no PC novo: rodar `INICIAR_SERVIDOR.bat` e informar a URL de
origem — ou baixar o `servidor.zip` do `/setup` e extrair.

---

## IS-088 — Sábado manual recomeçava a numeração em 13 🟢

**Sintoma:** com a aula **23** já registrada no portal (Fundamentos UI/UX, I-A,
turma 309197), o botão **➕ Gerar até 4 planos** da aba **🟣 Sábados
(reposição)** do app 8510 gerou os planos de 20/06 com `AULA_NUM 13..16` e
conteúdo da “Aula 13 Coleta de Informações”, em vez de partir da **24**.

**Causa:** `proximo_numero()` (em
`apps/planejamento_registro/planejamento_registro_streamlit.py`) usava
`COUNT(*)` de `historico_aulas` e `planejamento`. O histórico local tinha 8
linhas e a fila 12 planos → `max(8, 12) + 1 = 13`. Os planos **21..23** já
registrados estavam em `aulas/registradas/` **sem linha em `planejamento`**, e
o `COUNT` ainda é instável a exclusões/mudança de status (mesmo defeito do
IS-042/AP-013 no gerador automático).

**Mudança:** novo helper `core/banco.maior_aula_num_por_arquivo` (maior
`AULA_NUM` dos `.txt` em `pendentes/`, `prontas/` e `registradas/`).
- `proximo_numero()` (aba 🟣 Sábados) usa o maior entre `COUNT(historico)`,
  `MAX(numero_aula)` do `planejamento` e esse helper.
- `core/gerador.py` (aba 📄 Planos) mescla o mesmo mapa em `next_aula_num`:
  antes partia de `MAX(planejamento)+1 = 21`, e com o filtro **“De 24”** os
  slots 07:10/08:10/11:30 do sábado eram descartados — só o 13:30 virava 24.
  Agora os 4 slots iniciais são gerados como 24..27.
- A ocupação do gerador também passa a considerar os `.txt` (data+horário):
  as aulas já registradas em 22/06 e 23/06 não são regeradas.
- **Sábado alvo em ⚙️ Config:** chave `sabado_alvo_planejamento` (selectbox)
  + parâmetro `data_alvo` no gerador/API. A aba Sábados já abre nele; no
  «🚀 Gerar planos» a restrição é **opcional** (checkbox desmarcado por
  padrão). Marcado como **20/06/2026**; 10/06 tem registro e não é planejado.
- **Grade normal depois do sábado:** a fila continua em **24/06** (28..), pois
  20/06 já foi gerado (24..27) e 22/06/23/06 estão registrados.
- **«Sobrescrever» protege aulas registradas:** `registrados_set` (`.txt` de
  `aulas/registradas/`) é respeitado **sempre**, mesmo com force ligado. Antes
  o force ignorava a ocupação e gerou 5 planos em 15/16/17-06 como 28..32;
  esses 5 `.txt`/linhas foram removidos. O force renumera só pendentes/prontas.
- **Reposição da disc. 5 (sem buraco entre disciplinas):** Fundamentos termina
  em 03/07 07:10 (aula 40) e a disc. 5 começa no **slot seguinte, 03/07 08:10**
  (aula 1). Demais repostas: **11/07** (sábado letivo de sexta, 07:10=2),
  **15/08** (08:10=3, 09:30=4) e **12/09** (07:10=5); 22/08 já tinha P.C.II às
  07:10. Disc. 5 volta a **1–40**. Janela de Fundamentos volta a 03/07.
- **Turma I-B (314114), Fundamentos UI:** **40/40 planos** (1–40, sem
  buracos/duplicatas/conflitos), em `aulas/prontas/` como `pronta`; **0
  registrados** no histórico. O **20/06 não é usado** (a A já tem 4 planos).
  Seminários **36–39** foram para **27/06** (07:10, 08:10, 09:30, 13:30);
  aulas **33–35** voltaram a 02/07 (13:30/14:30) e 03/07 (08:10); a **40** foi
  para **11/07 14:30**. Fundamentos B termina em **03/07** (aula 35), liberando
  06/07 e 09/07.
- **Programação Mobile na I-B:** aulas **1–3** em **11/07** (sábado de sexta)
  às **08:10, 09:30 e 13:30**; a aula 40 de Fundamentos ocupa 14:30 — 4 aulas
  da B no dia (a A fica no 07:10).

**Arquivos:** `apps/planejamento_registro/planejamento_registro_streamlit.py`,
`apps/planejamento_registro/core/banco.py`,
`apps/planejamento_registro/core/gerador.py` (registro em `apps/ISSUES.md` →
**AP-028**).

**Validar:** harness com o banco real (`309197` / disciplina `8`):
`_maior_aula_em_arquivos = 23` e `proximo_numero = 24`; sandbox do gerador com
`aula_min=24` e `data_alvo=2026-06-20` → exatamente 4 planos: 20/06
**07:10=24, 08:10=25, 11:30=26, 13:30=27**; com `force_overwrite=True` +
`aula_min=28` → **24/06 28..31 + 26/06=32**, sem tocar em 15/16/17-06
(registrados); `py_compile` + 71 testes OK. Foram excluídos os planos errados
de 20/06 (13..16), os da base antiga (24 em 13:30 e 25 em 22/06), os de 10/06
(24..26) e os 5 de 15/16/17-06 (28..32).

---

## IS-089 — Título e ícone da aba do SysAva 🟢

**Sintomas:** a aba do app principal aparecia como **“Streamlit”** com o ícone
padrão, diferente do app de Planejamento (8510); e a sidebar mostrava um
**logo do Google** grande, sem sentido para o SysAva.

**Causa:** o `app.py` principal nunca chamava `st.set_page_config()`. Pior: a
sidebar usava `https://cdn-icons-png.flaticon.com/512/2991/2991148.png`, e essa
URL retorna o **“G” do Google** (não um capacete/logo do portal).

**Mudança:**
- Logo próprio copiado para **`assets/logo_sysava.png`**.
- No topo de `app.py`, antes de qualquer outro comando `st.*`:

```python
APP_LOGO = os.path.join(project_root, "assets", "logo_sysava.png")
st.set_page_config(
    page_title="SysAva",
    page_icon=APP_LOGO if os.path.exists(APP_LOGO) else "🎓",
)
```

- A sidebar passou a usar `st.image(APP_LOGO, width=100)` (com fallback
  `## 🎓 SysAva` se o arquivo não existir).

**Arquivos:** `app.py`, `assets/logo_sysava.png`.

**Validar:** subir o app principal e conferir `document.title === "SysAva"` e o
favicon servido localmente (`/media/...png`), além do logo SysAva na sidebar
(verificado via browser-automation). Reinicie o Streamlit para carregar.

---

## IS-090 — Tema azul do SysAva 🟢

**Pedido:** aplicar o **azul do logo** ao app principal (fundo/sidebar/botões),
mantendo o visual escuro.

**Mudança:**
- Novo `.streamlit/config.toml` com `base = "dark"`,
  `primaryColor = "#2563EB"`, `backgroundColor = "#0A1220"`,
  `secondaryBackgroundColor = "#101A2E"` e `textColor = "#E5E7EB"`.
- CSS global do `app.py`: fundo `linear-gradient(135deg, #0B1E3F, #070D18)`,
  sidebar azul-escura com borda `rgba(37,99,235,.35)`, botões com borda
  `#2563EB`, hover `#60A5FA` (substituiu o verde `#00ffa3`), inputs `#0F1B2E`
  e links `#60A5FA`.

**Arquivos:** `.streamlit/config.toml`, `app.py`.

**Validar:** subir o app e conferir o fundo
`linear-gradient(135deg, rgb(11,30,63), rgb(7,13,24))` e o texto
`rgb(229,231,235)` (verificado via browser-automation + screenshot da tela de
login). Reinicie o Streamlit para carregar o `config.toml`.

---

## IS-091 — Visualização da prova (folha branca) 🟢

**Sintoma:** na aba de emissão/impressão, o “Visualizar Prova” mostrava o texto
da prova em cinza-escuro direto sobre o fundo navy do app — sem contraste e
sem cara de folha.

**Causa:** `generate_assessment_print_html()` (em `views/avaliacoes.py`) definia
`body { color:#333 }` mas **não** definia fundo. O `components.html` é
transparente, então o navy do Streamlit aparecia atrás do texto.

**Mudança:** a prévia agora tem:
- fundo geral claro (`#e8eef8`) e uma **folha `.paper`** branca centralizada,
  com `max-width: 820px`, padding de 40px, cantos arredondados e sombra;
- texto escuro (`#1f2937`) e cabeçalho/linhas ajustados para papel;
- botão **“🖨️ Imprimir / Salvar PDF”** azul (`#2563EB`), centralizado;
- `@media print` preservado: A4, margens de 15mm, sem sombra/padding da folha
  e sem o botão (`.no-print`).

**Arquivos:** `views/avaliacoes.py`.

**Validar:** gerar o HTML com dados de exemplo e abrir no navegador — body
`rgb(232,238,248)`, `.paper` branco, texto `rgb(31,41,55)` (verificado via
browser-automation + screenshot). No app, clicar em **Visualizar Prova**;
imprimir/PDF continua em A4.

---

## IS-092 — Fontes pequenas com o navegador a 100% 🟢

**Sintoma:** em telas grandes, com o zoom do navegador em 100%, as letras do
menu, títulos e controles ficavam pequenas demais.

**Causa:** o Streamlit usa base de **16px**; em monitores grandes/4K, 100% de
zoom deixa tudo reduzido.

**Mudança:** no CSS global do `app.py`:

```css
html { font-size: 112.5% !important; } /* 18px (padrão Streamlit: 16px) */
```

Como os componentes usam `rem`, títulos, menus, botões, inputs e textos sobem
juntos (~12,5%). O layout continua centralizado e o tema azul intacto.

**Arquivos:** `app.py`.

**Validar:** com o app aberto, `getComputedStyle(document.documentElement)
.fontSize === "18px"` e `h1` em `49.5px` (verificado via browser-automation);
screenshot da tela de login mostra o texto maior. Reinicie/rerrole o app.

---

## IS-093 — Boxes de código/conteúdo em azul mais claro 🟢

**Pedido:** com o tema azul escuro, os boxes de código/conteúdo e o dropdown
de planos prontos (8510) ficavam escuros demais. Um primeiro ajuste em branco
ficou com contraste excessivo; o pedido final é **mesma tonalidade azul, só
um pouco mais clara**.

**Mudança:**
- No **app principal** (`app.py`): `pre`, `code` e
  `[data-testid="stCodeBlock"]` com fundo `#152C52` (azul mais claro), texto
  `#E5E7EB` e borda `#2E4F7A`.
- No **Planejamento 8510**: mesmo estilo + `[data-testid="stTextArea"]
  textarea` (conteúdo do plano) e popover do multiselect
  (`[data-baseweb="popover"]`, `[role="listbox"]`/`option`) no mesmo azul, com
  hover `#1C3A66`.

**Arquivos:** `app.py`,
`apps/planejamento_registro/planejamento_registro_streamlit.py` (registro no
repo de apps: **AP-029**).

**Validar:** abrir uma aula com código no app principal e, no 8510, 📄 Planos
(conteúdo `.txt`) e 🤖 Registrar / Sincronizar (dropdown dos planos) — fundo
azul mais claro e texto claro; `py_compile` OK.

---

## IS-094 — Google Drive (conta bot/service account) 🟢

**Pedido:** manter a pasta `data/` no Google Drive e deixar plugins e banco
funcionais no Cloud, usando uma “conta bot”. O login da service account e o
download da pasta foram validados.

**Implementação:**
- `services/drive_storage.py`: autentica com service account (JSON em
  `data/drive_credentials.json` local ou `[gcp_service_account]` nos Secrets),
  lista/baixa/envia arquivos. A pasta padrão é
  `1db5qPNH9vOQKIabfNgWpetvjQsYsUuQi` (pode ser trocada por `DRIVE_FOLDER_ID`).
- `sync_repo_down()` baixa `repo/` para `data/repo` pulando `__pycache__`,
  `.pyc`, logs e arquivos > 1 MB (plugins, JSONs e scripts).
- `sync_db_down()` baixa `escola_ativa.db` para `data/` (nunca abre direto do
  Drive); `sync_db_up()` envia o SQLite como backup.
- `app.py`: no login, `_drive_bootstrap()` (cache_resource) sincroniza o repo
  uma vez por processo e baixa o banco apenas se ele não existir.
- **Plugins → ☁️ Drive**: testar conexão, baixar repo/plugins, enviar banco
  local e baixar banco do Drive (com confirmação).
- `scripts/drive_check.py`: CLI `--pull`/`--push` para validar/sincronizar.

**Limitação:** service account **não tem cota para criar** arquivos no Meu
Drive. Ela baixa normalmente; para criar o `escola_ativa.db` pela primeira vez,
envie pelo Drive web (ou use Shared Drive/OAuth de uma conta comum). Depois,
atualizações de um arquivo existente podem funcionar.

**Arquivos:** `services/drive_storage.py`, `scripts/drive_check.py`,
`app.py`, `views/plugins.py`, `requirements.txt`, `.gitignore`,
`docs/ISSUES_LOCAIS.md`.

**Validar:** `python scripts/drive_check.py` lista a pasta; `--pull <tmp>`
baixa 109→72 arquivos úteis (~1,2 MB, sem logs/backups); `py_compile` OK.

---

## IS-095 — Notas: `float(None)` no JSON do Drive 🟢

**Sintoma:** ao abrir **Plugins → Notas**, o plugin era interrompido com
`float() argument must be a string or a real number, not 'NoneType'`.

**Causa:** o `student_scores.json` sincronizado do Drive tem notas `null`
(ex.: estudante `[RA]`, disciplina 8, T1/N2). O plugin fazia
`float(nm2)` / `float(p.get('points'))` / `float(calc['total'])` direto.

**Mudança:** helper `_to_float(valor, default=0.0)` no
`student_scores.py` e uso nas médias, notas do trimestre, pontos
qualitativos, score do sistema e bônus. As notas `None` viram `0.0`
na planilha (editáveis normalmente).

**Arquivos:** `data/repo/plugins/student_scores.py` (também atualizado no
Drive; o Cloud baixa no boot ou em **Plugins → ☁️ Drive → Baixar repo/plugins**).

**Validar:** `py_compile` OK; JSON do Drive saneado (nota `None` → `0.0`).
Reinicie o app no Cloud ou clique em “Baixar repo/plugins”.

---

## IS-096 — Monitor: links do painel web com IP real da LAN 🟢

**Sintoma:** em **Plugins → Monitor**, os botões "Abrir Dashboard Web" e
"Abrir Dashboard Web do Monitor" exibiam `http://127.0.0.1:5000/`, que só
funciona no próprio servidor — de qualquer outro PC do laboratório o link
não abria.

**Causa:** `data/repo/plugins/lab_monitor.py` montava as URLs de exibição a
partir de `LOCAL_RECEIVER_URL = "http://127.0.0.1:5000"`.

**Mudança:** novo helper `get_local_ip()` (mesma lógica do `lab_agent.py`,
via socket UDP para `10.255.255.255`) e `get_dashboard_base_url()`, que
devolve `http://<IP-da-LAN>:5000`. As chamadas internas da API continuam em
loopback (mais rápido/robusto); apenas os links exibidos usam o IP real. A
variável de ambiente `SYSAVA_SERVER_URL` (ex.: `http://192.168.10.126:5000`)
permite fixar uma URL quando necessário. O receiver já escuta em
`0.0.0.0:5000`, então nada mais precisa mudar.

**Arquivos:** `data/repo/plugins/lab_monitor.py`, `docs/ISSUES_LOCAIS.md`.

**Validar:** abrir **Plugins → Monitor** e conferir que o link mostra o IP
da LAN (ex.: `http://192.168.10.126:5000/`) e abre de outro PC. O IP pode
mudar por DHCP; para fixá-lo, defina `SYSAVA_SERVER_URL` ou um IP estático.

---

## IS-097 — Roblox fora da bandeja/inicialização em todos os PCs 🟢

**Sintoma:** após instalar o Roblox, ele deixava um inicializador que subia
junto com o Windows e ficava na bandeja do sistema em cada PC do laboratório.

**Causa:** o instalador do Roblox registra auto-inicialização (valor em
`Run`/`RunOnce`, atalho na pasta Startup e/ou tarefa agendada). O agente só
matava o processo quando o watchdog rodava, mas a entrada de inicialização
permanecia e o ícone voltava no próximo logon.

**Mudança:** nova função `limpar_inicializacao_roblox()` no agente, que:
1. encerra processos com `roblox` no nome (some o ícone da bandeja);
2. apaga valores de `Run`/`RunOnce` (HKCU/HKLM, 32/64 bits) e de
   `StartupApproved` cujo nome ou comando contenha `roblox`;
3. remove atalhos `.lnk`/`.url` das pastas Startup (usuário e todos os usuários);
4. exclui tarefas agendadas com `roblox` no nome.

Ela roda automaticamente no boot do agente (quando `AUTO_BLOCK=True`) e também
pelo comando remoto **"Limpar Inicialização do Roblox (bandeja)"** no Monitor
(inclusive em massa: "Limpar Inicialização do Roblox em TODAS"). A limpeza é
idempotente e não afeta o SysAva (nomes não contêm `roblox`).

**Arquivos:** `data/repo/plugins/lab_agent.py`,
`data/repo/plugins/lab_agent.ps1` (cópia embutida do agente),
`data/repo/plugins/lab_monitor.py`,
`data/repo/plugins/lab_receiver.py`, `docs/ISSUES_LOCAIS.md`.

**Validar:** no Monitor, selecionar as máquinas (ou "Selecionar TODAS") e
executar o comando; no PC, conferir em **Gerenciador de Tarefas → Inicializar**
e na bandeja que o Roblox não reaparece após logoff/logon. `py_compile` e
parser do `.ps1` OK.

---

## IS-098 — Tela de bloqueio: só RA válido ou senha do admin 🟢

**Sintoma:** na tela de bloqueio do SysAva, digitar qualquer palavra liberava
o computador, mesmo sem ser um RA cadastrado.

**Causa:** o `sysava_lock.ps1` tinha dois fallbacks que liberavam a tela:
servidor não descoberto (`Servidor indisponivel - entrando em modo offline`) e
exceção na requisição (ex.: rede ainda não pronta no logon). Nos dois casos
qualquer texto era aceito e salvo como "último RA".

**Mudança:** o RA agora é validado **somente** no receiver (`/api/auth_ra`),
com até 5 tentativas de rede (1,5 s entre elas) para o logon. Se o servidor
não responder, a tela **não abre** e orienta usar a senha do administrador.
A senha secreta padrão é **`labadmin`** (guardada como hash SHA-256 no script,
não em texto puro) e libera mesmo offline. Para trocar sem editar o script,
defina `SYSAVA_ADMIN_UNLOCK` ou crie `unlock_secret.txt` ao lado do arquivo.
O "último RA" só é salvo quando o servidor confirma que o RA existe; a senha
do admin nunca é gravada. Após 5 RAs errados há uma pausa de 5 s.

Para gerar o hash de uma nova senha:
`[BitConverter]::ToString([Security.Cryptography.SHA256]::Create().ComputeHash([Text.Encoding]::UTF8.GetBytes("NOVA_SENHA"))).Replace("-","").ToLower()`

**Arquivos:** `data/repo/plugins/sysava_lock.ps1`, `docs/ISSUES_LOCAIS.md`.

**Validar:** rodar `powershell -ExecutionPolicy Bypass -File
data\repo\plugins\sysava_lock.ps1`; RA inexistente deve continuar bloqueado
(com servidor no ar), `labadmin` deve liberar, e desligar o receiver deve
manter a tela bloqueada para RAs. Parser do `.ps1` OK.

---

## IS-099 — Tela de bloqueio: entrar com o primeiro nome do aluno 🟢

**Pedido:** aceitar o primeiro nome do aluno sem caixa definida. Ex.: **Ana
Roberta** digita `ana`; mas, se existirem várias "Ana", precisa digitar
`anaroberta`, `Ana Roberta` ou `ANA ROBERTA`.

**Mudança:** `lab_receiver.py` (`/api/auth_ra`) tenta, nesta ordem:
1. RA/username exato (como antes);
2. nome do aluno, normalizado (minúsculas, sem acentos/pontuação e com
   espaços colapsados). O primeiro nome só libera se for **único** entre os
   alunos (`role=student`); havendo mais de um, responde
   "Varios alunos com esse nome. Digite o nome completo.";
3. nome completo com ou sem espaços (`ana roberta`, `ANA ROBERTA`,
   `anaroberta`) e prefixo único (`Ana Roberta` → `Ana Roberta Silva`,
   inclusive `anaroberta` → `Ana Roberta Silva`).

O retorno inclui o `ra` canônico, e o `sysava_lock.ps1` passa a exibir a
mensagem de erro do servidor e salva o RA resolvido (não o apelido digitado).
O label da tela virou "Digite seu RA ou nome:".

**Arquivos:** `data/repo/plugins/lab_receiver.py`,
`data/repo/plugins/sysava_lock.ps1`,
`data/repo/plugins/lab_monitor_doc.md`, `docs/ISSUES_LOCAIS.md`.

**Validar:** com o receiver reiniciado, testar `ana` (única), `ana`
(com duas Anas → deve pedir nome completo), `anaroberta`, `Ana Roberta`,
`ANA ROBERTA` e um nome inexistente (deve continuar bloqueado). `py_compile`
e parser do `.ps1` OK.

---

## IS-100 — Admin não aparece pré-preenchido nem na lista de máquinas 🟢

**Sintoma:** a senha do admin (`labadmin`) podia ficar salva em
`%LOCALAPPDATA%\SysAva\ultimo_ra.txt` por versões antigas e era pré-preenchida
na tela de bloqueio, expondo a senha (bastava teclar Enter). Se `labadmin`
existisse em `app_users` como admin/professor, o `/api/auth_ra` também podia
associá-lo à máquina em `lab_users.json`, fazendo-o aparecer no radar.

**Mudança:**
- `sysava_lock.ps1`: ao abrir, se o último valor salvo casar com a senha do
  admin, o arquivo é apagado e o campo **não** é preenchido. A senha do admin
  nunca é gravada (o fluxo retorna antes de `Save-UltimoRA`).
- `lab_receiver.py`: `/api/auth_ra` só associa usuários com `role == 'student'`.
  Admin/professor não é aceito por RA/nome (usa a senha secreta local), então
  não entra no cache de RAs nem em `lab_users.json`.

**Arquivos:** `data/repo/plugins/sysava_lock.ps1`,
`data/repo/plugins/lab_receiver.py`, `docs/ISSUES_LOCAIS.md`.

**Validar:** apagar/editar `ultimo_ra.txt` com `labadmin` e abrir a tela: o
campo deve vir vazio. Digitar `labadmin` deve liberar pelo caminho local e
**não** criar entrada em `lab_users.json`. `py_compile` e parser OK.

---

## IS-101 — Desligar/Reiniciar fecham a tela de bloqueio 🟢

**Sintoma:** os comandos remotos **Desligar PC** e **Reiniciar PC** podiam
ficar presos na tela de bloqueio: o `FormClosing` cancelava qualquer
fechamento enquanto não houvesse desbloqueio, inclusive o encerramento
disparado pelo Windows. Além disso, ao matar o `sysava_lock.ps1` à força, a
política `DisableTaskMgr` podia ficar gravada como `1` no registro do usuário.

**Mudança:**
- `lab_agent.py`/`lab_agent.ps1`: nova `fechar_tela_bloqueio()` chamada antes
  de `shutdown /l`, `/s` e `/r`. Ela remove `DisableTaskMgr` do HKCU (restaura o
  Gerenciador de Tarefas) e encerra o processo `sysava_lock.ps1` se ainda estiver
  aberto; o `/f` do shutdown continua fechando os demais apps.
- `sysava_lock.ps1`: o `FormClosing` agora permite fechar quando
  `CloseReason = WindowsShutDown`/`ApplicationExitCall` ou
  `Environment.HasShutdownStarted`, restaurando as políticas. Fechamento por
  usuário continua bloqueado.

**Arquivos:** `data/repo/plugins/lab_agent.py`,
`data/repo/plugins/lab_agent.ps1`, `data/repo/plugins/sysava_lock.ps1`,
`docs/ISSUES_LOCAIS.md`.

**Validar:** com a tela de bloqueio aberta, enviar **Desligar PC** ou
**Reiniciar PC** pelo Monitor: o PC deve desligar/reiniciar sem travar e, no
próximo logon, o Gerenciador de Tarefas deve voltar ao normal após desbloquear.
`py_compile` (agente + cópia embutida) e parser dos `.ps1` OK.

---

## IS-102 — Atualizações sem UAC (agente + tela de bloqueio) 🟢

**Pedido:** parar de digitar a senha de Administrador do Windows em cada
atualização (e evitar o risco de vazamento da senha).

**Agente — `Atualizar Monitor (rápido, sem UAC)`:**
- `lab_agent.py` baixa `/download/lab_agent.py` do receiver, valida a sintaxe
  com `compile()`, guarda um `.bak`, substitui o próprio arquivo e inicia uma
  nova cópia (`sys.executable`) encerrando a antiga. Nada de `-Verb RunAs`.
- A ação antiga foi dividida no Monitor e no painel web:
  **Atualizar Monitor (rápido, sem UAC)** e **Reinstalar Monitor (com UAC)**
  (esta continua usando o `lab_agent.ps1` para instalar dependências/autostart).
- `DOWNLOAD_WHITELIST` agora libera `lab_agent.py`.
- O bloco Python embutido no `lab_agent.ps1` estava **dessincronizado** em
  relação ao `lab_agent.py` (faltavam recursos recentes). Ele foi regerado a
  partir do `lab_agent.py` (here-string de aspas simples, sem interpolação) e
  os fallbacks fixos de MAC/IP foram removidos; a descoberta usa cache, UDP e
  varredura da sub-rede.
- Limitação: a primeira máquina que receber o comando com o agente **antigo**
  ainda executa o instalador com UAC (o código antigo não conhece o caminho
  rápido). Depois desse primeiro push, as próximas atualizações são silenciosas.

**Tela de bloqueio — auto-atualização:**
- A cópia instalada em `C:\ProgramData\SysAva` (somente leitura para o aluno)
  agora atua como bootstrap: baixa `sysava_lock.ps1` do servidor para
  `%LOCALAPPDATA%\SysAva\sysava_lock.ps1` e executa essa cópia gravável com
  `-SemAtualizar`. O download é validado pelo parser do PowerShell antes de
  substituir a cópia local.
- Assim, atualizar o `sysava_lock.ps1` no servidor não exige novo instalador:
  no próximo logon o PC pega a versão nova. Se o servidor estiver fora, usa a
  última cópia local; se não houver cópia local válida, roda o script instalado.
- O `unlock_secret.txt` é procurado tanto em `%LOCALAPPDATA%\SysAva` quanto em
  `C:\ProgramData\SysAva`.
- Limitação: é preciso instalar **uma vez** esta versão do `sysava_lock.ps1`
  (via `/setup` card 3 ou `instalar_tela_sysava.ps1`, com UAC); a partir daí as
  atualizações da tela são sem UAC.

**Arquivos:** `data/repo/plugins/lab_agent.py`,
`data/repo/plugins/lab_agent.ps1`, `data/repo/plugins/lab_monitor.py`,
`data/repo/plugins/lab_receiver.py`, `data/repo/plugins/sysava_lock.ps1`,
`docs/ISSUES_LOCAIS.md`.

**Validar:** executar **Atualizar Monitor (rápido, sem UAC)** em um PC com o
agente novo: ele deve reiniciar sem UAC e continuar reportando no radar.
Trocar o `sysava_lock.ps1` no servidor e fazer logoff/logon: a tela deve abrir
com a versão nova (conferir `%LOCALAPPDATA%\SysAva\sysava_lock.ps1`).
`py_compile` (agente + cópia embutida) e parser dos `.ps1` OK.

---

## IS-103 — Liberação temporária do Roblox (padrão 20 min) ⚪

> **Substituído pelo IS-104.** O campo/ação de tempo foi removido: o Roblox
> não é mais fechado automaticamente. Mantido aqui apenas como histórico.

**Pedido:** um campo no dashboard para definir por quanto tempo o Roblox pode
ficar aberto antes de ser fechado, com padrão de **20 minutos**.

**Como ficou:**
- Dashboard web (`lab_receiver.py`): campo **“min Roblox”** ao lado da ação,
  com valor padrão **20**, e a ação **“Liberar Roblox (tempo do campo, min)”**.
- Plugin Streamlit (`lab_monitor.py`): ao escolher **“Liberar Roblox (tempo do
  campo)”**, aparece o `number_input` **Tempo de liberação do Roblox (min)**
  (0–1440, padrão 20, passo 5). O mesmo campo é usado pelo botão em massa
  **“Liberar Roblox em TODAS”**.
- Agente: o comando envia os minutos em `command_msg`. `permitir_roblox(min)`
  define `ROBLOX_ALLOW_UNTIL = agora + min*60`. O watchdog deixa o Roblox
  rodar enquanto `agora < ROBLOX_ALLOW_UNTIL`; ao expirar, mata o processo e
  continua bloqueando (reabrir não libera). `0` bloqueia na hora. O comando
  **Bloquear Jogos** cancela a liberação imediatamente.
- O timer começa quando o comando é aplicado (não quando o aluno abre o jogo).
  Para nova janela, o professor reenvia a ação.

**Arquivos:** `data/repo/plugins/lab_agent.py`,
`data/repo/plugins/lab_agent.ps1`, `data/repo/plugins/lab_monitor.py`,
`data/repo/plugins/lab_receiver.py`, `docs/ISSUES_LOCAIS.md`.

**Validar:** enviar 20 min para uma máquina com Roblox aberto: ele continua
por 20 min, fecha sozinho e não reabre; enviar com 0 fecha na hora; reenviar
libera de novo. `py_compile` (agente + embutido) e parser dos `.ps1` OK.

---

## IS-104 — Roblox não é mais derrubado automaticamente 🟢

**Sintoma:** alunos reclamavam que o Roblox fechava em segundos e “não
carregava”. O ícone da bandeja não tem relação: o watchdog do agente matava
qualquer processo com `roblox` a cada ~4 s (a janela do IS-103 só valia se o
comando chegasse ao agente novo).

**Mudança:** o watchdog agora ignora processos cujo nome contenha `roblox`
(`WATCHDOG_EXCLUDE_KEYWORDS = ["roblox"]`). O Roblox **permanece aberto** e só
é encerrado pelo comando manual **Bloquear Jogos (Fechar Roblox/Loki/Games)**.
Os demais jogos/launchers continuam sujeitos ao auto-bloqueio. O campo “min
Roblox” e a ação **Liberar Roblox** foram removidos do dashboard web e do
plugin Streamlit, e as entradas de Roblox saíram do `blocked_apps.json`.

**Importante:** PCs com o agente antigo continuam matando o Roblox até
receberem esta versão. Faça um **Reinstalar Monitor (com UAC)** (ou o primeiro
push) uma vez; depois as atualizações são sem UAC. O `lab_agent.ps1` embutido
foi ressincronizado.

**Arquivos:** `data/repo/plugins/lab_agent.py`,
`data/repo/plugins/lab_agent.ps1`, `data/repo/plugins/lab_monitor.py`,
`data/repo/plugins/lab_receiver.py`, `data/repo/plugins/blocked_apps.json`,
`docs/ISSUES_LOCAIS.md`.

**Validar:** abrir o Roblox e deixá-lo rodando por vários minutos: o watchdog
não deve matá-lo (log sem `WATCHDOG: bloqueado Roblox...`). Enviar **Bloquear
Jogos** deve fechá-lo na hora. `py_compile` e parser dos `.ps1` OK.

---

## IS-105 — Dois servidores em conjunto (notebook + PC do laboratório) 🟢

**Pedido:** subir o servidor automaticamente com o Windows no PC do
laboratório e fazê-lo trabalhar junto com o do notebook. Quem está online
segura o comando; o que inicia depois vira assistente. Ambos enxergam as
máquinas e enviam instruções.

**Como funciona:**
- Cada `lab_receiver.py` tem `SERVER_ID`/`SERVER_STARTED_AT` e anuncia-se por
  **UDP 5002** (`SYSAVA_PEER_DISCOVER`) e também pela **UDP 5001** já liberada
  para os agentes. Fallback manual: `peers.txt` (uma URL por linha) ou
  `PEER_URLS=http://ip:5000,...` no `.env`.
- A cada 5 s cada servidor consulta `/api/peer/state` do outro e guarda
  máquinas, alunos e `started_at`. O dashboard e o `/api/status` mostram a
  **união** das máquinas (com `_owner`/`_peer`), então o radar do Streamlit
  também vê as duas redes.
- Comandos do dashboard web ou do Streamlit vão para `/api/command`; o
  servidor grava localmente se a máquina é dele e, se for do outro, encaminha
  para `/api/peer/command`. Os dois conseguem mandar instruções.
- **Papel:** entre os servidores online, o que tem `started_at` mais antigo é
  **primário**; o que subiu depois é **assistente**. O papel aparece no topo do
  dashboard e é recalculado quando o peer expira (30 s), então há failover se
  o primário cair.
- Os agentes continuam escolhendo um servidor pelo UDP 5001 e fazem failover
  sozinhos se ele sumir; o outro servidor recebe o comando por encaminhamento.
- **Auto-start:** `instalar_servidor_auto.ps1` registra a tarefa agendada
  **SysAva Servidor**, abre TCP 5000/UDP 5001 e 5002 e inicia agora.
  `-Remover` desfaz. (Desde o **IS-111** o padrão é boot/SYSTEM com watchdog;
  `-Logon` mantém o modo antigo de logon do usuário.)
- O `/servidor.zip` inclui `instalar_servidor_auto.ps1` e `lab_agent.py`; o
  card **7** do `/setup` traz o download.

**Arquivos:** `data/repo/plugins/lab_receiver.py`,
`data/repo/plugins/instalar_servidor_auto.ps1`,
`data/repo/plugins/INICIAR_SERVIDOR.ps1`,
`data/repo/plugins/lab_monitor.py`, `docs/ISSUES_LOCAIS.md`.

**Como aplicar no PC do laboratório:**
1. Copiar/baixar a pasta `plugins` nova (`servidor.zip`) e criar o `.env`.
2. Rodar `INICIAR_SERVIDOR.bat` uma vez como Administrador (Python/deps/firewall).
3. Rodar `instalar_servidor_auto.ps1` como Administrador.
4. Subir/reiniciar o servidor do notebook com o `lab_receiver.py` novo; ele
   encontra o PC sozinho. Se não encontrar, use `peers.txt`.

**Validar:** com os dois online, abrir o dashboard de cada um: as máquinas dos
dois aparecem (marcadas “via <host>”), o papel aparece como primário/assistente
e um comando enviado de qualquer um chega ao agente. `py_compile` e parser dos
`.ps1` OK.

---

## IS-106 — Atualizar a pasta do servidor exige reiniciar o processo 🟢

**Sintoma:** trocar o `lab_receiver.py` na pasta em uso “não mudava nada”:
o dashboard continuava sem as funções novas (peers, versão, `/api/command`).
O `servidor.zip` baixado também podia vir do processo antigo.

**Causa:** Python carrega o `.py` em memória. Substituir o arquivo no disco
não recarrega o processo que já está na porta 5000. Se o `lab_receiver.bat`
(loop de auto-recuperação) ou a tarefa **SysAva Servidor** estiverem rodando,
a instância antiga continua atendendo; uma nova tentativa de subir morre no
check “PORTA 5000 JÁ EM USO”.

**Mudança:**
- Novo `reiniciar_servidor.ps1`: encerra `lab_receiver.py`, o loop do
  `lab_receiver.bat` e `INICIAR_SERVIDOR.ps1`, espera a porta 5000 liberar,
  reinicia pela tarefa **SysAva Servidor** (se ela apontar para esta pasta) ou
  diretamente pelo Python (`.python` → `.sysenv` → PATH) e confere
  `/health`. Use `-Parar` para só encerrar.
- `/health` e `/api/peer/state` passaram a retornar `version`, `role`,
  `server_id` e `peers`; o dashboard mostra `v2026-10-20-cluster`. Se o
  `/health` não tiver `version`, o processo rodando é antigo.
- O `/servidor.zip` agora inclui automaticamente qualquer `.ps1`/`.bat` da
  pasta, envia `Cache-Control: no-store` e `X-SysAva-Version`; o `/setup`
  mostra a versão em execução e o link do zip com `?v=<versao>`. Ainda assim,
  o zip é montado pelo **processo em memória**: só após reiniciar ele passa a
  trazer os arquivos novos.
- O script avisa quando a tarefa agendada aponta para outra pasta/arquivo
  (aí rode `instalar_servidor_auto.ps1` na pasta correta).
- `reiniciar_servidor.ps1` entra no `/servidor.zip`, no whitelist de download
  e no card 7 do `/setup`.

**Se o Windows reclamar de assinatura/execução de scripts:**
- Rode pelo **`.bat`** (`reiniciar_servidor.bat` / `instalar_servidor_auto.bat`),
  que chama o PowerShell com `-ExecutionPolicy Bypass`.
- Ou, no PowerShell:
  `Unblock-File .\reiniciar_servidor.ps1`
  `powershell -NoProfile -ExecutionPolicy Bypass -File .\reiniciar_servidor.ps1`
- Se uma política de grupo (GPO) bloquear tudo, faça o restart inline:
  `Get-CimInstance Win32_Process | ? { $_.CommandLine -match 'lab_receiver\.py|lab_receiver\.bat' } | % { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }`
  e `Start-ScheduledTask -TaskName "SysAva Servidor"`.

**Passo a passo para atualizar o PC do laboratório:**
1. Baixar o `servidor.zip` novo e extrair **sobre** a pasta em uso (conferir
   que `lab_receiver.py` ficou na raiz, com a data/hora nova).
2. Rodar `reiniciar_servidor.ps1` como Administrador.
3. Conferir `http://127.0.0.1:5000/health` → `version: 2026-10-20-cluster`.

**Arquivos:** `data/repo/plugins/lab_receiver.py`,
`data/repo/plugins/reiniciar_servidor.ps1`,
`data/repo/plugins/instalar_servidor_auto.ps1`, `docs/ISSUES_LOCAIS.md`.

**Validar:** antes de reiniciar, `/health` sem `version`; depois, com a versão
nova. `py_compile` e parser dos `.ps1` OK.

---

## IS-107 — Guia rápido de instalação do Flutter 🟢

**Pedido:** um tutorial mais simples, só para baixar, instalar e testar o
Flutter, a partir do material em `plugins/atividades`.

**Mudança:** criado `plugins/atividades/flutter-instalar-e-testar.md`:
- instalação do Git (winget ou site);
- download do Flutter SDK stable (ZIP oficial ou `git clone`);
- extração em `C:\src\flutter` e inclusão de `C:\src\flutter\bin` no PATH;
- teste com `flutter --version`, `flutter doctor`, `flutter create meu_app`,
  `flutter test` e, opcionalmente, `flutter run -d chrome`/`flutter build web`;
- o que é normal no `flutter doctor` (X em Android/Visual Studio);
- problemas comuns, atualização/remoção e checklist.

Os tutoriais `flutter-android-e-web.md` e `Android-sdk-tools-flutter.md`
ganharam uma nota no topo apontando para o guia curto.

**Arquivos:** `plugins/atividades/flutter-instalar-e-testar.md`,
`plugins/atividades/flutter-android-e-web.md`,
`plugins/atividades/Android-sdk-tools-flutter.md`,
`docs/ISSUES_LOCAIS.md`.

**Validar:** seguir o guia em um PC sem Flutter e conferir o checklist final
(`where.exe flutter`, `flutter --version`, `flutter test`).

---

## IS-108 — Tela de bloqueio: RA falhava com o notebook offline 🟢

**Sintoma:** a tela de bloqueio não aceitava o RA dos alunos. O overlay
tentava validar 5 vezes e terminava em “Servidor indisponivel. Use a senha do
administrador.”

**Causa:** o `sysava_lock.ps1` usava direto a URL `-Server` gravada na
instalação (normalmente o notebook). Se o notebook estava desligado e o PC do
laboratório era o servidor online, o lock continuava tentando o IP antigo/
offline, sem cair para a descoberta. O endpoint `/api/auth_ra` está OK (testado
com RA real do Supabase: 200 para aluno, 404 para RA inexistente).

**Mudança:** `Get-SysAvaServer` agora:
1. testa `/health` da URL `-Server` e só a usa se responder;
2. senão testa o cache do agente (`C:\Local\SysVa_lab\server_cache.txt`);
3. senão faz broadcast UDP 5001, escuta **mais de uma** resposta (notebook/PC
   do laboratório) e testa `/health` de cada uma;
4. só retorna vazio se nenhum servidor responder.

Assim o RA valida no servidor que estiver online, inclusive quando o notebook
cai. O `Get-SysAvaServer` também é usado pelo bootstrap de auto-atualização da
tela, então ela baixa a versão do servidor correto.

**Importante:** o PC precisa estar com a versão da tela que tem
`Start-FromLocalCopy`/`Get-SysAvaServer` novo (IS-102/IS-108). Se a cópia
instalada em `C:\ProgramData\SysAva` for antiga, reinstale uma vez pelo
`/setup` card 3; depois ela se auto-atualiza no logon.

**Arquivos:** `data/repo/plugins/sysava_lock.ps1`,
`docs/ISSUES_LOCAIS.md`.

**Validar:** com o notebook desligado e o PC do laboratório online, abrir a
tela e digitar um RA válido: deve liberar. `py_compile`/parser do `.ps1` OK.

---

## IS-109 — Comando remoto para atualizar a tela de bloqueio 🟢

**Pedido:** atualizar a tela de bloqueio nos PCs sem acessar cada máquina e
sem UAC.

**Como funciona (`Atualizar Tela de Bloqueio (sem UAC)`):**
- O agente baixa `sysava_lock.ps1`, `wallpaper_sysava.png` e `logo_sysava.png`
  de `/download/...` para `%LOCALAPPDATA%\SysAva`.
- Encerra a tela antiga (`fechar_tela_bloqueio`, que também restaura
  `DisableTaskMgr`) e abre a cópia local com `-SemAtualizar` e `-Server`.
- Se `C:\ProgramData\SysAva\sysava_lock.ps1` já tem o bootstrap
  (`Start-FromLocalCopy`), não cria nada extra: o bootstrap usa a cópia local
  no próximo logon. Se não tem, cria
  `%APPDATA%\...\Startup\SysAva Lock (usuario).vbs` apontando para a cópia
  local (sem Administrador).
- A tela nova tem `Close-OtherLocks`: encerra outra instância de
  `sysava_lock.ps1` na mesma sessão nos primeiros 10 s, evitando duas telas
  quando o CommonStartup antigo e o Startup do usuário coexistem.
- `Restore-Policies` agora remove `DisableTaskMgr` quando o valor anterior já
  era `1` (tela encerrada à força), em vez de deixá-lo desabilitado.

**Ação:** disponível no dashboard web (`ACOES_CONTROLE`) e no plugin Streamlit
(selectbox de ações). O agente trata antes de `Atualizar Monitor`.

**Arquivos:** `data/repo/plugins/lab_agent.py`,
`data/repo/plugins/lab_agent.ps1`, `data/repo/plugins/lab_receiver.py`,
`data/repo/plugins/lab_monitor.py`,
`data/repo/plugins/sysava_lock.ps1`, `docs/ISSUES_LOCAIS.md`.

**Validar:** selecionar uma máquina no Monitor → **Atualizar Tela de Bloqueio
(sem UAC)**. Conferir `%LOCALAPPDATA%\SysAva\sysava_lock.ps1` com a data nova
e a tela abrindo. No próximo logon, deve continuar a versão nova sem UAC.
`py_compile` (agente + embutido) e parser dos `.ps1` OK.

---

## IS-110 — Dashboard demorava a remover PCs desligados 🟢

**Sintoma:** máquinas já desligadas continuavam no dashboard e a página não
se atualizava sozinha; era preciso clicar em **Atualizar** (e às vezes o
navegador ainda mostrava a versão em cache).

**Causa:** o filtro do dashboard web era de **300 s (5 min)** e não havia
auto-refresh. O fallback do plugin Streamlit lia o `lab_status.json` inteiro,
sem filtrar os timestamps.

**Mudança:**
- `OFFLINE_SECONDS = 60` no `lab_receiver.py`: dashboard, `/api/peer/state` e
  a escolha local/peer em `dispatch_commands` usam 60 s (o agente pinga a
  cada 10 s). `/api/status` continua com 30 s para o radar ao vivo.
- O dashboard recarrega sozinho a cada **15 s**, mas pausa enquanto houver
  máquina marcada (para não perder a seleção).
- Respostas HTML recebem `Cache-Control: no-store` (link **Atualizar** não
  mostra mais página velha).
- O fallback do `lab_monitor.py` (quando o receiver está fora) filtra por
  `OFFLINE_SECONDS` em vez de devolver todo o JSON antigo.

**Arquivos:** `data/repo/plugins/lab_receiver.py`,
`data/repo/plugins/lab_monitor.py`, `docs/ISSUES_LOCAIS.md`.

**Validar:** desligar uma máquina e aguardar ~60 s; com a página aberta (sem
checkbox marcado), ela deve sumir em até ~75 s. `py_compile` OK.

---

## IS-111 — Servidor do monitor no PC do laboratório inicia com o Windows 🟢

**Pedido:** deixar o servidor do monitor (`lab_receiver.py`) em um PC fixo do
laboratório subindo sozinho com o Windows, sem depender de abrir o
`INICIAR_SERVIDOR.bat` nem de um usuário logado.

**Antes:** o `instalar_servidor_auto.ps1` registrava a tarefa **SysAva Servidor**
no **logon do usuário atual**. Em PC compartilhado, ela só subia depois que
aquele usuário entrava; se o receiver caísse, a tarefa só tentava reiniciar 3
vezes; e o `.bat`/manual podia deixar duas instâncias disputando a porta 5000.
O `-Port` do `INICIAR_SERVIDOR.ps1` também era ignorado (porta fixa 5000).

**Mudança:**
- `instalar_servidor_auto.ps1` agora registra por padrão **AtStartup como
  SYSTEM** (sem exigir usuário logado). `-Logon` mantém o comportamento antigo;
  `-System` continua aceito por compatibilidade.
- A tarefa roda o novo `servidor_watchdog.ps1`, que reinicia o `lab_receiver.py`
  a cada 5 s se ele encerrar e grava `servidor.log` (rotação em 5 MB).
- Configuração da tarefa: `MultipleInstances IgnoreNew` (não duplica),
  `RestartCount 999`, sem limite de execução, `StartWhenAvailable`, não para em
  bateria/idle.
- O instalador confere/instala `flask, waitress, filelock, requests, bcrypt,
  python-dotenv`, avisa se faltar `.env` e se a pasta estiver em caminho de rede
  (SYSTEM pode não ver a rede), abre TCP 5000/UDP 5001/5002 e testa `/health`.
- `reiniciar_servidor.ps1` passou a encerrar o watchdog antes do Python e a
  aceitar a tarefa apontando para o watchdog (ou para o receiver antigo).
- O `LAB_PORT` (definido pelo `INICIAR_SERVIDOR.ps1 -Port`) agora é respeitado
  pelo receiver (antes a porta 5000 era fixa).
- Com os **dois servidores online** (notebook + PC01-LAB02), o
  `dispatch_commands` passou a escolher o servidor cujo último reporte da
  máquina é o mais recente (margem de 5 s para relógio), em vez de sempre
  preferir o local. Assim, um comando enviado de qualquer um dos dois chega ao
  agente mesmo quando ele trocou de servidor por failover/reinício. O papel
  primário/assistente continua apenas informativo.
- O auto-start deve ser instalado **no PC fixo**; no notebook, se desejado, use
  `-Logon` (não SYSTEM). Com `PEER_TOKEN`, usar o **mesmo valor nos dois `.env`**
  (ou deixar em branco nos dois).
- `servidor_watchdog.ps1` entrou no `DOWNLOAD_WHITELIST` e no `/servidor.zip`
  (que já inclui automaticamente todo `.ps1`/`.bat` novo).
- Card 7 do `/setup` e `lab_monitor_doc.md` atualizados (boot por padrão,
  `-Logon`, watchdog e log).

**Arquivos:** `data/repo/plugins/instalar_servidor_auto.ps1`,
`data/repo/plugins/servidor_watchdog.ps1`,
`data/repo/plugins/reiniciar_servidor.ps1`,
`data/repo/plugins/lab_receiver.py`,
`data/repo/plugins/lab_monitor_doc.md`, `docs/ISSUES_LOCAIS.md`.

**Como usar no PC do laboratório:**
1. Rodar uma vez o `INICIAR_SERVIDOR.bat` na pasta do servidor (baixa Python e
   dependências) e conferir o `.env`.
2. Rodar `instalar_servidor_auto.bat` como Administrador (aceitar o UAC).
3. Conferir `http://127.0.0.1:5000/health` e o `servidor.log`.
4. Reiniciar o PC e, sem logar em nada, abrir `http://<ip-do-pc>:5000/` de outra
   máquina.
5. Para atualizar o código: extrair o `servidor.zip` sobre a pasta e rodar
   `reiniciar_servidor.bat`.
6. Para remover o auto-start: `instalar_servidor_auto.bat -Remover`.

**Validar:** nos três `.ps1`, `[System.Management.Automation.Language.Parser]`
sem erros; `python -m py_compile lab_receiver.py`; `schtasks /query /tn "SysAva
Servidor"` mostrando `SYSTEM` + `At Start-up`; `/health` respondendo após reboot
sem usuário logado. Observação: a máquina de desenvolvimento já tinha um
receiver manual na porta 5000 — nesse caso o instalador avisa e não sobe uma
segunda instância (use `reiniciar_servidor.bat` para trocar pela tarefa).

---

## IS-112 — Tela de bloqueio presa em “Servidor indisponível (1/5)” 🟢

**Fluxo esperado:** o professor chega, liga o **PC01-LAB02** (servidor) e só
depois os alunos usam as máquinas; o notebook fica para gerenciamento/comandos.
Na prática, as máquinas dos alunos podem terminar o boot antes de o receiver do
PC01 estar aceitando conexões.

**Sintoma:** a tela de bloqueio encontrava o servidor pela descoberta, mas o
`/api/auth_ra` ainda recusava/conectava; ela tentava **5 vezes (~8 s)** e
terminava em “Servidor indisponivel. Use a senha do administrador.” — o aluno
precisava clicar de novo (e o RA não era revalidado sozinho).

**Mudança (`sysava_lock.ps1`):**
- Se o servidor ainda não responde, a tela agora **aguarda até 3 minutos**,
  redescoberto o servidor a cada ~2 s (URL `-Server` → cache do agente → UDP
  5001), mostrando “Aguardando o servidor do laboratorio iniciar... (Ns)”.
- Se encontrou o servidor mas a autenticação ainda falha por rede, mostra
  “Servidor encontrado; aguardando liberar a tela... (Ns)” e continua tentando
  **com o mesmo RA**, sem exigir nova digitação.
- Nova função `Wait-UI` usa `Application.DoEvents()`: a janela continua
  respondendo, o foco/TopMost não trava e a **senha do administrador** ainda
  pode ser usada durante a espera (o handler checa admin antes de aguardar).
- Guarda `$script:aguardandoServidor` evita reentrada de cliques duplicados.
- Após 3 min sem servidor, mostra a mensagem final e permite tentar de novo.
- O instalador do servidor não usa mais o atraso de 15 s no boot: a tarefa
  inicia o quanto antes, reduzindo a janela de espera dos alunos.

**Arquivos:** `data/repo/plugins/sysava_lock.ps1`,
`data/repo/plugins/instalar_servidor_auto.ps1`, `docs/ISSUES_LOCAIS.md`.

**Como aplicar nos PCs dos alunos:** o lock se auto-atualiza no próximo logon a
partir do `/download/sysava_lock.ps1` do servidor. Se as máquinas estiverem
presas com a versão antiga, use o comando **Atualizar Tela de Bloqueio (sem
UAC)** no Monitor (IS-109) ou reinstale pelo `/setup` card 3 uma vez.

**Validar:** 1) desligar o PC01 e abrir a tela em outro PC; tentar um RA e
confirmar a mensagem de espera; 2) ligar o PC01 e, sem clicar de novo, ver a
tela liberar quando o servidor subir; 3) digitar `labadmin` durante a espera e
confirmar que o admin ainda libera; 4) parser do `.ps1` sem erros.

---

## IS-113 — Comando para PC desligado executava horas depois 🟢

**Sintoma:** o professor mandava **Desligar** ou **Reiniciar** para todas as
máquinas; as que estavam desligadas ficavam com o comando pendente no
`lab_status.json` e o executavam no dia seguinte (ou depois de duas aulas),
quando o aluno ligava o PC.

**Causa:** `pending_command` não tinha validade. O `command_ts` era só
`HH:MM:SS` (sem data), então não havia como saber se o comando era de agora ou
de ontem; o `/ping` entregava qualquer pendência no próximo reporte do agente.

**Mudança:**
- Todo comando agora grava `command_created_at` e `command_expires_at`
  (epoch). Padrão: **30 minutos** (`COMMAND_TTL_SECONDS=1800`; pode ser
  ajustado no `.env`/ambiente do servidor).
- No `/ping`, antes de entregar, o receiver chama `_comando_expirado()`: se
  venceu, descarta (com log `COMANDO EXPIRADO descartado para ...`) e responde
  sem `pending_command`.
- Comando antigo gravado por versão anterior (sem `command_expires_at`) é
  tratado como vencido — mais seguro do que desligar o PC do aluno horas
  depois.
- `lab_monitor.py` também grava os campos de validade nos fallbacks locais e
  passou a tentar o receiver **antes** de escrever localmente (evita duplicar
  comando em massa).
- A resposta do `/ping` inclui `command_expires_at` (o agente atual ignora,
  mas ajuda em diagnóstico).

**Arquivos:** `data/repo/plugins/lab_receiver.py`,
`data/repo/plugins/lab_monitor.py`, `docs/ISSUES_LOCAIS.md`.

**Validar:** 1) com o PC desligado, enviar `Desligar PC (Shutdown)` e conferir
`command_expires_at` no `lab_status.json`; 2) simular o `/ping` depois de
vencido e confirmar que não retorna `pending_command` e que o log registra o
descarte; 3) com o PC ligado, enviar o comando e confirmar execução normal
(pendência entregue e limpa); 4) `py_compile` OK.

---

## IS-114 — Identificação de máquina e aluno no painel 🟢

**Sintoma:** o painel web mostrava o **hostname cru** (`22139923-LAB-60040`,
`DESKTOP-7H3URJE`) e usava a **conta Windows** (`ALUNO`) como se fosse o aluno
quando não havia RA associado. Além disso, uma associação antiga podia continuar
aparecendo para o próximo aluno.

**Mudança:**
- O painel web passou a usar o **rótulo** de `lab_labels.json`
  (ex.: `22139923-LAB-60040 → PC04-LAB02`) como nome principal; o hostname
  continua visível em letra pequena (chave técnica usada por comandos/agente).
- Nova página **🏷️ Rótulos** (`/rotulos`) no painel web para editar os nomes
  das máquinas (mesmo arquivo usado pelo Streamlit). Antes isso só existia no
  expander do Streamlit.
- A coluna **Aluno (RA)** mostra o nome completo + RA associado pela tela de
  bloqueio; se não houver, mostra **“sem RA”**. A conta Windows aparece como
  **“conta: ALUNO”** apenas como informação secundária.
- A associação aluno↔máquina vale por **16 h** (`USER_MAP_TTL_SECONDS=57600`):
  evita mostrar o aluno anterior depois de uma sessão antiga. O lock continua
  sobrescrevendo no próximo RA.
- Busca de hostname/rótulo/aluno agora é **case-insensitive** e ignora espaços,
  evitando divergência entre `COMPUTERNAME` (tela de bloqueio) e
  `socket.gethostname()` (agente).
- Detalhes da máquina (`/detalhes`) usam o rótulo no título e separam
  “Aluno (RA)” de “Conta Windows”.

**Arquivos:** `data/repo/plugins/lab_receiver.py`,
`data/repo/plugins/lab_monitor.py`, `docs/ISSUES_LOCAIS.md`.

**Como usar:** abrir o painel web no notebook → **🏷️ Rótulos** → preencher os
nomes (ex.: `PC01-LAB02`, `PC04-LAB02`) → salvar. O Streamlit continua lendo o
mesmo `lab_labels.json`. O aluno aparece após o RA na tela de bloqueio; sem RA,
o painel mostra “sem RA” em vez de `ALUNO`.

**Validar:** painel mostrando rótulo + host, aluno “NOME (RA)” e “conta: ALUNO”
em linha secundária; máquina sem RA mostrando “sem RA”; `/rotulos` salvando e
refletindo no painel; associação com mais de 16 h não exibida; `py_compile` OK
e teste do Flask client nos templates (`/`, `/detalhes`, `/rotulos`).

---

## IS-115 — Seletor de aluno na tela de bloqueio e RA no login 🟢

**Pedido:** o aluno esquece/esquece o RA ou tem preguiça de digitar. A tela de
bloqueio deve oferecer uma **lista de alunos** e abrir o SysAva já com o RA
escolhido.

**Mudança:**
- Novo endpoint **`/api/alunos`** no receiver: lista `{ra, name}` dos alunos
  (`app_users.role = student`), ordenada por nome. Cache em memória de **30 min**
  + cópia em `alunos_cache.json` no disco do servidor, para o **PC01** servir o
  seletor mesmo depois de reiniciar e antes de o Supabase responder — o notebook
  não é necessário. Se o banco estiver fora, devolve a última lista conhecida.
- `sysava_lock.ps1`: o campo de texto virou um **ComboBox** com
  auto-complete (dá para digitar para filtrar) exibindo `NOME COMPLETO - RA`.
  A lista é cacheada em `%LOCALAPPDATA%\SysAva\alunos.json`, então aparece mesmo
  se o PC01 ainda estiver subindo; se não houver cache, uma timer tenta carregar
  do servidor por até ~2 min.
- O **último RA não é mais pré-selecionado** (evita liberar/identificar o aluno
  anterior por engano). O aluno escolhe o próprio nome.
- O item escolhido é convertido de volta para o RA e validado em
  `/api/auth_ra` (o combo não substitui a validação no servidor).
- Ao liberar, o lock abre o SysAva com **`?ra=<RA>`** (antes abria a URL sem
  RA no início). A tela de login (`views/login.py`) lê `ra` de
  `st.query_params` e **preenche o campo Usuário**; a senha continua sendo
  exigida.
- Correção de regressão: em PowerShell `$url` e `$Url` são a **mesma variável**
  (case-insensitive). A URL local de `/api/auth_ra` sobrescrevia a URL do portal
  e o navegador abria o **JSON da API**. Agora a variável local é `$authUrl` e a
  função usa `$script:Url`, garantindo abrir o `sysava.streamlit.app?ra=...`.
- O link “Abrir sysava.streamlit.app” também usa o RA selecionado, quando houver.
- A senha do administrador continua funcionando durante a espera pelo servidor
  e abre o portal sem RA.

**Arquivos:** `data/repo/plugins/sysava_lock.ps1`,
`data/repo/plugins/lab_receiver.py`, `views/login.py`,
`data/repo/plugins/lab_monitor_doc.md`, `docs/ISSUES_LOCAIS.md`.

**Validar:** 1) `/api/alunos` retornando nome/RA e usando cache; 2) lock com o
combo preenchido (inclusive a partir do cache com o servidor desligado);
3) escolher um aluno, liberar e conferir `https://sysava.streamlit.app/?ra=...`
com o campo Usuário preenchido; 4) senha do admin ainda libera; 5) parser do
`.ps1`, `py_compile` do receiver/login e teste Flask de `/api/alunos`.

---

## IS-116 — Opera subindo com o Windows 🟢

**Sintoma:** o Opera abria sozinho na inicialização (Run/RunOnce ou atalho na
pasta Startup), atrapalhando a aula e sendo reportado como janela ativa.

**Mudança:**
- `limpar_inicializacao_roblox()` foi generalizada para
  `_limpar_inicializacao(termos, encerrar_processos=True)`, reaproveitada por:
  - `limpar_inicializacao_roblox()` (mantém o comportamento antigo);
  - `limpar_inicializacao_opera()` (novo).
- O limpador do Opera remove valores em **Run/RunOnce** (HKCU/HKLM/WOW6432),
  atalhos nas pastas **Startup** (usuário e todos) e **tarefas agendadas** com
  “Opera” no nome — ignorando tarefas de **update/atualização** para não
  quebrar o updater. Ele **não mata** o Opera aberto manualmente; fecha apenas
  processos `opera.exe` que tenham `--autostart` na linha de comando.
- O agente roda essa limpeza no início (quando `AUTO_BLOCK=True`), junto com a
  do Roblox; assim, mesmo que o Opera reative o auto-start, ele é removido no
  próximo logon/início do agente.
- Novo comando **Limpar Inicialização do Opera (bandeja)** no Monitor (web e
  Streamlit) e nas ações em massa, para aplicar na hora sem reiniciar o PC.
- `lab_agent.ps1` (instalador com o Python embutido) recebeu as mesmas funções
  e o mesmo tratamento de comando.

**Arquivos:** `data/repo/plugins/lab_agent.py`,
`data/repo/plugins/lab_agent.ps1`, `data/repo/plugins/lab_receiver.py`,
`data/repo/plugins/lab_monitor.py`, `data/repo/plugins/lab_monitor_doc.md`,
`docs/ISSUES_LOCAIS.md`.

**Como aplicar:** atualizar a pasta `plugins` dos servidores (`servidor.zip`) →
reiniciar o receiver → no Monitor selecionar as máquinas e enviar
**Atualizar Monitor (rápido, sem UAC)** (baixa o `lab_agent.py` novo e
reinicia). Ao reiniciar, o agente já limpa o auto-start do Opera; se quiser
aplicar sem esperar, envie também **Limpar Inicialização do Opera (bandeja)**.
O `blocked_apps.json` **não** inclui Opera (não é para matar o navegador).

**Validar:** em um PC de teste, conferir que não há valor “Opera” em
`HKCU\...\Run`/`RunOnce`, atalho na pasta Startup nem tarefa de inicialização;
reiniciar o PC e confirmar que o Opera **não** abre sozinho; abrir o Opera
manualmente e confirmar que ele **continua aberto**. `py_compile` do
`lab_agent.py` e do Python embutido no `.ps1` OK.

---

## IS-117 — Apps Microsoft subindo com o Windows 🟢

**Pedido:** tirar da inicialização o **Outlook, OneDrive** e outros apps da
Microsoft que abrem sozinhos no laboratório.

**Mudança:**
- Lista `MICROSOFT_STARTUP_KEYWORDS` com: `onedrive`, `outlook`, `teams`,
  `ms-teams`, `msteams`, `onenote`, `skype`, `copilot`, `microsoft edge`,
  `msedge`, `yourphone`, `phoneexperiencehost`, `gamebar`, `xbox`, `widgets`,
  `cortana`, `officehub`, `microsoft office`, `microsoft365`/`microsoft 365`.
- Nova `limpar_inicializacao_microsoft()`: remove **Run/RunOnce**,
  **atalhos na pasta Startup** e tarefas de **startup/logon** que casem com a
  lista. Não fecha Outlook/OneDrive/Teams em uso; só remove o auto-start.
- `_limpar_inicializacao()` ganhou `tarefas_startup=True`: para os apps
  Microsoft só apaga tarefas cujo nome tenha `startup`/`logon`/`inicio`, e
  ignora `update`/`atualiz`/`install`/`setup` — evita quebrar atualizadores e
  instaladores (ex.: `MicrosoftEdgeUpdate`, `Teams Machine-Wide Installer`).
- O agente aplica no início (junto com Roblox/Opera) e há o comando
  **Limpar Inicialização de Apps Microsoft (bandeja)** no Monitor web,
  Streamlit e ações em massa.
- `lab_agent.ps1` (Python embutido) recebeu as mesmas mudanças.

**Arquivos:** `data/repo/plugins/lab_agent.py`,
`data/repo/plugins/lab_agent.ps1`, `data/repo/plugins/lab_receiver.py`,
`data/repo/plugins/lab_monitor.py`, `data/repo/plugins/lab_monitor_doc.md`,
`docs/ISSUES_LOCAIS.md`.

**Como aplicar:** atualizar `servidor.zip` nos servidores → reiniciar o
receiver → no Monitor enviar **Atualizar Monitor (rápido, sem UAC)** para baixar
o agente novo → opcionalmente **Limpar Inicialização de Apps Microsoft
(bandeja)** para aplicar na hora. No próximo logon o agente também limpa.

**Validar:** em um PC de teste, conferir que Outlook/OneDrive/Teams não estão
em `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` nem na pasta Startup;
reiniciar e ver que não abrem sozinhos; abrir cada um manualmente e confirmar
que continuam funcionando. `py_compile` do `lab_agent.py` e do Python embutido
no `.ps1` OK.

---

## IS-118 — Fechar / Bloquear / Desbloquear Sites/Jogos 🟢

**Pedido:** nas ações do Monitor, ter **Fechar**, **Bloquear** e
**Desbloquear** para YouTube, Roblox, Loki, outros games e redes sociais.

**Mudança:**
- Três novas ações no Monitor web/Streamlit (e botões em massa):
  - **Fechar Sites/Jogos (YouTube/Roblox/Loki/Games/Redes)** — fecha agora
    (mata processos de jogos/Roblox e fecha janelas cujo título contenha
    YouTube/Loki/games/redes); não mantém bloqueio.
  - **Bloquear Sites/Jogos (...)** — grava `block_state.json` no PC e o
    watchdog passa a fechar janelas e derrubar processos de jogos/Roblox a
    cada ciclo (~4 s) **até desbloquear**.
  - **Desbloquear Sites/Jogos (...)** — remove `block_state.json`; o watchdog
    volta ao comportamento normal (sem fechar Roblox/YouTube sozinho).
- Sem bloqueio ativo, o Roblox continua fora do auto-bloqueio (só o comando
  manual “Bloquear Jogos” o fecha). Com bloqueio ativo, o watchdog inclui o
  Roblox e fecha as janelas das categorias.
- O estado sobrevive a reboot/atualização do agente; é local por PC. O comando
  de bloqueio pode ser enviado para todas as máquinas de uma vez.

**Limitação:** sem privilégio de Administrador o agente não altera `hosts` nem
firewall; o “bloqueio” é por **watchdog** (fecha janelas por título e mata
processos). Para bloquear por DNS/hosts, use `bloquear_hosts.ps1` com UAC.

**Arquivos:** `data/repo/plugins/lab_agent.py`,
`data/repo/plugins/lab_agent.ps1`, `data/repo/plugins/lab_receiver.py`,
`data/repo/plugins/lab_monitor.py`, `data/repo/plugins/lab_monitor_doc.md`,
`docs/ISSUES_LOCAIS.md`.

**Como aplicar:** atualizar o `servidor.zip` → reiniciar o receiver → enviar
**Atualizar Monitor (rápido, sem UAC)** para os PCs (para o agente entender as
ações novas) → enviar **Bloquear** ou **Desbloquear** conforme a aula.

**Validar:** 1) “Fechar” derruba Roblox/jogo aberto e fecha a janela do
YouTube/Loki; 2) “Bloquear” faz o Roblox/janela voltar a ser fechado se o aluno
reabrir; 3) “Desbloquear” permite abrir YouTube/Roblox normalmente; 4)
`block_state.json` aparece/desaparece na pasta do agente; 5) `py_compile` do
agente e do Python embutido no `.ps1` OK.

---

## IS-119 — Admin/Avaliações: editar o nome da avaliação 🟢

**Pedido:** na página **Admin → Avaliações**, poder **editar o nome** (título)
de uma avaliação já criada (ex.: `Prog_Mobile Grupo1 Aulas:25-28`).

**Mudança:**
- Nova função `db.update_assessment_title(assessment_id, new_title)` em
  `services/database.py` (UPDATE em `assessments.title`).
- Na seção "Editando: …", novo expander **"✏️ Editar nome da avaliação"** com
  formulário (campo pré-preenchido com o título atual e botão **Salvar nome**).
- Validações: não permite título vazio; avisa quando o nome não mudou; mostra
  erro do banco, se houver.
- Após salvar, atualiza `st.session_state["sel_edit_av"]` para `tipo - novo
  título`, mantendo a avaliação selecionada no `selectbox` após o `rerun`.

**Arquivos:** `services/database.py`, `views/admin.py`,
`docs/ISSUES_LOCAIS.md`.

**Como validar:** 1) Admin → aba de avaliações → selecionar disciplina e uma
avaliação existente; 2) abrir **✏️ Editar nome da avaliação**, alterar o nome e
salvar; 3) confirmar que o cabeçalho "Editando:" e o `selectbox` exibem o novo
nome; 4) tentar salvar vazio (deve recusar); 5) `python -m py_compile
services/database.py views/admin.py`.

---

## IS-120 — Seminário Prog. Dispositivos Móveis: aulas 33–40 no SysAva 🟢

**Pedido:** subir ao SysAva, em aulas separadas, o seminário de Programação
para Dispositivos Móveis — Grupo1 (pesquisa 25–28, apresentação 33–36) e Grupo2
(pesquisa 29–32, apresentação 37–40), nas turmas 2A e 2B (carga horária 40h).

**Decisão:** a disciplina `PROGRAMAÇÃO PARA DISPOSITIVOS MÓVEIS` (`subject_id=5`)
é **compartilhada** entre 2A e 2B (`class_subjects`). Como os integrantes diferem
por turma, foi gerada uma **versão única neutra** (sem nomes de turma) e feito o
upsert uma vez; as duas turmas veem o mesmo material.

**Mudança (dados):** aulas criadas no Supabase (`lessons`, `subject_id=5`):

| ID | Título |
|----|--------|
| 740 | AULA 33 — Seminário: Widgets e Árvore de UI no Flutter |
| 742 | AULA 34 — Seminário: Modularização de Projetos Flutter |
| 743 | AULA 35 — Seminário: Debug e Performance no Flutter |
| 744 | AULA 36 — Seminário: Layouts e Design Responsivo no Flutter |
| 745 | Aula 37 Seminario Grupo2 A29 |
| 746 | Aula 38 Seminario Grupo2 A30 |
| 747 | Aula 39 Seminario Grupo2 A31 |
| 748 | Aula 40 Seminario Grupo2 A32 |

A Aula 32 (IMC) já existia (id 738). Fontes locais em
`data/repo/.../S05` (2A) e `data/Turmas/.../S05` (2A e 2B), com H1 = título.

**Como validar:** abrir o portal → Programação para Dispositivos Móveis → S05 →
conferir as aulas 33–40; ou consultar
`db.get_lessons_for_subject(5)` e verificar os títulos/IDs.

---

## IS-121 — Aula criada no Admin não aparecia na página Aulas 🟢

**Sintoma:** a professora (ex.: `adriana`) criava a aula em **Admin → Aulas**
com título fora do padrão `Aula N` (ex.: "Aula Teste", "A importância da
retenção de clientes"). A aula aparecia na lista do Admin/`st.dataframe`, mas
**não aparecia na página Aulas** (visão de professor).

**Causa:** `views/aulas.py` → `group_lessons()` usava
`get_lesson_number(title)` (regex `Aula\s*(\d+)`) e montava o agrupamento semanal
**apenas com aulas numeradas**. Aulas com `number=None` eram descartadas e o
grupo ficava vazio, então a tela não listava nada.

**Correção:** `group_lessons()` agora separa `numbered_lessons` e
`unnumbered_lessons`; as sem número entram no grupo
**"Outras aulas (sem número)"**, garantindo que toda aula criada apareça
(Admin, professor e aluno).

**Arquivos:** `views/aulas.py`, `docs/ISSUES_LOCAIS.md`.

**Validar:** criar uma aula com título sem "Aula N" em Admin → Aulas, abrir
**Aulas** → selecionar a turma/disciplina → a aula deve aparecer em
"Outras aulas (sem número)". Teste real: `subject 37` da turma 312076 mostrou
"A importância da retenção de clientes" após a correção.

---

## IS-122 — IA: aulas de seminário 36 e 37 (2A e 2B) 🟢

**Pedido:** criar duas aulas de Inteligência Artificial no formato Seminário,
com os temas das aulas **20–24** e **25–28**, para as duas turmas, usando os
grupos do seminário anterior.

**Mudança (dados):** 4 aulas no `subject_id=11` (INTELIGÊNCIA ARTIFICIAL), com
título por turma (a disciplina é compartilhada):

| ID | Título | Grupo |
|----|--------|-------|
| 756 | Aula 36 Seminário IA 1 (Aulas 20-24) - 2A | Grupo2 (2A) |
| 757 | Aula 37 Seminário IA 2 (Aulas 25-28) - 2A | Grupo1 (2A) |
| 758 | Aula 36 Seminário IA 1 (Aulas 20-24) - 2B | Grupo2 (2B) |
| 759 | Aula 37 Seminário IA 2 (Aulas 25-28) - 2B | Grupo1 (2B) |

Cada aula tem: organização dos tempos (60 min), objetivos, pesquisa das aulas
correspondentes, ilustrações (ASCII/Mermaid), roteiro cronometrado, perguntas,
checklist e referências. Fontes locais em
`data/Turmas/.../INTELIGÊNCIA ARTIFICIAL/S05/`.

**Como validar:** no portal, abrir Inteligência Artificial e conferir as aulas
36/37 de cada turma; ou `db.get_lessons_for_subject(11)` (IDs 756–759).

## IS-123 — DevOps: aulas 1–3 da S01 a partir dos PDFs (I-A e I-B) 🟢

**Pedido:** gerar as aulas a partir dos PDFs de aprofundamento
`texto_aprofundamento_aula_1.pdf`, `aula_2.pdf` e `aula_3.pdf` da pasta
`data/Turmas/2ª SÉRIE - Turma I-A (Técnico DS)/INTRODUÇÃO AO ECOSSISTEMA DEVops/S01/seductec`,
salvando no banco e no disco. Em seguida, criar a versão da turma
**2ª SÉRIE - Turma I-B (Técnico DS)**.

**Mudança (dados):**

| Turma | Disciplina | Aulas | IDs |
|-------|------------|-------|-----|
| I-A | `subject_id=9` (compartilhada) | 1, 2 e 3 | 900, 901, 902 |
| I-B | `subject_id=41` (nova, só I-B) | 1, 2 e 3 | 903, 904, 905 |

- A aula quebrada `id=899` (erro 404 do Gemini, sem conteúdo) foi removida.
- A disciplina nova da I-B foi criada como
  `INTRODUÇÃO AO ECOSSISTEMA DEVops (2ª SÉRIE - Turma I-B (Técnico DS))`
  e vinculada apenas à turma I-B (`class_id=2`), para não sobrescrever a I-A.
- Cada aula tem: objetivos, introdução, conteúdo teórico baseado no PDF,
  exemplo prático em Python executável, conclusão, links/referências e quiz
  com 4 perguntas × 4 alternativas (`4 questões` validadas por aula).
- Arquivos `.md` gravados em:
  - `data/Turmas/2ª SÉRIE - Turma I-A (Técnico DS)/INTRODUÇÃO AO ECOSSISTEMA DEVops/S01/`
  - `data/Turmas/2ª SÉRIE - Turma I-B (Técnico DS)/INTRODUÇÃO AO ECOSSISTEMA DEVops/S01/`

**Como validar:** abrir a disciplina no portal e conferir as aulas 1–3 de cada
turma; ou `db.get_lessons_for_subject(9)` (900–902) e
`db.get_lessons_for_subject(41)` (903–905), verificando `week="S01"` e o quiz
com 4 questões.

## IS-124 — Gerador de Aulas: DeepSeek Cloud 🟢

**Pedido:** adicionar a opção **DeepSeek Cloud** no Gerador de Aulas. A chave
deve ser buscada na variável `DEEPSEEK_API_KEY` e preenchida automaticamente
quando o app estiver rodando em modo local.

**Mudança (código):**

- `views/gerador_aulas.py`
  - nova opção `DeepSeek Cloud (Nuvem)` no seletor de IA;
  - `ia_source="deepseek"`, campo de chave e seletor de modelo
    (`deepseek-chat` / `deepseek-reasoner`);
  - helpers `_is_local_mode()` e `_deepseek_default_key()`: a chave só é
    pré-preenchida localmente (`.env` presente e sem marcadores de nuvem),
    lendo `DEEPSEEK_API_KEY` do ambiente ou de `st.secrets`;
  - DeepSeek entrou no limite de contexto de nuvem (32.000 caracteres) e no
    prompt completo de nuvem (não é tratado como modelo local).
- `services/ai_generation.py`
  - nova `generate_content_with_deepseek()` usando a API compatível com OpenAI
    (`https://api.deepseek.com`), com tratamento de erro amigável.

**Como validar:** no Gerador de Aulas, selecionar **DeepSeek Cloud (Nuvem)** e
conferir que a chave aparece preenchida em modo local; gerar uma aula e
verificar a resposta. Para testar sem interface:
`python -c "import views.gerador_aulas as g; print(bool(g._deepseek_default_key()))"`.

## IS-125 — Comando para definir o volume em 30% 🟢

**Pedido:** um comando no Monitor para deixar o volume de som dos PCs em 30%
(útil no início da aula), e outro para restaurar.

**Mudança:**
- Novo script `data/repo/plugins/definir_volume.ps1` usando a **Core Audio API**
  (`IAudioEndpointVolume.SetMasterVolumeLevelScalar` + `SetMute(false)`):
  `-Percent 30` deixa o volume em 30% e desmuta o dispositivo padrão de saída.
- O agente baixa esse script para `%LOCALAPPDATA%\SysAva\definir_volume.ps1`
  (com validação básica do conteúdo) e executa na **sessão do aluno**, sem UAC.
- Novas ações no Monitor web/Streamlit: **Definir Volume em 30%** e
  **Restaurar Volume (100%)**; botões em massa “Volume 30%/100% em TODAS”.
- `definir_volume.ps1` entrou no `DOWNLOAD_WHITELIST` e no `/servidor.zip`
  (que já inclui .ps1 automaticamente). O agente também tem as mesmas funções
  no Python embutido do `lab_agent.ps1`.

**Arquivos:** `data/repo/plugins/definir_volume.ps1`,
`data/repo/plugins/lab_agent.py`, `data/repo/plugins/lab_agent.ps1`,
`data/repo/plugins/lab_receiver.py`, `data/repo/plugins/lab_monitor.py`,
`docs/ISSUES_LOCAIS.md`.

**Como aplicar:** atualizar o `servidor.zip` → reiniciar o receiver (para
liberar `/download/definir_volume.ps1`) → enviar **Atualizar Monitor (rápido,
sem UAC)** aos PCs → enviar **Definir Volume em 30%** (ou 100%).

**Validar:** enviar o comando e conferir o ícone de volume do Windows em 30% e
desmutado; o script retorna 0; testar também o 100%. A leitura/escrita da API
foi validada localmente lendo e reaplicando o volume atual; não deixei o volume
do PC de desenvolvimento em 30% durante o teste.

## IS-126 — Gerador de Aulas: vídeo da aula via `links_aulas.md` 🟢

**Pedido:** o plano gerado não incluía o vídeo da aula que está no
`links_aulas.md` da pasta `seductec`.

**Causa:** o `links_aulas.md` não era sugerido por padrão na seleção de arquivos
da Rota 2 (o nome não contém o número da aula/semana) e, quando lido, o prompt
não informava qual vídeo correspondia à aula gerada.

**Mudança:**
- `services/contexto_aulas.py`
  - `links_aulas.md` passou a ser **sempre sugerido** e sempre lido na Rota 2;
  - novo `obter_link_video_aula(turma, disciplina, semana, numero_aula)`, que
    localiza a seção `### Aula_0N` e devolve o link correspondente;
  - a Rota 2 recebe `numero_aula` e adiciona o “VÍDEO OBRIGATÓRIO DA AULA N” ao
    contexto.
- `services/generate_lessons_gemini.py`
  - `gerar_prompt_aula(..., video_url=...)` inclui o vídeo nos dados de entrada
    e exige que ele apareça em “Recursos e Links”.
- `views/gerador_aulas.py`
  - busca o vídeo antes de montar o prompt e garante o link no Markdown final
    com `_ensure_video_link()` (mesmo se o modelo omitir).

**Como validar:** gerar uma aula da semana e conferir a seção
`## 🧰 Recursos e Links` com o link do vídeo da aula; ou
`obter_link_video_aula("2ª SÉRIE - Turma I-A (Técnico DS)", "INTRODUÇÃO AO ECOSSISTEMA DEVops", 1, 2)`
→ `https://www.youtube.com/watch?v=urIikjGkjXo`.

## IS-127 — Replicação para a I-B na disciplina errada 🟢

**Pedido:** as aulas 4–8 replicadas para a **2ª SÉRIE - Turma I-B** não
apareciam na disciplina própria da I-B (`subject_id=41`).

**Causa:** a replicação escolhia a primeira disciplina com nome compatível.
Como a disciplina compartilhada (`subject_id=9`) também estava vinculada à I-B,
as aulas caíam nela; a disciplina específica da I-B ficava só com as aulas 1–3.

**Mudança:**
- `views/gerador_aulas.py`: ao replicar, a disciplina de destino agora prioriza
  a que contém o nome da turma (ex.: `... (2ª SÉRIE - Turma I-B ...)`) antes da
  compartilhada.
- Aulas **4–8** importadas para `subject_id=41` (I-B) como IDs **916–920**,
  com `week="S01"`, vídeo e **quiz de 4 questões** (dados dos `.md` replicados).
- A disciplina compartilhada `subject_id=9` foi **desvinculada da I-B**
  (`class_subjects`), deixando só a disciplina própria. A I-A continua com a 9.
- `services/quiz_parser.py`: passou a reconhecer numeração com emoji
  (`1️⃣`), cabeçalhos `### ❓ Questão N`, gabaritos em negrito (`**1. B**`) e
  perguntas em que o texto está na linha seguinte.

**Como validar:** abrir a I-B e conferir a disciplina
`INTRODUÇÃO AO ECOSSISTEMA DEVops (2ª SÉRIE - Turma I-B (Técnico DS))` com as
8 aulas da S01; `db.get_lessons_for_subject(41)` deve retornar 903–905 e
916–920, todas com quiz de 4 questões.

## IS-128 — "Nenhuma turma cadastrada" mesmo com turmas no Supabase 🟢

**Sintoma:** ao abrir o app por outro dispositivo da rede (celular/repetidor
Wi-Fi, `http://10.224.244.171:8501`) a aba **Aulas** exibia
"Nenhuma turma cadastrada no sistema", embora as 3 turmas existissem no
Supabase e o cache tivesse `subjects`/`lessons`/`app_users` atualizados.

**Causa:** `get_classes()` engolia a exceção da consulta e devolvia `[]`; o
`local_cache.get_or_fetch()` tratava esse `[]` como resultado **válido** e o
gravava com `TTL_BASE` (6 h). Uma oscilação de rede na primeira carga (08:00)
deixou `classes` = `[]` em cache até 14:00 para **todas** as sessões. O
`python-dotenv` também reclamava da linha 10 do `.env` (chave truncada
`DEEPSEEK_API_KEY="`) e o `run.bat` subia uma segunda API de modelos que
falhava com `WinError 10048` na porta 8001.

**Mudança:**
- `services/local_cache.py`: `get_or_fetch(..., cache_empty=False)` — resultado
  vazio/`None` não é gravado; se existir cache anterior não vazio, ele é
  preferido (evita esconder dados válidos por oscilação).
- `services/database.py`: `get_classes()` e `get_subjects()` deixam a exceção
  subir (fallback para cache antigo) e usam `cache_empty=False`; listas de
  aulas e quizzes também passaram a usar `cache_empty=False`.
- `.env`: removidas a linha solta `DeepSeeks` e a chave `DEEPSEEK_API_KEY="`
  truncada (a chave real duplicada mais abaixo foi mantida).
- `run.bat`: só inicia a API de modelos (porta 8001) se a porta estiver livre.

**Como validar:** limpar a entrada `classes` do cache, reiniciar o app e abrir
`http://<ip-da-lan>:8501` no celular; a lista de turmas deve aparecer. No
terminal não deve haver `could not parse statement` nem `WinError 10048`.

## IS-129 — Servidor auxiliar não sobe no boot e não aparece no monitor 🟢

**Sintoma:** no PC do laboratório (`PC01-LAB02`) o servidor auxiliar
(`lab_receiver`) não subia com o Windows e o monitor do SysAva mostrava
`peers: 0` (nenhum servidor auxiliar). Não havia `servidor.log` na pasta,
sinal de que a tarefa/watchdog nunca chegou a rodar.

**Causa:** o auto-start dependia só da tarefa agendada `SysAva Servidor`
(boot como SYSTEM). Quando a tarefa não está registrada, aponta para uma pasta
antiga (Drive/sync moveu o caminho), o SYSTEM não tem acesso à pasta de nuvem
ou o Python não está disponível, nada avisa o usuário — o servidor simplesmente
não sobe e o monitor fica sem peer. Não havia como ver o estado nem o motivo
na máquina.

**Mudança (em `data/repo/plugins/`):**
- `tray_servidor.ps1` + `tray_servidor.vbs` + `tray_servidor.bat`: ícone na
  **bandeja do Windows** (verde = online, amarelo = porta ocupada sem resposta,
  vermelho = offline). Sobe o servidor pelo `servidor_watchdog.ps1` se a porta
  5000 estiver livre e **nunca abre segunda instância**. Menu: abrir painel,
  abrir log, reiniciar, iniciar/parar, **Iniciar com o Windows** (atalho na
  pasta Inicializar, sem Administrador) e sair. `-Status` mostra o estado no
  console; `-Instalar`/`-Remover` controlam o atalho.
- `diagnostico_servidor.ps1` + `.bat`: relatório no PC do servidor com
  arquivos/atributos (detecta "somente online" do OneDrive/Drive),
  Python/dependências, porta/`/health`, peers, tarefa agendada (estado, último
  resultado e pasta de destino), atalho da bandeja, firewall, log e rede,
  terminando com as prováveis causas. Salva `diagnostico_servidor.txt`.
- `lab_monitor.py`: a faixa de status do radar agora mostra claramente
  **online (primário/auxiliar) | peers | máquinas | versão**, avisa quando não
  há servidor auxiliar conectado e alerta quando o servidor local está offline
  (antes a falha era silenciosa).
- `lab_monitor_doc.md`: seção de auto-start atualizada com bandeja e diagnóstico.

**Como validar (no PC do laboratório):**
1. `tray_servidor.bat` → ícone aparece ao lado do relógio; menu →
   **Iniciar com o Windows**; reiniciar o PC e conferir o ícone verde.
2. `diagnostico_servidor.bat` → seção 4 mostra a tarefa e o último resultado;
   seção 3 mostra `/health OK` e peers.
3. No notebook, aba **Plugins → Monitor**: a faixa deve mostrar
   `peers: 1` quando o PC estiver online.

## IS-130 — Monitor em abas + estrutura de pastas de atividades + pacote de atualização 🟢

**Pedido:** o painel concentrava todas as ações no mesmo `selectbox`
("Ação de Controle") **nos dois dashboards**: o web do receiver (porta 5000) e a
aba **Plugins → Monitor** do Streamlit. A criação de pastas usava caminho fixo
`C:\Projetos\<Escola>\<Turma>\<Disciplina>\<Aluno>`. Era preciso: separar as
funções em **abas**, criar na aba **Ferramentas** a ação que escolhe **turma** e
**disciplina** e gera **`<turma>\<disciplina>\<aluno>\Aula_NN`** no PC do aluno, e
disponibilizar o **pacote de atualização** para download no dashboard.

**Mudança:**
- `data/repo/plugins/lab_receiver.py` (**painel web**, `DASHBOARD_TEMPLATE`):
  layout em **abas** 📊 Monitor (cards + tabela) / 🕹️ Controle (ação + mensagem)
  / 🧰 Ferramentas (estrutura de pastas + pacote). A aba ativa fica no `#hash`.
  Novas rotas: `POST /estruturar` (monta o JSON e chama `dispatch_commands`) e
  `GET /api/disciplinas?class_id=` (selects em cascata). Turmas/disciplinas do
  Supabase com **cache de 10 min** (`_load_classes`/`_load_disciplinas`) para não
  gastar egress a cada reload.
- `data/repo/plugins/lab_monitor.py` (Streamlit): `show_lab_monitor()` em
  **6 abas** — 📊 Radar, 🕹️ Controle, 🧰 Ferramentas, ⚡ Ações em Massa,
  📜 Histórico e 🔍 Diagnóstico; a barra lateral ficou só com utilitários.
- **Ferramentas (ambos):** **Turma**, **Disciplina**, **Aulas** (`1-32`) e
  **Pasta base** (`%USERPROFILE%\Documents\SysAva`, expandida no PC do aluno —
  sem Administrador). No web, marcar PCs na aba Monitor ou “todas as online”.
  O comando `Estruturar Pastas` leva JSON (`build_estrutura_payload`/rota
  `/estruturar`) e é registrado no histórico.
- `lab_agent.py` (e a cópia embutida em `lab_agent.ps1`, agora sincronizada):
  `_criar_estrutura_atividades()` cria `<base>/<turma>/<disciplina>/<aluno>/Aula_NN`
  (uma pasta por aluno, pois o PC do laboratório é compartilhado; o nome usa só
  os **dois primeiros nomes, sem sobrenome** — `PEDRO HENRIQUE PEREIRA GARCIAS`
  → `PEDRO_HENRIQUE`),
  **trocando espaços por `_`** em todos os nomes de pasta (ex.:
  `2ª_SÉRIE_-_Turma_I-A_(Técnico_DS)`), sanitiza nomes inválidos do Windows
  (`_pasta_segura`), aceita o **JSON novo** e o **formato antigo**
  `escola|turma|disciplina|aluno|aulas` (ignora escola/aluno) e mostra um balão
  com o resultado. O agente passou a enviar `agent_version`, `last_cmd` e
  `last_result` no `/ping` (diagnóstico no painel). `AGENT_VERSION` =
  `2026-10-28-pastas2`.
- `lab_receiver.py`: `SERVER_VERSION = "2026-10-28-ferramentas"`; o
  `/servidor.zip` passou a incluir **tray/bandeja**, **diagnóstico** e `.vbs`
  (auto-inclusão de `.ps1`/`.bat`/`.vbs`); link **⬇️ Pacote de atualização** no
  topo do painel web e na aba Ferramentas.
- `reiniciar_servidor.ps1` / `diagnostico_servidor.ps1`: a checagem de versão
  passou a ler `SERVER_VERSION` do `lab_receiver.py` local (não fica mais presa a
  uma string fixa).
- `tests/test_lab_agent_estrutura.py`: cobre a criação das pastas (JSON, formato
  antigo, sanitização), o contrato dashboard → agente e garante que a cópia do
  agente embutida no instalador está idêntica ao `lab_agent.py`.

**Como validar:**
1. `http://<ip>:5000/` (após `reiniciar_servidor.bat`): topo mostra
   `v2026-10-28-ferramentas` e **⬇️ Pacote de atualização**; aparecem as abas
   **Monitor / Controle / Ferramentas**.
2. Aba **Ferramentas** → escolher turma/disciplina, `1-3`, marcar “todas” ou PCs
   na aba Monitor → **Criar estrutura de pastas**; no PC do aluno deve existir
   `%USERPROFILE%\Documents\SysAva\<turma>\<disciplina>\<aluno>\Aula_01..03`
   (espaços viram `_`, ex.: `2ª_SÉRIE_-_Turma_I-A/PEDRO_HENRIQUE/Aula_01`).
3. `Plugins → Monitor`: 6 abas; "Ação de Controle" não lista mais "Estruturar
   Pastas".
4. Topo do painel web ou aba Ferramentas → o `servidor.zip` contém
   `tray_servidor.*` e `diagnostico_servidor.*` (31 arquivos).
5. `python -m pytest -q` (25 testes) e `py_compile` dos arquivos alterados.

## IS-131 — Baixar as atividades dos alunos zipadas no notebook 🟢

**Pedido:** baixar, em ZIP, as pastas de atividades dos PCs dos alunos para o
notebook, para backup e revisão das atividades.

**Mudança:**
- `lab_agent.py`: novo comando **Enviar Atividades** — `_zipar_atividades()`
  compacta a pasta (`%USERPROFILE%\Documents\SysAva`, ou a `base` enviada) e
  `_enviar_atividades_zip()` faz `POST` multipart em `/upload/atividades`.
  O resultado (`ok: X MB`) aparece em **Último comando por PC**.
  `AGENT_VERSION = 2026-10-28-backup1`.
- `lab_receiver.py`: `POST /upload/atividades` salva em
  `data/repo/plugins/.atividades/<maquina>.zip` (limite de 500 MB por envio);
  `GET /atividades` lista os recebidos; `GET /atividades/<arquivo>` baixa um;
  `GET /atividades.zip` baixa todos; `POST /backup_atividades` pede o ZIP aos
  PCs marcados (ou “todas”).
- Painel web: link **📦 Atividades** no topo e seção **📦 Backups de atividades**
  na aba Ferramentas (botão *Solicitar ZIP* + *Ver/baixar recebidos*).
  No Streamlit, link para a mesma página.
- `.gitignore`: `.atividades/` e `.relatorios/` (dados de alunos não vão pro Git).

**Como validar:**
1. Aba Ferramentas → marcar os PCs → **📦 Solicitar ZIP das atividades**.
2. Em ~10–60 s (depende do tamanho), **📦 Atividades** lista cada PC com tamanho
   e hora; **Baixar todos** gera `atividades_sysava.zip` no notebook.
3. Os ZIPs individuais contêm `<turma>/<disciplina>/<ALUNO>/Aula_NN/...`.

**Trava por versão do agente (build):** o agente passou a enviar `agent_build`
(6 = pasta do aluno + dois nomes + backup ZIP). O painel mostra
`agente v… (build N)` ou `agente antigo (build N) — atualize`, e as ações
**ignoram** PCs com agente antigo, avisando no flash
(“N com agente antigo (ignorados)”) em vez de criar pasta no formato errado.
`AGENT_BUILD = 6` / `AGENT_VERSION = 2026-10-28-backup2`.

## IS-132 — Designar o aluno (RA) de um PC pelo painel do notebook 🟢

**Pedido:** escolher do notebook qual RA será “logado”/associado em cada PC
(sem precisar ir até o PC digitar na tela de bloqueio).

**Mudança:**
- `lab_receiver.py`: nova rota `POST /designar_aluno` — valida o RA na lista de
  alunos (ou no Supabase), grava em `lab_users.json` pela mesma função da tela de
  bloqueio (`_associar_usuario_maquina`) e registra no histórico/log.
- Aba **Controle** do painel: seção **👤 Aluno do PC (designar RA)** com dois
  seletores (PC e Aluno) e o botão *Designar aluno ao PC*. Com isso o radar
  mostra **Aluno (RA)** e a criação de pastas usa o nome do aluno
  (`PEDRO_HENRIQUE`), mesmo sem o aluno ter passado pelo lock.
- `_lista_alunos()` extraído de `/api/alunos` (cache de 30 min + disco), então o
  seletor funciona também com o Supabase instável (72 alunos na base).

**Limite:** isso associa o aluno ao PC (radar/histórico/pastas) — **não**
desbloqueia a tela de bloqueio. Para desbloquear de longe seria preciso a
`sysava_lock.ps1` consultar o servidor por um RA designado (próximo passo).

**Como validar:** Controle → escolher PC e aluno → *Designar aluno ao PC* →
Monitor passa a mostrar o nome/RA na linha e a próxima criação de pastas usa o
nome do aluno.

## IS-133 — Bandeja (tray) do SysAva e apps no notebook 🟢

**Pedido:** uma bandeja parecida com a do LM Studio (ícone ao lado do relógio,
menu com status, abrir apps, submenu e Sair) que suba junto com o Windows no
notebook.

**Mudança (novos arquivos na raiz):**
- `sysava_tray.ps1` — ícone na bandeja com:
  - cabeçalho **SysAva | IP** e status do app 8501;
  - **Abrir SysAva (8501)**;
  - **Apps >** Verificador de Duplicatas (8502), Monitor do Supabase (8503),
    Down SeducTec (8504), Planejamento/Registro (8510), Análise de Notas (8511)
    e **Parar todos os apps**. Cada item inicia o Streamlit na porta se estiver
    parado e abre o navegador; uma **•** indica o app online;
  - **Servidor do laboratório (5000) >** abrir painel / iniciar / parar;
  - **Copiar URL do SysAva**, **Abrir pasta do projeto**;
  - **Abrir o SysAva ao iniciar a bandeja** (flag em `%LOCALAPPDATA%\SysAva`),
    **Iniciar com o Windows** (atalho na pasta Inicializar) e **Sair**.
- `sysava_tray.vbs` + `sysava_tray.bat` — abre a bandeja sem janela de console.
- Ícone usa `logo_sysava.png` (fallback: círculo colorido). Instância única
  (mutex) e monitor de portas em runspace (não trava o menu).

**Como validar:**
1. `sysava_tray.bat` → ícone aparece; menu mostra o status e os apps.
2. Marcar **Iniciar com o Windows** (ou `powershell -File sysava_tray.ps1 -Instalar`)
   e reiniciar o notebook → a bandeja volta sozinha.
3. `powershell -File sysava_tray.ps1 -Status` lista as portas 8501..8511, 5000
   e 8001.

## IS-134 — Organização dos plugins: monitor em `plugins/monitor_rede/` 🟢

**Pedido:** parar de misturar tudo em `data/repo/plugins` e migrar de forma
gradativa, começando pelo plugin de monitoramento.

**Mudança (fase 1):**
- `data/repo/plugins/lab_monitor.py` → **`plugins/monitor_rede/lab_monitor.py`**.
- `data/repo/plugins/lab_monitor_doc.md` → **`plugins/monitor_rede/README.md`**.
- `lab_monitor.py`: `PLUGIN_DIR` agora resolve a pasta de **runtime**
  (`SYSAVA_PLUGIN_DIR` → `data/repo/plugins` → pasta do arquivo), então
  `lab_status.json`, `lab_labels.json`, `lab_users.json` e o `lab_receiver.py`
  continuam sendo lidos do deploy.
- `views/plugins.py`: carrega `plugins/monitor_rede/lab_monitor.py` (fallback
  para o caminho antigo).
- `plugins/README.md`: estrutura alvo e fases 2 (servidor) e 3 (agente/
  ferramentas). `data/repo/plugins` fica como pasta de **deploy/runtime**
  (plana, gitignored), porque o receiver serve os arquivos de lá.

**Como validar:** Plugins → Monitor abre normalmente; `AppTest` do arquivo novo
não gera exceções; o radar mostra as máquinas do receiver.

## IS-135 — Tela de bloqueio com modo offline 🟢

**Pedido:** o PC do aluno não pode ficar preso quando o servidor/internet cai.
Ter alternativas (lista em cache, pasta sincronizada do Drive e carência de
15 min) para liberar a tela com a credencial do aluno.

**Mudança (`data/repo/plugins/sysava_lock.ps1`):**
- Novos parâmetros `-GraceMin` (padrão 15; 0 = imediato) e `-SemOffline`
  (mantém o comportamento antigo: só libera com servidor ou senha admin).
- Se o servidor não responder em 3 min, `Invoke-LiberacaoOffline` procura o
  RA/nome na lista local: cache `%LOCALAPPDATA%\SysAva\alunos.json` + cópias
  sincronizadas (`C:\Local\servidor_sysava\alunos_cache.json`,
  `C:\SysAva\plugins\alunos_cache.json`, `SYSAVA_ALUNOS_CACHE`).
- Enquanto espera, tenta o servidor a cada 5 s (se voltar, valida normal).
  Esgotada a carência, libera com o RA do aluno em **modo offline**.
- Login offline é gravado em `%LOCALAPPDATA%\SysAva\desbloqueios_offline.log` e
  na fila `logins_offline.jsonl`; quando o servidor volta, `Sync-LoginsOffline`
  envia cada um para `/api/auth_ra` (histórico/radar) e limpa a fila.

**Limite:** ainda não valida direto no Supabase (precisa das credenciais no PC;
próximo passo: `cloud.json` distribuído pelo instalador/atualizador). O modo
offline confia na lista local — aceitável no laboratório (RA como credencial).

**Como validar:** com o servidor desligado, digitar um RA que esteja na lista
local: após a carência a tela libera e o log offline registra; ao religar o
servidor, o histórico recebe o login.

## IS-136 — Acesso remoto com Tailscale (guia) 🟢

**Pedido:** entender/viabilizar manutenção dos PCs do laboratório de fora da
escola sem depender de DDNS nem de abrir portas.

**Decisão:** o Google Drive **não** funciona como DDNS (IPs `192.168.x` são
privados; Drive tem latência e conflitos de escrita) e a chave da service
account não pode ir para os PCs. O acesso remoto fica com **Tailscale**
(mesh WireGuard) e um **subnet router** no PC01-LAB02, que anuncia a faixa
`192.168.10.0/23`; o inventário (`pc_registry`) é assunto separado.

**Entregue:** `docs/TAILSCALE.md` com a explicação da essência, diagrama,
passo a passo (instalar no notebook e no PC01, `--advertise-routes`,
aprovar a rota no admin, `--accept-routes`, testes de fora), segurança,
limitações e problemas comuns. Nenhuma mudança de código: o agente, a tela de
bloqueio e o painel continuam iguais (o Tailscale só muda o caminho).

## IS-137 — Projeto Feira das Profissões (6 aulas) 🟢

**Pedido:** colocar em `plugins/atividades/Atividades_florestan/` as **seis
aulas** do projeto *Feira das Profissões: dos orçamentos ao cronograma*,
integrando a Profa. Adriana (Técnico em Marketing) e o Prof. Raylson
(Robótica), com as turmas **1ª B** (Marketing) e **2ª A / 2ª B**
(Desenvolvimento de Sistemas).

**Entregue:** guia geral + 6 planos de aula em Markdown:

- `00_LEIA-ME_Feira_das_Profissoes.md` — visão geral, áreas de incubação,
  distribuição por turma, papéis dos parceiros, cronograma e rubrica geral;
- `AULA_01_Abertura_e_Formacao_das_Equipes.md` — áreas, equipes e papéis;
- `AULA_02_Problema_Publico_e_Proposta_de_Valor.md` — pesquisa e Canvas;
- `AULA_03_Orcamento_e_Viabilidade.md` — custos, receita e ponto de equilíbrio;
- `AULA_04_Cronograma_e_Gestao_de_Tarefas.md` — EAP, marcos, Kanban e riscos;
- `AULA_05_Prototipo_Identidade_e_Pitch.md` — MVP, comunicação e pitch;
- `AULA_06_Feira_Avaliacao_e_Retrospectiva.md` — feira, rubrica e relatório.

As quatro áreas de incubação (Agroindústria, compra e venda local, IA aplicada
à Indústria e Robótica) estão distribuídas com vocação por turma, sem engessar
as equipes. Nenhuma alteração de código: é conteúdo pedagógico versionado no
repositório.

**Como validar:** abrir a pasta e conferir os 7 arquivos; cada aula tem
objetivos, desenvolvimento com tempos, entregável, rubrica e adaptação por
turma.

## IS-138 — Post do fórum (Aula 01 DevOps): Tailscale com conta institucional 🟢

**Pedido:** material em Markdown para publicar no fórum da Aula 01 de DevOps,
usando o **Gmail institucional** (não a conta pessoal) no notebook e no PC01.

**Entregue:** `docs/FORUM_AULA01_DEVOPS_TAILSCALE.md` — post didático com
objetivo, ideia em 30 s, diagrama, pré-requisitos (conta institucional e
liberação do Workspace, se houver bloqueio), instalação nos dois PCs, descoberta
da sub-rede, `--advertise-routes`, aprovação da rota no admin, `--accept-routes`,
teste de fora (4G), segurança, problemas comuns, checklist e próximo passo
(`pc_registry`). `docs/TAILSCALE.md` ganhou a nota para usar a conta
institucional nos dois dispositivos.

## IS-139 — Abrir site (Prova Motriz) nos PCs 🟢

**Pedido:** uma ação para abrir `prova-motriz.jovensgenios.com/entrar` em todos
os PCs do laboratório.

**Mudança:**
- `lab_agent.py`: `AGENT_BUILD = 7` / `AGENT_VERSION = 2026-10-28-abrir1`;
  `_normalizar_url()` (adiciona `https://` se faltar) e `_abrir_url()` via
  `os.startfile` (abre no navegador padrão da sessão do aluno). Comando
  **Abrir Prova Motriz (jovensgenios)** ou **Abrir Site** com
  `command_msg` = `{"url": "..."}` (ou a URL pura). Resultado no
  *Último comando por PC* (`ok: aberto https://...`).
- `lab_receiver.py`: `ACOES_CONTROLE` ganhou o preset; nova rota
  `POST /abrir_site` (URL livre, respeita máquinas marcadas ou “todas”) com
  trava `AGENT_BUILD_MIN_SITE = 7` (ignora agentes antigos e avisa no flash).
- Painel web: seção **🌐 Abrir site nos PCs** na aba Ferramentas (campo URL já
  com a Prova Motriz) e link no topo; Ações em Massa não tem botão próprio (use
  a seleção “todas” da Ferramentas).
- Streamlit (`plugins/monitor_rede/lab_monitor.py`): ação no seletor de Controle
  e botão **🌐 Abrir Prova Motriz em TODAS** nas Ações em Massa.
- `tests/test_lab_agent_estrutura.py`: cobre `_normalizar_url`.

**Como validar:** Ferramentas → marcar “todas” → **🌐 Abrir site** (ou Controle →
Abrir Prova Motriz). O navegador dos PCs abre a página de entrada da Prova
Motriz; o resultado aparece em *Último comando por PC*. Requer agente build 7
(Controle → Atualizar Monitor rápido).

## IS-140 — Bandeja do aluno + e-mail institucional 🟢

**Pedido:** uma bandeja nos PCs do laboratório (como a do notebook) e uma forma
de o aluno **copiar o e-mail institucional**; os e-mails estão em `.txt` nas
pastas das turmas (`data/Turmas/<turma>/emails*.txt`).

**Mudança:**
- `lab_receiver.py`: `emails.json` (nome normalizado → nome/email/turma) gerado
  por `_construir_mapa_emails()` a partir dos `emails*.txt`; rota
  `POST /publicar_emails` (login; gera o arquivo) e `GET /api/email`
  (`?maquina=` resolve pela tela de bloqueio, ou `?ra=`/`?nome=`).
  Aba **Ferramentas → 📧 Lista de e-mails institucionais** mostra a contagem e o
  botão *Publicar lista*. `emails.json` entrou no `servidor.zip` e no
  `/download`.
- `tray_aluno.ps1` + `.vbs` + `.bat`: ícone ao lado do relógio com
  **Mostrar meu e-mail**, **Copiar meu e-mail** (área de transferência),
  **Abrir SysAva**, **Abrir Gmail**, **Iniciar com o Windows** e **Sair**.
  Descobre o servidor pelo cache do agente (`C:\Local\SysVa_lab\server_cache.txt`),
  UDP 5001 ou `127.0.0.1:5000`; guarda cópia em
  `%LOCALAPPDATA%\SysAva\meu_email.txt` para funcionar com o servidor fora.
- `lab_agent.py` (build 8 / `2026-10-29-bandeja1`): comando
  **Atualizar Bandeja do Aluno** — baixa `tray_aluno.*` + logo para
  `%LOCALAPPDATA%\SysAva`, cria o atalho `SysAva Aluno.lnk` na Startup e inicia.
  Ação disponível em **ACOES_CONTROLE**.
- `tests`: 26 testes passando (inclui `_normalizar_url` e sincronização do
  instalador do agente).

**Como validar:**
1. No notebook: Ferramentas → **Publicar lista de e-mails** (41 alunos hoje).
2. Controle → PCs com agente build 8 → **Atualizar Bandeja do Aluno**.
3. No PC do aluno: ícone na bandeja → **Copiar meu e-mail** (cola no Gmail).
   Com o servidor fora, usa a cópia local.
4. Aluno sem associação (tela de bloqueio) ou fora da lista → aviso "não
   encontrado"; associe pelo painel (Designar aluno) ou confira o `.txt` da turma.

## IS-141 — Faxina (limpeza segura) nos PCs 🟢

**Pedido:** alguns PCs demoram para iniciar; rodar uma “faxina” para limpar
arquivos acumulados.

**Mudança:**
- `lab_agent.py` (build 9 / `2026-10-29-faxina1`): comando **Faxina (limpeza)** →
  `_faxina(cfg)` limpa, sem UAC e sem tocar no Windows/inicialização:
  1. `%TEMP%`, `%LOCALAPPDATA%\Temp` (itens com mais de 1 dia; arquivos em uso são ignorados);
  2. restos de atualização em `%LOCALAPPDATA%\SysAva` (`*.novo`, `*.bak`, `*.old`, `*.tmp`);
  3. logs do agente (`agent_runtime.log`/`install_debug.log` truncados; `*.bak`/`*.log.1` removidos);
  4. **opcional** caches de navegador (Chrome/Edge, só com o navegador fechado);
  5. **opcional** esvaziar a lixeira.
  Devolve `ok: X MB liberados, N itens` no *Último comando por PC*.
- `lab_receiver.py`: rota `POST /faxina` (máquinas marcadas ou “todas”, trava
  build 9) e seção **🧹 Faxina nos PCs** na aba Ferramentas (checkboxes de
  caches/lixeira). Ação **Faxina (limpeza)** também no seletor de Controle.
- Streamlit: ação no Controle e botão **🧹 Faxina em TODAS** nas Ações em Massa.
- `tests`: `_apagar_conteudo` coberto (27 testes).

**Como validar:** Ferramentas → marcar “todas” → **🧹 Fazer faxina**; em cada PC o
resultado aparece em *Último comando por PC* (ex.: `ok: 820 MB liberados, 143 itens`).

**Nota sobre inicialização lenta:** a faxina remove acúmulo, mas o que mais
atrasa o logon são programas de inicialização (Opera/Roblox/OneDrive/Teams) —
use também **Limpar Inicialização …** no Controle. Se continuar lento, o próximo
passo é um diagnóstico de boot (tempo de logon + itens de inicialização).

## IS-142 — WPS Office e apps de segundo plano 🟢

**Pedido:** o WPS Office (e outros apps do Windows) sobe sozinho e fica na RAM;
desativar a inicialização e os apps desnecessários.

**Mudança (`lab_agent.py`, build 10 / `2026-10-29-wps1`):**
- `WPS_STARTUP_KEYWORDS` + `limpar_inicializacao_wps()`: remove o WPS do
  auto-start (Run/RunOnce, Startup, tarefas de logon) **sem fechar** o documento
  aberto (`wps.exe`/`et.exe`/`wpp.exe`); encerra só os helpers de segundo plano
  (`wpscloudsvr`, `wpscenter`, `wpsupdate`, `wpsnotify`, `ksomisc`, `kdocs`,
  `wpscloud`). Também roda no start do agente (como Roblox/Opera/Microsoft).
- `_aplicar_tweaks_windows()` (HKCU, sem admin): desativa **Widgets**
  (`TaskbarDa`), **Copilot** (`ShowCopilotButton`), **Chat/Teams pessoal**
  (`TaskbarMn`) e **Game Bar/DVR** (`AutoGameModeEnabled`, `GameDVR_Enabled`).
  (Widgets/Copilot somem após reiniciar o Explorer/logon.)
- Comandos novos em `ACOES_CONTROLE`:
  **Limpar Inicialização do WPS (bandeja)** e
  **Desativar Apps em Segundo Plano (WPS/Microsoft/Opera)** — este último também
  aplica os tweaks e reporta `ok: N itens de inicializacao, M ajustes`.
- Streamlit: as duas ações no seletor de Controle.

**Como validar:** Controle → PCs com agente build 10 → *Limpar Inicialização do
WPS* (ou *Desativar Apps em Segundo Plano*). No PC: Gerenciador de Tarefas não
mostra mais os helpers do WPS e, após logoff/logon, Widgets/Copilot/Game Bar
ficam desligados. O `server_cache`/resultado aparece em *Último comando por PC*.

## IS-143 — Desativar o Copilot na inicialização 🟢

**Pedido:** o Copilot aparece habilitado na inicialização de todos os PCs.

**Causa:** o Copilot do Windows 11 não é uma entrada “Run” clássica; muitas
vezes é um *startup task* do shell e continua elegível mesmo removendo os
atalhos.

**Mudança (`lab_agent.py`, build 11 / `2026-10-29-copilot1`):**
- `_desativar_copilot()`:
  - política do usuário `HKCU\Software\Policies\Microsoft\Windows\WindowsCopilot`
    → `TurnOffWindowsCopilot=1` (desliga o Copilot);
  - `ShowCopilotButton=0` e `...\Shell\Copilot\BingChat\IsUserEligible=0`;
  - entradas do Copilot em `StartupApproved\Run|Run32|StartupFolder` marcadas
    como **desativadas** (blob `03 00 …`);
  - encerra o processo `copilot*` se estiver rodando.
- Roda em: **Limpar Inicialização de Apps Microsoft** (e no start do agente) e
  no novo comando **Desativar Copilot (Windows)**; o comando
  **Desativar Apps em Segundo Plano** também aplica (`_aplicar_tweaks_windows`).
- `_set_dword_hkcu()` centraliza a escrita no registro (testado com chave
  temporária; 28 testes passando).

**Como validar:** Controle → *Desativar Copilot (Windows)* em todos; fazer
logoff/logon (ou reiniciar o Explorer). Em *Configurações → Aplicativos →
Inicializar* o Copilot não deve mais ficar habilitado, e o botão some da barra.
Como é HKCU, vale para a conta usada no laboratório (ex.: `ALUNO`).

## IS-144 — Status do servidor na tela de bloqueio 🟢

**Pedido:** a tela de bloqueio deve mostrar se o servidor está **conectado** ou
**desconectado** e pedir para **ligar o PC01**.

**Mudança (`data/repo/plugins/sysava_lock.ps1`):**
- Novo rótulo `$lblServidor` no cartão (abaixo da mensagem), atualizado por um
  **runspace** a cada 6 s: testa `/health` nos candidatos
  (`-Server`, cache do agente `C:\Local\SysVa_lab\server_cache.txt`,
  `%LOCALAPPDATA%\SysAva\servidor.txt`, `127.0.0.1:5000`) e grava o estado num
  hashtable sincronizado.
- Um timer de UI (1,5 s) só troca o texto/cor: **“Servidor conectado”** (verde)
  ou **“Servidor desconectado - ligue o PC01 (servidor do laboratorio)”**
  (laranja). Não trava a tela: a verificação fica em segundo plano.
- `FormClosing` encerra o timer e o runspace.

**Como validar:** com o PC01 desligado, a tela mostra o aviso; ligando o PC01,
em ~6 s muda para “Servidor conectado”. O login continua funcionando com o modo
offline (IS-135) quando o servidor está fora.

**Deploy:** Controle → *Atualizar Tela de Bloqueio (sem UAC)* (ou o próximo
logon, que baixa a versão nova automaticamente).

## IS-145 — Aviso em destaque e seta para baixo na tela de bloqueio 🟢

**Pedido:** destacar o aviso “Selecione seu nome ou …” e usar a seta para baixo
(ou Page Down) do teclado para abrir a lista, facilitando o acesso.

**Mudança (`data/repo/plugins/sysava_lock.ps1`):**
- `$lblSub`: 13 pt **negrito** na cor âmbar (`255,214,90`) e texto
  “Selecione seu nome ou RA (seta para baixo abre a lista)”.
- `$txt` (ComboBox) e o formulário (`KeyPreview`) tratam **Down/PageDown**:
  se a lista estiver fechada, abrem (`DroppedDown = $true`) e consomem a tecla;
  se já estiver aberta, a navegação normal continua.
- Clicar no aviso também foca e abre a lista (cursor de mão).

**Como validar:** na tela de bloqueio, apertar ↓ (ou Page Down) abre os nomes;
digitar filtra (autocomplete) e Enter confirma. Deploy: Controle →
*Atualizar Tela de Bloqueio (sem UAC)*.

## IS-146 — Chrome fora da inicialização e sem modo segundo plano 🟢

**Pedido:** desativar a inicialização do Chrome junto com os demais apps.

**Mudança (`lab_agent.py`, build 12 / `2026-10-29-chrome1`):**
- `limpar_inicializacao_chrome()`: remove o Chrome do auto-start
  (Run/RunOnce, pasta Inicializar e tarefas de logon) **sem fechar** o navegador
  aberto pelo aluno e aplica a política
  `HKCU\Software\Policies\Google\Chrome\BackgroundModeEnabled=0` (impede o Chrome
  de continuar na RAM depois de fechado).
- Roda no start do agente (junto com Roblox/Opera/Microsoft/WPS).
- Comandos: **Limpar Inicialização do Chrome (bandeja)** e inclusão no
  **Desativar Apps em Segundo Plano (WPS/Chrome/Microsoft/Opera)**.

**Como validar:** Controle → *Limpar Inicialização do Chrome*; em
`chrome://settings/system` o “continuar executando apps em segundo plano” fica
desligado e o Chrome não aparece mais em *Inicializar* após logoff/logon.

## IS-147 — Conta compartilhada `Alunos_EJA_Noite` 🟢

**Pedido:** criar a conta `Alunos_EJA_Noite` (turma do EJA à noite).

**Feito:** inserida em `app_users` (Supabase) como **aluno compartilhado**:
- `username`/`ra`: `Alunos_EJA_Noite`
- `name`: `Alunos EJA - Noite`
- `role`: `student`, `is_active: true`
- senha inicial definida pelo professor (trocar no Admin se necessário) e
  hash bcrypt no mesmo formato do login.

**Observações:**
- Login aceita o usuário **ou** o RA (iguais), sem diferenciar maiúsculas.
- Aparece no seletor da tela de bloqueio (`/api/alunos` → 73 alunos) e no Admin
  (cache `app_users:v2` foi invalidado; `alunos_cache.json` regenerado).
- Ainda **não** está matriculada em turma (`student_enrollments`) — matricular
  no Admin quando a turma do EJA existir.
- A pasta de atividades do agente usará `ALUNOS_EJA` (dois primeiros nomes) se
  essa conta estiver associada a um PC.

## IS-148 — Liberar a tela de bloqueio remotamente 🟢

**Pedido:** em casos excepcionais (ex.: a turma do EJA à noite não consegue
desbloquear), o professor deve conseguir, **de casa**, liberar as máquinas.

**Mudança (agente build 13 / `2026-10-29-liberar1` + tela nova):**
- Agente: comando **Liberar Telas (desativar bloqueio)** → `_liberar_tela(cfg)`
  grava `tela_liberada.json` em `%LOCALAPPDATA%\SysAva` e `C:\ProgramData\SysAva`
  com `expira_em` (epoch). Duração: minutos do comando ou **fim do dia (23:59)**
  por padrão. Devolve `ok: telas liberadas ate HH:MM`.
- **Reativar Telas (bloqueio)**: apaga o arquivo — o bloqueio volta no próximo
  logon.
- `sysava_lock.ps1`: `Test-TelaLiberada()` na inicialização (não abre a tela) e
  no timer de status (se estava aberta, fecha sozinha via `$form.Close()`, o que
  restaura as políticas, ex.: Gerenciador de Tarefas).
- Painel: seção **🔓 Liberar telas (caso excepcional)** na aba Ferramentas
  (fim do dia / 2h / 4h / 8h / 24h + botões Liberar e Reativar) e as duas ações
  no seletor de Controle; trava build 13.

**Ordem de deploy:** PC01 → *Atualizar Monitor (rápido)* até **build 13** →
**Atualizar Tela de Bloqueio (sem UAC)** (necessário para a tela ler o arquivo)
→ Ferramentas → *Liberar telas*.

**Segurança:** a liberação expira sozinha; o arquivo fica no perfil do usuário
(e em `ProgramData`, se gravável). Para uso excepcional, prefira “fim do dia”.

## IS-149 — Status das telas de bloqueio no dashboard 🟢

**Pedido:** saber no dashboard do servidor o estado das telas dos PCs.

**Mudança (`lab_agent.py` build 14 / `2026-10-29-status-tela1`):**
- `_status_tela()`: verifica se o `sysava_lock.ps1` está rodando (psutil, lendo a
  linha de comando) e lê o `tela_liberada.json` (expiração válida).
- O `/ping` passou a enviar `lock_running` (bool) e `lock_released_until` (epoch).
- Painel web: nova coluna **Tela** na tabela do Monitor, com selos:
  **liberada até HH:MM** (verde), **bloqueada** (vermelho), **sem tela** (cinza)
  e **-** para agente antigo. `/detalhes` mostra “Tela de bloqueio: …”.
- Streamlit (`plugins/monitor_rede`): coluna **Tela** no radar.

**Como validar:** Controle → PCs build 14. A tabela mostra “bloqueada” quando a
tela está aberta, “liberada até …” depois de usar *Liberar telas* e “sem tela”
quando o lock não está rodando.

## IS-150 — “Abrir site” lembra a última URL 🟢

**Pedido:** deixar gravada no servidor a URL do “Abrir site” (ex.:
`http://192.168.11.99:5000/download/ATUALIZAR_PC01.bat`) para não redigitar.

**Mudança (`lab_receiver.py`):**
- `site_padrao.json` na pasta do receiver guarda `{"url", "atualizado_em"}`.
- O campo **URL** da aba Ferramentas carrega `_load_site_padrao()` (padrão:
  `http://192.168.11.99:5000/download/ATUALIZAR_PC01.bat`).
- `POST /abrir_site` grava a URL usada (`_save_site_padrao`) — a próxima visita
  já abre com ela.
- Sem `site_padrao.json`, o padrão continua sendo a Prova Motriz.

**Atenção:** “Abrir site” abre a URL no **navegador** dos PCs selecionados. Para
um `.bat`, o navegador **baixa** o arquivo (não executa). Para efetivamente
atualizar o PC01, rode o `ATUALIZAR_PC01.bat` nele.

## IS-151 — Aluno (RA) vencido não some mais do painel: mostra "último em dd/mm" 🟢

**Sintoma:** depois de `USER_MAP_TTL_SECONDS` (16 h), o painel web do receiver
trocava o aluno por **“sem RA”**, mesmo havendo uma associação anterior
(ex.: `PC03-LAB03-V02` com VICTOR em 29/10 e `22139923-LAB-50137` com a conta
compartilhada `Alunos_EJA_Noite`). No Streamlit a célula ficava **vazia**.

**Mudança:**
- `lab_receiver.py`: novo `_aluno_exibicao()` mantém o último RA conhecido e
  acrescenta **“— último em dd/mm”** quando a associação venceu; sem nenhuma
  associação a coluna mostra **“Não logado”** (antes “sem RA”). `/detalhes` idem.
- `_fmt_aluno()` agora delega a `_aluno_exibicao()` (mesmo texto no dashboard e
  nos detalhes).
- Streamlit (`plugins/monitor_rede/lab_monitor.py` e cópia
  `data/repo/plugins/lab_monitor.py`): mesma regra; célula vazia vira
  **“Não logado”**.

**Arquivos:** `data/repo/plugins/lab_receiver.py`,
`plugins/monitor_rede/lab_monitor.py`, `data/repo/plugins/lab_monitor.py`,
`docs/ISSUES_LOCAIS.md`.

**Validar:** abrir o painel com uma máquina cuja associação tenha > 16 h —
mostra `NOME (RA) — último em dd/mm`; máquina sem nenhuma associação mostra
`Não logado`; associação recente continua só `NOME (RA)`; `py_compile` e render
do template OK.

## IS-152 — DevOps (Aulas 07 e 08): 3 projetos de CI/CD por aula no fórum 🟢

**Pedido:** criar, no plugin **Atividades**, atividades das aulas 07 (Integração
Contínua) e 08 (Entrega Contínua) de DevOps com GitHub e CI/CD, em equipes de 3,
com tutorial passo a passo no VSCode (Python ou Node): criar repositório,
rodar o projeto, subir por terminal/VSCode e cada integrante fazer commit ou
issue. Três projetos por aula.

**Feito:**
- Script `scripts/seed_atividades_devops_ci_cd.py` publica **3 posts por aula**
  (um por projeto), como `EduBot 🤖`, no fórum das aulas:
  - I-A (subject 9): Aula 07 = lesson 912, Aula 08 = lesson 914.
  - I-B (subject 41): Aula 07 = lesson 919, Aula 08 = lesson 920.
- **Aula 07 — CI:** (1) Python + pytest + Actions; (2) Node + Jest + Actions;
  (3) fluxo profissional com branches, 3 Issues e Pull Requests com matriz de CI.
- **Aula 08 — CD:** (1) Python gera relatório e publica **Release** em tag `v*`;
  (2) Node faz build e **deploy no GitHub Pages**; (3) pipeline
  build → deploy com **ambiente `producao` e aprovação manual**.
- Cada post traz divisão da equipe de 3 (A dono do repo, B branch/PR, C issue +
  review/merge), comandos, arquivos, workflow YAML, critérios (3 commits +
  1 issue + 1 PR + pipeline verde) e erros comuns.
- Seed **idempotente** (pula pelo título do projeto); `--dry-run` para conferir,
  `--apply` para gravar. Total publicado: **12 posts** (6 projetos × 2 turmas).

**Arquivos:** `scripts/seed_atividades_devops_ci_cd.py`, `docs/ISSUES_LOCAIS.md`.

**Validar:** abrir Aulas → disciplina DevOps → Aula 7/8 → fórum com 3 posts de
projeto; reexecutar o script deve informar `12 já existiam` (sem duplicar).

## IS-153 — DevOps (Aula 09): atividade de automação com pipeline 🟢

**Pedido:** pensar/criar uma atividade da Aula 09 (“Automação em TI: o motor da
eficiência e segurança no ecossistema DevOps”) envolvendo automação com
pipeline — podendo ser chatbot ou outra automação.

**Feito:** uma atividade publicada no fórum (uma por turma), como `EduBot 🤖`:
- I-A (subject 9): lesson 927.
- I-B (subject 41): lesson 928.

**Projeto:** **chatbot de atendimento (FAQ) automatizado por GitHub Actions**.
- `bot.py` responde por similaridade sobre `faq.json` (normaliza acentos/caixa).
- `run_batch.py` executa o bot em lote sobre `casos_teste.json`, gera
  `relatorio/relatorio.html` e **falha o pipeline** se a taxa de acerto < 80%.
- Pipeline com 2 jobs: `testes` (push/PR) e `automacao`
  (`schedule` diário em UTC + `workflow_dispatch`) que publica o relatório como
  **artefato** `relatorio-automacao`.
- Equipe de 3 (A bot/repo, B lote/PR, C workflow agendado + issue + review) e
  desafio extra: trocar por bot que lista issues com `GITHUB_TOKEN` (sem
  segredos externos), mantendo os 2 jobs.

**Arquivos:** `scripts/seed_atividade_devops_a09_automacao.py`,
`docs/ISSUES_LOCAIS.md`.

**Validar:** Aulas → DevOps → Aula 9 → fórum com o post do projeto; reexecutar o
script deve informar `2 já existiam`.

## IS-154 — Monitor: “Designar aluno” precisa valer na criação das pastas 🟢

**Sintoma:** designar **Julia** a um PC (`Controle → Aluno do PC`) e depois
criar a estrutura de pastas resultava em `7_Ano` (aluno anterior), não
`JULIA_GABRIELLA`.

**Diagnóstico (dados de 04/11):** a designação da Julia foi gravada
(`lab_users.json`, 08:35:30). O `7_Ano` veio de **outros PCs** que estavam
designados com a conta `7 Ano A` (08:38) e foram incluídos na criação (a ação usa
os PCs marcados na aba Monitor / “todas”). A pasta usa os **dois primeiros
nomes** de propósito (regra do agente `_nome_pasta_aluno`).

**Mudança (sem mexer na regra de 2 nomes):**
- `lab_receiver.py`: a aba **Ferramentas** ganhou a prévia
  **👥 Aluno e pasta que serão usados em cada PC** (Rótulo · Aluno designado ·
  Pasta), deixando claro o que cada PC vai criar. A pasta usa os **dois
  primeiros nomes** (`JULIA GABRIELLA...` → `JULIA_GABRIELLA`; `7 Ano A` →
  `7_Ano`).
- `designar_aluno()` agora **propaga a designação na hora** para os servidores
  auxiliares (novo `POST /api/peer/user`, com `PEER_TOKEN`), sem esperar o sync
  de 5 s. Assim, criar pastas no painel de outro servidor usa o aluno novo.
- `_associar_usuario_maquina(..., registrar_historico=False)` no peer evita
  gravar o histórico em duplicidade.
- `estruturar()` registra no log
  `ESTRUTURAR: <PC> -> aluno '<nome>' pasta '<pasta>'`, para conferir o nome real
  usado.
- `SERVER_VERSION` → `2026-11-04-designar-aluno`.

**Arquivos:** `data/repo/plugins/lab_receiver.py`,
`plugins/monitor_rede/lab_monitor.py`, `docs/ISSUES_LOCAIS.md`.

**Validar:** designar Julia ao PC X → Ferramentas → abrir a prévia e conferir
`X → JULIA GABRIELLA... → JULIA_GABRIELLA` → marcar **só o PC X** (ou usar
“todas” ciente de que cada PC usa o seu aluno) → *Criar estrutura* → pasta
`...\JULIA_GABRIELLA\Aula_01`. Teste do Flask: payload de um PC designado para
Julia leva `JULIA GABRIELLA DE OLIVEIRA SALES` (agente corta em
`JULIA_GABRIELLA`). Reiniciar o receiver (`reiniciar_servidor.bat`).

## IS-163 — Bandeja: busca o servidor atual antes de abrir o painel 🟢

**Pedido:** o item **Servidor do laboratório (5000) → Abrir painel do monitor**
abria sempre `http://<IP deste PC>:5000`. Em PCs que não são o servidor (ou
quando o servidor mudou de IP por DHCP ou está no notebook/PC auxiliar), o
navegador caía em página vazia.

**Mudança (`sysava_tray.ps1`):**
- Nova descoberta em camadas (`Find-ServidorUrl`), na mesma ordem do agente:
  1. porta 5000 local (este PC é o servidor);
  2. cache da bandeja `%LOCALAPPDATA%\SysAva\servidor_tray.txt`;
  3. cache do agente (`plugins/server_cache.txt`, normaliza o sufixo `/ping`);
  4. URLs de `plugins/peers.txt`;
  5. **broadcast UDP 5001** (`SYSAVA_DISCOVER` → `SYSAVA_SERVER ip:porta`),
     também em `192.168.10.255`/`192.168.11.255`.
- Cada candidato só é aceito se `GET /health` responder `status=online`; a URL
  encontrada é gravada no cache da bandeja.
- **Abrir painel do monitor** e o novo **Buscar servidor na rede** usam essa
  descoberta. O item do menu passa a mostrar `online (IP)`/`offline`, o tooltip
  inclui o servidor e o monitor em segundo plano (runspace) relê os caches a
  cada ~10 s — o ícone fica verde/amarelo mesmo com o servidor em outro PC.
- **Iniciar servidor** só fica habilitado quando nenhum servidor é encontrado
  (evita abrir uma segunda instância); **Parar servidor** só com a porta 5000
  local ativa.
- `-Status` agora mostra a linha **Servidor atual**.

**Arquivos:** `sysava_tray.ps1`, `docs/ISSUES_LOCAIS.md`.

**Validar:** `powershell -File sysava_tray.ps1 -Status` → linha **Servidor
atual** com a URL correta (ou `nao encontrado`). Na bandeja: **Servidor do
laboratório → Abrir painel do monitor** abre o painel mesmo com a porta 5000
fechada neste PC; **Buscar servidor na rede** mostra `Servidor encontrado:
http://...:5000`. Desligar o servidor e reabrir → aviso de servidor não
encontrado. Reiniciar a bandeja para carregar o código novo.

## IS-164 — Bloqueio rígido de jogos e tela reaberta sem login 🟢
> ⚠️ A parte de *jogos sempre fechados* foi ajustada pela **IS-172**: agora os jogos só são fechados com o bloqueio persistente ativo.

**Sintoma:** PCs com aluno jogando **Roblox** e **Loki/Poki** apareciam no painel
como `Roblox`/`Games` mas continuavam ativos; **Fortnite** não era fechado e a
tela de bloqueio podia ser encerrada sem o aluno validar o RA.

**Mudança (`lab_agent.py`, build 15 / `2026-11-12-bloqueio2`):**
- `BLOCKED_PROCESS_KEYWORDS` agora inclui **Fortnite** (`fortnite`,
  `fortnitelauncher`) e o launcher da **Epic**; `BLOCKED_SITE_KEYWORDS` cobre
  Fortnite/Epic, Roblox, Loki/Poki/Friv/Y8/ClickJogos/Gartic, Temple Run,
  Subway Surf, Among Us, Free Fire, Valorant/CS/Minecraft etc.
- O **watchdog** derruba esses processos e fecha as janelas de jogos **sempre**
  (`WATCHDOG_EXCLUDE_KEYWORDS` vazio), sem depender de "Bloquear Sites/Jogos".
  Esse bloqueio persistente (`block_state.json`) fica só para redes sociais/YouTube.
- `get_category()` detecta jogos também por **processo** (Roblox/Fortnite/LoL),
  não só pelo título da janela.
- **Tela de bloqueio:** `sysava_lock.ps1` grava
  `%LOCALAPPDATA%\SysAva\tela_ok.json` ao validar (aluno, admin ou modo offline).
  O agente comparar o `em` com o **início da sessão do Windows**
  (`psutil.users().started`) e **relança a tela** quando o processo some sem
  token válido (cooldown de 30 s; não relança se o professor liberou via
  `tela_liberada.json`). O payload passou a enviar `lock_ok`/`lock_ok_ra`; o
  painel mostra **liberada (aluno)** em vez de "sem tela".
- `bloquear_hosts.ps1` ganhou Fortnite/Epic e os portais de jogos.
- `lab_agent.ps1` foi **ressincronizado** (cópia embutida idêntica ao `.py`).

**Arquivos:** `data/repo/plugins/lab_agent.py`, `lab_agent.ps1`,
`sysava_lock.ps1`, `lab_receiver.py`, `plugins/monitor_rede/lab_monitor.py`,
`bloquear_hosts.ps1`, `blocked_apps.json`, `AGENTS.md`,
`plugins/monitor_rede/README.md`.

**Validar:** rodar **Atualizar Monitor (rápido)** nos PCs (painel mostra build
15). Abrir Roblox/Fortnite → processo encerrado em até ~4 s. Fechar a tela de
bloqueio sem validar → ela reabre em até ~30 s; validar o RA → painel mostra
**liberada (aluno)** e a tela não volta até o próximo logon.

## IS-165 — Controle com várias ações simultâneas 🟢

**Pedido:** às vezes é preciso aplicar duas ações juntas (ex.: fechar jogos +
alerta), mas a aba Controle só tinha **um** `selectbox`.

**Mudança (`lab_receiver.py`):**
- Ações viraram **chips agrupados** (Avisos, Jogos/sites, Limpeza, Tela/áudio,
  Sistema) com `name="acao"` repetido, **Marcar/desmarcar todas**, contador e
  **presets** de 1 clique (Anti-jogo, Aula focada, Liberar aula, Faxina, Fim da
  aula). O formulário aceita `request.form.getlist('acao')`.
- `_write_local_commands()` passa a **enfileirar** em `pending_queue` (limite de
  50 por PC, dedup do mesmo par ação/mensagem, expira em `COMMAND_TTL_SECONDS`).
  O `/ping` entrega **uma ação por ciclo** (~10 s) e devolve `queue_left`; o
  fallback `pending_command` de agentes/versões antigas continua funcionando.
- O plugin Streamlit (`plugins/monitor_rede/lab_monitor.py`) trocou o
  `selectbox` por `st.multiselect` + os mesmos presets e envia um POST por ação.

**Arquivos:** `data/repo/plugins/lab_receiver.py`,
`plugins/monitor_rede/lab_monitor.py`, `plugins/monitor_rede/README.md`,
`AGENTS.md`.

**Validar:** aba Controle → marcar 2+ ações (ou clicar em **Anti-jogo**) →
*Executar nas selecionadas*; a mensagem mostra `N ação(ões)` e o PC recebe uma a
cada ~10 s (log do agente `Comando recebido...`). Repetir a mesma ação não
duplica na fila.

## IS-169 — Runtime do monitor movido para `data/repo/plugins/monitor/` 🟢

**Pedido:** concentrar todos os arquivos do sistema de monitoramento em uma pasta
`monitor/` e corrigir os caminhos de apontamento, conferindo o que ficou fora.

**Mudança de layout (runtime, `data/repo/plugins/monitor/`):**
- Scripts: `lab_receiver.py`, `lab_receiver.bat`, `lab_agent.py/.ps1`,
  `lab_monitor.py`, `lab_monitor_doc.md`, `sysava_lock.ps1`, `tray_servidor.*`,
  `tray_aluno.*`, `diagnostico_servidor.*`, `reiniciar_servidor.*`,
  `INICIAR_SERVIDOR.*`, `instalar_servidor_auto.*`, `servidor_watchdog.ps1`,
  `bloquear_hosts.*`, `ATUALIZAR_PC01.*`, `check_sysava.bat`, `audit_log.py`.
- Dados/apoio movidos para a mesma pasta: `acesso_coletivos.json`,
  `alunos_cache.json`, `blocked_apps.json`, `emails.json`, `lab_users.json`,
  `lab_status.json`, `lab_labels.json`, `site_padrao.json`,
  `receiver_secret.key`, `logo_sysava.png`, `wallpaper_sysava.png`,
  `definir_volume.ps1`, `aplicar_papel_parede.ps1`,
  `aplicar_dns_seguro.ps1`, `config.env.example`, `gerar_logo_sysava.py`,
  `categorias/`, `.atividades/`, `.relatorios/`.
- O restante de `data/repo/plugins/` (notas, frequência, planos, auditoria,
  backups) ficou onde estava — não é runtime do monitor.

**Paths corrigidos:**
- `lab_receiver.py`: `PROJECT_ROOT` e a leitura de `data/Turmas` passaram a subir
  **quatro** níveis (monitor → plugins → repo → data → raiz); `.env` continua
  sendo lido da raiz. O receiver agora serve `/download/*` e `/servidor.zip` da
  pasta `monitor/` (todos os arquivos da whitelist e do zip estão lá).
- `lab_monitor.py` (Streamlit): resolução robusta (`SYSAVA_PLUGIN_DIR` →
  `data/repo/plugins/monitor` → `data/repo/plugins`), achando a raiz por
  `app.py`/`data/repo/plugins`; a cópia de runtime foi sincronizada.
- `.sysenv`/`.env`: `lab_receiver.bat`, `tray_servidor.ps1`,
  `reiniciar_servidor.ps1`, `instalar_servidor_auto.ps1` e
  `diagnostico_servidor.ps1` passaram a procurar quatro níveis acima (mantendo
  o caminho antigo como fallback).
- `ATUALIZAR_PC01.bat`, `check_serv.py`, `run_installer.bat`,
  `servidor_instalacao.bat` e `sysava_tray.ps1` (receiver/logo/peers) apontam
  para `monitor/` com fallback para a pasta antiga.
- `SERVER_VERSION` → `2026-11-12-monitor-pasta`.

**Arquivos:** `data/repo/plugins/monitor/*`, `plugins/monitor_rede/lab_monitor.py`
e `README.md`, `check_serv.py`, `run_installer.bat`, `servidor_instalacao.bat`,
`sysava_tray.ps1`, `AGENTS.md`, `plugins/README.md`, `docs/PLUGINS.md`.

**Validar:** `python -m py_compile` nos `.py`; parser do PowerShell nos `.ps1`;
receiver iniciado de `monitor/` responde `/health` (versão
`2026-11-12-monitor-pasta`); `/download/lab_agent.py`, `logo_sysava.png`,
`emails.json`, `definir_volume.ps1` e `config.env.example` retornam 200;
`/servidor.zip` contém `lab_receiver.py`, `audit_log.py`, `emails.json`,
`blocked_apps.json`, `categorias/LEIA-ME.txt` e `check_sysava.bat`.

## IS-170 — Ferramentas em abas + abrir SysAva com RA no navegador 🟢

**Pedido:** a aba **Ferramentas** do painel web era uma página longa e cansativa.
Separar por funcionalidade, com abas/controles, e criar um recurso para abrir o
SysAva já com o RA do aluno no navegador escolhido — sem reiniciar o PC ao
trocar de estudante.

**Mudança (painel web, `data/repo/plugins/monitor/lab_receiver.py`):**
- A seleção de PCs (e **Aplicar em todas**) ficou fixa no topo; abaixo entraram
  **sub-abas**: **📁 Atividades**, **🌐 Sites e RA**, **🔒 Tela** e
  **🧹 Manutenção**. A seção "Último comando por PC" virou um `details`
  recolhível. O visual usa chips/abas no mesmo estilo da aba Controle.
- **🌐 Sites e RA → Abrir SysAva com o RA do aluno:** escolhe **aluno (RA)**,
  **navegador** (padrão, Chrome, Edge, Firefox, Brave ou Opera) e a **URL**
  (padrão `https://sysava.streamlit.app`, ou `SYSAVA_PORTAL_URL` no `.env`);
  grava a última URL em `sysava_padrao.json`.
  - A rota `POST /abrir_sysava` monta `?ra=<RA>`, associa o aluno ao PC
    (`lab_users.json`) e propaga aos peers, e envia o comando
    **"Abrir SysAva (RA)"** com `{url, browser, ra}`. Requer **agente build 16+**
    (PCs antigos são ignorados com aviso).
- **🌐 Abrir site** ganhou o mesmo seletor de navegador (`navegador_site`); o
  JSON agora leva `browser`. O agente build 16 usa o navegador escolhido; os
  anteriores continuam abrindo no padrão.
- **Agente (`lab_agent.py` 16 / `2026-11-12-sysava-ra`):** novo branch
  **"Abrir SysAva (RA)"**, `_abrir_url(url, navegador)` e
  `_encontrar_navegador` (Chrome/Edge/Firefox/Brave/Opera em Program Files/
  LocalAppData + `shutil.which`), com fallback para `os.startfile`.
  `lab_agent.ps1` foi ressincronizado.
- A tabela do Monitor passou a usar `agent_build_min=16`, sinalizando
  **"agente antigo — atualize"** nos PCs com build anterior.
- **🔄 Atualizar lista de alunos**: botão em **Ferramentas → Sites e RA** e em
  **Controle → Aluno do PC**. `POST /atualizar_alunos` chama
  `_lista_alunos(forcar=True)`, ignora o cache de 30 min e relê
  `app_users` (`role=student`); a lista atualiza o seletor de RA e a tela de
  bloqueio (`/api/alunos`). Em falha de Supabase, mantém o cache e avisa.

**Arquivos:** `data/repo/plugins/monitor/lab_receiver.py`, `lab_agent.py`,
`lab_agent.ps1`, `docs/ISSUES_LOCAIS.md`, `AGENTS.md`,
`plugins/monitor_rede/README.md`.

**Validar:** (1) `py_compile`/parser OK; (2) render do dashboard com 4 sub-abas
e 1 campo `todas`; (3) teste do `/abrir_sysava` com dispatch fake devolve
`{"url": "...?ra=123", "browser": "chrome"}` e associa o RA; (4) no painel,
atualizar os agentes (build 16) e usar **Ferramentas → Sites e RA → Abrir
SysAva com RA** em um PC; o navegador escolhido abre a página com o RA.

## IS-171 — Bandejas: IP/2º servidor e RA do aluno 🟢

**Pedido:** a bandeja do servidor não atualizava o IP nem abria a janela do
segundo servidor (só mostrava o IP encontrado); a bandeja do aluno precisava
mostrar o RA para copiar.

**Mudança (`data/repo/plugins/monitor/`):**
- **`tray_servidor.ps1`**: o título/tooltip/menu passam a mostrar o **IP atual**
  (atualizado a cada ~15 s) e o item **Abrir painel web (IP:5000)**. Novo item
  **Abrir painel do 2º servidor** consulta `/api/peer/state` e abre o peer
  (notebook ou PC auxiliar). `-Status` mostra o IP. Também ganhou os atalhos
  **Abrir SysAva (8501)** e **Apps** (inicia o Streamlit local quando `.sysenv`/
  `app.py` existem; senão abre o portal na nuvem) e **Parar todos os apps**.
- **`sysava_tray.ps1`** (bandeja do notebook): além do servidor principal, o
  menu agora lista **todos os servidores encontrados** (local + peers + UDP),
  com **Abrir painel do 2º servidor** e submenu por IP; o título mostra o IP do
  servidor atual (não só o IP local). A descoberta roda em runspace a cada 20 s.
  O **IP local e o `ServidorIp` são recalculados a cada ~25 s** e cada candidato
  só entra na lista se `/health` responder — o IP antigo da escola
  (`192.168.11.x`) deixa de aparecer como online quando o notebook muda para
  `192.168.0.x`; o servidor local atual (`192.168.0.8`) é detectado por UDP.
  **A bandeja antiga precisa ser reiniciada** para carregar essa versão.
- **`tray_aluno.ps1`**: o título mostra **nome + RA**; novos itens **Mostrar meu
  RA** e **Copiar meu RA** (além do e-mail). O RA vem da API/cache
  (`meu_email.txt`) ou de `%LOCALAPPDATA%\SysAva\ultimo_ra.txt` (gravado pelo
  `sysava_lock.ps1`). `-Status` mostra o RA.

**Arquivos:** `sysava_tray.ps1`, `data/repo/plugins/monitor/tray_servidor.ps1`,
`data/repo/plugins/monitor/tray_aluno.ps1`, `plugins/monitor_rede/README.md`,
`AGENTS.md`.

**Validar:** `powershell -File ...\tray_servidor.ps1 -Status` mostra o IP;
`tray_aluno.ps1 -Status` mostra o RA (após passar pela tela de bloqueio). Na
bandeja, o item do 2º servidor abre o painel do peer; o aluno copia o RA pelo
menu. Reinicie as bandejas para carregar o script novo (ou use **Atualizar
Bandeja do Aluno** no painel).

## IS-172 — Roblox não desbloqueava (watchdog) 🟢

**Sintoma:** depois de "Desbloquear Sites/Jogos", o Roblox continuava sendo
encerrado a cada ~4 s. Causa: na IS-164 o watchdog passou a derrubar
Roblox/Fortnite/League **sempre**, ignorando o `block_state.json`; o
"Desbloquear" só apagava o arquivo de estado.

**Correção (`lab_agent.py` 17 / `2026-11-12-desbloqueio`):**
- O watchdog volta a respeitar o estado: com `block_state.json` **inativo**,
  processos em `WATCHDOG_EXCLUDE_KEYWORDS` (**roblox**, **fortnite**,
  **leagueclient**, **epicgameslauncher**) ficam livres.
- Janelas de jogos/sites só são fechadas quando o bloqueio está **ativo**; com
  "Desbloquear Sites/Jogos" param de ser fechadas.
- O comando manual **Bloquear Jogos** continua fechando uma vez (sem manter).
- `lab_agent.ps1` foi ressincronizado. A tabela do painel passa a mostrar
  build 17.

**Como liberar um PC agora:**
1. **Controle → Atualizar Monitor (rápido, sem UAC)** para instalar o agente 17.
2. **Controle → Jogos → Desbloquear Sites/Jogos** (remove o `block_state.json`).
3. Se o painel não estiver acessível, no PC: apague
   `C:\Local\SysVa_lab\block_state.json`, substitua o `lab_agent.py` pelo novo
   (`/download/lab_agent.py`) e reinicie o agente/logon.

**Arquivos:** `data/repo/plugins/monitor/lab_agent.py`,
`data/repo/plugins/monitor/lab_agent.ps1`, `plugins/monitor_rede/README.md`,
`AGENTS.md`, `docs/ISSUES_LOCAIS.md`.

**Validar:** com `block_state.json` ausente, o watchdog não mata
`RobloxPlayerBeta.exe`; com o arquivo ativo, volta a matar e fecha janelas;
"Desbloquear" remove o arquivo e libera.

## IS-188 - Notas iSeduc: replicação entre trimestres lendo o portal 🟢

**Contexto:** Fundamentos de UI/UX (I-A) estava com notas só no 1º trimestre
no iSeduc. O caderno local divergia da tela, então a cópia precisava sair dos
inputs do próprio portal (T1) para T2/T3.

**Solução:** ver `apps/ISSUES.md` **AP-042**. Resumo: modo
`--replicar-origem/--replicar-destinos` no `bot_lancar_notas.py`, leitura
`ler_notas_trimestre()` no `RegistradorNotas`, conferência com F5 + releitura e
regravação das células divergentes, commit por `TAB`/`blur` (`ng-blur` do
portal) e retry no mapeamento dos RAs após troca de aba.

**Execução:** I-A / Fundamentos UI/UX, T1 → T2 e T3, 17 alunos (LUARA sem nota
no portal; “0,0” da tela é placeholder de input vazio). T3 foi reescrito após
a correção do `TAB`.

**Ficha de acompanhamento:** `data/fichas/` regerada com
`scripts/baixar_ficha_rendimento.py --preset fundamentos-ui` (I-A e I-B); o
PDF de I-A passou a mostrar T2/T3 iguais ao T1.

**Arquivos:** `apps/bots/registrar_notas.py`,
`apps/analise_notas/bot_lancar_notas.py`,
`apps/analise_notas/analise_notas_streamlit.py`,
`apps/analise_notas/core.py`, `apps/analise_notas/README.md`,
`scripts/baixar_ficha_rendimento.py`, `data/fichas/*.pdf` (local),
`apps/ISSUES.md`.

**Como validar:** iSeduc → Notas → FUNDAMENTOS DE UI/UX (I-A) → 2º e 3º
trimestres com os mesmos `NM1/NM2/NM3` do 1º e médias recalculadas. No app
8511, usar o expander *🔁 Replicar notas do portal entre trimestres* em modo
simulação.

## IS-189 - Notas iSeduc: recuperações RPT a partir do SysAva 🟢

**Contexto:** Fundamentos UI/UX (I-A e I-B) estava com T1=T2=T3, mas as
colunas `RPT1/2/3` da ficha vazias. As recuperações estavam no SysAva como
avaliações `type='RM'` no Supabase: `RECUPERAÇÃO_T1` (id 63), com ANDRESSA
(I-A) 10, ANA KAROLLINY (I-B) 10 e MATHEUS SOUSA SILVA (I-B) 9. No portal, o
RPT fica nas abas **`RESULTADO DO Xº TRIMESTRE`** (colunas `1RPT/2RPT/3RPT`),
não na tabela normal de notas.

**Solução:** ver `apps/ISSUES.md` **AP-043**. Resumo: seleção de aba por texto
exato (`selecionar_aba_exata`), `lancar_recuperacao()` (lê RPT/MTF, grava,
recalcula, F5 e confere), CLI `--recuperacao`/`--rm-assessment-id` lendo a RM
do Supabase e recortando pela matrícula da turma.

**Execução (17/11/2026):** I-B ANA 10,0→MTF 10,0 e MATHEUS 9,0→MTF 9,0; I-A
ANDRESSA 10,0→MTF 10,0. Fichas regeradas em `data/fichas/`: MAF 7,1 / 5,7 /
6,7 (antes 5,6 / 4,0 / 5,0).

**Arquivos:** `apps/bots/registrar_notas.py`,
`apps/analise_notas/bot_lancar_notas.py`, `apps/analise_notas/README.md`,
`apps/tests/test_analise_notas.py`, `apps/ISSUES.md`,
`data/fichas/*.pdf` (local).

**Como validar:** iSeduc → Notas → UI/UX → `RESULTADO DO 1º TRIMESTRE`; rodar
`bot_lancar_notas.py --turma-id 1|2 --disciplina-id 8 --trimestre 1
--recuperacao --simular` e conferir RPT/MTF.

## IS-190 - Programação Mobile: T1/T2/T3 da I-A (plugin Notas → portal) 🟢

**Contexto:** o portal estava vazio em Mobile nas duas turmas. O professor
lançou as notas da I-A no plugin **Notas** e salvou o quadro em
`data/fichas/quadro_notas_..._ProgMobile.png`. O quadro confere com o caderno
local (N1/N2/N3 do T1).

**Execução:** `bot_lancar_notas.py --turma-id 1 --disciplina-id 5
--trimestre 1 --incluir-zeros` → 17 alunos (FRANCISCO JOEL fora do portal;
LUARA/[ALUNO]/GUILHERME pela lista negra). Piso AEE: **CLEISON** `6/9/6` e
**PEDRO** `6/6/6`. ANDRESSA `4/0/2,5` (como no plugin; AV02 10,0 não usada).

**T2/T3:** `--replicar-origem 1 --replicar-destinos 2 3` copiou os 17 alunos;
conferência pós-F5 em cada destino: 17 iguais ao T1. Ficha regerada com
T1=T2=T3 e MAF (0 divergências em 18 linhas).

**Verificação:** releitura em sessão nova: 17 alunos com T1/T2/T3 e MTF;
RPT vazio. Ficha em
`data/fichas/2ª SÉRIE - Turma I-A (Técnico DS)_PROGRAMAÇÃO PARA DISPOSITIVOS MÓVEIS.pdf`;
levantamento em `data/logs/mobile_notas_sysava.csv`.

**Pendente:** só a I-B (há seminários/AV02 no Supabase; falta definir o N3).

**Arquivos:** `apps/analise_notas/bot_lancar_notas.py`,
`scripts/baixar_ficha_rendimento.py`, `data/fichas/*` (local),
`data/logs/mobile_notas_sysava.csv` (local), `apps/ISSUES.md`.

**Como validar:** iSeduc → Notas → Mobile (I-A) → 1º trimestre; abrir a ficha
em `data/fichas/` e conferir as 17 linhas + LUARA sem nota.

## IS-191 - Registro de aulas: Mobile I-B (23/07 a 30/07) 🟢

**Contexto:** a I-B tinha 12 registros de Mobile no portal (até 20/07, todos
“Aguardando confirmação”) e **10 planos prontos** em `aulas/prontas/` para
23/07–30/07 (Aulas 13–22) que nunca foram registrados.

**Execução:** `registrar_aulas.py --files ...` com os 10 planos; todos
registrados e movidos para `aulas/registradas/`.

**Verificação:** portal I-B passou de **12 → 22 registros** (23/07: 5; 24/07:
1; 27/07: 2; 30/07: 2), todos “Aguardando confirmação”. I-A continua com 36.

**Pendente (sábados, o robô pula por regra):**
- I-A: 11/07 07:10 (Aula 9); 15/08 08:10/09:30 e 12/09 07:10 — os dois últimos
  têm conteúdo da I-B e repetem Aulas 3/4/5 já registradas; conferir.
- I-B: 11/07 08:10/09:30 (Aulas 1/2), “reservado para a coordenação”.

**Arquivos:** `aulas/prontas/` (planos movidos), `aulas/registradas/`,
`apps/bots/registrar_aulas.py`, `apps/ISSUES.md`.

**Como validar:** iSeduc → Registro de aulas → Mobile I-B → 23/07 a 30/07.

## IS-192 - Mobile: fechamento 40/40 e sincronização da carga anual 🟢

**Contexto:** a carga anual tem **8 disciplinas modulares mensais** de 40
aulas. Mobile estava em 36/40 na I-A e 22/40 na I-B. Sábado não pode ser
registrado pelo professor (calendário recusa o dia), então fica para a
coordenação.

**Execução:**
- I-B: 16 planos gerados/registrados (Aulas 23–32 e 35–40) em 31/07, 03/08,
  06/08, 07/08, 10/08 e 13/08 → portal 22 → 38.
- I-A: 36 (4 restantes são sábados).
- `historico_aulas` sincronizado com os 74 registros do portal (36 I-A + 38
  I-B), incluindo “Aguardando confirmação”.
- `planejamento` I-A: 36 `registrada` + 4 `pendente`; I-B: 2 `pendente`
  (11/07 Aulas 1/2). Removidas 6 linhas falsas do gerador + 1 obsoleta.

**Carga (Mobile = 40):** I-A 36+4=40; I-B 38+2=40; faltantes 0.

**Sábados para a coordenação (`aulas/pendentes/`):**
- I-A: 11/07 Aula 9; 15/08 Aulas 3/4; 12/09 Aula 5 (os dois últimos com
  conteúdo da I-B — conferir).
- I-B: 11/07 Aulas 1/2.

**Importante:** `registrar_aulas.py` voltou a **pular sábados sempre**; a
tentativa com `--permitir-sabado` foi revertida e falhou no calendário
(“Dia 11 não encontrado”). Não registrar sábado pelo robô.

**Arquivos:** `apps/bots/registrar_aulas.py`, `aulas/pendentes/`,
`aulas/registradas/`, `data/escola_ativa.db` (histórico/planejamento),
`apps/ISSUES.md`.

**Como validar:** app 8510 → Consolidadas → Mobile I-A/I-B = 40 (registradas
+ pendentes), faltantes 0; portal com 36/38 registros.

## Comandos úteis

```powershell
# Push (o `credential.helper=helper-selector` do gitconfig do sistema trava em
# GUI e o GCM não está no PATH — git só procura em libexec/git-core, onde só
# há wincred). Bypass: ignora o config do sistema e aponta o GCM absoluto.
$env:GIT_CONFIG_NOSYSTEM='1'; $env:GIT_TERMINAL_PROMPT='0'; $env:GCM_INTERACTIVE='never'
git -c "credential.helper=C:/Users/Helio/AppData/Local/hermes/git/mingw64/bin/git-credential-manager.exe" push origin main

# Migração de títulos de quiz (simulação / aplicar)
python scripts/migrate_quiz_titles.py
python scripts/migrate_quiz_titles.py --apply

# Reset seletivo de tentativas (simulação / aplicar)
python scripts/reset_quiz_attempts.py
python scripts/reset_quiz_attempts.py --apply

# Verificar se o cache local está ligado
python -c "from services import local_cache as lc; print(lc.cache_enabled())"

# Limpar uma chave "envenenada" do cache local (ex.: lista vazia de turmas)
python -c "from services import local_cache as lc; lc.invalidate('classes')"
python -c "from services import local_cache as lc; print(lc.status())"

# Bandeja do SysAva (notebook): status + servidor atual descoberto na rede
sysava_tray.bat
powershell -NoProfile -ExecutionPolicy Bypass -File sysava_tray.ps1 -Status

# Servidor auxiliar (PC do laboratorio): bandeja no logon + diagnostico
data\repo\plugins\monitor\tray_servidor.bat
powershell -NoProfile -ExecutionPolicy Bypass -File data\repo\plugins\monitor\tray_servidor.ps1 -Status
data\repo\plugins\monitor\diagnostico_servidor.bat

# Pacote de atualizacao servido pelo receiver (ja inclui tray + diagnostico)
curl.exe -L -o servidor.zip http://127.0.0.1:5000/servidor.zip

# Tailscale (acesso remoto ao laboratorio - ver docs/TAILSCALE.md)
tailscale status
tailscale ip -4
# no PC01-LAB02 (Admin): anunciar a sub-rede do laboratorio
tailscale up --advertise-routes=192.168.10.0/23
# no notebook: aceitar as rotas anunciadas
tailscale up --accept-routes

# Backup limpo (sem Base64) a partir de data/escola_ativa.db
python scripts/backup_clean.py

# Preparar o backup para restauração (normaliza datas e remove duplicatas)
python scripts/prepare_restore.py

# Simular / executar a restauração no novo Supabase
python scripts/restore_new_supabase.py --dry-run
python scripts/restore_new_supabase.py --url <nova-url> --key <nova-anon-key>

# Auditar/limpar duplicatas de bot no fórum (dry-run / aplicar)
python scripts/cleanup_forum_duplicates.py
python scripts/cleanup_forum_duplicates.py --apply

# Lista negra: JSON -> banco (dry-run / aplicar + regenera o espelho local)
python scripts/migrar_excecoes_para_banco.py --dry-run
python scripts/migrar_excecoes_para_banco.py

# Bloqueio não invasivo via hosts (rodar em cada PC; pede Administrador)
powershell -NoProfile -ExecutionPolicy Bypass -File data\repo\plugins\monitor\bloquear_hosts.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File data\repo\plugins\monitor\bloquear_hosts.ps1 -Revert

# Verificar se o receiver esta ouvindo (TCP 5000 + UDP discovery 5001)
netstat -ano | findstr ":5000 :5001"

# Contas coletivas e janela EJA (editar e reiniciar o receiver)
data\repo\plugins\monitor\acesso_coletivos.json
# Lista: {"coletivos": ["7anoA","8ano","1alunoEja"], "eja": {"contas": ["1alunoEja"], "inicio": 17, "fim": 23}}

# PC mestre (senha admin da tela de bloqueio) - hostnames exatos ou curinga
C:\ProgramData\SysAva\master_hosts.txt   # uma entrada por linha; padrao: PC01*
# ou definir SYSAVA_MASTER_HOSTS="PC01,NOTE-PROF" antes de abrir a tela

# Criar conta coletiva no Supabase (exemplo via REST; senha = hash bcrypt)
# role=student, is_active=true, is_portal=true; depois incluir em acesso_coletivos.json
```

## Histórico de commits relacionados

| Commit | Descrição |
| ------ | --------- |
| `c413d8f` | Sync `data/calendario_letivo.json` → `master_config` (datas + 18 sábados) e gitignore do backup |
| `704a1ae` | Registra IS-038 revisado: carga de 880h, Gantt de 22 barras e divergência das fontes do calendário |
| `c72046a` | Registra IS-038: aba Consolidadas no app 8510 e disciplina_ids no calendario |
| `39ad23d` | Planejamento: feriados bloqueiam geração/registro, configs migram p/ master_config e frequência ao vivo (IS-037) |
| `55e94f1` | Corrige quizzes com títulos duplicados e conclusão cruzada |
| `3e365c5` | Cache SQLite de scores no plugin de atividades diárias |
| `0393486` | Reduz egress do Supabase com cache local e documenta issues |

## IS-155 - Monitor: backup de atividades no plugin e comandos perdidos por concorr?ncia 🟢

**Problema:** no plugin Monitor (Streamlit) existia s? o link ?Backups de atividades
(recebidos)?; n?o havia bot?o para *solicitar* o ZIP aos PCs. Al?m disso, o bot?o do
painel web ?s vezes ?no fazia nada?: o /ping e o enfileiramento de comandos faziam
l?r-modificar-gravar separados no lab_status.json, e o /ping podia sobrescrever um
comando rec?m-gravado (alguns PCs ?n?o recebiam?). O save_data ainda engolia erro de
lock (	imeout=1), ent?o a UI dizia ?enviado? sem ter gravado. Por fim, o agente
falhava com FileNotFoundError quando %USERPROFILE%\Documents\SysAva n?o existia.

**Corre??o:**
- plugins/monitor_rede/lab_monitor.py: se??o ?Backup de atividades? na aba
  Ferramentas (multiselect de PCs + pasta base) que enfileira Enviar Atividades.
- data/repo/plugins/lab_receiver.py: _mutate_status() (l?/grava sob um ?nico lock);
  /ping e _write_local_commands usam esse helper; save_data at?mico (tmp+replace)
  e timeout de lock de 5s; dispatch_commands devolve quantas m?quinas receberam o
  comando (sem contar falhas).
- data/repo/plugins/lab_agent.py e lab_agent.ps1: _escolher_base_atividades()
  procura a pasta em perfis do Windows/OneDrive/Public e d? erro claro se n?o achar,
  em vez de falhar em C:\Users\Aluno\....

**Como validar:**
1. Reiniciar o receiver (
einiciar_servidor.bat) e atualizar os agentes
   (Controle ? Atualizar Monitor (r?pido, sem UAC)).
2. No plugin Monitor ? Ferramentas ? Backup de atividades, selecionar PCs e clicar
   ?Solicitar ZIP das atividades?.
3. Conferir lab_receiver.log (BACKUP ATIVIDADES solicitado... seguido de
   ATIVIDADES recebidas de ...) e a p?gina /atividades.
4. Em PC sem a pasta, o resultado do comando deve mostrar
   erro: pasta de atividades nao encontrada (procurei: ...).

## IS-156 - Tela de bloqueio: bloquear palavras fora da lista (exceto PC01) 🟢

**Problema:** a tela de bloqueio (sysava_lock.ps1) aceitava a senha de
administrador (padrao labadmin) em qualquer PC. Assim era possivel liberar os
PCs dos alunos digitando labadmin, luno ou qualquer outra palavra. Tambem
nao havia uma checagem local de que o texto digitado pertencia a lista de alunos
exibida na tela.

**Correcao:**
- data/repo/plugins/sysava_lock.ps1:
  - Test-MasterPC / Get-MasterHosts: a senha admin (Test-SenhaAdmin) so
    funciona no **PC mestre**. Padrao: hostnames que comecam com PC01.
    Personalize com SYSAVA_MASTER_HOSTS (ex.: PC01,NOTE-PROF) ou com
    C:\ProgramData\SysAva\master_hosts.txt.
  - Test-PalavraProibida: recusa palavras genericas (labadmin, luno,
    dmin, professor,
oot, ...) em PCs comuns, mesmo antes de a lista
    carregar.
  - Test-ItemDaLista: nos PCs comuns, o texto digitado precisa existir na
    lista da tela de bloqueio (item do seletor, nome completo ou RA).
- instalar_tela_sysava.ps1 nao muda: o script atualizado e baixado do servidor
  por Atualizar Tela de Bloqueio (sem UAC).

**Como validar:**
1. Atualizar a tela: Controle ? Atualizar Tela de Bloqueio (sem UAC) (ou
   reinstalar em setup/instalar_tela_sysava.ps1).
2. Em um PC de aluno, tentar labadmin, luno, dmin ? deve recusar.
3. Em um PC de aluno, selecionar um aluno da lista ou digitar o RA ? deve liberar.
4. No PC01 (ou hostname configurado em master_hosts.txt), a senha admin
   continua liberando mesmo sem servidor.

## IS-157 - RA unico: nao pode logar o mesmo RA em dois PCs 🟢

**Problema:** o mesmo RA podia passar pela tela de bloqueio em varios PCs ao
mesmo tempo (o `lab_users.json` guardava a ultima maquina, mas nao impedia o
login em outra).

**Correcao (data/repo/plugins/lab_receiver.py):**
- `_autorizar_login_ra()`: antes de associar o RA, verifica se ele esta ativo em
  outra maquina (`_ra_em_outra_maquina`). Se estiver, devolve **400** com
  `error` (a tela de bloqueio mostra a mensagem) e `em_uso` (hostname).
- `_maquinas_ativas()`: considera ocupada apenas a maquina com sinal recente
  (`OFFLINE_SECONDS`, 60s). Ao **deslogar/desligar** o PC, o agente para de
  pingar e o RA e liberado para entrar em outro PC.
- `_USERS_LOCK` (RLock) serializa checagem + associacao; `_save_users_map`
  grava de forma atomica (tmp + replace) para nao perder dados em logins
  simultaneos.
- `SERVER_VERSION` -> `2026-11-05-ra-unico`.

**Como validar:**
1. Reiniciar o receiver (`reiniciar_servidor.bat`).
2. Logar um RA no PC A; tentar o mesmo RA no PC B: deve aparecer
   "O RA ... ja esta em uso em <PC>. Saia daquela maquina para entrar nesta."
3. Fazer logoff no PC A (ou desliga-lo), esperar ~60s e repetir no PC B: deve
   liberar. Entrar de novo no PC A com o mesmo RA continua permitido.

## IS-158 - Contas coletivas e janela de acesso do EJA 🟢

**Pedido:** manter as contas coletivas (ex.: `7anoA`, `7anoB`) fora da regra de
RA unico; criar `8ano`, `9ano` e `1alunoEja`; e permitir que as contas do EJA
entrem apenas das **17h as 23h**.

**Contas criadas no Supabase (`app_users`, role `student`, `is_active=true`):**
| username/ra | name | senha inicial |
| ----------- | ---- | ------------- |
| `8ano` | 8 Ano | `8ano` |
| `9ano` | 9 Ano | `9ano` |
| `1alunoEja` | 1 Aluno EJA | `1alunoEja` |

Troque as senhas no Admin se necessario.

**Mudancas (data/repo/plugins/lab_receiver.py):**
- `acesso_coletivos.json` (novo) configura `coletivos` e `eja.contas` +
  `eja.inicio`/`eja.fim` (padrao 17 e 23). Ha um padrao embutido caso o arquivo
  nao exista.
- `_e_conta_coletiva()`: contas em `coletivos` **nao** entram na regra de RA
  unico (`_autorizar_login_ra` pula `_ra_em_outra_maquina`). Assim `7anoA`,
  `8ano`, etc. podem estar em varios PCs ao mesmo tempo.
- `_e_conta_eja()` + `_janela_eja_aberta()` + `_eja_pode_entrar()`: contas EJA
  (`1alunoEja`, `Alunos_EJA_Noite`) so sao aceitas entre 17h e 23h (hora local
  do servidor). Fora da janela o `/api/auth_ra` responde **400** com
  "Acesso EJA permitido apenas das 17h as 23h." e a tela de bloqueio exibe.
- `alunos_cache.json` foi apagado para o seletor recarregar as novas contas.

**Observacao:** a janela bloqueia **novos logins** fora do horario. Sessoes EJA
que ja estao abertas as 23h continuam ate o logoff (nao ha re-bloqueio
automatico). Se quiser o re-bloqueio as 23h, isso exige um comando/agendador no
agente.

**Como validar:**
1. Reiniciar o receiver (`reiniciar_servidor.bat`).
2. As novas contas devem aparecer no seletor da tela de bloqueio.
3. Entrar com `7anoA` em dois PCs ao mesmo tempo: deve permitir (coletivo).
4. Entrar com `1alunoEja` antes das 17h ou depois das 23h: deve recusar; entre
   17h e 23h: deve liberar.

## IS-159 - MENTORIAS TEC II: duplicatas das Aulas 21–35 e ordem das aulas 🟢

**Problema:** a disciplina `MENTORIAS TEC II` (`subjects.id=2`) tinha 51 aulas, com
as Aulas 21–25 e 26–35 duplicadas (cópias com `:`/emoji no título) e as Aulas
18/19/20 aparecendo depois da 35 na tela. A `id=70` (material de apoio de
PowerShell) é uma aula real, com posts de alunos, e foi mantida.

**Decisão "zero prejuízo":** as cópias duplicadas NÃO foram apagadas. Elas
receberam `status='arquivada'` e ficam ocultas das listagens, mas continuam no
banco — preservando 100% dos quizzes, mensagens do fórum e pontuações.

**Mudanças:**
- Banco: `status='arquivada'` nas aulas B `495-499` e `836-845`.
  Script: `scripts/archive_duplicate_lessons_mentorias.py` (`--apply`).
  Backup: `data/backups/lessons_mentorias_dedup_*.json`.
- `services/database.py`: `_LESSON_LIST_COLUMNS`/`_LESSON_FULL_COLUMNS` passaram a
  incluir `status`; `get_lessons_for_subject()` e `get_lessons_for_subject_full()`
  filtram `status='arquivada'`. `get_lessons()` continua retornando tudo (mapa de
  score).
- `views/aulas.py` (`group_lessons`): no agrupamento `anual`, ordena pelo número de
  "Aula N"; aulas sem número mantêm posição relativa à última numerada.

**Como validar:**
1. Abrir Aulas de "MENTORIAS TEC II": deve mostrar 36 itens (Aulas 1–35 + material
   sem número) sem repetições, com 18/19/20 entre 17 e 21.
2. Conferir que o fórum das Aulas 21–35 ainda mostra as mensagens e que o score dos
   alunos não caiu (arquivadas seguem contando no fórum).

## IS-160 - DevOps 2º ano: duplicatas do I-A e novas Aulas 17–20 🟢

**Contexto:** "INTRODUÇÃO AO ECOSSISTEMA DEVops" existe em duas turmas de 2º ano:
I-A (`subject_id=9`) e I-B (`subject_id=41`). As duas paravam na Aula 16.

**Duplicatas do I-A (`subject_id=9`):** as Aulas 4–16 tinham duas cópias. A segunda
cópia (ids `952-956`, `960-967`) tinha quiz genérico "📝 Quiz: Teste seu
Conhecimento!" sem questões e pouca atividade. Estratégia zero-prejuízo: ela foi
**arquivada** (`status='arquivada'`), mantendo quiz/fórum/pontuação. As cópias boas
(`906-941`) permanecem visíveis.

**Novas Aulas 17–20 (geradas via DeepSeek e replicadas nas duas turmas):**
| Aula | Tema | I-A (subject 9) | I-B (subject 41) |
| ---- | ---- | --------------- | ---------------- |
| 17 | Cloud Computing e DevOps | lesson 984 / quiz 805 | lesson 985 / quiz 806 |
| 18 | Pipeline CI/CD com Docker e deploy automatizado | lesson 986 / quiz 807 | lesson 987 / quiz 808 |
| 19 | SRE e gestão de incidentes (SLI/SLO/Error Budget) | lesson 988 / quiz 809 | lesson 989 / quiz 810 |
| 20 | Projeto Integrador DevOps | lesson 990 / quiz 811 | lesson 991 / quiz 812 |

- Semana `S03` (Aulas 17–24), conteúdo em `description` no padrão atual.
- Cada aula tem quiz próprio (`Quiz: Aula N: ...`) com **4 perguntas x 4 alternativas**.
- Cabeçalho de turma ajustado por disciplina (I-A na 9, I-B na 41). Sem imagens/Base64.

**Arquivos:**
- `scripts/seed_devops_aulas_17_20.py` (`dedup` e `generate`, ambos com `--apply`).
- Backups: `data/backups/devops_dedup_subject9_*.json` e
  `data/backups/devops_17_20_generated.json` (cache do conteúdo gerado).

**Como validar:**
1. Abrir Aulas de DevOps nas duas turmas: deve listar Aulas 1–20 sem repetição.
2. Abrir as Aulas 17–20 e confirmar conteúdo e quiz (4 questões).
3. Conferir que o fórum/pontuação antigos do I-A continuam intactos.

## IS-161 - iSeduc: planos de outubro/2026 (IA, Mentorias Tech II e PC II) 🟢

**Pedido:** atualizar as aulas registradas no iSeduc das disciplinas IA,
Mentorias Tech II e Pensamento Computacional II — setembro estava registrado e
faltava outubro.

**Diagnóstico confirmado:**
- Setembro/2026 registrado nas duas turmas (I-A `309197` e I-B `314114`).
- Outubro/2026 com **zero** registros em `historico_aulas`.
- `lessons` local defasada (parava em ~28–30) fazia o gerador cair em fallback e
  trocar o conteúdo (`AULA_NUM 31` → conteúdo da Aula 26).
- Havia só 7 planos de outubro (todos da I-B).

**Ações (fases seguras, sem tocar no portal):**
- `scripts/sync_lessons_from_supabase.py --subject 1,2,11 --apply`
  (backup `data/escola_ativa_backup_lessons_20261109_173728.db`).
- `scripts/gerar_planos_outubro_iseduc.py --apply`: gera 20 planos em
  `aulas/pendentes/` (8 na I-A, 12 na I-B) e faz upsert em `planejamento`.
  - `AULA_NUM` = sequência da turma; conteúdo = número da aula de conteúdo
    (que vinha atrasado), lido do Supabase ignorando `arquivada`.
  - Frequência exata só quando é da mesma disciplina; caso contrário usa o
    padrão (Presente, respeitando a lista negra).
  - Relatório: `data/logs/planos_outubro_validacao.json`.

**Pendente (fora desta fase):**
- Testar **1 aula** no iSeduc para confirmar se o portal aceita registro
  retroativo de outubro; depois rodar o lote com
  `apps/bots/registrar_aulas.py --files ...`.
- 9 datas ficaram com frequência padrão (sem `attendance` exata da disciplina).
- Observação: alguns planos de **setembro** já registrados também mostram
  `AULA_NUM` diferente do conteúdo (ex.: 31→Aula 26); revisar se necessário.

**Como validar:**
1. `python scripts/gerar_planos_outubro_iseduc.py` (dry-run) sem divergências.
2. Conferir os 20 `.txt` em `aulas/pendentes/` e as linhas de outubro em
   `planejamento`.
3. Após o teste no portal, confirmar em `historico_aulas` e `aulas/registradas`.

## IS-162 - iSeduc: notas de Programação Web Front-End (out/nov 2026) 🟢

**Sintoma:** PROGRAMAÇÃO WEB FRONT-END aparecia "sem notas" no iSeduc.
A investigação (somente leitura) mostrou:
- I-A (`subject 33`): só o **1º tri** tinha notas; **2º e 3º vazios**.
- I-B (`subject 34`): **1º, 2º e 3º vazios**.
- Único lançamento real anterior: 03/10/2026, I-A / 1º tri (log
  `RegistradorNotas_20261003_142108.log`). O 2º tri foi só dry-run e a I-B
  nunca foi lançada.

**Regras aplicadas (definidas pelo professor):**
- Web Front-End é módulo de 1º tri: **T2 e T3 = cópia do T1**.
- **Alice ([ALUNA], RA [RA])** está de **licença** →
  status `Licença` (piso 6,0) no `master_config`; ficou **6,0 nas 3 colunas**.
- Notas baixas permanecem (recuperação depois).
- **I-A 1º tri não foi alterado** (já estava lançado).

**Lançamentos (payloads em `data/logs/web_fe_payload_*.json`):**
- I-B: T1, T2 e T3 (20 alunos cada).
- I-A: T2 e T3 (16 alunos cada; bloqueados/transferidos fora).

**Verificação (leitura no portal após gravar):**
- I-B: 17/20 com nota nos **três** trimestres; Alice `6/6/6`.
- I-A: 14/18 com nota no **2º e 3º** tri (antes 0/18).

**Como validar:** abrir Notas → PROGRAMAÇÃO WEB FRONT-END nas turmas I-A e I-B
e conferir os três trimestres.

---

## IS-163 - DevOps 2º ano: Aulas 21-32 (conteúdo) e 33-40 (seminários) 🟢

**Contexto:** o professor está na Aula 16 e vai fechar o módulo DevOps (40h)
com sala de aula invertida: aulas 17-32 normais (pesquisa/registro) e 33-40
seminários de apresentação/debate dos pares de 17-32.

**Execução:** `scripts/seed_devops_aulas_21_40.py generate --apply` gerou as
Aulas 21-32 via DeepSeek (conteúdo + quiz 4x4) e criou as 33-40 como
seminários (roteiro, temas, questões de debate e rubrica; sem quiz),
replicando nas disciplinas `subject 9` (I-A) e `subject 41` (I-B), semana S03.

**IDs:** subject 9 → lessons 992-1030 (21-40), quizzes 813-835; subject 41 →
lessons 993-1031, quizzes 814-836. Cache:
`data/backups/devops_21_40_generated.json`.

**Verificação:** 40 aulas ativas por disciplina (1-40); quizzes 21-32 com 4
questões em ambas.

**Como validar:** abrir Aulas → INTRODUÇÃO AO ECOSSISTEMA DEVops e conferir
as Aulas 21-40 e os quizzes.

---

## IS-164 - DevOps: seminários 33-40 como Avaliações e grupos por chamada 🟢

**Contexto:** faltava lançar os 8 seminários de DevOps (Aulas 33-40) como
Avaliações e compor os grupos. O Lázaro (RA [RA]) estava com
`frequencia_status='falta'` no banco (`frequency_flags`, motivo "migracao do
JSON"), mesmo fora do `excecoes_alunos.json`, e por isso iniciava a chamada
como Falta.

**Execução:** `scripts/create_devops_seminars_assessments.py create --apply`:
- Corrigiu a flag do Lázaro para `normal` (`set_frequency_flag`) e sincronizou
  o espelho `data/excecoes_alunos.json` (ele continua fora da blacklist).
- Compôs **4 grupos por turma** (17 ativos, sem blacklist/dropouts) pela lista
  de chamada (ordem alfabética, distribuição round-robin; 5/4/4/4).
- Criou **8 avaliações tipo "Seminário"** por disciplina, no formato compatível
  com o plugin Atividades (`daily_activities.py`): questão subjetiva com
  "Integrantes do grupo" e "Pesquise e apresente as aulas abaixo".
- IDs: subject 9 (I-A) 47-54; subject 41 (I-B) 55-62. Lázaro no Grupo 4 da I-B
  (seminários 39 e 40).

**Como validar:** Avaliações → disciplina DevOps (I-A/I-B): 8 seminários com
grupo listado; Frequência: Lázaro inicia como Presente.

---

## IS-165 - Mobile (I-A): 20 aulas registradas e sábados preparados 🟢

**Contexto:** o iSeduc já tinha 15 aulas de Programação Mobile (I-A) registradas;
faltavam 20 dias úteis e os sábados (que ficam com a coordenação).

**Execução:** `apps/bots/registrar_aulas.py` registrou os **20 dias úteis**
(05/08 13:30 a 24/08 09:30) e a **Aula 1 de 03/07 às 07:10** (o portal só
oferecia 07:10; o plano foi ajustado de 08:10). O portal passou a **36 aulas
aguardando confirmação**. Correções no bot: seletor de data resiliente
(`data-day`/`td`/`button` + fallback JS), pulo explícito de sábado e
retry/abort no "Tipo de Aula" (evita falso sucesso). O 24/08 08:10, que havia
sido movido por falso sucesso, foi devolvido e re-registrado.

**Sábados (coordenação):** I-A 11/07 (1), 15/08 (2; equiv. segunda) e 12/09 (1)
= 4 planos em `aulas/pendentes`; I-B 11/07 (3) em `aulas/prontas`. Gerados por
`scripts/gerar_planos_sabados_mobile.py`.

**Como validar:** iSeduc → Registro de aulas (309197): 36 aguardando; 4 sábados
da I-A não registrados.

---

## IS-166 - Mobile (I-B): 2 primeiras aulas registradas em 13/07 🟢

**Contexto:** a I-B (turma `314114`) tinha Fundamentos UI com 40 aulas
confirmadas; a última em **11/07/2026 14:30–15:30**. Os planos antigos de
Mobile estavam em 11/07 08:10/09:30/13:30, mas o iSeduc **bloqueia 11/07**
(sábado) no formulário, inclusive para Aula Normal/Extra/Reposição.

**Execução:** o próximo slot livre era **segunda 13/07**, com 14:30 e 15:50
livres. Os planos foram ajustados para
`plano_314114_5_2026-07-13_1430.txt` (Aula 01) e
`plano_314114_5_2026-07-13_1550.txt` (Aula 02) e registrados por
`apps/bots/registrar_aulas.py --files ...`.

**Resultado:** 2 registros em 13/07 (14:30 e 15:50) como "Aguardando
confirmação"; os planos foram movidos para `aulas/registradas/`. O terceiro
plano antigo (11/07 13:30) ficou em
`aulas/prontas/_backup_mobile_ib_11-07/` até ser reagendado. O bot também foi
corrigido para não marcar falha falsa quando o print pós-salvamento quebra no
console cp1252 (AP-040).

**Como validar:** iSeduc → Registro de aulas (`314114`) → Programação Mobile:
2 aulas em 13/07 aguardando confirmação.

---

## IS-167 - Mobile (I-B): Aulas 33/34 antecipadas para a Feira das Profissões 🟢

**Contexto:** fechar a carga de Mobile I-B e reduzir o impacto do recesso,
usando buracos no passado. Foram localizados 13 horários livres nas sextas de
abril–junho (09:30–10:30) e 3 aulas excluídas pelo Núcleo Gestor (Front-End
11/04 07:10; IA 21/04 10:30; Mentorias 03/04 10:30).

**Execução:** Aulas **33 e 34** de Mobile antecipadas como **Reposição** para a
**Feira das Profissões**:
- 03/04/2026 09:30–10:30 (Aula 33)
- 10/04/2026 09:30–10:30 (Aula 34)

Planos em `aulas/registradas/plano_314114_5_2026-04-03_0930.txt` e
`plano_314114_5_2026-04-10_0930.txt`, com `TIPO_AULA: Reposição`.

**Resultado:** portal com 4 aulas de Mobile I-B aguardando confirmação
(03/04, 10/04, 13/07 14:30 e 13/07 15:50). O bot passou a aceitar
`TIPO_AULA` no plano (AP-041).

**Como validar:** iSeduc → Registro de aulas (`314114`) → Mobile → Visualizar
Aula: Tipo "Reposição" e conteúdo "Feira das Profissões — Aula 33/34
(antecipada como reposição)".

---

## IS-168 - Mobile (I-B): Aulas 3–12 registradas e 1/2 reservadas para 11/07 🟢

**Contexto:** as duas aulas de 13/07 (antigas Aulas 1/2) foram removidas do
portal. As **Aulas 1 e 2** ficam reservadas para o sábado **11/07** (coordenação
registra), e a sequência regular recomeça em **13/07** com as **Aulas 3–12**.

**Execução:** 10 planos registrados por `apps/bots/registrar_aulas.py --files`:
- 13/07: 14:30 (Aula 3) e 15:50 (Aula 4)
- 16/07: 07:10, 08:10, 09:30, 13:30 e 14:30 (Aulas 5–9)
- 17/07: 09:30 (Aula 10)
- 20/07: 14:30 e 15:50 (Aulas 11–12)

Frequência: todos presentes no plano; o bot marca **3 faltas** da blacklist
(Gustavo, Isadora e Janayra).

**Resultado:** portal com **12 aulas** de Mobile I-B aguardando confirmação
(2 de abril + 10 de julho). Os dois planos de 11/07 seguem em
`aulas/pendentes/` com o aviso `RESERVADO PARA A COORDENACAO REGISTRAR`.

**Como validar:** iSeduc → Registro de aulas (`314114`) → Mobile: 12 aulas
aguardando confirmação; as de 20/07 aparecem na segunda página.

---

## IS-169 - Arquitetura de Microsserviços: Aulas 01–08 geradas 🟢

**Contexto:** o portal iSeduc está instável; as 8 primeiras aulas foram geradas
localmente a partir dos PDFs SeducTec (material da I-A, aulas 1–8).

**Conteúdo:** em
`data/Turmas/2ª SÉRIE - Turma I-B (Técnico DS)/ARQUITETURA DE MICROSSERVIÇOS/S01/`:
- 01 Introdução aos Testes de Software
- 02 Garantia da Qualidade (QA) e Controle da Qualidade (QC)
- 03 Princípios Fundamentais dos Testes
- 04 Ciclo de Vida de Teste de Software
- 05 Categorias e Tipos de Testes
- 06 Níveis de Teste: unitário, integração, sistema e aceitação
- 07 Teste de Caixa Branca
- 08 Domain-Driven Design (DDD) e a transição para microsserviços

Cada aula tem objetivos, conteúdo, atividade e quiz 4x4 (parser validado:
4 questões e 4 alternativas). Links em `links_aulas.md`; índice em `README.md`.

**Pendência:** gerar os planos TXT e registrar no iSeduc quando o portal
normalizar; o conteúdo ainda não foi gravado no Supabase nem no portal.

**Como validar:** abrir `README.md`/`Aula_01.md`...`Aula_08.md` e rodar o
parser de quiz.

---

## IS-173 - Gerador de aulas: "Pasta não encontrada" em Microsserviços (Turma I-A) 🟢

**Sintoma:** no Gerador de Planos de Aula, a Rota 2 exibia
`Pasta não encontrada: ...\2ª SÉRIE - Turma I-A (Técnico DS)\ARQUITETURA DE MICROSSERVIÇOS\S01`
e o rodapé mostrava o mesmo erro, apesar de a pasta existir.

**Causa:** a pasta física da Turma I-A estava gravada como
`ARQUITETURA DE MICROSSERIÇOS` (sem o "V"), enquanto o Supabase
(`subjects.name`) e a pasta da Turma I-B usam `ARQUITETURA DE MICROSSERVIÇOS`.
A busca resiliente de `services/contexto_aulas.py` só cobria igualdade/substring
do nome normalizado; sem correspondência, voltava ao nome do banco e a Rota 2
falhava.

**Correção:** pasta renomeada para `ARQUITETURA DE MICROSSERVIÇOS` em
`data/Turmas/2ª SÉRIE - Turma I-A (Técnico DS)/`. Em
`services/contexto_aulas.py`, `resolver_pasta_turma` e
`resolver_pasta_disciplina` ganharam fallback por similaridade
(`difflib.SequenceMatcher`, limiar 0.9) para tolerar erros de digitação futuros.

**Arquivos:** `data/Turmas/2ª SÉRIE - Turma I-A (Técnico DS)/ARQUITETURA DE MICROSSERVIÇOS/`
(renomeada) e `services/contexto_aulas.py`.

**Como validar:** no Gerador de Aulas, selecionar a Turma I-A + Arquitetura de
Microsserviços e clicar em "Listar Arquivos Disponíveis" — deve listar os
arquivos do `S01` sem o aviso de pasta não encontrada.

---

## IS-174 - Monitor: preferência de servidor pelo PC01 do laboratório 🟢

**Pedido:** o PC01 do laboratório deve ter preferência quando o notebook e o PC
fixo estão online ao mesmo tempo.

**Solução:**
- `lab_receiver.py`: novo `SYSAVA_PREFERRED_SERVERS` (padrão `PC01*`) e
  `is_preferred_server()`. `current_role()` agora coloca o hostname preferido
  como **primário** mesmo que o notebook tenha subido antes; sem o PC01, vale
  quem iniciou primeiro. `/health` publica `hostname`/`preferred` e
  `/api/peer/state` acrescenta `preferred`.
- A descoberta UDP (`SYSAVA_SERVER ip:port`) não mudou: cada cliente consulta
  o `/health` de cada respondedor e escolhe o `preferred`/hostname `PC01*`.
- `lab_agent.py`/`lab_agent.ps1` (**build 18**): cache só é usado na hora se for
  o PC01; caso contrário, guarda o notebook como reserva, consulta o UDP e
  escolhe o servidor preferido (`preferred`/hostname).
- `sysava_lock.ps1`, `sysava_tray.ps1`, `tray_aluno.ps1` e `tray_servidor.ps1`:
  escolhem primeiro o `/health` com `preferred`/hostname `PC01*`; sem ele, usam
  o servidor que já estava configurado/cache. A bandeja do servidor abre o
  peer preferido no item do 2º servidor.

**Arquivos:** `data/repo/plugins/monitor/lab_receiver.py`,
`data/repo/plugins/monitor/lab_agent.py`,
`data/repo/plugins/monitor/lab_agent.ps1`,
`data/repo/plugins/monitor/sysava_lock.ps1`,
`data/repo/plugins/monitor/tray_aluno.ps1`,
`data/repo/plugins/monitor/tray_servidor.ps1`, `sysava_tray.ps1`,
`data/repo/plugins/monitor/config.env.example`,
`plugins/monitor_rede/README.md`, `data/repo/plugins/monitor/lab_monitor_doc.md`,
`AGENTS.md`.

**Como validar:**
1. Reiniciar o receiver do notebook e o do PC01 (`reiniciar_servidor.bat`).
2. `http://<pc01>:5000/health` e `http://<notebook>:5000/health`: o PC01 deve
   responder `"role": "primary"` e `"preferred": true`; o notebook,
   `"role": "assistant"`.
3. Em um PC de aluno, apagar `C:\Local\SysVa_lab\server_cache.txt` e reiniciar
   o agente: o log deve registrar o servidor preferido via UDP/cache.
4. Na tela de bloqueio/bandejas, o painel/RA deve abrir no PC01 enquanto ele
   estiver online; desligar o PC01 e repetir para o notebook assumir.
5. Para customizar: `SYSAVA_PREFERRED_SERVERS=PC01*,PC02*` no `.env`/ambiente
   dos dois receivers.

---

## IS-175 - Arquitetura de Microsserviços: PDFs do S01 tratam de testes de software 🟢

**Sintoma:** a disciplina **Arquitetura de Microsserviços** (2ª série, Turmas
I-A e I-B) exibia aulas sobre *testes de software* (fundamentos, QA/QC,
princípios, ciclo de vida, tipos, níveis, caixa branca e DDD), sem relação com a
ementa oficial. Os PDFs em `S01/seductec/` (`texto_aprofundamento_aula_1..8.pdf`)
são de outra disciplina e foram usados como base das `Aula_01..08.md` antigas.

**Correção:** geradas 8 aulas novas alinhadas aos itens 1–8 da ementa, em
formato completo com emojis (objetivos, introdução, conteúdo teórico com
tabelas, glossário, atividade prática e **quiz 4x4** com `[x]`/`[ ]`):
- Aula 01 — Conceitos Fundamentais de Microsserviços
- Aula 02 — Arquitetura Monolítica vs. Microsserviços
- Aula 03 — Design de Microsserviços: Módulos, Serviços Independentes e APIs
- Aula 04 — Comunicação entre Microsserviços: REST, gRPC e Eventos
- Aula 05 — Implementação e Gerenciamento de Microsserviços
- Aula 06 — Escalabilidade e Redundância com Microsserviços
- Aula 07 — Monitoramento e Testes de Microsserviços
- Aula 08 — Desafios e Vantagens da Arquitetura de Microsserviços

Arquivos criados em `S01` das duas turmas, **sem apagar** as aulas antigas.

**Arquivos:** `data/Turmas/2ª SÉRIE - Turma I-A (Técnico DS)/ARQUITETURA DE MICROSSERVIÇOS/S01/Aula 01..08*.md`
e o equivalente em `Turma I-B`.

**Como validar:**
1. Conferir que os novos `.md` estão em `S01` de cada turma.
2. Importar/replicar as aulas no Gerador de Aulas e verificar 4 perguntas com 4
   alternativas e gabarito correto em cada quiz.
3. Os PDFs antigos do `seductec` continuam errados para a ementa: devem ser
   substituídos pelo material oficial da disciplina quando disponível.

---

## IS-176 - Monitor: campo "Texto e Comando" na aba Ferramentas 🟢

**Pedido:** ter na aba Ferramentas um campo para enviar textos (alertas) e
comandos aos PCs selecionados, sem precisar ir até a aba Controle.

**Solução:**
- Painel web (`lab_receiver.py`): nova sub-aba **Ferramentas → 💬 Texto e
  Comando**, com:
  - **Texto / mensagem** (textarea) e botão **💬 Enviar texto**, que dispara
    `Enviar Alerta Visual` com o texto digitado.
  - **Comando** (input com `datalist` das ações do Controle) e botão
    **🚀 Executar comando**, que enfileira o comando digitado; se houver texto,
    também envia o alerta antes (o texto acompanha o comando quando ele é um
    alerta).
  - Usa a mesma seleção de PCs e a opção **Aplicar em todas** do topo da aba.
  - Nova rota `POST /ferramenta_texto_comando` (login obrigatório) e helper
    `_maquinas_do_form()`.
- Plugin Streamlit (`plugins/monitor_rede/lab_monitor.py`): seção **💬 Texto e
  comando** no início da aba Ferramentas, com multiselect de PCs, texto,
  comando, **Enviar texto** e **Executar comando**, gravando no histórico do
  professor.

**Arquivos:** `data/repo/plugins/monitor/lab_receiver.py`,
`plugins/monitor_rede/lab_monitor.py`, `plugins/monitor_rede/README.md`,
`data/repo/plugins/monitor/lab_monitor_doc.md`, `docs/ISSUES_LOCAIS.md`.

**Como validar:**
1. Reiniciar o receiver (`reiniciar_servidor.bat`) e abrir o painel web.
2. Aba **Ferramentas → 💬 Texto e Comando**, marcar um PC, digitar um texto e
   clicar **Enviar texto** — deve aparecer o alerta no PC e o comando em
   **Último comando por PC**.
3. Digitar `Desligar PC (Shutdown)` no comando (com um texto opcional) e
   confirmar; o agente deve receber a ação e o histórico registrar o envio.
4. No plugin Streamlit, repetir pela seção **💬 Texto e comando** da aba
   Ferramentas.

---

## IS-177 - PC01: `ATUALIZAR_PC01.bat` usava IP antigo do notebook 🟢

**Sintoma:** o atalho de atualização do PC01 tentava baixar o `servidor.zip` de
um IP fixo antigo do notebook e falhava quando o DHCP mudava o endereço.

**Solução:**
- Removido o IP fixo do `ATUALIZAR_PC01.bat`.
- Novo `descobrir_servidor.ps1` (na pasta `monitor/`) encontra o servidor de
  origem sem IP fixo:
  1. `SYSAVA_UPDATE_SERVER`, se definida;
  2. caches `%LOCALAPPDATA%\SysAva\servidor_tray.txt`,
     `C:\Local\SysVa_lab\server_cache.txt` e `peers.txt`;
  3. broadcast UDP 5001 (`SYSAVA_DISCOVER`).
  Ele descarta o próprio PC (IPs/hostname locais), valida `/health` e devolve
  as URLs em uma linha (`-Inline`) para o `.bat`.
- O `.bat` usa a URL descoberta; se nada for encontrado, pede a URL ao usuário
  e aceita tanto `http://ip:5000` quanto apenas `ip:5000` (prefixa `http://`
  automaticamente, inclusive no argumento da linha de comando).
- `descobrir_servidor.ps1` entrou no `DOWNLOAD_WHITELIST` e no `servidor.zip`.

**Arquivos:** `data/repo/plugins/monitor/ATUALIZAR_PC01.bat`,
`data/repo/plugins/monitor/ATUALIZAR_PC01.txt`,
`data/repo/plugins/monitor/descobrir_servidor.ps1`,
`data/repo/plugins/monitor/lab_receiver.py`, `docs/ISSUES_LOCAIS.md`.

**Como validar:**
1. No PC01, rodar o `ATUALIZAR_PC01.bat` sem argumentos: ele deve mostrar
   `Servidor de origem: http://<ip-atual-do-notebook>:5000`.
2. Se a descoberta falhar, rodar informando a URL:
   `ATUALIZAR_PC01.bat http://<ip-atual>:5000`.
3. Conferir que o `servidor.zip` extraído contém `descobrir_servidor.ps1`.

---

## IS-178 - PC01: acesso ao 5000 pelo Tailscale/LAN 🟢

**Sintoma:** o receiver aparecia online no próprio PC, mas `http://<ip>:5000`
não respondia de outro computador (Tailscale). O `ATUALIZAR_PC01.bat` também
falhava ao informar apenas `ip:5000`.

**Diagnóstico feito no notebook:**
- Tailscale online e `tailscale ping` direto para o PC01.
- Porta 445 do PC01 acessível pelo Tailscale, mas porta 5000 sem resposta.
- Isso indica firewall/receiver no PC01, não a rede Tailscale em si.

**Solução:**
- `ATUALIZAR_PC01.bat` passou a aceitar `ip:5000` sem `http://`.
- Novo `CORRIGIR_ACESSO_PC01.bat` + `corrigir_acesso_pc01.ps1` (rodar como
  Administrador no PC01):
  - inicia o serviço Tailscale e muda a rede Tailscale para **Private**;
  - cria/atualiza regras de firewall **TCP 5000**, **TCP 8501** e **UDP 5001**
    para qualquer perfil;
  - confere o listener em `0.0.0.0:5000` e tenta reiniciar o receiver se estiver
    offline;
  - testa o próprio PC e o notebook e grava
    `%TEMP%\sysava_diagnostico_tailscale.txt`.
- Os dois arquivos entram no `servidor.zip` e no `DOWNLOAD_WHITELIST`.

**Arquivos:** `data/repo/plugins/monitor/CORRIGIR_ACESSO_PC01.bat`,
`data/repo/plugins/monitor/corrigir_acesso_pc01.ps1`,
`data/repo/plugins/monitor/ATUALIZAR_PC01.bat`,
`data/repo/plugins/monitor/lab_receiver.py`, `docs/ISSUES_LOCAIS.md`.

**Como validar:**
1. No PC01, execute `CORRIGIR_ACESSO_PC01.bat` como Administrador.
2. No relatório, confira: regras criadas, `0.0.0.0:5000` escutando e
   `Teste notebook` = OK.
3. De outro PC da tailnet: `curl.exe http://<ip-do-pc01>:5000/health`.

---

## IS-179 - PC01 autônomo quando o notebook está desligado 🟢

**Problema:** com o notebook desligado, as máquinas ficavam bloqueadas. O PC01
não assumia a validação do RA, e a tela caía no modo offline até bloquear.

**Causa provável:** o PC01 não tinha o receiver rodando no boot (tarefa
`SysAva Servidor` ausente/apontando para outra pasta), `.env` sem
`SUPABASE_URL/SUPABASE_KEY` e/ou `alunos_cache.json` ausente. Sem a lista em
cache, o `/api/auth_ra` dependia só do Supabase/notebook.

**Solução:**
- `_buscar_usuario()` e `_buscar_aluno_por_nome()` agora usam
  `alunos_cache.json` como fallback quando o Supabase está indisponível. Assim o
  PC01 valida RA/nome mesmo sem internet/notebook, desde que o cache exista.
- `/api/alunos` já usava o cache; agora ele também é distribuído.
- `SERVIDOR_ZIP_ITENS`/`DOWNLOAD_WHITELIST` passaram a incluir
  `alunos_cache.json`, `lab_users.json` e `acesso_coletivos.json`.
- `diagnostico_servidor.ps1` mostra a quantidade de alunos em `/api/alunos` e
  avisa quando `alunos_cache.json` está ausente.
- `ATUALIZAR_PC01.txt` ganhou a seção **“PC01 SEM O NOTEBOOK (autônomo)”**.

**Para o PC01 assumir sozinho (fazer uma vez, com o notebook ligado):**
1. `ATUALIZAR_PC01.bat` (baixa/extrai o `servidor.zip` novo).
2. `instalar_servidor_auto.bat` como Administrador (tarefa no boot + firewall).
3. `diagnostico_servidor.bat`: confirmar `/health OK`, tarefa, `.env` e
   `/api/alunos` com alunos.
4. Desligar o notebook e testar um RA em um PC de aluno.

**Arquivos:** `data/repo/plugins/monitor/lab_receiver.py`,
`data/repo/plugins/monitor/diagnostico_servidor.ps1`,
`data/repo/plugins/monitor/ATUALIZAR_PC01.txt`, `docs/ISSUES_LOCAIS.md`.

---

## IS-180 - Tela de bloqueio: mensagens maiores e status real do servidor 🟢

**Pedido:** aumentar as letras de mensagem na tela de bloqueio e parar de pedir
para "ligar o PC01" quando ele está ligado, mas o servidor está sem resposta.

**Solução (`sysava_lock.ps1`):**
- `$lblMsg` (mensagens/erros) passou de Segoe UI **11** para **14 Bold**, com
  quebra de linha em 472 px.
- `$lblServidor` (status) passou de **10** para **12 Bold**.
- O card cresceu de 320 para **360 px** para acomodar as mensagens maiores.
- Texto do status desconectado mudou para:
  **"Servidor sem resposta - verifique/reinicie o PC01"**.
- O monitor de status agora, quando o cache aponta para o notebook desligado,
  faz **descoberta UDP 5001** e mostra "Servidor conectado" se o PC01 responder
  (antes ele só olhava cache/localhost e podia exibir "ligue o PC01" mesmo com o
  PC01 servindo a rede).

**Arquivos:** `data/repo/plugins/monitor/sysava_lock.ps1`,
`docs/ISSUES_LOCAIS.md`.

**Como validar:** aplicar a tela nova nos PCs (Controle → Atualizar Tela de
Bloqueio) e conferir as letras maiores. Com o notebook desligado e o PC01
servindo, a linha deve mudar para **"Servidor conectado"** em ~6 s.

---

## IS-181 - Bandeja: não deixava iniciar o servidor do PC01 com o notebook online 🟢

**Sintoma:** depois de mexer no buscador de servidores da bandeja do notebook, o
servidor do PC01 não voltava a subir. A bandeja mostrava o notebook online e
desabilitava o item **Iniciar servidor**, mesmo com a porta 5000 do PC01 livre.

**Causa:** `sysava_tray.ps1` usava `$srvOn = servidor local OU remoto` para
habilitar/desabilitar o botão. Se qualquer servidor fosse encontrado na rede
(notebook), **Iniciar servidor** ficava desabilitado no PC01. O botão existe
para subir o servidor **deste PC**, então o remoto não deveria bloquear.

**Solução:**
- **Iniciar servidor neste PC** agora habilita quando a porta 5000 **local**
  está livre (`-not $srvLocalOn`), independente de haver outro servidor online.
- **Parar servidor deste PC** continua habilitado só quando o servidor local
  está rodando.
- O menu passa a diferenciar: **online NESTE PC** / **Servidor encontrado:
  <host> (este PC offline)** / **offline neste PC**.
- Com o PC01 iniciado, a preferência já existente (`PC01*`) faz ele assumir como
  primário, e o agente build 18/tela/bandejas o escolhem primeiro.

**Arquivos:** `sysava_tray.ps1`, `docs/ISSUES_LOCAIS.md`.

**Como validar:**
1. No PC01, abra a bandeja com o notebook ligado: o item **Iniciar servidor
   neste PC** deve estar habilitado.
2. Clique; confirme `http://127.0.0.1:5000/health` e o papel `primary`.
3. Desligue o notebook e valide um RA em um PC de aluno.

---

## IS-182 - Bandeja: encontrar o PC01 pelo Tailscale (fora da LAN) 🟢

**Pedido:** a bandeja do notebook deveria encontrar o servidor e abrir o painel
de controle dele mesmo estando em casa, para escolher/gerenciar o PC01.

**Solução (`sysava_tray.ps1`):**
- Novo `Get-TailscaleCandidatos`: lê `tailscale status --json` e adiciona os
  IPs `100.x` dos peers online como candidatos `http://<ip>:5000`.
- `Get-ServidorCandidatos`/`Find-Servidores`/`Find-ServidorUrl` e o monitor em
  segundo plano passaram a incluir esses candidatos. A verificação continua
  sendo `/health` (só entra na lista quem realmente está servindo).
- O menu mostra **online NESTE PC**, **Servidor encontrado: <host> (este PC
  offline)** ou **offline neste PC**, e **Iniciar servidor neste PC** funciona
  mesmo com outro servidor online (IS-181).

**Diagnóstico no momento:** o notebook estava em outra rede (`192.168.0.9`) e
o `tailscale status` mostrava o **PC01 offline**; por isso a bandeja não achava
nenhum servidor. Quando o PC01 voltar ao Tailscale, a busca o encontrará.

**Arquivos:** `sysava_tray.ps1`, `docs/ISSUES_LOCAIS.md`.

**Como validar:** no notebook (casa/4G), abrir a bandeja → **Buscar servidores
na rede** com o PC01 online; ele deve aparecer e **Abrir painel** deve carregar
`http://100.113.128.78:5000/`.

---

## IS-183 - Arquitetura de Microsserviços: aulas 09-10 de laboratório 🟢

**Pedido:** as aulas 01-08 são conceituais; criar as aulas 09 e 10 como
atividades práticas de laboratório, com instalação de ferramentas e um projeto
que exercite os assuntos das aulas 02 a 08, já que o calendário foi comprimido.

**Solução:** duas aulas práticas em torno do projeto **SysLoja** (FastAPI):
- **Aula 09:** instalação de Python/VS Code/Git, ambiente virtual, estrutura do
  projeto e primeiro microsserviço (**Catálogo**, porta 8001) com `/health`,
  `/produtos` e `/produtos/{id}`, testes no `/docs` e commit no Git.
- **Aula 10:** serviços de **Pagamentos** (8003) e **Pedidos** (8002) integrados
  por REST com `httpx`, timeout, tratamento de erro e idempotência simples;
  fluxo completo, health checks, resiliência (derrubar Pagamentos), escala com
  `--workers 2` e teste de fumaça (`teste_smoke.py`).

As aulas retomam os itens 2-8 da ementa na prática (monólito x serviços,
design/APIs, comunicação, implementação, escala/redundância, monitoramento e
testes, trade-offs). Cada uma mantém o **quiz 4x4**.

**Arquivos:** `data/Turmas/2ª SÉRIE - Turma I-A (Técnico DS)/ARQUITETURA DE MICROSSERVIÇOS/S01/Aula 09*.md`
e `Aula 10*.md`, com cópias em `Turma I-B`; `README.md` do S01 (I-B) atualizado.

**Como validar:**
1. Conferir as aulas 09 e 10 em `S01` das duas turmas.
2. Importar no Gerador de Aulas e verificar 4 perguntas × 4 alternativas.
3. Seguir o laboratório: Catálogo em 8001, Pagamentos em 8003 e Pedidos em 8002;
   criar um pedido deve resultar em pagamento aprovado.
4. Derrubar Pagamentos e confirmar que Pedidos devolve erro controlado.

---

## IS-184 - Arquitetura de Microsserviços: aulas 11-13 de laboratório 🟢

**Pedido:** após as aulas 09-10 (ambiente e integração do SysLoja), criar as
aulas 11, 12 e 13 dando continuidade prática aos itens de implementação,
gerenciamento, escala e entrega da ementa.

**Solução:** três laboratórios sequenciais:
- **Aula 11 — Containers com Docker:** imagem x container x registry, instalação
  do Docker Desktop, `requirements.txt` e `.dockerignore` por serviço,
  `Dockerfile` do Catálogo, `docker build`/`run`, boas práticas (slim, cache de
  camadas, HEALTHCHECK).
- **Aula 12 — Docker Compose:** variáveis `CATALOGO_URL`/`PAGAMENTOS_URL` no
  Pedidos, Dockerfiles de Pagamentos/Pedidos e `docker-compose.yml` com os três
  serviços, rede por nome, `depends_on`, healthchecks e troubleshooting.
- **Aula 13 — CI/CD com GitHub Actions:** testes com `pytest` + `TestClient`,
  workflow `.github/workflows/ci.yml` (jobs `testes` e `build`), cache de pip,
  GitHub Secrets e proteção de branch.

As três mantêm o padrão das demais (emojis, tabelas, atividade, entregável,
desafio e **quiz 4x4**). A linha `Turma` é genérica (“Turmas I-A e I-B”) para o
`upsert` por `subject_id,title` não sobrescrever o conteúdo entre turmas.

**Arquivos:** `data/Turmas/2ª SÉRIE - Turma I-A (Técnico DS)/ARQUITETURA DE MICROSSERVIÇOS/S01/Aula 11*.md`,
`Aula 12*.md` e `Aula 13*.md`, com cópias em `Turma I-B`.

**Como validar:**
1. Conferir as aulas 11-13 em `S01` das duas turmas.
2. Rodar o `seed_lessons.bat` (logs da disciplina foram limpos) e verificar que
   cada uma importou com 4 perguntas × 4 alternativas.
3. Aula 11: `docker build` e `docker run` do Catálogo em 8001.
4. Aula 12: `docker compose up --build` e criar um pedido em 8002.
5. Aula 13: `pytest -q` local e pipeline verde na aba Actions do GitHub.

---

## IS-185 - Arquitetura de Microsserviços: bloco 1 fechado e plano da disciplina 🟢

**Pedido:** fechar as 40h de forma balanceada: temas 1-4 até a AV1 (aula 20),
temas 5-8 nas aulas 21-32 com AV2 na 32, e seminário nas aulas 33-40 (AV3).
Registrar o combinado em `plano.txt` na pasta da disciplina.

**Solução:**
- **Aulas 14-19** reorganizadas para o bloco 1 (temas 1-4): DDD/decomposição,
  contratos de API, mensageria/eventos, REST x gRPC na prática, API Gateway/BFF
  e estudo de caso/revisão.
- **Aula 20** reescrita como **AV1** (temas 1-4): quiz 4x4 + parte prática com
  rubrica.
- Os rascunhos das aulas 17-19 anteriores (Resiliência, Observabilidade,
  Segurança/Custos) e a avaliação integradora foram movidos para
  `S01/_rascunhos_bloco2/` (I-A) para reaproveitamento no bloco 2.
- **`plano.txt`** criado em `ARQUITETURA DE MICROSSERVIÇOS/` das duas turmas,
  com o combinado, mapa de aulas 01-40, o que já está pronto e pendências.

**Arquivos:** `S01/Aula 14..20*.md` (I-A e I-B),
`S01/_rascunhos_bloco2/` (I-A),
`ARQUITETURA DE MICROSSERVIÇOS/plano.txt` (I-A e I-B) e este registro.

**Como validar:**
1. Conferir `plano.txt` e as aulas 14-20 em `S01` das duas turmas.
2. Rodar o parser do seed: 20 aulas por turma, cada uma com 4 perguntas × 4
   alternativas (AV1 inclusa).
3. Rodar `seed_lessons.bat` e conferir as 20 aulas no portal.
4. Aplicar a AV1 e seguir para o planejamento das aulas 21-32.

---

## IS-186 - Alerta do Monitor com texto copiável 🟢

**Pedido:** o texto enviado por **Ferramentas → Texto e Comando** precisava ser
copiável no PC que recebe o alerta; o MessageBox do Windows não permite
selecionar o texto.

**Solução (`lab_agent.py` + `lab_agent.ps1`, build 19):**
- Novo `mostrar_alerta()`: janela própria, sempre no topo, com o texto em caixa
  somente leitura (selecionável), botão **Copiar texto** e **Fechar**.
- Ao abrir, o texto já é colocado na área de transferência (Ctrl+V funciona).
- Roda em thread separada, sem travar o loop do agente.
- Fallback para `MessageBoxW` se o Tkinter não estiver disponível.
- O histórico do painel registra `ok: alerta exibido (texto copiavel)`.
- `AGENT_BUILD` passou para **19**; o `lab_agent.ps1` foi sincronizado.
- No painel web, **Ferramentas → Texto e Comando** ganhou o botão
  **📋 Copiar texto** (Clipboard API com fallback `execCommand`).

**Arquivos:** `data/repo/plugins/monitor/lab_agent.py`,
`data/repo/plugins/monitor/lab_agent.ps1`, `AGENTS.md`,
`docs/ISSUES_LOCAIS.md`.

**Como aplicar:** no painel do PC01, **Controle → Atualizar Monitor (rápido,
sem UAC)** nos PCs; envie um texto de teste e use **Copiar texto** ou Ctrl+V.

---

## IS-187 - Monitor: instruções via HTTP e alerta com texto selecionável 🟢

**Contexto:** o alerta ainda aparecia como janela do Python (agente antigo) e
não era possível copiar; além disso, as instruções eram difíceis de transportar
para o PC01.

**Solução:**
- `mostrar_alerta()` (build 20) agora abre uma janela Tk **640x380**, centralizada,
  com a fonte maior, o texto **editável/selecionável** (Ctrl+C funciona) e o
  botão **Copiar texto** copiando o conteúdo atual da caixa. O texto continua
  indo automaticamente para a área de transferência.
- Nova rota **`/instrucoes`** no receiver: página HTML com os passos e botões
  **Copiar** para: atualizar o agente build 20, reiniciar/conferir o servidor,
  preparar o PC01 sozinho, Tailscale e parar/religar. Sem senhas.
- Link **📋 Instruções para copiar** em **Ferramentas → Texto e Comando**.

**Importante:** se o alerta ainda abre como “janela do Python” sem copiar, o
agente do PC ainda é o **build 18**; rode **Controle → Atualizar Monitor
(rápido, sem UAC)** e confirme o badge **build 20**.

**Arquivos:** `data/repo/plugins/monitor/lab_receiver.py`,
`data/repo/plugins/monitor/lab_agent.py`,
`data/repo/plugins/monitor/lab_agent.ps1`, `docs/ISSUES_LOCAIS.md`.

**Como validar:**
1. Abrir `http://127.0.0.1:5000/instrucoes` e usar os botões Copiar.
2. Atualizar um PC para build 20 e enviar um texto.
3. Na janela do alerta, selecionar o texto ou clicar em **Copiar texto**.

---

## IS-193 — Bandeja do aluno: sair da conta, reabrir a tela de bloqueio e liberar o RA 🟢

**Pedido:** a bandeja do aluno (`tray_aluno.ps1`) tinha poucos recursos. Era
preciso conseguir **sair da conta** e **abrir a tela de bloqueio novamente**
sem esperar o próximo logon.

**Solução:**
- Novos itens no menu: **Atualizar meus dados agora**, **Abrir SysAva com meu
  RA**, **Abrir tela de bloqueio**, **Sair da conta (voltar a tela de bloqueio)**
  e **Sair do Windows (logoff)**. O antigo **Sair** virou **Fechar bandeja
  (continuar logado)** para não confundir com o logout.
- O menu mostra também o estado da tela (**bloqueada**, **liberada pelo
  professor até HH:mm** ou **sem bloqueio**).
- **Sair da conta:** confirma, remove `%LOCALAPPDATA%\SysAva\tela_ok.json`,
  `ultimo_ra.txt` e `meu_email.txt`, chama `POST /api/logout_ra` e reabre o
  `sysava_lock.ps1` na hora. A conta do Windows continua logada (para deslogar
  de verdade use **Sair do Windows**).
- **Receiver:** nova rota `POST /api/logout_ra` remove a associação da máquina
  em `lab_users.json` (respeitando o RA informado, para não apagar um login
  novo) e propaga aos peers por `POST /api/peer/logout`. Assim o RA fica livre
  para outro PC imediatamente, sem esperar `OFFLINE_SECONDS`.
- **Servidor fora:** o logout fica em `logout_pendente.json` e é sincronizado
  quando o servidor voltar; enquanto isso a bandeja não repõe o aluno antigo.
- Se a tela estiver liberada pelo professor (`tela_liberada.json`), a bandeja
  avisa que o bloqueio volta no próximo logon em vez de forçar a tela.

**Importante:** reinicie o receiver do servidor (PC01/notebook) para a rota
`/api/logout_ra` entrar em vigor. Até lá a bandeja guarda o pedido em
`logout_pendente.json` e conclui sozinha quando o servidor atualizado responder.

**Arquivos:** `data/repo/plugins/monitor/tray_aluno.ps1`,
`data/repo/plugins/monitor/lab_receiver.py`, `AGENTS.md`,
`plugins/monitor_rede/README.md`, `docs/ISSUES_LOCAIS.md`.

**Como validar:**
1. Reiniciar a bandeja do aluno (`tray_aluno.bat`) e conferir os novos itens.
2. Clicar em **Sair da conta**, confirmar e ver a tela de bloqueio reabrir.
3. Conferir que `lab_users.json` não tem mais a máquina associada e que o mesmo
   RA consegue entrar em outro PC na hora.
4. Com o servidor desligado, sair da conta e religar o servidor: o
   `logout_pendente.json` deve ser enviado e removido sozinho.
5. Testar **Abrir tela de bloqueio** e **Sair do Windows (logoff)**.

---

## IS-194 — Monitor: Atualizar Bandeja do Aluno reinicia a instância antiga 🟢

**Problema:** o comando **Controle → Atualizar Bandeja do Aluno** baixava os
arquivos novos para `%LOCALAPPDATA%\SysAva`, mas a bandeja antiga continuava
rodando (o mutex `SysAvaTrayAluno` fazia a instância nova sair na hora). Na
prática a atualização só valia depois de logoff/reboot.

**Solução:** `_instalar_bandeja_aluno()` agora chama `_encerrar_bandeja_aluno()`
antes de abrir a nova cópia. Ela encerra somente `powershell.exe`/`wscript.exe`
cuja linha de comando aponta para `tray_aluno.ps1`/`tray_aluno.vbs` dentro do
`%LOCALAPPDATA%\SysAva` do usuário atual, espera 1 s e inicia pelo `.vbs`. O
resultado do comando informa quantas instâncias antigas foram fechadas.

**Arquivos:** `data/repo/plugins/monitor/lab_agent.py`, `AGENTS.md`,
`plugins/monitor_rede/README.md`, `docs/ISSUES_LOCAIS.md`.

**Como validar:**
1. **Controle → Atualizar Monitor (rápido, sem UAC)** e confirmar build 20.
2. **Controle → Atualizar Bandeja do Aluno** nos PCs marcados.
3. Conferir no histórico do painel o resultado
   `ok: bandeja do aluno instalada (... instancia(s) antiga(s) fechada(s))`.
4. Abrir o menu da bandeja e ver os itens novos (Sair da conta etc.).

---

## IS-195 — Gestão de Usuários: adicionar, desativar acesso e remover contas 🟢

**Pedido:** uma aba de gestão de usuários para o professor adicionar,
desativar e remover contas.

**Problema encontrado:** a aba antiga (Admin → Usuários) usava `is_active`
para "desativar", mas esse campo passou a significar **Falta** na frequência
(IS-040). O login nem consultava `is_active`, então a conta continuava entrando
no portal.

**Solução:**
- Nova página **Gestão de Usuários** no menu lateral (admin e professor).
- Abas **Contas cadastradas** (busca, filtros, tabela) e **Adicionar conta**
  (nome, login, RA, senha, função e turma opcional).
- **Desativar/Reativar acesso** grava `app_users.status = 'blocked'` /
  `'active'`; não mexe em `is_active`/`is_portal`, preservando a frequência.
- **Remover conta** apaga o cadastro e a matrícula (com confirmação por
  checkbox); o histórico já registrado permanece.
- **Redefinir senha** grava novo hash bcrypt.
- Segurança: professor só gerencia alunos; ninguém desativa/remove a própria
  conta; o último administrador ativo não pode ser desativado/removido.
  Sessões ativas do usuário desativado são encerradas.
- Login (`views/login.py`) e restauração de sessão (`app.py`) passaram a
  recusar `status='blocked'`. `get_user()`/`get_all_users()` agora leem
  `status` com fallback para bancos antigos.
- `set_frequency_flag()` preserva `status='blocked'` ao alterar Falta/Inativo.
- Admin → Usuários ganhou um aviso indicando que a gestão de acesso fica na
  nova aba e que os botões de lá são de frequência.

**Arquivos:** `views/usuarios.py` (novo), `views/login.py`, `app.py`,
`services/database.py`, `services/auth.py`, `views/admin.py`,
`docs/FEATURES.md`, `docs/ISSUES_LOCAIS.md`.

**Como validar:**
1. Entrar como professor/admin e abrir **Gestão de Usuários** no menu.
2. Criar uma conta de aluno com turma; confirmar que ela aparece na tabela.
3. **Desativar acesso** e tentar logar com ela: deve mostrar "Conta desativada".
4. **Reativar acesso** e logar novamente: deve entrar.
5. **Remover conta** e confirmar que o RA fica livre para um novo cadastro.
6. Como professor, confirmar que só aparecem/ são gerenciáveis contas de aluno.

---

## IS-196 — Painel do monitor: aba Usuários (criar, desativar, remover) 🟢

**Pedido:** a gestão de usuários também no painel web do monitor (porta 5000),
para o professor não precisar abrir o portal.

**Solução (`lab_receiver.py`):**
- Nova aba **Usuários** ao lado de Monitor/Controle/Ferramentas.
- **Adicionar conta** (nome, login, RA, função e senha) com hash bcrypt; professor
  cria apenas aluno, administrador cria qualquer função.
- **Desativar/Reativar acesso** e **Remover** por linha, com confirmação.
- Usa `app_users.status='blocked'` (mesma regra do portal), sem alterar
  `is_active`/`is_portal`; lista com cache de 30 s para reduzir egress.
- Proteções: não desativa/remove a própria conta; último administrador ativo não
  pode ser desativado; último administrador não pode ser removido; professor só
  gerencia alunos.
- O login do painel (`_validar_professor`) também recusa contas bloqueadas.
- Novas rotas: `POST /usuarios_criar`, `POST /usuarios_bloquear`,
  `POST /usuarios_reativar` e `POST /usuarios_remover`; helpers
  `_rest_update`/`_rest_delete`.
- Filtro de busca na tabela (JavaScript) e Enter nos campos de cadastro envia para
  `/usuarios_criar`.

**Arquivos:** `data/repo/plugins/monitor/lab_receiver.py`, `AGENTS.md`,
`plugins/monitor_rede/README.md`, `docs/FEATURES.md`, `docs/ISSUES_LOCAIS.md`.

**Como validar:**
1. Reiniciar o receiver (`reiniciar_servidor.bat`) e abrir `http://127.0.0.1:5000`.
2. Entrar como professor/admin e abrir a aba **Usuários**.
3. Criar uma conta de aluno; usar o filtro para encontrá-la.
4. **Desativar** e tentar logar no portal (deve recusar); **Reativar** e logar.
5. **Remover** e confirmar que o RA fica livre.
6. Como professor, confirmar que só aparecem contas de aluno e que a opção
   Professor/Administrador não aparece no cadastro.

---

## IS-197 — Tela de bloqueio: professora Adriana liberada no PC01 🟢

**Pedido:** permitir que a professora **adriana** (`role=teacher`,
RA `[RA]`) desbloqueie a tela do **PC01**.

**Solução:**
- `acesso_coletivos.json` ganhou a chave `professores` (`["adriana"]`).
- `/api/auth_ra` aceita professor/admin da lista por **login, RA ou nome**
  (`adriana`, `Adriana`, RA ou nome completo), associa ao PC e devolve
  `role=teacher`. Professores não entram na regra de RA único.
- O acesso de professor é permitido **somente em PCs mestres** (`PC01*` via
  `SYSAVA_MASTER_HOSTS`/`master_hosts.txt`); em outros PCs o endpoint responde
  **400** e a tela continua exigindo aluno da lista ou senha admin.
- `/api/alunos?maquina=...` inclui os professores liberados no seletor **somente
  no PC mestre**; o `sysava_lock.ps1` passou a enviar `maquina` na consulta.
- Contas bloqueadas (`status='blocked'`) não liberam a tela.
- O login do painel web já recusa contas bloqueadas (IS-196).

**Arquivos:** `data/repo/plugins/monitor/acesso_coletivos.json`,
`data/repo/plugins/monitor/lab_receiver.py`,
`data/repo/plugins/monitor/sysava_lock.ps1`, `AGENTS.md`,
`plugins/monitor_rede/README.md`, `docs/ISSUES_LOCAIS.md`.

**Como validar:**
1. Reiniciar o receiver no PC01 (ele lê `acesso_coletivos.json`).
2. Na tela de bloqueio do PC01, digitar `adriana`, `Adriana`, o RA
   `[RA]` ou o nome completo; a tela deve liberar e abrir o portal.
3. Em um PC que não seja `PC01*`, tentar o mesmo nome: deve recusar.
4. Atualizar a tela (`Atualizar Tela de Bloqueio`) para Adriana aparecer também
   no seletor do PC01.
5. Se a conta for desativada em **Usuários**, a tela deixa de liberar.

---

## IS-198 - Aulas: status não ficava verde por quizzes duplicados 🟢

**Sintoma:** na disciplina **Arquitetura de Microsserviços**, o aluno acessava a
aula, respondia ao quiz e o indicador continuava **amarelo** ("Visitada, quiz
pendente"), sem virar verde.

**Causa:** o `seed_lessons.py` criava um quiz novo a cada importação, sem remover
os anteriores. As aulas 01–20 ficaram com **dois quizzes** (ex.: lesson 1058 com
852 e 862). A tela de status montava `quiz_map = {lesson_id: último quiz}` (862),
mas `get_quiz_for_lesson` exibe o **primeiro** (852) e o histórico gravava
`quiz_id:852`. O id não batia e o status ficava amarelo.

**Correção:**
- `views/aulas.py`: status passa a considerar **todos** os quizzes da aula
  (`quizzes_by_lesson`) e também registra o **título** do quiz do histórico
  (mesmo quando há `quiz_id`), além de filtrar o histórico pelo `subject_id`.
- `scripts/seed_lessons.py`: chama `delete_quizzes_for_lesson(lesson_id)` antes
  de criar o quiz, evitando novas duplicatas.
- Limpeza no banco: mantido **um quiz por aula** (o de menor id, que é o exibido)
  e removidos os duplicados sem respostas no histórico (50 quizzes no total,
  incluindo 20 desta disciplina).

**Arquivos:** `views/aulas.py`, `scripts/seed_lessons.py` e este registro.

**Como validar:**
1. Abrir a disciplina, acessar uma aula e responder ao quiz.
2. Voltar à lista: o círculo deve ficar **verde**.
3. Aula apenas visitada, sem quiz respondido: permanece **amarela**.
4. Conferir em `quizzes` que cada aula tem apenas um quiz ativo.
