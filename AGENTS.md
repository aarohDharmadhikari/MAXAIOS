# Working on MAX AI OS

- Inspect the current tree, Git status, and relevant documentation before editing.
  Documentation describes target designs too; claim implementation only when
  working code and verification support it.
- Follow `Development.md` and existing conventions: Python 3.11+, public function
  and method type hints, Ruff, Black, and no bare `except` blocks.
- Preserve API, core, reasoning, model, and client boundaries. Clients use the API;
  core must not depend on agents, and capabilities must not depend on models.
- LLMs and agents must never directly perform side effects. Future actions must
  pass through the controlled capability/Execution Engine boundary for
  authorization, execution, and auditing. Do not bypass it while it is absent.
- Implement only the requested scope. Do not invent missing requirements, create
  fake engines, or silently change architectural decisions. Surface conflicts.
- Keep dependencies minimal, pin direct dependencies in `pyproject.toml`, and
  explain each addition. Do not add infrastructure for future features.
- Run package installation, pytest, Ruff, Black checks, and the relevant entry
  point before declaring completion. Report actual outcomes and limitations.
- Modify only related files; preserve user changes. Keep current and planned
  functionality distinct in documentation and reports.
- Work on feature branches, never push directly to the default branch, and use
  Conventional Commits. The current default branch is `master`, although the
  handbook refers to `main`.
