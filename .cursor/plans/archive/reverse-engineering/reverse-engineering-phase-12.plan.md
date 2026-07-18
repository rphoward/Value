# Reverse-engineering phase 12

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)  
Prior phase: [Reverse-engineering phase 11](reverse-engineering-phase-11.plan.md)

## Goal

Run both benchmark arms through all pre-validation mechanics with fixture verdicts only.

## Prerequisites

- Phase 11 passed and all benchmark hashes match.
- Reserved consumption is false.
- The `dry-run-001` generation does not exist.

## Read first

1. Phase 11 handoff
2. Benchmark manifest and lock
3. `src/eliotwf_skills/workflow/benchmark.py`
4. `.cursor/skills/workflow/scripts/benchmark_once.py`

Do not read reserved-validation files.

## In scope

- Create one new `dry-run-001` generation.
- Exercise baseline and treatment arms for all eight items.
- Replay fixture development judgments and both vetoes.
- Exercise finalist, veto, tie, disagreement, and no-finalist paths.
- Verify arm comparability, lineage, terminal state, and zero reserved consumption.
- Record a dry-run report and gate artifact.

## Out of scope

- Code, test, skill, agent, prompt, manifest, or policy edits.
- Live drafting or judging.
- Reserved evidence access.
- Quality or cost conclusions from fixtures.
- Reusing a failed generation.

## Files

Allowed:

- Create `tools/runs/reverse-engineering-quality/dry-run-001/**`.
- Create `handoff/REVERSE-ENGINEERING-PHASE-12-PASSED.md`.
- Modify `handoff/STATE.md` after the gate.

Forbidden:

- `src/**`
- `tests/**`
- `.cursor/agents/**`
- `.cursor/skills/**`
- Benchmark and protocol inputs
- Historical run folders

## Test-first steps

1. Validate all frozen hashes and reserved-consumption state.
2. Run the full suite before creating output.
3. Initialize `dry-run-001`.
4. Run both arms with fixture verdicts.
5. Require sixteen terminal arm/item results with complete lineage.
6. Revalidate benchmark hashes and reserved consumption.
7. Run the full suite again.

## Gate

PASS only when both arms have terminal comparable artifacts for all items, every artifact resolves through one generation, no live calls occur, and reserved consumption remains false.

## Handoff

Record generation and report hashes, terminal counts, zero-live-call proof, reserved state, and test output in `handoff/REVERSE-ENGINEERING-PHASE-12-PASSED.md`.

## Stop conditions

- A frozen hash differs.
- `dry-run-001` already exists.
- The harness requests reserved evidence.
- A defect appears. Record it and derive a corrective phase instead of editing the instrument.
- Any lineage, status, or test check fails.
