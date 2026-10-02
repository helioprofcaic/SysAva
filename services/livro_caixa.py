"""Livro-caixa de aulas — IS-045 / AP-016.

Model' somente leitura entre o banco e os front-ends Streamlit: resolve a
estrutura de blocos semanais com zonas livres

    {01-08} {09-16} [LIVRE] {17-24} {25-32} [LIVRE]

em uma fila posicional (`entradas`) que o gerador de planos consuma.
Fechamento por horas (meta `max_hours`), não por contagem de linhas.

O documento mora na tabela `master_config` do SQLite local
(`escola_ativa.db`), chave `livro_caixa:<subject_id>` — mesmo padrão de
`feriados.json` — e é espelhado para o Supabase pelo ``audit_backup``.

Regras fechadas no IS-045:
- NADA escreve em ``lessons``: a estrutura não afeta conteúdo nem
  relações (quizzes, fórum, histórico).
- A posição (``AULA_NUM`` no .txt / ``numero_aula`` no plano) é
  figurante: só guarda a posição no portal e PODE divergir do número do
  título (título 17 pode ficar na posição 20).
- Aula especial não é conteúdo: não aparece na página Aulas; é avaliação
  (plugin Atividades) e ocupa a posição do livro com o título lançado lá.
- Disciplina sem documento (ou ``estrutura: linear``) = fila legada por
  título, sem mudança de comportamento.

Uso típico::

    from services import livro_caixa
    doc = livro_caixa.carregar(subject_id)      # dict | None
    livro_caixa.salvar(livro_caixa.estrutura_padrao(subject_id, 40))
    entradas = livro_caixa.resolver(doc)        # [{'pos','tipo',...}, ...]
    rel = livro_caixa.conferir(doc)             # {'ok','erros','avisos',...}
"""

import json
import os
import re
import sqlite3
from datetime import datetime

PREFIXO = "livro_caixa:"
VERSAO = 1
TIPOS_ESPECIAIS = ("Avaliação", "Seminário", "Pesquisa", "Oficina",
                   "Revisão", "Apresentação", "Outro")
PADRAO_BLOCOS = [[1, 8], [9, 16], [17, 24], [25, 32]]

# Harness de sandbox aponta para a cópia do banco (ver docs/ISSUES_LOCAIS.md).
DB_PATH_OVERRIDE = None


# ---------------------------------------------------------------------------
# Acesso ao SQLite local (master_config)
# ---------------------------------------------------------------------------

def caminho_banco():
    if DB_PATH_OVERRIDE:
        return DB_PATH_OVERRIDE
    env = os.environ.get("SYSAVA_DB_PATH")
    if env:
        return env
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for p in (
        os.path.join(root, "data", "escola_ativa.db"),
        os.path.join(root, "escola_ativa.db"),
        os.path.join(root, "data", "automacao", "escola_ativa.db"),
    ):
        if os.path.exists(p):
            return p
    return os.path.join(root, "data", "escola_ativa.db")


def _conectar():
    caminho = caminho_banco()
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Banco não encontrado: {caminho}")
    conn = sqlite3.connect(caminho, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def _ler_bruto(chave_txt):
    try:
        conn = _conectar()
    except FileNotFoundError:
        return None
    try:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(master_config)")]
        if not cols:
            return None
        if "value" in cols:
            row = conn.execute("SELECT value FROM master_config WHERE key = ?",
                               (chave_txt,)).fetchone()
        else:
            row = conn.execute("SELECT valor FROM master_config WHERE chave = ?",
                               (chave_txt,)).fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def _gravar_bruto(chave_txt, valor_txt):
    conn = _conectar()
    try:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(master_config)")]
        if not cols:
            conn.execute('''CREATE TABLE master_config (
                            chave TEXT PRIMARY KEY,
                            valor TEXT)''')
            cols = ["chave", "valor"]
        if "key" in cols:
            cur = conn.execute("UPDATE master_config SET value = ?, "
                               "updated_at = datetime('now') WHERE key = ?",
                               (valor_txt, chave_txt))
            if cur.rowcount == 0:
                if "updated_at" in cols:
                    conn.execute("INSERT INTO master_config (key, value, updated_at) "
                                 "VALUES (?, ?, datetime('now'))",
                                 (chave_txt, valor_txt))
                else:
                    conn.execute("INSERT INTO master_config (key, value) VALUES (?, ?)",
                                 (chave_txt, valor_txt))
        else:
            cur = conn.execute("UPDATE master_config SET valor = ? WHERE chave = ?",
                               (valor_txt, chave_txt))
            if cur.rowcount == 0:
                conn.execute("INSERT INTO master_config (chave, valor) VALUES (?, ?)",
                             (chave_txt, valor_txt))
        conn.commit()
    finally:
        conn.close()


def chave_de(subject_id):
    return f"{PREFIXO}{int(subject_id)}"


# ---------------------------------------------------------------------------
# CRUD do documento
# ---------------------------------------------------------------------------

def carregar(subject_id):
    """Documento do livro-caixa da disciplina (dict) ou None."""
    bruto = _ler_bruto(chave_de(subject_id))
    if not bruto:
        return None
    try:
        doc = json.loads(bruto)
    except (ValueError, TypeError):
        return None
    if not isinstance(doc, dict):
        return None
    doc.setdefault("subject_id", int(subject_id))
    doc.setdefault("versao", VERSAO)
    return doc


def salvar(doc):
    """Persiste o documento em `master_config` (local, espelhado no Supabase)."""
    if not isinstance(doc, dict) or not doc.get("subject_id"):
        raise ValueError("Documento do livro-caixa sem subject_id.")
    doc = dict(doc)
    doc.setdefault("versao", VERSAO)
    doc["atualizado_em"] = datetime.now().isoformat(timespec="seconds")
    _gravar_bruto(chave_de(doc["subject_id"]),
                  json.dumps(doc, ensure_ascii=False))
    return chave_de(doc["subject_id"])


def remover(subject_id):
    try:
        conn = _conectar()
    except FileNotFoundError:
        return False
    try:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(master_config)")]
        if "key" in cols:
            cur = conn.execute("DELETE FROM master_config WHERE key = ?",
                               (chave_de(subject_id),))
        else:
            cur = conn.execute("DELETE FROM master_config WHERE chave = ?",
                               (chave_de(subject_id),))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


def carregar_todos():
    """{subject_id int: doc} de todos os livros-caixa cadastrados."""
    try:
        conn = _conectar()
    except FileNotFoundError:
        return {}
    try:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(master_config)")]
        if not cols:
            return {}
        col_chave = "key" if "key" in cols else "chave"
        col_valor = "value" if "value" in cols else "valor"
        rows = conn.execute(
            f"SELECT {col_chave} AS k, {col_valor} AS v FROM master_config "
            f"WHERE {col_chave} LIKE ?", (f"{PREFIXO}%",)).fetchall()
    finally:
        conn.close()
    out = {}
    for r in rows:
        sid_txt = str(r["k"])[len(PREFIXO):]
        if not sid_txt.isdigit():
            continue
        try:
            doc = json.loads(r["v"])
        except (ValueError, TypeError):
            continue
        if isinstance(doc, dict):
            doc.setdefault("subject_id", int(sid_txt))
            doc.setdefault("versao", VERSAO)
            out[int(sid_txt)] = doc
    return out


# ---------------------------------------------------------------------------
# Estruturas e resolução
# ---------------------------------------------------------------------------

def estrutura_padrao(subject_id, meta_horas=40):
    """{01-08}{09-16}[LIVRE]{17-24}{25-32}[LIVRE] com fechamento por horas."""
    return {
        "versao": VERSAO,
        "subject_id": int(subject_id),
        "estrutura": "blocos",
        "meta_horas": int(meta_horas or 40),
        "blocos": [list(b) for b in PADRAO_BLOCOS],
        "zonas": [
            {"id": "z1", "apos_bloco": 2, "itens": []},
            {"id": "z2", "apos_bloco": 4, "itens": []},
        ],
        "entradas": [],
        "resolvido_em": None,
    }


def estrutura_linear(subject_id, meta_horas=40):
    """Equivalente à fila legada: posição N = conteúdo N, sem zonas."""
    meta = int(meta_horas or 40)
    return {
        "versao": VERSAO,
        "subject_id": int(subject_id),
        "estrutura": "linear",
        "meta_horas": meta,
        "cobertura": meta,
        "zonas": [],
        "entradas": [],
        "resolvido_em": None,
    }


def resolver(doc):
    """Filas posicional resolvida: [{'pos', 'tipo', ...}] ou None se inválido.

    ``tipo`` = 'conteudo' (carrega ``aula_numero`` do bloco) ou 'especial'
    (carrega ``titulo``/``tipo_nome``/``descricao`` vindos do lançamento no
    plugin Atividades). As posições são 1..N contínuas e independentes do
    número do título — é o ``AULA_NUM`` figurante do IS-045.
    """
    if not isinstance(doc, dict):
        return None
    entradas = []
    estrutura = str(doc.get("estrutura") or "blocos").lower()

    if estrutura == "linear":
        cobertura = int(doc.get("cobertura") or doc.get("meta_horas") or 40)
        if cobertura < 1:
            return None
        for n in range(1, cobertura + 1):
            entradas.append({"pos": n, "tipo": "conteudo", "aula_numero": n})
        return entradas

    if estrutura != "blocos":
        return None

    blocos = doc.get("blocos") or []
    if not blocos:
        return None
    zonas = {}
    for z in doc.get("zonas") or []:
        try:
            zonas[int(z.get("apos_bloco"))] = z
        except (TypeError, ValueError):
            return None

    for i, bloco in enumerate(blocos, start=1):
        try:
            ini, fim = int(bloco[0]), int(bloco[1])
        except (TypeError, ValueError, IndexError):
            return None
        if ini < 1 or fim < ini:
            return None
        for n in range(ini, fim + 1):
            entradas.append({"pos": len(entradas) + 1, "tipo": "conteudo",
                             "aula_numero": n})
        zona = zonas.get(i)
        if zona:
            for item in zona.get("itens") or []:
                if not isinstance(item, dict):
                    return None
                entradas.append({
                    "pos": len(entradas) + 1,
                    "tipo": "especial",
                    "titulo": str(item.get("titulo") or "").strip(),
                    "tipo_nome": str(item.get("tipo_nome") or "Avaliação").strip(),
                    "descricao": str(item.get("descricao") or "").strip(),
                    "estrategia": str(item.get("estrategia") or "").strip(),
                    "objetivos": list(item.get("objetivos") or []),
                    "recursos": str(item.get("recursos") or "").strip(),
                    "atividade": str(item.get("atividade") or "").strip(),
                    "origem": item.get("origem") or "manual",
                    "assessment_id": item.get("assessment_id"),
                })
    return entradas or None


def _numero_aula_titulo(titulo):
    m = re.match(r"^\s*Aula\s+(\d+)", str(titulo or ""), re.IGNORECASE)
    return int(m.group(1)) if m else None


def conferir(doc, lessons=None, max_hours=None):
    """Valida a estrutura. ``lessons`` (list[{'title'}]) habilita a checagem
    de números de conteúdo ausentes; ``max_hours`` compara com a meta."""
    rel = {"ok": False, "erros": [], "avisos": [], "n_conteudo": 0,
           "n_especial": 0, "horas": 0, "meta": None, "cobertura": 0}
    if not isinstance(doc, dict):
        rel["erros"].append("Documento inválido.")
        return rel

    rel["meta"] = doc.get("meta_horas")
    rel["erros"].extend(_erros_estrutura(doc))

    entradas = resolver(doc)
    if entradas is None:
        rel["erros"].append("Estrutura não resolve (blocos/zonas inválidos).")
        return rel

    rel["cobertura"] = len(entradas)
    rel["n_conteudo"] = sum(1 for e in entradas if e["tipo"] == "conteudo")
    rel["n_especial"] = sum(1 for e in entradas if e["tipo"] == "especial")
    rel["horas"] = len(entradas)

    for e in entradas:
        if e["tipo"] == "especial" and not e.get("titulo"):
            rel["erros"].append(f"Posição {e['pos']}: aula especial sem título.")

    nums = [e["aula_numero"] for e in entradas if e["tipo"] == "conteudo"]
    vistos = set()
    for n in nums:
        if n in vistos:
            rel["erros"].append(f"Blocos duplicam a Aula {n:02d}.")
        vistos.add(n)

    meta = rel["meta"]
    if meta and rel["horas"] != int(meta):
        rel["avisos"].append(
            f"Estrutura cobre {rel['horas']} posição(ões) e a meta é {meta}h "
            "(zonas vazias ou blocos incompletos — as posições restantes caem "
            "na fila legada).")
    if max_hours and meta and int(max_hours) != int(meta):
        rel["avisos"].append(
            f"Meta do livro ({meta}h) difere de subjects.max_hours ({max_hours}h).")

    if lessons:
        numeros_lessons = set()
        for l in lessons:
            n = _numero_aula_titulo(l.get("title"))
            if n:
                numeros_lessons.add(n)
        faltando = sorted(vistos - numeros_lessons)
        for n in faltando:
            rel["avisos"].append(
                f"Aula {n:02d} prevista nos blocos não existe em `lessons` "
                "(a posição vira «sem lição» no gerador).")

    rel["ok"] = not rel["erros"]
    return rel


def _erros_estrutura(doc):
    erros = []
    estrutura = str(doc.get("estrutura") or "").lower()
    if estrutura not in ("blocos", "linear"):
        erros.append(f"Estrutura desconhecida: {doc.get('estrutura')!r}.")
        return erros
    if estrutura == "linear":
        try:
            cob = int(doc.get("cobertura") or doc.get("meta_horas") or 0)
        except (TypeError, ValueError):
            cob = 0
        if cob < 1:
            erros.append("Estrutura linear sem cobertura válida.")
        return erros

    blocos = doc.get("blocos") or []
    if not blocos:
        erros.append("Sem blocos definidos.")
        return erros
    prev_fim = 0
    for i, b in enumerate(blocos, start=1):
        try:
            ini, fim = int(b[0]), int(b[1])
        except (TypeError, ValueError, IndexError):
            erros.append(f"Bloco {i} inválido: {b!r}.")
            continue
        if ini < 1 or fim < ini:
            erros.append(f"Bloco {i} fora de ordem: {b!r}.")
        elif ini != prev_fim + 1:
            erros.append(f"Bloco {i} ({ini}-{fim}) não continua o anterior "
                         f"(esperado a partir de {prev_fim + 1}).")
        prev_fim = max(prev_fim, fim)

    n_blocos = len(blocos)
    for z in doc.get("zonas") or []:
        zid = z.get("id") or "?"
        try:
            pos = int(z.get("apos_bloco"))
        except (TypeError, ValueError):
            erros.append(f"Zona {zid}: `apos_bloco` inválido.")
            continue
        if pos < 1 or pos > n_blocos:
            erros.append(f"Zona {zid}: aponta para o bloco {pos} "
                         f"(existem {n_blocos}).")
        for item in z.get("itens") or []:
            if not isinstance(item, dict) or not str(item.get("titulo") or "").strip():
                erros.append(f"Zona {zid}: item sem título.")
    return erros


def resolver_e_marcar(doc):
    """Resolve e devolve o doc com `entradas`/`resolvido_em` preenchidos
    (a gravação em `master_config` é responsabilidade do chamador)."""
    entradas = resolver(doc)
    if entradas is None:
        return None
    doc = dict(doc)
    doc["entradas"] = entradas
    doc["resolvido_em"] = datetime.now().isoformat(timespec="seconds")
    return doc
