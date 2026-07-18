# Reverse-engineering phase 14

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)  
Prior phase: [Reverse-engineering phase 13](reverse-engineering-phase-13.plan.md)

## Goal

Open reserved validation exactly once, judge the frozen arms, and return the Phase 1 `PASS`, `FAIL`, or `INCONCLUSIVE` outcome.

## Prerequisites

- Phases 1–13 passed.
- Development freeze and all parent hashes match.
- Validation state is unopened with zero consumption.
- Phase 10 fixture-tested the validation commands and aggregation.

## Read first

1. Phase 1 and 13 handoffs
2. Experiment manifest
3. Benchmark manifest and lock
4. Development freeze and lineage report
5. `src/eliotwf_skills/workflow/benchmark.py`
6. `.cursor/skills/workflow/scripts/benchmark_once.py`

Do not open reserved prose manually.

## In scope

- Run validation preflight.
- Atomically mark validation opened before resolving reserved text.
- Build blind jobs with frozen judge contracts and budgets.
- Record judgments without answer keys in worker inputs.
- Cluster fragment trials under independent benchmark items.
- Report item fidelity, content and quality non-losses, severe collapses, originality, cost, wall time, uncertainty, and parent hashes.
- Preserve a valid treatment failure as evidence.

## Out of scope

- Code, test, prompt, agent, scorer, benchmark, margin, finalist, or budget edits.
- Retry or tuning after opening.
- A second validation opening.
- Multi-passage work or adaptive stopping.

## Files

Allowed:

- Create `tools/runs/reverse-engineering-quality/development-001/reserved-validation/**`.
- Create `handoff/REVERSE-ENGINEERING-PHASE-14-PASSED.md`.
- Modify `handoff/STATE.md` after execution.

Forbidden:

- All source, test, skill, agent, and frozen input files
- Development drafts and finalist records
- Historical run folders

## Test-first steps

1. Run validation preflight and the full suite.
2. Require unopened state, matching hashes, frozen arms, and zero pending development work.
3. Open validation once.
4. Immediately prove a second open and every tuning command fail.
5. Complete only the blind jobs returned by the validation queue.
6. Finalize after zero pending jobs.
7. Validate the report schema, independent item count, clustered fragments, hashes, cost, time, and outcome.
8. Run the full suite again.

## Gate

Execution passes when validation opened once, all required jobs completed, hashes remained unchanged, no tuning occurred, and the full suite passed. The experiment outcome is separately `PASS`, `FAIL`, or `INCONCLUSIVE` under the frozen Phase 1 rules.

## Handoff

Record opening count, timestamps, item and fragment counts, model roles, cost, time, execution status, experiment outcome, failed criteria, hashes, and test results in `handoff/REVERSE-ENGINEERING-PHASE-14-PASSED.md`.

## Stop conditions

- A prerequisite gate or hash is missing.
- Validation was already opened.
- Any frozen fact needs correction.
- A worker receives an answer key or development history.
- Any post-open tuning write succeeds.
- Execution fails after opening. Record `INCONCLUSIVE`; do not reopen this generation.
