"""ACME RAG workbench. One corpus, one question file, every pipeline prints a delta."""

from rag.ask import run_ask
from rag.corpus import load_documents

__version__ = "0.1.0"
__all__ = ["load_documents", "run_ask"]
