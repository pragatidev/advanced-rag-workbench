"""Your first working RAG program: load, chunk, embed, store, retrieve, extract an answer. No API key."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.stores.chroma_store import ChromaStore

docs = load_documents()
chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
embedder = HashEmbedder()
store = ChromaStore("mini_rag", persist=False)
store.reset()
store.add(chunks, embedder)
question = "What was ACME revenue growth in Q2 2023?"
hits = store.query(embedder.embed(question).tolist(), k=3)
source = hits[0].chunk.text
sentences = [s.strip() for s in source.replace("\n", " ").split(".") if s.strip()]
picked = [s for s in sentences if "revenue" in s.lower()]
answer = (picked[0] if picked else sentences[0]) + "."
print("question", question)
print("answer", answer)
print("from_chunk")
print(source)
