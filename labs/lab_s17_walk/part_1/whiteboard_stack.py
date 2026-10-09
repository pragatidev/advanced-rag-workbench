"""Whiteboard the workbench stack onto six stations.

A whiteboard is not vendor logos. Fill each station from a path on disk.
Speak a 2-second bar and a cost column.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.eval.cost import estimate
from rag.gov import prefilter
from rag.observe import REQUIRED_SPAN_FIELDS
from rag.retrieve import RRF_K
from rag.settings import DEFAULT_RERANK_MODEL, LAB_EMBEDDER
from rag.stores.chroma_store import ChromaStore

BOARD_MS = {
    "embed": "50-100",
    "retrieve": "50-150",
    "rerank": "100-300",
    "first_token": "300-800",
}

docs = load_documents()
words = sum(len(d.text.split()) for d in docs)
chunks = chunk_corpus(docs, "recursive")
east = prefilter(chunks, "helix-east")
west = prefilter(chunks, "helix-west")
qpath = ROOT / "eval" / "questions.jsonl"
questions = [
    json.loads(line)
    for line in qpath.read_text(encoding="utf-8").splitlines()
    if line.strip()
]
emb = HashEmbedder()
bakeoff = ", ".join(LAB_EMBEDDER["production_swap"])


def on_disk(rel: str) -> bool:
    p = ROOT / rel
    return p.is_file() or p.is_dir()


print("=== whiteboard, not vendor logos ===")
print("corpus data/acme files", len(docs), "words", words)
print("questions eval/questions.jsonl rows", len(questions))

print()
print("=== station 1 requirements ===")
print("path data/acme", on_disk("data/acme"))
print("path eval/questions.jsonl", on_disk("eval/questions.jsonl"))
print("p95 2 seconds interview board")

print()
print("=== station 2 ingestion ===")
print("path rag/chunkers.py", on_disk("rag/chunkers.py"))
print("embedder", emb.name, "dim", emb.dim)
print("bakeoff", bakeoff)
print(
    "path rag/stores/chroma_store.py",
    on_disk("rag/stores/chroma_store.py"),
    "backend",
    ChromaStore.backend,
)
print("path rag/incremental.py tombstone", on_disk("rag/incremental.py"))

print()
print("=== station 3 retrieval ===")
print("path rag/retrieve.py hybrid dense+bm25 rrf_k", RRF_K, on_disk("rag/retrieve.py"))
print("path rag/rerank.py", DEFAULT_RERANK_MODEL, on_disk("rag/rerank.py"))
print("path rag/gov.py prefilter", on_disk("rag/gov.py"))
print("east", len(east), "west", len(west))

print()
print("=== station 4 generation ===")
print("path rag/generate.py extractive", on_disk("rag/generate.py"))
print("path rag/llm.py SYSTEM REFUSE", on_disk("rag/llm.py"))

print()
print("=== station 5 evals ===")
print("path eval/questions.jsonl rows", len(questions), on_disk("eval/questions.jsonl"))
print("path rag/eval", on_disk("rag/eval"))

print()
print("=== station 6 ops ===")
print("path rag/observe.py spans", ",".join(REQUIRED_SPAN_FIELDS))
print("path rag/gov.py tenant pre-filter")

print()
print("=== two second bar ===")
print("embed", BOARD_MS["embed"], "ms")
print("retrieve", BOARD_MS["retrieve"])
print("rerank", BOARD_MS["rerank"])
print("first_token", BOARD_MS["first_token"])
print("note Interview Coder Q29 board. Not this clone clock.")

print()
print("=== cost column ===")
for name, extra in (("naive", 0), ("hybrid", 0), ("hyde", 1)):
    row = estimate(name, extra_generates=extra)
    print(name, "generate_calls", row["generate_calls"], "usd", row["usd"])
print("rule refuse Hyde when p95 budget is 2 seconds")
