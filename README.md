# 🎓 Plataforma de Ensino - SysAva

Este é um protótipo de uma Plataforma de Ensino (LMS - Learning Management System) desenvolvida com Streamlit e Supabase. O objetivo é criar um sistema modular e escalável para gerenciar o progresso de alunos através de aulas, quizzes e avaliações.

## ✨ Funcionalidades

-   **Autenticação de Usuários:** Sistema de login e registro com senhas criptografadas e persistência de sessão.
-   **Perfis de Usuário:** Distinção entre `aluno`, `professor` e `admin` com permissões diferentes.
-   **Estrutura Acadêmica:**
    -   **Aulas:** Organizadas por turmas e disciplinas, com conteúdo em vídeo e resumos.
    -   **Fórum:** Espaço para discussões gerais ou por aula específica.
    -   **Quizzes:** Testes rápidos de conhecimento ao final de cada aula.
    -   **Avaliações:** Provas formais (MN1, MN2, MN3, RM) com questões objetivas e subjetivas (com envio de links).
-   **Sistema de Progressão:** Liberação automática de avaliações (MN1, MN2, MN3) baseada no histórico de atividades do aluno (aulas assistidas, quizzes realizados, etc.).
-   **Dashboard do Aluno:**
    -   **Notas das Avaliações:** Visualização completa das notas por disciplina, com status (realizada/pendente) e estatísticas (média, melhor/pior nota).
    -   **Score Geral:** Pontuação total baseada em aulas, quizzes e participação no fórum.
    -   **Histórico de Atividades:** Lista cronológica de todas as ações realizadas na plataforma.
-   **Dashboard do Professor/Admin:**
    -   **Central de Comando:** Métricas da plataforma em tempo real (usuários, turmas, disciplinas, conteúdo).
    -   **Conteúdo da Plataforma:** Visão geral de aulas, quizzes e avaliações com indicadores de cobertura.
    -   **Atividade Recente:** Últimas ações dos usuários na plataforma.
    -   **Consulta de Score Individual:** Busca detalhada de notas por aluno, turma e disciplina.
    -   **Participação da Turma:** Gráfico de engajamento por aluno.
-   **Painel Administrativo Completo:**
    -   **Setup Guiado:** Interface para configuração inicial do banco de dados, criação de tabelas e importação de estrutura escolar sem necessidade de código.
    -   **Gerenciamento de Usuários:**
        -   Cadastro, exclusão e ativação/desativação de contas.
        -   Visualização agrupada por turma para alunos.
        -   Filtros por função (aluno, professor, administrador) e turma.
    -   **Gerenciamento de Disciplinas:**
        -   Configuração de carga horária (40h/80h) por disciplina.
        -   Ativação/desativação de disciplinas por turma.
        -   Isolamento de disciplinas (clonagem de matriz).
    -   **Gerenciamento de Aulas:** Criação de aulas vinculadas a turmas e disciplinas.
    -   **Gerador de Aulas com IA:** Integração com Google Gemini para ler cronogramas e gerar conteúdo de aulas, quizzes e planos de ensino automaticamente.
    -   **Extração Otimizada de PDFs:** Sistema avançado de extração de texto de PDFs com formatação otimizada para modelos de IA.
    -   **Gerenciamento de Quizzes:** Criação de quizzes e questões para cada aula.
    -   **Gerenciamento de Avaliações:** Criação de provas (MN1, etc.), com banco de questões e importação de perguntas dos quizzes.
    -   **Correção de Provas:** Interface para o professor corrigir questões subjetivas, atribuir notas e exportar resultados em CSV.
    -   **Simulador de Aluno:** Ferramenta para popular o histórico de um aluno para testes e zerar seus dados antes do uso real.
    -   **Auditoria de Questões:** Verificação automática de problemas em questões de quizzes e avaliações.
    -   **Revisor de Gabaritos:** Interface para revisar e corrigir gabaritos rapidamente.
-   **Treinamentos:** Disciplinas flutuantes que podem ser vinculadas a múltiplas turmas (ideal para olimpíadas e preparatórios).
-   **Banco de Dados Persistente:** Utiliza o Supabase para armazenar todas as informações.

## 🧅 Arquitetura

O projeto segue uma arquitetura em camadas (inspirada na "Onion Architecture") para separar responsabilidades e facilitar a manutenção.

```text
SysAva/
├── .streamlit/
│   └── secrets.toml      # Segredos para rodar localmente
├── data/
│   └── Turmas/
│       └── Escola.txt    # Dados brutos para popular o banco (seeding)
├── docs/
│   ├── ARCHITECTURE.md   # Documentação da arquitetura
│   └── DATABASE_MODEL.md # Comandos SQL para o banco
├── views/                # Camada de Apresentação (UI)
│   ├── __init__.py
│   ├── admin.py
│   ├── aulas.py
│   ├── avaliacoes.py
│   ├── home.py
│   ├── forum.py
│   ├── login.py
│   ├── quiz.py
│   └── register.py
├── scripts/              # Scripts utilitários
│   ├── seed_data.py      # Script para popular o banco de dados
│   ├── test_pdf_extraction.py  # Testes de extração de PDF
│   └── demo_pdf_improvements.py # Demonistração das melhorias
├── services/             # Camada de Negócios e Dados
│   ├── __init__.py
│   ├── auth.py           # Lógica de autenticação (criptografia)
│   ├── database.py       # Acesso centralizado ao banco de dados
│   ├── pdf_extractor.py  # Extrator otimizado de PDFs para IA
│   └── contexto_aulas.py # Gerenciamento de contexto para aulas
├── .env                  # Credenciais para o script de seeding
├── commits.ps1           # Utilitário interativo para Git
├── app.py                # Ponto de entrada e roteador principal
└── requirements.txt      # Dependências do projeto
```

## 📄 Extração Otimizada de PDFs

O sistema possui um módulo avançado de extração de texto de PDFs, otimizado para uso com modelos de IA:

### Melhorias Implementadas

1. **Extração Precisa**: Utiliza `pdfplumber` para extração precisa de texto, superando as limitações do `pypdf` padrão.

2. **Preservação de Estrutura**: Mantém a hierarquia do documento com cabeçalhos, seções e listas formatados em Markdown.

3. **Detecção de Tabelas**: Identifica e formata tabelas automaticamente, preservando sua estrutura para melhor compreensão pela IA.

4. **Limpeza de Texto**: Remove artefatos de formatação, corrige problemas de encoding e normaliza espaços em branco.

5. **Metadados**: Extrai informações importantes como título, autor, número de páginas e produtor do PDF.

6. **Resumo Estruturado**: Gera um resumo automático do conteúdo, facilitando a navegação para o modelo de IA.

### Uso

```python
# Extração básica
from services.pdf_extractor import extract_pdf_text

text = extract_pdf_text("documento.pdf")

# Extração com metadados
from services.pdf_extractor import PDFExtractor

extractor = PDFExtractor()
content = extractor.extract_from_file("documento.pdf")
formatted = extractor.format_for_ai(content)
```

### Resultados

- **+35% mais conteúdo extraído** em comparação com o método anterior
- **Tabelas detectadas** e formatadas em Markdown
- **Texto mais legível** para modelos de IA
- **Metadados preservados** para melhor contexto

Para testar as melhorias, execute:
```bash
python scripts/demo_pdf_improvements.py
```

## 🚀 Como Executar

1.  **Configure o Banco de Dados:** Siga as instruções em `docs/DATABASE_MODEL.md` para criar as tabelas no Supabase.
2.  **Instale as Dependências:** `pip install -r requirements.txt`
3.  **Configure as Credenciais:**
    -   Crie o arquivo `.streamlit/secrets.toml` para o app Streamlit.
    -   Crie o arquivo `.env` para o script de `seed`.
4.  **Popule o Banco (Opcional):** `python scripts/seed_data.py`
5.  **Execute a Aplicação (Modo Desenvolvimento):** No Windows, simplesmente execute o arquivo `run.bat`. Ele cuidará da criação do ambiente virtual, instalação de dependências, população do banco e inicialização do app.

## 📦 Gerando um Executável Standalone

Para criar uma versão "standalone" do aplicativo (um arquivo `.exe` que pode ser distribuído), você pode usar o script PowerShell `setup.ps1`.

1.  Abra um terminal PowerShell.
2.  (Primeira vez) Permita a execução de scripts: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
3.  Navegue até a pasta do projeto e execute: `.\setup.ps1`

O script irá criar uma pasta `dist/SysAva` contendo o executável e todos os arquivos necessários. Siga as instruções no final do processo de build para copiar os arquivos de configuração (`.env` e `.streamlit/`) para a pasta de destino antes de executar.

## ☁️ Deploy e Privacidade

Este projeto foi desenhado para ser "forkado". Se você é um professor e deseja usar o SysAva:

1.  Faça um **Fork** deste repositório no GitHub.
2.  Crie seu próprio projeto no **Supabase** (para ter seu próprio banco de dados).
3.  Faça o deploy do seu repositório no **Streamlit Cloud**.
4.  Ao acessar seu novo link pela primeira vez, vá na aba **Admin > Configuração** e insira suas credenciais do Supabase.

Isso garante que os dados dos seus alunos fiquem isolados e sob seu controle.