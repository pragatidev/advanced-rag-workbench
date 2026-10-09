"""STARTER Whiteboard the workbench stack onto six stations. Fill the TODOs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO: import HashEmbedder, estimate, prefilter, REQUIRED_SPAN_FIELDS, RRF_K, ChromaStore

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.eval.cost import estimate
from rag.gov import prefilter
from rag.observe import REQUIRED_SPAN_FIELDS
from rag.retrieve import RRF_K
from rag.settings import DEFAULT_RERANK_MODEL, LAB_EMBEDDER
from rag.stores.chroma_store import ChromaStore

# TODO: fill six stations from workbench paths, then print the 2-second bar and the cost column

docs = load_documents()
print("files", len(docs))
print("embedder", HashEmbedder().name)
print("rrf_k", RRF_K)
print("rerank", DEFAULT_RERANK_MODEL)
print("backend", ChromaStore.backend)
print("bakeoff", ", ".join(LAB_EMBEDDER["production_swap"]))
print("spans", ",".join(REQUIRED_SPAN_FIELDS))
print("east", len(prefilter(chunk_corpus(docs, "recursive"), "helix-east")))
print("usd", estimate("naive")["usd"])
