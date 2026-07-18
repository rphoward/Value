# Reverse-engineering phase 17

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)  
Prior phase: [Reverse-engineering phase 16](reverse-engineering-phase-16.plan.md)

## Goal

Conditionally ship adaptive discrimination stopping that reproduces locked benchmark winners and vetoes while retaining fixed-budget fallback.

## Prerequisites

- Read the Phase 16 report before any code change.
- If Phase 16 is not `PASS`, this phase is `SKIP`.
- On `PASS`, the selected policy and all parent hashes must match the Phase 16 handoff.
- The decision margin must not be smaller than the metric's measurement resolution.

## Read first

1. Phase 16 handoff and replay report
2. `src/eliotwf_skills/evaluator/discrimination.py`
3. `src/eliotwf_skills/workflow/job_board.py`
4. `.cursor/skills/workflow/scripts/hillclimb_once.py`
5. `tests/test_job_board.py`
6. `.cursor/skills/workflow/SKILL.md`
7. `.cursor/skills/workflow/references/one-command.md`

## In scope

Only when Phase 16 passes:

- Export the exact selected policy with its parent report hash.
- Add backward-compatible adaptive fields to discrimination jobs.
- Preserve fixed-budget behavior when no policy is supplied.
- Enforce minimum trials, checkpoint boundaries, decision margin, and hard maximum.
- Record completed, pending, and skipped trial identities.
- Aggregate completed trials only after an adaptive stop.
- Add a production-code replay command against locked traces.
- Document the opt-in command and fixed-budget fallback.

## Out of scope

- Any production change when Phase 16 fails or is inconclusive.
- Judge, scorer, prompt, retry, veto, benchmark, or iteration-count changes.
- Making adaptive mode mandatory.
- Raising the hard maximum.
- Live benchmark reruns.

## Files

On `SKIP`, allowed:

- Create `handoff/REVERSE-ENGINEERING-PHASE-17-SKIPPED.md`.

On `PASS`, allowed:

- Modify `src/eliotwf_skills/evaluator/discrimination.py`.
- Modify `src/eliotwf_skills/workflow/job_board.py`.
- Modify `.cursor/skills/workflow/scripts/hillclimb_once.py`.
- Modify `tests/test_job_board.py`.
- Create `.cursor/skills/workflow/references/adaptive-stopping.json`.
- Modify `.cursor/skills/workflow/SKILL.md`.
- Create `tools/runs/reverse-engineering-quality/phase-17/production-replay-report.json`.

Forbidden:

- `loop.py`
- Other evaluator modules and tests
- Agent and command contracts
- Phase 1–16 evidence

## Test-first steps

1. If Phase 16 is not `PASS`, write the skipped handoff and stop.
2. Add failing tests for legacy fixed-budget loading, measurement resolution, minimum trials, checkpoints, skipped trials, hard maximum, boundary fallback, completed-only aggregation, and winner/veto replay agreement.
3. Implement adaptive policy validation and stop decisions.
4. Extend job state backward-compatibly.
5. Add policy input and production replay to the existing CLI.
6. Run `$env:PYTHONPATH="src"; python -m pytest tests/test_job_board.py -q`.
7. Run production replay and require every winner, finalist, and veto to match Phase 16.
8. Run the full suite.

## Gate

SKIP is mandatory unless Phase 16 passed. PASS requires exact winner and veto agreement, hard-maximum compliance, unchanged fixed-budget behavior, valid measurement resolution, and a passing full suite.

## Handoff

On SKIP, record the Phase 16 outcome, report hash, reason, and proof that no production file changed. On PASS, record policy values and hashes, agreement counts, trial reduction, hard-maximum proof, fallback proof, opt-in command, and tests in `handoff/REVERSE-ENGINEERING-PHASE-17-PASSED.md`.

## Stop conditions

- Phase 16 is not `PASS`.
- Policy or parent hashes differ.
- The decision margin is below measurement resolution.
- Legacy fixed-budget behavior changes.
- Production replay changes any winner or veto.
- Any adaptive job exceeds its maximum.
- Any focused or full-suite test fails.
