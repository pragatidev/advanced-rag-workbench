"""S11B.1 The hop budget and the stop condition, written against the Section 11 loop.

Run it from the workbench root: python hop_budget.py
"""

from __future__ import annotations

from rag.loops.tool_loop import EDGES, NODES, run_loop

QUESTION = (
    "Can I paste a national id into ACME's assistant, and what does the "
    "retention policy require before that text reaches a model?"
)

MAX_HOPS = 2


def stop_reason(hops: int, grade: str, chunk_ids: set[str], seen: set[str]) -> str:
    if grade == "Correct":
        return "grade is Correct"
    if chunk_ids and chunk_ids <= seen:
        return "this hop returned only chunks already seen"
    if hops >= MAX_HOPS:
        return "hop budget spent"
    return ""


print("nodes", NODES)
for src, dst, when in EDGES:
    mark = "   <-- the only edge out of rewrite" if src == "rewrite" else ""
    print(f"  {src} -> {dst}   [{when}]{mark}")
print("edges leaving rewrite:", sum(1 for edge in EDGES if edge[0] == "rewrite"))

out = run_loop(QUESTION, web_enabled=False)
hops = 1 + out["path"].count("rewrite")
chunk_ids = {hit["chunk_id"] for hit in out["hits"]}

print("path", out["path"])
print("hops", hops, "of", MAX_HOPS)
print("stop:", stop_reason(hops, out["grade"], chunk_ids, set()))
