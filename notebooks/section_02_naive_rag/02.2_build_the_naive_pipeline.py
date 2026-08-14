# %% [markdown]
# # S2.2 Build the naive pipeline
#
# Naive RAG in a real project is five steps:
# 1. Load documents
# 2. Chunk
# 3. Embed with a **named** model
# 4. Write a **real vector store** (here: Chroma)
# 5. Query, then generate only from the hits
#
# We use Chroma first because that is the store most Python RAG apps start with.
# The next notebook (02.2b) runs the same chunks through FAISS, Qdrant, and pgvector.

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
from rag.embedders import HashEmbedder, PRODUCTION_EMBEDDERS
from rag.generate import generate_answer
from rag.stores.chroma_store import ChromaStore

QUESTION = "What was ACME revenue growth in Q2 2023?"

# %% [markdown]
# ## 1. Load
# These are ordinary files. Open them in the editor. There is no hidden Nike dump.

# %%
docs = load_documents()
print(len(docs), "documents")
for d in docs:
    print(f"  {d.doc_id:18}  {d.path}")

# %% [markdown]
# ## 2. Chunk
# Naive default: fixed windows, 80 words, no overlap. That is a guess. S3 will swap it.

# %%
chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
print("chunker=fixed size=80 overlap=0 ->", len(chunks), "chunks")
print("first chunk id:", chunks[0].chunk_id)
print(chunks[0].text[:240])

# %% [markdown]
# ## 3. Name the embedder
# This cell uses HashEmbedder so the lecture runs offline.
# A shipped app would put `all-MiniLM-L6-v2` or `text-embedding-3-small` in config.

# %%
print("this cell:", HashEmbedder.name, "dim", HashEmbedder.dim)
print("production names:")
for row in PRODUCTION_EMBEDDERS:
    print(" ", row["name"], "|", row["where"], "| key=", row["key"])
embedder = HashEmbedder(semantic_mode=True)
vectors = embedder.encode([c.text for c in chunks])
print("vectors.shape", tuple(vectors.shape))

# %% [markdown]
# ## 4. Store in Chroma
# After this cell, open `store/chroma/` on disk. That folder is the index.

# %%
store = ChromaStore("naive", persist=True)
store.reset()
store.add(chunks, vectors.tolist())
print(store.info())

# %% [markdown]
# ## 5. Retrieve, then generate
# Generation is extractive (no key). A production generate would call your model API.

# %%
hits = store.query(embedder.embed(QUESTION).tolist(), k=3)
print("Q:", QUESTION)
for i, h in enumerate(hits, start=1):
    print(f"#{i} {h.score:.3f} {h.chunk.chunk_id}")
    print("   ", h.chunk.text.replace(chr(10), " ")[:160])
answer, meta = generate_answer(QUESTION, [h.chunk for h in hits], mode="extractive")
print("generator:", meta)
print("answer:", answer)
