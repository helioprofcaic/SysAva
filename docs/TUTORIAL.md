# 📚 Tutorial: Plataforma de Ensino (SysAva) com Streamlit e Supabase

Este guia explica como configurar o ambiente, criar o banco de dados e colocar a aplicação no ar.

## 1. Configuração do Banco de Dados (Supabase)

Para que o **Fórum** funcione e as mensagens fiquem salvas, precisamos configurar o Supabase.

1.  Crie uma conta e um projeto em [supabase.com](https://supabase.com).
2.  No menu lateral, vá em **SQL Editor**.
3.  Abra o arquivo `docs/DATABASE_MODEL.md`, copie todo o conteúdo SQL e cole no editor do Supabase para criar todas as tabelas de uma vez.
4.  Após criar as tabelas, vá em **Project Settings** (ícone de engrenagem) > **API**.
5.  Anote os seguintes dados para os próximos passos:
    *   **Project URL**
    *   **anon public key**

---

## 2. Rodando Localmente (No seu computador)

### Instalação das Dependências
Certifique-se de ter o Python instalado. No terminal, execute:

```bash
pip install -r requirements.txt
```

### Configurando as Senhas (Secrets)
O Streamlit gerencia senhas de forma segura. Localmente, usamos um arquivo `.toml`.

1.  Crie uma pasta chamada `.streamlit` na raiz do projeto (se não existir).
2.  Dentro dela, crie um arquivo chamado `secrets.toml`.
3.  Adicione suas chaves do Supabase:

```toml
# .streamlit/secrets.toml
SUPABASE_URL = "Sua_URL_do_Supabase_Aqui"
SUPABASE_KEY = "Sua_Chave_Anon_Publica_Aqui"
```

### Executando o App
No terminal, rode:

```bash
streamlit run app.py
```

---

## 3. Deploy no Streamlit Cloud (Online)

Para disponibilizar o site para outras pessoas:

1.  Suba seu código para o **GitHub** (incluindo `app.py` e `requirements.txt`). **NÃO** suba o arquivo `secrets.toml`.
2.  Acesse share.streamlit.io e conecte seu repositório.
3.  Antes de clicar em "Deploy" (ou nas configurações do app após criado), vá em **Advanced Settings** ou **Secrets**.
4.  Cole o conteúdo das suas chaves lá:

```toml
SUPABASE_URL = "..."
SUPABASE_KEY = "..."
```

5.  Clique em **Save** e reinicie o app.

---

**Pronto!** Agora seu sistema de ensino tem persistência de dados no fórum.