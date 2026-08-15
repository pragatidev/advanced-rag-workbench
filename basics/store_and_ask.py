"""A vector store keeps the chunks and returns the nearest neighbors for a question."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import fixed_size
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.stores.chroma_store import ChromaStore

doc = next(item for item in load_documents() if item.doc_id == "filing_q2_2023")
chunks = fixed_size(doc, size=80, overlap=0)
embedder = HashEmbedder()
store = ChromaStore("basics", persist=False)
store.reset()
store.add(chunks, embedder)
question = "What was ACME revenue growth in Q2 2023?"
hits = store.query(embedder.embed(question).tolist(), k=3)
print("question", question)
print("backend chroma (in memory)")
print("neighbors", len(hits))
for hit in hits:
    print(f"{hit.score:.3f}  {hit.chunk.chunk_id}")
    print(hit.chunk.text)
    print("---")
