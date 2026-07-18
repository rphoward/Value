# Full-workflow local webapp — overview

Back-link: [full_workflow_webapp_829fdc0a.plan.md](../full_workflow_webapp_829fdc0a.plan.md)

## Context

The Starlette/HTMX shell stages files then ejects to Cursor for analyze and climb. Mutation already exists as `tools/sdk-climb.py` plus hillclimb CLI. Product goal is a local single-operator browser journey: brainstorm → passage → analyze → invent → hillclimb → pick draft.

## Scope

**In**

- Browser full chain on Document Canvas with Studio onboarding and Cockpit climb strip
- Starlette + HTMX + Jinja under `eliotapp/presentation/`
- Background jobs that spawn SDK climb; one active job per slug
- Human story progress; style-fidelity while climbing
- Fix `open_preference_job` missing import in `tools/sdk-climb.py`

**Out**

- Multi-user SaaS, accounts, remote deploy
- Replacing `decide()` or a second climb engine on HTTP
- SPA / React rewrite

## Constraints

- Local only. `CURSOR_API_KEY` + `pip install -e ".[sdk]"` on the box.
- Hillclimb mutation stays CLI/SDK-owned. HTTP queues and observes.
- One active job per slug. No second writer on `scores.json`.
- Keep Starlette + HTMX + Jinja.
- Dual-read migrate: align `--runs-base` with `WorkProductLocator`; prefer per-run ledger over global `.sdk-climb-last.json` for UI truth.
- Redesign as if the webapp were day-one; deliver in thin phases.

## Alternatives

| Candidate | Verdict |
|-----------|---------|
| Guided Studio | Graft onboarding only; not permanent shell |
| Run Cockpit | Graft climb strip + ledger; not cold-start home |
| Document Canvas (chosen) | Base shell; drafts as product |

Shared rule from all three: HTTP never writes `scores.json`; one worker per slug; `inspect`/`decide` stays traffic cop.

## Applicable skills / non-negotiables

- **how** before editing unfamiliar climb/presentation subsystems
- **architect** already synthesized; re-arena only on repeated friction
- **interrogate** on contested job-boundary before phase 8 merge
- **control-ui** for every UI phase
- **prototype** for Phase 1 throwaway switcher
- `/deslop` + **unslop** before commit
- **show-me-your-work** decision trail at `handoff/decision-trails/full-workflow-webapp.tsv`
- **babysit** after PR open
- `tool-ui-htmx`, `pipeline` / `workflow` / `evaluator` for contracts

## Phases

0. Plan dir split (this directory) — done when these files exist
1. [phase-01-ux-prototype.md](phase-01-ux-prototype.md)
2a. [phase-02a-job-ledger.md](phase-02a-job-ledger.md)
2b. [phase-02b-spawn.md](phase-02b-spawn.md)
3. [phase-03-document-canvas.md](phase-03-document-canvas.md)
4. [phase-04-onboarding.md](phase-04-onboarding.md)
5a. [phase-05a-improve-queue.md](phase-05a-improve-queue.md)
5b. [phase-05b-climb-strip.md](phase-05b-climb-strip.md)
6a. [phase-06a-analyze-job.md](phase-06a-analyze-job.md)
6b. [phase-06b-invent-job.md](phase-06b-invent-job.md)
7. [phase-07-pick-polish.md](phase-07-pick-polish.md)
8. [phase-08-interrogate-ship.md](phase-08-interrogate-ship.md)

See also [testing.md](testing.md).

## Verification

- Static: `pytest` (presentation + sdk-climb + job_runner)
- Runtime: control-ui against local `:8000`
- Prove disk: only CLI/SDK writes `scores.json`; HTTP writes revisions + job request/ledger only

## Implementation guidance

Prefer 2–3 files per phase. Sequence scaffold types before UI. Commit liberally per verifiable unit.
