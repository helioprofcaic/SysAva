---
title: Documentação do Plugin de Monitoramento de Laboratório (lab_monitor.py)
description: Guia sobre o radar de atividade, estatísticas de uso e painel de controle remoto para o laboratório de informática.
---

# 🖥️ Plugin de Monitoramento de Laboratório (`lab_monitor.py`)

Este plugin permite que o professor tenha uma visão em tempo real do que está acontecendo em cada computador do laboratório, facilitando a gestão da sala de aula e garantindo que o foco permaneça nas atividades pedagógicas.

## 🚀 Visão Geral

O `lab_monitor.py` atua como um "radar" que categoriza automaticamente a atividade dos alunos em: **Produtivo**, **Roblox**, **Games**, **Redes Sociais** ou **Celular (Proibido)**. Ele utiliza o mapeamento de IP para identificar qual aluno está em qual máquina e permite o monitoramento manual de alunos que não estão usando os PCs do laboratório.

## ✨ Principais Funcionalidades

### 1. Dashboard de Estatísticas (Radar)
- **Métricas Globais**: Exibe o total de máquinas online e a contagem específica de alunos no Roblox, em Redes Sociais/Games e em atividades produtivas.
- **Contador de Infrações**: Soma em tempo real alunos detectados em jogos ou usando o celular indevidamente.
- **Gráfico de Distribuição**: Um gráfico de barras que resume visualmente o comportamento atual do laboratório.

### 2. Monitoramento ao Vivo (Tabela de Calor)
- **Categorização Visual**: A tabela de monitoramento utiliza cores para facilitar a identificação rápida:
    - 🔴 **Vermelho**: Roblox detectado.
    - 🟠 **Laranja**: Sites de Games ou entretenimento.
    - 🔵 **Azul**: Redes Sociais (Instagram, YouTube, etc).
    - 🟣 **Roxo**: Uso de celular flagrado/registrado.
    - 🟢 **Verde**: Atividade Produtiva (VS Code, Google Docs, etc).
- **Identificação por IP**: Mostra o IP do dispositivo, permitindo cruzar dados com o histórico de login do aluno no SysAva.

### 3. Central de Intervenção (Comandos Remotos)
Permite selecionar uma ou mais máquinas para executar ações imediatas:
- **Enviar Alerta Visual**: Exibe uma mensagem na tela do aluno (ex: "Foco na atividade!").
- **Bloquear Processo**: Encerra o executável do Roblox ou do jogo detectado.
- **Bloquear Navegador**: Fecha as abas do navegador que não são relacionadas à aula.
- **Registrar Uso Indevido de Celular**: Altera o status do aluno para "Roxo" no radar e grava uma infração permanente no histórico do aluno (RA).
- **Forçar Logoff**: Desloga o usuário da máquina em casos de reincidência grave.

### 4. Monitoramento Manual (Celular/BYOD)
- **Alunos Externos**: Permite selecionar alunos da turma que não estão nos PCs (usando celular ou notebooks próprios) e inseri-los no radar com um status manual.
- **Rastreamento de IP Automático**: Ao adicionar um aluno manualmente, o sistema busca o último IP de login para validar o dispositivo.

### 5. Histórico de Infrações
- Exibe um log consolidado das infrações detectadas no dia, incluindo a hora, o nome do aluno, a categoria da infração e a ação tomada pelo professor.

## 📦 Instalação do Agente (`lab_agent.ps1`)

Para que os computadores apareçam no radar, é necessário instalar o agente standalone:
1. Localize o arquivo `lab_agent.ps1` na pasta de plugins.
2. Edite a variável `$SERVER_IP` com o IP do seu computador (servidor).
3. Execute o script com privilégios de administrador nos PCs dos alunos.
4. O script baixará um Python portátil, configurará o ambiente e iniciará o monitoramento oculto automaticamente.

## 🛠️ Como Usar

1.  **Acesse o Plugin**: No menu lateral do SysAva, selecione a aba **Plugins** e clique em **Grade** (ou no ícone de monitoramento).
2.  **Selecione a Turma**: Na barra lateral, selecione a turma que está no laboratório para habilitar o monitoramento manual.
3.  **Analise o Dashboard**: Verifique os números no topo para sentir o "clima" da sala.
4.  **Identifique Alvos**: Role a tabela de monitoramento. Procure pelas linhas em vermelho (Roblox) ou roxo (Celular).
5.  **Monitore Celulares**: Se notar um aluno no celular, use o expansor "Monitorar Alunos Externos" para adicioná-lo ao radar com o status apropriado.
6.  **Intervenha**:
    - No painel **Central de Intervenção**, selecione as máquinas que deseja controlar.
    - Escolha a ação (ex: "Enviar Alerta Visual").
    - Se necessário, digite a mensagem personalizada.
    - Clique em **🚀 Executar Comando Remoto**.
7.  **Acompanhe o Resultado**: O status da máquina na tabela será atualizado assim que o comando for processado ou quando a infração for registrada.

## 🛠️ Solução de Problemas de Conexão

Se as máquinas clientes não estiverem conectando ou a conexão estiver inconstante, verifique os seguintes pontos:

1. **Importação do Módulo `re`**: Verifique se o arquivo `lab_agent.py` possui o `import re` no topo. Sem ele, a função de busca por MAC falha silenciosamente no loop principal, impedindo a localização do servidor.
2. **Tabela ARP Vazia**: O comando `arp -a` pode não listar o servidor se não houve comunicação recente entre as máquinas. Se uma máquina não conectar, tente realizar um ping manual do cliente para o IP do servidor para "acordar" a tabela ARP.
3. **Firewall do Servidor**: Garanta que a porta `5000` (TCP) esteja aberta para conexões de entrada no Windows Firewall do computador do professor (Servidor). Sem isso, as máquinas podem encontrar o servidor mas não conseguirão enviar os dados.
4. **Diferença de Sub-rede**: Se o agente logar `Invalid URL 'http:///ping'`, significa que ele encontrou o MAC mas não resolveu o IP. Verifique se todas as máquinas estão na mesma máscara de sub-rede e se não há isolamento de AP (em redes Wi-Fi).

## ⚠️ Considerações Importantes

-   **Necessidade de Agente Local**: Este plugin depende de um pequeno script Python (agente) rodando em segundo plano em cada máquina do laboratório que envie os dados para o arquivo `lab_status.json`.
-   **IP Fixo/Reserva**: É recomendado que as máquinas do laboratório tenham IPs reservados para facilitar a identificação constante.
-   **Segurança**: Os comandos remotos são registrados no histórico para fins de auditoria pedagógica.

---
*Documentação criada para o sistema SysAva.*