"""Backend SQLite local do SysAva.

Implementa o subconjunto do query builder do Supabase/PostgREST usado pelo
projeto (``services/database.py``, ``views/admin.py`` e ``views/portal.py``)
sobre o espelho local ``data/escola_ativa.db``.

A ideia é permitir o modo local/offline sem reescrever a camada de dados:

    supa.table("lessons").select("id, title").eq("subject_id", 3).order("id").execute()

O modo é escolhido em ``services/database.py`` por ``SYSAVA_DB_MODE``
(``auto``, ``online`` ou ``local``). O caminho do banco pode ser trocado por
``SYSAVA_SQLITE_PATH`` (útil para testes).
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import threading
import unicodedata
import uuid
from datetime import datetime, timezone

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_PATH = os.path.join(PROJECT_ROOT, "data", "escola_ativa.db")

_WRITE_LOCK = threading.RLock()

# Colunas JSON (o Supabase devolve list/dict; o SQLite guarda texto).
_JSON_COLS = {
    "subjects": {"aliases"},
    "master_config": {"value"},
    "quiz_questions": {"options"},
    "assessment_questions": {"options"},
}
# Colunas booleanas no espelho (TEXT "0"/"1" no SQLite).
_BOOL_COLS = {
    "app_users": {"is_active"},
    "class_subjects": {"is_active"},
    "attendance": {"is_present"},
    "historico_aulas": {"is_duplicate"},
}
# Colunas que o app indexa/usa como inteiro.
_INT_COLS = {
    "quiz_questions": {"correct_option_index"},
    "assessment_questions": {"correct_option_index"},
}


def db_path() -> str:
    return os.environ.get("SYSAVA_SQLITE_PATH") or DEFAULT_DB_PATH


def available() -> bool:
    return os.path.exists(db_path())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _quote(ident: str) -> str:
    return '"' + str(ident).replace('"', '""') + '"'


def _split_top(text: str, sep: str = ",") -> list[str]:
    out, buf, depth = [], [], 0
    for ch in text or "":
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == sep and depth == 0:
            out.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    if "".join(buf).strip():
        out.append("".join(buf).strip())
    return out


def _norm(value) -> str:
    s = unicodedata.normalize("NFKD", str(value or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^A-Za-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


class SQLiteResponse:
    """Objeto parecido com a APIResponse do Supabase (data/count/error)."""

    def __init__(self, data=None, count=None, error=None):
        self.data = data if data is not None else []
        self.count = count
        self.error = error

    def __iter__(self):
        # Compatibilidade com `response, error = ....execute()` (código legado).
        yield self
        yield self.error


class _NotProxy:
    def __init__(self, query):
        self.query = query

    def is_(self, col, value):
        self.query._negate = True
        return self.query.is_(col, value)

    def eq(self, col, value):
        self.query._negate = True
        return self.query.eq(col, value)

    def in_(self, col, values):
        self.query._negate = True
        return self.query.in_(col, values)


class SQLiteClient:
    def __init__(self, path: str | None = None):
        self.path = path or db_path()

    def available(self) -> bool:
        return os.path.exists(self.path)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=10, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA busy_timeout=10000")
            conn.execute("PRAGMA journal_mode=WAL")
        except sqlite3.Error:
            pass
        return conn

    def table(self, name: str) -> "SQLiteQuery":
        return SQLiteQuery(self, name)

    def rpc(self, name: str, params: dict | None = None) -> "SQLiteRpc":
        return SQLiteRpc(self, name, params or {})


class SQLiteQuery:
    def __init__(self, client: SQLiteClient, table: str):
        self.client = client
        self.table = table
        self._op = "select"
        self._select = "*"
        self._count = None
        self._head = False
        self._filters = []
        self._orders = []
        self._limit = None
        self._payload = None
        self._on_conflict = None
        self._negate = False

    # ---------------------------------------------------------------- filtros
    def _add(self, col, op, value):
        negate = self._negate
        self._negate = False
        self._filters.append((col, op, value, negate))
        return self

    def eq(self, col, value):
        return self._add(col, "=", value)

    def neq(self, col, value):
        return self._add(col, "!=", value)

    def gt(self, col, value):
        return self._add(col, ">", value)

    def gte(self, col, value):
        return self._add(col, ">=", value)

    def lt(self, col, value):
        return self._add(col, "<", value)

    def lte(self, col, value):
        return self._add(col, "<=", value)

    def in_(self, col, values):
        return self._add(col, "IN", list(values or []))

    def like(self, col, value):
        return self._add(col, "LIKE", value)

    def ilike(self, col, value):
        return self._add(col, "ILIKE", value)

    def is_(self, col, value):
        return self._add(col, "IS", value)

    @property
    def not_(self):
        return _NotProxy(self)

    # ------------------------------------------------------------ operações
    def select(self, columns: str = "*", count: str | None = None, head: bool = False):
        self._op = "select"
        self._select = columns or "*"
        self._count = count
        self._head = bool(head)
        return self

    def order(self, col, desc: bool = False, **kwargs):
        self._orders.append((col, bool(desc)))
        return self

    def limit(self, n):
        self._limit = int(n)
        return self

    def range(self, start, end):
        self._limit = max(0, int(end) - int(start) + 1)
        return self

    def insert(self, payload):
        self._op = "insert"
        self._payload = payload
        return self

    def update(self, payload):
        self._op = "update"
        self._payload = payload
        return self

    def delete(self):
        self._op = "delete"
        return self

    def upsert(self, payload, on_conflict: str | None = None):
        self._op = "upsert"
        self._payload = payload
        self._on_conflict = on_conflict
        return self

    # --------------------------------------------------------------- execute
    def execute(self):
        if self._op == "select":
            return self._select_exec()
        if self._op == "insert":
            return self._insert_exec()
        if self._op == "update":
            return self._update_exec()
        if self._op == "delete":
            return self._delete_exec()
        if self._op == "upsert":
            return self._upsert_exec()
        return SQLiteResponse([])

    # --------------------------------------------------------------- helpers
    def _table_info(self, conn):
        try:
            return {
                row[1]: (row[2] or "").upper()
                for row in conn.execute(f'PRAGMA table_info({_quote(self.table)})')
            }
        except sqlite3.Error:
            return {}

    def _where(self):
        parts, params = [], []
        for col, op, value, negate in self._filters:
            qcol = _quote(col)
            if op == "IN":
                values = list(value or [])
                if not values:
                    parts.append("0=1" if not negate else "1=1")
                    continue
                ph = ",".join("?" for _ in values)
                parts.append(f"{qcol} {'NOT ' if negate else ''}IN ({ph})")
                params.extend(values)
            elif op == "IS":
                val = "null" if value is None else str(value).strip().lower()
                if val in ("null", "none"):
                    parts.append(f"{qcol} IS {'NOT ' if negate else ''}NULL")
                elif val in ("true", "false", "1", "0"):
                    b = 1 if val in ("true", "1") else 0
                    parts.append(f"{qcol} IS {'NOT ' if negate else ''}{b}")
                else:
                    parts.append(f"{qcol} IS {'NOT ' if negate else ''}?")
                    params.append(value)
            elif op == "ILIKE":
                parts.append(f"LOWER({qcol}) {'NOT ' if negate else ''}LIKE LOWER(?)")
                params.append(value)
            elif op == "LIKE":
                parts.append(f"{qcol} {'NOT ' if negate else ''}LIKE ?")
                params.append(value)
            else:
                if negate:
                    parts.append(f"NOT ({qcol} {op} ?)")
                else:
                    parts.append(f"{qcol} {op} ?")
                params.append(value)
        where = (" WHERE " + " AND ".join(parts)) if parts else ""
        return where, params

    def _coerce(self, conn, col, value):
        if value is None:
            return None
        if col in _JSON_COLS.get(self.table, set()) and isinstance(value, str):
            try:
                return json.loads(value)
            except (TypeError, ValueError):
                return value
        if col in _BOOL_COLS.get(self.table, set()):
            if isinstance(value, str):
                return value.strip().lower() in ("1", "true", "t", "yes", "sim")
            return bool(value)
        if col in _INT_COLS.get(self.table, set()):
            try:
                return int(value)
            except (TypeError, ValueError):
                return value
        return value

    def _write_value(self, col, value):
        if col in _JSON_COLS.get(self.table, set()) and isinstance(value, (list, dict)):
            return json.dumps(value, ensure_ascii=False)
        if col in _BOOL_COLS.get(self.table, set()):
            return 1 if bool(value) else 0
        return value

    def _row(self, col_info, row):
        return {
            key: self._coerce(None, key, row[key])
            for key in row.keys()
        }

    def _prepare(self, conn, col_info, payload, update=False):
        data = {}
        for key, value in (payload or {}).items():
            if key not in col_info:
                print(f"[SQLite] coluna ignorada em {self.table}: {key}")
                continue
            data[key] = self._write_value(key, value)
        if update:
            if "updated_at" in col_info and not data.get("updated_at"):
                data["updated_at"] = _now()
            return data
        if "id" in col_info and "id" not in data:
            if "INT" not in (col_info.get("id") or ""):
                # Os IDs do espelho sao numericos em TEXT; manter o padrao para
                # nao quebrar codigo que faz int(id) nem referencias existentes.
                try:
                    mx = conn.execute(
                        f'SELECT MAX(CAST(id AS INTEGER)) FROM {_quote(self.table)}'
                    ).fetchone()[0]
                except sqlite3.Error:
                    mx = 0
                data["id"] = str(int(mx or 0) + 1)
        if "created_at" in col_info and not data.get("created_at"):
            data["created_at"] = _now()
        if "updated_at" in col_info and not data.get("updated_at"):
            data["updated_at"] = _now()
        return data

    def _unique_cols(self, conn, data):
        try:
            indexes = list(conn.execute(f'PRAGMA index_list({_quote(self.table)})'))
        except sqlite3.Error:
            return []
        for idx in indexes:
            if not idx[2]:  # not unique
                continue
            cols = [r[2] for r in conn.execute(f'PRAGMA index_info({_quote(idx[1])})')]
            if cols and all(c in data for c in cols):
                return cols
        return []

    def _fetch_by(self, conn, col_info, data, lastrowid=None):
        if "id" in data and "id" in col_info:
            row = conn.execute(
                f'SELECT * FROM {_quote(self.table)} WHERE id = ?', (data["id"],)
            ).fetchone()
        elif lastrowid is not None and "id" in col_info:
            row = conn.execute(
                f'SELECT * FROM {_quote(self.table)} WHERE id = ?', (lastrowid,)
            ).fetchone()
        elif "username" in data and "username" in col_info:
            row = conn.execute(
                f'SELECT * FROM {_quote(self.table)} WHERE username = ?', (data["username"],)
            ).fetchone()
        else:
            unique = self._unique_cols(conn, data)
            if unique:
                where = " AND ".join(f'{_quote(c)} = ?' for c in unique)
                row = conn.execute(
                    f'SELECT * FROM {_quote(self.table)} WHERE {where}',
                    [data[c] for c in unique],
                ).fetchone()
            else:
                return dict(data)
        return self._row(col_info, row) if row is not None else dict(data)

    # ---------------------------------------------------------------- select
    def _select_exec(self):
        with self.client._connect() as conn:
            col_info = self._table_info(conn)
            base_cols, embeds = self._parse_select()
            if embeds and base_cols != ["*"]:
                for rel, _inner, _selected in embeds:
                    mapping = self._relation(rel)
                    if not mapping:
                        continue
                    fk = mapping[0]
                    if _quote(fk) not in base_cols:
                        base_cols.append(_quote(fk))
            where, params = self._where()
            count = None
            if self._count == "exact":
                row = conn.execute(
                    f'SELECT COUNT(*) FROM {_quote(self.table)}{where}', params
                ).fetchone()
                count = row[0] if row else 0
            if self._head or self._limit == 0:
                return SQLiteResponse([], count)

            cols_sql = ", ".join(base_cols)
            sql = f'SELECT {cols_sql} FROM {_quote(self.table)}{where}'
            if self._orders:
                sql += " ORDER BY " + ", ".join(
                    f'{_quote(c)} {"DESC" if d else "ASC"}' for c, d in self._orders
                )
            if self._limit is not None:
                sql += f" LIMIT {int(self._limit)}"
            rows = [self._row(col_info, r) for r in conn.execute(sql, params)]
            if embeds:
                rows = self._attach_embeds(conn, rows, embeds)
            return SQLiteResponse(rows, count)

    def _parse_select(self):
        base, embeds = [], []
        for part in _split_top(self._select):
            if not part:
                continue
            if part == "*":
                base.append("*")
                continue
            m = re.match(r"^([A-Za-z0-9_]+)(!inner)?\((.*)\)$", part, re.I)
            if m:
                rel, inner, cols = m.group(1), bool(m.group(2)), m.group(3)
                embeds.append((rel, inner, cols or "*"))
            else:
                base.append(_quote(part))
        if not base:
            base = ["*"]
        return base, embeds

    def _relation(self, rel):
        if rel == "app_users":
            if self.table == "student_assessments":
                return "user_username", "username"
            if self.table == "forum_posts":
                return "user_name", "name"
        if rel == "subjects" and self.table == "class_subjects":
            return "subject_id", "id"
        return None

    def _attach_embeds(self, conn, rows, embeds):
        for rel, inner, selected in embeds:
            mapping = self._relation(rel)
            if not mapping or not rows:
                continue
            local_fk, remote_pk = mapping
            values = []
            for r in rows:
                v = r.get(local_fk)
                if v is not None and v not in values:
                    values.append(v)
            related = {}
            if values:
                cols = "*" if selected.strip() == "*" else ", ".join(
                    _quote(c) for c in _split_top(selected)
                )
                if selected.strip() != "*":
                    cols += f", {_quote(remote_pk)}"
                    if rel == "app_users":
                        cols += ", username"
                ph = ",".join("?" for _ in values)
                sql = f'SELECT {cols} FROM {_quote(rel)} WHERE {_quote(remote_pk)} IN ({ph})'
                for rr in conn.execute(sql, values):
                    item = {k: rr[k] for k in rr.keys()}
                    key = str(item.get(remote_pk))
                    if rel == "app_users":
                        item.setdefault("username", item.get("username") or key)
                    if rel == "subjects":
                        item.setdefault("id", item.get(remote_pk))
                    related[key] = item
            new_rows = []
            for r in rows:
                key = str(r.get(local_fk))
                item = related.get(key)
                if item is None and inner:
                    continue
                r[rel] = item
                new_rows.append(r)
            rows = new_rows
        return rows

    # ---------------------------------------------------------------- insert
    def _insert_exec(self):
        payload = self._payload
        items = payload if isinstance(payload, list) else [payload]
        out = []
        with _WRITE_LOCK:
            with self.client._connect() as conn:
                col_info = self._table_info(conn)
                for item in items:
                    data = self._prepare(conn, col_info, item or {}, update=False)
                    if not data:
                        continue
                    cols = [_quote(c) for c in data]
                    ph = ",".join("?" for _ in data)
                    cur = conn.execute(
                        f'INSERT INTO {_quote(self.table)} ({", ".join(cols)}) VALUES ({ph})',
                        list(data.values()),
                    )
                    out.append(self._fetch_by(conn, col_info, data, cur.lastrowid))
                conn.commit()
        return SQLiteResponse(out)

    # ---------------------------------------------------------------- update
    def _update_exec(self):
        payload = self._payload or {}
        with _WRITE_LOCK:
            with self.client._connect() as conn:
                col_info = self._table_info(conn)
                data = self._prepare(conn, col_info, payload, update=True)
                if not data:
                    return SQLiteResponse([])
                where, params = self._where()
                sets = ", ".join(f"{_quote(c)} = ?" for c in data)
                conn.execute(
                    f'UPDATE {_quote(self.table)} SET {sets}{where}',
                    list(data.values()) + params,
                )
                conn.commit()
                rows = [
                    self._row(col_info, r)
                    for r in conn.execute(
                        f'SELECT * FROM {_quote(self.table)}{where}', params
                    )
                ]
        return SQLiteResponse(rows)

    # ---------------------------------------------------------------- delete
    def _delete_exec(self):
        with _WRITE_LOCK:
            with self.client._connect() as conn:
                col_info = self._table_info(conn)
                where, params = self._where()
                antes = [
                    self._row(col_info, r)
                    for r in conn.execute(
                        f'SELECT * FROM {_quote(self.table)}{where}', params
                    )
                ]
                conn.execute(f'DELETE FROM {_quote(self.table)}{where}', params)
                conn.commit()
        return SQLiteResponse(antes)

    # ---------------------------------------------------------------- upsert
    def _upsert_exec(self):
        payload = self._payload
        items = payload if isinstance(payload, list) else [payload]
        out = []
        with _WRITE_LOCK:
            with self.client._connect() as conn:
                col_info = self._table_info(conn)
                for item in items:
                    data = self._prepare(conn, col_info, item or {}, update=False)
                    if not data:
                        continue
                    cols = [_quote(c) for c in data]
                    ph = ",".join("?" for _ in data)
                    conflict = []
                    if self._on_conflict:
                        conflict = [c.strip() for c in self._on_conflict.split(",") if c.strip()]
                    if not conflict:
                        conflict = self._unique_cols(conn, data)
                    if conflict:
                        updates = [c for c in data if c not in conflict]
                        if updates:
                            set_sql = ", ".join(
                                f"{_quote(c)} = excluded.{_quote(c)}" for c in updates
                            )
                            action = f"DO UPDATE SET {set_sql}"
                        else:
                            action = "DO NOTHING"
                        sql = (
                            f'INSERT INTO {_quote(self.table)} ({", ".join(cols)}) '
                            f'VALUES ({ph}) ON CONFLICT ({", ".join(_quote(c) for c in conflict)}) {action}'
                        )
                    else:
                        sql = (
                            f'INSERT OR REPLACE INTO {_quote(self.table)} ({", ".join(cols)}) '
                            f'VALUES ({ph})'
                        )
                    cur = conn.execute(sql, list(data.values()))
                    out.append(self._fetch_by(conn, col_info, data, cur.lastrowid))
                conn.commit()
        return SQLiteResponse(out)


class SQLiteRpc:
    def __init__(self, client: SQLiteClient, name: str, params: dict):
        self.client = client
        self.name = name
        self.params = params or {}

    def execute(self):
        name = (self.name or "").lower()
        with self.client._connect() as conn:
            if name == "resolver_subject_exato":
                alvo = _norm(self.params.get("p_nome") or self.params.get("p_name") or "")
                for row in conn.execute("SELECT id, name, aliases FROM subjects"):
                    aliases = row["aliases"]
                    try:
                        aliases = json.loads(aliases) if aliases else []
                    except (TypeError, ValueError):
                        aliases = [aliases] if aliases else []
                    nomes = [row["name"]] + (aliases if isinstance(aliases, list) else [aliases])
                    if any(_norm(n) == alvo for n in nomes if n):
                        return SQLiteResponse([{"resolver_subject_exato": row["id"]}])
                return SQLiteResponse([])

            if name == "f_fuzzy_match":
                alvo = _norm(self.params.get("p_name") or self.params.get("p_nome") or "")
                melhor = None
                for row in conn.execute("SELECT id, name FROM subjects ORDER BY name"):
                    nome = _norm(row["name"])
                    if nome == alvo:
                        melhor = row
                        break
                    if alvo and (alvo in nome or nome in alvo):
                        melhor = melhor or row
                if melhor:
                    return SQLiteResponse([{"id": melhor["id"], "name": melhor["name"]}])
                return SQLiteResponse([])

            if name == "resolver_subject_raiz":
                try:
                    atual = int(self.params.get("p_id"))
                except (TypeError, ValueError):
                    return SQLiteResponse([])
                for _ in range(10):
                    row = conn.execute(
                        "SELECT aliases_id FROM subjects WHERE id = ?", (atual,)
                    ).fetchone()
                    if not row or row["aliases_id"] is None:
                        break
                    try:
                        atual = int(row["aliases_id"])
                    except (TypeError, ValueError):
                        break
                return SQLiteResponse([{"resolver_subject_raiz": atual}])

        return SQLiteResponse([])
