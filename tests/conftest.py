"""Fixtures globais dos testes do SysAva.

Mantém a raiz do projeto no sys.path (mesmo bootstrap dos scripts em
subpastas, regra do AGENTS.md). Fixtures específicas ficam junto dos testes.
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
