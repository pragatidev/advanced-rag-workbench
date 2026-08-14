# %% [markdown]
# # S12.2 Run the final comparison
#
# Naive vs hybrid on the same question file. Keep the winner. Write a one-page
# decision note from `runs/naive_vs_hybrid/metrics.json`. That is the course.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.eval.runner import run_eval

summary = run_eval(a="naive", b="hybrid")
print(summary["mean"])
print("Open runs/naive_vs_hybrid/metrics.json and defend the stack you keep.")
