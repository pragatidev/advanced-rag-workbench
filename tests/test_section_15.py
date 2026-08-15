from rag.cache import SemanticCache
from rag.eval.cost import estimate
from rag.observe import missing_span_fields, shape_span


def test_section_15_cost_cache_trace():
    assert estimate("hyde", extra_generates=1)["generate_calls"] == 2
    assert estimate("naive")["generate_calls"] == 1
    cache = SemanticCache()
    cache.store("What does error code TS-999 mean?", "dup")
    assert cache.lookup("What does error code TS-999 mean?")["status"] == "HIT"
    assert cache.lookup("mine", personalized=True)["status"] == "SKIP_PERSONALIZED"
    span = shape_span(
        question="q",
        pipeline="hybrid",
        chunk_ids=["c1"],
        model="extractive",
        latency_ms=1.0,
        tokens=10,
        usd=0.0,
    )
    assert missing_span_fields(span) == []
