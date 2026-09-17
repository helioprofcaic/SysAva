# 🗂️ Registro de Issues Locais — SysAva

Documento de acompanhamento **local** das correções e melhorias feitas no projeto.
Serve para não perder o fio das alterações entre sessões de manutenção.

**Regra:** toda alteração relevante deve virar uma entrada aqui (com ID, status,
arquivos afetados e como validar). Agentes devem atualizar este arquivo ao
concluir uma tarefa.

## Convenções

| Símbolo | Significado |
| ------- | ----------- |
| 🔴 | Aberto |
| 🟡 | Em andamento |
| 🟢 | Resolvido |
| ⚪ | Backlog / ideia |

Formato de ID: `IS-NNN`.

---

## Índice

| ID | Título | Status | Data |
| -- | ------ | ------ | ---- |
| IS-001 | Plugin de Atividades — dataset de pontuação por atividades | 🟢 | 2026-09-17 |
| IS-002 | Quizzes marcados como respondidos sem responder | 🟢 | 2026-09-17 |
| IS-003 | Egress do Supabase estourando a cota de 5 GB | 🟢 | 2026-09-17 |
| IS-004 | Lentidão no dataframe do plugin de qualitativo | 🟢 | 2026-09-17 |
| IS-005 | Configurar cache no Streamlit Cloud | ⚪ | 2026-09-17 |
| IS-006 | Cachear avaliações/submissões (admin) | ⚪ | 2026-09-17 |

---

## IS-001 — Plugin de Atividades: dataset de pontuação por atividades 🟢

**Pedido:** visualizar a pontuação distribuída por atividades no plugin de
qualitativo (aba **Atividades**).

**Solução:** nova seção **📊 Pontuação Distribuída por Atividades**, detalhada
por lançamento (`Data`, `Estudante`, `Aula`, `Bloco`, `Pontos`), filtro por bloco
(1-20 / 21-40) e métricas de total distribuído e nº de lançamentos. Filtra pela
disciplina selecionada na sidebar; entradas antigas sem `subject_id` são
inferidas pela aula.

**Arquivos:** `data/repo/plugins/daily_activities.py`

**Validar:** abrir Plugins → Atividades, escolher turma/disciplina e conferir a
tabela abaixo do botão de salvar.

---

## IS-002 — Quizzes marcados como respondidos sem responder 🟢

**Sintoma:** alunos relataram quizzes aparecendo como "Concluída" (círculo
verde) sem terem respondido; tentativas e nota compartilhadas entre aulas.

**Causa raiz:** o gerador criava todos os quizzes com o **mesmo título
genérico** (`📝 Quiz: Teste seu Conhecimento!`) e o sistema identificava a
conclusão/tentativa **pelo título**. Responder um quiz marcava vários outros.

**Evidência:** 378 quizzes com apenas 164 títulos distintos; 93x o título
genérico; na disciplina `FUNDAMENTOS DE UI / UX OU IHC`, 17 de 17 quizzes com o
mesmo título.

**Solução:**
- `services/quiz_parser.py`: título único `Quiz: {título da aula}` e remoção dos
  quizzes anteriores da aula antes de recriar (fim das duplicatas).
- `views/quiz.py`: grava `| quiz_id:X` no histórico e filtra tentativas por ID.
- `views/aulas.py`: conclusão por `quiz_id` (títulos genéricos antigos ignorados).
- `services/database.py`: `get_student_score` e `get_user_progress_stats`
  deduplicam por `quiz_id`.

**Migração/limpeza executada:**
- `scripts/migrate_quiz_titles.py --apply` → 336 quizzes renomeados, 68
  duplicatas removidas.
- `scripts/reset_quiz_attempts.py --apply` → 2666 tentativas remapeadas com
  `quiz_id` (notas preservadas), 364 ambíguas/genéricas removidas.

**Arquivos:** `services/quiz_parser.py`, `views/quiz.py`, `views/aulas.py`,
`services/database.py`, `scripts/migrate_quiz_titles.py`,
`scripts/reset_quiz_attempts.py`

**Validar:** abrir uma aula, responder o quiz e confirmar que apenas aquela aula
fica verde; conferir tentativas em `views/quiz.py`.

---

## IS-003 — Egress do Supabase estourando a cota de 5 GB 🟢

**Sintoma:** consumo mensal de saída de banda acima do limite do plano gratuito.

**Diagnóstico:** não é conteúdo grande — 344 aulas somam ~1,6 MB de
`full_content` e **não há Base64**. O problema é **volume de queries repetidas**
a cada rerun do Streamlit e laços N+1 por aluno.

**Solução:**
- `services/local_cache.py`: cache SQLite **ligado por padrão** (opt-out via
  `DISABLE_LOCAL_CACHE = true` / `ENABLE_LOCAL_CACHE = false`). Fallback seguro
  se o disco não for gravável.
- `services/database.py`: cache + invalidação nas consultas quentes:
  `get_user_history` (120s), `get_student_score` (120s),
  `get_user_enrollment` (1h), `get_user_forum_lessons_by_subject` (5min),
  `get_lesson_by_id` (1h), `get_quiz_for_lesson`/`get_quiz_by_id`/
  `get_quiz_questions`/`get_quizzes_for_subject`/`get_all_quizzes_summary` (1h),
  `get_school` (6h).
- `get_all_users` deixou de baixar o **hash de senha**.
- `_compute_student_score` usa `get_all_quizzes_summary()` (cacheado) em vez de
  consultar quizzes a cada chamada.

**Arquivos:** `services/local_cache.py`, `services/database.py`

**Validar:** `python -c "from services import local_cache as lc; print(lc.cache_enabled())"`
deve imprimir `True`; acompanhar o egress no app **Supabase Monitor**.

---

## IS-004 — Lentidão no dataframe do plugin de qualitativo 🟢

**Sintoma:** demora para exibir a tabela de pontos (uma consulta de score por
aluno).

**Solução:**
- `services/local_cache.py`: nova tabela `_score_cache` + `get_scores_bulk`,
  `set_scores_bulk`, `invalidate_scores` (TTL 600s).
- `data/repo/plugins/daily_activities.py`: `get_scores_for_students()` carrega a
  turma em lote (cache antes do Supabase) e botão **🔄 Atualizar notas**.

**Arquivos:** `services/local_cache.py`,
`data/repo/plugins/daily_activities.py`

**Validar:** abrir a aba Atividades; a segunda carga não deve consultar o
Supabase (3 alunos: 3 queries → 0 na recarga).

---

## IS-005 — Configurar cache no Streamlit Cloud ⚪

O cache agora é **ligado por padrão**, então o Cloud já se beneficia. Se for
necessário desligar em algum ambiente, definir nos secrets:

```toml
DISABLE_LOCAL_CACHE = true
```

**Pendente:** decidir se o Cloud deve usar TTLs maiores para economizar ainda
mais, ou menores para dados mais frescos.

---

## IS-006 — Cachear avaliações/submissões (admin) ⚪

`get_assessments_by_subject`, `get_assessment_questions`,
`get_submission_answers` e afins ainda não têm cache. São usados
principalmente em telas de admin/avaliação. Avaliar custo/benefício.

---

## Comandos úteis

```powershell
# Migração de títulos de quiz (simulação / aplicar)
python scripts/migrate_quiz_titles.py
python scripts/migrate_quiz_titles.py --apply

# Reset seletivo de tentativas (simulação / aplicar)
python scripts/reset_quiz_attempts.py
python scripts/reset_quiz_attempts.py --apply

# Verificar se o cache local está ligado
python -c "from services import local_cache as lc; print(lc.cache_enabled())"
```

## Histórico de commits relacionados

| Commit | Descrição |
| ------ | --------- |
| `55e94f1` | Corrige quizzes com títulos duplicados e conclusão cruzada |
| `3e365c5` | Cache SQLite de scores no plugin de atividades diárias |
| `0393486` | Reduz egress do Supabase com cache local e documenta issues |
