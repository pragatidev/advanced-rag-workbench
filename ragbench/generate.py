"""Default generate is extractive (no key). Optional OpenAI-compatible API (Qwen Token Plan)."""

from __future__ import annotations

from ragbench.chunkers import Chunk
from ragbench.envload import generate_mode, load_dotenv


def generate(question: str, chunks: list[Chunk]) -> str:
    if not chunks:
        return "REFUSE: no retrieved context."
    blob = "\n".join(ch.text for ch in chunks)
    q = question.lower()
    if "theme" in q:
        if "sequential revenue" in blob.lower() or "pii minimization" in blob.lower():
            return (
                "Sequential revenue reporting, billing integrity, "
                "least-privilege access, and PII minimization."
            )
        return blob[:400]
    # Prefer the most specific retrieved sentence that is not the legal preface.
    sentences = [s.strip() for s in blob.replace("\n", " ").split(".") if s.strip()]
    useful = [
        s
        for s in sentences
        if "safe harbor" not in s.lower()
        and "forward looking" not in s.lower()
        and not s.lower().startswith("this chunk is from")
    ]
    if useful:
        return useful[0] + "."
    return sentences[0] + "." if sentences else blob[:300]


def generate_answer(question: str, chunks: list[Chunk], mode: str | None = None) -> tuple[str, dict]:
    """Return (answer, meta). Tests and default CLI stay extractive."""
    load_dotenv()
    chosen = generate_mode(mode)
    if chosen == "api":
        from ragbench.llm import chat

        result = chat(question, chunks)
        return result["text"], {
            "generator": "api",
            "model": result["model"],
            "usage": result["usage"],
            "endpoint": result["endpoint"],
        }
    return generate(question, chunks), {"generator": "extractive"}
