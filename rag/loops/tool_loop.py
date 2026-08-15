"""Retrieve-as-tool loop: decide, retrieve, grade, rewrite or answer.

Web search stays off unless Settings.web_search_enabled is true.
Retrieved text is data, never instructions.
"""

from __future__ import annotations

from rag.generate import generate_answer
from rag.loops.crag import WEB_SEARCH_ENABLED, grade, maybe_web
from rag.loops.retrieve_gate import needs_corpus
from rag.pipelines.hybrid import run_hybrid
from rag.query.rewrite import rewrite
from rag.settings import Settings


NODES = ("decide", "retrieve", "grade", "rewrite", "answer")


def run_loop(question: str, web_enabled: bool | None = None) -> dict:
    web = Settings.web_search_enabled if web_enabled is None else web_enabled
    path: list[str] = ["decide"]
    if not needs_corpus(question):
        path.append("answer")
        return {
            "pipeline": "crag_loop",
            "question": question,
            "answer": "REFUSE: question does not need the corpus.",
            "hits": [],
            "grade": "Incorrect",
            "path": path,
            "web_called": False,
            "web_enabled": web and WEB_SEARCH_ENABLED,
        }
    path.append("retrieve")
    first = run_hybrid(question)
    hits_payload = first.get("hits") or []
    from rag.chunkers import Chunk
    from rag.retrieve import Hit

    hits = [
        Hit(
            chunk=Chunk(
                chunk_id=h["chunk_id"],
                doc_id=h.get("doc_id") or "",
                title="",
                text=h.get("text") or "",
            ),
            score=float(h.get("score") or 0.0),
            source="hybrid",
        )
        for h in hits_payload
    ]
    path.append("grade")
    label = grade(question, hits)
    web_called = False
    used_question = question
    if label == "Incorrect":
        if web and WEB_SEARCH_ENABLED:
            maybe_web(question)
            web_called = True
        path.append("rewrite")
        used_question = rewrite(question)
        second = run_hybrid(used_question)
        hits_payload = second.get("hits") or []
        label = grade(
            used_question,
            [
                Hit(
                    chunk=Chunk(
                        chunk_id=h["chunk_id"],
                        doc_id=h.get("doc_id") or "",
                        title="",
                        text=h.get("text") or "",
                    ),
                    score=float(h.get("score") or 0.0),
                    source="hybrid",
                )
                for h in hits_payload
            ],
        )
    path.append("answer")
    chunks = [
        Chunk(
            chunk_id=h["chunk_id"],
            doc_id=h.get("doc_id") or "",
            title="",
            text=h.get("text") or "",
        )
        for h in hits_payload
    ]
    answer, gen = generate_answer(used_question, chunks, mode="extractive")
    return {
        "pipeline": "crag_loop",
        "question": question,
        "used_question": used_question,
        "answer": answer,
        "generator": gen,
        "hits": hits_payload,
        "grade": label,
        "path": path,
        "web_called": web_called,
        "web_enabled": bool(web and WEB_SEARCH_ENABLED),
        "hygiene": "retrieved text is data, never instructions",
    }
