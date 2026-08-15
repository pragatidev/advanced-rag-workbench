# %% [markdown]
# # S6.2 Retrieve only when the question needs the corpus
#
# This is a prompt-loop gate, not Asai Self-RAG (trained reflection tokens).
# Chitchat should not hit the index.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.loops.retrieve_gate import needs_corpus

for q in ["Good morning, how are you?", "What does error code TS-999 mean?"]:
    print(repr(q), "->", needs_corpus(q))
