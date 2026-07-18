# Reverse-engineering phase 2

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)  
Prior phase: [Reverse-engineering phase 1](reverse-engineering-phase-01.plan.md)

## Goal

Add one read-only run-inspection seam that classifies valid partial and complete runs and returns exactly one `next_action`.

## Prerequisites

- Phase 1 passed and its manifest hash matches the handoff.
- Existing run writers remain unchanged in this phase.

## Read first

1. `AGENTS.md`
2. `handoff/STATE.md`
3. Phase 1 handoff and experiment manifest
4. `docs/adr/001-run-persistence.md`
5. `src/eliotwf_skills/workflow/loop.py`
6. `src/eliotwf_skills/workflow/job_board.py`
7. `.cursor/skills/workflow/scripts/hillclimb_once.py`
8. `tests/test_hillclimb.py`
9. `tests/test_job_board.py`

## In scope

- Create `src/eliotwf_skills/workflow/run_state.py`.
- Define `RunInspection` with `valid`, `generation_id`, `iteration_state`, `next_action`, and ordered `issues`.
- Recognize initialized runs, seed rounds, orphan drafts, pending or scored discrimination, completed iterations, stopped runs, and mixed evidence.
- Treat a total-based stop without attached discrimination as incomplete.
- Return `repair_required` for contradictions or missing dependencies.
- Add a read-only `inspect --run-dir` command that emits one JSON object and changes no files.

## Out of scope

- Schema changes or generation IDs on writers.
- Repair, cleanup, migration, or deletion.
- Changes to scoring, stopping, promotion, or UI behavior.

## Files

Allowed:

- Create `src/eliotwf_skills/workflow/run_state.py`.
- Modify `.cursor/skills/workflow/scripts/hillclimb_once.py`.
- Create `tests/test_run_state.py`.
- Modify `handoff/STATE.md` after the gate.

Forbidden:

- `src/eliotwf_skills/workflow/loop.py`
- `src/eliotwf_skills/workflow/job_board.py`
- Existing run artifacts

## Test-first steps

1. Add failing tests for initialized, seed, pending-trial, scored-job, missing-discrimination, complete, stopped, and contradictory fixtures.
2. Add `test_inspection_returns_exactly_one_next_action`.
3. Add `test_inspect_cli_is_read_only`, comparing every fixture file hash before and after the command.
4. Implement the smallest parser and state classifier.
5. Run `$env:PYTHONPATH="src"; python -m pytest tests/test_run_state.py -q`.
6. Run adjacent hillclimb and job-board tests.
7. Run the full suite.

## Gate

PASS only when every fixture returns one expected action, contradictory evidence requires repair, provisional stops cannot hide pending discrimination, and inspection changes no bytes.

## Handoff

Record the `RunInspection` fields, action vocabulary, parent-manifest hash, and actual test results in `handoff/REVERSE-ENGINEERING-PHASE-2-PASSED.md`.

## Stop conditions

- Classification requires mutating a run.
- More than one next action is needed.
- A missing dependency is silently accepted.
- Existing writer behavior must change.
- Any focused or full-suite test fails.
