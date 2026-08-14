# %% [markdown]
# # S7.2 Score the retrieved set
#
# CRAG (Yan et al. 2024): Correct / Incorrect / Ambiguous.
# We grade by query-token coverage of the top hit. No web.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.chunking import Chunk
from rag.loops.crag import grade
from rag.retrieve import Hit

def H(text):
    return [Hit(chunk=Chunk("c","d","t",text), score=1.0, source="x")]

print("empty", grade("TS-999", []))
print("good ", grade("What does TS-999 mean?", H("TS-999 means duplicate invoice")))
print("bad  ", grade("What does TS-999 mean?", H("Warehouse throughput improved.")))
