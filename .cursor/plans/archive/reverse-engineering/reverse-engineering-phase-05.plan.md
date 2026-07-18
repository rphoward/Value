# Reverse-engineering phase 5

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)  
Prior phase: [Reverse-engineering phase 4](reverse-engineering-phase-04.plan.md)

## Goal

Pass immutable content requirements separately from mutable craft guidance through draft and revision work.

## Prerequisites

- Phase 4 passed and exposes one content-contract loader and hash verifier.
- Reconcile this plan before implementation if Phase 4 used different public names.

## Read first

1. Phase 4 plan and handoff
2. `src/eliotwf_skills/workflow/content_contracts.py`
3. `src/eliotwf_skills/workflow/prepare.py`
4. `.cursor/agents/emulate-drafter.md`
5. `.cursor/agents/revise-drafter.md`
6. `.cursor/skills/workflow/SKILL.md`
7. `.cursor/skills/pipeline/SKILL.md`

## In scope

- Create `src/eliotwf_skills/workflow/draft_inputs.py`.
- Define immutable paths and hashes for style block and content brief, plus a separate per-iteration craft brief.
- Require prior draft only for revision iterations.
- Verify the content-brief hash before constructing draft inputs.
- Give content requirements precedence over craft guidance.
- Explicitly forbid source text, calibration, score history, qualitative history, discrimination artifacts, and reserved-validation evidence from drafter inputs.
- Update the paired drafter contracts and workflow/pipeline contracts to use the split.
- Treat `emulate-drafter.md` and `revise-drafter.md` as one paired interface for this phase. Their input names, precedence rule, and forbidden evidence list must remain identical.

## Out of scope

- Evidence roles or validation opening.
- Scoring, discrimination, pairwise, and stop changes.
- Live drafting or benchmark runs.
- Historical-run rewrites.

## Files

Allowed:

- Create `src/eliotwf_skills/workflow/draft_inputs.py`.
- Create `tests/test_draft_inputs.py`.
- Modify `.cursor/agents/emulate-drafter.md`.
- Modify `.cursor/agents/revise-drafter.md`.
- Modify `.cursor/skills/workflow/SKILL.md`.
- Modify `.cursor/skills/pipeline/SKILL.md`.

Forbidden:

- Evaluator modules and agents
- `loop.py` and `job_board.py`
- Existing run artifacts

## Test-first steps

1. Add failing tests that content and craft paths remain distinct.
2. Prove changing a craft brief does not change the content hash.
3. Prove content mutation and invalid prior-draft combinations are rejected.
4. Add contract tests for content precedence and the forbidden-input list.
5. Implement the input builder and per-iteration craft-brief writer.
6. Update the paired drafter and workflow contracts.
7. Run `$env:PYTHONPATH="src"; python -m pytest tests/test_draft_inputs.py -q`.
8. Run the full suite and `git diff --check`.

## Gate

PASS only when craft guidance can change without changing content requirements, both drafter contracts reject leakage, and the full suite passes.

## Handoff

Record the input fields, content hash, craft filenames, leakage assertions, and test output in `handoff/REVERSE-ENGINEERING-PHASE-5-PASSED.md`.

## Stop conditions

- The content contract must be duplicated or reparsed elsewhere.
- A craft brief can replace content requirements.
- A drafter requires forbidden evidence.
- Any focused or full-suite test fails.
