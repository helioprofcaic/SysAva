# 🎓 Plataforma de Ensino - SysAva

Este é um protótipo de uma Plataforma de Ensino (LMS - Learning Management System) desenvolvida com Streamlit e Supabase. O objetivo é criar um sistema modular e escalável para gerenciar aulas, fóruns, avaliações e usuários (alunos e administradores).

## ✨ Funcionalidades

-   **Autenticação de Usuários:** Sistema de login e registro com senhas criptografadas.
-   **Perfis de Usuário:** Distinção entre `aluno` e `admin` com permissões diferentes.
-   **Módulos de Ensino:**
    -   **Aulas:** Exibição de conteúdo em vídeo.
    -   **Fórum:** Espaço para discussões com moderação por administradores.
    -   **Quiz:** Testes rápidos de conhecimento.
    -   **Avaliações:** Painel de notas e desempenho.
-   **Painel Administrativo:** Visualização de todos os usuários cadastrados.
-   **Banco de Dados Persistente:** Utiliza o Supabase para armazenar todas as informações.

## 🧅 Arquitetura

O projeto segue uma arquitetura em camadas (inspirada na "Onion Architecture") para separar responsabilidades e facilitar a manutenção.

```
SysAva/
├── .streamlit/
│   └── secrets.toml      # Segredos para rodar localmente
├── data/
│   └── Turmas/
│       └── Escola.txt    # Dados brutos para popular o banco
├── docs/
│   ├── ARCHITECTURE.md   # Documentação da arquitetura
│   └── DATABASE_SETUP.md # Comandos SQL para o banco
├── views/                # Camada de Apresentação (UI)
│   ├── __init__.py
│   ├── admin.py
│   ├── aulas.py
│   ├── avaliacoes.py
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

1.  **Configure o Banco de Dados:** Siga as instruções em `docs/DATABASE_SETUP.md` para criar as tabelas no Supabase.
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