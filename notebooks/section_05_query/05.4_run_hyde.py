# %% [markdown]
# # S5.4 Run HyDE and decide
#
# Gao et al. 2022: invent a fake document, embed it, retrieve neighbors.
# The fake text is allowed to be wrong. Table 4: nDCG@10 61.3 vs 44.5 on TREC DL19.
# That is their number, not a promise for ACME. HyDE often hurts exact IDs.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.query.hyde import hypothetical_document, run_hyde

q = "What was ACME revenue growth in Q2 2023?"
print("fake document:\n", hypothetical_document(q))
out = run_hyde(q)
print("\nanswer:", out["answer"])
print("top hits:")
for h in out["hits"][:3]:
    print(" ", h["chunk_id"], h["text"][:100].replace("\n", " "))
