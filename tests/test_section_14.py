from rag.chunkers import fixed_size, recursive
from rag.corpus import load_documents
from rag.eval.golden import confirm_tags
from rag.eval.judge import agreement, pick_first, pick_longer, pick_same_family
from rag.eval.metrics import (
    average_precision,
    context_recall,
    faithfulness,
    mrr,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
)
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


def test_section_14_ranking_metrics_two_golds_at_bottom():
    rels = [0, 0, 0, 1, 1]
    assert precision_at_k(rels, 5) == 0.4
    assert recall_at_k(rels, 5) == 1.0
    assert mrr(rels) == 0.25
    assert average_precision(rels) == 0.325
    assert round(ndcg_at_k(rels, 5), 4) == 0.5013
    first_then_second = [1, 1, 0, 0, 0]
    first_then_buried = [1, 0, 0, 0, 1]
    assert mrr(first_then_second) == mrr(first_then_buried) == 1.0
    assert average_precision(first_then_second) == 1.0
    assert average_precision(first_then_buried) == 0.7


def test_section_14_judge_failure_modes():
    gold = "ACME revenue grew by 3% over the previous quarter."
    miss = "Warehouse throughput improved. Marketing spend was steady."
    verbose_miss = (
        "Warehouse throughput improved. Marketing spend was steady. "
        "Nothing in this preface names the growth rate. "
        "The filing discusses seasonality, supply chain recovery, "
        "and the way management talks about sequential growth."
    )
    assert pick_first(gold, miss) == gold
    assert pick_first(miss, gold) == miss
    assert pick_longer(gold, verbose_miss) == verbose_miss
    assert pick_same_family((gold, "other"), (verbose_miss, "family_a"), "family_a") == verbose_miss
    agree, n = agreement([(gold, gold), (gold, miss), (gold, verbose_miss), (gold, verbose_miss)])
    assert (agree, n) == (1, 4)
    docs = {d.doc_id: d for d in load_documents()}
    filing = docs["filing_q2_2023"]
    fixed_ids = {c.chunk_id for c in fixed_size(filing)}
    rec_ids = {c.chunk_id for c in recursive(filing)}
    assert fixed_ids
    assert rec_ids
    assert not (fixed_ids & rec_ids)
