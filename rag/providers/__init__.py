"""Provider facts the labs print. The hosted doors (Anthropic, OpenAI-compatible) live in hosted.py; local needs no module."""
from rag.providers.hosted import ANTHROPIC, ENV_NAMES, OPENAI, door_for, doors  # noqa: F401
