# Reverse-engineering phase 8

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)  
Prior phase: [Reverse-engineering phase 7](reverse-engineering-phase-07.plan.md)

## Goal

Define and fixture-test a finalist-only content-adherence veto against the immutable content brief.

## Prerequisites

- Phase 7 passed.
- Content requirements have stable identifiers.
- This phase makes no live model calls.

## Read first

1. Phase 4 and 7 handoffs
2. `src/eliotwf_skills/workflow/content_contracts.py`
3. `src/eliotwf_skills/workflow/loop.py`
4. `src/eliotwf_skills/evaluator/score_draft_v2.py`
5. `.cursor/agents/eval-audit.md`
6. `.cursor/skills/evaluator/SKILL.md`

## In scope

- Create `src/eliotwf_skills/evaluator/content_adherence.py`.
- Build a judge packet containing only content brief and frozen draft.
- Require strict pass/fail JSON with one finding per required and forbidden identifier and evidence from the draft.
- Reject scores, unknown identifiers, duplicates, and missing findings.
- Create `.cursor/agents/content-adherence.md`.
- Persist `content-adherence.json` without changing `scores.json`.
- Require a recorded pass before reserved validation can open.
- Keep source-derived cast and scene replay diagnostic only unless the content brief names them.

## Out of scope

- Live judging.
- General prose quality.
- Changes to totals, deltas, ranking, calibration, pairwise, or discrimination.
- Deriving requirements from source prose.

## Files

Allowed:

- Create `src/eliotwf_skills/evaluator/content_adherence.py`.
- Modify `src/eliotwf_skills/workflow/loop.py`.
- Create `.cursor/agents/content-adherence.md`.
- Create `tests/test_content_adherence.py`.
- Modify `.cursor/skills/evaluator/SKILL.md`.
- Modify `.cursor/skills/workflow/SKILL.md`.

Forbidden:

- Existing scorer, calibration, pairwise, and discrimination modules
- Existing judge agents
- Run evidence

## Test-first steps

1. Add failing packet and parser tests.
2. Use one on-topic fixture and one stylistically convincing off-topic fixture.
3. Prove unknown, missing, duplicate, and scored findings fail.
4. Snapshot `scores.json` before and after pass and fail records.
5. Prove reserved validation cannot open without a pass.
6. Implement packet construction, parsing, persistence, and enforcement.
7. Run `$env:PYTHONPATH="src"; python -m pytest tests/test_content_adherence.py -q`.
8. Run the full suite.

## Gate

PASS only when fixture mechanics accept the on-topic draft, veto the off-topic draft, leave climb scores byte-identical, and block validation without a pass.

## Handoff

Record both fixture outcomes, score-file hashes, validation-open rejection, and test output in `handoff/REVERSE-ENGINEERING-PHASE-8-PASSED.md`.

## Stop conditions

- The instrument needs source, style block, calibration, score history, or reserved evidence.
- Its result would enter the climb score.
- A live call is proposed.
- Any focused or full-suite test fails.
