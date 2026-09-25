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
| IS-011 | Aba Portal (iSeduc): esqueleto Planejar/Registrar/Notas | 🟡 | 2026-09-22 |
| IS-012 | Gerador de aulas salvando opções com marcador "[x]/[ ]" no texto | 🟢 | 2026-09-24 |
| IS-013 | Plugin Atividades: exportar relatório CSV de pontos por aula | 🟢 | 2026-09-24 |
| IS-014 | Qualitativo vazando entre disciplinas (pontos órfãos sem subject_id) | 🟢 | 2026-09-24 |
| IS-015 | Planejamento/Registro: contagem da disciplina IA 51/40 vs 28/27 no portal | 🟢 | 2026-09-24 |
| IS-016 | Gerador de planos: Mentoria Tech II não gerava datas novas com lições | 🟢 | 2026-09-24 |
| IS-017 | Gerador de planos: lições fora do padrão de título "Aula XX" quebravam a fila de planejamento | 🟢 | 2026-09-25 |
| IS-018 | Frequência dos planos só consultava a lista negra — tabela `attendance` e JSON de plugins não eram lidos | 🟢 | 2026-09-25 |
| IS-019 | Gerador de planos: tipos de estratégia configuráveis + filtro de intervalo de aulas a gerar | 🟢 | 2026-09-25 |
| IS-020 | Numeração de planos pulava os pares (grade duplicada) + "Sobrescrever" agora limpa `planejamento` | 🟢 | 2026-09-25 |
| IS-021 | Frequência diária não persistia no `escola_ativa.db` e a leitura ignorava disciplina (estrutura data → turma → disciplina) | 🟢 | 2026-09-25 |
| IS-022 | Plugins Notas/Frequência: `escola_ativa` como 1ª persistência e Supabase como redundância (sem travar na conexão) | ⚪ | 2026-09-25 |
| IS-023 | Plugin Atividades: lançamento de Seminário como avaliação (intervalo de aulas + nome + lista de pesquisa) | 🟡 | 2026-09-25 |
| IS-024 | Admin/Gerenciar Avaliações: opção de excluir avaliação (com respostas, questões e notas) | 🟢 | 2026-09-25 |
| IS-025 | Plugin Atividades: últimas 8 aulas da disciplina fora do teto de 6 pts (40h→33-40, 80h→73-80) + aulas de apresentação criadas | 🟢 | 2026-09-25 |
| IS-026 | Prova impressa/salva: separar lista de integrantes e lista de aulas do seminário (quebras de linha e listas) | 🟢 | 2026-09-25 |
| IS-027 | Visualizar/Imprimir Prova: prova cortada à direita (overflow do container 800px) | 🟢 | 2026-09-25 |

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
- `views/gerador_aulas.py`: nova opção na sidebar **💬 Fórum → "Publicar desafio
  do EduBot no fórum"** (marcada por padrão). Desmarcada, gera/salva a aula sem
  criar o post do EduBot (geração e replicação).

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

## IS-011 — Aba Portal (iSeduc): esqueleto Planejar/Registrar/Notas 🟡

**Objetivo:** separar no app principal a responsabilidade de lidar com o **Portal
iSeduc** (planejar aula, registrar aula com plano/frequência/atividades e lançar
notas), hoje espalhada em `apps/api` e `apps/planejamento_registro`.

**Decisões:**
- Página **Portal** no menu principal (visível a `admin`/`teacher`), com submenu
  interno: **Planejar aulas**, **Registrar no Portal**, **Notas**.
- Arquitetura **híbrida**: leitura de dados no **Supabase**; ações de robô
  (registrar/raspagem) via **API local** (`apps/api`), que só existe rodando
  localmente — no Cloud a UI mostra aviso e desabilita as ações.
- Construção incremental: primeiro o esqueleto (feito), depois cada subpágina.

**Entregue (esqueleto):**
- `services/portal_api.py`: cliente da API local com falha graciosa
  (`PORTAL_API_URL`, padrão `http://127.0.0.1:8000`).
- `views/portal.py`: página com as 3 subpáginas, status da automação local e
  resumos de leitura (planejamento pendente, histórico recente, avaliações).
- `app.py`: item **Portal** no menu (admin/teacher) e roteamento.

**Observação:** `apps/` está no `.gitignore` (não vai ao Cloud), por isso o Portal
mora em `views/`/`services/` e não importa módulos de `apps/`.

**Arquivos:** `services/portal_api.py`, `views/portal.py`, `app.py`

**Próximos passos:** definir e implementar as ações de cada subpágina
(gerar/editar plano; disparar `registrar_lote`/`raspagem`; lançar/sincronizar
notas).

**Validar:** logar como admin/professor → menu **Portal** → alternar as 3 seções.

---

## IS-012 — Gerador de aulas salvando opções com marcador "[x]/[ ]" no texto 🟢

**Pedido:** ao gerar uma aula, o quiz salvo apresentava alternativas com o marcador
`[x]`/`[ ]` impresso no texto da opção, além de nem sempre marcar a resposta
correta.

**Causa:** a IA produz variações do formato de alternativas (`A) [x] Opção`,
`**A) [x]**`, `**[x]**`, `A. Opção (x)`), mas o parser (`services/quiz_parser.py`)
só reconhecia o marcador `[x]` quando ele iniciava a linha (checkbox). Quando vinha
combinado com letra (`a) [x] ...`), a opção era salva com o `[x]` literal no texto e
o índice da correta ficava errado.

**Correção:** em `services/quiz_parser.py`:
- Normaliza marcadores em negrito: `**[x]**` → `[x]`, `**b)**` → `b)`, `**(x)**` → `(x)`.
- Reconhece `[x]`/`(x)` embutido em opções com letra e marca a alternativa correta.
- Remove marcadores residuais `[x]`/`[ ]`/`(x)` (e `*` de negrito) do texto salvo.

**Arquivos:** `services/quiz_parser.py`, `docs/ISSUES_LOCAIS.md`

**Validar:** gerar uma aula com quiz (`A) [ ] … B) [x] …`) e conferir no banco/
painel que as opções saem sem o `[x]` e com a correta marcada.

---

## IS-013 — Plugin Atividades: exportar relatório CSV de pontos por aula 🟢

**Pedido:** após um erro na pontuação dos qualitativos, precisar exportar um
relatório para conferir os pontos de atividade de **todas as aulas** de uma
disciplina.

**Solução:** a seção **📊 Pontuação Distribuída por Atividades** ganhou dois
botões de exportação — **📥 Baixar CSV** e **🌐 Baixar HTML** — sempre com
**todas as aulas** da disciplina (ignorando o filtro de bloco da tela), com as
colunas `Data, Estudante, Aula, Bloco, Pontos`.

**Arquivos:** `data/repo/plugins/daily_activities.py`

**Validar:** Plugins → Atividades → escolher turma/disciplina → tabela de
detalhe → botões CSV/HTML geram `relatorio_atividades_{turma}_{disciplina}.(csv|html)`.

---

## IS-014 — Qualitativo vazando entre disciplinas (pontos órfãos sem subject_id) 🟢

**Sintoma:** aluna sem atividades em **FUNDAMENTOS DE UI / UX OU IHC** aparecia
com **Qualitativo 6.0**. Exemplo: `MARIA FERNANDA DOS SANTOS LIMA` → 6.0 no
quadro de notas, embora não tivesse nenhuma atividade/lesson daquela disciplina.

**Causa raiz:** no plugin `student_scores.py`, `get_student_qualitative_points`
somava **qualquer ponto sem `subject_id`** ao total de **todas** as disciplinas
(`elif p_sid is None: total_pts += pts`). A aluna tinha 4 lançamentos órfãos de
27/05/2025 (2 + 4 − 6 + 6 = 6.0), lançados via Quadro de Notas da disciplina
**INTELIGÊNCIA ARTIFICIAL** sem preencher `subject_id`/`lesson_id` — e eles
inflavam o qualitativo de toda disciplina.

**Correção:** pontos sem `subject_id` (ex: lançados na "Visão Geral") só são
atribuídos à disciplina atual se o nome dela (normalizado) aparecer no campo
`notes` do lançamento. Pontos com `lesson_id` continuam resolvidos pelo mapa
de aulas.

**Resultado validado (dados reais da aluna):** UI/UX=IHC → 0.0, IA → 6.0,
POO → 2.5, Web Front-end 2026B → 0.5, Visão Geral → 6.0.

**Arquivos:** `data/repo/plugins/student_scores.py`

**Validar:** Plugins → Notas → Fundamentos UI → qualitativo da aluna agora 0.0;
Inteligência Artificial mantém 6.0.

---

## IS-015 — Planejamento/Registro: IA com 51/40 registros local vs 28/27 no portal 🟢

**Sintoma:** no app de Planejamento e Registro, a disciplina **INTELIGÊNCIA
ARTIFICIAL** mostrava **51** registros na Turma I-A (309197) e **40** na I-B
(314114), mas o portal iSeduc exibia **28** e **27**.

**Causa raiz:** `historico_aulas` tinha **duplicatas das mesmas aulas**. A
raspagem grava o histórico com o **nome atual da turma** (ex.: `2ª SÉRIE -
Turma I-A (Técnico DS)`), mas o robô de registro antigo gravou as mesmas aulas
com o rótulo antigo do portal (`EMTPDES-SIS-2ª SERIE - INTEGRAL-I-A`) e, nos
meses de fev-mar/2026, também no horário antigo `09:10 às 10:10` (aulas depois
movidas para `10:30 às 11:30`). Como o UNIQUE de `historico_aulas` é sobre o
**texto** `(data_aula, horario, turma, disciplina)`, o `INSERT OR REPLACE` da
raspagem **não** substituiu essas linhas — gerando 2-3 linhas por aula. O app
contava **linhas**; o portal conta **aulas**.

**Evidência:** Turma A = 28 linhas com o nome atual da turma (status `Aula
confirmada`) = exatamente o que o portal mostra; o restante (09:10 antigos,
duplicatas `10:30` e `Aguardando confirmação`) é resíduo. Turma B: a aula
excluída usa o rótulo antigo, então some com o filtro (27 = 28 datas − 1 excluída).

**Correção:** todas as consultas de histórico do app
(`apps/planejamento_registro/planejamento_registro_streamlit.py`) agora filtram
`turma = <nome atual da turma>` (via `_nome_turma_atual()`) e ignoram status
`Aula Excluída`: `panel_data`, `listar_historico`, `proximo_numero`,
`renumerar_planejamento`, `reconciliar` e `status_sabado`. Dados **não** foram
apagados — as linhas residuais continuam no banco.

**Arquivos:** `apps/planejamento_registro/planejamento_registro_streamlit.py`

**Validar:** app Planejamento e Registro → Turma A/B → IA → Painel mostra
**28/27** "Registradas (portal)" e Reconciliação bate com o portal.

---

## IS-016 — Gerador de planos: Mentoria Tech II não gerava datas novas com lições 🟢

**Sintoma:** em Planejamento e Registro → MENTORIAS TEC II, o Painel mostrava
"Última aula registrada no portal: 29/08/2026" (Turma A) / 28/08 (Turma B), mas
o botão "Gerar planos" não criava **nenhuma** data nova com lição até hoje
(24/09/2026).

**Causa raiz:** o contador `next_aula_num` do gerador
(`apps/planejamento_registro/core/gerador.py`) era inicializado com o **total
de linhas** de `historico_aulas` por turma/disciplina — incluindo o **resíduo
de bot antigo** (nome de turma/horário antigos, mesmo problema do IS-015). Na
Mentoria isso dava **45** (Turma A) e **38** (Turma B) vs. `max_hours = 40`
(subjects). Como toda aula gerada exige `seq_num = current_count + 1 ≤
max_hours`, o primeiro `seq = 46` já estourava o limite → **todos os slots eram
pulados** em `if seq_num > max_hours_disc: continue`.

**Evidência:** Turma A/B com `max_hours=40`; grade semanal tem slots reais
`Ment.Tec.II` (Terça 13:30 p/ 309197; Sexta 10:30 p/ 314114), sem bloqueios nem
feriados em set/2026; `planejamento` de disc 2 vazio. Linhas canônicas = 26 por
turma (set raspado do portal = 378 ao todo). Com a correção, o gerador produz
planos com lição de 01/09 a 22/09 (A) e 04/09 a 18/09 (B).

**Correção:** o gerador agora desconsidera linhas não-canônicas do histórico
(turma ≠ nome atual; fallback p/ turmas sem nenhuma linha canônica), tanto na
montagem de `historico_set` (bloqueio de slots) quanto na contagem
`hist_count` usada por `next_aula_num`. Removido o `GROUP BY` sobre todas as
linhas.

**Arquivos:** `apps/planejamento_registro/core/gerador.py`

**Validar:** app Planejamento e Registro → Turma A → MENTORIAS TEC II → "Gerar
planos" gera `plano_309197_2_2026-09-01_1330.txt` … `2026-09-22` (com lição) e
continua até 13/10; Turma B gera `plano_314114_2_2026-09-04_1030.txt` … 16/10.
Obs.: cada slot de Mentoria aparece 2× na grade (2h semanais) — o 2º passa a
ser reportado como `skipped` (arquivo já existe), comportamento pré-existente.

---

## IS-017 — Gerador de planos: lições fora do padrão de título "Aula XX" quebravam a fila de planejamento 🟢

**Sintoma:** ao revisar `aulas/prontas` de MENTORIAS TEC II da Turma A, os planos
de 22/09 a 06/10/2026 traziam conteúdo-lixo de lições que **não seguem** o padrão
de título `Aula XX`, p.ex.: "--- Configurações Iniciais ---", "Usamos o
$PSScriptRoot...", "Conta Pessoal (Padrão)" e "Setup PowerShell" (subject 2,
ids 69–72), "[Markdown] Estrutura para o seu Jupyter Notebook" (subject 11,
id 55) e "Documentação Técnica..."/"Jogo 2D simples com Pygame" (subject 1,
ids 1–2). Essas lições (fragmentos/placeholders) eram escolhidas normalmente
quando a sequência chegava às suas posições.

**Causa raiz:** a seleção de lição usava apenas a posição
`lessons_list[pedagogical_idx - 1]`, sem validar o formato do título; qualquer
registro solto na tabela `lessons` entrava na fila elegível ao planejamento.

**Correção:** adicionada a helper de módulo `_eh_lesson_planejavel(titulo)`
(regex `^\s*Aula\s+\d+`, `re.IGNORECASE`, contemplando acentos/variações como
"Aula 05", "Aula 27: ..."). Na seleção (`gerar_txt_planos`), a lição candidata
só é atribuída se o título passar no filtro; caso contrário `lesson = None` (o
plano não é gerado com conteúdo inválido e, no modo `prontas`, o arquivo não é
criado). **Não** se alterou o índice da lista / `sequence_map`.

**Ordenação (atualização 25/09):** a fila de lições planejáveis era montada com
`ORDER BY subject_id, id ASC`, o que fazia os títulos saírem **fora da ordem
crescente** (lições legadas da auditoria têm `id` alto, ex.: "Aula 11" com
`id=103` antes de "Aula 1" com `id=40`; a sequência gerada degradava para
"Aula 24/25" seguida de "Aula 11/12"). A fila agora é ordenada pelo **número
extraído do título** via `_numero_aula()`/`_ordenar_lessons_fila()` (None por
último; empates de mesmo número mantêm a ordem original — duplicatas legadas
ex.: Aula 11 id 103/50, Aula 24 id 478/498). O caminho manual do app
(`database_model.get_lesson_content_by_number`) já ordenava por número de
título e não precisou de mudança.

**Verificação:** regex validada contra todas as lições de subjects 1, 2, 3, 4,
6, 8, 11, 30, 33, 34, 35 (válidas por subject: 11=40, 3=21, 4=40, 2=33, 1=33,
30=38, 34=41, 33=44, 6=17, 8=31, 35=0). Teste end-to-end: rodada `pendentes`
p/ Turma A disc 2 e 11 com **zero** planos contendo conteúdo proibido; no modo
`prontas` p/ disc 2, nenhum arquivo novo é criado (as posições inválidas 34–37
caem como `Sem lição`, igual 38–40 p/ superfície de lições).

**Arquivos:** `apps/planejamento_registro/core/gerador.py`

**Validar:** Planejamento e Registro → Turma A → "Gerar planos" (pendentes):
nenhum `[CONTEUDO]` contém "--- Configurações Iniciais ---", "Setup PowerShell",
"Conta Pessoal (Padrão)" ou "Jupyter Notebook"; e os títulos das lições no
plano seguem ordem crescente de Aula (Mentoria A 01→22/09: Aula 24, 25, 26,
28 — a "27" só seria gravada no 2º passe do slot duplicado de 2h, que já cai
como `skipped`). Planos além da grade curricular continuam caindo no fallback
genérico "DISC - Aula N" (comportamento pré-existente no modo `pendentes`).
Planos já existentes em `aulas/prontas` com conteúdo-lixo permanecem no disco
(não são apagados nem regenerados automaticamente); para limpar, usar
"Sobrescrever existentes".

---

## IS-018 — Frequência dos planos só consultava a lista negra (tabela `attendance`/JSON não eram lidos) 🟢

**Sintoma:** os planos gerados traziam a chamada `[FREQUENCIA]` com **todos os
alunos como Presente**, exceto os da lista negra
(`data/excecoes_alunos.json` → `blacklist`/`blacklist_names`). A frequência
real (faltas registradas) não aparecia, mesmo existindo duas fontes:
a **tabela `attendance`** do banco local (sincronizada do Supabase, datas até
26/05/2026) e o **`data/repo/plugins/student_attendance.json`** (147KB).

**Causa raiz:** `banco.load_attendance_map_for()` lia os JSONs apenas em
`api/plugins/` (pasta que **não existe** no projeto) e esperava o formato
aninhado `{turma: {disc: {data: {ra}}}}` — mas o arquivo real usa o formato
plano `{turma: {data: {ra}}}` e vive em `data/repo/plugins/`. Resultado: o mapa
de frequência sempre voltava vazio e só restava a regra da lista negra. O
"Gerar plano" manual do app (`montar_conteudo_plano`) nem sequer consultava o
mapa de frequência (passava `attendance_map=None` ao `build_plan_txt`).

**Correção** em `apps/planejamento_registro/core/banco.py`:
- `load_attendance_json()` agora procura em `data/repo/plugins/` (atual) e
  depois em `api/plugins/` (compatibilidade).
- Novo `load_attendance_from_db(turma_id, data_iso)`: lê a tabela `attendance`
  por **data exata**, casando as linhas pelo **nome da turma normalizado**
  (a coluna `class_name` tem variações de escrita/acento; `student_number`
  guarda o nº de ordem, não o RA — o mapa sai por NOME em maiúsculas).
- `load_attendance_map_for()` prioriza: **1)** tabela `attendance`, **2)** JSONs
  (corrigido → normalizado → raw → planejado), e passou a reconhecer o
  **formato plano** do JSON.
- `montar_conteudo_plano()` (plano manual no app) agora também consulta
  `load_attendance_map_for` e repassa ao `build_plan_txt`.

**Arquivos:** `apps/planejamento_registro/core/banco.py`,
`apps/planejamento_registro/planejamento_registro_streamlit.py`

**Validar:** `load_attendance_map_for("309197", "2", "2026-05-12")` → origem
`tabela attendance`, 8 faltas reais (12 Presente / 8 Falta no plano manual);
datas sem chamada seguem com `Presente` + lista negra. A regra absoluta da
lista negra (`blacklist` SEMPRE `Falta`) foi mantida.

---

## IS-019 — Gerador de planos: tipos de estratégia configuráveis + filtro de intervalo de aulas a gerar 🟢

**Solicitação:** criar uma lista de tipos de estratégia ("Aula expositiva",
"Aula baseada em projetos", "Aula de atividades em laboratório") e um filtro
que permita gerar planos apenas dentro de um intervalo de número de aula (seq).

**Causa raiz:** a estratégia era um valor fixo `"Aula expositiva e prática."`
(no `'estrategia'` do plano e como default do `build_plan_txt`) e
`gerar_txt_planos` não tinha parâmetro de intervalo — a UI não oferecia escolha
de estratégia nem limites de aula.

**Correção:**
- `gerador.py`: novos parâmetros de `gerar_txt_planos`:
  `estrategia: str = None` (valor aplicado na seção `[ESTRATEGIA]` do TXT;
  `None`/omitido mantém o default `"Aula expositiva e prática."`) e
  `aula_min`/`aula_max: int = None` (limita o intervalo de `seq_num`/`AULA_NUM`
  gerado; `None` ou `0` = sem filtro). O filtro é aplicado logo após a checagem
  de `max_hours_disc`, **depois** de avançar os contadores (`next_aula_num`),
  então a numeração das aulas seguintes não muda e o modo `prontas`/existente
  continua sendo respeitado (não sobrescreve sem `force_overwrite`).
- `planejamento_registro_streamlit.py`: helper
  `_estrategias_disponiveis()`/`_salvar_estrategias()` persistindo a lista na
  chave `estrategias_disponiveis` de `planejamento_config` (JSON; default
  `["Aula expositiva", "Aula baseada em projetos", "Aula de atividades em
  laboratório"]`). Na seção "Gerar planos (grade/calendário)": `selectbox` de
  estratégia, checkbox "Limitar intervalo de aulas" com inputs "De/Até (aula nº)"
  e `expander` "Gerenciar lista de tipos de estratégia (uma por linha)". Os
  valores escolhidos são repassados ao `_gerar_txt_planos`.

**Verificação:** teste end-to-end (turma 309197, disc 1, numeração atual 30→31):
- sem estratégia → `[ESTRATEGIA] = Aula expositiva e prática.` (default preservado);
- `"Aula baseada em projetos"`, `"Aula de atividades em laboratório"`,
  `"Aula expositiva"` → aplicadas corretamente em todos os TXT gerados;
- `aula_min=32` → seq 31 NÃO gerada; `aula_min=29, aula_max=33` → apenas 31 e 33.
- Cleanup do teste confirmou que nada foi deixado no banco (1/6/24 pendentes
  originais) nem na pasta `aulas/padrao`.

**Arquivos:** `apps/planejamento_registro/core/gerador.py`,
`apps/planejamento_registro/planejamento_registro_streamlit.py`

**Validar:** Planejamento e Registro → "Gerar planos": escolher uma estratégia,
marcar "Limitar intervalo de aulas" (ex.: 30–33) e gerar; os TXT devem trazer
`[ESTRATEGIA]` com a opção escolhida e `AULA_NUM` dentro do intervalo. O
expander "Gerenciar lista de tipos de estratégia" salva a lista em
`planejamento_config` (persiste entre sessões).

---

## IS-020 — Numeração de planos pulava os pares (grade duplicada) + "Sobrescrever" agora limpa `planejamento` 🟢

**Sintoma (relatado):** "Não gerou planos do intervalo de 22 a 32"; IA da Turma A
tem 28 aulas canônicas e as pendentes saíram numeradas 29, 31, 33, 35, 37, 39 —
nunca pares; não era possível gerar 29–32 em sequência.

**Causa raiz:** a tabela `weekly_schedule` contém cada slot **duplicado**
("I.A.", "P.C. II"/"P.C.II", "Disc.Tec.", "Ment.Tec.II" — 22 linhas = 11 slots).
O gerador processava as duas linhas: a 1ª gera o plano (seq 29) e a 2ª **avançava
o contador de novo** antes de ser pulada pelo "arquivo já existe" → o `seq`/`AULA_NUM`
aumentava +2 por semana. Além disso, `force_overwrite` não regenerava slots já
existentes na tabela `planejamento` (pulados em `planejamento_set`) e não removia
linhas antigas com numeração divergente.

**Correção:**
- `gerador.py`: **deduplicação dos slots** da grade por `(class_name, day_of_week,
  time_slot)` no carregamento — cada slot gera UMA aula → numeração consecutiva.
- `gerador.py`: em modo `force_overwrite` (check "Sobrescrever existentes"):
  - o piso de contagem **não soma mais os pendentes** existentes (a numeração parte
    do histórico e é renumerada em ordem natural dentro da rodada);
  - o skip de `planejamento_set` é **ignorado** (slots já planejados são regenerados);
  - no save no banco, linhas antigas do mesmo slot com `numero_aula` divergente são
    **deletadas** antes do upsert (sem resíduos duplicados).

**Verificação:** force-regen com intervalo 29–34 na IA → 6 arquivos `AULA_NUM`
29,30,31,32,33,34 consecutivos e tabela `planejamento` atualizada (09-14 sai de 31
para 30, linha antiga 31 removida); depois do intervalo, continua 35,36,…40 nas
segundas livres. Pendentes IA existentes foram re-numerados no banco (29→34) em
ordem de data (aulas 29–32 atendem ao pedido). Estado do banco restaurado após os
testes (1 + 6 + 24 pendentes originais).

**Arquivos:** `apps/planejamento_registro/core/gerador.py`

**Validar:** Planejamento e Registro → Turma A → IA → "Gerar planos" marcando
"Sobrescrever existentes" com intervalo 29–32: os TXT/lista devem vir 29, 30, 31,
32 consecutivos e sem duplicar linhas em `planejamento`.

---

## IS-021 — Frequência diária não persistia no `escola_ativa.db` + leitura sem disciplina 🟢

**Sintoma:** em 25/09/2026, planos gerados (ex.: `plano_309197_11_2026-09-14_1030.txt`)
traziam a chamada `[FREQUENCIA]` sem a frequência real — só `Presente` e os alunos
da lista negra global (`data/excecoes_alunos.json`). O usuário registra a chamada
todo dia no plugin Frequência e esperava que ela persistisse nas **3 fontes**:
Supabase + `escola_ativa.db` + JSON.

**Causa raiz (2 frentes):**
1. **Persistência:** `data/repo/plugins/student_attendance.py` (plugin ativo do
   portal) gravava apenas o **JSON** (`turma → disciplina → data`) e o **Supabase**;
   a tabela `attendance` do **`escola_ativa.db` nunca era escrita** pelo plugin.
   Como a tabela local só era populada por restore/sync pontual, ela estava
   parada em 26/05/2026 com `subject_id` **NULL** em todas as 1431 linhas — sem
   nunca chegar as chamadas de junho em diante.
2. **Leitura:** `load_attendance_from_db` era "disciplina agnóstica" (filtrava por
   data + turma, ignorava `subject_id`), então a frequência de um dia caía em
   qualquer disciplina daquele dia.

**Correção:**
- `data/repo/plugins/student_attendance.py`: novo helper
  `_write_local_attendance(db_records)` grava a chamada também na tabela
  `attendance` do `escola_ativa.db`, **com `subject_id` preenchido**. Upsert
  **manual** por `(student_name, class_name, subject_id, date)` — a tabela local
  (restaurada do Supabase) **não tem UNIQUE**, então `ON CONFLICT` falharia. O
  botão "Salvar Chamada do Dia" agora redunda nas **3 fontes**: JSON + banco
  local + Supabase (o Supabase continua condicional a `db.supabase`).
- `apps/planejamento_registro/core/banco.py`: resolução da frequência estruturada
  como **DATA → TURMA → DISCIPLINA**:
  - `load_attendance_from_db(turma_id, data_iso, disc_id=None)`: filtra pela
    **data exata**, casa a turma por nome normalizado e separa as linhas por
    `subject_id` — as **exatas da disciplina** têm prioridade; linhas legadas
    **sem** `subject_id` servem de fallback; linhas de **outra** disciplina são
    ignoradas.
  - `load_attendance_map_for` passa a aceitar também o formato **data-first** no
    JSON `{data: {turma: {disciplina: {ra: status}}}}`, além do plano legado
    `{turma: {data: {ra}}}` e do canônico `{turma: {disciplina: {data: {ra}}}}`.

**Observação:** `apps/api/*` é apenas leitura/referência e **não** foi alterado
(conforme orientação). A tabela local `attendance` tem schema legado (id TEXT,
sem UNIQUE) — o upsert manual do plugin casa com esse schema.

**Validação executada:** escrita via `_write_local_attendance` → `load_attendance_map_for`,
retornando `{ANDRE…: Falta, BRUNA…: Presente}` somente para a disciplina 11 da
Turma A na data; outra disciplina na mesma data e a Turma B retornam **vazio**;
upsert reexecutado atualizou `is_present` sem duplicar. Formato data-first do JSON
validado em `data/repo/plugins/student_attendance_corrigido.json` temporário
(removido após o teste) para 309197/11 e 314114/11.

**Arquivos:** `data/repo/plugins/student_attendance.py`,
`apps/planejamento_registro/core/banco.py`

**Validar:** (a) no plugin Frequência, salvar a chamada de uma data → conferir
linhas novas com `subject_id` na tabela `attendance` de `data/escola_ativa.db`;
(b) `load_attendance_map_for("309197", "11", "<data>")` retorna a chamada daquele
(data, turma, disciplina); (c) gerar plano e conferir que `[FREQUENCIA]` reflete a
chamada real daquele dia/disciplina.

---

## IS-022 — Plugins Notas/Frequência: `escola_ativa` como 1ª persistência, Supabase como redundância ⚪

**Pedido (agenda):** "Sempre que vou colocar uma nota, fazer uma frequência fica
lento esperando conexão." Registrar **primeiro no `escola_ativa.db`** (rápido,
local) e usar o **Supabase como redundância** com um **tempo razoável de
redundância**, para não travar o trabalho do professor na chamada/nota.

**Situação atual:**
- `data/repo/plugins/student_attendance.py` (Diário de Frequência): após o
  IS-021 grava JSON + `escola_ativa.db` na hora, mas faz o **upsert no Supabase
  de forma síncrona** no próprio callback do botão — a latência/conexão do cloud
  bloqueia a interface até terminar (ou estourar o timeout).
- `data/repo/plugins/student_scores.py` / `daily_activities.py` (Notas e
  Atividades): gravação/leitura de pontos qualitativos passa pela nuvem na carga
  e no save (ex.: `db.supabase` / `get_student_score`), mesmo cenário de espera.

**Proposta (quando implementar):**
1. **Persistência primária local:** escrever instantâneo em `escola_ativa.db`
   (+ JSON de origem), sem depender de rede.
2. **Supabase = redundância em fila:** enfileirar o lote pendente localmente
   (ex.: tabela/arquivo `pendentes_sync`), enviar ao cloud em **lote com
   debounce** (ex.: a cada N minutos ou quando o app voltar ao foco), sem
   bloquear o botão "Salvar" (thread de fundo / timer).
3. Aplicar o mesmo padrão em Frequência, Notas e Atividades.
4. **Bônus (IS-003):** batching reduz o número de round-trips e ajuda a conter o
   egress.

**Arquivos (candidatos):** `data/repo/plugins/student_attendance.py`,
`data/repo/plugins/student_scores.py`, `data/repo/plugins/daily_activities.py`,
e um novo utilitário de fila de sincronização.

**Validar (quando implementar):** salvar chamada/nota com o Supabase
indisponível → operação conclui na hora; com nuvem disponível, o sync chega ao
Supabase no intervalo configurado.

---

## IS-023 — Plugin Atividades: Lançamento de Seminário como Avaliação 🟡

**Pedido:** no plugin de Atividades, lançar um **seminário** como avaliação — o
professor seleciona um **intervalo de aulas**, dá o **nome do seminário** e obtém
a **lista de aulas a pesquisar**; a avaliação deve aparecer na UI de professor e
alunos (mesmo mecanismo do admin de Avaliações).

**Implementação (IS-021/IS-022 não interferem):**
- Nova seção "🎤 Lançamento de Seminário (Avaliação)" em
  `data/repo/plugins/daily_activities.py`, logo após o carregamento das aulas da
  disciplina (turma/disciplina vêm da sidebar do plugin).
- `st.select_slider(range=True)` escolhe o intervalo entre as aulas numeradas
  (regex `Aula\s*(\d+)`); a "lista de aulas a pesquisar" é exibida em dataframe
  sem repetir o prefixo "Aula N" (helper `_lesson_display`).
- **Integrantes do grupo:** multiselect com os alunos da turma
  (`db.get_students_by_class(class_id)`, já cacheado) — obrigatório ao menos 1;
  a lista de integrantes é embutida na mesma questão subjetiva criada, ficando
  visível para professor e alunos ao abrir a avaliação.
- Lança via `db.create_assessment(subject_id, "Seminário", f"{nome} · Aulas {min}–{max}")`
  (tabela `assessments` do Supabase, reutilizada pelo admin/front) e anexa **1
  questão subjetiva** com a lista de pesquisa (1 único insert = menos round-trips
  que uma questão por aula). Guarda contra duplicidade por título e contra
  resposta vazia do Supabase.
- Visibilidade confirmada sem mudanças no front: professor vê em
  `views/avaliacoes.py` (filtro "Trimestre=Todos" inclui qualquer tipo) e aluno
  na mesma tela — apenas MN1/MN2/MN3 têm trava de bloqueio; "Seminário" cai no
  fluxo normal com botão "Iniciar Tentativa".

**Pendências:**
- (decisão) Correção da nota do seminário: hoje o professor corrige via UI de
  correção da avaliação (resposta subjetiva); não há fluxo específico de
  "nota de apresentação".

**Arquivos:** `data/repo/plugins/daily_activities.py`, `docs/ISSUES_LOCAIS.md`

**Validar:** no plugin Atividades (turma/disciplina), selecionar intervalo,
nomear e lançar → conferir em `views/avaliacoes.py` (professor e aluno logado)
que aparece "Seminário - {nome} · Aulas X–Y" e que, ao abrir, lista as aulas a
pesquisar.

---

## IS-024 — Admin/Gerenciar Avaliações: exclusão de avaliação 🟢

**Pedido:** "Em admin/Gerenciar Avaliações não tem a opção de excluir a
avaliação. Quero excluir e recriar os seminários."

**Implementação:**
- `services/database.py`: nova função `delete_assessment(assessment_id)` que
  remove na ordem **respostas → submissões → questões → avaliação** (apenas
  `assessment_questions` tem `ON DELETE CASCADE` no schema; `student_assessments`
  e `student_assessment_answers` não, então a exclusão manual evita violação de
  FK no Supabase).
- `views/admin.py` (aba "Avaliações"): botão "🗑️ Excluir ..." abaixo do seletor
  de avaliação, com **confirmação em duas etapas** via `session_state`
  (`confirm_del_av_{id}`) para evitar exclusão acidental; ao confirmar chama
  `db.delete_assessment` e faz `st.rerun()`.

**Arquivos:** `services/database.py`, `views/admin.py`

**Validar:** em Admin → Avaliações, selecionar a turma/disciplina, escolher uma
avaliação existente, clicar em Excluir, confirmar → a avaliação some da lista
(de Admin e da tela do aluno) e um seminário com o mesmo título pode ser
recriado pelo plugin sem "já existe".

---

## IS-025 — Plugin Atividades: últimas 8 aulas fora do teto de 6 pts + aulas de apresentação 🟢

**Pedido (após IS-023):** ao lançar seminários, o limite de 6 pontos por bloco
impede pontuar as apresentações. Regra definida pelo usuário: **deixar fora do
teto as últimas 8 aulas** da disciplina — 40h → **33-40**; 80h → **73-80**.

**Implementação (evita regra fixa "33-40", que quebraria em 80h):**
- `data/repo/plugins/daily_activities.py`:
  - `APRESENTACAO_QTD = 8`; `_bloco_regular(aula_num)` divide a disciplina em
    blocos de 20 (1-20, 21-40, 41-60, ...) — generalizado para 80h;
  - `_bloco_info(aula_num, ultima_aula)` retorna o bloco "Apresentação
    (X-última)" com `capped=False` para as **8 aulas finais**, tomando
    `ultima_aula` = maior número de aula da disciplina (`get_lessons_for_subject`);
  - UI dinâmica: mensagem "Apresentação (33-40)/(73-80)... sem limite de 6
    pontos", coluna Pontuar com passo 0.5 e teto 10, "Disponível" 999, e filtro
    de bloco no relatório montado a partir dos blocos reais;
  - guarda: disciplinas com menos de 8 aulas não têm bloco de apresentação.
- **Aulas criadas no Supabase** (`lessons`, subject 8 FUNDAMENTOS DE UI/UX
  ORA IHC, 40h — só ia até a Aula 32): "Aula 33..40 Apresentação de Seminários
  — Grupo 1..8" (ids 634-641) com título, descrição, objetivo, roteiro da
  apresentação, critérios de avaliação e recursos (sem Base64).

**Arquivos:** `data/repo/plugins/daily_activities.py`; dados em `lessons`
(Supabase, subject 8).

**Validar (40h):** plugin Atividades → Fundamentos de UI/UX → aula 33-40 mostra
"Apresentação (33-40)... sem limite de 6 pontos" e aceita nota até 10; aula 25
segue em Bloco 21-40 com teto 6. (80h: aula 73-80 mostra Apresentação 73-80.)

---

## IS-026 — Prova impressa: separar integrantes e lista de aulas do seminário 🟢

**Pedido:** "Ao salvar a prova falta formatar melhor o layout, pois a lista de
alunos e a lista das aulas estão juntas". A questão subjetiva do seminário
(1 único texto com integrantes + aulas) era impressa em uma única linha porque
`markdown_to_html` descarta `\n` e itens `- `.

**Implementação:** em `views/avaliacoes.py`, nova `text_block_to_html(text)` —
mantém `markdown_to_html` (bold/italic/code + escape) e adiciona:
- quebras de linha como `<br>` e linhas em branco como espaçador de 8px;
- itens iniciados com `- ` ou `• ` agrupados em `<ul><li>` (recuo 22px).

Aplicada no texto das questões nas 3 telas de prova: Prova corrigida
(`generate_printable_view`), Prova em branco (`generate_blank_printable_view`)
e Impressão/Salvar da avaliação (`generate_assessment_print_html`). Options,
código web e respostas continuam com `markdown_to_html`.

**Arquivos:** `views/avaliacoes.py`

**Validar:** admin/avaliações de um Seminário → "Imprimir Prova" ou "Salvar
Prova (HTML)" → integrantes e lista de aulas aparecem em listas separadas.

---

## IS-027 — Visualizar/Imprimir Prova cortada à direita 🟢

**Pedido:** "No campo Imprimir Prova/Visualizar Prova a prova aparece na metade
do layout cortando na metade do lado direito". O container de 800px (`max-width:
800px`, sem `width`/`box-sizing`) estourava em telas estreitas e a faixa
"Aluno(a)/Nota" (linhas de `_` longas em flex `space-between`) transbordava o
bloco, cortando o lado direito.

**Implementação:** em `views/avaliacoes.py`, nos 3 templates
(`generate_printable_view`, `generate_blank_printable_view` e
`generate_assessment_print_html`):
- container centralizado com `max-width: min(800px, 100%); box-sizing:
  border-box; overflow-wrap: break-word;` — nunca ultrapassa a largura da tela;
- faixas `Aluno(a)/Nota Final` com `flex-wrap: wrap;` (e `gap` no template de
  impressão da avaliação) para quebrar linha quando não houver espaço.

**Arquivos:** `views/avaliacoes.py`

**Validar:** Visualizar Prova / Imprimir Prova de uma avaliação (ex. Seminário)
em janela estreita e larga — a prova fica centralizada e sem corte à direita.

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
