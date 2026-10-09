.PHONY: test dest smoke section-1 section-2 section-3 section-4 section-5 section-6 section-7 section-8 section-8b section-9 section-10 section-11 section-11b section-12 section-13 section-14 section-15 section-15b section-16 section-17 section-18

PY ?= python

# pytest.ini already adds -q, so no -q here: each run ends with its count line.
test:
	$(PY) -m pytest

dest:
	$(PY) -c "from rag.eval.runner import run_eval; import json; s=run_eval('naive','hybrid'); print(json.dumps(s['mean'], indent=2))"

# Every test file, one at a time, as a PASS/FAIL table.
smoke:
	$(PY) scripts/smoke_all.py

# section-N runs tests/test_section_N.py. N is the number in the test file's name,
# which is older than the course map in README.md (like the notebook folder names).

section-1:
	$(PY) -m pytest tests/test_section_01.py

section-2:
	$(PY) -m pytest tests/test_section_02.py

section-3:
	$(PY) -m pytest tests/test_section_03.py

section-4:
	$(PY) -m pytest tests/test_section_04.py

section-5:
	$(PY) -m pytest tests/test_section_05.py

section-6:
	$(PY) -m pytest tests/test_section_06.py

section-7:
	$(PY) -m pytest tests/test_section_07.py

section-8:
	$(PY) -m pytest tests/test_section_08.py

section-8b:
	$(PY) -m pytest tests/test_section_08b.py

section-9:
	$(PY) -m pytest tests/test_section_09.py

section-10:
	$(PY) -m pytest tests/test_section_10.py

section-11:
	$(PY) -m pytest tests/test_section_11.py

section-11b:
	$(PY) -m pytest tests/test_section_11b.py

section-12:
	$(PY) -m pytest tests/test_section_12.py

section-13:
	$(PY) -m pytest tests/test_section_13.py

section-14:
	$(PY) -m pytest tests/test_section_14.py

section-15:
	$(PY) -m pytest tests/test_section_15.py

section-15b:
	$(PY) -m pytest tests/test_section_15b.py

section-16:
	$(PY) -m pytest tests/test_section_16.py

section-17:
	$(PY) -m pytest tests/test_section_17.py

section-18:
	$(PY) -m pytest tests/test_section_18.py
