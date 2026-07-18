# Phase 01 — Inspect split

Back-link: [overview.md](overview.md)

## Goal

Callers pass `run_id` + locator. Store loads facts. Core decides. `inspect_run` no longer takes a bare `Path`.

## Changes

- Today: `eliotapp/application/workflow/run_state.py` `inspect_run(run_dir: Path)`. **No** `eliotapp/core/progression.py` yet — create it in this phase.
- Introduce store load → `InspectedRun` / `RunSnapshot` (names per SYNTHESIS).
- Extract pure progression decide into new `core.progression` (no Path).
- Rewrite application compose + SDK (`tools/sdk_climb_lib.py`) to the new signature.
- Keep behavior identical for existing hillclimb decisions.

## Data structures

- `InspectedRun` / `RunSnapshot`: facts loaded from disk once.
- Decide input/output: pure progression verdict (next action, issues).

## Verification

**Static.** Pytest covering inspect / run_state / preference / SDK resume paths.

**Runtime.** `control-cli` or existing hillclimb_cli / `tools/sdk-climb.py` dry path on a fixture run: inspect returns the same next-action class as before.
