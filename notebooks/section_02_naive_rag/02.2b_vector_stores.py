# %% [markdown]
# # S2.2b The same index on Chroma, FAISS, Qdrant, pgvector
#
# Real projects pick a store. They do not invent a `.npy` file format.
# This notebook writes the **same chunks and the same vectors** into every local store
# this course runs:
#
# | Store | What you open | Needs |
# |---|---|---|
# | Chroma | `store/chroma/` | pip only |
# | FAISS | `store/faiss/naive/` | pip only |
# | Qdrant | `store/qdrant/` | pip only |
# | pgvector | Postgres | `docker compose up -d` (optional) |
#
# Hosted stores we name but do not run (they need a paid key): Pinecone, Weaviate, Milvus.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd()
if not (ROOT / "rag").is_dir():
    ROOT = ROOT.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunking import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.stores.base import PRODUCTION_STORES
from rag.stores import ChromaStore, FaissStore, QdrantStore

QUESTION = "What does error code TS-999 mean?"
docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
embedder = HashEmbedder(semantic_mode=True)
vectors = embedder.encode([c.text for c in chunks]).tolist()
qvec = embedder.embed(QUESTION).tolist()

print("Stores this industry uses:")
for row in PRODUCTION_STORES:
    flag = "RUN" if row["lab"] else "name only"
    print(f"  [{flag:9}] {row['name']:12} {row['why']}")

# %% [markdown]
# ## Chroma

# %%
chroma = ChromaStore("compare", persist=True)
chroma.reset()
chroma.add(chunks, vectors)
print("CHROMA", chroma.info())
for h in chroma.query(qvec, k=2):
    print(" ", round(h.score, 3), h.chunk.chunk_id)

# %% [markdown]
# ## FAISS (IndexFlatIP, cosine via L2-normalized vectors)

# %%
faiss_store = FaissStore("compare")
faiss_store.reset()
faiss_store.add(chunks, vectors)
print("FAISS", faiss_store.info())
for h in faiss_store.query(qvec, k=2):
    print(" ", round(h.score, 3), h.chunk.chunk_id)

# %% [markdown]
# ## Qdrant (local embedded client)

# %%
qdrant = QdrantStore("compare")
qdrant.reset()
qdrant.add(chunks, vectors)
print("QDRANT", qdrant.info())
for h in qdrant.query(qvec, k=2):
    print(" ", round(h.score, 3), h.chunk.chunk_id)

# %% [markdown]
# ## pgvector (optional)
# Start Postgres first: `docker compose up -d` from the repo root.
# If it is not up, this cell prints SKIP and the rest of the course still runs.

# %%
from rag.stores import pgvector_store as pgs
if pgs.available():
    pg = pgs.PgVectorStore("compare")
    pg.reset()
    pg.add(chunks, vectors)
    print("PGVECTOR", pg.info())
    for h in pg.query(qvec, k=2):
        print(" ", round(h.score, 3), h.chunk.chunk_id)
else:
    print("SKIP pgvector. Start it with: docker compose up -d")
    print("Default URL", pgs.DEFAULT_URL)
