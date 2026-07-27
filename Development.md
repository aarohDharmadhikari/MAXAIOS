# MAX AI OS — Developer Handbook

This is the onboarding reference for anyone contributing code. If something here conflicts with `CONTRIBUTING.md`, this document governs day-to-day workflow; `CONTRIBUTING.md` governs how to submit changes as an external contributor.

## Repository Workflow

- `main` is always deployable/importable — no broken builds committed directly to it.
- All work happens on feature branches off `main`, merged via pull request. No direct pushes to `main`.
- Each PR should map to one logical change (one engine feature, one bug fix, one doc update) — not a batch of unrelated changes.

## Branching Strategy

| Branch pattern | Purpose |
|---|---|
| `main` | Stable, always buildable |
| `feature/<short-description>` | New functionality |
| `fix/<short-description>` | Bug fixes |
| `docs/<short-description>` | Documentation-only changes |
| `refactor/<short-description>` | Non-functional restructuring |

## Commit Conventions

Follows [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short summary>

<optional body explaining why, not just what>
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`. Example:

```
feat(memory-engine): add episodic memory retrieval by recency

Adds a recency-weighted query path to the episodic store so the
Reasoning Engine can pull relevant recent context without a full
table scan. Vector-based semantic retrieval remains out of scope
until Phase 1 completes.
```

## Coding Standards

- Python 3.11+, type-hinted on all public functions/methods.
- Formatting via `black`, linting via `ruff` — both run in pre-commit and CI; a PR with lint failures will not be reviewed until fixed.
- No bare `except:` blocks — catch specific exceptions, especially around LLM Router calls and Execution Engine side effects, where silent failure is a correctness/security issue, not just style.
- Every module that performs a side effect (filesystem, network, shell) must go through the Execution Engine's dispatch path — no ad hoc `subprocess.run` calls scattered in other modules.

## Documentation Standards

- Every new subsystem needs an entry in `docs/modules.md` before merge (purpose, responsibilities, current status).
- Docs use the 🟢/🟡/⚪ status markers established in `docs/architecture.md` — keep them accurate; a stale "implemented" marker is worse than an honest "planned" one.

## Testing Strategy

| Layer | Requirement |
|---|---|
| Unit tests | Required for all engine logic (Reasoning, Planning, Memory retrieval) |
| Integration tests | Required for any change touching the API layer or Execution Engine dispatch |
| Contract tests | Required for plugin manifest schema changes |
| Manual verification | Required for desktop automation adapters (no reliable CI environment for UI Automation yet) |

Target: no PR merges without passing tests; coverage is tracked but not gated at an arbitrary percentage — a well-tested critical path beats padding coverage on trivial code.

## Dependency Management

- Dependencies pinned in `pyproject.toml`; no unpinned installs in CI.
- New dependencies require justification in the PR description: what problem it solves, why an existing dependency can't cover it.
- Security-sensitive dependencies (anything touching secrets, subprocess execution, or network calls) get called out explicitly in PR review.

## Code Review Expectations

- At least one approving review required before merge.
- Reviewers check: does this respect the Reasoning/Execution separation (`docs/architecture.md` §7)? Does it introduce an unaudited side effect path? Is the status marker in relevant docs updated?
- Disagreements get resolved by discussion in the PR thread, not by re-requesting review from someone more likely to approve.

## Development Environment

See `docs/installation.md` for full setup. Summary: Python 3.11+, virtual environment, `pip install -e .[dev]`, pre-commit hooks installed via `pre-commit install`.

## Release Process

- Versioning follows SemVer.
- Every release updates `CHANGELOG.md` under a new version heading before tagging.
- Pre-1.0 releases (`0.x.y`) may include breaking changes between minor versions — this is called out explicitly since MAX AI OS is early-stage and the plugin/API contracts are not yet stable.

## Missing Documentation (Recommended)

- A **local development troubleshooting FAQ** distinct from `docs/installation.md`'s troubleshooting section, once real contributors start hitting environment-specific issues worth cataloging.