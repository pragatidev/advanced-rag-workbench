# %% [markdown]
# # Wire decide, retrieve, grade, rewrite or answer
#
# Lab `lab_s11_crag` / `part_3`.

# %%
"""Wire decide, retrieve, grade, rewrite or answer."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.loops.tool_loop import NODES

print("nodes", NODES)
print("edges: decide->retrieve, retrieve->grade, grade->rewrite, grade->answer, rewrite->answer")
print("web branch exists and stays closed")
