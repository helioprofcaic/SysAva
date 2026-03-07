# 🧅 Arquitetura da Aplicação (Modo Cebola)

Este documento descreve a arquitetura em camadas da aplicação, inspirada em princípios como a "Onion Architecture", para garantir o isolamento de responsabilidades e a manutenibilidade do código.

A estrutura separa a lógica em três camadas principais:

### 1. Camada de Apresentação (`views/`)
-   **Responsabilidade:** Controlar a interface do usuário (UI).
-   **Descrição:** Cada arquivo nesta pasta corresponde a uma página ou um componente visual principal da aplicação (ex: `forum.py`, `admin.py`). Estes arquivos são responsáveis por desenhar os botões, tabelas e formulários, e por chamar os serviços da camada de negócios quando uma ação é necessária. Eles não devem conter lógica de banco de dados direta.

### 2. Camada de Serviços/Negócios (`services/`)
-   **Responsabilidade:** Orquestrar a lógica de negócios da aplicação.
-   **Descrição:** Esta camada atua como intermediária. Por exemplo, o serviço `auth.py` contém a lógica de como a autenticação deve funcionar (criptografar, verificar senha). Ele usa a camada de dados para buscar ou salvar informações.

### 3. Camada de Dados (`services/database.py`)
-   **Responsabilidade:** Isolar todo o acesso ao banco de dados.
-   **Descrição:** Este é o único arquivo que tem permissão para "falar" com o Supabase. Ele expõe funções claras e diretas para as operações necessárias (ex: `get_user()`, `create_forum_post()`). Se um dia quisermos trocar o Supabase por outro banco, este é o único lugar que precisará ser modificado.

### Ponto de Entrada (`app.py`)
-   **Responsabilidade:** Atuar como o roteador principal da aplicação.
-   **Descrição:** O `app.py` é agora um arquivo enxuto. Sua principal função é verificar se o usuário está logado e, com base na navegação, chamar a função de renderização da página correta que está no diretório `views/`.