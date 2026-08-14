from rag.graph.tiny import answer_global
from rag.pipelines.hybrid import run_hybrid
from rag.pipelines.naive import run_naive
from rag.query.hyde import run_hyde

PIPELINES = {
    "naive": run_naive,
    "hybrid": run_hybrid,
    "hyde": run_hyde,
    "graph": answer_global,
}

__all__ = ["PIPELINES", "run_naive", "run_hybrid", "run_hyde", "answer_global"]
