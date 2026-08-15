from rag.loops.crag import WEB_SEARCH_ENABLED, grade, maybe_web
from rag.loops.tool_loop import NODES, run_loop


def test_section_11_crag_loop():
    assert WEB_SEARCH_ENABLED is False
    assert maybe_web("q") is None
    assert grade("q", []) == "Incorrect"
    assert set(NODES) >= {"decide", "retrieve", "grade", "rewrite", "answer"}
    out = run_loop("What does error code TS-999 mean?", web_enabled=False)
    assert out["web_called"] is False
    assert "decide" in out["path"]
    assert "hygiene" in out
