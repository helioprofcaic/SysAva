# 🔎 Auditoria do Banco e Redução de Tabelas — SysAva

Data: 2026-09-22 · Contexto: bloqueio do Supabase por cota e migração para um novo projeto.

Objetivo: reduzir o número de tabelas do **novo Supabase**, identificar espelhos JSON
e serviços não essenciais, **sem risco para a rotina**.

---

## 1. Arquitetura atual (2 bancos)

| Camada | Banco | O que usa |
| ------ | ----- | --------- |
| Portal Streamlit (`app.py`, `views/`, `services/database.py`) | **Supabase (nuvem)** | 21 tabelas |
| Automação (API local `apps/api/` na porta 8000 + plugins em `data/repo/plugins/`) | **SQLite `data/escola_ativa.db`** | 34 tabelas |

Os dois se sobrepõem em 21 tabelas. As outras 13 **só existem no SQLite** e a
automação as acessa via SQL (nunca via `.table()` do Supabase).

> Conclusão: o novo Supabase **não precisa** das 13 tabelas de automação. Elas
> continuam no `escola_ativa.db` sem qualquer perda.

---

## 2. Tabelas essenciais no novo Supabase (21)

Usadas direto pelo portal (`services/database.py`) e pelos sincronizadores
(`audit_backup.py`, `class_registry.py`, `grade_semanal.py`, `student_attendance.py`,
`sync_lessons.py`, `duplicate_checker`, `supabase_monitor`):

`app_users`, `schools`, `classes`, `subjects`, `class_subjects`,
`student_enrollments`, `lessons`, `forum_posts`, `quizzes`, `quiz_questions`,
`user_history`, `assessments`, `assessment_questions`, `student_assessments`,
`student_assessment_answers`, `schedules`, `attendance`, `weekly_schedule`,
`historico_aulas`, `planejamento`, `master_config`.

---

## 3. Tabelas que NÃO vão para o novo Supabase (13)

Só locais (automação via SQLite). **Mantidas no `escola_ativa.db`.**

| Tabela | Linhas | Observação |
| ------ | -----: | ---------- |
| `student_grades` | 207 | Notas da automação (não usada pelo portal) |
| `blocked_dates` | 3 | Calendário da automação |
| `aula_sequence_map` | 8 | Mapeamento de sequência da automação |
| `planejamento_config` | 2 | Config (ver §5) |
| `turma_disciplina_config` | 8 | Config de vínculo turma/disciplina |
| `discipline_aliases` | 2 | Aliases da automação |
| `registration_queue` | 26 | Fila do robô de registro |
| `settings` | 19 | Config (ver §5) |
| `qualitative_points` | **0** | Vazia/abandonada |
| `grade_milestones` | **0** | Vazia/abandonada |
| `user_reminders` | **0** | Vazia/abandonada |
| `user_profiles` | 1 | Praticamente vazia |
| `student_scores` | — | Tabela referenciada por `apps/analise_notas/export_student_scores.py`, **mas não existe** no schema/backup → código provavelmente morto |

---

## 4. Tabelas replicando / duplicando dados (espelhos)

| Dado | Cópias | Risco |
| ---- | ------ | ----- |
| Grade horária | `grade_horaria.json` + SQLite `weekly_schedule` + Supabase `weekly_schedule` | Triplo espelho |
| Frequência | `student_attendance.json` + SQLite `attendance` + Supabase `attendance` | Triplo espelho |
| Notas/score | `student_scores.json` (237 KB) + `apps/api/plugins/student_scores.json` (137 KB) + Supabase `student_scores` (inexistente) | 3 representações |
| Histórico de aulas | `aulas_coletadas.json` + `class_registries.json` + SQLite `historico_aulas` + Supabase `historico_aulas` | 4 cópias |
| Notas do aluno | `student_grades` (SQLite) × `assessments`/`student_assessments` (Supabase) × `qualitative_points` (vazia) × `student_scores.json` | 4 modelos de nota |

---

## 5. Redundância de configuração (3 tabelas de config)

`master_config` (Supabase, `key/value`) · `planejamento_config` (SQLite, `chave/valor`) ·
`settings` (SQLite, `chave/valor`). Fazem a mesma coisa em bancos diferentes.
Consolidação é possível, mas é **local e de risco médio** — recomenda-se depois.

---

## 6. Duplicação de código / serviços

| Item | Situação |
| ---- | -------- |
| `data/repo/plugins/*` × `apps/api/plugins/*` | Cópias divergentes dos mesmos plugins (o **vivo** é `data/repo/plugins`, usado por `views/plugins.py`) |
| `apps/api/tools/vesão_aulas_selenium/*` × `apps/api/tools/*` | Versões legado duplicadas |
| `data/Turmas` × `data/repo/Turmas` | Árvore de arquivos duplicada |
| `apps/analise_notas/export_student_scores.py` | Lê tabela Supabase `student_scores` inexistente → não essencial |
| `apps/supabase_monitor`, `apps/duplicate_checker` | Úteis (monitor de egress / auditoria) — manter |
| `apps/api`, `apps/planejamento_registro` | Automação da rotina — essencial |

---

## 7. Decisões e plano (faseado, do menor para o maior risco)

**✅ Fase 1 — aprovada e aplicada:** o novo Supabase terá apenas as **21 tabelas
essenciais**. As 13 locais permanecem no `escola_ativa.db`.
`docs/NOVO_BANCO_SCHEMA.sql` foi enxugado; `scripts/restore_new_supabase.py`
restaura só as 21 (25.228 linhas).

**✅ Fase 2 — aprovada:** as tabelas vazias/abandonadas (`qualitative_points`,
`grade_milestones`, `user_reminders`, `user_profiles`) e a inexistente
`student_scores` **não** serão recriadas no Supabase. Os JSONs continuam como
estão (memória da automação).

**⏳ Fase 3 — adiada (após a migração):** unificar as 3 tabelas de config e
consolidar as representações de nota.

**⏳ Fase 4 — adiada (opcional):** remover cópias de plugins (`apps/api/plugins`)
e a árvore `data/repo/Turmas` duplicada, após confirmar que a API local não as
usa em produção.

---

## 7b. Resultado da migração (2026-09-22) ✅

- Novo projeto Supabase criado com as **21 tabelas** de `docs/NOVO_BANCO_SCHEMA.sql`.
- **24.087 linhas** restauradas; sequências reajustadas.
- Verificação origem × Supabase: **21/21 tabelas com contagem idêntica**.
- Cache local limpo; smoke test do portal OK (2 turmas, 16 disciplinas, 364 aulas,
  sem Base64).
- Limpezas aplicadas na preparação: datas `dd/mm/aaaa` → ISO (566), 107 linhas de
  teste corrompidas e 835 duplicatas de `attendance`, 167 de `historico_aulas`,
  20 de `weekly_schedule`, 11 de `assessments`, 1 aula com `id` UUID, 214 ids nulos.
- **Pendência conhecida:** `historico_aulas` local (566 → 399) é menor que o do
  Supabase antigo (1.234), inacessível durante o bloqueio. A tabela é repopulada
  pelo bot do portal iSeduc.
- **Correção pós-migração:** `historico_aulas.data_aula` é **TEXTO `dd/mm/aaaa`**
  (não `DATE`), para casar com o bot do iSeduc e com `class_registry` /
  `compare_routes` / `duplicate_checker`. Ajuste aplicado no schema e no
  `prepare_restore.py`; no projeto já criado, requer
  `ALTER TABLE ... ALTER COLUMN data_aula TYPE text USING to_char(data_aula,'DD/MM/YYYY')`.

## 8. Como validar

```powershell
# Tabelas e contagem no banco local
python -c "import sqlite3;c=sqlite3.connect('data/escola_ativa.db');print([r[0] for r in c.execute(\"SELECT name FROM sqlite_master WHERE type='table' ORDER BY name\")])"

# Backup limpo + simulação de restore (sem gravar)
python scripts/backup_clean.py
python scripts/restore_new_supabase.py --dry-run
```
