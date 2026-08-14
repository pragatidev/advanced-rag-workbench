"""Retrieve-or-not. This is a prompt-loop, not Asai's trained Self-RAG tokens."""

from __future__ import annotations

import re

_CHITCHAT = re.compile(
    r"^(hi|hello|hey|good morning|good evening|how are you|thanks|thank you)\b",
    re.I,
)


def needs_corpus(question: str) -> bool:
    q = question.strip()
    if _CHITCHAT.search(q) and len(q.split()) <= 8:
        return False
    return True


def support_or_refuse(answer: str, retrieved_texts: list[str]) -> str:
    blob = " ".join(retrieved_texts).lower()
    tokens = [t for t in re.findall(r"[a-z0-9%]{3,}", answer.lower())]
    if not tokens:
        return "REFUSE: empty answer."
    supported = sum(1 for t in tokens if t in blob)
    if supported / len(tokens) < 0.4:
        return "REFUSE: answer is not supported by retrieved text."
    return answer
