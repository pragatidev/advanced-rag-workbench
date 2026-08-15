# %% [markdown]
# # S9.2 Parse tables and captions
#
# A text splitter smashes rows. We chunk one table row at a time and keep the
# figure caption as its own document. That is how 12420 and South 2000 stay findable.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.corpus import load_documents
from rag.multimodal import table_row_chunks

docs = {d.doc_id: d for d in load_documents()}
rows = table_row_chunks(docs["q2_kpis"])
print("table rows", len(rows))
for r in rows:
    print(" ", r.chunk_id, r.text)
print("\nfigure caption:\n", docs["figure_seats"].text)
