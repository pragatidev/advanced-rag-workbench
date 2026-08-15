"""Graph cost and refuse when local holds."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import json

from rag.graph.tiny import answer_global, build, refuse_if_local_holds
from rag.pipelines.hybrid import run_hybrid

local_q = "What does error code TS-999 mean?"
global_q = "What are the main themes in this ACME corpus?"
local = run_hybrid(local_q)
print("local_ok", "TS-999" in " ".join(h["text"] for h in local["hits"]))
print(refuse_if_local_holds(True))
g = build()
print("index_cost", g["index_cost"])
print(answer_global(global_q)["answer"])
board = {"index_cost": g["index_cost"], "refuse_local": refuse_if_local_holds(True)}
dest = ROOT / "runs" / "smoke" / "graph_board.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(board, indent=2), encoding="utf-8")
print("wrote", dest)
