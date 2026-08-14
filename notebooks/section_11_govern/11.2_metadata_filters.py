# %% [markdown]
# # S11.2 Metadata filters and redaction
#
# Retrieval is access control. The FAQ is tagged tenant=helix-east.
# Shared docs are visible to everyone. Redact PII before the prompt.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.chunking import chunk_corpus
from rag.corpus import load_documents
from rag.gov import allowed, redact

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
print("tenant helix-east sees", sum(1 for c in chunks if allowed(c, "helix-east")), "chunks")
print("tenant other sees    ", sum(1 for c in chunks if allowed(c, "other")), "chunks")
print(redact("Do not send a national id to the model."))
