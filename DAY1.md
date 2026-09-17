# Day 1: runtime foundation

The implemented surface is an installable `max` Python package and a FastAPI
application factory, `max.api.app:create_app`. `GET /health` returns HTTP 200 with
`{"status":"ok"}`. This means the HTTP application responds; it does not indicate
that future MAX systems are ready. No credentials or external services are needed.

The `core`, `reasoning`, `llm`, and `cli` packages contain package markers only.
The LLM Router, Reasoning, Memory, Planning and Execution Engines, Agent Runtime,
Plugin Manager, Event Bus, Voice, Vision, and Automation remain unimplemented.
Existing architecture documents describe future designs and contain some
implementation claims that are not backed by code. No roadmap phase is completed
by this foundation.

## Install and run

Use Python 3.11 or newer. From the repository root on PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m uvicorn max.api.app:create_app --factory --host 127.0.0.1 --port 8000
```

In another terminal, `Invoke-RestMethod http://127.0.0.1:8000/health` checks
liveness. Stop the server with Ctrl+C. On POSIX systems, use `python3` to create
the environment and `.venv/bin/python` for the remaining commands.

## Validation

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m black --check .
.\.venv\Scripts\python.exe -m pip check
```

Tests exercise installed package imports, independent application creation,
startup/shutdown through FastAPI's test client, the health response, and HTTP
rejection of unsupported routes and methods.

## Dependencies and choices

- Setuptools builds the standard `src` layout; distribution name `max-ai-os`
  and initial version `0.1.0` identify this foundation only.
- FastAPI supplies the requested API framework. Uvicorn is the ASGI server
  needed to run it over HTTP; optional server extras are not installed.
- pytest tests behavior. HTTPX is required by FastAPI's `TestClient`, which
  exercises ASGI requests in process. These tests do not need pytest-asyncio.
- Ruff checks lint, import ordering, and annotations; Black formats code.
  Both use 88 columns and Python 3.11 syntax, following `Development.md` and
  the Day 1 request. Direct dependencies are pinned; transitive dependencies
  are resolved by pip, so this is not a fully locked environment.

Application serving is transport initialization, not a capability execution
path. No agent actions or execution boundary are implemented. The factory is
the entry point; a MAX command-line client remains future work.
