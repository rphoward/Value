# Reverse-engineering phase 15

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)  
Prior phase: [Reverse-engineering phase 14](reverse-engineering-phase-14.plan.md)

## Goal

Run a report-only pilot that tests whether additional scoped passages reduce or increase winner reversals for one target.

## Prerequisites

- Phase 14 execution passed.
- Its experiment outcome is not `INCONCLUSIVE`.
- Phase 1 names the pilot target and reversal rule.

## Read first

1. Phase 14 handoff and report
2. Experiment and benchmark manifests
3. Frozen baseline and treatment finalists for the selected target
4. `src/eliotwf_skills/evaluator/discrimination.py`
5. `.cursor/agents/discriminate.md`

## In scope

- Create `src/eliotwf_skills/workflow/multi_passage_pilot.py`.
- Create `.cursor/skills/workflow/scripts/run_multi_passage_pilot.py`.
- Use exactly one target and three additional passages.
- Record author, work, edition or translator, register, chapter mode, topic scope, source identity, retrieval facts, word count, and hash.
- Compare frozen baseline and treatment finalists with the existing fidelity instrument.
- Define reversal relative to the corresponding clean benchmark winner.
- Report winner order, reversal count, uncertainty, cost, time, and unchanged production hashes.
- Keep the result report-only.

## Out of scope

- Production selection or retry changes.
- More targets or passages.
- Prompt, scorer, judge, budget, or benchmark changes.
- Automatic Exa fetching in Python.
- Adaptive stopping.

## Files

Allowed:

- Create `src/eliotwf_skills/workflow/multi_passage_pilot.py`.
- Create `.cursor/skills/workflow/scripts/run_multi_passage_pilot.py`.
- Create `tests/test_multi_passage_pilot.py`.
- Create `tools/runs/reverse-engineering-quality/phase-15/**`.

Forbidden:

- Existing evaluator and workflow behavior
- Agent and skill contracts
- Frozen benchmark and production artifacts

## Test-first steps

1. Add failing tests for exactly three passages, complete provenance, translator rules, hashes, reversal calculation, clustered fragments, and write prohibition.
2. Implement manifest validation, blind-job construction, recording, and report generation.
3. Run `$env:PYTHONPATH="src"; python -m pytest tests/test_multi_passage_pilot.py -q`.
4. Intake three passages without adding network behavior to Python.
5. Validate, execute, and finalize the pilot.
6. Prove all frozen production hashes are unchanged.
7. Run the full suite.

## Gate

Execution passes only with one target, three valid passages, complete item-clustered judgments, unchanged production artifacts, and passing tests. Report `PASS`, `FAIL`, or `INCONCLUSIVE` against the frozen reversal rule without changing production.

## Handoff

Record passage provenance, clean and pilot winner orders, reversals, uncertainty, cost, time, unchanged hashes, outcome, and tests in `handoff/REVERSE-ENGINEERING-PHASE-15-PASSED.md`.

## Stop conditions

- Phase 14 is inconclusive.
- Passage scope or provenance cannot be established.
- The fidelity instrument must change.
- Pilot evidence enters a retry brief or production selection.
- Any focused or full-suite test fails.
