"""Testes da criacao de pastas de atividades pelo agente (IS-130).

Os testes extraem apenas as funcoes necessarias do `lab_agent.py` (via AST),
sem executar o modulo inteiro (que inicia logging/descoberta de servidor).
"""

import ast
import getpass
import json
import logging
import os
import re
import shutil
import socket
import tempfile
import time
import zipfile
from pathlib import Path

import pytest

AGENT = Path(__file__).resolve().parents[1] / "data" / "repo" / "plugins" / "lab_agent.py"
INSTALADOR = AGENT.with_suffix(".ps1")

FUNCOES = {
    "_parse_aula_range",
    "_pasta_segura",
    "_nome_pasta_aluno",
    "_base_pastas_padrao",
    "_criar_estrutura_atividades",
    "_zipar_atividades",
    "_normalizar_url",
    "_tamanho_arvore",
    "_apagar_conteudo",
    "_set_dword_hkcu",
    "_calcular_expiracao",
}


def _carregar_funcoes():
    src = AGENT.read_text(encoding="utf-8")
    tree = ast.parse(src)
    corpo = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in FUNCOES]
    assert {n.name for n in corpo} == FUNCOES, "funcoes do agente mudaram de nome"
    modulo = ast.Module(body=corpo, type_ignores=[])
    ns = {
        "os": os,
        "re": re,
        "json": json,
        "logging": logging,
        "getpass": getpass,
        "shutil": shutil,
        "socket": socket,
        "tempfile": tempfile,
        "time": time,
        "show_balloon": lambda *a, **k: None,
    }
    exec(compile(modulo, str(AGENT), "exec"), ns)
    return ns


def test_zipar_atividades(tmp_path):
    ns = _carregar_funcoes()
    base = tmp_path / "Documents" / "SysAva"
    (base / "Turma_2A" / "PROG" / "PEDRO_HENRIQUE" / "Aula_01").mkdir(parents=True)
    (base / "Turma_2A" / "PROG" / "PEDRO_HENRIQUE" / "Aula_01" / "atividade.txt").write_text(
        "feito", encoding="utf-8"
    )

    caminho = ns["_zipar_atividades"](str(base), str(tmp_path / "zips"))

    assert os.path.isfile(caminho) and caminho.endswith(".zip")
    with zipfile.ZipFile(caminho) as z:
        nomes = z.namelist()
    assert any(n.endswith("atividade.txt") for n in nomes)


def test_cria_turma_disciplina_aluno_e_aulas(tmp_path):
    ns = _carregar_funcoes()
    msg = json.dumps({
        "base": str(tmp_path),
        "turma": "2ª SÉRIE - Turma I-A (Técnico DS)",
        "disciplina": "PROGRAMAÇÃO WEB FRONT-END",
        "aluno": "Pedro Henrique Pereira Garcias",
        "aulas": "1-3",
    }, ensure_ascii=False)

    destino, criadas = ns["_criar_estrutura_atividades"](msg)

    assert criadas == 3
    esperado = (tmp_path / "2ª_SÉRIE_-_Turma_I-A_(Técnico_DS)"
                / "PROGRAMAÇÃO_WEB_FRONT-END" / "Pedro_Henrique")
    assert Path(destino) == esperado
    assert sorted(p.name for p in esperado.iterdir()) == ["Aula_01", "Aula_02", "Aula_03"]


def test_escapa_caracteres_invalidos_do_windows(tmp_path):
    ns = _carregar_funcoes()
    msg = json.dumps({
        "base": str(tmp_path),
        "turma": "Turma 1",
        "disciplina": "WEB/FRONT:END?",
        "aluno": "Aluno Teste",
        "aulas": "7",
    }, ensure_ascii=False)

    destino, _ = ns["_criar_estrutura_atividades"](msg)

    assert Path(destino).name == "Aluno_Teste"
    assert Path(destino).parent.name == "WEB-FRONT-END-"
    assert (Path(destino) / "Aula_07").is_dir()


def test_formato_antigo_pipe_continua_funcionando(tmp_path, monkeypatch):
    ns = _carregar_funcoes()
    original = os.path.expanduser
    monkeypatch.setattr(os.path, "expanduser", lambda p: str(tmp_path) if p == "~" else original(p))

    msg = "ESCOLA TESTE|Turma X|Disc Y|Aluno Z|5-6"
    destino, criadas = ns["_criar_estrutura_atividades"](msg)

    esperado = tmp_path / "Documents" / "SysAva" / "Turma_X" / "Disc_Y" / "Aluno_Z"
    assert Path(destino) == esperado
    assert criadas == 2
    assert sorted(p.name for p in esperado.iterdir()) == ["Aula_05", "Aula_06"]


def test_sem_aluno_usa_conta_windows(tmp_path):
    ns = _carregar_funcoes()
    msg = json.dumps({
        "base": str(tmp_path), "turma": "T", "disciplina": "D", "aulas": "1",
    }, ensure_ascii=False)

    destino, _ = ns["_criar_estrutura_atividades"](msg)

    import getpass
    esperado = ns["_pasta_segura"](ns["_nome_pasta_aluno"](getpass.getuser()), "Aluno")
    assert Path(destino).name == esperado


def test_nome_do_aluno_usa_so_dois_primeiros_nomes():
    ns = _carregar_funcoes()
    f = ns["_nome_pasta_aluno"]
    assert f("PEDRO HENRIQUE PEREIRA GARCIAS") == "PEDRO HENRIQUE"
    assert f("  MARIA   CLARA  ") == "MARIA CLARA"
    assert f("JOSÉ ISAC ARAUJO DA SILVA") == "JOSÉ ISAC"
    assert f("ANA") == "ANA"
    assert f("") == ""


def test_apagar_conteudo(tmp_path):
    ns = _carregar_funcoes()
    pasta = tmp_path / "temp"
    (pasta / "sub").mkdir(parents=True)
    (pasta / "a.txt").write_text("a" * 1000, encoding="utf-8")
    (pasta / "sub" / "b.txt").write_text("b" * 500, encoding="utf-8")
    (pasta / "novo.txt").write_text("n", encoding="utf-8")
    velho = time.time() - 3 * 86400
    for alvo in (pasta / "a.txt", pasta / "sub" / "b.txt", pasta / "sub"):
        os.utime(alvo, (velho, velho))

    livre, itens = ns["_apagar_conteudo"](str(pasta), 1)

    assert itens == 2
    assert livre >= 1500
    assert (pasta / "novo.txt").exists()
    assert not (pasta / "a.txt").exists()
    assert not (pasta / "sub").exists()


def test_calcular_expiracao():
    ns = _carregar_funcoes()
    f = ns["_calcular_expiracao"]
    agora = int(time.time())

    assert abs(f(60) - (agora + 3600)) < 5

    fim = f(0)
    assert fim > agora
    t = time.localtime(fim)
    assert (t.tm_hour, t.tm_min) == (23, 59)


def test_set_dword_hkcu():
    if os.name != "nt":
        pytest.skip("Windows only")
    import uuid
    import winreg

    ns = _carregar_funcoes()
    caminho = "Software\\\\SysAvaTeste\\\\" + uuid.uuid4().hex[:8]
    try:
        assert ns["_set_dword_hkcu"](caminho, "Teste", 1) is True
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, caminho, 0, winreg.KEY_READ) as chave:
            valor, _tipo = winreg.QueryValueEx(chave, "Teste")
        assert valor == 1
    finally:
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, caminho)
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, "Software\\\\SysAvaTeste")
        except OSError:
            pass


def test_normalizar_url():
    ns = _carregar_funcoes()
    f = ns["_normalizar_url"]
    assert f("prova-motriz.jovensgenios.com/entrar") == "https://prova-motriz.jovensgenios.com/entrar"
    assert f(" http://x.y/z ") == "http://x.y/z"
    assert f("") == ""
    assert f(chr(34) + "https://a.b" + chr(34)) == "https://a.b"


def test_parse_aula_range():
    ns = _carregar_funcoes()
    assert ns["_parse_aula_range"]("3") == [1, 2, 3]
    assert ns["_parse_aula_range"]("5-7") == [5, 6, 7]
    assert ns["_parse_aula_range"]("") == []
    assert ns["_parse_aula_range"]("abc") == []


def test_copia_embutida_no_instalador_esta_sincronizada():
    ps1 = INSTALADOR.read_text(encoding="utf-8")
    bloco = re.search(r"\$agentCode = @'\n(.*?)\n'@", ps1, re.S)
    assert bloco, "here-string $agentCode nao encontrado no instalador"

    def normalizar(texto):
        return texto.replace("\r\n", "\n").rstrip("\n")

    assert normalizar(bloco.group(1)) == normalizar(AGENT.read_text(encoding="utf-8"))


MONITOR = AGENT.parent / "lab_monitor.py"
if not MONITOR.exists():  # IS-134: o monitor foi movido para plugins/monitor_rede/
    MONITOR = AGENT.parents[3] / "plugins" / "monitor_rede" / "lab_monitor.py"


def test_payload_do_dashboard_cria_estrutura_no_agente(tmp_path):
    """Contrato dashboard -> agente: o JSON gerado pela aba Ferramentas funciona."""
    src = MONITOR.read_text(encoding="utf-8")
    tree = ast.parse(src)
    fn = next(
        n for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name == "build_estrutura_payload"
    )
    ns_monitor = {"json": json}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(MONITOR), "exec"), ns_monitor)

    payload = ns_monitor["build_estrutura_payload"](
        str(tmp_path), "Turma 2A", "WEB", "1-2", "Maria Clara Oliveira"
    )

    ns_agente = _carregar_funcoes()
    destino, criadas = ns_agente["_criar_estrutura_atividades"](payload)

    assert criadas == 2
    assert Path(destino) == tmp_path / "Turma_2A" / "WEB" / "Maria_Clara"
    assert (Path(destino) / "Aula_02").is_dir()
