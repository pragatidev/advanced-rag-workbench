import subprocess
import sys
from pathlib import Path

from rag.multimodal import dump_print_commands

ROOT = Path(__file__).resolve().parents[1]
DUMP = ROOT / "notebooks/section_13_multimodal_tables_and_images/S13_1_dump_print_commands.py"
RESTORE = ROOT / "notebooks/section_13_multimodal_tables_and_images/S13_1_restore_rows.py"


def test_dump_print_commands_shears_12420_off_the_label():
    dump = dump_print_commands()
    assert dump["pdf"] == "data/acme/tables/q2_kpis.pdf"
    assert dump["print_commands"][0] == "ACME Q2 2023 KPI extract"
    assert dump["print_commands"][2] == "paid_seats 11800"
    assert dump["print_commands"][3] == "12420"
    assert dump["label_command"] == "paid_seats 11800"
    assert dump["has_12420"] is True
    assert dump["row_intact"] is False
    assert dump["shear_window"] == [
        "(paid_seats 11800) Tj",
        "0 -16 Td",
        "(12420) Tj",
    ]


def test_s13_1_dump_screened_receipts():
    out = subprocess.run(
        [sys.executable, str(DUMP)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    ).stdout
    assert "pdf data/acme/tables/q2_kpis.pdf" in out
    assert "Tj paid_seats 11800" in out
    assert "Tj 12420" in out
    assert "label_command paid_seats 11800" in out
    assert "has_12420 True" in out
    assert "row_intact False" in out
    assert "(paid_seats 11800) Tj" in out
    assert "(12420) Tj" in out


def test_s13_1_restore_screened_receipts():
    out = subprocess.run(
        [sys.executable, str(RESTORE)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    ).stdout
    assert "parser markdown-fallback" in out
    assert "Docling not installed. Using labeled markdown restore of data/acme/tables/q2_kpis.md." in out
    assert "- paid_seats | 11800 | 12420" in out
    assert "- regions | 4 | 4" in out
    assert "has_12420 True" in out
