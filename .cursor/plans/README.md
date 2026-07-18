# Plans index

Cursor plan files for EliotWF. **Living state:** `handoff/STATE.md`. Completed plans are in [archive/](archive/README.md).

Last indexed: 2026-07-17.

## Active

None. UI/UX wave is next per `handoff/STATE.md` (no plan file yet).

## Deferred (no active plan file)

| Item | Record |
|------|--------|
| UI/UX wave (Canvas restyle + invent surfaces) | `handoff/CLIMB-SIGNAL-INTERROGATE-HANDOFF.md` protocol-4; keep consumer contracts + scores-write lock |
| Soft-fail Canvas on corrupt accept | Intent-repair out-of-scope migrate; `handoff/CLIMB-SIGNAL-INTENT-REPAIR-PASSED.md` |
| Delete flat `accept_*` dual-write | Same migrate wave after Canvas sole-reads `accept_decision` |
| Source ingest (EPUB/PDF) | `handoff/EPUB to Markdown.md` |
| Invent UI polish | Optional; `handoff/PIPELINE-UI-CATALOG.md` |

## Archived tracks

See [archive/README.md](archive/README.md) for climb-signal, full-workflow webapp, eliotapp peel, invent seeds, hooks/SDK climb, workflow build, thermos `.cursor` fixes, reverse-engineering, preference, scorer v2, Web UI v2, and hillclimb.

## Historical (not plans)

| Path | Role |
|------|------|
| `handoff/PLAN.md` | Original phased build order from the pre-scaffold planning chat |
| `handoff/ARCHITECTURE.md` | Skill vs subagent vs automation decisions |
| `handoff/WORKFLOW.md` | Pipeline in the owner's words |
