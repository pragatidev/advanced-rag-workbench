# %% [markdown]
# # S16.3 Ingest poisoning and retrieval injection
#
# Treat retrieved text as data is the generate half.
# Ingest trust is the other half. No exploit lab.

# %%
"""S16.3: ingest allow-list and planted-doc canary. Not an exploit."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.generate import HYGIENE
from rag.gov import (
    ALLOW_LIST,
    ECHOLEAK_CVE,
    ECHOLEAK_CVSS,
    ECHOLEAK_YEAR,
    PLANTED_ID,
    POISONEDRAG_ASR_PCT,
    POISONEDRAG_CORPUS_SCALE,
    POISONEDRAG_PAGES,
    POISONEDRAG_TEXTS_PER_TARGET,
    POISONEDRAG_VENUE,
    canary_pass,
    ingest_filter,
    planted_email,
)
from rag.retrieve import bm25_search

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
planted = planted_email()
mixed = list(chunks) + [planted]
query = "What inbound mail is not in the ACME catalog?"
k = 3

print("=== generate half ===")
print(HYGIENE)

print()
print("=== allow list ===")
print("allow_list", " ".join(sorted(ALLOW_LIST)))
print("allow_n", len(ALLOW_LIST))

print()
print("=== planted ===")
print("planted_id", planted.chunk_id)
print("planted_doc_type", planted.metadata.get("doc_type"))
print("planted_text", planted.text)
print("exploit_lab", False)

print()
print("=== without ingest filter ===")
print("query", query)
print("mixed_n", len(mixed))
print("planted_in_index", any(c.chunk_id == PLANTED_ID for c in mixed))
raw = bm25_search(query, mixed, k=k)
raw_ids = [h.chunk.chunk_id for h in raw]
print("raw_ids", raw_ids)
print("planted_won", PLANTED_ID in raw_ids)

print()
print("=== with ingest filter ===")
candidates = ingest_filter(mixed)
print("candidate_n", len(candidates))
print("planted_in_candidates", any(c.chunk_id == PLANTED_ID for c in candidates))
print("canary_pass", canary_pass(candidates))
kept = bm25_search(query, candidates, k=k)
kept_ids = [h.chunk.chunk_id for h in kept]
print("kept_ids", kept_ids)
print("planted_won", PLANTED_ID in kept_ids)

print()
print("=== paper board ===")
print("paper PoisonedRAG")
print("venue", POISONEDRAG_VENUE)
print("pages", POISONEDRAG_PAGES)
print("texts_per_target", POISONEDRAG_TEXTS_PER_TARGET)
print("corpus_scale", POISONEDRAG_CORPUS_SCALE)
print("attack_success_pct", POISONEDRAG_ASR_PCT)
print("name EchoLeak")
print("cve", ECHOLEAK_CVE)
print("cvss", ECHOLEAK_CVSS)
print("year", ECHOLEAK_YEAR)
