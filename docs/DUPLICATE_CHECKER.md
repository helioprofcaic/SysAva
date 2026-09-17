# 🔍 Verificador de Duplicatas Inteligente (Duplicate Checker)

O **Verificador de Duplicatas** é um aplicativo complementar construído em Streamlit para realizar auditorias e limpezas seguras na tabela `historico_aulas` do banco de dados Supabase do SysAva.

---

## 🛡️ Por que esta ferramenta é segura?

Diferente de scripts de limpeza automatizados genéricos, este aplicativo foi desenhado para garantir que **nenhum registro legítimo seja perdido**.

### 1. Critério de Duplicidade Real
O sistema agrupa e identifica duplicatas com base na restrição única real do banco de dados (`UNIQUE`):
* **Data da Aula (`data_aula`)**
* **Horário da Aula (`horario`)**
* **ID da Turma (`turma_id` ou nome da turma)**
* **ID da Disciplina (`disciplina_id` ou nome da disciplina)**

> **Aulas Seguidas:** Se uma matéria (como *POO* ou *IA*) tiver 3 aulas seguidas no mesmo dia, elas ocorrerão em **horários diferentes** (ex: *1º Horário*, *2º Horário*, *3º Horário*). Por terem horários distintos, elas **NÃO** serão agrupadas como duplicatas. O sistema as preserva integralmente.

### 2. Sempre Mantém um Registro Ativo
Para cada conjunto de registros duplicados idênticos (por exemplo, 3 registros exatamente para o mesmo horário, dia, turma e disciplina), o sistema **mantém 1 registro** e apenas propõe a exclusão dos outros 2 registros extras redundantes.

---

## ⚙️ Principais Funcionalidades

### 🏫 Filtros de Segurança Avançados
* **Filtro por Turma:** Permite focar a análise em apenas uma turma específica.
* **Filtro por Disciplina:** Permite que você filtre para auditar matérias críticas (como *POO* ou *IA*) de forma isolada.

### 🔧 Estratégias de Resolução (Barra Lateral)
Você pode escolher qual registro deseja manter ativo de cada grupo:
* **Manter o mais antigo (Recomendado):** Mantém o registro original de menor ID (criado primeiro) e remove as cópias mais novas.
* **Manter o mais recente:** Mantém o registro mais atual de maior ID e remove os anteriores.

### 📊 Painel de Pré-visualização Interativo
Ao executar a busca, os grupos de duplicatas são exibidos em cartões expansíveis. Dentro de cada grupo, você verá todos os registros e uma tabela dinâmica identificando claramente:
* **`✅ MANTER`** para o registro que será preservado.
* **`❌ APAGAR`** para os registros extras redundantes que serão removidos.

### 🗑️ Exclusão Controlada com Confirmação
O botão de exclusão permanente só se torna ativo após você marcar manualmente a caixa de seleção:
`"Eu revisei a lista de duplicatas acima e confirmo que desejo excluir os registros duplicados extras."`

---

## 🚀 Como Iniciar

### Opção 1: Via Painel de Controle (Painel Inicial)
Execute o arquivo `run.bat` na raiz do SysAva e escolha a **Opção [2]** no menu interativo.

### Opção 2: Comando Direto no Terminal
Com o ambiente virtual ativo, execute:
```bash
streamlit run apps/duplicate_checker/duplicate_checker_streamlit.py
```
