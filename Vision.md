# MAX AI OS — Vision

## The Problem

Current AI assistants are conversational interfaces bolted onto stateless API calls. Ask a question, get an answer, close the tab, and the system knows nothing about you tomorrow. Meanwhile "automation" tools (Zapier, IFTTT, OS-level scripting) are powerful but require the user to explicitly wire every trigger and action by hand — there is no layer that understands intent and decides *how* to accomplish it.

The gap between "a chatbot that talks" and "a system that acts on your behalf reliably" is unfilled by any single mainstream product. Closing that gap requires the properties of an operating system — persistent state, resource arbitration, a permission model, multi-process isolation — applied to AI-driven execution, not just a bigger prompt.

## What MAX AI OS Is

MAX AI OS is a long-running software layer that:

1. **Remembers** — maintains context across sessions instead of resetting on every conversation.
2. **Reasons and plans** — decomposes multi-step intents into ordered, verifiable actions rather than one-shot text generation.
3. **Executes safely** — performs real actions (files, automation, APIs) through an auditable, permissioned execution layer instead of blindly running whatever a model outputs.
4. **Extends** — supports third-party plugins with explicit capability scoping, the way browser extensions or OS drivers do, so the ecosystem can grow without every integration living in the core codebase.
5. **Runs anywhere** — designed from the start to target desktop (Windows/Linux), web, and eventually mobile/embedded, with one consistent core and thin platform-specific adapters.

## What MAX AI OS Is Not

- Not a wrapper prompt around a single LLM API call.
- Not a hardcoded set of "skills" — capabilities are pluggable and permissioned.
- Not a replacement for the underlying OS. MAX AI OS is a layer that automates and reasons *on top of* Windows/Linux, not a kernel replacement.

## Engineering Principles

| Principle | What it means in practice |
|---|---|
| Separation of reasoning from execution | The Reasoning Engine never directly executes side effects; only the Execution Engine does, through one auditable path. |
| Explicit over implicit permissions | Plugins declare what they need; nothing gets filesystem/network access by default. |
| Provider independence | No hard dependency on a single model vendor — the LLM Router abstracts this so the system survives provider changes/outages/pricing shifts. |
| Fail loud, not silent | A failed or ambiguous step surfaces to the user rather than the system guessing and proceeding. |
| Current vs. planned is always labeled | Documentation and code both distinguish what exists from what's designed, so contributors and evaluators never mistake intent for implementation. |

## Long-Term Impact

If this succeeds, the measurable outcome isn't "a chatbot with more features" — it's a reusable, inspectable substrate that other developers can build agents and automations on top of, the way Home Assistant became the substrate for home automation rather than a single smart-speaker app. Success looks like third-party plugins existing that the core team didn't write, and a security/permission model that made that possible without turning into an attack surface.

## Honest Constraints

This is a solo/early-stage project, not a funded team. The vision above is the target architecture; it will be built incrementally, and the roadmap (`docs/roadmap.md`) reflects a realistic build order rather than parallel-tracking everything at once. Where a decision was made for pragmatism (single-machine deployment first, cloud later) that is stated explicitly rather than presented as if it were always the multi-year plan.
