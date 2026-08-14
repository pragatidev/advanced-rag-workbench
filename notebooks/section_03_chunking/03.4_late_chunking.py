# %% [markdown]
# # S3.4 Late chunking, one measured try
#
# Late chunking embeds a longer span first, then splits. We simulate that cheaply:
# embed the parent section, copy the vector to each child. Compare to recursive
# on the 3% question. Keep it only if the retrieved span is better. On this corpus
# it often is not. That is the point of measuring.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.chunking import chunk_corpus, parent_child
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.retrieve import dense_search

docs = load_documents()
q = "What was ACME revenue growth in Q2 2023?"
emb = HashEmbedder(semantic_mode=False)
rec = chunk_corpus(docs, "recursive")
pc = []
for d in docs:
    pc.extend(parent_child(d))
print("recursive", len(rec), "parent_child", len(pc))
for label, pool in ("recursive", rec), ("parent_child", pc):
    hits = dense_search(q, pool, embedder=emb, k=2)
    print(label, "top:", hits[0].chunk.chunk_id if hits else None)
    if hits:
        print(" ", hits[0].chunk.text[:180].replace("\n", " "))
