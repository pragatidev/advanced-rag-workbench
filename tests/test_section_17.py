from pathlib import Path

from rag.eval.runner import run_eval

ROOT = Path(__file__).resolve().parents[1]


def test_section_17_capstone(tmp_path):
    summary = run_eval(a="naive", b="hybrid", out_dir=tmp_path)
    assert "context_recall" in summary["mean"]["naive"]
    assert "context_recall" in summary["mean"]["hybrid"]
    note = ROOT / "docs" / "mechanisms" / "capstone_brief.md"
    refuse = ROOT / "docs" / "mechanisms" / "refuse_shelf.md"
    assert note.is_file() and refuse.is_file()
