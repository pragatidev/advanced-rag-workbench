import subprocess
import sys
from pathlib import Path

from rag.eval.runner import run_eval

ROOT = Path(__file__).resolve().parents[1]
S17_2 = ROOT / "labs/lab_s17_walk/part_1/whiteboard_stack.py"


def test_section_17_design_walk():
    page = (ROOT / "docs" / "mechanisms" / "system_design_walk.md").read_text(encoding="utf-8")
    assert "six stations in interview order" in page
    assert "tombstone" in page
    assert "missing, mis-ranked, ignored" in page
    assert "Refuse to start at a vendor name" in page


def test_section_17_whiteboard_stack():
    out = subprocess.run(
        [sys.executable, str(S17_2)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    ).stdout
    assert "=== whiteboard, not vendor logos ===" in out
    assert "corpus data/acme files 7 words 571" in out
    assert "embedder HashEmbedder dim 64" in out
    assert "backend chroma" in out
    assert "rrf_k 60" in out
    assert "BAAI/bge-reranker-base" in out
    assert "east 12 west 11" in out
    assert "path rag/generate.py extractive True" in out
    assert "tenant pre-filter" in out
    assert "embed 50-100 ms" in out
    assert "naive generate_calls 1 usd 0.0" in out
    assert "hyde generate_calls 2 usd 0.0" in out
    assert "rule refuse Hyde when p95 budget is 2 seconds" in out


def test_section_17_capstone(tmp_path):
    summary = run_eval(a="naive", b="hybrid", out_dir=tmp_path)
    assert "context_recall" in summary["mean"]["naive"]
    assert "context_recall" in summary["mean"]["hybrid"]
    note = ROOT / "docs" / "mechanisms" / "capstone_brief.md"
    refuse = ROOT / "docs" / "mechanisms" / "refuse_shelf.md"
    assert note.is_file() and refuse.is_file()
    refuse_text = refuse.read_text(encoding="utf-8")
    assert "The refuse is the point. You can name the paper and still not ship it." in refuse_text
    assert "Course 2 is Agentic Architecture" in refuse_text
    assert "RAFT" in refuse_text
    assert "ColPali GPU" in refuse_text
    assert "SWE-bench" in refuse_text
