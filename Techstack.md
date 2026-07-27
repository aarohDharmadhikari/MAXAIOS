# MAX AI OS — Technology Stack

Each entry states why the technology was chosen, what was considered instead, and known tradeoffs. Entries marked (guessing) reflect a reasonable default choice for the target design rather than a finalized decision — revise as the project matures.

## AI

| Technology | Why chosen | Alternatives considered | Tradeoffs | Scalability |
|---|---|---|---|---|
| Anthropic API (Claude models) | Strong instruction-following and tool-use support needed for the Reasoning/Planning Engines | OpenAI API, open-weight models only | Cloud dependency, per-token cost | LLM Router abstracts provider, so switching cost is contained |
| llama.cpp / Ollama (guessing, planned) | Local inference for privacy-sensitive or offline execution | Cloud-only | Lower quality than frontier cloud models for complex planning | Deferred to Phase 4 — do not build until there's a real offline use case |

## Backend

| Technology | Why chosen | Alternatives considered | Tradeoffs | Scalability |
|---|---|---|---|---|
| Python 3.11+ | Ecosystem maturity for AI/ML tooling, fastest path to a working core given the reasoning/memory logic is I/O and orchestration heavy, not CPU-bound | Node.js/TypeScript, Go | Slower raw execution than Go for CPU-bound tasks (not the bottleneck here — model latency dominates) | Sufficient; execution-heavy plugins can be written in other languages behind the plugin process boundary |
| FastAPI | Async-first, typed request/response models reduce integration bugs at the API boundary | Flask, Django REST | Smaller ecosystem than Django for things MAX AI OS doesn't need (admin panels, ORM-heavy CRUD) | Handles the WebSocket + REST hybrid needed for streaming responses |
| asyncio (Event Bus, current) | No extra infrastructure needed for single-process Phase 0–3 scope | Redis Streams, NATS, Kafka | Doesn't survive a multi-process/multi-machine deployment as-is | Explicitly designed to be swapped in Phase 4 — see `docs/architecture.md` §10 |

## Frontend / Desktop

| Technology | Why chosen | Alternatives considered | Tradeoffs | Scalability |
|---|---|---|---|---|
| Web client: React (guessing) | Team familiarity, large ecosystem, matches the eventual Electron/desktop-wrapper path | Vue, Svelte | Larger bundle size than Svelte | Fine for a control-panel-style UI, not a performance-critical rendering app |
| Desktop shell: Electron (guessing, planned) | Reuse the web client instead of maintaining separate native UIs across Windows/Linux | Native Win32/Qt, Tauri | Higher memory footprint than Tauri | Acceptable tradeoff while the UI is not the bottleneck; revisit if resource usage becomes a complaint |

## Database

| Technology | Why chosen | Alternatives considered | Tradeoffs | Scalability |
|---|---|---|---|---|
| SQLite (current) | Zero-config persistence for local single-user deployment during early phases | PostgreSQL from day one | Doesn't support concurrent multi-process writes well | Explicitly a Phase 0–1 choice; migration to PostgreSQL is planned before multi-agent (Phase 4) concurrent access needs |
| PostgreSQL + pgvector (planned) | One database for structured episodic memory and vector semantic search, avoiding a second DB dependency | Standalone vector DB (Qdrant/Weaviate) | pgvector's ANN performance lags purpose-built vector DBs at very large scale | Sufficient for expected memory volume per user; revisit only if benchmarks show it's the bottleneck |

## DevOps / Infrastructure

| Technology | Why chosen | Alternatives considered | Tradeoffs | Scalability |
|---|---|---|---|---|
| GitHub Actions | Native CI integration, no separate infra to maintain for an open-source repo | Jenkins, CircleCI | Less powerful than self-hosted CI for heavy build matrices | Sufficient for current test/lint scope |
| Docker (planned) | Reproducible deployment target once cloud hosting (Phase 5) is in scope | Bare-metal install scripts only | Adds a layer new contributors must understand | Necessary for the Phase 5 cloud deployment goal |

## Security

| Technology | Why chosen | Alternatives considered | Tradeoffs | Scalability |
|---|---|---|---|---|
| OS keychain integration (planned) | Avoids plaintext secrets in `.env` for production use | Vault, AWS Secrets Manager | OS keychain doesn't work identically across Windows/Linux — needs an abstraction layer | Sufficient for single-machine deployment; revisit for hosted multi-tenant scenario |
| Subprocess-per-plugin sandboxing (planned) | Prevents a plugin crash/exploit from taking down or accessing the core process | In-process plugin loading (current), containers-per-plugin | Subprocess isolation is weaker than container/VM isolation but far cheaper to implement and sufficient against non-adversarial bugs | Revisit if MAX AI OS is ever used to run untrusted third-party plugins at scale |

## Testing

| Technology | Why chosen | Alternatives considered | Tradeoffs |
|---|---|---|---|
| pytest | Standard, async-test support via `pytest-asyncio` matches FastAPI's async model | unittest | None significant |
| Contract tests for plugin manifests (planned) | Manifests are a public interface once third parties write plugins; needs schema validation tests, not just unit tests | Manual review only | Requires maintaining a schema alongside the loader |

## Developer Experience

| Technology | Why chosen | Alternatives considered | Tradeoffs |
|---|---|---|---|
| `ruff` + `black` | Fast linting/formatting, low config overhead | `flake8` + `isort` separately | None significant |
| Pre-commit hooks | Catch formatting/lint issues before CI, faster feedback loop | CI-only enforcement | Requires contributor setup step, documented in `docs/development.md` |