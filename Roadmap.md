# MAX AI OS — Roadmap

This roadmap spans approximately two years, broken into six phases. Timeframes are planning targets, not commitments — each phase's completion criteria gate progression to the next, so a delayed phase pushes the schedule rather than skipping quality bars.

## Progress Overview

| Phase | Focus | Target Window | Status |
|---|---|---|---|
| 0 | Foundation & Core Loop | Months 0–2 | 🟡 In Progress |
| 1 | Memory + Reasoning MVP | Months 2–5 | ⚪ Planned |
| 2 | Planning + Execution + Plugin v1 | Months 5–9 | ⚪ Planned |
| 3 | Desktop Automation + Security Hardening | Months 9–13 | ⚪ Planned |
| 4 | Multi-Agent Orchestration + Local Models | Months 13–18 | ⚪ Planned |
| 5 | Cloud Deployment + Cross-Platform (Web/Android) | Months 18–24 | ⚪ Planned |

## Phase 0 — Foundation & Core Loop (Months 0–2)

**Objectives:** Establish the API layer, a minimal Reasoning Engine (single-pass, no planning), and basic LLM Router with one provider.

**Deliverables:** FastAPI service, CLI client, working single-turn request/response through the LLM Router, project scaffolding (CI, linting, test harness).

**Architecture changes:** None yet — this phase establishes the skeleton described in `docs/architecture.md`.

**Technical challenges:** Getting the API/engine boundary right early so later phases don't require a rewrite; over-engineering here (e.g., building plugin sandboxing before there's a single plugin) is a real risk to avoid.

**Completion criteria:** A user can send a natural-language request via CLI and receive a model-backed response through the full API → Reasoning → LLM Router path, with tests covering that path.

## Phase 1 — Memory + Reasoning MVP (Months 2–5)

**Objectives:** Working memory (session-scoped) and episodic memory (SQLite-backed) operational; Reasoning Engine assembles context from memory before calling the model.

**Deliverables:** Memory read/write API, context assembly logic, basic intent classification (query vs. command).

**Architecture changes:** Introduces the Memory Engine's working/episodic tiers (see `docs/architecture.md` §5). Semantic/procedural tiers remain out of scope.

**Technical challenges:** Deciding retrieval ranking (recency vs. relevance) without over-building — a naive "last N messages" approach may be sufficient for MVP and should be validated before adding vector search.

**Completion criteria:** A multi-session conversation demonstrably uses prior-session context; benchmark showing retrieval latency doesn't materially slow response time.

## Phase 2 — Planning + Execution + Plugin v1 (Months 5–9)

**Objectives:** Task decomposition for multi-step requests; Execution Engine with a small built-in capability set (file ops, shell allowlist); first plugin manifest format (no sandboxing yet).

**Deliverables:** Task graph representation, Execution Engine dispatch, plugin manifest schema + loader (in-process, trusted-only).

**Architecture changes:** Planning Engine and Execution Engine move from ⚪ to 🟡/🟢. Plugin architecture introduced without process isolation — an explicitly accepted interim security tradeoff, documented in `SECURITY.md`.

**Technical challenges:** Failure handling in task graphs (partial completion, retry vs. replan) is the highest-risk design problem in this phase.

**Completion criteria:** A three-plus-step task (e.g., "find X, summarize it, save to file") executes end-to-end with visible per-step status and failure recovery.

## Phase 3 — Desktop Automation + Security Hardening (Months 9–13)

**Objectives:** Windows automation adapter (UI Automation/pywinauto-based); plugin process isolation; secrets moved out of `.env` into OS keychain integration.

**Deliverables:** Desktop automation capability class, sandboxed plugin execution (subprocess-per-plugin), audit logging for all Execution Engine actions.

**Architecture changes:** Security Model table in `docs/architecture.md` moves from mostly-planned to mostly-implemented.

**Technical challenges:** Cross-version Windows UI Automation reliability; IPC design for sandboxed plugins without excessive latency.

**Completion criteria:** A desktop automation task runs through a sandboxed plugin with a full audit trail; a deliberately malicious test plugin cannot access resources outside its declared manifest.

## Phase 4 — Multi-Agent Orchestration + Local Models (Months 13–18)

**Objectives:** Support multiple concurrent reasoning agents coordinating through the Event Bus; local model support (llama.cpp/Ollama) via LLM Router for privacy-sensitive or offline tasks.

**Deliverables:** Multi-agent task delegation, local model routing rules (latency/privacy/cost-based).

**Architecture changes:** Event Bus likely needs to move from in-process asyncio to a real broker (Redis Streams/NATS) if agent count and cross-process communication grow.

**Technical challenges:** Coordinating agents without race conditions on shared memory/state; local model quality tradeoffs vs. cloud models for complex planning tasks.

**Completion criteria:** Two agents complete a coordinated task (e.g., one gathers data, one drafts output) without manual orchestration by the user.

## Phase 5 — Cloud Deployment + Cross-Platform (Months 18–24)

**Objectives:** Optional hosted deployment of the core runtime; web client parity with desktop; initial Android client.

**Deliverables:** Containerized deployment (Docker), web client, Android client consuming the same API layer.

**Architecture changes:** Cloud Architecture section of `docs/architecture.md` moves from ⚪ to 🟡/🟢.

**Technical challenges:** Multi-tenant memory isolation if hosted; mobile automation capabilities are fundamentally different from desktop (no equivalent of UI Automation) and may require a separate capability class rather than reuse.

**Completion criteria:** A user can access the same memory/session from web and desktop clients against a hosted instance.

## Missing Documentation (Recommended)

- A **risk register** tracking the technical risks named in each phase (task-graph failure handling, plugin sandbox escape, cross-platform automation) with mitigation owners as the team grows beyond one person.