# Testes do SysAva

Scaffold da bateria de testes — fase 1 (unitário puro, sem rede).
CI: `.github/workflows/ci.yml` roda `pytest -q` automaticamente assim que
existir arquivo `tests/**/*.py` (ver `docs/CI_WORKFLOW.md`).

## Como rodar (PowerShell, `.sysenv` ativo)

```powershell
pip install -r requirements-dev.txt   # 1x (pytest + mínimas deps de teste)
pytest -q                             # tudo
pytest tests/test_quiz_parser.py -q   # um arquivo
pytest -k gabarito -v                 # por nome
```

## Estrutura

```
pytest.ini               # testpaths = tests
requirements-dev.txt     # só o que os testes precisam (CI instala isto)
tests/
  conftest.py            # raiz do projeto no sys.path
  test_quiz_parser.py    # regras 4x4 do quiz (AGENTS.md)
  test_livro_caixa.py    # estrutura em blocos / zonas / fila posicional
```

## Convenções

* Arquivo `test_<modulo>.py`; funções `test_<comportamento>` (sem classe —
  pytest é baseado em funções; classe só se um cenário crescer muito).
* **Sem rede**: nada de Supabase real nos testes — usar duplo
  (`monkeypatch`), como o `captura` do `test_quiz_parser.py`.
* Um teste por regra comportamental; afirmar o comportamento documentado no
  `AGENTS.md`/`ISSUES_LOCAIS.md` (ex.: título único `Quiz: {aula}`).
* Novo módulo merece teste: crie `test_<modulo>.py` e mantenha este índice.

## Limitações conhecidas do parser (documentadas pelos testes)

* Variação `Pergunta 1:` (com dois-pontos **logo após o número**) ainda não
  casa no parser — usar `Pergunta 1 ` ou `1. `. Candidato a issue futura.
