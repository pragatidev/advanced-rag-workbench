# %% [markdown]
# # Run faithfulness and context recall
#
# Lab `lab_s14_eval` / `part_2`.

# %%
"""Run faithfulness and context recall."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.eval.golden import load_golden
from rag.eval.metrics import context_recall, faithfulness

rows = load_golden()
row = next(r for r in rows if r["id"] == "q_revenue_growth")
gold = row["gold_spans"]
wrong_ctx = [
    "Warehouse throughput improved. Marketing spend was steady. Nothing in this preface names the growth rate."
]
fluent_wrong = "Warehouse throughput improved. Marketing spend was steady."
right_ctx = ["The company's revenue grew by 3% over the previous quarter."]
gold_answer = "revenue grew by 3%"

print("id", row["id"])
print("gold_span", gold[0])
print("=== wrong chunks ===")
print("retrieved", wrong_ctx[0])
print("answer", fluent_wrong)
print("faithfulness", faithfulness(fluent_wrong, wrong_ctx))
print("context_recall", context_recall(gold, wrong_ctx))
print("this is the failure: fluent answer, missing gold span")
print("=== gold span retrieved ===")
print("retrieved", right_ctx[0])
print("answer", gold_answer)
print("faithfulness", faithfulness(gold_answer, right_ctx))
print("context_recall", context_recall(gold, right_ctx))
