---
title: DocumentaÃ§Ã£o do Plugin de Monitoramento de LaboratÃ³rio (lab_monitor.py)
description: Guia sobre o radar de atividade, estatÃ­sticas de uso e painel de controle remoto para o laboratÃ³rio de informÃ¡tica.
---

# ðŸ–¥ï¸ Plugin de Monitoramento de LaboratÃ³rio (`lab_monitor.py`)

Este plugin permite que o professor tenha uma visÃ£o em tempo real do que estÃ¡ acontecendo em cada computador do laboratÃ³rio, facilitando a gestÃ£o da sala de aula e garantindo que o foco permaneÃ§a nas atividades pedagÃ³gicas.

## ðŸš€ VisÃ£o Geral

O `lab_monitor.py` atua como um "radar" que categoriza automaticamente a atividade dos alunos em: **Produtivo**, **Roblox**, **Games**, **Redes Sociais** ou **Celular (Proibido)**. Ele utiliza o mapeamento de IP para identificar qual aluno estÃ¡ em qual mÃ¡quina e permite o monitoramento manual de alunos que nÃ£o estÃ£o usando os PCs do laboratÃ³rio.

## âœ¨ Principais Funcionalidades

A tela **Plugins â†’ Monitor** Ã© organizada em **abas** (antes as aÃ§Ãµes ficavam
todas no mesmo `selectbox`):

| Aba | ConteÃºdo |
| --- | --- |
| ðŸ“Š Radar | mÃ©tricas, distribuiÃ§Ã£o, tabela ao vivo, rÃ³tulos e alunos externos |
| ðŸ•¹ï¸ Controle | seleÃ§Ã£o de PCs + aÃ§Ã£o de intervenÃ§Ã£o |
| ðŸ§° Ferramentas | estrutura de pastas de atividades, texto/comando, Kit Lab DS e pacote de atualizaÃ§Ã£o |
| âš¡ AÃ§Ãµes em Massa | comandos para todo o laboratÃ³rio |
| ðŸ“œ HistÃ³rico | entradas, aÃ§Ãµes do professor e infraÃ§Ãµes do dia |
| ðŸ” DiagnÃ³stico | uptime e varredura de rede do receiver |

### 1. Dashboard de EstatÃ­sticas (Radar)
- **MÃ©tricas Globais**: Exibe o total de mÃ¡quinas online e a contagem especÃ­fica de alunos no Roblox, em Redes Sociais/Games e em atividades produtivas.
- **Contador de InfraÃ§Ãµes**: Soma em tempo real alunos detectados em jogos ou usando o celular indevidamente.
- **GrÃ¡fico de DistribuiÃ§Ã£o**: Um grÃ¡fico de barras que resume visualmente o comportamento atual do laboratÃ³rio.

### 2. Monitoramento ao Vivo (Tabela de Calor)
- **CategorizaÃ§Ã£o Visual**: A tabela de monitoramento utiliza cores para facilitar a identificaÃ§Ã£o rÃ¡pida:
    - ðŸ”´ **Vermelho**: Roblox detectado.
    - ðŸŸ  **Laranja**: Sites de Games ou entretenimento.
    - ðŸ”µ **Azul**: Redes Sociais (Instagram, YouTube, etc).
    - ðŸŸ£ **Roxo**: Uso de celular flagrado/registrado.
    - ðŸŸ¢ **Verde**: Atividade Produtiva (VS Code, Google Docs, etc).
- **IdentificaÃ§Ã£o por IP**: Mostra o IP do dispositivo, permitindo cruzar dados com o histÃ³rico de login do aluno no SysAva.
- **RÃ³tulos**: o expander **ðŸ·ï¸ RÃ³tulos das mÃ¡quinas** (no Streamlit) ou a pÃ¡gina **ðŸ·ï¸ RÃ³tulos** do painel web permitem dar um nome amigÃ¡vel a cada PC (ex.: `PC02-LAB01`), salvo em `lab_labels.json`. O rÃ³tulo vira a 1Âª coluna da tabela e aparece tambÃ©m nas listas de seleÃ§Ã£o/target (o hostname continua visÃ­vel como â€œMÃ¡quina (host)â€). RÃ³tulos de PCs offline permanecem editÃ¡veis.
- **Aluno (RA)**: coluna com o nome completo + RA associado ao PC pela tela de bloqueio (`lab_users.json`). Se o aluno ainda nÃ£o passou pelo lock, mostra **â€œsem RAâ€**. A conta Windows (`ALUNO`/`SYSTEM`) aparece apenas como informaÃ§Ã£o secundÃ¡ria (â€œconta: â€¦â€), nunca como aluno. A associaÃ§Ã£o vale por **16 h** (`USER_MAP_TTL_SECONDS`) para nÃ£o exibir o aluno anterior. Cada RA comum sÃ³ pode estar **logado em um PC por vez** (ver â€œRegras de acessoâ€); contas **coletivas** (`7anoA`, `8ano`, `1alunoEja`...) sÃ£o a exceÃ§Ã£o.

### 3. Central de IntervenÃ§Ã£o (Comandos Remotos)
Permite selecionar uma ou mais mÃ¡quinas (**ou marcar "Selecionar TODAS as
mÃ¡quinas"**) e **marcar vÃ¡rias aÃ§Ãµes ao mesmo tempo**. No painel web as aÃ§Ãµes
ficam em chips agrupados (Avisos, Jogos/sites, Limpeza, Tela/Ã¡udio, Sistema),
com presets de 1 clique (**Anti-jogo**, **Aula focada**, **Liberar aula**,
**Faxina**, **Fim da aula**), **marcar todas** e contador. No Streamlit use o
`st.multiselect` "AÃ§Ãµes de Controle" + os mesmos presets. O receiver enfileira
em `pending_queue` e entrega **uma aÃ§Ã£o por ping** (~10 s) na ordem marcada:
- **Enviar Alerta Visual**: Exibe uma mensagem na tela do aluno (ex: "Foco na atividade!"). No agente **build 20+** o alerta abre em uma janela com texto selecionável, botão **Copiar texto** e já deixa o conteúdo na área de transferência.
- **Definir Volume em 30% / Restaurar Volume (100%)**: ajusta o volume master do Windows na sessÃ£o do aluno via Core Audio (`definir_volume.ps1`), sem UAC e desmutando o dispositivo padrÃ£o.
- **Fechar / Bloquear / Desbloquear Sites/Jogos**: para **YouTube, Roblox, Loki, outros games e redes sociais**. **Fechar** encerra agora; **Bloquear** mantÃ©m o watchdog fechando janelas e derrubando processos de jogos atÃ© **Desbloquear**. O estado fica em `block_state.json` no PC e sobrevive a reboot.
- **Bloquear Jogos**: Encerra os executÃ¡veis de jogos instalados (Roblox, Fortnite/Epic, League of Legends) e fecha janelas do navegador que estejam exibindo sites/proxies de jogos (**Loki**, Poki, Friv, Y8, ClickJogos, Gartic...). O watchdog fecha esses jogos/janelas quando o bloqueio persistente (**Bloquear Sites/Jogos**) está ativo; **Desbloquear** libera Roblox/Fortnite/League; o comando manual **Bloquear Jogos** fecha uma vez.
- **Limpar InicializaÃ§Ã£o do Opera**: remove o Opera do **auto-start** (Run/RunOnce, pasta Startup e tarefas de inicializaÃ§Ã£o), sem fechar o Opera que o aluno abriu manualmente. O agente tambÃ©m aplica isso ao iniciar.
- **Limpar InicializaÃ§Ã£o de Apps Microsoft**: remove do auto-start **Outlook, OneDrive, Teams, OneNote, Skype, Copilot, Office Hub, Xbox/Game Bar, Widgets** e entradas equivalentes (Edge/Phone Link). NÃ£o fecha os apps em uso; sÃ³ evita que subam sozinhos no prÃ³ximo logon.
- **Bloquear Sites**: Fecha **apenas** as janelas de **YouTube, Instagram, TikTok, Facebook, X/Twitter** (e sites de jogos), sem matar o navegador inteiro.
- **Bloquear Navegador**: Encerra todos os navegadores abertos na mÃ¡quina.
- **Registrar Uso Indevido de Celular**: Altera o status do aluno para "Roxo" no radar e grava uma infraÃ§Ã£o permanente no histÃ³rico do aluno (RA).
- **ForÃ§ar Logoff / Desligar / Reiniciar**: AÃ§Ãµes de energia (`shutdown /l|/s|/r`).
  Comandos pendentes tÃªm **validade de 30 min** (`COMMAND_TTL_SECONDS=1800` no
  `.env`): se o PC estava desligado, o Desligar/Reiniciar nÃ£o Ã© executado horas
  depois, quando o aluno liga a mÃ¡quina. Os comandos sÃ£o gravados no
  `lab_status.json` sob um **Ãºnico lock** (leitura + gravaÃ§Ã£o), entÃ£o um `/ping`
  concorrente nÃ£o apaga o comando recÃ©m-enfileirado â€” se o painel mostra
  â€œsolicitado a N mÃ¡quina(s)â€, o comando foi realmente gravado.
- **Instalar Kit Lab DS**: instala o kit de desenvolvimento via winget (aba **Ferramentas**).
- **Abrir Prova Motriz**: abre https://prova-motriz.jovensgenios.com/entrar no navegador dos PCs selecionados (ou de todos, na Ferramentas/painel web). Requer agente build 7.

- **Atualizar Monitor (rÃ¡pido, sem UAC)**: baixa sÃ³ o `lab_agent.py` do servidor,
  valida, substitui o arquivo na pasta do agente e reinicia o processo. **NÃ£o**
  pede senha de Administrador e nÃ£o mexe em dependÃªncias/autostart.
- **Reinstalar Monitor (com UAC)**: baixa o `lab_agent.ps1` e reexecuta o
  instalador elevado â€” aparece o **UAC pedindo a senha de Administrador**. Use
  para instalaÃ§Ã£o nova ou quando o update rÃ¡pido falhar (pasta sem permissÃ£o).
  Obs.: o **primeiro** push do update rÃ¡pido em agentes antigos ainda cai no
  instalador com UAC; depois disso as atualizaÃ§Ãµes sÃ£o silenciosas.
- **Atualizar Tela de Bloqueio (sem UAC)**: baixa o `sysava_lock.ps1` (e
  wallpaper/logo) para `%LOCALAPPDATA%\SysAva`, encerra a tela antiga e abre a
  nova. Se a cÃ³pia em `C:\ProgramData\SysAva` nÃ£o tiver o bootstrap, cria um
  Startup por usuÃ¡rio; senÃ£o o prÃ³prio bootstrap jÃ¡ usa a cÃ³pia local no
  prÃ³ximo logon. NÃ£o pede Administrador.

> ðŸ• **Watchdog (auto-bloqueio, IS-078/IS-104/IS-164):** o agente **derruba sozinho** os
> jogos de `blocked_apps.json` + `BLOCKED_PROCESS_KEYWORDS` a cada ~4s (thread no
> agente, flag `AUTO_BLOCK`) e fecha janelas de sites de jogos. **Roblox,
> Fortnite/Epic e League of Legends são fechados enquanto o bloqueio persistente
> (`block_state.json`) estiver ativo**; **Desbloquear** remove o bloqueio e libera os jogos.

> âš¡ **AÃ§Ãµes em Massa**: o expansor "AÃ§Ãµes em Massa" tem **Desligar TODAS**,
> **Reiniciar TODAS** e **Bloquear Sites em TODAS** em um clique (exige marcar a
> confirmaÃ§Ã£o). Cada aÃ§Ã£o tambÃ©m Ã© registrada no histÃ³rico de auditoria.

> ðŸ’¡ As listas de bloqueio ficam no topo do `lab_agent.py`:
> `BLOCKED_PROCESS_KEYWORDS` (jogos instalados), `BLOCKED_SITE_KEYWORDS`
> (sites de jogos) e `BLOCKED_SOCIAL_KEYWORDS` (redes sociais).

### 3.1 Ferramentas (aba ðŸ§°)

- **Estrutura de pastas de atividades**: escolha **turma** e **disciplina**
  (vindas do Supabase), o intervalo de aulas (ex.: `1-32`), a **pasta base**
  (padrÃ£o `Documentos\SysAva`, gravÃ¡vel sem Administrador) e os PCs alvo. O
  agente cria **`<base>\<turma>\<disciplina>\<aluno>\Aula_01 â€¦ Aula_NN`** no PC do
  aluno (cada aluno tem a prÃ³pria pasta dentro da disciplina), de forma
  idempotente e sem UAC. O `<aluno>` usa sÃ³ os **dois primeiros nomes, sem
  sobrenome** (`PEDRO HENRIQUE PEREIRA GARCIAS` â†’ `PEDRO_HENRIQUE`), com
  espaÃ§os trocados por `_`.
  O `command_msg` vai em JSON:
  `{"base": "...", "turma": "...", "disciplina": "...", "aulas": "1-32"}`.
  O formato antigo `escola|turma|disciplina|aluno|aulas` continua aceito
  (escola/aluno sÃ£o ignorados), para nÃ£o quebrar agentes antigos.
- **Instalar Kit Lab DS (winget)**: VS Code, JDK 17, Node.js LTS e NetBeans
  nos PCs selecionados (pede UAC no PC do aluno).
- **Texto e Comando**: em **Ferramentas → 💬 Texto e Comando**, digite uma
  mensagem/alerta e/ou um comando do monitor (mesmo nome das ações do Controle).
  **Enviar texto** dispara `Enviar Alerta Visual`; **Executar comando** envia o
  comando digitado e, se houver texto, também mostra o alerta no PC (o texto
  acompanha o comando quando ele é um alerta).
- **Pacote de atualizaÃ§Ã£o**: baixa o `servidor.zip` (receiver, watchdog,
  bandeja/tray, diagnÃ³stico e demais scripts). Copie por cima da pasta
  `monitor` do outro PC e rode `reiniciar_servidor.bat`. O mesmo link aparece
  no topo do painel web (`/servidor.zip`).

- **Ferramentas em sub-abas**: **Atividades**, **Texto e Comando**, **Sites e
  RA**, **Tela** e **Manutenção**. A seleção de PCs (e **Aplicar em todas**)
  fica no topo.
- **Abrir SysAva com o RA do aluno**: escolha o aluno, o navegador
  (padrão/Chrome/Edge/Firefox/Brave/Opera) e a URL; o painel associa o RA ao
  PC, propaga aos peers e envia **"Abrir SysAva (RA)"** (`{url,browser,ra}`).
  O portal abre com `?ra=...` no navegador escolhido, **sem reiniciar o PC**.
  Requer **agente build 16+** (o `lab_agent.ps1` embute o código do agente).
- **Abrir site** também aceita o navegador; agentes antigos abrem no padrão.
- **Atualizar lista de alunos**: em **Sites e RA** (e no Controle), o
  botão **🔄 Atualizar lista de alunos** força a releitura de `app_users`
  (`role=student`), ignorando o cache de 30 min; em falha do Supabase,
  mantém a lista em cache e avisa.

### 4. Modo NÃ£o Invasivo (Bloqueio via Hosts) ðŸ›¡ï¸
Para mÃ¡quinas em que **nÃ£o Ã© possÃ­vel instalar o agente**, existe uma alternativa
que nÃ£o instala nada: o script **`bloquear_hosts.bat`** (acompanha
`bloquear_hosts.ps1`).
- Copie os dois arquivos num pendrive â€” **ou baixe em `http://<ip>:5000/setup`** â€” e
  execute o `.bat` (duplo-clique) em cada PC.
- Menu: **[1] Roblox**, **[2] Roblox + Redes Sociais** (YouTube, Instagram, TikTok,
  Facebook, X/Twitter) e **[3] Remover**. O script pede Administrador, Ã©
  **idempotente** e escreve apenas num bloco marcado do arquivo `hosts`, limpando o
  DNS ao final.
- A lista de domÃ­nios fica no prÃ³prio `.ps1` (`$Dominios` / `$DominiosSociais`).
  Para adicionar o Loki, inclua os domÃ­nios em `$Dominios` **ou** crie um
  `dominios_extra.txt` na mesma pasta, com um domÃ­nio por linha.

> âš ï¸ O bloqueio por `hosts` atua por **nome de domÃ­nio**; conexÃµes diretas por IP
> e alguns subdomÃ­nios fora da lista podem escapar. Ã‰ um complemento leve, nÃ£o
> substitui o agente quando o objetivo for controle total.

### 5. Monitoramento Manual (Celular/BYOD)
- **Alunos Externos**: Permite selecionar alunos da turma que nÃ£o estÃ£o nos PCs (usando celular ou notebooks prÃ³prios) e inseri-los no radar com um status manual.
- **Rastreamento de IP AutomÃ¡tico**: Ao adicionar um aluno manualmente, o sistema busca o Ãºltimo IP de login para validar o dispositivo.

### 6. HistÃ³rico de InfraÃ§Ãµes
- Exibe um log consolidado das infraÃ§Ãµes detectadas no dia, incluindo a hora, o nome do aluno, a categoria da infraÃ§Ã£o e a aÃ§Ã£o tomada pelo professor.

## ðŸ›¡ï¸ Tela de Bloqueio e Papel de Parede (SysAva)

DÃ¡ para deixar os PCs com a marca do SysAva e uma tela de bloqueio no logon:

- **Arquivos** (servidos em `http://<ip>:5000/setup`, card **3**):
  - `logo_sysava.png` / `wallpaper_sysava.png` â€” marca gerada por
    `gerar_logo_sysava.py`.
  - `aplicar_papel_parede.ps1` â€” sÃ³ o papel de parede (usuÃ¡rio atual) e, com admin,
    a tela de bloqueio/desktop via `PersonalizationCSP`.
  - `sysava_lock.ps1` â€” **tela cheia** com a marca e um **seletor de aluno**
    (nome + RA) para liberar. A lista vem de `/api/alunos` (cache de 30 min no
    servidor e cÃ³pia local em `%LOCALAPPDATA%\SysAva\alunos.json`), entÃ£o o aluno
    nÃ£o precisa digitar o RA: escolhe o prÃ³prio nome (dÃ¡ para digitar para
    filtrar). O Ãºltimo RA **nÃ£o** Ã© prÃ©-selecionado, para nÃ£o identificar o aluno
    errado. Ao liberar, abre o **sysava.streamlit.app com `?ra=<RA>`**, jÃ¡ com o
    campo **UsuÃ¡rio** preenchido na tela de login.
    Nos PCs comuns sÃ³ um **nome/RA da lista** libera; palavras soltas como
    `labadmin`, `aluno` ou `admin` sÃ£o recusadas. A **senha secreta**
    (`labadmin` por padrÃ£o) sÃ³ funciona no **PC mestre** (hostnames `PC01*` por
    padrÃ£o), mesmo sem servidor. Personalize o PC mestre com
    `SYSAVA_MASTER_HOSTS` (ex.: `PC01,NOTE-PROF`) ou
    `C:\ProgramData\SysAva\master_hosts.txt`.
    A cÃ³pia instalada em `C:\ProgramData\SysAva` se auto-atualiza no logon: baixa
    a versÃ£o do servidor para `%LOCALAPPDATA%\SysAva\sysava_lock.ps1` e roda essa
    cÃ³pia (gravÃ¡vel), sem UAC.
  - `instalar_tela_sysava.ps1` â€” baixa os arquivos para `C:\ProgramData\SysAva`,
    aplica o papel de parede e registra a tela para abrir no logon via **pasta
    Startup comum** (confiÃ¡vel; roda no logon de qualquer usuÃ¡rio) com **tarefa
    agendada como fallback**. `-Remover` limpa tarefa + Startup. Ao final mostra
    como testar na hora (rodar o `sysava_lock.ps1`).
- **ValidaÃ§Ã£o do RA/nome**: o overlay chama o receiver local em **`/api/auth_ra`**,
  que consulta o banco do SysAva: primeiro RA/username exato, depois o nome do
  aluno (sem caixa/acentos; nome completo quando o primeiro nome Ã© ambÃ­guo).
  Sem senha (modo simplificado). Descobre o servidor pelo cache do agente
  (`C:\Local\SysVa_lab\server_cache.txt`) ou por **broadcast UDP 5001**.
  A URL `-Server` gravada na instalaÃ§Ã£o sÃ³ Ã© usada se `/health` responder;
  se o notebook estiver desligado, o lock cai para o cache/UDP e encontra o
  PC do laboratÃ³rio. Sem servidor alcanÃ§Ã¡vel, nÃ£o libera por RA.
- **AssociaÃ§Ã£o aluno â†” PC**: ao validar o RA, a mÃ¡quina Ã© registrada em
  `lab_users.json` (`mÃ¡quina â†’ RA/nome`). No radar, a coluna **Aluno (RA)** mostra o
  aluno que desbloqueou aquele PC â€” resolve o caso do agente reportar `user: SYSTEM`.
  TambÃ©m grava no **histÃ³rico do aluno** (`Entrou no <RÃ³tulo> (tela de bloqueio)`),
  no mÃ¡ximo **1x por aluno/mÃ¡quina/dia** para nÃ£o pesar no Supabase.
- **Como usar**: no cliente, abra `http://<ip>:5000/setup` â†’ card **3** â†’
  `instalar_tela.bat` (pede Administrador). RefaÃ§a logoff para ver a tela.

### Regras de acesso (RA Ãºnico, coletivos e EJA)

- **RA Ãºnico**: o mesmo RA comum nÃ£o pode desbloquear dois PCs ao mesmo tempo.
  O `/api/auth_ra` devolve **400** com â€œO RA X jÃ¡ estÃ¡ em uso em `<PC>`. Saia
  daquela mÃ¡quina para entrar nesta.â€. Ao **deslogar/desligar** o PC de origem,
  o agente para de pingar e o RA Ã© liberado em ~60s (`OFFLINE_SECONDS`).
- **Contas coletivas**: contas de turma (ex.: `7anoA`, `7anoB`, `8ano`, `9ano`,
  `1alunoEja`, `Alunos_EJA_Noite`) **ficam fora** da regra de RA Ãºnico e podem
  estar em vÃ¡rios PCs. A lista Ã© configurÃ¡vel em
  `data/repo/plugins/monitor/acesso_coletivos.json`.
- **Janela do EJA**: as contas em `eja.contas` (padrÃ£o `1alunoEja` e
  `Alunos_EJA_Noite`) sÃ³ entram entre **17h e 23h** (hora local do servidor).
  Fora da janela o `/api/auth_ra` responde **400** e a tela de bloqueio exibe o
  aviso; a checagem tambÃ©m Ã© feita localmente no `sysava_lock.ps1` (vale no modo
  offline). A janela bloqueia **novos logins**: quem jÃ¡ estÃ¡ logado Ã s 23h
  continua atÃ© sair.
- **PC mestre**: a senha administrativa (e o bypass da lista) vale apenas nos
  hostnames configurados (padrÃ£o `PC01*`).
- **Professores na tela**: `acesso_coletivos.json` → `professores` (ex.:
  `["adriana"]`) libera docentes por login, RA ou nome **apenas nos PCs
  mestres** (`PC01*`). O `/api/auth_ra` associa o professor ao PC e o
  `/api/alunos?maquina=...` inclui esses nomes no seletor somente no mestre.
  Professores não entram na regra de RA único.

> ðŸ”’ **ReforÃ§o (IS-078/IS-164):** enquanto bloqueado, a tela **reafirma o topo** a cada 1s,
> **mata o `taskmgr.exe`** e **desabilita o Gerenciador de Tarefas** (`DisableTaskMgr`
> no HKCU, restaurado ao desbloquear). Ao validar o RA, `sysava_lock.ps1` grava
> `%LOCALAPPDATA%\SysAva\tela_ok.json`; o agente **relanÃ§a a tela** se o processo
> desaparecer sem esse token vÃ¡lido para a sessÃ£o do Windows (o painel mostra
> **liberada (aluno)**). Ainda **nÃ£o** Ã© um kiosk rÃ­gido (Alt+F4/Alt+Tab podem
> escapar por alguns segundos atÃ© a tela voltar).

## ðŸ›¡ï¸ ProteÃ§Ã£o do Aluno e Alertas (planejado â€” IS-072)

> âš ï¸ **Parcialmente implementado** (Tier 1/Tor). Finalidade: **proteÃ§Ã£o**
> (autorizada pela escola/responsÃ¡veis), nÃ£o vigilÃ¢ncia genÃ©rica. RelatÃ³rios com
> acesso restrito; retenÃ§Ã£o definida.

**JÃ¡ disponÃ­vel:**
- **`aplicar_dns_seguro.ps1`** (card **4** em `/setup`): DNS de famÃ­lia
  (Cloudflare for Families) bloqueia **adulto + malware** por PC (`-Perfil
  family-adult`); `-Revert` desfaz. Ideal: aplicar no **roteador/DHCP** tambÃ©m.
- **`bloquear_hosts.ps1 -Perigo`**: adiciona ao `hosts` os domÃ­nios das listas em
  `categorias/*.txt` (adulto/apostas/malware/anÃ´nimos). O `.bat` tem a opÃ§Ã£o
  **[3] ProteÃ§Ã£o**.
- **Tor/anonimizadores**: o agente detecta e classifica como **"AnÃ´nimo"** (categoria
  no radar) e hÃ¡ a aÃ§Ã£o **"Bloquear AnÃ´nimos (Tor)"** no painel.

**Ainda planejado:** alerta automÃ¡tico por limiar (sugerir/bloquear), categorias de
risco emocional/criminal e log/relatÃ³rio (ISâ€‘071).

O monitor terÃ¡ uma **polÃ­tica de tiers** (bloquear x alertar x registrar):

| Tipo | AÃ§Ã£o | Alerta ao professor |
|---|---|---|
| Adulto/pornografia, malware/phishing, apostas, Tor/anÃ´nimos/VPN de evasÃ£o | **Bloqueia automÃ¡tico** (silencioso) | **NÃ£o** â€” sÃ³ log |
| Redes sociais e jogos/streaming em **excesso** | **Sugere bloquear** (professor aciona no painel) | Sim (agrupado por limiar) |
| Risco emocional (automutilaÃ§Ã£o, violÃªncia) e criminal (aliciamento) | **Bloqueia + destaca** | **PrioritÃ¡rio e discreto** |
| Qualquer ocorrÃªncia | **Registra** (log/relatÃ³rio) | â€” |

Diretrizes:
- **Tier 1** (rede/hosts): DNS de filtro (famÃ­lia Cloudflare `1.1.1.3`/`1.1.1.2` ou
  OpenDNS FamilyShield) + `bloquear_hosts.ps1` com listas por categoria. NÃ£o alerta
  por evento (sÃ³ grava) para nÃ£o gerar fadiga de alerta.
- **Tor/dark web**: `.onion` nÃ£o acessa na rede normal; detectar/bloquear `tor.exe`,
  bridges e I2P e alertar.
- **Tiers 2 e 3**: o **agente** classifica por janela ativa/histÃ³rico do navegador e
  sinaliza; o **painel do Monitor** mostra, sugere a aÃ§Ã£o e destaca o Tier 3.
- **Log/registro**: pasta oculta na pasta do monitor (ex.: `.relatorios/`) com `.log`
  e `.html` (o que/quando/quem/mÃ¡quina/categoria).
- **NÃ£o bloquear tudo automaticamente**: o ambÃ­guo Ã© decisÃ£o do professor (evita
  bypass por VPN/celular e preserva a visibilidade).

## ðŸŒ Painel Web do Receiver (login + controles)

AlÃ©m do plugin no Streamlit, o prÃ³prio **receiver** (porta 5000) tem um painel web
acessÃ­vel de qualquer navegador/tablet na rede:

- **EndereÃ§o:** `http://<ip-do-professor>:5000/`
- **Login:** exige um usuÃ¡rio do SysAva com `role` **teacher** ou **admin** (valida
  login/senha no banco; aceita tambÃ©m RA e ignora maiÃºsculas). SessÃ£o por cookie
  assinado (`receiver_secret.key`). As pÃ¡ginas `/` e `/diagnostics` sÃ£o protegidas.
- **Controles:** marque as mÃ¡quinas (checkbox, com â€œselecionar todasâ€), escolha a
  **aÃ§Ã£o** (alerta, bloquear jogos/sites/anÃ´nimos/navegador, deslogar, desligar,
  reiniciar), opcionalmente a mensagem do alerta, e **Executar** â€” o comando Ã©
  gravado para o agente (`pending_command`) e aplicado no prÃ³ximo ciclo (~10s).
- **Abas do painel:** ðŸ“Š **Monitor** (cards + tabela com os checkboxes), ðŸ•¹ï¸
  **Controle** (aÃ§Ã£o + mensagem + Executar) e ðŸ§° **Ferramentas** (estrutura de
  pastas de atividades + pacote de atualizaÃ§Ã£o). A aba ativa fica no `#hash` da
  URL, entÃ£o recarregar mantÃ©m a mesma aba.
- **ðŸ‘¤ Aluno do PC (designar RA):** na aba **Controle**, escolha o PC e o aluno e
  clique em *Designar aluno ao PC* â€” equivale a o aluno ter passado pela tela de
  bloqueio: atualiza `lab_users.json` (radar/histÃ³rico) e passa a ser o nome
  usado na pasta de atividades. NÃ£o desbloqueia a tela de bloqueio do PC.
- **Ferramentas â†’ Estrutura de pastas:** escolha **turma** e **disciplina**
  (carregadas do Supabase, com cache de 10 min), as aulas (`1-32`) e a pasta
  base (`%USERPROFILE%\Documents\SysAva` por padrÃ£o, expandida no PC do aluno).
  Marque **â€œAplicar em todas as mÃ¡quinas onlineâ€** ou selecione PCs na aba
  Monitor. O comando `Estruturar Pastas` leva um JSON em `command_msg` e o
  agente cria `<base>\<turma>\<disciplina>\<aluno>\Aula_01..NN` (uma pasta por
  aluno â€” sÃ³ os dois primeiros nomes, sem sobrenome â€” sem UAC, idempotente).
- **Pacote de atualizaÃ§Ã£o:** link **â¬‡ï¸ Pacote de atualizaÃ§Ã£o** no topo (e dentro
  da aba Ferramentas) â†’ `/servidor.zip` com receiver, watchdog, bandeja (tray),
  diagnÃ³stico e demais scripts.
- **ðŸ“¦ Backups de atividades:** o botÃ£o **ðŸ“¦ Solicitar ZIP das atividades** existe
  na aba **Ferramentas** do Streamlit **e** do painel web e envia o comando
  `Enviar Atividades` aos PCs selecionados; o agente compacta a pasta de
  atividades e envia para `/upload/atividades`. O agente procura a pasta na base
  pedida (`%USERPROFILE%\Documents\SysAva`) e, se nÃ£o existir, nos perfis do
  Windows/OneDrive/Public; sem pasta ele devolve um erro claro no resultado do
  comando. O servidor guarda `data/repo/plugins/monitor/.atividades/<PC>.zip`
  (sobrescreve o envio anterior do mesmo PC) e a pÃ¡gina **ðŸ“¦ Atividades**
  (`/atividades`) lista, baixa um por PC ou **baixar todos** em
  `atividades_sysava.zip` para revisÃ£o/backup no notebook. Se um PC nÃ£o
  responder, confira o **Ãšltimo comando por PC** (aba Ferramentas) e reenvie sÃ³
  para ele.
- **Detalhes por PC (ðŸ”Ž):** cada linha tem o link **ðŸ”Ž** â†’ `/detalhes?maquina=X`, que
  mostra usuÃ¡rio/IP, janela ativa, categoria, portas e **trÃªs listas**: ðŸŒ Navegadores,
  ðŸŽ® Jogos e âš™ï¸ Outros processos em atividade (o agente envia a lista `procs` a cada ciclo).
- **Abertos (sem login):** endpoints usados pelos agentes (`/ping`, `/health`,
  `/api/*`, `/scan`) e as pÃ¡ginas `/setup` e `/download/*`.

> Ãštil para operar do celular quando nÃ£o estiver no notebook do SysAva. Sair pelo
> link **Sair** (`/logout`) encerra a sessÃ£o do painel.

## ðŸ“‹ Registro de Atividade dos UsuÃ¡rios (IS-071)

Auditoria de **o que cada usuÃ¡rio fez e quando** no SysAva, guardada numa **pasta
oculta** para consulta:

- **Onde fica:** `data/repo/plugins/monitor/.relatorios/` (pasta marcada como **oculta**),
  com um arquivo por dia `atividade-AAAA-MM-DD.log` (JSON-lines) e um
  `relatorio.html`.
- **O que Ã© registrado:** **Login**, **NavegaÃ§Ã£o** (troca de pÃ¡gina, 1x por pÃ¡gina,
  com data/hora e IP) e **Logout**. Feito em `services/audit_log.py`, com ganchos em
  `app.py` e `views/login.py`. NÃ£o faz chamada de rede (nÃ£o afeta o egress).
- **Como consultar:** no painel web do receiver, **ðŸ“‹ RelatÃ³rios** â†’
  `http://<ip>:5000/relatorios` (exige login). LÃ¡ tambÃ©m Ã© possÃ­vel gerar/regerar o
  HTML.
- **HistÃ³rico do navegador:** o **agente** lÃª o `History` do **Chrome/Edge** (copiando
  o arquivo, pois fica travado aberto) a cada ~180s e envia para `POST /api/historico`;
  o relatÃ³rio mostra uma segunda tabela com essas visitas.
- **Residual (opcional):** filtros por dia/usuÃ¡rio na tela e polÃ­tica de retenÃ§Ã£o/limpeza
  dos logs.

> Dado sensÃ­vel: mantenha o acesso restrito e defina finalidade/retenÃ§Ã£o com a escola.

## ðŸ–¥ï¸ Servidor PortÃ¡til (sem depender do notebook)

O receiver pode rodar num **PC fixo sempre ligado** em vez do notebook:

1. Copie a pasta **`data/repo/plugins/monitor`** para o PC fixo (ela jÃ¡ contÃ©m o `lab_receiver.py`, o
   `audit_log.py`, os assets e os scripts).
2. Crie um **`.env`** na pasta (modelo: `config.env.example`) com `SUPABASE_URL` e
   `SUPABASE_KEY`.
3. Rode **`INICIAR_SERVIDOR.bat`** (duplo-clique). Ele baixa um **Python portÃ¡til** se
   preciso, instala `flask/waitress/filelock/requests/bcrypt/python-dotenv`, **abre o
   firewall** (TCP 5000 / UDP 5001/5002) e sobe o servidor.
4. Acesse `http://<ip-do-pc>:5000/` (login) ou `/setup` para instalar/atualizar os
   clientes.
5. Para subir sozinho com o Windows, rode **`instalar_servidor_auto.ps1`** como
   Administrador. Por padrÃ£o a tarefa **SysAva Servidor** inicia no **boot**
   (SYSTEM, sem precisar de usuÃ¡rio logado); use `-Logon` para iniciar sÃ³ no
   logon do usuÃ¡rio e `-Remover` para desfazer. A tarefa roda o
   `servidor_watchdog.ps1`, que reinicia o receiver se ele cair e grava
   `servidor.log` (rotaÃ§Ã£o em 5 MB). O card **7** do `/setup` tambÃ©m baixa os
   scripts.

### ðŸ¤ Notebook + PC do laboratÃ³rio ao mesmo tempo

Os dois receivers podem ficar online e se completam:

- Descobrem-se por **UDP 5002** (e tambÃ©m pela 5001, jÃ¡ liberada). Fallback:
  `peers.txt` com uma URL por linha (ex.: `http://192.168.10.126:5000`) ou
  `PEER_URLS=http://ip:5000,...` no `.env`.
- Cada um consulta `/api/peer/state` do outro a cada 5 s e mostra no dashboard a
  **uniÃ£o** das mÃ¡quinas (marcadas â€œvia <host>â€). O radar do Streamlit tambÃ©m vÃª
  as duas.
- Comandos enviados de qualquer dashboard vÃ£o para `/api/command`; se a mÃ¡quina
  pertence ao outro servidor, o comando Ã© encaminhado para `/api/peer/command`.
  O roteamento escolhe o servidor cujo **Ãºltimo reporte** da mÃ¡quina Ã© mais
  recente (o agente fala com um servidor por vez), entÃ£o funciona mesmo com os
  dois servidores reiniciando/fazendo failover.
- Se usar `PEER_TOKEN`, ele deve ser **igual nos dois `.env`** (ou ficar em
  branco nos dois); token diferente faz o encaminhamento ser recusado com 401.
- **Preferência de servidor (PC01):** o **PC01 do laboratório** tem prioridade.
  O `/health` informa `hostname` e `preferred`, e os agentes, a tela de bloqueio
  e as bandejas escolhem primeiro o servidor cujo hostname casa com `PC01*`
  (mesmo que o notebook responda antes). No cluster, o PC01 também fica como
  **primário** mesmo subindo depois do notebook; sem ele, vale quem iniciou
  primeiro. Ajuste a lista com `SYSAVA_PREFERRED_SERVERS` (ex.: `PC01*,PC02*`;
  vazio desliga a preferência).
- **Auto-start:** instale no PC fixo (`PC01-LAB02`) com
  `instalar_servidor_auto.bat`. No notebook, se quiser iniciar junto com o
  Windows, use `-Logon` (roda na sessÃ£o do usuÃ¡rio, nÃ£o como SYSTEM); para
  manutenÃ§Ã£o, o normal Ã© subir o notebook manualmente.
- **Bandeja (tray) do servidor:** rode `tray_servidor.bat` no PC do laboratório.
  Mostra o **IP atual** no título/menu (atualiza sozinho), o status (verde/amarelo/
  vermelho) e permite abrir o painel local, **abrir o painel do 2º servidor**
  (peer via `/api/peer/state`), ver o log, reiniciar, iniciar/parar e marcar
  **"Iniciar com o Windows"**. Também tem **Abrir SysAva (8501)** e **Apps**
  (Streamlit local quando há `.sysenv`/`app.py`; senão abre o portal na
  nuvem) e **Parar todos os apps**. Se a tarefa `SysAva Servidor` (SYSTEM) já estiver
  rodando, a bandeja apenas monitora: nunca abre uma segunda instância.
- **Bandeja do aluno (`tray_aluno`)**: mostra **nome + RA** no título e permite
  **Mostrar/Copiar o RA** além do e-mail institucional, **Atualizar meus dados**,
  **Abrir SysAva com meu RA**, **Abrir tela de bloqueio**, **Sair da conta** e
  **Sair do Windows (logoff)**. O RA vem da API/cache (`meu_email.txt`) ou de
  `%LOCALAPPDATA%\SysAva\ultimo_ra.txt` (gravado pela tela de bloqueio).
  **Sair da conta** remove `tela_ok.json`/`ultimo_ra.txt`/`meu_email.txt`, chama
  `POST /api/logout_ra` (que apaga a associação da máquina em `lab_users.json` e
  avisa os peers em `/api/peer/logout`) e reabre a tela de bloqueio. Se o
  servidor estiver fora, o logout fica em `logout_pendente.json` e é sincronizado
  quando ele voltar. Assim o RA fica livre para outro PC na hora. Reinicie o
  receiver do servidor para a rota `/api/logout_ra` entrar em vigor (até lá o
  logout fica na fila local). **Atualizar Bandeja do Aluno** (Controle) baixa os
  arquivos e reinicia a instância antiga; para mudanças manuais, feche e reabra
  o `tray_aluno.bat`.
- **Aba Usuários no painel web:** o painel (porta 5000) tem a aba **Usuários**
  para criar contas, **Desativar/Reativar** o acesso ao portal e **Remover**
  cadastros. O bloqueio grava `app_users.status='blocked'` e não altera a
  frequência (`is_active`/`is_portal`). Professor gerencia apenas alunos;
  administrador gerencia qualquer função. A própria conta e o último
  administrador ativo são protegidos. O login do painel também recusa contas
  bloqueadas. Reinicie o receiver (`reiniciar_servidor.bat`) para carregar a aba.
- **Quando o servidor nÃ£o sobe no boot:** rode `diagnostico_servidor.bat` **no PC
  do laboratÃ³rio**. Ele confere arquivos (`servidor.log` existir Ã© o sinal de que
  o watchdog jÃ¡ rodou), Python/dependÃªncias, porta 5000/`/health`, peers, a tarefa
  agendada (estado + Ãºltimo resultado + pasta de destino), firewall, rede e
  arquivos "somente online" do OneDrive/Google Drive, e lista as provÃ¡veis causas.
- **Ordem de ligaÃ§Ã£o:** ligue o **PC01 primeiro**. Se as mÃ¡quinas dos alunos
  terminarem o boot antes, a tela de bloqueio espera atÃ© **3 min** redescoberto
  o servidor e valida o RA sozinha, sem precisar clicar de novo. Mesmo que o
  notebook suba antes, o PC01 assume como preferido assim que aparecer.
- O **PC01** (hostnames `PC01*`) Ã© o **primÃ¡rio** sempre que estiver online; os
  demais sÃ£o **assistentes**. Sem o PC01, vale quem **comeÃ§ou primeiro**. O papel
  aparece no topo do dashboard e Ã© recalculado quando um peer fica 30 s sem sinal
  (failover). Comandos podem ser enviados dos dois.

O receiver agora Ã© **autÃ´nomo**: login e relatÃ³rio usam **REST do Supabase** (nÃ£o
dependem do app/venv), entÃ£o sÃ³ precisa de `flask`, `requests`, `bcrypt` etc. Precisa
de **internet** para login/relatÃ³rio; agentes/downloads funcionam na LAN.

## ðŸ“¦ InstalaÃ§Ã£o do Agente (`lab_agent.ps1`)

Para que os computadores apareÃ§am no radar, Ã© necessÃ¡rio instalar o agente standalone.
**A descoberta do servidor Ã© automÃ¡tica** (cache â†’ MAC/ARP â†’ broadcast UDP â†’ IP
conhecido â†’ varredura), entÃ£o nÃ£o Ã© mais preciso editar IP no script.

InstalaÃ§Ã£o **sem pendrive** (pela rede):
1. No notebook do professor, garanta que o **receiver** estÃ¡ rodando (`lab_receiver.bat`
    ou abrindo o plugin Monitor no SysAva). Ele cria as regras de firewall TCP 5000 e UDP 5001/5002.
2. No PC cliente, abra o navegador e acesse **`http://<ip-do-professor>:5000/setup`**
   (o IP aparece no diagnÃ³stico; ex.: `http://192.168.11.253:5000/setup`).
3. Baixe o **`instalar_agente.bat`** (ou o `lab_agent.ps1`) e execute. O `.bat` baixa
   o script do prÃ³prio servidor e roda como Administrador.
4. O script baixa um Python portÃ¡til, instala `psutil`, `requests` e `pygetwindow` e
   inicia o monitoramento oculto. **Rodar de novo atualiza o agente** â€” a instÃ¢ncia
   anterior Ã© encerrada automaticamente antes de iniciar a nova.
5. **Auto-inicializaÃ§Ã£o**: o instalador registra a tarefa **â€œSysAva Agentâ€** (no
   logon, para `BUILTIN\Users`), entÃ£o o agente **volta sozinho apÃ³s reiniciar** â€”
   sem isso, a mÃ¡quina some do radar depois de um reboot/desligamento.
6. Os mesmos downloads tambÃ©m servem o **bloqueio nÃ£o invasivo** (`bloquear_hosts.bat`).

> ðŸ” **SessÃ£o do agente:** se o agente for iniciado como **SYSTEM** (sessÃ£o 0 â€” comum
> ao empurrar via GPO/Intune/RMM ou `psexec -s`), ele **relanÃ§a automaticamente na
> sessÃ£o do usuÃ¡rio logado** (`WTSQueryUserToken` + `CreateProcessAsUser`) para
> conseguir ver a janela ativa real do aluno, e a cÃ³pia de sistema encerra. Se o
> aluno nÃ£o for administrador da mÃ¡quina, comandos que exigem privilÃ©gio
> (desligar/reiniciar) podem ser recusados â€” nesse caso rode o agente na sessÃ£o
> do usuÃ¡rio com privilÃ©gios elevados.

> O servidor de arquivos lÃª os `.ps1`/`.bat` do disco a cada download, entÃ£o basta
> atualizar o arquivo na pasta de plugins e rebaixar nos clientes para atualizar.

## ðŸ› ï¸ Como Usar

1.  **Acesse o Plugin**: No menu lateral do SysAva, selecione a aba **Plugins** e clique em **Grade** (ou no Ã­cone de monitoramento).
2.  **Selecione a Turma**: Na barra lateral, selecione a turma que estÃ¡ no laboratÃ³rio para habilitar o monitoramento manual.
3.  **Analise o Dashboard**: Verifique os nÃºmeros no topo para sentir o "clima" da sala.
4.  **Identifique Alvos**: Role a tabela de monitoramento. Procure pelas linhas em vermelho (Roblox) ou roxo (Celular).
5.  **Monitore Celulares**: Se notar um aluno no celular, use o expansor "Monitorar Alunos Externos" para adicionÃ¡-lo ao radar com o status apropriado.
6.  **Intervenha**:
    - No painel **Central de IntervenÃ§Ã£o**, selecione as mÃ¡quinas que deseja controlar.
    - Escolha a aÃ§Ã£o (ex: "Enviar Alerta Visual").
    - Se necessÃ¡rio, digite a mensagem personalizada.
    - Clique em **ðŸš€ Executar Comando Remoto**.
7.  **Acompanhe o Resultado**: O status da mÃ¡quina na tabela serÃ¡ atualizado assim que o comando for processado ou quando a infraÃ§Ã£o for registrada.

## ðŸ› ï¸ SoluÃ§Ã£o de Problemas de ConexÃ£o

Se as mÃ¡quinas clientes nÃ£o estiverem conectando ou a conexÃ£o estiver inconstante, verifique os seguintes pontos:

1. **ImportaÃ§Ã£o do MÃ³dulo `re`**: Verifique se o arquivo `lab_agent.py` possui o `import re` no topo. Sem ele, a funÃ§Ã£o de busca por MAC falha silenciosamente no loop principal, impedindo a localizaÃ§Ã£o do servidor.
2. **Tabela ARP Vazia**: O comando `arp -a` pode nÃ£o listar o servidor se nÃ£o houve comunicaÃ§Ã£o recente entre as mÃ¡quinas. Se uma mÃ¡quina nÃ£o conectar, tente realizar um ping manual do cliente para o IP do servidor para "acordar" a tabela ARP.
3. **Firewall do Servidor**: Garanta que a porta `5000` (TCP) esteja aberta para conexÃµes de entrada no Windows Firewall do computador do professor (Servidor). Sem isso, as mÃ¡quinas podem encontrar o servidor mas nÃ£o conseguirÃ£o enviar os dados.
4. **DiferenÃ§a de Sub-rede**: Se o agente logar `Invalid URL 'http:///ping'`, significa que ele encontrou o MAC mas nÃ£o resolveu o IP. Verifique se todas as mÃ¡quinas estÃ£o na mesma mÃ¡scara de sub-rede e se nÃ£o hÃ¡ isolamento de AP (em redes Wi-Fi).
5. **Descoberta automÃ¡tica do servidor**: o agente procura o servidor nesta ordem â€” **cache local** (`server_cache.txt`, o Ãºltimo que funcionou), **MAC/ARP**, **broadcast UDP** (porta **5001**), **IP conhecido** e, por fim, **varredura da sub-rede**. Garanta que a porta **TCP 5000** e a **UDP 5001** estejam liberadas no firewall do notebook do professor. O par TCP 5000 + UDP 5001 faz o agente reencontrar o servidor mesmo quando o IP muda por DHCP.

## ðŸ’¡ Dica para OperaÃ§Ã£o Offline (Sem Roteador)
Para usar o monitoramento sem uma rede Wi-Fi, vocÃª pode criar uma rede Ad-Hoc (Hotspot) diretamente do seu notebook.
1. No Windows, vÃ¡ em "ConfiguraÃ§Ãµes" > "Rede e Internet" > "Hotspot mÃ³vel".
2. Ative o Hotspot. Os computadores dos alunos devem se conectar a esta nova rede.
3. O agente (`lab_agent.py`) encontrarÃ¡ seu notebook automaticamente, pois estarÃ£o na mesma "mini-rede".
## âš ï¸ ConsideraÃ§Ãµes Importantes

-   **Necessidade de Agente Local**: Este plugin depende de um pequeno script Python (agente) rodando em segundo plano em cada mÃ¡quina do laboratÃ³rio que envie os dados para o arquivo `lab_status.json`.
-   **IP Fixo/Reserva**: Ã‰ recomendado que as mÃ¡quinas do laboratÃ³rio tenham IPs reservados para facilitar a identificaÃ§Ã£o constante.
-   **SeguranÃ§a**: Os comandos remotos sÃ£o registrados no histÃ³rico para fins de auditoria pedagÃ³gica.

---
*DocumentaÃ§Ã£o criada para o sistema SysAva.*
