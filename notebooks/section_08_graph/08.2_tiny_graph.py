# %% [markdown]
# # S8.2 Build a tiny graph on the sample corpus
#
# Vector RAG is local. "What are the themes?" needs a community summary.
# This is a seeded toy graph, not a Microsoft GraphRAG index. Cost is printed.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.graph.tiny import answer_global, build

g = build()
print("nodes", g["nodes"])
print("members", g["members"])
print("cost", g["index_cost"])
print("answer", answer_global("What are the main themes in this ACME corpus?")["answer"])
