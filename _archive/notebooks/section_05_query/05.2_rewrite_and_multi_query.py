# %% [markdown]
# # S5.2 Rewrite and multi-query
#
# One user question is often a bad search string. Rewrite fixes vocabulary.
# Multi-query covers facets, then you fuse with RRF. Cost: extra searches.
# Keep a rewrite only if recall moves.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.query.rewrite import multi_query, rewrite

q = "What was ACME revenue growth in Q2 2023?"
print("original:", q)
print("rewrite: ", rewrite(q))
print("multi:")
for i, item in enumerate(multi_query(q), start=1):
    print(f"  {i}. {item}")
