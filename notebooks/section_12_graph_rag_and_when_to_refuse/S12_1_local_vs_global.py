# %% [markdown]
# # S12.1 Local questions and global questions
#
# One local question, asked two ways, through the product door.
# The receipt is the lecture: the ids tell you the index sees strips, not paragraphs.

# %%
"""S12.1: ask the same local question two ways and read the strip ids."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.ask import run_ask


def receipt(question: str) -> dict:
    """Print one ask the way the lecture reads it: the call, the strips, the answer."""
    payload = run_ask(question, pipeline="naive", generate="extractive")
    print(f'run_ask("{question}", pipeline="naive", generate="extractive")')
    for hit in payload["hits"]:
        print(f'  {hit["chunk_id"]:<22} {hit["score"]:>8.4f}')
    print(f'answer: {payload["answer"]}')
    return payload


# The question a person would actually type. The error catalog does not come back.
receipt("What does error code TS-999 mean?")
print()
# The same local answer, asked with the bare token. The home strip comes back at rank two.
receipt("TS-999")
