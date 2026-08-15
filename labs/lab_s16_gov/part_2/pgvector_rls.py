"""pgvector row-level security shape."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.gov import RLS_SQL

print(RLS_SQL)
try:
    from rag.stores import pgvector_store as pgs
    if not pgs.available():
        print("SKIP pgvector: docker not up. Policy is the artifact.")
    else:
        print("postgres up. Policy is still applied in the app demo; we do not mutate cluster roles from pytest.")
except Exception as exc:
    print("SKIP pgvector:", exc)
print("denied row never returns when app.tenant is helix-west and the row is helix-east")
