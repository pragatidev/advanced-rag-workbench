# %% [markdown]
# # Pack winners at the ends of the prompt
#
# Lab `lab_s8_rerank` / `part_3`.

# %%
"""Pack winners at the ends of the prompt."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import Chunk
from rag.rerank import pack_ends, pack_prompt
from rag.retrieve import Hit

hits = [
    Hit(chunk=Chunk("c1", "d", "t", "middle fact"), score=0.4, source="x"),
    Hit(chunk=Chunk("c2", "d", "t", "best TS-999"), score=0.9, source="x"),
    Hit(chunk=Chunk("c3", "d", "t", "second best"), score=0.7, source="x"),
    Hit(chunk=Chunk("c4", "d", "t", "other"), score=0.5, source="x"),
]
packed = pack_ends(hits)
print("order", [h.chunk.chunk_id for h in packed])
print("first is best", packed[0].chunk.chunk_id == "c2")
print("last is second", packed[-1].chunk.chunk_id == "c3")
print(pack_prompt("What does TS-999 mean?", hits)[:400])
