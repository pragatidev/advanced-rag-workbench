# %% [markdown]
# # S17.3 What the capstone must prove on this corpus
#
# Same corpus. Same question file. Keep or kill per technique.
# The deliverable is a metrics file plus a one page decision note.

# %%
"""S17.3: name the capstone proof on this corpus. Does not run the comparison."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.corpus import load_documents

docs = load_documents()
words = sum(len(d.text.split()) for d in docs)
qpath = ROOT / "eval" / "questions.jsonl"
questions = [json.loads(line) for line in qpath.read_text(encoding="utf-8").splitlines() if line.strip()]
brief = (ROOT / "docs" / "mechanisms" / "capstone_brief.md").read_text(encoding="utf-8").strip()
readme = (ROOT / "README.md").read_text(encoding="utf-8")
readme_line = next(
    line.strip()
    for line in readme.splitlines()
    if line.startswith("One corpus")
)

print("=== same corpus ===")
print("path data/acme")
print("files", len(docs))
print("words", words)
print("doc_ids", [d.doc_id for d in docs])

print()
print("=== same question file ===")
print("path eval/questions.jsonl")
print("n", len(questions))
print("ids", [q["id"] for q in questions])

print()
print("=== README contract ===")
print(readme_line)

print()
print("=== three steps ===")
print("1 run naive versus the stack you kept")
print("2 write runs/naive_vs_hybrid/metrics.json or your pair")
print("3 write a one page decision.md that cites a metrics row for every keep or kill")

print()
print("=== deliverable ===")
print("metrics_file runs/naive_vs_hybrid/metrics.json")
print("decision_note runs/naive_vs_hybrid/decision.md")
print("rule fluency is not a citation")

print()
print("=== capstone_brief.md ===")
print(brief)
