# Reverse-engineering phase 16

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)  
Prior phase: [Reverse-engineering phase 15](reverse-engineering-phase-15.plan.md)

## Goal

Replay frozen evaluation traces offline and test whether staged evaluation preserves winners and vetoes while reducing cost.

## Prerequisites

- Phase 15 execution passed.
- Workstream E traces are frozen and content-addressed.
- Phase 1 fixes small-batch size, boundary rule, agreement margins, cost reduction, wall-time ratio, and hard maximum.
- Replay requires no live call.

## Read first

1. Phase 15 handoff
2. Experiment manifest
3. Development freeze and evaluation traces
4. Phase 14 validation report
5. `src/eliotwf_skills/evaluator/discrimination.py`
6. `src/eliotwf_skills/evaluator/pairwise.py`
7. `src/eliotwf_skills/workflow/loop.py`

## In scope

- Create `src/eliotwf_skills/workflow/staged_replay.py`.
- Create `.cursor/skills/workflow/scripts/run_staged_replay.py`.
- Replay deterministic checks, one cold qualitative result, a small blind batch, and extra recorded judgments only near a decision boundary.
- Use only evidence available at each replay checkpoint.
- Preserve content and quality vetoes unchanged.
- Compare winner, finalist, veto, cost, wall time, and trials against the full policy.
- Emit a selected policy only on `PASS`; retain the full policy on `FAIL` or `INCONCLUSIVE`.

## Out of scope

- Live calls or new judgments.
- Trace, verdict, prompt, scorer, margin, benchmark, or production changes.
- Reading future full-policy results to make an earlier staged decision.
- Production adaptive stopping.

## Files

Allowed:

- Create `src/eliotwf_skills/workflow/staged_replay.py`.
- Create `.cursor/skills/workflow/scripts/run_staged_replay.py`.
- Create `tests/test_staged_replay.py`.
- Create `tools/runs/reverse-engineering-quality/phase-16/staged-replay-report.json`.

Forbidden:

- Frozen traces and benchmark artifacts
- Existing evaluator, loop, job-board, agent, and skill files
- Production run artifacts

## Test-first steps

1. Add failing tests for trace hashes, ordering, one qualitative pass, small batch, boundary expansion, hard maximum, veto preservation, recorded cost/time, no live calls, and deterministic output.
2. Add tests that future evidence cannot affect an earlier checkpoint.
3. Implement strict trace loading and replay.
4. Run `$env:PYTHONPATH="src"; python -m pytest tests/test_staged_replay.py -q`.
5. Run replay twice and require byte-identical reports.
6. Compare item-level winners and vetoes with the full policy.
7. Run the full suite.

## Gate

PASS requires every frozen agreement, veto, cost, time, uncertainty, and hard-maximum threshold. FAIL or INCONCLUSIVE retains the full policy and forbids Phase 17 implementation.

## Handoff

Record trace hashes, policies, agreement, veto, cost, time, trial counts, measurement resolution, outcome, and `phase_17: READY|SKIP` in `handoff/REVERSE-ENGINEERING-PHASE-16-PASSED.md`.

## Stop conditions

- A trace lacks identity, order, result, cost, time, or veto facts.
- Replay requires a live judgment.
- Expansion logic sees future evidence.
- The hard maximum is exceeded.
- Output is not deterministic.
- Any focused or full-suite test fails.
