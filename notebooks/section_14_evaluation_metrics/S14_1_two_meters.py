# %% [markdown]
# # S14.1 Why faithfulness is not context recall
#
# A fluent answer that used the wrong chunks can score high on faithfulness
# and low on context recall.

# %%
"""S14.1: two meters on a fluent wrong-span answer."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.eval.metrics import context_recall, faithfulness

gold = ["revenue grew by 3%"]
wrong_ctx = [
    "Warehouse throughput improved. Marketing spend was steady. Nothing in this preface names the growth rate."
]
fluent_wrong = "Warehouse throughput improved. Marketing spend was steady."
right_ctx = ["The company's revenue grew by 3% over the previous quarter."]
gold_answer = "revenue grew by 3%"

print("=== wrong chunks ===")
print("gold_span", gold[0])
print("retrieved", wrong_ctx[0])
print("answer", fluent_wrong)
print("faithfulness", faithfulness(fluent_wrong, wrong_ctx))
print("context_recall", context_recall(gold, wrong_ctx))
print("this is the failure: fluent answer, missing gold span")
print()
print("=== gold span retrieved ===")
print("retrieved", right_ctx[0])
print("answer", gold_answer)
print("faithfulness", faithfulness(gold_answer, right_ctx))
print("context_recall", context_recall(gold, right_ctx))
