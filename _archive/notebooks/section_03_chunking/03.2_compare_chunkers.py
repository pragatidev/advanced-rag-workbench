# %% [markdown]
# # S3.2 Recursive vs semantic vs parent-child
#
# Same corpus. Four chunkers. Count chunks. See who keeps the heading next to 3%.
# Parent-child indexes a small window and keeps the parent section for generation
# (the sentence-window idea).

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.chunking import CHUNKERS, chunk_corpus
from rag.corpus import load_documents

docs = load_documents()
print(f"{'chunker':16} {'n':>6} {'has 3%':>8} {'3% names ACME/Q2':>18}")
for name in CHUNKERS:
    kwargs = {"size": 80, "overlap": 0} if name == "fixed" else {}
    chunks = chunk_corpus(docs, name, **kwargs) if kwargs else chunk_corpus(docs, name)
    growth = [c for c in chunks if "3%" in c.text]
    named = [c for c in growth if "acme" in c.text.lower() or "q2" in c.text.lower()]
    print(f"{name:16} {len(chunks):6} {len(growth):8} {len(named):18}")

rec = chunk_corpus(docs, "recursive")
keep = next(c for c in rec if "3%" in c.text)
print("\nrecursive chunk with 3%:\n", keep.chunk_id, "\n", keep.text)
