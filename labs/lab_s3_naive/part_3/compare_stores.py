"""Same chunks on FAISS, Qdrant, and optional pgvector."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.stores.chroma_store import ChromaStore
from rag.stores.faiss_store import FaissStore
from rag.stores.qdrant_store import QdrantStore

docs = load_documents()
chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
emb = HashEmbedder(semantic_mode=True)
vecs = emb.encode([c.text for c in chunks]).tolist()

rows = []
chroma = ChromaStore("compare", persist=False)
chroma.reset()
chroma.add(chunks, vecs)
rows.append(("chroma", chroma.info().count))

faiss = FaissStore("compare", path=ROOT / "store" / "faiss" / "compare")
faiss.reset()
faiss.add(chunks, vecs)
rows.append(("faiss", faiss.info().count))

qdrant = QdrantStore("compare", path=ROOT / "store" / "qdrant")
qdrant.reset()
qdrant.add(chunks, vecs)
rows.append(("qdrant", qdrant.info().count))

print("HNSW: M and ef live in the store config, not the notebook")
for name, n in rows:
    print(f"{name:8} count={n}")
assert rows[0][1] == rows[1][1] == rows[2][1]

try:
    from rag.stores import pgvector_store as pgs
    if pgs.available():
        pg = pgs.PgVectorStore("compare")
        pg.reset()
        pg.add(chunks, vecs)
        print("pgvector", pg.info().count)
    else:
        print("SKIP pgvector: docker not up")
except Exception as exc:
    print("SKIP pgvector:", exc)
