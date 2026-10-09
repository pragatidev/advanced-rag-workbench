# %% [markdown]
# # S17.1 Design a RAG system for ACME, station by station
#
# Six stations in interview order. Five scoping questions answered on this corpus.
# A 2-second bar and a cost column. Three-bin debug.

# %%
"""S17.1: ACME as X. Stations, scoping, 2s bar, cost, three-bin."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.corpus import load_documents
from rag.eval.cost import estimate
from rag.llm import SYSTEM

docs = load_documents()
words = sum(len(d.text.split()) for d in docs)
formats = sorted({Path(d.path).suffix.lstrip(".") or "txt" for d in docs})
qpath = ROOT / "eval" / "questions.jsonl"
questions = [json.loads(line) for line in qpath.read_text(encoding="utf-8").splitlines() if line.strip()]
classes = Counter(q.get("query_class", "") for q in questions)
lookup_keys = {"exact_id", "local_anaphora", "table", "figure"}
lookup = sum(classes[k] for k in lookup_keys)
multi_hop = classes.get("multi_hop", 0)
list_all = classes.get("global", 0)
abstain = classes.get("no_retrieve", 0)
acl = classes.get("acl", 0)

print("=== ACME as X ===")
print("files", len(docs))
print("words", words)
print("formats", ",".join(formats))
print("questions", len(questions))

print()
print("=== five scoping ===")
print("Q1 corpus size and formats")
print("A1 files", len(docs), "words", words, "formats", ",".join(formats))
print("Q2 query mix lookup vs multi-hop vs list-all")
print("A2 lookup", lookup, "multi_hop", multi_hop, "list_all", list_all, "abstain", abstain, "acl", acl)
print("Q3 p95 latency")
print("A3 2 seconds interview board")
print("Q4 cost per query")
print("A4 generate_calls tokens usd. local toy usd 0.0")
print("Q5 who is allowed, is abstention allowed")
print("A5 FAQ tenant helix-east. prefilter. SYSTEM REFUSE. abstention allowed")

print()
print("=== six stations ===")
print("1 requirements")
print("2 ingestion")
print("3 retrieval")
print("4 generation")
print("5 evals")
print("6 ops")

print()
print("=== two second bar ===")
print("embed 50-100 ms")
print("retrieve 50-150")
print("rerank 100-300")
print("first_token 300-800")
print("note Interview Coder Q29 board. Not this clone clock.")

print()
print("=== cost column ===")
for name, extra in (("naive", 0), ("hybrid", 0), ("hyde", 1)):
    row = estimate(name, extra_generates=extra)
    print(name, "generate_calls", row["generate_calls"], "usd", row["usd"])
print("rule refuse Hyde when p95 budget is 2 seconds")

print()
print("=== three bin debug ===")
print("missing")
print("mis-ranked")
print("ignored")

print()
print("=== refuse ladder ===")
print("abstain")
print("show sources")
print("clarify")
print("ticket")
print("SYSTEM", SYSTEM)

print()
print("=== tenant isolation ===")
print("separate_index")
print("shared_plus_filter")
print("hybrid")
print("note spoken tradeoff. not a 10k tenant lab")
