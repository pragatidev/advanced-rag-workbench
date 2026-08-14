from rag.eval.metrics import context_recall, faithfulness
from rag.eval.runner import run_eval
from rag.graph.tiny import answer_global
from rag.gov import audit_row, redact
from rag.chunkers import Chunk
from rag.loops.crag import WEB_SEARCH_ENABLED, grade
from rag.retrieve import Hit


def test_metrics_split_retrieval_from_generation():
    recall = context_recall(["revenue grew by 3%"], ["The company's revenue grew by 3% over the previous quarter."])
    faith = faithfulness("Revenue grew by 3%.", ["The company's revenue grew by 3% over the previous quarter."])
    assert recall == 1.0
    assert faith > 0.5


def test_eval_writes_naive_vs_hybrid(tmp_path):
    summary = run_eval(a="naive", b="hybrid", out_dir=tmp_path)
    assert (tmp_path / "metrics.json").is_file()
    assert summary["n"] >= 5
    assert "context_recall" in summary["mean"]["hybrid"]


def test_eval_accepts_hyde_and_graph(tmp_path):
    summary = run_eval(a="hyde", b="graph", out_dir=tmp_path)
    assert summary["mean"]["graph"]["context_recall"] >= 0.0
    assert (tmp_path / "metrics.json").is_file()


def test_graph_answers_global_themes():
    result = answer_global("What are the main themes in this ACME corpus?")
    text = result["answer"].lower()
    assert "sequential revenue" in text
    assert "pii minimization" in text
    assert result["graph"]["index_cost"]["llm_extract_calls"] == 0


def test_web_search_defaults_off():
    assert WEB_SEARCH_ENABLED is False


def test_crag_grades_empty_incorrect():
    assert grade("anything", []) == "Incorrect"
    hit = Hit(
        chunk=Chunk(chunk_id="c", doc_id="d", title="t", text="TS-999 duplicate invoice"),
        score=1.0,
        source="x",
    )
    assert grade("What does TS-999 mean?", [hit]) in {"Correct", "Ambiguous"}


def test_redact_and_audit():
    text = redact("Do not send a national id to the model.")
    assert "[REDACTED_PII]" in text
    row = audit_row("q", [Chunk(chunk_id="c1", doc_id="d", title="t", text="hello")])
    assert row["chunk_ids"] == ["c1"]
    assert row["chunk_hashes"]
