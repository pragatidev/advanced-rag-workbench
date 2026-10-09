import subprocess
import sys
from pathlib import Path

from rag.multimodal import caption_chunks, multimodal_chunks, parse_tables, smash_report
from rag.retrieve import bm25_search

ROOT = Path(__file__).resolve().parents[1]
S13_1 = ROOT / "notebooks/section_13_multimodal_tables_and_images/S13_1_smash_and_restore.py"
S13_2 = ROOT / "notebooks/section_13_multimodal_tables_and_images/S13_2_caption_vs_page.py"
S13_6 = ROOT / "labs/lab_s13_mm/part_4/run_multimodal.py"


def test_section_13_tables_and_captions():
    smash = smash_report()
    assert smash["has_12420"]
    parsed = parse_tables()
    assert parsed["parser"] in {"docling", "markdown-fallback"}
    assert any("12420" in r["text"] for r in parsed["rows"])
    assert "South 2000" in caption_chunks()[0].text
    hits = bm25_search("paid seats Q2", multimodal_chunks(), k=3)
    assert any("12420" in h.chunk.text for h in hits)


def test_s13_1_screened_receipts():
    out = subprocess.run(
        [sys.executable, str(S13_1)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    ).stdout
    assert "pdf data/acme/tables/q2_kpis.pdf" in out
    assert "row_intact False" in out
    assert "has_12420 True" in out
    assert "(paid_seats 11800)" in out
    assert "(12420)" in out
    assert "parser markdown-fallback" in out
    assert "paid_seats | 11800 | 12420" in out


def test_s13_2_screened_receipts():
    out = subprocess.run(
        [sys.executable, str(S13_2)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    ).stdout
    assert "file data/acme/figures/caption.txt" in out
    assert "has_South_2000 True" in out
    assert "top_has_South_2000 True" in out
    assert "table_has_South_2000 False" in out
    assert "name ColPali ColQwen" in out
    assert "lab installed False" in out
    assert "tax next" in out


def test_s13_6_screened_receipts():
    out = subprocess.run(
        [sys.executable, str(S13_6)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    ).stdout
    assert "chunks 3" in out
    assert "q2_kpis:row:0" in out
    assert "figure_seats:caption:0" in out
    assert "paid_seats | 11800 | 12420" in out
    assert "12420 True" in out
    assert "South 2000 True" in out
    table_block = out.split("=== table question ===", 1)[1].split("=== figure question ===", 1)[0]
    figure_block = out.split("=== figure question ===", 1)[1]
    assert "1 q2_kpis:row:0" in table_block
    assert "1 figure_seats:caption:0" in figure_block
