"""
Cache local (SQLite) para reduzir o egress do Supabase.

Segurança / deploy:
- É **inerte por padrão**. Só atua quando `ENABLE_LOCAL_CACHE` estiver ligado
  (via `.streamlit/secrets.toml` local ou variável de ambiente). Sem a flag,
  `get_or_fetch()` simplesmente chama o fetch original — comportamento idêntico
  ao de hoje. Isso torna o commit seguro para o Streamlit Cloud (alunos).
- Nunca quebra: qualquer erro de SQLite cai de volta para o Supabase.

Uso:
    from services import local_cache as lc
    data = lc.get_or_fetch("classes", fetch_fn, ttl=lc.TTL_BASE)
"""

import os
import json
import sqlite3
import threading
from datetime import datetime

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CACHE_DIR = os.path.join(_PROJECT_ROOT, "data", "cache")
_CACHE_DB = os.path.join(_CACHE_DIR, "sysava_cache.db")

_LOCK = threading.Lock()
_CONN = None

# TTLs sugeridos (segundos)
TTL_BASE = 6 * 3600     # tabelas que mudam pouco (classes, subjects, ...)
TTL_MEDIUM = 3600       # dados que mudam ocasionalmente
TTL_FORUM = 300         # fórum
TTL_SCORE = 600         # score do aluno (dados de engajamento)


def _read_flag() -> bool:
    """Lê ENABLE_LOCAL_CACHE de env ou st.secrets. Default: desligado."""
    val = os.environ.get("ENABLE_LOCAL_CACHE", "")
    if not val:
        try:
            import streamlit as st
            val = st.secrets.get("ENABLE_LOCAL_CACHE", "")
        except Exception:
            val = ""
    return str(val).strip().lower() in ("1", "true", "yes", "on", "sim")


def cache_enabled() -> bool:
    try:
        return _read_flag()
    except Exception:
        return False


def _conn() -> sqlite3.Connection:
    global _CONN
    if _CONN is not None:
        return _CONN
    os.makedirs(_CACHE_DIR, exist_ok=True)
    conn = sqlite3.connect(_CACHE_DB, check_same_thread=False, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS _cache_blob (
            cache_key TEXT PRIMARY KEY,
            data      TEXT NOT NULL,
            row_count INTEGER,
            synced_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS _score_cache (
            username   TEXT NOT NULL,
            subject_id TEXT NOT NULL,
            payload    TEXT NOT NULL,
            synced_at  TEXT NOT NULL,
            PRIMARY KEY (username, subject_id)
        )
    """)
    conn.commit()
    _CONN = conn
    return _CONN


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _age_seconds(synced_at: str):
    try:
        return (datetime.now() - datetime.fromisoformat(synced_at)).total_seconds()
    except Exception:
        return None


def _get_blob(cache_key: str):
    row = _conn().execute(
        "SELECT data, synced_at FROM _cache_blob WHERE cache_key = ?", (cache_key,)
    ).fetchone()
    if not row:
        return None, None
    return json.loads(row[0]), row[1]


def _set_blob(cache_key: str, data):
    payload = json.dumps(data, ensure_ascii=False, default=str)
    count = len(data) if isinstance(data, list) else None
    with _LOCK:
        conn = _conn()
        conn.execute(
            "INSERT INTO _cache_blob (cache_key, data, row_count, synced_at) "
            "VALUES (?, ?, ?, ?) "
            "ON CONFLICT(cache_key) DO UPDATE SET "
            "data=excluded.data, row_count=excluded.row_count, synced_at=excluded.synced_at",
            (cache_key, payload, count, _now()),
        )
        conn.commit()


def get_or_fetch(cache_key: str, fetch_fn, ttl: int = TTL_BASE, force: bool = False):
    """Devolve do cache se fresco; senão busca no Supabase, grava e devolve.

    Em qualquer erro, delega para `fetch_fn()` (fallback seguro).
    """
    if not cache_enabled():
        return fetch_fn()

    try:
        if not force:
            data, synced_at = _get_blob(cache_key)
            age = _age_seconds(synced_at) if synced_at else None
            if data is not None and age is not None and age < ttl:
                return data

        fresh = fetch_fn()
        try:
            _set_blob(cache_key, fresh)
        except Exception:
            pass
        return fresh
    except Exception:
        # Se a busca falhar, tenta devolver o que estiver em cache (mesmo vencido).
        try:
            data, _ = _get_blob(cache_key)
            if data is not None:
                return data
        except Exception:
            pass
        return fetch_fn()


def get_scores_bulk(subject_id, usernames, ttl: int = TTL_SCORE) -> dict:
    """Lê do cache SQLite os scores frescos de vários alunos de uma disciplina.

    Retorna {username: score_dict} apenas para entradas dentro do TTL. O que não
    estiver aqui deve ser buscado no Supabase e depois gravado com `set_scores_bulk`.
    """
    if not cache_enabled() or not usernames:
        return {}
    try:
        usernames = [str(u) for u in usernames]
        placeholders = ",".join("?" for _ in usernames)
        rows = _conn().execute(
            f"SELECT username, payload, synced_at FROM _score_cache "
            f"WHERE subject_id = ? AND username IN ({placeholders})",
            (str(subject_id), *usernames),
        ).fetchall()
        out = {}
        for username, payload, synced_at in rows:
            age = _age_seconds(synced_at)
            if age is not None and age < ttl:
                out[username] = json.loads(payload)
        return out
    except Exception:
        return {}


def set_scores_bulk(subject_id, scores: dict):
    """Grava {username: score_dict} no cache SQLite (upsert)."""
    if not cache_enabled() or not scores:
        return
    try:
        now = _now()
        payload_rows = [
            (str(u), str(subject_id), json.dumps(s, ensure_ascii=False, default=str), now)
            for u, s in scores.items()
        ]
        with _LOCK:
            conn = _conn()
            conn.executemany(
                "INSERT INTO _score_cache (username, subject_id, payload, synced_at) "
                "VALUES (?, ?, ?, ?) "
                "ON CONFLICT(username, subject_id) DO UPDATE SET "
                "payload=excluded.payload, synced_at=excluded.synced_at",
                payload_rows,
            )
            conn.commit()
    except Exception:
        pass


def invalidate_scores(subject_id=None):
    """Invalida o cache de scores (de uma disciplina ou tudo)."""
    if not cache_enabled():
        return
    try:
        with _LOCK:
            conn = _conn()
            if subject_id is None:
                conn.execute("DELETE FROM _score_cache")
            else:
                conn.execute("DELETE FROM _score_cache WHERE subject_id = ?", (str(subject_id),))
            conn.commit()
    except Exception:
        pass


def invalidate(cache_key: str = None):
    """Limpa uma chave (ou tudo, se cache_key=None). No-op se o cache estiver off."""
    if not cache_enabled():
        return
    try:
        with _LOCK:
            conn = _conn()
            if cache_key is None:
                conn.execute("DELETE FROM _cache_blob")
            else:
                conn.execute("DELETE FROM _cache_blob WHERE cache_key = ?", (cache_key,))
            conn.commit()
    except Exception:
        pass


def invalidate_prefix(prefix: str):
    """Limpa todas as chaves que começam com `prefix` (ex.: 'lessons_subject:')."""
    if not cache_enabled():
        return
    try:
        with _LOCK:
            conn = _conn()
            conn.execute("DELETE FROM _cache_blob WHERE cache_key LIKE ?", (prefix + "%",))
            conn.commit()
    except Exception:
        pass


def status() -> dict:
    """Resumo do cache para exibir na UI."""
    if not cache_enabled():
        return {"enabled": False, "path": _CACHE_DB, "entries": []}
    try:
        rows = _conn().execute(
            "SELECT cache_key, row_count, synced_at FROM _cache_blob ORDER BY cache_key"
        ).fetchall()
        entries = [
            {
                "key": r[0],
                "rows": r[1],
                "synced_at": r[2],
                "age_min": round((_age_seconds(r[2]) or 0) / 60, 1),
            }
            for r in rows
        ]
        return {"enabled": True, "path": _CACHE_DB, "entries": entries}
    except Exception as e:
        return {"enabled": True, "path": _CACHE_DB, "entries": [], "error": str(e)}
