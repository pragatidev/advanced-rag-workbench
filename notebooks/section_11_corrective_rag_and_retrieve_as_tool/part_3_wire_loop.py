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

from rag.loops.crag import WEB_SEARCH_ENABLED, maybe_web
from rag.loops.tool_loop import EDGES, NODES

for i, node in enumerate(NODES, start=1):
    print(f"node {i} {node}")

print()
print(f"{'from':<12}{'to':<12}when")
for src, dst, when in EDGES:
    print(f"{src:<12}{dst:<12}{when}")

print()
print("web branch WEB_SEARCH_ENABLED", WEB_SEARCH_ENABLED)
print("maybe_web", maybe_web("What does TS-999 mean?"))

for src, dst, _when in EDGES:
    assert src in NODES, src
    assert dst in NODES, dst
print("edge table checked against NODES")
