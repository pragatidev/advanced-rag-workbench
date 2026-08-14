# %% [markdown]
# # S4.2 Hybrid search with RRF
#
# Dense search (Chroma) misses exact IDs when the embedder is semantic.
# BM25 locks the token TS-999.
# Reciprocal Rank Fusion (k=60, Cormack 2009) merges the two lists.
# That pair is the Monday default in this course.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.chunking import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.retrieve import bm25_search, rrf_fuse
from rag.stores.chroma_store import ChromaStore

q = "What does error code TS-999 mean?"
docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
emb = HashEmbedder(semantic_mode=True)
store = ChromaStore("hybrid_demo", persist=True)
store.reset()
store.add(chunks, emb.encode([c.text for c in chunks]).tolist())

dense = store.query(emb.embed(q).tolist(), k=5)
sparse = bm25_search(q, chunks, k=5)
fused = rrf_fuse([dense, sparse], k=60, top_n=5)

def show(label, hits):
    print(label)
    for h in hits[:3]:
        print(f"  {h.score:.4f} {h.chunk.chunk_id}  {h.chunk.text[:70]!r}")

show("dense / Chroma", dense)
show("BM25", sparse)
show("RRF k=60", fused)
print("BM25 top has TS-999?", "ts-999" in sparse[0].chunk.text.lower())
