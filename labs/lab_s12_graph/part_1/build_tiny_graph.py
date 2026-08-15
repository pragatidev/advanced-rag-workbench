"""Build a tiny graph on the sample corpus."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.graph.tiny import build

g = build()
print("nodes", g["nodes"])
print("members", g["members"])
print("communities", list(g["communities"]))
