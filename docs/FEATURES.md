# ✨ Funcionalidades da Plataforma de Ensino

Este documento descreve as principais funcionalidades do sistema.

## Módulos Principais (Para Alunos)

-   **Login & Registro:** Sistema de autenticação seguro com senhas criptografadas. Novos alunos podem se cadastrar sozinhos.
-   **Aulas:** Área para visualização de conteúdo em vídeo, com um menu para navegar entre as aulas.
-   **Fórum:** Um espaço de discussão onde os alunos podem postar dúvidas e interagir. As mensagens são salvas permanentemente.
-   **Quiz:** Um questionário interativo para testar o conhecimento adquirido nas aulas.
-   **Avaliações:** Uma página para visualizar o desempenho, como notas e média geral.

## 🛡️ Funcionalidades Administrativas

O sistema possui um papel especial de **"Admin"** com privilégios elevados.

### Como se Tornar um Admin?
1.  Cadastre uma conta normalmente pelo aplicativo na página "Registre-se".
2.  Peça para alguém com acesso ao banco de dados (Supabase) para "promover" sua conta para o papel de `admin`. O comando SQL para isso está no arquivo `DATABASE_SETUP.md`.

### O que um Admin Pode Fazer?
-   **Painel Administrativo:** Acessar um menu exclusivo "Admin" na barra lateral para visualizar todos os usuários cadastrados no sistema.
-   **Moderar o Fórum:** Excluir qualquer mensagem postada no fórum clicando no ícone de lixeira (🗑️) que aparece ao lado do post.