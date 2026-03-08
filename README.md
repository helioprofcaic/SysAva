# 🎓 Plataforma de Ensino - SysAva

Este é um protótipo de uma Plataforma de Ensino (LMS - Learning Management System) desenvolvida com Streamlit e Supabase. O objetivo é criar um sistema modular e escalável para gerenciar o progresso de alunos através de aulas, quizzes e avaliações.

## ✨ Funcionalidades

-   **Autenticação de Usuários:** Sistema de login e registro com senhas criptografadas e persistência de sessão.
-   **Perfis de Usuário:** Distinção entre `aluno` e `admin` com permissões diferentes.
-   **Estrutura Acadêmica:**
    -   **Aulas:** Organizadas por turmas e disciplinas, com conteúdo em vídeo e resumos.
    -   **Fórum:** Espaço para discussões gerais ou por aula específica.
    -   **Quizzes:** Testes rápidos de conhecimento ao final de cada aula.
    -   **Avaliações:** Provas formais (MN1, MN2, MN3, RM) com questões objetivas e subjetivas (com envio de links).
-   **Sistema de Progressão:** Liberação automática de avaliações (MN1, MN2, MN3) baseada no histórico de atividades do aluno (aulas assistidas, quizzes realizados, etc.).
-   **Painel Administrativo Completo:**
    -   **Gerenciamento de Usuários:** Cadastro e exclusão de alunos e administradores.
    -   **Gerenciamento de Aulas:** Criação de aulas vinculadas a turmas e disciplinas.
    -   **Gerenciamento de Quizzes:** Criação de quizzes e questões para cada aula.
    -   **Gerenciamento de Avaliações:** Criação de provas (MN1, etc.), com banco de questões e importação de perguntas dos quizzes.
    -   **Correção de Provas:** Interface para o professor corrigir questões subjetivas, atribuir notas e exportar resultados em CSV.
    -   **Simulador de Aluno:** Ferramenta para popular o histórico de um aluno para testes e zerar seus dados antes do uso real.
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
│   └── seed_data.py      # Script para popular o banco de dados
├── services/             # Camada de Negócios e Dados
│   ├── __init__.py
│   ├── auth.py           # Lógica de autenticação (criptografia)
│   └── database.py       # Acesso centralizado ao banco de dados
├── .env                  # Credenciais para o script de seeding
├── app.py                # Ponto de entrada e roteador principal
└── requirements.txt      # Dependências do projeto
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