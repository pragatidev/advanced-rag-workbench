from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "labs/lab_s2_env/part_1/setup_clone.py",
    "labs/lab_s2_env/part_2/configure_env.py",
    "labs/lab_s2_env/part_3/configure_qwen.py",
    "labs/lab_s2_env/part_4/ping_generate.py",
    "labs/lab_s3_naive/part_1/load_and_chunk.py",
    "labs/lab_s3_naive/part_2/embed_and_persist.py",
    "labs/lab_s3_naive/part_3/compare_stores.py",
    "labs/lab_s3_naive/part_4/run_naive_ask.py",
    "labs/lab_s4_diagnose/part_4/run_diagnosis.py",
    "labs/lab_s5_chunk/part_2/cosine_breakpoint.py",
    "labs/lab_s6_s2b/part_2/sentence_window.py",
    "labs/lab_s7_hybrid/part_4/run_hybrid.py",
    "labs/lab_s8_rerank/part_2/cross_encoder.py",
    "labs/lab_s9_query/part_3/hyde.py",
    "labs/lab_s10_route/part_3/router.py",
    "labs/lab_s11_crag/part_4/run_loop.py",
    "labs/lab_s12_graph/part_4/run_graph.py",
    "labs/lab_s13_mm/part_2/docling_parse.py",
    "labs/lab_s14_eval/part_3/run_suite.py",
    "labs/lab_s15_prod/part_2/semantic_cache.py",
    "labs/lab_s16_gov/part_2/pgvector_rls.py",
    "labs/lab_s17_cap/part_2/decision_note.py",
    "docs/mechanisms/retrieve_then_generate.md",
    ".env.example",
]


def test_every_curriculum_lab_exists():
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    assert missing == []


def test_checkpoint_folders_have_starter_and_solution():
    labs = sorted(p for p in (ROOT / "labs").iterdir() if p.is_dir() and p.name.startswith("lab_"))
    assert len(labs) == 16
    for lab in labs:
        assert (lab / "starter").is_dir(), lab
        assert (lab / "solution").is_dir(), lab
        assert (lab / "part_1").is_dir(), lab


def test_env_example_has_verified_qwen_id():
    text = (ROOT / ".env.example").read_text(encoding="utf-8")
    assert "qwen3.8-max" in text
    assert "qwen3.8-max-preview" not in text
    assert "dashscope-intl.aliyuncs.com/compatible-mode/v1" in text
