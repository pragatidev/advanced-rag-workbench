# %% [markdown]
# # S11.3 Audit what left the building
#
# Log chunk ids and hashes, not just the final answer. Retrieved text is data.
# Treat it as untrusted (OWASP LLM01: a chunk can carry instructions).

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.ask import run_ask
from rag.chunking import Chunk
from rag.gov import audit_row

out = run_ask("What does error code TS-999 mean?", pipeline="hybrid", generate="extractive")
chunks = [Chunk(h["chunk_id"], h["doc_id"], "", h["text"]) for h in out["hits"]]
print(audit_row(out["question"], chunks))
