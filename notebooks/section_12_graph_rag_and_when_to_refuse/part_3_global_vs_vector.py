# %% [markdown]
# # A global question fails vector RAG
#
# Lab `lab_s12_graph` / `part_3`.

# %%
"""A global question fails vector RAG."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.graph.tiny import answer_global
from rag.pipelines.naive import run_naive

q = "What are the main themes in this ACME corpus?"
vec = run_naive(q)
graph = answer_global(q)
print("vector", vec["answer"][:200])
print("graph ", graph["answer"])
print("vector_names_all_four", all(s in vec["answer"].lower() for s in ("sequential", "billing", "least-privilege", "pii")))
print("graph_names_all_four", all(s in graph["answer"].lower() for s in ("sequential", "billing", "least-privilege", "pii")))
