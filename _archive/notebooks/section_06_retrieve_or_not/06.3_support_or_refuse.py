# %% [markdown]
# # S6.3 Support or refuse
#
# After generate, check the answer against retrieved text. If it is not supported,
# refuse. A confident lie from the wrong chunks is still a failure.

# %%
import sys
from pathlib import Path
ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path.cwd().parent.parent
sys.path.insert(0, str(ROOT))
from rag.loops.retrieve_gate import support_or_refuse

ctx = ["TS-999 means the billing ledger rejected a duplicate invoice id."]
print(support_or_refuse("TS-999 is a duplicate invoice rejection.", ctx))
print(support_or_refuse("The CEO said revenue doubled overnight.", ctx))
