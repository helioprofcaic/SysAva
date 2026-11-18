# `plugins/` — código dos plugins do SysAva

Esta pasta guarda o **código-fonte** dos plugins (UI e ferramentas versionadas).
A pasta **`data/repo/plugins/`** continua sendo a **pasta de deploy/runtime**:
o monitor fica em **`data/repo/plugins/monitor/`** (receiver, agente, tela,
bandejas, logs e dados) e o restante dos plugins segue em `data/repo/plugins/`.

> Regra de ouro: **código novo mora aqui; runtime mora em `data/repo/plugins/` (monitor em `monitor/`).**
> Nada de dados de aluno, logs ou `.env` nesta pasta.

## Estrutura alvo

```
plugins/
  monitor_rede/            # FASE 1 (concluída)
    lab_monitor.py         # UI Streamlit (Radar/Controle/Ferramentas/...)
    README.md              # documentação do plugin
  atividades/              # planos/roteiros de atividades (já existente)
  aulas/                   # planos de aula prontos/pendentes (já existente)
  servidor/                # FASE 2 (proposta)
    lab_receiver.py        # fonte do servidor; deploy copia para data/repo/plugins/monitor
    audit_log.py
    tray_servidor.ps1 / .vbs / .bat
    servidor_watchdog.ps1
  agente/                  # FASE 3 (proposta)
    lab_agent.py / .ps1
    sysava_lock.ps1
    instalar_tela_sysava.ps1
  ferramentas/             # FASE 3 (proposta)
    definir_volume.ps1, bloquear_hosts.ps1/.bat, aplicar_dns_seguro.ps1,
    aplicar_papel_parede.ps1, gerar_logo_sysava.py
  assets/                  # logo_sysava.png, wallpaper_sysava.png
```

## O que fica em `data/repo/plugins/monitor/` (runtime/deploy)

- Executáveis que os PCs baixam/rodam: `lab_receiver.py`, `lab_agent.py`,
  `*.ps1`/`*.bat`/`*.vbs`, `sysava_lock.ps1`, `servidor_watchdog.ps1`.
- Dados e configuração: `.env` (também é lido da raiz do projeto),
  `lab_status.json`, `lab_users.json`, `lab_labels.json`, `alunos_cache.json`,
  `acesso_coletivos.json` (contas coletivas + janela EJA), `emails.json`,
  `site_padrao.json`, `receiver_secret.key`, `*.log`, `peers.txt`,
  `.atividades/`, `.relatorios/`, `categorias/`.
- O `lab_receiver.py` **serve os arquivos dessa pasta** (`/download/...` e
  `/servidor.zip`). Os caminhos internos (`PROJECT_ROOT`, `.sysenv`) sobem
  quatro níveis até a raiz do projeto.
- O restante de `data/repo/plugins/` continua guardando os outros plugins
  (notas, frequência, planos, auditoria) e os dados de Turmas.

## Fases da migração

1. **Monitor (feito):** `lab_monitor.py` → `plugins/monitor_rede/`.
   - `views/plugins.py` carrega `plugins/monitor_rede/lab_monitor.py` (com
     fallback para o caminho antigo).
   - O runtime do monitor foi movido para `data/repo/plugins/monitor/`; o
     plugin resolve a pasta por `SYSAVA_PLUGIN_DIR` ou por
     `data/repo/plugins/monitor` (com fallback para `data/repo/plugins`).
2. **Servidor:** mover o **fonte** para `plugins/servidor/` e criar um script
   `scripts/sync_deploy.py` que copia para `data/repo/plugins/monitor/` antes de
   empacotar/baixar. Só fazer depois de validar que o `/servidor.zip` continua
   com todos os arquivos e que `reiniciar_servidor.bat` segue funcionando.
3. **Agente/ferramentas:** mesma ideia, um plugin por pasta, sem mexer no
   runtime de deploy até o sync estar estável.

## Como um plugin é carregado

`views/plugins.py` importa o arquivo `.py` por **caminho** (recarrega do disco a
cada clique) e procura um ponto de entrada (`show_lab_monitor`, `show_agenda`,
`show_page`, ...). Por isso basta mover o arquivo e atualizar o caminho — não é
necessário virar pacote Python (nada de `__init__.py`).
