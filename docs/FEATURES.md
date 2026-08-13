# Documentação de Funcionalidades Avançadas

Este documento detalha o funcionamento de recursos avançados do SysAva, como dashboards, gerenciamento de usuários e a página de Plugins.

## 👨‍🎓 Dashboard do Aluno

A home page do aluno exibe suas notas, progresso e atividades recentes.

### Seletor de Disciplina
- Filtro para visualizar progresso e notas de uma disciplina específica ou "Visão Geral (Todas)".

### Score do Aluno
- **Pontuação Total:** Soma de pontos de aulas, quizzes e fórum.
- **Aulas Vistas:** 1 ponto por aula visualizada.
- **Pontos em Quizzes:** Nota dos quizzes realizados.
- **Fórum por Aula:** 1 ponto por participação no fórum.

### Notas das Avaliações
- **Visualização por Disciplina:** Cada disciplina aparece como um expander com título: `"Nome Disciplina — 3/5 avaliadas"`.
- **Tabela de Notas:**
  - Tipo da avaliação (T1_N1, T1_N2, etc.)
  - Título da avaliação
  - Nota (ou "-" se pendente)
  - Status (Realizada / Pendente)
  - Data de submissão
- **Estatísticas:**
  - Média das notas
  - Melhor nota
  - Pior nota
- **Alertas:** Aviso quando há avaliações pendentes.

### Histórico de Atividades
- Lista cronológica de todas as ações realizadas na plataforma.

---

## 📊 Dashboard do Professor/Admin

O dashboard é a primeira tela exibida após o login para professores e administradores. Ele fornece uma visão completa da plataforma.

### Status da Plataforma
- **Métricas gerais:** Total de usuários, alunos, professores, turmas e disciplinas.
- **Atualização em tempo real:** Os dados são carregados a cada acesso.

### Conteúdo da Plataforma
- **Aulas e Quizzes:** Total de aulas, aulas com quiz, aulas sem quiz.
- **Barra de progresso:** Indicador visual da cobertura de quizzes.
- **Avaliações:** Total de provas, questões cadastradas, provas sem questões.

### Atividade Recente
- Últimas 10 ações realizadas por todos os usuários na plataforma.

### Ações Rápidas
- Atalhos para Gerenciar Avaliações, Conteúdo e Plugins.

### Consulta de Score Individual
- Busca de notas por turma, disciplina e aluno específico.

### Participação da Turma
- Gráfico de engajamento por aluno (aulas, quizzes, fórum).

---

## 👥 Gerenciamento de Usuários

A aba "Usuários" no painel administrativo oferece controle completo sobre as contas.

### Funcionalidades

1. **Cadastro de Usuários:**
   - Formulário para criar novos usuários com nome, login, RA, senha e função.

2. **Filtros:**
   - Filtrar por função: Todos, Alunos, Professores, Administradores.
   - Filtrar por turma (quando "Alunos" está selecionado).

3. **Visualização Agrupada (Alunos):**
   - Quando "Todas as Turmas" está selecionado, os alunos são exibidos **agrupados por turma** em expanders.
   - Cada turma mostra a quantidade de alunos entre parênteses.

4. **Controle de Contas:**
   - **Ativar/Desativar:** Botão para desativar contas sem excluí-las. Contas desativadas podem ser reativadas posteriormente.
   - **Excluir:** Remoção permanente da conta (com confirmação implícita).
   - **Proteção:** O usuário atual não pode excluir ou desativar a própria conta.

5. **Coluna de Status:**
   - Indica se a conta está "Ativa" ou "Inativa".

### Migracao do Banco

Para usar a funcionalidade de ativar/desativar, execute no SQL Editor do Supabase:

```sql
ALTER TABLE public.app_users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true;
NOTIFY pgrst, 'reload schema';
```

---

## ⚙️ Configuração de Disciplinas (Carga Horária)

Na aba "Turmas" do painel administrativo, é possível configurar a carga horária de cada disciplina.

### Opções Disponíveis

| Carga Horária | `duration_type` | Aulas/Semana | Uso Recomendado |
|---------------|-----------------|--------------|-----------------|
| **40h** | `mensal` | 8 aulas | Disciplinas modulares, optativas |
| **80h** | `anual` | 10 aulas | Disciplinas obrigatórias, anuais |

### Como Configurar

1. Acesse **Admin > Configurações de Conteúdos > Turmas**.
2. Selecione a turma desejada.
3. Na seção "Configuração das Disciplinas":
   - Use o seletor "Carga Horária" para escolher entre 40h ou 80h.
   - Ative/desative disciplinas conforme necessário.
4. Clique em "Salvar Configurações".

### Impacto

- A carga horária afeta o escopo de importação de questões para avaliações.
- Disciplinas 40h são tratadas como modulares (mensais).
- Disciplinas 80h são tratadas como anuais.

---

## 🧩 Página de Plugins

A página de "Plugins", acessível no menu lateral para **Administradores** e **Professores**, é um centro para estender as funcionalidades do SysAva. Ela é dividida em duas seções principais:

### 1. Plugins Nativos

Esta aba contém funcionalidades interativas que já vêm integradas à interface do SysAva.

#### 📚 Leitor de E-books (PDF)
- **O que faz:** Permite visualizar arquivos PDF diretamente na plataforma.
- **Como usar:** O sistema busca automaticamente por arquivos `.pdf` nos seguintes locais:
  - `data/repo/ebooks/` (para e-books gerais)
  - `data/Turmas/` (em qualquer subpasta, permitindo associar PDFs a turmas ou disciplinas específicas)
- **Requisito:** A biblioteca `streamlit-pdf-viewer` precisa estar instalada (`pip install streamlit-pdf-viewer`).

#### 🎓 Gerador de Certificados
- **O que faz:** Apresenta uma interface de exemplo para a geração de certificados de conclusão para os alunos.

### 2. Plugins Externos

Esta aba permite executar scripts Python (`.py`) para realizar tarefas de backend, como manutenção, relatórios e análises.

- **Localização:** Os scripts devem ser colocados na pasta `data/repo/plugins/`.
- **Execução:** A interface lista os scripts encontrados. Ao clicar em "Executar", o script é rodado em um processo separado e sua saída (qualquer `print`) é exibida na tela.
- **⚠️ Segurança:** Execute apenas scripts de fontes confiáveis, pois eles têm acesso ao ambiente do servidor e ao banco de dados.

#### Exemplos de Plugins Externos:
- **`audit_backup.py`**: Realiza uma contagem de registros nas tabelas principais e cria um backup do banco de dados em um arquivo SQLite na mesma pasta.
- **`friction_radar.py`**: Analisa as disciplinas em busca de "pontos de fricção" (aulas sem quiz, baixo engajamento, etc.) e gera um relatório.
- **`focus_report.py`**: Gera um relatório de todas as vezes que os alunos saíram da tela durante uma avaliação.
- **`student_scores.py`**: Permite gerenciar as notas gerais dos alunos e adicionar pontos qualitativos diários.

---

## 🚀 Treinamentos (Disciplinas Flutuantes)

O recurso de "Treinamentos" permite criar disciplinas especiais que não pertencem a uma única turma, mas podem ser vinculadas a várias delas. É ideal para preparatórios, olimpíadas, nivelamento e revisões.

### Como Funciona

1.  **Criação:**
    - Vá para a página **Admin** e acesse a aba **"🚀 Treinamentos"**.
    - Use o formulário "Criar Novo Treinamento/Olimpíada" para criar a disciplina flutuante. No banco de dados, ela será uma `subject` com `type = 'training'`.

2.  **Vínculo com Turmas:**
    - Após criar o treinamento, selecione-o na lista.
    - Use a caixa de seleção múltipla para escolher todas as turmas que devem ter acesso a este treinamento.
    - Os alunos das turmas vinculadas verão o treinamento em sua lista de disciplinas.

3.  **Adicionar Aulas:**
    Existem duas maneiras de popular as aulas de um treinamento:

    - **Via Interface:** Na mesma aba "Treinamentos", use o formulário "Adicionar Nova Aula" para criar aulas individualmente.

    - **Em Lote (com `seed_lessons.py`):** Para adicionar muitas aulas de uma vez, você pode usar o script de importação. Para que ele reconheça o treinamento, siga a estrutura de pastas abaixo:

      ```
      data/
      └── Turmas/
          └── Nome Exato do Treinamento/
              ├── Nome Exato do Treinamento/  (Repita o nome aqui)
              │   └── S01/
              │       ├── aula_01.md
              │       └── aula_02.md
              └── logs.txt
      ```

      **Por que a pasta é repetida?**
      Essa estrutura `Treinamento/Treinamento/Semana` foi projetada para ser compatível com a ferramenta **"🤖 Gerador de Aulas"**, que espera o formato `Turma/Disciplina/Semana`. Dessa forma, você pode usar o gerador de aulas com IA para criar o conteúdo do seu treinamento de forma automatizada. O script `seed_lessons.py` foi ajustado para entender essa estrutura e importar as aulas para a disciplina flutuante correta.
