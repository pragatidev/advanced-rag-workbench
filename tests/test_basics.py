import importlib.util
from pathlib import Path

import rag.llm
from rag.llm import _source_blob
from rag.settings import _KEY_ENV_NAMES

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "embed_two_sentences",
    "similarity_scores",
    "cut_one_document",
    "store_and_ask",
    "mini_rag",
    "grounded_ask",
]
# Every variable that can move generate off the local default door, or pick the embedder.
_DOOR_ENV_NAMES = (
    "RAGBENCH_API_BASE", "RAGBENCH_BASE_URL", "LLM_BASE_URL", "ANTHROPIC_BASE_URL",
    "RAGBENCH_PROVIDER", "LLM_PROVIDER", "RAGBENCH_API_BACKEND", "LLM_BACKEND",
    "RAGBENCH_MODEL", "LLM_MODEL", "ANTHROPIC_MODEL", "RAGBENCH_EMBED_MODEL",
)


def _load(name: str):
    path = ROOT / "basics" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"basics_{name}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_each_basics_script_importable():
    for name in SCRIPTS:
        module = _load(name)
        assert module.__doc__


def test_mini_rag_returns_nonempty_answer_keyless():
    module = _load("mini_rag")
    assert str(module.answer).strip()


def _grounded_ask_offline(monkeypatch, server_up: bool):
    """grounded_ask with no .env, no key, the default local door and the offline hash embedder."""
    module = _load("grounded_ask")
    monkeypatch.setattr(module, "load_dotenv", lambda path=None: None)
    for name in _KEY_ENV_NAMES + _DOOR_ENV_NAMES:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("EMBED_MODEL", "hash")
    monkeypatch.setattr(module, "_port_open", lambda host, port, timeout=0.3: server_up)
    return module


def test_grounded_ask_offline_prints_step_one_and_skips_step_two(monkeypatch, capsys):
    module = _grounded_ask_offline(monkeypatch, server_up=False)
    calls = []

    def no_network(*args, **kwargs):
        calls.append(args)
        raise AssertionError("grounded_ask made a network call")

    monkeypatch.setattr(rag.llm, "_post", no_network)
    monkeypatch.setattr(rag.llm.urllib.request, "urlopen", no_network)
    assert module.main() == 0
    out = capsys.readouterr().out
    _, hits = module.retrieved(module.QUESTION)
    assert len(hits) == 3
    for i, h in enumerate(hits, 1):
        assert f"\n    {i}. {h.chunk.chunk_id}  score {h.score:.3f}\n" in out
    assert "\n    SKIPPED: no model server at http://localhost:11434/v1 " in out
    assert "user message" not in out and "ANSWER (" not in out
    assert calls == []


def test_grounded_ask_prints_the_user_message_exactly_as_sent(monkeypatch, capsys):
    module = _grounded_ask_offline(monkeypatch, server_up=True)
    sent = []

    def fake_post(url, headers, body, timeout):
        sent.append(body)
        return {"model": body["model"], "choices": [{"message": {"content": "It is a duplicate [1]."}}]}

    monkeypatch.setattr(rag.llm, "_post", fake_post)
    assert module.main() == 0
    out = capsys.readouterr().out
    assert len(sent) == 1
    user = sent[0]["messages"][1]["content"]
    _, hits = module.retrieved(module.QUESTION)
    assert user == _source_blob(module.QUESTION, [h.chunk for h in hits])
    for i, h in enumerate(hits, 1):
        assert f"       | [{i}] {h.chunk.chunk_id}\n" in out
    printed = "\n".join(f"       | {line}" for line in user.splitlines())
    assert printed in out
    assert "\n    ANSWER (qwen3:8b):\n    It is a duplicate [1].\n" in out
