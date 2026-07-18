# Reverse-engineering phase 7

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)  
Prior phase: [Reverse-engineering phase 6](reverse-engineering-phase-06.plan.md)

## Goal

Permit tuning only against development evidence, freeze the finalist configuration, and reject every post-validation retry in the same generation.

## Prerequisites

- Phases 3 and 6 passed.
- No iteration, seed round, or discrimination job is incomplete.

## Read first

1. Phase 3 and 6 handoffs
2. `src/eliotwf_skills/workflow/loop.py`
3. `src/eliotwf_skills/workflow/evidence_roles.py`
4. `src/eliotwf_skills/workflow/job_board.py`
5. `.cursor/skills/workflow/scripts/hillclimb_once.py`
6. `.cursor/skills/workflow/SKILL.md`

## In scope

- Add generation states `development`, `frozen`, and `validation_opened` to the existing run state.
- Add one finalist-freeze operation that records the selected draft, content brief, style block, craft briefs, evidence manifest, configuration, prompt, and model-role hashes.
- Refuse freezing while development work is incomplete.
- Add a validation-open operation that verifies the reserved identity and hash before making the evidence available.
- Guard all tuning mutations after freeze and validation opening.
- Expose freeze and validation-open commands through the existing CLI.
- Use one precise error directing post-validation tuning to a new generation.

## Out of scope

- Reserved-validation judging or outcome calculation.
- Content and quality vetoes.
- Scorer or judge formula changes.
- Automatic creation of a replacement generation.

## Files

Allowed:

- Modify `src/eliotwf_skills/workflow/loop.py`.
- Modify `.cursor/skills/workflow/scripts/hillclimb_once.py`.
- Create `tests/test_validation_freeze.py`.
- Modify `docs/adr/001-run-persistence.md`.
- Modify `.cursor/skills/workflow/SKILL.md`.

Forbidden:

- Evidence and draft-input modules
- Evaluator modules
- Agent contracts
- Existing run artifacts

## Test-first steps

1. Add failing tests for complete freeze contents and incomplete-work refusal.
2. Add tests requiring freeze and a matching reserved hash before validation opens.
3. Add one test for each mutating command after `validation_opened`.
4. Prove a reserved hash mismatch leaves state and files unchanged.
5. Implement the state transitions and shared tuning guard.
6. Run `$env:PYTHONPATH="src"; python -m pytest tests/test_validation_freeze.py -q`.
7. Run hillclimb, job-board, and run-state tests.
8. Run the full suite.

## Gate

PASS only when a fixture reaches `validation_opened`, every post-open mutation fails, the freeze contains complete hashes, and mismatched reserved evidence leaves no partial write.

## Handoff

Record state transitions, freeze hash, rejected commands, and test output in `handoff/REVERSE-ENGINEERING-PHASE-7-PASSED.md`.

## Stop conditions

- Required parent hashes are unavailable.
- Reserved validation can open before a complete freeze.
- Any post-validation tuning succeeds.
- A failed open leaves partial state.
- Any focused or full-suite test fails.
