"""Run faithfulness and context recall."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.eval.metrics import context_recall, faithfulness

gold = ["revenue grew by 3%"]
wrong_ctx = ["Most error codes in general are transient."]
fluent_wrong = "Revenue grew by 3%."
print("faithfulness_on_wrong_ctx", faithfulness(fluent_wrong, wrong_ctx))
print("context_recall_on_wrong_ctx", context_recall(gold, wrong_ctx))
print("this is the failure: fluent answer, missing gold span")
print("faithfulness_on_right_ctx", faithfulness(fluent_wrong, ["The company's revenue grew by 3%."]))
print("context_recall_on_right_ctx", context_recall(gold, ["The company's revenue grew by 3%."]))
