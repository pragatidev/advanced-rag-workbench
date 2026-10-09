"""Build every notebook twin from its lab part. The lab part is the source of truth.

A twin is notebooks/<section folder>/part_N_<name>.py, made from labs/<lab>/part_N/<name>.py:
a markdown cell (title from the part's docstring, then the lab and part), then one code cell
holding the part with its path anchors rewritten so the twin runs from the repo root in
VS Code (Run Cell) or as a plain script from notebooks/.

    python scripts/make_twins.py          write every twin
    python scripts/make_twins.py --check  exit 1 and list any twin that differs from its part

tests/test_twins.py runs the check, so a twin can never drift from its part.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Lab folder -> notebook folder. Labs not listed here have no part twins
# (their notebook folder holds concept walks instead).
TWIN_FOLDERS = {
    "lab_s2_env": "section_02_set_up_any_provider_and_local",
    "lab_s3_naive": "section_03_run_naive_rag",
    "lab_s4_diagnose": "section_04_watch_naive_fail",
    "lab_s5_chunk": "section_05_chunk_with_a_measured_reason",
    "lab_s6_s2b": "section_06_small_to_big_and_late_chunking",
    "lab_s7_hybrid": "section_07_hybrid_search_and_rrf",
    "lab_s8_rerank": "section_08_contextual_rerank_and_pack",
    "lab_s8b_budget": "section_08b_rerank_budget_and_self_route",
    "lab_s9_query": "section_09_query_enhancement",
    "lab_s10_route": "section_10_self_rag_and_adaptive_routing",
    "lab_s11_crag": "section_11_corrective_rag_and_retrieve_as_tool",
    "lab_s12_graph": "section_12_graph_rag_and_when_to_refuse",
    "lab_s13_mm": "section_13_multimodal_tables_and_images",
    "lab_s14_eval": "section_14_evaluation_metrics",
    "lab_s15_prod": "section_15_cost_cache_and_traces",
    "lab_s16_gov": "section_16_enterprise_data_governance",
    "lab_s17_cap": "section_17_ship_one_pipeline_from_evidence",
}

# A lab part sits three folders below the root; a twin sits two. The twin prefers the
# working directory when it is the repo root, because Run Cell may not set __file__.
TWIN_ROOT = 'Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]'
PART_ROOT = "Path(__file__).resolve().parents[3]"
PART_HERE = "Path(__file__).resolve().parent"


def part_files() -> list[Path]:
    out = []
    for lab in sorted(TWIN_FOLDERS):
        for part_dir in sorted((ROOT / "labs" / lab).glob("part_*")):
            files = sorted(part_dir.glob("*.py"))
            if len(files) != 1:
                raise SystemExit(f"{part_dir.relative_to(ROOT).as_posix()}: expected one .py, found {len(files)}")
            out.append(files[0])
    return out


def twin_path(part: Path) -> Path:
    lab, part_dir = part.parts[-3], part.parts[-2]
    return ROOT / "notebooks" / TWIN_FOLDERS[lab] / f"{part_dir}_{part.name}"


def build_twin(part: Path) -> str:
    lab, part_dir = part.parts[-3], part.parts[-2]
    source = part.read_text(encoding="utf-8")
    doc = ast.get_docstring(ast.parse(source)) or part.stem.replace("_", " ")
    # The docstring's first sentence is the title; the rest of its first line rides after the lab.
    first = doc.strip().splitlines()[0].strip()
    title, _, note = first.partition(". ")
    title = title.rstrip(".")
    note = f" {note}" if note else ""
    here = f'({TWIN_ROOT}) / "labs" / "{lab}" / "{part_dir}"'
    body = re.sub(re.escape(PART_HERE) + r"(?!s)", lambda _: here, source).replace(PART_ROOT, TWIN_ROOT)
    leftover = body.replace(TWIN_ROOT, "")
    if "__file__" in leftover:
        raise SystemExit(f"{part.relative_to(ROOT).as_posix()}: a __file__ use the twin rules do not cover")
    return f"# %% [markdown]\n# # {title}\n#\n# Lab `{lab}` / `{part_dir}`.{note}\n\n# %%\n{body}"


def drifted() -> list[str]:
    bad = []
    expected = set()
    for part in part_files():
        twin = twin_path(part)
        expected.add(twin)
        if not twin.is_file() or twin.read_text(encoding="utf-8") != build_twin(part):
            bad.append(twin.relative_to(ROOT).as_posix())
    for folder in TWIN_FOLDERS.values():
        for twin in sorted((ROOT / "notebooks" / folder).glob("part_*.py")):
            if twin not in expected:
                bad.append(f"{twin.relative_to(ROOT).as_posix()} (no lab part)")
    return bad


def main(argv: list[str]) -> int:
    if "--check" in argv:
        bad = drifted()
        for rel in bad:
            print("DRIFT", rel)
        print(f"twins {len(part_files())} drifted {len(bad)}")
        return 1 if bad else 0
    written = 0
    for part in part_files():
        twin = twin_path(part)
        text = build_twin(part)
        if not twin.is_file() or twin.read_text(encoding="utf-8") != text:
            twin.write_text(text, encoding="utf-8", newline="\n")
            written += 1
            print("wrote", twin.relative_to(ROOT).as_posix())
    print(f"twins {len(part_files())} written {written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
