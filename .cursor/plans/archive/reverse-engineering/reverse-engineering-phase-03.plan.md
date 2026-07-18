# Reverse-engineering phase 3

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)  
Prior phase: [Reverse-engineering phase 2](reverse-engineering-phase-02.plan.md)

## Goal

Bind run transitions to one generation, make owned writes atomic, and make interruption recovery idempotent.

## Prerequisites

- Phases 1 and 2 passed.
- `inspect_run` is the sole recovery-decision seam.
- Legacy runs remain readable, but unverifiable legacy mutation may be refused.

## Read first

1. Phase 1 and 2 handoffs
2. `docs/adr/001-run-persistence.md`
3. `src/eliotwf_skills/workflow/run_state.py`
4. `src/eliotwf_skills/workflow/loop.py`
5. `src/eliotwf_skills/workflow/job_board.py`
6. `.cursor/skills/workflow/scripts/hillclimb_once.py`
7. Existing hillclimb and job-board tests

## In scope

- Add a schema version and generation ID to new runs.
- Freeze hashes for source, style block, configuration, parent experiment manifest, drafts, and genuine comparison text.
- Add same-directory atomic writes for state and job artifacts owned by the touched modules.
- Represent recorded drafts as awaiting discrimination until the binding result attaches.
- Refuse stale generation IDs, changed frozen inputs, and conflicting sidecars.
- Make retries converge without duplicate drafts, verdicts, results, decisions, or score entries.
- Refuse force reinitialization when dependent sidecars exist. Direct the operator to a new slug.
- Document schema, recovery, and legacy-read behavior in ADR 001.

## Out of scope

- Deleting, moving, or rewriting stale evidence.
- Legacy migration.
- Scorer, prompt, held-out, pipeline, or UI changes.
- Live interruption tests.

## Files

Allowed:

- Modify `src/eliotwf_skills/workflow/loop.py`.
- Modify `src/eliotwf_skills/workflow/job_board.py`.
- Modify `.cursor/skills/workflow/scripts/hillclimb_once.py`.
- Create `tests/test_run_recovery.py`.
- Modify `docs/adr/001-run-persistence.md`.

Forbidden:

- `src/eliotwf_skills/workflow/run_state.py`
- Scorer and agent contracts
- Historical run folders

## Test-first steps

1. Add failing tests for generation creation, frozen hashes, awaiting-discrimination state, and stale-generation refusal.
2. Add one interruption test at each write boundary: orphan draft, verdict before job update, result before job update, discrimination sidecar before manifest attachment, and seed copy before promotion.
3. Require each replay to produce one logical artifact.
4. Implement atomic writes and generation checks without adding a second state module.
5. Run `$env:PYTHONPATH="src"; python -m pytest tests/test_run_recovery.py tests/test_run_state.py -q`.
6. Run existing hillclimb and job-board tests.
7. Run the full suite.

## Gate

PASS only when every simulated interruption resumes without duplication, stale evidence is refused without deletion, incomplete iterations stay incomplete, and legacy reads still pass.

## Handoff

Record schema fields, generation rules, recovery cases, manifest hash, and actual test output in `handoff/REVERSE-ENGINEERING-PHASE-3-PASSED.md`.

## Stop conditions

- Recovery requires deleting or silently replacing evidence.
- A hash mismatch is ignored.
- A retry duplicates a logical artifact.
- Legacy reading breaks.
- Any focused or full-suite test fails.
