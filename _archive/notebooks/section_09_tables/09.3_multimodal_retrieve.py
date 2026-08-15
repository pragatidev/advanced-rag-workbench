# %% [markdown]
# # S9.3 Multimodal retrieve on the same questions
#
# Same questions as the eval file. Row chunks should hit 12420.
# The caption document should hit South 2000.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.multimodal import table_row_chunks
from rag.retrieve import bm25_search

docs = {d.doc_id: d for d in load_documents()}
rows = table_row_chunks(docs["q2_kpis"])
hits = bm25_search("How many paid seats did ACME have in Q2?", rows, k=2)
print("table retrieve:")
for h in hits:
    print(" ", h.chunk.text)
print("12420 in top?", any("12420" in h.chunk.text for h in hits))
print("caption has South 2000?", "South 2000" in docs["figure_seats"].text)
