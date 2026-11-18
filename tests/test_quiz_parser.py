"""Regras do parser de quizzes (AGENTS.md § Estrutura do Quiz 4x4).

Cobrem: split resiliente ao cabeçalho `## Quiz` (sem depender do emoji),
título único por aula, 4 perguntas × 4 alternativas com `[x]` e comparação
do gabarito como inteiro (zeros à esquerda).
"""

import pytest

from services import database as db
from services import quiz_parser as qp

QUIZ_4X4 = """## 📝 Quiz

1. Qual a cor do céu em dia limpo?
- [ ] Verde
- [x] Azul
- [ ] Vermelho
- [ ] Preto

2. Quanto é 2 + 2?
- [ ] 3
- [ ] 5
- [x] 4
- [ ] 7

3. Qual é o maior planeta do sistema solar?
- [x] Júpiter
- [ ] Terra
- [ ] Marte
- [ ] Vênus

4. O que é uma função em programação?
- [x] Um bloco de código reutilizável
- [ ] Um erro de digitação
- [ ] Uma variável de laço
- [ ] Um laço infinito
"""

QUIZ_GABARITO = """## Quiz
Pergunta 01 Qual a cor do céu?
a) Verde
b) Azul
c) Preto
d) Roxo

Pergunta 02 Quanto e 2 + 2?
a) 3
b) 5
c) 4
d) 7

**Gabarito**
01 - b
02 - c"""


@pytest.fixture
def captura(monkeypatch):
    """Substitui a gravação no banco por um duplo em memória."""
    dados = {"apagados": [], "titulo": None, "questoes": []}

    def fake_delete(lesson_id):
        dados["apagados"].append(lesson_id)

    def fake_create(lesson_id, titulo):
        dados["titulo"] = titulo
        return [{"id": 7}], None

    def fake_question(quiz_id, texto, opcoes, idx):
        dados["questoes"].append({
            "texto": texto,
            "opcoes": list(opcoes),
            "idx": idx,
        })
        return None, None

    monkeypatch.setattr(db, "delete_quizzes_for_lesson", fake_delete)
    monkeypatch.setattr(db, "create_quiz", fake_create)
    monkeypatch.setattr(db, "create_quiz_question", fake_question)
    return dados


def test_split_depende_do_padrao_quiz_e_nao_do_emoji():
    aula, quiz = qp.split_lesson_and_quiz("Resumo da aula.\n\n## 📝 Quiz\n\n1. ...")
    assert quiz.startswith("## 📝 Quiz")
    assert "Resumo" in aula


def test_split_funciona_sem_emoji_no_cabecalho():
    _, quiz = qp.split_lesson_and_quiz("Texto.\n\n## Quiz\n\n1. ...")
    assert quiz.startswith("## Quiz")


def test_split_sem_quiz_devolve_tudo():
    aula, quiz = qp.split_lesson_and_quiz("Só conteúdo, sem quiz.")
    assert quiz is None
    assert aula == "Só conteúdo, sem quiz."


def test_processa_4_perguntas_com_4_alternativas(captura):
    ok, msg = qp.process_quiz_content(42, QUIZ_4X4, "Funções")
    assert ok
    # Limpa quizzes anteriores da MESMA aula antes de gravar (sem duplicatas)
    assert captura["apagados"] == [42]
    # Título único por aula — nunca o cabeçalho genérico do template
    assert captura["titulo"] == "Quiz: Funções"
    assert len(captura["questoes"]) == 4
    for q in captura["questoes"]:
        assert len(q["opcoes"]) == 4
        assert 0 <= q["idx"] < 4
    assert [q["idx"] for q in captura["questoes"]] == [1, 2, 0, 0]
    assert "4 questoes" in msg


def test_gabarito_com_zeros_a_esquerda_vira_inteiro(captura):
    ok, _ = qp.process_quiz_content(7, QUIZ_GABARITO, "Aula Y")
    assert ok
    assert [q["idx"] for q in captura["questoes"]] == [1, 2]
    assert captura["questoes"][0]["texto"] == "Qual a cor do céu?"


def test_variacao_pergunta_sem_emoji(captura):
    conteudo = ("## Quiz\nPergunta 1 Qual a cor?\n- [ ] Verde\n- [x] Azul\n"
                "- [ ] Preto\n- [ ] Roxo")
    qp.process_quiz_content(1, conteudo, "Aula Z")
    assert len(captura["questoes"]) == 1
    assert captura["questoes"][0]["idx"] == 1
