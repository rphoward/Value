# Reverse-engineering phase 10

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)  
Prior phase: [Reverse-engineering phase 9](reverse-engineering-phase-09.plan.md)

## Goal

Build and fixture-test the benchmark runner without creating benchmark prose or making live calls.

## Prerequisites

- Phases 1–9 passed.
- Phase 1 freezes all benchmark, veto, validation, and outcome rules consumed by this runner.

## Read first

1. Phase 1 and 9 handoffs
2. `docs/adr/001-run-persistence.md`
3. `src/eliotwf_skills/workflow/loop.py`
4. `src/eliotwf_skills/workflow/run_state.py`
5. Existing scorer-v2 gate manifests and scripts

## In scope

- Create `src/eliotwf_skills/workflow/benchmark.py`.
- Create `.cursor/skills/workflow/scripts/benchmark_once.py`.
- Define strict manifest loading, path containment, role filtering, hashes, generation initialization, status, freeze, and reserved-consumption state.
- Fixture-test dry-run terminal paths, development freeze, one-time validation opening, item-clustered aggregation, and `PASS`, `FAIL`, and `INCONCLUSIVE`.
- Prove pre-validation commands cannot resolve reserved text.
- Keep all fixtures synthetic and local to one focused test file.

## Out of scope

- Real benchmark passages, briefs, baseline outputs, or run folders.
- Live drafting or judging.
- Existing scorer, workflow, agent, prompt, and policy changes.
- Automatic Exa fetching.

## Files

Allowed:

- Create `src/eliotwf_skills/workflow/benchmark.py`.
- Create `.cursor/skills/workflow/scripts/benchmark_once.py`.
- Create `tests/test_reverse_engineering_benchmark.py`.
- Modify `docs/adr/001-run-persistence.md`.

Forbidden:

- `tools/runs/reverse-engineering-quality/benchmark-v1/**`
- Existing evaluator, loop, job-board, agent, and skill files
- Historical run evidence
- Phase 1 experiment manifest

## Test-first steps

1. Add failing tests for manifest shape, path containment, hashes, provenance, roles, budgets, and instrument identities.
2. Add tests that pre-validation access to reserved roles fails.
3. Add fixture-only dry-run, finalist, veto, no-finalist, and freeze cases.
4. Add one-time validation opening and item-clustered outcome cases.
5. Add deterministic replay and byte-identical report tests.
6. Implement the module and thin CLI.
7. Run `$env:PYTHONPATH="src"; python -m pytest tests/test_reverse_engineering_benchmark.py -q`.
8. Run the full suite.

## Gate

PASS only when synthetic fixtures cover every terminal path, reserved access remains sealed before validation, reports are deterministic, and the full suite passes without live calls.

## Handoff

Record public commands, schemas, fixture cases, reserved-access proof, and test output in `handoff/REVERSE-ENGINEERING-PHASE-10-PASSED.md`.

## Stop conditions

- Real evidence or a live call is needed to test mechanics.
- Existing instruments must change.
- Pre-validation can resolve reserved content.
- More than one runtime module or focused test file is needed.
- Any focused or full-suite test fails.
