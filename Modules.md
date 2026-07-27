# MAX AI OS — Module Reference

Status legend: 🟢 Implemented · 🟡 In Progress · ⚪ Planned. See `docs/architecture.md` for how these modules connect.

## Memory Engine ⚪

- **Purpose:** Persist context across sessions so reasoning isn't limited to a single conversation's context window.
- **Responsibilities:** Store/retrieve working, episodic, semantic, and procedural memory (tiers defined in `docs/architecture.md` §5); rank retrieval by recency/relevance.
- **Dependencies:** SQLite (current), PostgreSQL + pgvector (planned).
- **Current status:** Working and episodic tiers functional; semantic and procedural tiers not started.
- **Public interface (planned):** `memory.store(entry: MemoryEntry) -> id`, `memory.retrieve(query: str, k: int) -> list[MemoryEntry]`.

## Reasoning Engine ⚪

- **Purpose:** Convert user intent into a structured task, delegating multi-step work to the Planning Engine.
- **Responsibilities:** Intent classification, context assembly via Memory Engine, confidence scoring on ambiguous input.
- **Dependencies:** LLM Router, Memory Engine.
- **Current status:** Single-pass pipeline with basic intent tagging; no self-critique/multi-strategy reasoning yet.
- **Public interface (planned):** `reasoning.process(intent: str, context: Context) -> ReasoningResult`.

## Planning Engine ⚪

- **Purpose:** Decompose multi-step intents into a dependency-aware task graph.
- **Responsibilities:** Build DAG of steps, handle replanning on step failure, hand ordered steps to Execution Engine.
- **Dependencies:** Reasoning Engine (input), Execution Engine (output).
- **Current status:** Not implemented — design only (`docs/architecture.md` §6).
- **Public interface (planned):** `planning.decompose(task: ReasoningResult) -> TaskGraph`.

## Execution Engine ⚪

- **Purpose:** The sole component permitted to perform side effects (filesystem, shell, automation, API calls).
- **Responsibilities:** Dispatch planned steps to registered capabilities, enforce permission checks, log every action.
- **Dependencies:** Plugin Manager (for third-party capabilities), OS Automation Adapters.
- **Current status:** Direct dispatch for a small built-in capability set (file ops, allowlisted shell commands); no sandboxing yet.
- **Public interface (planned):** `execution.run(step: TaskStep) -> StepResult`.

## Voice Engine ⚪

- **Purpose:** Speech-to-text/text-to-speech interface layer so voice becomes another client on top of the same API layer, not a separate codepath.
- **Responsibilities:** Audio capture, transcription, response synthesis.
- **Dependencies:** API Layer (consumes it like any other client).
- **Current status:** Not started. No technology selection made yet — deliberately deferred rather than guessed at here.

## Vision Engine ⚪

- **Purpose:** Image/screen understanding for tasks like "read what's on my screen" or document/image analysis.
- **Responsibilities:** Image ingestion, model-backed description/extraction, hand-off to Reasoning Engine as structured input.
- **Dependencies:** LLM Router (multimodal model calls).
- **Current status:** Not started.

## Automation Engine ⚪

- **Purpose:** OS-level UI/file automation distinct from the general Execution Engine — encapsulates platform-specific automation logic behind a common interface.
- **Responsibilities:** Windows UI Automation adapter, future Linux AT-SPI/xdotool adapter, exposing one capability interface regardless of underlying platform.
- **Dependencies:** Execution Engine (registers as a capability provider).
- **Current status:** Not started — targeted for Roadmap Phase 3.

## Plugin Manager ⚪

- **Purpose:** Load, sandbox, and mediate communication for third-party plugins.
- **Responsibilities:** Manifest validation, capability permission enforcement, process isolation, lifecycle management (start/stop/crash recovery).
- **Dependencies:** Event Bus (sole communication path with plugins).
- **Current status:** Manifest format not yet designed. In-process trusted-plugin loading only exists conceptually in architecture docs, not in code.

## Device Manager ⚪

- **Purpose:** Track connected devices/endpoints (future: smart home, mobile companion devices) as first-class entities the Planning Engine can target.
- **Responsibilities:** Device registration, capability discovery per device, status tracking.
- **Dependencies:** Plugin Manager (most device integrations will be plugins).
- **Current status:** Not started; no concrete device integration exists yet to validate this design against.

## LLM Router ⚪

- **Purpose:** Single integration point for all model calls; abstracts provider differences from the rest of the system.
- **Responsibilities:** Provider routing, response normalization, retry/fallback handling.
- **Dependencies:** None internal — this is a leaf dependency other engines call into.
- **Current status:** Implemented for Anthropic API; local model routing (llama.cpp/Ollama) planned for Phase 4.
- **Public interface:** `llm_router.complete(request: LLMRequest) -> LLMResponse`.

## Knowledge Base ⚪

- **Purpose:** Structured/curated knowledge distinct from episodic memory — facts the user has explicitly taught the system, versioned and editable, rather than inferred from conversation history.
- **Responsibilities:** CRUD for structured facts, retrieval integration with Reasoning Engine.
- **Dependencies:** Memory Engine (semantic tier, once built).
- **Current status:** Not started; depends on semantic memory tier existing first.

## Task Scheduler ⚪

- **Purpose:** Time/event-triggered task execution ("remind me," "run this every morning") distinct from on-demand user requests.
- **Responsibilities:** Cron-like scheduling, event-triggered task queuing into the Planning Engine.
- **Dependencies:** Planning Engine, Event Bus.
- **Current status:** Not started.

## Notification System ⚪

- **Purpose:** Deliver system/task outcomes back to the user outside of an active session (desktop notification, email, push).
- **Responsibilities:** Channel abstraction (desktop/email/push), delivery retry, user notification preferences.
- **Dependencies:** Execution Engine (notifications are a capability like any other side effect).
- **Current status:** Not started.

## Security Manager ⚪

- **Purpose:** Central enforcement point for plugin permissions, secrets access, and execution audit logging — referenced throughout `docs/architecture.md` §14 but not yet a distinct module (currently, what little exists is scattered across the Execution Engine).
- **Responsibilities:** Permission manifest validation, secrets retrieval abstraction (keychain/vault), audit log querying.
- **Dependencies:** Plugin Manager, Execution Engine.
- **Current status:** Not started as a distinct module; this is flagged as technical debt to address no later than Roadmap Phase 3.