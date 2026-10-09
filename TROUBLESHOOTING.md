# Troubleshooting

Every error below was really produced on a Windows 11 machine on 2026-10-09, in a fresh clone of this repo. Most were
caused on purpose so we could capture them for this page: a PATH with no Git or no Python, a blocked script policy, a
venv with nothing installed, a command typed one folder too high. The model errors were caused with a small stand-in
server in place of Ollama or the provider, so nothing was sent to a real service; the stand-in answered with the error
the real service sent in an earlier test on 2026-10-04 and 2026-10-05.

Each entry gives the error as it was printed, what it means, and the fix. A fix marked **(tested)** was run and worked;
a fix marked **(not tested here)** comes from the error itself or the tool's docs and was not run on that machine.
Paths in the output show the test machine's folders; yours will show your own.

## Setting up

### `git` is not recognized

In PowerShell:

```
git : The term 'git' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the
spelling of the name, or if a path was included, verify that the path is correct and try again.
```

In Command Prompt:

```
'git' is not recognized as an internal or external command,
operable program or batch file.
```

What it means: Git is not installed, or the terminal was opened before it was installed.

Fix **(not tested here)**: install Git for Windows from https://git-scm.com, then open a new terminal and clone again.

### `git clone` says the folder already exists

```
fatal: destination path 'advanced-rag-workbench' already exists and is not an empty directory.
```

What it means: you already cloned the repo into this folder, and Git will not clone over a folder that has files in it.

Fix **(tested)**: do not clone again. Go into the folder you have and update it: `cd advanced-rag-workbench`, then
`git pull`. It answers `Already up to date.` or brings the newest files.

### `py` is not recognized

In PowerShell:

```
py : The term 'py' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the
spelling of the name, or if a path was included, verify that the path is correct and try again.
```

In Command Prompt:

```
'py' is not recognized as an internal or external command,
operable program or batch file.
```

What it means: `py` is the Python launcher, and it is not on your PATH. Python itself can still be there: on the test
machine the launcher's folder was left off PATH with the Microsoft Store Python's `python` command still on it, and
`py -3.13 -m venv .venv` failed like this.

Fix **(tested)**: use `python` instead, as INSTALL.md says: `python -m venv .venv`. To check you got 3.13,
`.venv\Scripts\python --version` printed `Python 3.13.14` on the test machine.

### `python` is not recognized

In PowerShell:

```
python : The term 'python' is not recognized as the name of a cmdlet, function, script file, or operable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
```

In Command Prompt:

```
'python' is not recognized as an internal or external command,
operable program or batch file.
```

What it means: Windows cannot find any Python on your PATH, usually because none is installed.

Fix **(not tested here)**: install Python 3.13 from python.org, open a new terminal, and start INSTALL.md again from
`py -3.13 -m venv .venv`.

### `No suitable Python runtime found`

```
No suitable Python runtime found
Pass --list (-0) to see all detected environments on your machine
or set environment variable PYLAUNCHER_ALLOW_INSTALL to use winget
or open the Microsoft Store to the requested version.
```

What it means: you asked the `py` launcher for a Python version that is not installed, for example `py -3.13` on a
machine with no 3.13. The message names no version, so it reads the same for every missing one; on the test machine it
came from `py -3.10` and from `py -3.14`.

Fix **(tested)**: run `py --list` to see the versions you have. On the test machine it printed:

```
 -V:3.13 *        Python 3.13 (Store)
 -V:3.11          Python 3.11 (64-bit)
```

If 3.11, 3.12 or 3.13 is on your list, make the venv with that one, for example `py -3.11 -m venv .venv` (see the next
entry). If none of them is, install Python 3.13 from python.org and open a new terminal.

### I have Python 3.11 or 3.12, not 3.13

There is no error, and you do not need to reinstall. The repo supports 3.11, 3.12 and 3.13 and recommends 3.13. On
2026-10-09 a fresh clone passed the whole suite on all three, with the same count each time: `150 passed, 1 skipped`
on Python 3.11.9, 3.12.13 and 3.13.14, and the first lab ended `pytest_exit 0` on each. The one skip is pgvector, which
needs Docker.

### PowerShell will not run the activate script

```
.venv\Scripts\Activate.ps1 : File D:\rag_r3\gh\advanced-rag-workbench\.venv\Scripts\Activate.ps1 cannot be loaded
because running scripts is disabled on this system. For more information, see about_Execution_Policies at
https:/go.microsoft.com/fwlink/?LinkID=135170.
At line:1 char:1
+ .venv\Scripts\Activate.ps1
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : SecurityError: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```

What it means: Windows is set to block PowerShell scripts, and activating a venv in PowerShell runs one.

Fix **(tested)**: for this one window, run `Set-ExecutionPolicy -Scope Process RemoteSigned`, then
`.venv\Scripts\Activate.ps1` again. Or use Command Prompt, where `.venv\Scripts\activate` needs no policy change. Both
put the venv's `python.exe` first on the test machine.

Fix **(not tested here)**: to stop seeing this in every new window, run this once, as INSTALL.md says:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`. The test machine already had that setting, so it was not run
there.

### `uv` is not recognized

```
uv : The term 'uv' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the
spelling of the name, or if a path was included, verify that the path is correct and try again.
```

What it means: the README's quick start uses uv, and uv is not installed.

Fix **(tested)**: you do not need uv. Follow the pip steps in INSTALL.md instead: they make the venv with Python
itself and install the same pinned versions from `requirements.txt`.

### `make` is not recognized

In PowerShell:

```
make : The term 'make' is not recognized as the name of a cmdlet, function, script file, or operable program. Check
the spelling of the name, or if a path was included, verify that the path is correct and try again.
```

In Command Prompt:

```
'make' is not recognized as an internal or external command,
operable program or batch file.
```

What it means: Windows does not come with `make`. The Makefile is a shortcut, not a step you need.

Fix **(tested)**: type the command the target runs. `make test` is `python -m pytest`, `make smoke` is
`python scripts/smoke_all.py`, and `make section-8b` is `python -m pytest tests/test_section_08b.py`.

## The venv

### `pytest` is not recognized

In PowerShell:

```
pytest : The term 'pytest' is not recognized as the name of a cmdlet, function, script file, or operable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
```

In Command Prompt:

```
'pytest' is not recognized as an internal or external command,
operable program or batch file.
```

What it means: pytest lives inside the course venv, and this terminal is not using it. Either the venv is not active
(no `(.venv)` at the start of the prompt), or it is active but nothing was installed into it. Both gave this text on
the test machine.

Fix **(tested)**: activate the venv (`.venv\Scripts\Activate.ps1`, or `.venv\Scripts\activate` in Command Prompt). If
pytest is still not recognized with `(.venv)` showing, run `pip install -r requirements.txt` now, inside the venv.

### The first lab says `No module named pytest` and `pytest_exit 1`

```
D:\rag_r3\ev\advanced-rag-workbench\.venv\Scripts\python.exe: No module named pytest
pytest_exit 1
```

The four lines above it (`python`, `root`, `pyproject`, `python-version`) print as normal. With no venv active, the
first path names your machine's Python instead of a `.venv` folder.

What it means: you ran `labs/lab_s2_env/part_1/setup_clone.py` with a Python that has no course packages: either not
the venv, or a venv nothing was installed into.

Fix **(tested)**: activate the venv, install if you have not, and run the lab again. It then prints the rows of dots,
`150 passed, 1 skipped`, and `pytest_exit 0`.

### `ModuleNotFoundError: No module named 'numpy'`, or another package

```
ModuleNotFoundError: No module named 'numpy'
```

That is the last line of a traceback that starts in the lab and ends in `rag\retrieve.py`. The package it names is the
first one your Python is missing: on the test machine a Python with nothing installed named `numpy`, and a Python that
already had numpy from other work named `rank_bm25`.

What it means: the same as the entry above. The lab ran on a Python without the course packages.

Fix **(tested)**: activate the venv and run the lab again. If you installed while the venv was not active, see the next
entry.

### I ran `pip install` and it still says `No module named ...`

There is no error at install time. The sign is where pip installs to. With no venv active, `pip --version` named the
machine's Python on the test machine:

```
pip 26.1.2 from C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0\Lib\site-packages\pip (python 3.13)
```

Inside the venv it names the venv:

```
pip 26.1.2 from D:\rag_r3\gh\advanced-rag-workbench\.venv\Lib\site-packages\pip (python 3.13)
```

And `pip list` in a venv nothing was installed into shows only pip:

```
Package Version
------- -------
pip     26.1.2
```

What it means: the install went into the machine's Python, not into the course venv, so the venv is still empty.

Fix **(tested)**: activate the venv, check that `pip --version` names your repo folder followed by
`.venv\Lib\site-packages\pip`, then run `pip install -r requirements.txt` again.

## The wrong folder

Every command in INSTALL.md after `cd advanced-rag-workbench` runs inside the repo folder. Typed one folder too high,
they fail like this:

```
.venv\Scripts\Activate.ps1 : The module '.venv' could not be loaded. For more information, run 'Import-Module .venv'.
```

```
The system cannot find the path specified.
```

(Command Prompt, `.venv\Scripts\activate`.)

```
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
```

```
copy : Cannot find path 'D:\rag_r3\gh\.env.example' because it does not exist.
```

(PowerShell; Command Prompt says `The system cannot find the file specified.`)

```
D:\rag_r3\gh\advanced-rag-workbench\.venv\Scripts\python.exe: can't open file 'D:\\rag_r3\\gh\\labs\\lab_s2_env\\part_1\\setup_clone.py': [Errno 2] No such file or directory
```

```
D:\rag_r3\gh\advanced-rag-workbench\.venv\Scripts\python.exe: can't open file 'D:\\rag_r3\\gh\\app.py': [Errno 2] No such file or directory
```

```
D:\rag_r3\gh\advanced-rag-workbench\.venv\Scripts\python.exe: No module named rag
```

(`python -m rag ask ...`.) And `pytest` from the folder above collects the repo's tests without the repo's settings:

```
!!!!!!!!!!!!!!!!!! Interrupted: 30 errors during collection !!!!!!!!!!!!!!!!!!!
```

with `E   ModuleNotFoundError: No module named 'rag'` under each test file.

What it means: the terminal is in the folder that holds `advanced-rag-workbench`, not in it. The path in the error
shows where it looked.

Fix **(tested)**: `cd advanced-rag-workbench`, then run the same command again.

## Running a lab

### The store lab ends with `Exception ignored in: <function QdrantClient.__del__ ...>`

`labs/lab_s3_naive/part_3/compare_stores.py` and its notebook twin print their result, then this:

```
qdrant   count=10
SKIP pgvector: docker not up
Exception ignored in: <function QdrantClient.__del__ at 0x000001C5FE55D260>
Traceback (most recent call last):
  ...
ModuleNotFoundError: import of typing halted; None in sys.modules
```

The `...` stands for six `File` lines inside `qdrant_client` and `portalocker`.

What it means: nothing went wrong. The lab finished and exits with 0; the count lines above are its result. As Python
shuts down, the Qdrant client tries to release its folder lock after Python has already unloaded part of itself, and
Python reports that it ignored the error. On the test machine it showed every time on Python 3.12 and 3.13, and not on
3.11.

Fix: none needed.

### `Storage folder ... is already accessed by another instance of Qdrant client`

```
RuntimeError: Storage folder D:\rag_r3\gh\advanced-rag-workbench\store\qdrant is already accessed by another instance of Qdrant client. If you require concurrent access, use Qdrant server instead.
```

What it means: another Python still has `store/qdrant` open, for example the notebook twin of the store lab in a VS
Code window, and the local Qdrant lets one Python at a time use the folder.

Fix **(tested)**: stop the other Python (for a notebook, restart or close its kernel), then run the lab again. On the
test machine it then printed all four stores.

### The first embedding run ends in `httpx.ConnectError`

`labs/lab_s3_naive/part_2/embed_and_persist.py` prints `embedder all-MiniLM-L6-v2 dim 384`, then a long traceback that
passes through Chroma's `_download_model_if_not_exists` and ends:

```
httpx.ConnectError: [WinError 10061] No connection could be made because the target machine actively refused it
```

What it means: the first time a lab uses the real embedder, Chroma downloads the all-MiniLM-L6-v2 model, and the
download could not connect. On the test machine it was caused with a proxy setting pointing at an address where nothing
answers; with no network at all, the last line names a different connection error.

Fix **(tested)**: once the model is downloaded, the lab needs no network: on the test machine, with the model already in
`.cache\chroma\onnx_models` in the user folder, the same lab ran to the end. Fix **(not tested here)**: run it once on
a network that can reach the internet, or remove a proxy setting you do not need (`HTTPS_PROXY`, `HTTP_PROXY`). pytest
never downloads anything.

## Calling a model

The model errors below were caused with the stand-in server described at the top. Where your output shows a base URL
or a model, it names your own.

### The local model cannot be reached

The ping lab, `labs/lab_s2_env/part_4/ping_generate.py`, prints its settings and then:

```
SKIPPED: no server on 11434/1234 and no LLM_API_KEY
```

It says this with `LLM_API_KEY=ollama` in `.env` too, because `ollama` is a stand-in word, not a real key. With the
LOCAL block uncommented in `.env` and `RAGBENCH_GENERATE=api`, `python -m rag ask "..."` prints a traceback of about 75
lines that ends:

```
urllib.error.URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it>
```

What it means: nothing answers at `http://localhost:11434`, so Ollama is not installed or not running.

Fix **(not tested here)**: install Ollama from https://ollama.com, start it, and pull the model: `ollama pull qwen3:8b`.
Fix **(tested with the stand-in)**: with a server answering at 11434, the ping lab printed `ping pong` and the ask
printed `"generator": "api"`.

### `SKIPPED: RAGBENCH_GENERATE=api needs a key in .env`, and you use Ollama

```
    "note": "SKIPPED: RAGBENCH_GENERATE=api needs a key in .env (RAGBENCH_API_KEY or ANTHROPIC_API_KEY). Do not commit the key."
```

This is inside the `"generator"` part of the answer from `python -m rag ask "..." --generate api`, and the answer is
copied from the retrieved text. On the test machine a model was answering at 11434 and was never called.

What it means: generate needs a key set, even for the local model, and your `.env` has none.

Fix **(tested)**: uncomment the LOCAL block in `.env`, which sets `LLM_API_KEY=ollama`, and set `RAGBENCH_GENERATE=api`
at the bottom. The ask then printed `"generator": "api"` and `"model": "qwen3:8b"`.

### The model is not pulled

The ping lab prints:

```
SKIPPED: generate call failed (model HTTP 404: {"error": {"message": "model 'qwen3:8b' not found", "type": "not_found_error", "param": null, "code": null}})
```

and `python -m rag ask "..."` puts the same `model HTTP 404` text in its `"note"` and answers from the retrieved text.

What it means: Ollama is running but does not have the model in `LLM_MODEL`. Your error names your model.

Fix **(not tested here)**: `ollama pull qwen3:8b`, or the model the error names. `ollama list` shows what you have.

### A key is set, but the answers are still copied from the text

There is no error. `python -m rag ask "..."` answers with:

```
  "generator": {
    "generator": "extractive"
  },
```

What it means: `.env.example` ships `RAGBENCH_GENERATE=extractive`, and that line wins over the key.

Fix **(tested)**: set `RAGBENCH_GENERATE=api` in `.env` (or pass `--generate api` for one question). The ask then
printed `"generator": "api"`.

## Hosted keys

### The provider says the key is wrong

OpenAI, in the ping lab:

```
SKIPPED: generate call failed (model HTTP 401: {"error": {"message": "Incorrect API key provided: sk-fake-*****************-lab. You can find your API key at https://platform.openai.com/account/api-keys.", "type": "invalid_request_error", "code": "invalid_api_key", "param": null}, "status": 401})
```

Anthropic, in the ping lab:

```
SKIPPED: generate call failed (model HTTP 401: {"type": "error", "error": {"type": "authentication_error", "message": "API key is invalid."}, "request_id": null})
```

`python -m rag ask "..."` puts the same `model HTTP 401` text in its `"note"` and answers from the retrieved text. The
JSON after `model HTTP 401:` is what the provider sent; its spacing may differ from the lines above.

What it means: the provider refused the key in `LLM_API_KEY`, so nothing was generated.

Fix **(not tested here, no real key was used)**: make a new key on the provider's site and paste it into `.env` as
`LLM_API_KEY=...` with no quotes or spaces. A key already set in your terminal wins over `.env`.

### The provider says the account has no credit

OpenAI, in the ping lab:

```
SKIPPED: generate call failed (model HTTP 429: {"error": {"message": "You have no credits remaining. Add credits to continue using the API at https://platform.openai.com/settings/organization/billing/.", "type": "insufficient_quota", "param": null, "code": "credit_balance_exhausted"}})
```

Anthropic, in the ping lab:

```
SKIPPED: generate call failed (model HTTP 400: {"type": "error", "error": {"type": "invalid_request_error", "message": "Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits."}, "request_id": "req_011CfiSBaBG2aFUAktkkiJZX"})
```

Your `request_id` will be different. OpenAI's says 429, which usually means too many requests, but its message and its
`insufficient_quota` type are about credit.

What it means: the key is real and the provider read it, but the account has no API credit to spend.

Fix **(not tested here, no credit was added)**: add credit on the provider's billing page; OpenAI's error gives the
address and Anthropic's names Plans & Billing. Fix **(tested)** to go on at no cost: empty the key line in `.env`
(`LLM_API_KEY=`). The ping lab then printed `SKIPPED: no API key configured`, and the labs answer from the retrieved
text. Retrieval never needs a key.

## Asking for help

If none of this fixes it, ask in the course Q&A on Udemy. Put three things in your question:

- the command you ran and the folder you ran it in;
- the full output, from the command to the last line, pasted as text;
- your door: Ollama and the model, or the provider and the model id from your `.env`.

Never paste your API key. Delete the key line from anything you post.
