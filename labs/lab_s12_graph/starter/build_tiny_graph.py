"""STARTER Build a tiny graph on the sample corpus. Fill the TODOs. part_1 is the first working slice."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO: import the package symbols this lab needs

from rag.graph.tiny import build

g = build()
print("nodes", g["nodes"])
print("members", g["members"])
print("communities", list(g["communities"]))
