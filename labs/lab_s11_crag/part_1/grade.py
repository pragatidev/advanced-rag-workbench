"""Grade the retrieved set."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import Chunk
from rag.loops.crag import grade
from rag.retrieve import Hit

empty = grade("anything", [])
good = grade(
    "What does TS-999 mean?",
    [Hit(Chunk("c", "d", "t", "TS-999 means duplicate invoice"), 1.0, "x")],
)
weak = grade(
    "What does TS-999 mean?",
    [Hit(Chunk("c", "d", "t", "restart the worker"), 0.2, "x")],
)
print("empty", empty)
print("supported", good)
print("weak", weak)
