# Reverse-engineering phase 6

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)  
Prior phase: [Reverse-engineering phase 5](reverse-engineering-phase-05.plan.md)

## Goal

Assign explicit roles to analysis source, development genuine evidence, and reserved validation while keeping reserved material out of every development view.

## Prerequisites

- Phase 5 passed.
- The Phase 1 manifest registers reserved identities and hashes without content.

## Read first

1. Phase 5 handoff
2. `docs/adr/001-run-persistence.md`
3. `src/eliotwf_skills/workflow/prepare.py`
4. `src/eliotwf_skills/workflow/draft_inputs.py`
5. `src/eliotwf_skills/evaluator/discrimination.py`
6. `src/eliotwf_skills/evaluator/pairwise.py`
7. `.cursor/skills/workflow/SKILL.md`

## In scope

- Create `src/eliotwf_skills/workflow/evidence_roles.py`.
- Define `analysis_source`, `development_genuine`, and `reserved_validation`.
- Persist source and development paths with hashes.
- Persist only reserved identity and hash. Do not store reserved text or a resolvable path in development artifacts.
- Make `prepare_run` write the evidence manifest.
- Treat existing `held-out.txt` as legacy development evidence.
- Keep `genuine_path` as a compatibility alias for the development path.
- Expose only a boolean reserved-registration fact to development reports.
- Keep discrimination and pairwise formulas unchanged.

## Out of scope

- Opening or copying reserved content.
- Finalist freezing or validation scoring.
- Retry and stopping changes.
- Historical-run migration.

## Files

Allowed:

- Create `src/eliotwf_skills/workflow/evidence_roles.py`.
- Modify `src/eliotwf_skills/workflow/prepare.py`.
- Create `tests/test_evidence_roles.py`.
- Modify `docs/adr/001-run-persistence.md`.
- Modify `.cursor/skills/workflow/SKILL.md`.

Forbidden:

- Evaluator formulas
- `loop.py`
- Drafter and judge agents
- Existing run artifacts

## Test-first steps

1. Add failing tests for all three roles and legacy held-out behavior.
2. Place a unique reserved-text canary outside the run directory.
3. Assert the canary and its path are absent from serialized development views and draft inputs.
4. Assert the development accessor can never resolve the reserved role.
5. Implement role parsing, hash checks, audience-specific accessors, and prepare adoption.
6. Run `$env:PYTHONPATH="src"; python -m pytest tests/test_evidence_roles.py -q`.
7. Run prepare and draft-input tests.
8. Run the full suite.

## Gate

PASS only when the reserved canary is absent from every development-facing artifact, development access cannot resolve reserved evidence, legacy runs remain readable, and formulas are unchanged.

## Handoff

Record the evidence schema, leakage result, compatibility behavior, and actual tests in `handoff/REVERSE-ENGINEERING-PHASE-6-PASSED.md`.

## Stop conditions

- Reserved text or its path must enter an active development run.
- A scorer or judge formula must change.
- Backward compatibility requires rewriting history.
- Any leakage or test assertion fails.
