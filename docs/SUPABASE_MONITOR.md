# 📊 Monitor de Consumo e Tráfego do Supabase (Egress Monitor)

O **Monitor de Consumo do Supabase** é uma ferramenta complementar de auditoria desenvolvida em Streamlit para analisar e mitigar problemas de estouro de banda de saída (Egress) no plano gratuito de 5GB do Supabase.

---

## ⚡ O Problema: Streamlit Rerun Multiplier Effect

O Streamlit utiliza uma arquitetura baseada em reexecução completa (**Rerun**). Toda vez que um usuário interage com um botão, menu ou caixa de seleção, o arquivo do script é executado inteiramente de cima a baixo.

Se as consultas ao banco de dados Supabase forem feitas diretamente, sem caching ou trazendo dados em excesso (`select("*")`), cada clique do aluno na tela recarrega e baixa os dados novamente.
* **Tamanho do banco de dados completo (dados de texto):** ~3 MB.
* **Tráfego por aluno ativo:** Se ele navegar fazendo 20 cliques por dia sem otimização, ele baixa 3MB * 20 = **60MB/dia**.
* **Escala com mais alunos:** **50 alunos ativos** gerando esse tráfego por dia durante 30 dias gerará **90GB de tráfego/mês**! Isso estoura a cota gratuita de 5GB em poucos dias.

---

## ⚙️ Funcionalidades do Aplicativo

O Monitor é dividido em quatro seções principais:

### 1. 📊 Diagnóstico em Tempo Real
Conecta-se ao seu Supabase ao vivo e lista todas as tabelas utilizadas no SysAva (`lessons`, `forum_posts`, `historico_aulas`, etc.), calculando o número exato de linhas, estimando o tamanho médio dos registros em bytes, e o peso total da tabela no banco.

### 2. 🕵️ Auditor Automático de Código
Varre o arquivo `services/database.py` do projeto buscando consultas que usam o padrão ineficiente `.select("*")` em tabelas pesadas (como `lessons` e `forum_posts`), apontando em quais linhas estão e sugerindo códigos de otimização específicos para o seu projeto.

### 3. 💸 Simulador Interativo de Tráfego
Permite alterar dinamicamente em sliders a quantidade de alunos ativos diários, interações por usuário, e ver matematicamente como o uso do **Cache do Streamlit** e de **Consultas Parciais (Metadados)** reduz a banda de saída, mantendo as contas totalmente de graça e dentro do plano free do Supabase.

### 4. 🛠️ Guia Prático de Mitigação
Guia passo a passo com exemplos de código prontos para colar e resolver o problema no SysAva em minutos.

---

## 🛠️ Como Resolver o Estouro de Banda (3 Passos)

### Passo 1: Adicionar `@st.cache_data` nas consultas de leitura
O cache do Streamlit armazena os dados buscados na memória RAM do servidor. Se outros alunos acessarem o sistema em seguida, o Streamlit servirá os dados salvos em cache, **evitando fazer chamadas adicionais e gastar cota de saída do Supabase**.

```python
import streamlit as st

@st.cache_data(ttl=300) # Mantém em cache local por 5 minutos
def get_lessons():
    # Consulta ao Supabase
```

### Passo 2: Evitar `select("*")` em listagens pesadas
Sempre que for exibir uma lista de aulas ou posts do fórum, traga apenas as colunas necessárias para renderizar a lista (ID, título, data). Busque o conteúdo longo completo (`full_content` das aulas) apenas quando o aluno abrir especificamente aquela página de aula.

```python
# ❌ LENTO (Baixa todo o conteúdo de todas as aulas de uma vez):
supabase.table("lessons").select("*").eq("subject_id", id).execute()

# ✅ RÁPIDO (Baixa apenas 5% do peso, guardando banda):
supabase.table("lessons").select("id, title, week, subject_id").eq("subject_id", id).execute()
```

### Passo 3: Limitar/Paginar o Fórum
Com mais de 3.300 posts, carregar todos eles de uma vez em um clique consome muita banda. Limite a consulta para os posts mais recentes:

```python
supabase.table("forum_posts").select("*").order("created_at", desc=True).limit(50).execute()
```

---

## 🚀 Como Iniciar

### Opção 1: Via Painel de Controle (Painel Inicial)
Abra o arquivo `run.bat` na raiz do SysAva e escolha a **Opção [3]** no menu interativo.

### Opção 2: Comando Direto no Terminal
Com o ambiente virtual ativo, execute:
```bash
streamlit run apps/supabase_monitor/supabase_monitor_streamlit.py
```
