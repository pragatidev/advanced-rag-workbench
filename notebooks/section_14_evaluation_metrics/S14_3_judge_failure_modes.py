# %% [markdown]
# # S14.3 LLM-as-judge failure modes, and offline versus online
#
# Judges have position bias, verbosity bias, and self-preference.
# Calibrate against humans. Offline golden is not online thumbs.
# Changing the chunker moves the IDs, so you also need end-to-end.

# %%
"""S14.3: named judge biases, calibration, offline vs online, chunker IDs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import fixed_size, recursive
from rag.corpus import load_documents
from rag.eval.golden import load_golden
from rag.eval.judge import agreement, pick_first, pick_longer, pick_same_family

GOLD = "ACME revenue grew by 3% over the previous quarter."
MISS = "Warehouse throughput improved. Marketing spend was steady."
VERBOSE_MISS = (
    "Warehouse throughput improved. Marketing spend was steady. "
    "Nothing in this preface names the growth rate. "
    "The filing discusses seasonality, supply chain recovery, "
    "and the way management talks about sequential growth."
)

print("=== position bias ===")
print("gold_words", len(GOLD.split()))
print("miss_words", len(MISS.split()))
first_order = pick_first(GOLD, MISS)
swap_order = pick_first(MISS, GOLD)
print("gold first then miss, judge picks", "GOLD" if first_order == GOLD else "MISS")
print("miss first then gold, judge picks", "GOLD" if swap_order == GOLD else "MISS")
print("same answers, order flipped the winner")
print("position_bias stamp")
print()

print("=== verbosity bias ===")
print("gold_words", len(GOLD.split()))
print("verbose_miss_words", len(VERBOSE_MISS.split()))
verbose_pick = pick_longer(GOLD, VERBOSE_MISS)
print("judge picks", "GOLD" if verbose_pick == GOLD else "VERBOSE_MISS")
print("longer answer won, gold span missed")
print("verbosity_bias stamp")
print()

print("=== self-preference ===")
judge_family = "family_a"
gold_pair = (GOLD, "other")
miss_pair = (VERBOSE_MISS, "family_a")
self_pick = pick_same_family(gold_pair, miss_pair, judge_family)
print("judge_family", judge_family)
print("gold_family other")
print("verbose_miss_family family_a")
print("judge picks", "GOLD" if self_pick == GOLD else "VERBOSE_MISS")
print("same family won")
print("self_preference stamp")
print()

print("=== calibrate against humans ===")
human_gold = GOLD
pairs = [
    (human_gold, first_order),
    (human_gold, swap_order),
    (human_gold, verbose_pick),
    (human_gold, self_pick),
]
agree, n = agreement(pairs)
print("pair 1 human GOLD judge", "GOLD" if first_order == GOLD else "MISS")
print("pair 2 human GOLD judge", "GOLD" if swap_order == GOLD else "MISS")
print("pair 3 human GOLD judge", "GOLD" if verbose_pick == GOLD else "VERBOSE_MISS")
print("pair 4 human GOLD judge", "GOLD" if self_pick == GOLD else "VERBOSE_MISS")
print("agree", agree, "of", n)
print("human_calibration tick")
print()

print("=== offline golden ===")
rows = load_golden()
row = next(r for r in rows if r["id"] == "q_revenue_growth")
print("id", row["id"])
print("question", row["question"])
print("gold_spans", ", ".join(row["gold_spans"]))
print("canary", row["canary"])
print()

print("=== online thumbs ===")
print("ticket t_104 thumbs_up")
print("answer", MISS)
print("offline gold_span", row["gold_spans"][0])
print("offline golden is not online thumbs")
print()

print("=== chunker moves the ids ===")
docs = {d.doc_id: d for d in load_documents()}
filing = docs["filing_q2_2023"]
fixed = fixed_size(filing)
rec = recursive(filing)
fixed_ids = [c.chunk_id for c in fixed]
rec_ids = [c.chunk_id for c in rec]
print("fixed", " ".join(fixed_ids))
print("recursive", " ".join(rec_ids))
print("id_overlap", len(set(fixed_ids) & set(rec_ids)))
print("retrieval metrics assume a fixed candidate set")
print("changing the chunker moves the ids, so you also need end-to-end")
