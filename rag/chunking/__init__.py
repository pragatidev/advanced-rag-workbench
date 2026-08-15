"""Chunking package. Stores and notebooks import Chunk from here."""

from rag.chunkers import (
    CHUNKERS,
    Chunk,
    chunk_corpus,
    contextualize,
    fixed_size,
    parent_child,
    recursive,
    semantic_by_heading,
    semantic_cosine,
    token_count,
)
from rag.chunking.auto_merge import merge_hits as auto_merge_hits
from rag.chunking.late import late_vectors
from rag.chunking.semantic import cosine_breakpoint_chunks, pairwise_similarities
from rag.chunking.sentence_window import build as sentence_window_chunks
from rag.chunking.sentence_window import expand_window

__all__ = [
    "CHUNKERS",
    "Chunk",
    "auto_merge_hits",
    "chunk_corpus",
    "contextualize",
    "cosine_breakpoint_chunks",
    "expand_window",
    "fixed_size",
    "late_vectors",
    "pairwise_similarities",
    "parent_child",
    "recursive",
    "semantic_by_heading",
    "semantic_cosine",
    "sentence_window_chunks",
    "token_count",
]
