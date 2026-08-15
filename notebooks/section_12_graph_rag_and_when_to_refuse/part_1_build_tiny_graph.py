# %% [markdown]
# # Build a tiny graph on the sample corpus
#
# Lab `lab_s12_graph` / `part_1`.

# %%
"""Build a tiny graph on the sample corpus."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.graph.tiny import build

g = build()
print("nodes", g["nodes"])
print("members", g["members"])
print("communities", list(g["communities"]))
