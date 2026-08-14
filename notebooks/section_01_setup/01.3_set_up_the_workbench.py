# %% [markdown]
# # S1.3 Set up the workbench
#
# Open this folder in VS Code. This file is a normal Python notebook (`# %%` cells).
# After this lecture you can run pytest and open a real vector store folder.

# %%
from pathlib import Path
import subprocess, sys
root = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
print("project root:", root)
print("python:", sys.version.split()[0])

# %% [markdown]
# The test suite is the first proof the project is installed. It uses HashEmbedder
# (offline) and Chroma in memory. No API key.

# %%
proc = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=root)
print("pytest exit", proc.returncode)
assert proc.returncode == 0

# %% [markdown]
# Layout you will live in:
# - `data/acme/` the corpus
# - `notebooks/section_XX/` these lectures
# - `rag/` the small library notebooks import (like `src/` at work)
# - `store/chroma`, `store/faiss`, `store/qdrant` the indexes you build
# - `app.py` the product HTTP door
