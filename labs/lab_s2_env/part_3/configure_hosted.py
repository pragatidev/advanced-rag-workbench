"""Point generate at Anthropic or an OpenAI-compatible provider (lab S2, part 3).

Reads the four variables from .env through rag.settings, prints the two hosted doors as cards,
then prints what your .env actually resolved to. The key is never printed, only whether one is set.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.providers.hosted import ENV_NAMES, door_for, doors  # noqa: E402
from rag.settings import Settings, load_env  # noqa: E402

load_env()

print("THE TWO HOSTED DOORS (same code, four variables)")
for d in doors():
    print(f"  {d['door']:<10} LLM_BACKEND={d['backend']:<10} LLM_BASE_URL={d['base_url']}")
    print(f"  {'':<10} LLM_MODEL={d['default_model']}   alternatives: {', '.join(d['models'])}")
    print(f"  {'':<10} {d['note']}")

print()
print("WHAT YOUR .env RESOLVED TO")
print("  backend    ", Settings.api_backend)
print("  base_url   ", Settings.llm_base_url)
print("  model      ", Settings.llm_model)
print("  provider   ", Settings.llm_provider)
print("  door       ", door_for(Settings.llm_base_url, Settings.api_backend))
print("  key_present", Settings.has_api_key)
print("  variables  ", ", ".join(ENV_NAMES))

if not Settings.has_api_key:
    print("SKIPPED: no LLM_API_KEY; a hosted door needs one. Local Ollama does not. Ready for part_4 ping either way.")
else:
    print("key present (not printed). Ready for part_4 ping.")
