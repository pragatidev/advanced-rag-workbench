"""Chunkers. Swap them. Measure. Recursive is the hybrid default until eval says otherwise."""

from __future__ import annotations

from dataclasses import dataclass, field

from ragbench.corpus import Document
from ragbench.text import tokenize


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    text: str
    metadata: dict = field(default_factory=dict)
    parent_text: str | None = None


def _words(text: str) -> list[str]:
    return text.split()


def _join(words: list[str]) -> str:
    return " ".join(words).strip()


def fixed_size(doc: Document, size: int = 80, overlap: int = 0) -> list[Chunk]:
    words = _words(doc.text)
    chunks: list[Chunk] = []
    i = 0
    n = 0
    step = max(size - overlap, 1)
    while i < len(words):
        piece = _join(words[i : i + size])
        if piece:
            chunks.append(
                Chunk(
                    chunk_id=f"{doc.doc_id}:fixed:{n}",
                    doc_id=doc.doc_id,
                    title=doc.title,
                    text=piece,
                    metadata={**doc.metadata, "chunker": "fixed", "offset": i},
                )
            )
            n += 1
        i += step
    return chunks


def recursive(doc: Document, size: int = 120, overlap: int = 20) -> list[Chunk]:
    """Split on headings, then fall back to word windows."""
    parts = [p.strip() for p in doc.text.split("\n## ")]
    chunks: list[Chunk] = []
    n = 0
    for part in parts:
        words = _words(part)
        if len(words) <= size:
            if part:
                chunks.append(
                    Chunk(
                        chunk_id=f"{doc.doc_id}:rec:{n}",
                        doc_id=doc.doc_id,
                        title=doc.title,
                        text=part,
                        metadata={**doc.metadata, "chunker": "recursive"},
                    )
                )
                n += 1
            continue
        i = 0
        step = max(size - overlap, 1)
        while i < len(words):
            piece = _join(words[i : i + size])
            if piece:
                chunks.append(
                    Chunk(
                        chunk_id=f"{doc.doc_id}:rec:{n}",
                        doc_id=doc.doc_id,
                        title=doc.title,
                        text=piece,
                        metadata={**doc.metadata, "chunker": "recursive", "offset": i},
                    )
                )
                n += 1
            i += step
    return chunks


def parent_child(doc: Document, child_size: int = 40) -> list[Chunk]:
    """Index small windows. Keep the parent section for generation."""
    sections = [p.strip() for p in doc.text.split("\n## ") if p.strip()]
    chunks: list[Chunk] = []
    n = 0
    for section in sections:
        words = _words(section)
        i = 0
        while i < len(words):
            child = _join(words[i : i + child_size])
            if child:
                chunks.append(
                    Chunk(
                        chunk_id=f"{doc.doc_id}:pc:{n}",
                        doc_id=doc.doc_id,
                        title=doc.title,
                        text=child,
                        parent_text=section,
                        metadata={**doc.metadata, "chunker": "parent_child"},
                    )
                )
                n += 1
            i += child_size
    return chunks


def semantic_by_heading(doc: Document) -> list[Chunk]:
    """Cheap stand-in for semantic chunking: one chunk per heading block."""
    parts = [p.strip() for p in doc.text.split("\n## ") if p.strip()]
    chunks: list[Chunk] = []
    for n, part in enumerate(parts):
        chunks.append(
            Chunk(
                chunk_id=f"{doc.doc_id}:sem:{n}",
                doc_id=doc.doc_id,
                title=doc.title,
                text=part,
                metadata={**doc.metadata, "chunker": "semantic_heading"},
            )
        )
    return chunks


def contextualize(chunk: Chunk) -> Chunk:
    """Anthropic-style prefix. Short. Uses the title we already have. No LLM call."""
    prefix = f"This chunk is from {chunk.title} (doc {chunk.doc_id})."
    return Chunk(
        chunk_id=chunk.chunk_id + ":ctx",
        doc_id=chunk.doc_id,
        title=chunk.title,
        text=f"{prefix} {chunk.text}",
        metadata={**chunk.metadata, "contextual": True},
        parent_text=chunk.parent_text,
    )


CHUNKERS = {
    "fixed": fixed_size,
    "recursive": recursive,
    "parent_child": parent_child,
    "semantic": semantic_by_heading,
}


def chunk_corpus(docs: list[Document], name: str = "fixed", **kwargs) -> list[Chunk]:
    fn = CHUNKERS[name]
    out: list[Chunk] = []
    for doc in docs:
        out.extend(fn(doc, **kwargs) if kwargs else fn(doc))
    return out


def token_count(chunk: Chunk) -> int:
    return len(tokenize(chunk.text))
