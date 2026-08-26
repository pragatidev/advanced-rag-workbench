"""Step four of a tiny graph: pay the index bill only after a global question failed.

Runs the whole path in one process: the refuse gate, the index with its cost on
screen, then the global answer read from summaries. TOY. Parts one through three
extracted entities with a seed dictionary instead of a language model, so the
real bill here is zero. The counter prints the toy number and the real number
side by side.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Ships extractive: no key is spent to teach a cost lesson. Set before any rag
# import reads it. A value already in your shell wins over this one.
os.environ.setdefault("RAGBENCH_GENERATE", "extractive")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# labs/ is not a package, so part_1 and part_2 go on the path by folder.
for folder in ("part_1", "part_2"):
    path = HERE.parent / folder
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from build_tiny_graph import (  # noqa: E402
    SEED,
    build_communities,
    build_edges,
    build_members,
    load_chunks,
)
from community_summaries import community_chunks, summarize  # noqa: E402

from rag.pipelines.hybrid import run_hybrid  # noqa: E402

LOCAL_Q = "What does error code TS-999 mean?"
GLOBAL_Q = "What are the main themes in this ACME corpus?"
ANSWER_TOKEN = "TS-999"

# The questions that actually failed on this pipeline, and what kind each one is.
# A graph is earned by a global entry, never by a local one.
FAILURE_LOG = ((LOCAL_Q, "local"), (GLOBAL_Q, "global"))


def local_holds() -> bool:
    """Does the cured hybrid pipeline still answer the local question?"""
    result = run_hybrid(LOCAL_Q)
    top = result["hits"][0]
    print(f"  top hit {top['chunk_id']:24s} {top['score']:.4f}")
    found = ANSWER_TOKEN in " ".join(hit["text"] for hit in result["hits"])
    print(f"  {ANSWER_TOKEN} in retrieved text {found}")
    return found


def refuse_if_local_holds(holds: bool) -> str | None:
    """The whole rule. Four lines."""
    if holds:
        return "REFUSE: local questions still hold. Do not pay for a graph index."
    return None


def gate() -> bool:
    """Open only when something that failed needed the whole corpus."""
    for question, kind in FAILURE_LOG:
        print(f"  {kind:7s} {question}")
    return any(kind == "global" for _, kind in FAILURE_LOG)


def build_index():
    """Part one's graph, part two's summarizer. Everything a graph costs happens here."""
    chunks = load_chunks()
    members = build_members(chunks)
    edges = build_edges(chunks, members)
    communities = build_communities(members, edges)
    by_id = {chunk.chunk_id: chunk.text for chunk in chunks}

    summaries = []
    summary_calls = 0
    mode = "extractive"
    for i, entity_names in enumerate(communities):
        name = f"community_{i}"
        chunk_ids = community_chunks(entity_names, members)
        summary, mode = summarize(name, entity_names, [by_id[cid] for cid in chunk_ids])
        if mode == "api":
            summary_calls += 1
        summaries.append((name, entity_names, summary))
    return chunks, members, communities, summaries, summary_calls, mode


def index_bill(chunks, communities, summary_calls, mode) -> int:
    """The bill, printed from the same variables the index was built from."""
    print(f"  chunks_indexed     {len(chunks)}")
    print(f"  entities           {len(SEED)}")
    print(f"  communities        {len(communities)}")
    print("  llm_extract_calls  0   seed dictionary, not a model extract")
    print(f"  llm_summary_calls  {summary_calls}   mode {mode}")
    total = len(chunks) + len(communities)
    print(
        f"  a real GraphRAG index here: {len(chunks)} extract calls "
        f"+ {len(communities)} summary calls = {total} model calls "
        f"before anyone asks a question"
    )
    return total


def answer_global(summaries) -> str:
    """Global mode reads what index time already wrote."""
    print("  chunks searched at question time 0")
    for name, entity_names, summary in summaries:
        print(f"  {name}  entities: {', '.join(entity_names)}")
        print(f"    {summary}")
    answer = " ".join(summary for _, _, summary in summaries)
    print(f"  answer: {answer}")
    return answer


def main() -> None:
    print("BLOCK 1  the refuse gate")
    holds = local_holds()
    refusal = refuse_if_local_holds(holds)
    print(f"  {refusal}" if refusal else "  local no longer holds")
    print()

    print("BLOCK 2  the question that earns the bill")
    earned = gate()
    print(f"  a global question is in the log {earned}")
    print()

    print("BLOCK 3  the index, and what it cost")
    chunks, members, communities, summaries, summary_calls, mode = build_index()
    total = index_bill(chunks, communities, summary_calls, mode)
    print()

    print("BLOCK 4  the global answer")
    print(f"  QUESTION {GLOBAL_Q}")
    answer_global(summaries)
    print()

    board = {
        "llm_extract_calls": 0,
        "llm_summary_calls": summary_calls,
        "real_graphrag_index_calls": total,
        "refuse_local": refuse_if_local_holds(True),
    }
    dest = ROOT / "runs" / "smoke" / "graph_board.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(board, indent=2, ensure_ascii=False), encoding="utf-8")
    print("wrote", dest.as_posix())


if __name__ == "__main__":
    main()
