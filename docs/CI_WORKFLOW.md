# CI — GitHub Actions (SysAva)

Workflow mínimo em `.github/workflows/ci.yml` — fase inicial: **garantir
sintaxe em todo push/PR** e deixar a bateria de testes pronta para ligar sozinha
quando existir. Estrutura inspirada no projeto antigo de Testes de Sistemas
([proj_test_cicd_jest](https://github.com/hiseg10/proj_test_cicd_jest): Jest +
Cypress + Actions), adaptada ao ecossistema Python/Streamlit.

## Gatilhos

* `push` em qualquer branch
* `pull_request`

## O que roda (job `testes`, ubuntu-latest, Python 3.11)

| Passo | O quê | Falha quando... |
|---|---|---|
| **Sintaxe** | `git ls-files -z "*.py" \| xargs -0 -r python -m py_compile` — compila **só os `.py` versionados** (59 na data da escrita) | qualquer arquivo Python rastreado tiver erro de sintaxe |
| **Testes (pytest)** | `pip install -r requirements.txt pytest` + `pytest -q` | **passo só aparece quando houver `tests/**/*.py`** (`if: hashFiles(...)`) — hoje ele está oculto por design |

Python 3.11 = mesma versão do venv local `.sysenv`.

## Rodar o mesmo em casa

```bash
git ls-files -z "*.py" | xargs -0 -r python -m py_compile   # sintaxe
pytest -q                                                   # quando existir tests/
```

## Como ampliar (próximas fases)

1. Criar a pasta `tests/` na raiz → o passo de pytest **liga automaticamente**
   (não precisa mexer no YAML).
2. Evolução sugerida, na mesma ordem de custo:
   * testes unitários de lógica pura (`services/`, parsers, `quiz_parser`);
   * `streamlit.testing.v1.AppTest` para UI sem navegador (nativo ≥1.52);
   * `pytest-playwright` só se precisar E2E no navegador (papel do Cypress).
3. Lint (ruff) e badge/status são passo seguinte — badge fica no README,
   proteção de branch é configuração no GitHub (Settings → Branches).

## Mapa JS → Python (projeto antigo → este)

| proj_test_cicd_jest (Node) | SysAva (Python) |
|---|---|
| Jest (unit + mocks) | pytest (+ `unittest.mock` / `pytest-mock`) |
| Cypress (`cypress/e2e`) | Playwright Python **ou** AppTest Streamlit |
| ESLint | ruff (futuro) |
| `.github/workflows/ci.yml` | idem — mesmo YAML da pasta oculta |

---

Vinculado a: `docs/ISSUES_LOCAIS.md` (sem issue própria — spike de infra CI).
