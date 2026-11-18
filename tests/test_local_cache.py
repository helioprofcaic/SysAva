"""Testes do cache local (IS-128): resultado vazio de uma falha de rede não
pode virar cache "fresco" por horas."""

from datetime import datetime, timedelta

from services import local_cache as lc


def _isolated_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(lc, "_CACHE_DIR", str(tmp_path))
    monkeypatch.setattr(lc, "_CACHE_DB", str(tmp_path / "sysava_cache.db"))
    monkeypatch.setattr(lc, "_CONN", None)
    monkeypatch.delenv("DISABLE_LOCAL_CACHE", raising=False)
    monkeypatch.delenv("ENABLE_LOCAL_CACHE", raising=False)
    return lc


def _age_entry(cache, key, seconds):
    synced_at = (datetime.now() - timedelta(seconds=seconds)).isoformat(timespec="seconds")
    conn = cache._conn()
    conn.execute("UPDATE _cache_blob SET synced_at = ? WHERE cache_key = ?", (synced_at, key))
    conn.commit()


def test_lista_vazia_nao_e_cacheada(tmp_path, monkeypatch):
    cache = _isolated_cache(tmp_path, monkeypatch)
    calls = []

    def fetch_com_falha():
        calls.append(1)
        return []

    cache.get_or_fetch("classes", fetch_com_falha, ttl=600, cache_empty=False)
    cache.get_or_fetch("classes", fetch_com_falha, ttl=600, cache_empty=False)

    assert len(calls) == 2


def test_lista_com_dados_e_cacheada(tmp_path, monkeypatch):
    cache = _isolated_cache(tmp_path, monkeypatch)
    calls = []

    def fetch():
        calls.append(1)
        return [{"id": 1, "name": "Turma I-A"}]

    primeira = cache.get_or_fetch("classes", fetch, ttl=600, cache_empty=False)
    segunda = cache.get_or_fetch("classes", fetch, ttl=600, cache_empty=False)

    assert len(calls) == 1
    assert primeira == segunda == [{"id": 1, "name": "Turma I-A"}]


def test_cache_antigo_preferido_a_resultado_vazio(tmp_path, monkeypatch):
    cache = _isolated_cache(tmp_path, monkeypatch)
    cache._set_blob("classes", [{"id": 1, "name": "Turma I-A"}])
    _age_entry(cache, "classes", seconds=3600)

    resultado = cache.get_or_fetch("classes", lambda: [], ttl=600, cache_empty=False)

    assert resultado == [{"id": 1, "name": "Turma I-A"}]
    assert cache._get_blob("classes")[0] == [{"id": 1, "name": "Turma I-A"}]


def test_cache_empty_padrao_mantem_comportamento_antigo(tmp_path, monkeypatch):
    cache = _isolated_cache(tmp_path, monkeypatch)
    calls = []

    def fetch():
        calls.append(1)
        return []

    cache.get_or_fetch("vazio", fetch, ttl=600)
    cache.get_or_fetch("vazio", fetch, ttl=600)

    assert len(calls) == 1
