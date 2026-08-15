# Rebuild run report

Date: 2026-08-15
Repo: student-facing course workbench (this git repo)
Curriculum: v1.0 LOCKED (17 sections, 96 lectures, 60 lab parts)

`.env` was not opened or written. No live keys appear in committed files.

## Commands

Working directory: repository root.

### `python -m pytest -q`

```
..............................................................s.         [100%]
```

Exit code: 0

The single skip is `tests/test_store.py::test_pgvector_optional` (Postgres not running). Docker is optional.

### `python scripts/smoke_all.py`

```
RAGBENCH smoke_all  (retrieval local; generate skips without a key)
suite                        status   note
------------------------------------------------------------------------
tests/test_smoke.py          PASS     ......                                  
tests/test_section_01.py     PASS     .                                       
tests/test_section_02.py     PASS     ...                                     
tests/test_section_03.py     PASS     ..                                      
tests/test_section_04.py     PASS     .                                       
tests/test_section_05.py     PASS     .                                       
tests/test_section_06.py     PASS     .                                       
tests/test_section_07.py     PASS     .                                       
tests/test_section_08.py     PASS     .                                       
tests/test_section_09.py     PASS     .                                       
tests/test_section_10.py     PASS     .                                       
tests/test_section_11.py     PASS     .                                       
tests/test_section_12.py     PASS     .                                       
tests/test_section_13.py     PASS     .                                       
tests/test_section_14.py     PASS     .                                       
tests/test_section_15.py     PASS     .                                       
tests/test_section_16.py     PASS     .                                       
tests/test_section_17.py     PASS     .                                       
------------------------------------------------------------------------
ALL                          PASS     0 failed
```

Exit code: 0

## Artifact check

Every `repo_artifact` path in `_planning/curriculum_map.json` exists (96/96, 0 missing).

## Notes

- Default generate id is `qwen3.8-max` (GA). `qwen3.8-max-preview` does not appear in `.env.example`.
- Default base URL is `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`.
- `uv.lock` was generated with `uv lock` (uv 0.11.28, CPython 3.11.9).
- One test was adjusted after the first pytest run: `test_section_07_rrf_recovers_ts999` now fuses `top_n=16` so a BM25-only TS-999 remains in the RRF set. Hybrid still recovers it via the existing rerank stack. Re-run after that change is the output above.
