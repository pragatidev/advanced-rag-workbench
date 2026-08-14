# %% [markdown]
# # S4.4 Rerank the shortlist
#
# Retrieve a wider set, score it again, keep 4. Production uses a cross-encoder
# (Cohere rerank, bge-reranker). This lab uses lexical overlap so it runs offline.
# ARAGOG found a commercial reranker did not always beat naive RAG. Measure yours.
# Watch 512-token rerankers silently truncate long chunks.

# %%
import sys, time
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.pipelines.hybrid import run_hybrid

t0 = time.perf_counter()
out = run_hybrid("What does error code TS-999 mean?", k=4, persist=False)
print("latency_s", round(time.perf_counter() - t0, 3))
print("answer", out["answer"])
for h in out["hits"]:
    print(round(h["score"], 3), h["chunk_id"])
