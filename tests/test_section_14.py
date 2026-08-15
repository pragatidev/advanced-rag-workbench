from rag.eval.golden import confirm_tags
from rag.eval.metrics import context_recall, faithfulness
from rag.eval.runner import run_eval


def test_section_14_eval_harness(tmp_path):
    assert confirm_tags()["ok"]
    gold = ["revenue grew by 3%"]
    wrong = ["Most error codes in general are transient."]
    assert context_recall(gold, wrong) == 0.0
    # fluent wrong-span answer is not supported by the retrieved set
    assert faithfulness("Revenue grew by 3%.", wrong) < 0.5
    summary = run_eval(a="naive", b="hybrid", out_dir=tmp_path)
    assert (tmp_path / "metrics.json").is_file()
    assert summary["n"] >= 5
