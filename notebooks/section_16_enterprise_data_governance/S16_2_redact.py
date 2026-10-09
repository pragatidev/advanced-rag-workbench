# %% [markdown]
# # S16.2 Why PII redaction and retrieved-text injection are one job
#
# Mask PII before the prompt. Retrieved text stays data.
# Regex is a stand-in for a Presidio-shaped detector.

# %%
"""S16.2: redact before generate; retrieved text stays data."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import Chunk, chunk_corpus
from rag.corpus import load_documents
from rag.generate import HYGIENE, generate
from rag.gov import DETECTOR, redact
from rag.llm import SYSTEM

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
privacy = next(c for c in chunks if c.doc_id == "privacy")
query = "What must retrieval redact?"

print("=== detector ===")
print("detector", DETECTOR)
print("stand_in", DETECTOR == "national_id_phrase")

print()
print("=== three sites ===")
print("input question before retrieve")
print("chunk retrieved text before generate")
print("output answer before it leaves")

print()
print("=== privacy chunk ===")
print("chunk_id", privacy.chunk_id)
print("raw_has_national_id", "national id" in privacy.text.lower())

print()
print("=== late redact ===")
raw_answer = generate(query, [privacy])
late_answer = redact(raw_answer)
print("query", query)
print("raw_answer", raw_answer)
print("late_answer", late_answer)
print("model_saw_pii", "national id" in raw_answer.lower())

print()
print("=== redact before generate ===")
sent = redact(privacy.text)
red_chunk = Chunk(
    chunk_id=privacy.chunk_id,
    doc_id=privacy.doc_id,
    title=privacy.title,
    text=sent,
    metadata=dict(privacy.metadata),
)
early_answer = generate(query, [red_chunk])
print("sent_has_national_id", "national id" in sent.lower())
print("sent_has_redacted", "[REDACTED_PII]" in sent)
print("redacted_count", sent.count("[REDACTED_PII]"))
print("early_answer", early_answer)
print("model_saw_pii", "national id" in sent.lower())

print()
print("=== hygiene ===")
print(HYGIENE)
print(SYSTEM)
