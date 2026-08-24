# %% [markdown]
# # S12.1 Local questions and global questions
#
# Two questions on one corpus, both through the naive vector door.
# The local miss is a ranking problem. The global miss is a shape problem.

# %%
"""S12.1: ask a local question and a global question, and test the answer sentence."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.ask import run_ask

LOCAL_ANSWER = "TS-999 means the billing ledger rejected a duplicate invoice id."
GLOBAL_ANSWER = "sequential revenue reporting, billing integrity, least-privilege access, and PII minimization"


def receipt(question: str, answer_sentence: str, label: str) -> None:
    """Print one ask: the call, the three returned strips, and whether the answer came back."""
    payload = run_ask(question, pipeline="naive", generate="extractive")
    print(f'run_ask("{question}", pipeline="naive")')
    for hit in payload["hits"]:
        print(f'  {hit["chunk_id"]:<24} {hit["score"]:>8.4f}')
    found = any(answer_sentence.lower() in hit["text"].lower() for hit in payload["hits"])
    print(f"{label} in the returned strips: {found}")


# 1. A local question. One document holds the answer.
receipt("What does error code TS-999 mean?", LOCAL_ANSWER, "answer sentence")
print()

# 2. The same local question with the words the document uses.
receipt("TS-999 billing ledger duplicate invoice id", LOCAL_ANSWER, "answer sentence")
print()

# 3. A global question. No document holds the answer to this one.
receipt("What themes run across all of this?", GLOBAL_ANSWER, "four-theme sentence")
