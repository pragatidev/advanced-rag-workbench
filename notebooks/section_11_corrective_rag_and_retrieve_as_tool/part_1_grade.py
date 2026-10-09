# %% [markdown]
# # Grade the retrieved set
#
# Lab `lab_s11_crag` / `part_1`.

# %%
"""Grade the retrieved set."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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
