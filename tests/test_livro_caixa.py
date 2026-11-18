"""Livro-caixa (IS-045): estrutura em blocos, zonas livres e fila posicional."""

from services import livro_caixa as lc


def test_estrutura_padrao_tem_blocos_e_zonas():
    doc = lc.estrutura_padrao(8, meta_horas=40)
    assert doc["estrutura"] == "blocos"
    assert doc["blocos"] == [[1, 8], [9, 16], [17, 24], [25, 32]]
    assert [z["id"] for z in doc["zonas"]] == ["z1", "z2"]
    assert doc["entradas"] == []
    assert doc["subject_id"] == 8


def test_resolver_linear_cobre_meta():
    entradas = lc.resolver(lc.estrutura_linear(8, meta_horas=5))
    assert [e["pos"] for e in entradas] == [1, 2, 3, 4, 5]
    assert all(e["tipo"] == "conteudo" and e["aula_numero"] == e["pos"]
               for e in entradas)


def test_resolver_blocos_padrao_32_posicoes():
    entradas = lc.resolver(lc.estrutura_padrao(8, 40))
    assert len(entradas) == 32
    assert [e["pos"] for e in entradas] == list(range(1, 33))
    assert [e["aula_numero"] for e in entradas] == list(range(1, 33))
    assert all(e["tipo"] == "conteudo" for e in entradas)


def test_resolver_insere_especial_na_zona_e_empurra_o_resto():
    doc = lc.estrutura_padrao(8, 40)
    doc["zonas"][0]["itens"] = [{"titulo": "Prova parcial",
                                 "tipo_nome": "Avaliação"}]
    entradas = lc.resolver(doc)
    assert len(entradas) == 33
    # Posição 17 = logo após o bloco 09-16 (zona z1)
    especial = entradas[16]
    assert especial["tipo"] == "especial"
    assert especial["titulo"] == "Prova parcial"
    # Aula 17 empurrada para a posição 18 — posição != número de título (IS-045)
    assert entradas[17]["aula_numero"] == 17
    assert entradas[17]["pos"] == 18


def test_resolver_rejeita_estruturas_invalidas():
    assert lc.resolver(None) is None
    assert lc.resolver("texto") is None
    assert lc.resolver({"estrutura": "qualquer"}) is None
    assert lc.resolver({"estrutura": "blocos", "blocos": []}) is None
    assert lc.resolver({"estrutura": "blocos", "blocos": [[16, 1]]}) is None


def test_conferir_padrao_ok_com_aviso_de_meta():
    rel = lc.conferir(lc.estrutura_padrao(8, 40))
    assert rel["ok"] is True
    assert rel["erros"] == []
    assert rel["n_conteudo"] == 32
    # meta 40h × cobertura 32 posições → aviso (zonas vazias)
    assert rel["avisos"]
