import pytest

from rag.envload import api_base, api_model, generate_mode
from rag.generate import generate_answer
from rag.chunkers import Chunk
from rag.llm import chat


def test_default_endpoint_is_token_plan_compatible(monkeypatch):
    monkeypatch.delenv("RAGBENCH_API_BASE", raising=False)
    monkeypatch.delenv("ANTHROPIC_BASE_URL", raising=False)
    monkeypatch.delenv("RAGBENCH_MODEL", raising=False)
    monkeypatch.delenv("ANTHROPIC_MODEL", raising=False)
    assert api_base().endswith("/compatible-mode/v1")
    assert "maas.aliyuncs.com" in api_base()
    assert "qwen3.8" in api_model()


def test_generate_mode_without_key_is_extractive(monkeypatch):
    monkeypatch.delenv("RAGBENCH_GENERATE", raising=False)
    monkeypatch.delenv("RAGBENCH_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
    monkeypatch.delenv("BAILIAN_TOKEN_PLAN_API_KEY", raising=False)
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert generate_mode(None) == "extractive"


def test_generate_mode_with_key_is_api(monkeypatch):
    monkeypatch.delenv("RAGBENCH_GENERATE", raising=False)
    monkeypatch.setenv("RAGBENCH_API_KEY", "test-not-real")
    assert generate_mode(None) == "api"


def test_extractive_still_default():
    chunk = Chunk(chunk_id="c", doc_id="d", title="t", text="TS-999 means duplicate invoice.")
    answer, meta = generate_answer("What is TS-999?", [chunk], mode="extractive")
    assert "duplicate" in answer.lower()
    assert meta["generator"] == "extractive"


def test_api_without_key_raises(monkeypatch):
    monkeypatch.delenv("RAGBENCH_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
    monkeypatch.delenv("BAILIAN_TOKEN_PLAN_API_KEY", raising=False)
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    chunk = Chunk(chunk_id="c", doc_id="d", title="t", text="hello")
    with pytest.raises(RuntimeError, match="key"):
        chat("q", [chunk])
