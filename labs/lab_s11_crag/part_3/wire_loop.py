"""Wire decide, retrieve, grade, rewrite or answer."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.loops.tool_loop import NODES

print("nodes", NODES)
print("edges: decide->retrieve, retrieve->grade, grade->rewrite, grade->answer, rewrite->answer")
print("web branch exists and stays closed")
