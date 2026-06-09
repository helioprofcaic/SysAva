---
title: Documentação do Plugin de Registro de Aula (class_registry.py)
description: Guia completo sobre as funcionalidades do plugin de registro de aulas do SysAva, incluindo integração com grade, currículo, histórico e automação de conteúdo.
---

# 📝 Plugin de Registro de Aula (`class_registry.py`)

Este documento detalha as funcionalidades e a lógica por trás do plugin `class_registry.py`, uma ferramenta essencial para automatizar e otimizar o processo de registro de diários de classe no SysAva. Ele integra diversas fontes de dados para sugerir e preencher automaticamente os campos do diário, garantindo consistência e agilidade.

## 🚀 Visão Geral

O `class_registry.py` atua como uma ponte entre a grade horária do professor, o currículo pedagógico (BNCC/EPT), o conteúdo das aulas (arquivos Markdown e banco de dados `lessons`) e o histórico oficial de registros do portal iSeduc (`historico_aulas`). Seu objetivo principal é minimizar o esforço manual no preenchimento do diário, sugerindo informações relevantes e alertando sobre inconsistências.

## ✨ Principais Funcionalidades

### 1. Integração com a Grade Horária (`grade_horaria.json` e `weekly_schedule`)

-   **Fonte de Dados**: O plugin carrega a grade horária da turma a partir do arquivo local `grade_horaria.json`. Caso este arquivo não exista ou esteja vazio, ele tenta sincronizar e baixar a grade do Supabase (tabela `weekly_schedule`).
-   **Seleção Dinâmica**: Com base na turma e data selecionadas, o plugin filtra e exibe apenas as disciplinas e horários previstos na grade para aquele dia.

### 2. Seleção Inteligente de Disciplinas (Anuais vs. Modulares)

Para cursos com estrutura modular (ex: Técnico em Desenvolvimento de Sistemas), o plugin diferencia disciplinas anuais de modulares:

-   **`Disc.Tec.` Handling**: Se a grade horária indica `Disc.Tec.`, o plugin entende que se trata de um slot para uma disciplina modular.
-   **Módulo Técnico Atual**: Um novo seletor é exibido, listando apenas as disciplinas marcadas como `duration_type = 'mensal'` na tabela `subjects` do banco de dados para a turma selecionada.
-   **Mapeamento de Nomes**: Utiliza `mapping_grade_to_db` para converter nomes abreviados da grade (ex: `P.C. II`) para os nomes completos das disciplinas no banco (`PENSAMENTO COMPUTACIONAL II`), garantindo a correta associação com o currículo e o conteúdo.

### 3. Cálculo do Número da Aula (`n_aula`) Baseado no Histórico Oficial

Esta é uma das funcionalidades mais críticas para a precisão do registro:

-   **Prioridade ao `historico_aulas`**: Em vez de contar aulas por data desde o início do ano (o que gerava a "Aula 114"), o plugin agora consulta a tabela `historico_aulas` do Supabase.
-   **Contagem de Registros**: O `n_aula` sugerido é `(total de registros oficiais para a disciplina + 1)`. Isso garante que o número da aula reflita o progresso real do registro no portal iSeduc.
-   **Alerta de Duplicidade**: Se já existir um registro oficial para a data e disciplina selecionadas no `historico_aulas`, um aviso é exibido para o professor.
-   **Fallback**: Em caso de falha na conexão com o banco de dados, o sistema retorna ao cálculo baseado em calendário (`calculate_lesson_number`) como um plano B.

### 4. Limite de Carga Horária (400h Anuais)

Para garantir a conformidade com a carga horária pedagógica:

-   **Cálculo Proporcional**: O limite máximo de aulas (`limit_lessons`) para uma disciplina é calculado dividindo a carga horária anual total (400 horas) pelo número de disciplinas cadastradas para a turma (`400 // num_subjects`).
-   **Teto de Aulas**: O `n_aula` sugerido nunca ultrapassará esse limite, evitando a sugestão de aulas inexistentes ou além do cronograma previsto.

### 5. Preenchimento Automático de Conteúdo (Smart-Fill)

O plugin tenta preencher o campo "Conteúdo Abordado" de forma inteligente:

-   **Catálogo Local (`data/Turmas`)**: Primeiro, ele busca um arquivo Markdown (`.md`) correspondente ao `n_aula` e à disciplina na estrutura de pastas `data/Turmas/{Turma}/{Disciplina}/SXX/Aula_XX.md`. Ele extrai o título e a introdução do arquivo.
-   **Banco de Dados (`lessons`)**: Se não encontrar localmente, ele consulta a tabela `lessons` do Supabase, buscando a aula pelo `subject_id` e `n_aula` no título. Ele extrai o título e a introdução da descrição da lição.
-   **Download de Conteúdo**: Se a aula for encontrada no banco de dados, um botão de download é disponibilizado para baixar o arquivo `.md` completo.
-   **Feedback**: Informa ao usuário se a aula foi encontrada localmente, no banco ou se não foi localizada.

### 6. Integração Curricular (BNCC/EPT)

-   **`curriculo_db.json`**: O plugin carrega dados de competências e habilidades do arquivo `curriculo_db.json`.
-   **Sugestão Automática**: Com base na disciplina selecionada, ele preenche os seletores de "Competência Específica" e "Habilidades", facilitando o alinhamento pedagógico.

### 7. Histórico de Registros

-   **Registros Manuais**: Uma aba exibe os registros de aula salvos localmente no `class_registries.json`.
-   **Portal iSeduc (Histórico)**: Outra aba exibe os últimos 50 registros oficiais da tabela `historico_aulas` do Supabase, permitindo ao professor auditar o que foi enviado pelo robô.

### 8. Persistência e Salvamento

-   **JSON Local**: Todos os registros de aula preenchidos são salvos no arquivo `class_registries.json` na pasta do plugin.
-   **Histórico de Usuário**: Opcionalmente, o registro pode ser adicionado ao histórico de atividades do usuário no banco de dados.

## 🛠️ Como Usar

1.  **Acesse o Plugin**: Navegue até a seção de Plugins no SysAva e selecione "Registro de Aula".
2.  **Selecione o Tipo de Aula**: Escolha entre "Aula Híbrida", "Aula Remota", "Aula Normal", "Reposição" ou "Aula Extra".
3.  **Selecione a Turma**: Escolha a turma desejada.
4.  **Selecione a Data**: Escolha a data da aula. O dia da semana será automaticamente identificado.
5.  **Selecione o Componente/Módulo**:
    -   Se for uma disciplina anual, ela aparecerá diretamente.
    -   Se for `Disc.Tec.`, um novo seletor "Módulo Técnico Atual" aparecerá para você escolher a disciplina modular correta.
    -   Um expander "Ajustar Início do Módulo" permite definir uma data de início específica para o módulo, resetando a contagem de aulas para ele.
6.  **Verifique o `n_aula`**: O número da aula será sugerido automaticamente com base no histórico do iSeduc.
7.  **Preenchimento Automático**: O "Objeto do Conhecimento" e o "Conteúdo Abordado" serão pré-preenchidos com base na disciplina e no `n_aula`.
8.  **Preencha os Detalhes**: Complete os campos de "Competência Específica", "Habilidades", "Habilidade Integrada", "Objetivo da Aprendizagem" e "Estratégia Metodológica".
9.  **Salve**: Clique em "Salvar e Avançar" para registrar a aula.
10. **Consulte Históricos**: Use as abas "Registros Manuais" e "Portal iSeduc (Histórico)" para revisar aulas anteriores.

## ⚠️ Considerações Importantes

-   **Conexão com o Banco**: Para o funcionamento ideal (cálculo de `n_aula` preciso, busca de `lessons`, histórico do iSeduc), a conexão com o Supabase é essencial.
-   **Estrutura de Pastas**: Mantenha a estrutura de pastas `data/Turmas/{Turma}/{Disciplina}/SXX/Aula_XX.md` para que o Smart-Fill de conteúdo funcione corretamente.
-   **Dados do Currículo**: O arquivo `curriculo_db.json` deve estar atualizado para que as sugestões de competências e habilidades sejam relevantes.
-   **`historico_aulas`**: A precisão do `n_aula` depende dos registros existentes na tabela `historico_aulas`. Certifique-se de que o robô de automação esteja funcionando corretamente.

Este plugin visa ser uma ferramenta poderosa para o professor, transformando o registro de aulas em um processo mais ágil e menos propenso a erros.