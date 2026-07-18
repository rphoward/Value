# Reverse-engineering phase 11

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)  
Prior phase: [Reverse-engineering phase 10](reverse-engineering-phase-10.plan.md)

## Goal

Populate and lock benchmark v1 with four clean targets, two independent briefs per target, and fresh baseline outputs.

## Prerequisites

- Phase 10 passed.
- Four owner-approved target corpora are available through permitted intake.
- Phase 1 supplies eight item identities and all fixed budgets and roles.

## Read first

1. Phase 1 and 10 handoffs
2. `docs/adr/001-run-persistence.md`
3. `docs/adr/002-owned-corpus-registry.md`
4. `src/eliotwf_skills/workflow/benchmark.py`
5. `.cursor/skills/workflow/scripts/benchmark_once.py`

## In scope

- Create `tools/runs/reverse-engineering-quality/benchmark-v1/**`.
- Populate Dostoevsky, Rilke, McCarthy, and AA targets.
- Create two independent content briefs per target.
- Store analysis, development, and reserved-validation roles with complete provenance and hashes.
- Generate fresh baseline outputs under the frozen baseline role and budget.
- Lock model roles, prompts, available seed facts, trial budgets, provenance, and instrument hashes.
- Initialize an empty reserved-consumption ledger.
- Validate the complete manifest without resolving reserved text.

## Out of scope

- Treatment generation or development judging.
- Reserved-validation scoring.
- Historical drafts, verdicts, or scores as inputs.
- Automatic Exa fetching in Python.
- Runtime, test, prompt, agent, scorer, or policy edits.

## Files

Allowed:

- Create `tools/runs/reverse-engineering-quality/benchmark-v1/**`.
- Create `handoff/REVERSE-ENGINEERING-PHASE-11-PASSED.md`.
- Modify `handoff/STATE.md` after the gate.

Forbidden:

- `src/**`
- `tests/**`
- `.cursor/agents/**`
- `.cursor/skills/**`
- Phase 1 manifest
- Historical run folders

## Test-first steps

1. Validate Phase 10 mechanics and run the full suite.
2. Confirm the benchmark directory does not exist.
3. Intake permitted passages and write complete provenance.
4. Create eight independent briefs and fresh baseline outputs.
5. Lock the benchmark through the Phase 10 CLI.
6. Require four targets, eight items, complete roles and hashes, and zero reserved consumption.
7. Re-run the full suite.

## Gate

PASS only when all eight items are complete and content-addressed, every baseline is fresh, provenance is reviewable, reserved consumption is false, and no frozen instrument changed.

## Handoff

Record benchmark manifest and lock hashes, item identities, baseline provenance, zero-consumption proof, live generation cost, and tests in `handoff/REVERSE-ENGINEERING-PHASE-11-PASSED.md`.

## Stop conditions

- Clean permitted evidence is unavailable.
- A baseline would come from historical output.
- Reserved text must be exposed to validation commands.
- A frozen instrument needs correction.
- Any hash or full-suite check fails.
