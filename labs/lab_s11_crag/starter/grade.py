"""STARTER Grade the retrieved set. Fill the TODOs. part_1 is the first working slice."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO: import the package symbols this lab needs

from rag.chunkers import Chunk
from rag.loops.crag import grade
from rag.retrieve import Hit


def _hits(text: str) -> list[Hit]:
    return [Hit(Chunk("c", "d", "t", text), 1.0, "x")]


empty = grade("anything", [])
good = grade(
    "TS-999",
    _hits(
        "TS-999 means the billing ledger rejected a duplicate invoice ID. It is not retryable"
    ),
)
thin = grade("What does TS-999 mean?", _hits("TS-999 means duplicate invoice"))
warehouse = grade(
    "What does TS-999 mean?",
    _hits("Warehouse throughput improved."),
)
print("empty", empty)
print("good", good)
print("thin", thin)
print("warehouse", warehouse)
