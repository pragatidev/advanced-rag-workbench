.PHONY: test dest section-1 section-2 section-3 section-4 section-5 section-6 section-7 section-8 section-9 section-10 section-11 section-12 section-13 section-14 section-15 section-16 section-17 smoke

PY ?= python

test:
	$(PY) -m pytest -q

dest:
	$(PY) -c "from rag.eval.runner import run_eval; import json; s=run_eval('naive','hybrid'); print(json.dumps(s['mean'], indent=2))"

smoke:
	$(PY) scripts/smoke_all.py

section-1:
	$(PY) -m pytest -q tests/test_section_01.py

section-2:
	$(PY) -m pytest -q tests/test_section_02.py

section-3:
	$(PY) -m pytest -q tests/test_section_03.py

section-4:
	$(PY) -m pytest -q tests/test_section_04.py

section-5:
	$(PY) -m pytest -q tests/test_section_05.py

section-6:
	$(PY) -m pytest -q tests/test_section_06.py

section-7:
	$(PY) -m pytest -q tests/test_section_07.py

section-8:
	$(PY) -m pytest -q tests/test_section_08.py

section-9:
	$(PY) -m pytest -q tests/test_section_09.py

section-10:
	$(PY) -m pytest -q tests/test_section_10.py

section-11:
	$(PY) -m pytest -q tests/test_section_11.py

section-12:
	$(PY) -m pytest -q tests/test_section_12.py

section-13:
	$(PY) -m pytest -q tests/test_section_13.py

section-14:
	$(PY) -m pytest -q tests/test_section_14.py

section-15:
	$(PY) -m pytest -q tests/test_section_15.py

section-16:
	$(PY) -m pytest -q tests/test_section_16.py

section-17:
	$(PY) -m pytest -q tests/test_section_17.py
