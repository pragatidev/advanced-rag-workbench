# %% [markdown]
# # S14.2 Precision, recall, MRR, MAP, and when MRR lies
#
# A ranked list with two gold chunks at the bottom. MRR celebrates
# the first hit. MAP counts both. Accuracy is the wrong word.

# %%
"""S14.2: ranking metrics on a list with two golds at the bottom."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.eval.metrics import average_precision, mrr, ndcg_at_k, precision_at_k, recall_at_k

rows = [
    (0, "Warehouse throughput improved. Marketing spend was steady."),
    (0, "TS-999 means the billing ledger rejected a duplicate invoice ID."),
    (0, "Customer email, phone, and national id are PII."),
    (1, "The company's revenue grew by 3% over the previous quarter."),
    (1, "Prior quarter revenue was 314 million USD."),
]
rels = [r[0] for r in rows]
k = 5

print("=== ranked list, two golds at the bottom ===")
print("k", k)
for i, (rel, text) in enumerate(rows, start=1):
    tag = "GOLD" if rel else "FAIL"
    print(f"rank {i} {tag} {text}")
print("precision_at_5", precision_at_k(rels, 5))
print("recall_at_5", recall_at_k(rels, 5))
print("mrr", mrr(rels))
print("map", average_precision(rels))
print("ndcg_at_5", round(ndcg_at_k(rels, 5), 4))
print("accuracy is the wrong word")
print("this is the failure: two golds at the bottom, MRR only saw rank 4")
print()

padded = rels + [0, 0, 0, 0, 0]
print("=== pad to ten ===")
print("precision_at_10", precision_at_k(padded, 10))
print("recall_at_10", recall_at_k(padded, 10))
print("perfect recall_at_10 with low precision_at_10 stuffs junk into generate")
print()

first_then_second = [1, 1, 0, 0, 0]
first_then_buried = [1, 0, 0, 0, 1]
print("=== when MRR lies ===")
print(
    "first_hit_rank_1_second_at_2",
    "mrr",
    mrr(first_then_second),
    "map",
    average_precision(first_then_second),
)
print(
    "first_hit_rank_1_second_at_5",
    "mrr",
    mrr(first_then_buried),
    "map",
    average_precision(first_then_buried),
)
print("same MRR, MAP moved")
