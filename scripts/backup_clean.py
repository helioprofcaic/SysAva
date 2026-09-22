"""
Backup limpo do SysAva (sem imagens Base64).

Objetivo:
- Extrair um backup portavel a partir de um banco SQLite local (por padrao
  `data/escola_ativa.db`) removendo apenas imagens embutidas em Base64
  (`data:image/...;base64,...`), preservando o SVG vetorial puro.
- Gerar um SQLite "limpo" + um dump JSONL por tabela + um manifesto com
  contagem de linhas e bytes economizados.

Uso:
    python scripts/backup_clean.py
    python scripts/backup_clean.py --source data/escola_ativa.db
    python scripts/backup_clean.py --source data/escola_ativa.db --out data/backup_clean_2026-09-22
"""

import argparse
import json
import os
import re
import shutil
import sqlite3
import sys
from datetime import datetime

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

_SVG_BLOCK = re.compile(r"<svg\b[^>]*?>.*?</svg>", re.IGNORECASE | re.DOTALL)
_MD_BASE64_IMG = re.compile(r"!\[[^\]]*\]\(\s*data:[^)]*;base64,[^)]*\)", re.IGNORECASE | re.DOTALL)
_MD_BASE64_LINK = re.compile(r"\]\(\s*data:[^)]*;base64,[^)]*\)", re.IGNORECASE | re.DOTALL)
_DATA_URI = re.compile(r"data:image/[a-zA-Z0-9.+-]+;base64,[A-Za-z0-9+/=\s]+", re.IGNORECASE)
_TITLE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def strip_base64(text):
    """Remove imagens Base64 de um texto, preservando SVG vetorial puro.

    Retorna (texto_limpo, bytes_removidos, blocos_removidos).
    """
    if not text or "base64" not in text:
        return text, 0, 0

    original_len = len(text)
    removed_blocks = 0

    def _svg_repl(match):
        nonlocal removed_blocks
        block = match.group(0)
        if "base64" not in block.lower():
            return block
        removed_blocks += 1
        title = _TITLE.search(block)
        label = title.group(1).strip() if title else ""
        if label:
            return f"\n\n> 🎨 **Ilustração:** *{label}*\n\n"
        return "\n"

    text = _SVG_BLOCK.sub(_svg_repl, text)
    text = _MD_BASE64_IMG.sub("", text)
    text = _MD_BASE64_LINK.sub("]", text)
    text = _DATA_URI.sub("", text)

    return text, max(0, original_len - len(text)), removed_blocks


def _table_columns(conn, table):
    return [(r[1], r[2]) for r in conn.execute(f'PRAGMA table_info("{table}")')]


def _table_names(conn):
    return [
        r[0]
        for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
    ]


def build_clean_backup(source, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    clean_db = os.path.join(out_dir, "backup_clean.db")
    dump_dir = os.path.join(out_dir, "dump")
    os.makedirs(dump_dir, exist_ok=True)

    src = sqlite3.connect(source)
    dst = sqlite3.connect(clean_db)
    src.row_factory = sqlite3.Row

    manifest = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source": os.path.abspath(source),
        "source_bytes": os.path.getsize(source),
        "tables": {},
    }

    for table in _table_names(src):
        cols = _table_columns(src, table)
        col_names = [c[0] for c in cols]
        text_cols = [c[0] for c in cols if (c[1] or "").upper() in ("TEXT", "CLOB", "")]

        rows = src.execute(f'SELECT * FROM "{table}"').fetchall()

        ddl_cols = ", ".join(f'"{c[0]}" {c[1] or "TEXT"}' for c in cols)
        dst.execute(f'DROP TABLE IF EXISTS "{table}"')
        dst.execute(f'CREATE TABLE "{table}" ({ddl_cols})')

        removed_bytes = 0
        removed_blocks = 0
        out_rows = []
        for row in rows:
            values = []
            for col in col_names:
                val = row[col]
                if col in text_cols and isinstance(val, str) and "base64" in val.lower():
                    val, rb, rc = strip_base64(val)
                    removed_bytes += rb
                    removed_blocks += rc
                values.append(val)
            out_rows.append(values)

        if out_rows:
            placeholders = ", ".join(["?"] * len(col_names))
            quoted = ", ".join(f'"{c}"' for c in col_names)
            dst.executemany(
                f'INSERT INTO "{table}" ({quoted}) VALUES ({placeholders})', out_rows
            )

        with open(os.path.join(dump_dir, f"{table}.jsonl"), "w", encoding="utf-8") as f:
            for values in out_rows:
                f.write(json.dumps(dict(zip(col_names, values)), ensure_ascii=False) + "\n")

        manifest["tables"][table] = {
            "rows": len(out_rows),
            "base64_bytes_removed": removed_bytes,
            "base64_blocks_removed": removed_blocks,
        }

    dst.commit()
    dst.close()
    src.close()

    manifest["clean_bytes"] = os.path.getsize(clean_db)
    manifest["bytes_saved"] = max(0, manifest["source_bytes"] - manifest["clean_bytes"])

    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    return manifest, clean_db


def main():
    parser = argparse.ArgumentParser(description="Backup limpo do SysAva sem Base64.")
    parser.add_argument(
        "--source",
        default=os.path.join(project_root, "data", "escola_ativa.db"),
        help="Banco SQLite de origem (padrao: data/escola_ativa.db).",
    )
    parser.add_argument(
        "--out",
        default=os.path.join(
            project_root, "data", f"backup_clean_{datetime.now().strftime('%Y-%m-%d_%H%M')}"
        ),
        help="Pasta de destino do backup.",
    )
    args = parser.parse_args()

    if not os.path.exists(args.source):
        print(f"[ERRO] Origem nao encontrada: {args.source}")
        return 1

    print(f"Origem : {args.source}")
    print(f"Destino: {args.out}\n")

    manifest, clean_db = build_clean_backup(args.source, args.out)

    total_removed = sum(t["base64_bytes_removed"] for t in manifest["tables"].values())
    total_blocks = sum(t["base64_blocks_removed"] for t in manifest["tables"].values())

    for table, info in manifest["tables"].items():
        flag = "  <-- base64 removido" if info["base64_blocks_removed"] else ""
        print(f"  {table:30s} linhas={info['rows']:<6} {flag}")
        if info["base64_blocks_removed"]:
            print(
                f"      blocos base64 removidos={info['base64_blocks_removed']} "
                f"bytes={info['base64_bytes_removed']:,}"
            )

    print(f"\nBanco limpo : {clean_db} ({manifest['clean_bytes']:,} bytes)")
    print(f"Bytes totais removidos : {total_removed:,}")
    print(f"Blocos base64 removidos: {total_blocks}")
    print(f"Economia total de arquivo: {manifest['bytes_saved']:,} bytes")
    print(f"\nManifesto: {os.path.join(args.out, 'manifest.json')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
