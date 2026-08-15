"""Generate lecture-aligned VS Code notebooks (# %% cells). Run from course_repo."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks"


def write(rel: str, body: str) -> None:
    path = NB / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.strip() + "\n", encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


write(
    "README.md",
    """# Lecture notebooks

Each file is one screen-walk lecture. Open it in VS Code. Run Cell on each `# %%` block
(Python Interactive), or Run the whole file.

Markdown cells (`# %% [markdown]`) are the teaching. Code cells are the run.

| File | Lecture |
|---|---|
| section_01_setup/01.3_set_up_the_workbench.py | 1.3 |
| section_02_naive_rag/02.2_build_the_naive_pipeline.py | 2.2 |
| section_02_naive_rag/02.2b_vector_stores.py | 2.2 (Chroma, FAISS, Qdrant, pgvector) |
| section_02_naive_rag/02.3_the_chunk_that_lost_the_company_name.py | 2.3 |
| section_03_chunking/03.2_compare_chunkers.py | 3.2 |
| section_03_chunking/03.4_late_chunking.py | 3.4 |
| section_04_hybrid/04.2_hybrid_search_with_rrf.py | 4.2 |
| section_04_hybrid/04.3_contextual_chunks.py | 4.3 |
| section_04_hybrid/04.4_rerank_the_shortlist.py | 4.4 |
| section_05_query/05.2_rewrite_and_multi_query.py | 5.2 |
| section_05_query/05.4_run_hyde.py | 5.4 |
| section_06_retrieve_or_not/06.2_retrieve_gate.py | 6.2 |
| section_06_retrieve_or_not/06.3_support_or_refuse.py | 6.3 |
| section_07_crag/07.2_score_the_retrieved_set.py | 7.2 |
| section_07_crag/07.3_web_search_is_a_policy.py | 7.3 |
| section_08_graph/08.2_tiny_graph.py | 8.2 |
| section_09_tables/09.2_parse_tables_and_captions.py | 9.2 |
| section_09_tables/09.3_multimodal_retrieve.py | 9.3 |
| section_10_eval/10.2_run_the_suite.py | 10.2 |
| section_10_eval/10.3_cost_per_query.py | 10.3 |
| section_10_eval/10.4_traces.py | 10.4 |
| section_11_govern/11.2_metadata_filters.py | 11.2 |
| section_11_govern/11.3_audit.py | 11.3 |
| section_12_capstone/12.2_final_comparison.py | 12.2 |

Concept lectures (1.1, 1.2, 1.4, 2.1, 2.4, ...) are animated. They do not need a notebook.
""",
)

write(
    "section_01_setup/01.3_set_up_the_workbench.py",
    '''
# %% [markdown]
# # S1.3 Set up the workbench
#
# Open this folder in VS Code. This file is a normal Python notebook (`# %%` cells).
# After this lecture you can run pytest and open a real vector store folder.

# %%
from pathlib import Path
import subprocess, sys
root = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
print("project root:", root)
print("python:", sys.version.split()[0])

# %% [markdown]
# The test suite is the first proof the project is installed. It uses HashEmbedder
# (offline) and Chroma in memory. No API key.

# %%
proc = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=root)
print("pytest exit", proc.returncode)
assert proc.returncode == 0

# %% [markdown]
# Layout you will live in:
# - `data/acme/` the corpus
# - `notebooks/section_XX/` these lectures
# - `rag/` the small library notebooks import (like `src/` at work)
# - `store/chroma`, `store/faiss`, `store/qdrant` the indexes you build
# - `app.py` the product HTTP door
''',
)

write(
    "section_02_naive_rag/02.2_build_the_naive_pipeline.py",
    '''
# %% [markdown]
# # S2.2 Build the naive pipeline
#
# Naive RAG in a real project is five steps:
# 1. Load documents
# 2. Chunk
# 3. Embed with a **named** model
# 4. Write a **real vector store** (here: Chroma)
# 5. Query, then generate only from the hits
#
# We use Chroma first because that is the store most Python RAG apps start with.
# The next notebook (02.2b) runs the same chunks through FAISS, Qdrant, and pgvector.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd()
if not (ROOT / "rag").is_dir():
    ROOT = ROOT.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunking import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder, PRODUCTION_EMBEDDERS
from rag.generate import generate_answer
from rag.stores.chroma_store import ChromaStore

QUESTION = "What was ACME revenue growth in Q2 2023?"

# %% [markdown]
# ## 1. Load
# These are ordinary files. Open them in the editor. There is no hidden Nike dump.

# %%
docs = load_documents()
print(len(docs), "documents")
for d in docs:
    print(f"  {d.doc_id:18}  {d.path}")

# %% [markdown]
# ## 2. Chunk
# Naive default: fixed windows, 80 words, no overlap. That is a guess. S3 will swap it.

# %%
chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
print("chunker=fixed size=80 overlap=0 ->", len(chunks), "chunks")
print("first chunk id:", chunks[0].chunk_id)
print(chunks[0].text[:240])

# %% [markdown]
# ## 3. Name the embedder
# This cell uses HashEmbedder so the lecture runs offline.
# A shipped app would put `all-MiniLM-L6-v2` or `text-embedding-3-small` in config.

# %%
print("this cell:", HashEmbedder.name, "dim", HashEmbedder.dim)
print("production names:")
for row in PRODUCTION_EMBEDDERS:
    print(" ", row["name"], "|", row["where"], "| key=", row["key"])
embedder = HashEmbedder(semantic_mode=True)
vectors = embedder.encode([c.text for c in chunks])
print("vectors.shape", tuple(vectors.shape))

# %% [markdown]
# ## 4. Store in Chroma
# After this cell, open `store/chroma/` on disk. That folder is the index.

# %%
store = ChromaStore("naive", persist=True)
store.reset()
store.add(chunks, vectors.tolist())
print(store.info())

# %% [markdown]
# ## 5. Retrieve, then generate
# Generation is extractive (no key). A production generate would call your model API.

# %%
hits = store.query(embedder.embed(QUESTION).tolist(), k=3)
print("Q:", QUESTION)
for i, h in enumerate(hits, start=1):
    print(f"#{i} {h.score:.3f} {h.chunk.chunk_id}")
    print("   ", h.chunk.text.replace(chr(10), " ")[:160])
answer, meta = generate_answer(QUESTION, [h.chunk for h in hits], mode="extractive")
print("generator:", meta)
print("answer:", answer)
''',
)

write(
    "section_02_naive_rag/02.2b_vector_stores.py",
    '''
# %% [markdown]
# # S2.2b The same index on Chroma, FAISS, Qdrant, pgvector
#
# Real projects pick a store. They do not invent a `.npy` file format.
# This notebook writes the **same chunks and the same vectors** into every local store
# this course runs:
#
# | Store | What you open | Needs |
# |---|---|---|
# | Chroma | `store/chroma/` | pip only |
# | FAISS | `store/faiss/naive/` | pip only |
# | Qdrant | `store/qdrant/` | pip only |
# | pgvector | Postgres | `docker compose up -d` (optional) |
#
# Hosted stores we name but do not run (they need a paid key): Pinecone, Weaviate, Milvus.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd()
if not (ROOT / "rag").is_dir():
    ROOT = ROOT.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunking import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.stores.base import PRODUCTION_STORES
from rag.stores import ChromaStore, FaissStore, QdrantStore

QUESTION = "What does error code TS-999 mean?"
docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
embedder = HashEmbedder(semantic_mode=True)
vectors = embedder.encode([c.text for c in chunks]).tolist()
qvec = embedder.embed(QUESTION).tolist()

print("Stores this industry uses:")
for row in PRODUCTION_STORES:
    flag = "RUN" if row["lab"] else "name only"
    print(f"  [{flag:9}] {row['name']:12} {row['why']}")

# %% [markdown]
# ## Chroma

# %%
chroma = ChromaStore("compare", persist=True)
chroma.reset()
chroma.add(chunks, vectors)
print("CHROMA", chroma.info())
for h in chroma.query(qvec, k=2):
    print(" ", round(h.score, 3), h.chunk.chunk_id)

# %% [markdown]
# ## FAISS (IndexFlatIP, cosine via L2-normalized vectors)

# %%
faiss_store = FaissStore("compare")
faiss_store.reset()
faiss_store.add(chunks, vectors)
print("FAISS", faiss_store.info())
for h in faiss_store.query(qvec, k=2):
    print(" ", round(h.score, 3), h.chunk.chunk_id)

# %% [markdown]
# ## Qdrant (local embedded client)

# %%
qdrant = QdrantStore("compare")
qdrant.reset()
qdrant.add(chunks, vectors)
print("QDRANT", qdrant.info())
for h in qdrant.query(qvec, k=2):
    print(" ", round(h.score, 3), h.chunk.chunk_id)

# %% [markdown]
# ## pgvector (optional)
# Start Postgres first: `docker compose up -d` from the repo root.
# If it is not up, this cell prints SKIP and the rest of the course still runs.

# %%
from rag.stores import pgvector_store as pgs
if pgs.available():
    pg = pgs.PgVectorStore("compare")
    pg.reset()
    pg.add(chunks, vectors)
    print("PGVECTOR", pg.info())
    for h in pg.query(qvec, k=2):
        print(" ", round(h.score, 3), h.chunk.chunk_id)
else:
    print("SKIP pgvector. Start it with: docker compose up -d")
    print("Default URL", pgs.DEFAULT_URL)
''',
)

write(
    "section_02_naive_rag/02.3_the_chunk_that_lost_the_company_name.py",
    '''
# %% [markdown]
# # S2.3 The chunk that lost the company name
#
# Anthropic (19 Sep 2024) described this failure: the retrieved sentence is true,
# and the company name is gone. Our filing was written so a fixed 80-word split
# does the same thing. This is a chunking failure, not a model failure.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.chunking import chunk_corpus
from rag.corpus import load_documents

docs = load_documents()
chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
hit = [c for c in chunks if "revenue grew by 3%" in c.text.lower()]
assert hit, "the 3 percent sentence should still exist in some chunk"
for c in hit:
    print(c.chunk_id)
    print("  contains ACME:", "acme" in c.text.lower())
    print("  contains Q2:", "q2" in c.text.lower())
    print(c.text)
    print("---")
print("A true sentence without ACME or Q2 cannot answer 'What was ACME revenue growth in Q2 2023?'")
''',
)

write(
    "section_03_chunking/03.2_compare_chunkers.py",
    '''
# %% [markdown]
# # S3.2 Recursive vs semantic vs parent-child
#
# Same corpus. Four chunkers. Count chunks. See who keeps the heading next to 3%.
# Parent-child indexes a small window and keeps the parent section for generation
# (the sentence-window idea).

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.chunking import CHUNKERS, chunk_corpus
from rag.corpus import load_documents

docs = load_documents()
print(f"{'chunker':16} {'n':>6} {'has 3%':>8} {'3% names ACME/Q2':>18}")
for name in CHUNKERS:
    kwargs = {"size": 80, "overlap": 0} if name == "fixed" else {}
    chunks = chunk_corpus(docs, name, **kwargs) if kwargs else chunk_corpus(docs, name)
    growth = [c for c in chunks if "3%" in c.text]
    named = [c for c in growth if "acme" in c.text.lower() or "q2" in c.text.lower()]
    print(f"{name:16} {len(chunks):6} {len(growth):8} {len(named):18}")

rec = chunk_corpus(docs, "recursive")
keep = next(c for c in rec if "3%" in c.text)
print("\\nrecursive chunk with 3%:\\n", keep.chunk_id, "\\n", keep.text)
''',
)

write(
    "section_03_chunking/03.4_late_chunking.py",
    '''
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
        print(" ", hits[0].chunk.text[:180].replace("\\n", " "))
''',
)

write(
    "section_04_hybrid/04.2_hybrid_search_with_rrf.py",
    '''
# %% [markdown]
# # S4.2 Hybrid search with RRF
#
# Dense search (Chroma) misses exact IDs when the embedder is semantic.
# BM25 locks the token TS-999.
# Reciprocal Rank Fusion (k=60, Cormack 2009) merges the two lists.
# That pair is the Monday default in this course.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.chunking import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.retrieve import bm25_search, rrf_fuse
from rag.stores.chroma_store import ChromaStore

q = "What does error code TS-999 mean?"
docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
emb = HashEmbedder(semantic_mode=True)
store = ChromaStore("hybrid_demo", persist=True)
store.reset()
store.add(chunks, emb.encode([c.text for c in chunks]).tolist())

dense = store.query(emb.embed(q).tolist(), k=5)
sparse = bm25_search(q, chunks, k=5)
fused = rrf_fuse([dense, sparse], k=60, top_n=5)

def show(label, hits):
    print(label)
    for h in hits[:3]:
        print(f"  {h.score:.4f} {h.chunk.chunk_id}  {h.chunk.text[:70]!r}")

show("dense / Chroma", dense)
show("BM25", sparse)
show("RRF k=60", fused)
print("BM25 top has TS-999?", "ts-999" in sparse[0].chunk.text.lower())
''',
)

write(
    "section_04_hybrid/04.3_contextual_chunks.py",
    '''
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
print("before:\\n", raw[0].text[:180])
print("\\nafter:\\n", ctx[0].text[:220])
print("\\ncount", len(raw), "->", len(ctx))
''',
)

write(
    "section_04_hybrid/04.4_rerank_the_shortlist.py",
    '''
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
''',
)

write(
    "section_05_query/05.2_rewrite_and_multi_query.py",
    '''
# %% [markdown]
# # S5.2 Rewrite and multi-query
#
# One user question is often a bad search string. Rewrite fixes vocabulary.
# Multi-query covers facets, then you fuse with RRF. Cost: extra searches.
# Keep a rewrite only if recall moves.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.query.rewrite import multi_query, rewrite

q = "What was ACME revenue growth in Q2 2023?"
print("original:", q)
print("rewrite: ", rewrite(q))
print("multi:")
for i, item in enumerate(multi_query(q), start=1):
    print(f"  {i}. {item}")
''',
)

write(
    "section_05_query/05.4_run_hyde.py",
    '''
# %% [markdown]
# # S5.4 Run HyDE and decide
#
# Gao et al. 2022: invent a fake document, embed it, retrieve neighbors.
# The fake text is allowed to be wrong. Table 4: nDCG@10 61.3 vs 44.5 on TREC DL19.
# That is their number, not a promise for ACME. HyDE often hurts exact IDs.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.query.hyde import hypothetical_document, run_hyde

q = "What was ACME revenue growth in Q2 2023?"
print("fake document:\\n", hypothetical_document(q))
out = run_hyde(q)
print("\\nanswer:", out["answer"])
print("top hits:")
for h in out["hits"][:3]:
    print(" ", h["chunk_id"], h["text"][:100].replace("\\n", " "))
''',
)

write(
    "section_06_retrieve_or_not/06.2_retrieve_gate.py",
    '''
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
''',
)

write(
    "section_06_retrieve_or_not/06.3_support_or_refuse.py",
    '''
# %% [markdown]
# # S6.3 Support or refuse
#
# After generate, check the answer against retrieved text. If it is not supported,
# refuse. A confident lie from the wrong chunks is still a failure.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.loops.retrieve_gate import support_or_refuse

ctx = ["TS-999 means the billing ledger rejected a duplicate invoice id."]
print(support_or_refuse("TS-999 is a duplicate invoice rejection.", ctx))
print(support_or_refuse("The CEO said revenue doubled overnight.", ctx))
''',
)

write(
    "section_07_crag/07.2_score_the_retrieved_set.py",
    '''
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
''',
)

write(
    "section_07_crag/07.3_web_search_is_a_policy.py",
    '''
# %% [markdown]
# # S7.3 Web search is a policy, not a default
#
# CRAG's paper can fall back to the public web. That is a policy decision.
# Default in this repo is OFF. Turning it on sends private questions outside.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.loops import crag

print("WEB_SEARCH_ENABLED", crag.WEB_SEARCH_ENABLED)
print("maybe_web", crag.maybe_web("What is ACME revenue?"))
print("Leave the flag false unless a written policy allows the public web.")
''',
)

write(
    "section_08_graph/08.2_tiny_graph.py",
    '''
# %% [markdown]
# # S8.2 Build a tiny graph on the sample corpus
#
# Vector RAG is local. "What are the themes?" needs a community summary.
# This is a seeded toy graph, not a Microsoft GraphRAG index. Cost is printed.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.graph.tiny import answer_global, build

g = build()
print("nodes", g["nodes"])
print("members", g["members"])
print("cost", g["index_cost"])
print("answer", answer_global("What are the main themes in this ACME corpus?")["answer"])
''',
)

write(
    "section_09_tables/09.2_parse_tables_and_captions.py",
    '''
# %% [markdown]
# # S9.2 Parse tables and captions
#
# A text splitter smashes rows. We chunk one table row at a time and keep the
# figure caption as its own document. That is how 12420 and South 2000 stay findable.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.corpus import load_documents
from rag.multimodal import table_row_chunks

docs = {d.doc_id: d for d in load_documents()}
rows = table_row_chunks(docs["q2_kpis"])
print("table rows", len(rows))
for r in rows:
    print(" ", r.chunk_id, r.text)
print("\\nfigure caption:\\n", docs["figure_seats"].text)
''',
)

write(
    "section_09_tables/09.3_multimodal_retrieve.py",
    '''
# %% [markdown]
# # S9.3 Multimodal retrieve on the same questions
#
# Same questions as the eval file. Row chunks should hit 12420.
# The caption document should hit South 2000.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.multimodal import table_row_chunks
from rag.retrieve import bm25_search

docs = {d.doc_id: d for d in load_documents()}
rows = table_row_chunks(docs["q2_kpis"])
hits = bm25_search("How many paid seats did ACME have in Q2?", rows, k=2)
print("table retrieve:")
for h in hits:
    print(" ", h.chunk.text)
print("12420 in top?", any("12420" in h.chunk.text for h in hits))
print("caption has South 2000?", "South 2000" in docs["figure_seats"].text)
''',
)

write(
    "section_10_eval/10.2_run_the_suite.py",
    '''
# %% [markdown]
# # S10.2 Run the suite
#
# One question file. Two pipelines. Faithfulness is not context recall.
# The metrics file is what you keep or kill a technique with.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.eval.runner import run_eval

summary = run_eval(a="naive", b="hybrid")
print("n", summary["n"])
print("mean", summary["mean"])
print("wrote runs/naive_vs_hybrid/metrics.json")
''',
)

write(
    "section_10_eval/10.3_cost_per_query.py",
    '''
# %% [markdown]
# # S10.3 Cost per query
#
# Local HashEmbedder + extractive generate is $0.00. The column still exists so
# you see generate_calls. HyDE adds a generate. A live API fills USD from usage.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.eval.cost import estimate

for name, extra in ("naive", 0), ("hybrid", 0), ("hyde", 1):
    print(name, estimate(name, extra_generates=extra))
''',
)

write(
    "section_10_eval/10.4_traces.py",
    '''
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
''',
)

write(
    "section_11_govern/11.2_metadata_filters.py",
    '''
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
''',
)

write(
    "section_11_govern/11.3_audit.py",
    '''
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
''',
)

write(
    "section_12_capstone/12.2_final_comparison.py",
    '''
# %% [markdown]
# # S12.2 Run the final comparison
#
# Naive vs hybrid on the same question file. Keep the winner. Write a one-page
# decision note from `runs/naive_vs_hybrid/metrics.json`. That is the course.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.eval.runner import run_eval

summary = run_eval(a="naive", b="hybrid")
print(summary["mean"])
print("Open runs/naive_vs_hybrid/metrics.json and defend the stack you keep.")
''',
)


if __name__ == "__main__":
    print("done")
