# %% [markdown]
# # S10.2 Run the suite
#
# One question file. Two pipelines. Faithfulness is not context recall.
# The metrics file is what you keep or kill a technique with.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.eval.runner import run_eval

summary = run_eval(a="naive", b="hybrid")
print("n", summary["n"])
print("mean", summary["mean"])
print("wrote runs/naive_vs_hybrid/metrics.json")
