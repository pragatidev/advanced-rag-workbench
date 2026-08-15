# %% [markdown]
# # S10.4 Traces you can debug
#
# Every ask appends one JSON line: question, pipeline, chunk ids. That is the
# audit trail you open when a user says "it made this up."

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.ask import run_ask

out = run_ask("What does error code TS-999 mean?", pipeline="hybrid", generate="extractive")
print("chunk_ids", [h["chunk_id"] for h in out["hits"]])
print("log file: runs/ask.jsonl")
