# %% [markdown]
# # S12.1 The global question, reworded
#
# The same global question, phrased with the words the corpus itself uses.
# It works, and the reason it works is the whole point:
# a human pre-wrote the global answer into one chunk.

# %%
"""S12.1: give the global question its best possible day, and read why it wins."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.ask import run_ask

QUESTION = "What are the themes across this corpus?"

payload = run_ask(QUESTION, pipeline="naive", generate="extractive")

print(f'run_ask("{QUESTION}", pipeline="naive")')
for hit in payload["hits"]:
    print(f'  {hit["chunk_id"]:<24} {hit["score"]:>8.4f}')
print(f'answer: {payload["answer"]}')
