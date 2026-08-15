# %% [markdown]
# # S7.3 Web search is a policy, not a default
#
# CRAG's paper can fall back to the public web. That is a policy decision.
# Default in this repo is OFF. Turning it on sends private questions outside.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.loops import crag

print("WEB_SEARCH_ENABLED", crag.WEB_SEARCH_ENABLED)
print("maybe_web", crag.maybe_web("What is ACME revenue?"))
print("Leave the flag false unless a written policy allows the public web.")
