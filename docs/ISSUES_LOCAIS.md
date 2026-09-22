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
| IS-007 | Quizzes feitos não contabilizados no score (regressão do IS-002) | 🟢 | 2026-09-17 |
| IS-008 | Lista negra de faltosos inicia a chamada como "Falta" (Frequência) | 🟢 | 2026-09-17 |
| IS-009 | Base64/SVG inflando aulas — backup limpo e migração para novo banco | 🟢 | 2026-09-22 |
| IS-010 | Auditoria e limpeza de duplicatas de bot no fórum | 🟢 | 2026-09-22 |

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

## IS-007 — Quizzes feitos não contabilizados no score 🟢

**Sintoma:** aluna com vários quizzes respondidos aparecia com **Quizzes = 0**
no painel do professor (ex.: `MARIA CRYSTHIELY DA SILVA`, disciplina 8).

**Causa:** o app em execução ainda usava o código antigo (sem `| quiz_id:`).
As tentativas foram gravadas com o **título novo** (já renomeado pela migração),
mas **sem `quiz_id`**. Como o IS-002 passou a exigir `quiz_id` no
`get_student_score`, esses pontos zeraram.

**Solução:** em `_compute_student_score` e `get_user_progress_stats`, quando o
log não tem `quiz_id`, resolve-se o quiz pelo **título** (que agora é único por
aula) via mapa `quiz_title_to_id`. Assim a tentativa antiga e a nova caem na
mesma chave `id:X` — não perde ponto nem conta em dobro.

**Arquivos:** `services/database.py`

**Validar:**
```powershell
python -c "from services import database as db; print(db.get_student_score('73166069283', filter_subject_id=8))"
```
Deve retornar `quiz` > 0 (no caso, 41).

---

## IS-008 — Lista negra de faltosos inicia a chamada como "Falta" 🟢

**Pedido:** no plugin **Frequência**, os alunos da lista negra de faltosos devem
já aparecer com status **Falta** (em vez do padrão "Presente").

**Solução:** `student_attendance.py` lê `data/excecoes_alunos.json`
(`blacklist` de RAs + `blacklist_names`, com nomes normalizados) e usa "Falta"
como status inicial desses alunos. Mostra um aviso com os nomes encontrados na
turma. Valores já salvos **não** são sobrescritos.

**Arquivos:** `data/repo/plugins/student_attendance.py`

**Validar:** Plugins → Frequência → turma `2ª SÉRIE - Turma I-B (Técnico DS)`:
`GUSTAVO RAFAEL FRIGERI`, `ISADORA FERNANDA DA SILVA`, `LÁZARO DE SOUSA SILVA`
e `JANAYRA SOARES BRANDÃO` devem iniciar como **Falta**.

**Observação:** `data/excecoes_alunos.json` está no `.gitignore` (é local). Se o
arquivo não existir, a lista fica vazia e o comportamento volta ao padrão
(todos "Presente").

---

## IS-009 — Base64/SVG inflando aulas — backup limpo e migração para novo banco 🟢

**Sintoma:** o Supabase restringiu o serviço (`Services restricted` — organização
estourou a cota). O app quebrava com `pydantic ValidationError` do `postgrest`
(que mascara a mensagem real `{"message": ...}`).

**Causa raiz:** `services/pdf_extractor.py::convert_markdown_images_to_svg`
embutia imagens em **Base64** (`<image href="data:image/...;base64,...">`) dentro
de `lessons.description`, e `views/aulas.py::clean_svg_content` re-embutia Base64
tanto na renderização quanto **antes de gravar** (`views/admin.py`,
`views/gerador_aulas.py`). O cache do Supabase confirmou: 37 blocos Base64 em
`lessons`, ~1 MB de texto inflado (linha de descrição chegava a 237 KB).

**Solução:**
- `services/pdf_extractor.py`: nova barreira `strip_base64_images()` (remove só o
  Base64, **preserva SVG vetorial puro** e links locais). O
  `convert_markdown_images_to_svg` deixou de codificar raster em Base64 — imagens
  viram link para o arquivo local (padrão do AGENTS.md).
- `views/aulas.py`: `clean_svg_content` agora remove Base64 em vez de re-embutir.
- `views/gerador_aulas.py` / `views/admin.py`: barreira final antes de salvar.
- `services/database.py`: `_sanitize_text()` aplicado em `create_lesson`,
  `upsert_lesson`, `update_lesson_plan_fields` e `add_forum_post` (choke point).
- `scripts/backup_clean.py`: backup limpo a partir de `data/escola_ativa.db`
  (SQLite + JSONL + manifesto), removendo Base64.
- `docs/NOVO_BANCO_SCHEMA.sql`: DDL idempotente do novo projeto Supabase
  (modelo canônico + tabelas de automação + funções de resolução de disciplinas).
- `scripts/restore_new_supabase.py`: restaura o backup limpo no novo projeto.

**Evidência:** backup gerado em `data/backup_clean_2026-09-22_0757/` — 37 blocos
Base64 removidos, ~1,01 MB de Base64 eliminados; `description` máxima caiu de
237 KB para 20,7 KB; 60 linhas com SVG vetorial preservadas; 0 Base64 restante.

**Auditoria e redução (ver `docs/AUDITORIA_BANCO.md`):** o portal usa o Supabase
(21 tabelas) e a automação usa o SQLite `escola_ativa.db` (34 tabelas). As 13
tabelas de automação **não** vão para o novo Supabase; as vazias/abandonadas
(`qualitative_points`, `grade_milestones`, `user_reminders`, `user_profiles`) e a
inexistente `student_scores` não serão recriadas. O novo projeto nasce com 21
tabelas (25.228 linhas no restore). Consolidações de config/plugins ficam para
depois da migração.

**Arquivos:** `services/pdf_extractor.py`, `services/database.py`,
`views/aulas.py`, `views/gerador_aulas.py`, `views/admin.py`,
`views/home.py`, `views/quiz.py`,
`scripts/backup_clean.py`, `scripts/prepare_restore.py`,
`scripts/restore_new_supabase.py`,
`docs/NOVO_BANCO_SCHEMA.sql`, `docs/AUDITORIA_BANCO.md`

**Migração concluída (2026-09-22):** novo projeto Supabase com as 21 tabelas
essenciais; 24.087 linhas restauradas e sequências reajustadas. Verificação
origem × Supabase: **21/21 tabelas com contagem idêntica**. Cache local limpo e
smoke test do portal OK (2 turmas, 16 disciplinas, 364 aulas, sem Base64).

Tratamentos aplicados na preparação (`scripts/prepare_restore.py`):
- `historico_aulas.data_aula` mantido em `dd/mm/aaaa` (o Supabase guarda como
  TEXTO, igual ao bot do iSeduc). No projeto novo, ajustar o tipo com
  `ALTER TABLE public.historico_aulas ALTER COLUMN data_aula TYPE text USING to_char(data_aula,'DD/MM/YYYY');`
- `attendance`: 107 linhas de teste corrompidas removidas + 835 duplicatas
  idênticas; 1 `student_number` fora do INTEGER normalizado.
- Duplicatas removidas respeitando as UNIQUE: `historico_aulas` 167,
  `weekly_schedule` 20, `assessments` 11 (PK).
- 1 aula de teste com `id` UUID removida; 214 ids nulos preenchidos.
- **Pós-migração:** o Supabase devolve `timestamptz` misturando com e sem
  microssegundos; `pd.to_datetime` estourava em `views/home.py` e `views/quiz.py`.
  Corrigido com `format='ISO8601', errors='coerce'`.
- **Pós-migração:** `get_user` deixou de estourar quando o banco falha (ex.: cota
  ou secret incorreta no Cloud): o fallback agora é protegido, registra o erro no
  log e retorna `None` (login mostra "usuário ou senha incorretos" em vez de
  traceback).

**Observação:** o `historico_aulas` local tinha 566 linhas contra 1.234 no
Supabase antigo (inacessível durante o bloqueio) — a diferença não pôde ser
recuperada.

**Validar:**
```powershell
python scripts/backup_clean.py
python scripts/prepare_restore.py
python scripts/restore_new_supabase.py --dry-run
```

---

## IS-010 — Auditoria e limpeza de duplicatas de bot no fórum 🟢

**Sintoma:** o EduBot/SysAva Bot aparecia com mensagens repetidas nos fóruns,
aumentando o fluxo de dados.

**Diagnóstico:** posts de bot eram republicados a cada ação:
- `views/gerador_aulas.py` postava o desafio do EduBot **toda vez** que a aula era
  salva/gerada/replicada (sem checar se já existia).
- `scripts/seed_lessons.py` postava o SysAva Bot a cada execução (não idempotente).

**Evidência:** 243 posts de bot; 27 grupos duplicados (mesmo texto na mesma aula),
29 cópias extras (~14,5 KB). Ex.: `SysAva Bot` 3× na aula 273; `EduBot 🤖` 2–3× em
27 aulas.

**Solução:**
- `services/database.py`: novo `has_bot_post(lesson_id, bot_name)`.
- `views/gerador_aulas.py`: só posta o desafio se a aula ainda não tiver post do
  EduBot (2 pontos: geração e replicação).
- `scripts/seed_lessons.py`: pula o post do SysAva Bot se já existir.
- `scripts/cleanup_forum_duplicates.py`: remove duplicatas (dry-run por padrão;
  `--apply` para remover). Só mexe em posts de bot.

**Resultado:** 29 posts removidos; 243 → 214 posts de bot, 0 duplicatas.

**Arquivos:** `services/database.py`, `views/gerador_aulas.py`,
`scripts/seed_lessons.py`, `scripts/cleanup_forum_duplicates.py`

**Validar:**
```powershell
python scripts/cleanup_forum_duplicates.py          # deve mostrar 0 a remover
```

**Nota (backlog):** o Fórum Geral (`get_forum_posts()` sem aula) ainda baixa
**todos** os posts (~1 MB) com cache só de `st.cache_data` (120 s), sem o
`local_cache` SQLite. É o maior ofensor de egress restante no fórum.

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

# Backup limpo (sem Base64) a partir de data/escola_ativa.db
python scripts/backup_clean.py

# Preparar o backup para restauração (normaliza datas e remove duplicatas)
python scripts/prepare_restore.py

# Simular / executar a restauração no novo Supabase
python scripts/restore_new_supabase.py --dry-run
python scripts/restore_new_supabase.py --url <nova-url> --key <nova-anon-key>

# Auditar/limpar duplicatas de bot no fórum (dry-run / aplicar)
python scripts/cleanup_forum_duplicates.py
python scripts/cleanup_forum_duplicates.py --apply
```

## Histórico de commits relacionados

| Commit | Descrição |
| ------ | --------- |
| `55e94f1` | Corrige quizzes com títulos duplicados e conclusão cruzada |
| `3e365c5` | Cache SQLite de scores no plugin de atividades diárias |
| `0393486` | Reduz egress do Supabase com cache local e documenta issues |
