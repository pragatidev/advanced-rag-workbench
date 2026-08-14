# %% [markdown]
# # S10.3 Cost per query
#
# Local HashEmbedder + extractive generate is $0.00. The column still exists so
# you see generate_calls. HyDE adds a generate. A live API fills USD from usage.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.eval.cost import estimate

for name, extra in ("naive", 0), ("hybrid", 0), ("hyde", 1):
    print(name, estimate(name, extra_generates=extra))
