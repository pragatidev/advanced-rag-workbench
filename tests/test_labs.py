from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "labs/lab_s2_env/part_1/setup_clone.py",
    "labs/lab_s2_env/part_2/configure_env.py",
    "labs/lab_s2_env/part_3/configure_hosted.py",
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
    "labs/lab_s8b_budget/part_1/budget_board.py",
    "labs/lab_s9_query/part_3/hyde.py",
    "labs/lab_s10_route/part_3/router.py",
    "labs/lab_s11_crag/part_4/run_loop.py",
    "labs/lab_s11b_hop/part_1/naive_hop.py",
    "labs/lab_s12_graph/part_4/run_graph.py",
    "labs/lab_s13_mm/part_2/docling_parse.py",
    "labs/lab_s14_eval/part_3/run_suite.py",
    "labs/lab_s15_prod/part_2/semantic_cache.py",
    "labs/lab_s16_gov/part_2/pgvector_rls.py",
    "labs/lab_s17_walk/part_1/whiteboard_stack.py",
    "labs/lab_s17_cap/part_2/decision_note.py",
    "docs/mechanisms/retrieve_then_generate.md",
    ".env.example",
]


def test_every_curriculum_lab_exists():
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    assert missing == []


def test_checkpoint_folders_have_starter_and_solution():
    labs = sorted(p for p in (ROOT / "labs").iterdir() if p.is_dir() and p.name.startswith("lab_"))
    assert len(labs) == 20
    for lab in labs:
        assert (lab / "part_1").is_dir(), lab
        if lab.name == "lab_s15b_fresh":
            continue
        assert (lab / "starter").is_dir(), lab
        assert (lab / "solution").is_dir(), lab


def test_env_example_has_the_three_doors():
    text = (ROOT / ".env.example").read_text(encoding="utf-8")
    assert "https://api.anthropic.com" in text and "LLM_MODEL=claude-haiku-5-5" in text
    assert "https://api.openai.com/v1" in text and "LLM_MODEL=gpt-6-luna" in text
    assert "http://localhost:11434/v1" in text and "LLM_MODEL=qwen3:8b" in text
    assert "EMBED_MODEL=all-MiniLM-L6-v2" in text
