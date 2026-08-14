# %% [markdown]
# # S4.3 Contextual chunks (Anthropic)
#
# Anthropic prepends a short context line to each chunk before embed and before BM25.
# Their 19 Sep 2024 post: contextual embeddings cut top-20 failure 5.7% to 3.7%;
# plus contextual BM25 to 2.9%; plus a reranker to 1.9%. Those are their numbers.
# We prepend the document title. No extra LLM call.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.chunking import chunk_corpus, contextualize
from rag.corpus import load_documents

docs = load_documents()
raw = chunk_corpus(docs, "recursive")
ctx = [contextualize(c) for c in raw]
print("before:\n", raw[0].text[:180])
print("\nafter:\n", ctx[0].text[:220])
print("\ncount", len(raw), "->", len(ctx))
