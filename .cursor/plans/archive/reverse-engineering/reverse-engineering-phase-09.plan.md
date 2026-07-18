# Reverse-engineering phase 9

Back-link: [Reverse-engineering quality master plan](reverse-engineering-quality-master_da289ff7.plan.md)  
Prior phase: [Reverse-engineering phase 8](reverse-engineering-phase-08.plan.md)

## Goal

Define fixture-tested, finalist-only general prose-quality comparison with pass, veto, and human-review outcomes.

## Prerequisites

- Phase 8 passed.
- Phase 1 fixes judge count and agreement rules.
- This phase makes no live model calls.

## Read first

1. Phase 1 and 8 handoffs
2. `src/eliotwf_skills/evaluator/pairwise.py`
3. `.cursor/agents/pair-judge.md`
4. `tests/test_scorer_v2.py`
5. `.cursor/skills/evaluator/SKILL.md`

## In scope

- Create `src/eliotwf_skills/evaluator/quality_veto.py`.
- Compare candidate and incumbent blindly for coherence, repetition, completeness, and obvious factual failure.
- Balance A/B orientation and hide candidate side from judge payloads.
- Permit `A`, `B`, and `TIE`.
- Return `pass` for candidate agreement or material parity, `veto` for incumbent agreement, and `human_review` for unresolved disagreement.
- Create `.cursor/agents/quality-judge.md`.
- Emit no numeric quality score and do not alter fidelity ranking.

## Out of scope

- Live judge calls.
- Source, style block, content brief, score history, author label, or filename in judge prompts.
- Promotion wiring and benchmark execution.
- Changes to existing pairwise questions or math.

## Files

Allowed:

- Create `src/eliotwf_skills/evaluator/quality_veto.py`.
- Create `.cursor/agents/quality-judge.md`.
- Create `tests/test_quality_veto.py`.
- Modify `.cursor/skills/evaluator/SKILL.md`.

Forbidden:

- `pairwise.py`
- Existing scorers and judge agents
- `loop.py`
- Run evidence

## Test-first steps

1. Add failing tests for deterministic balanced orientation and blind payloads.
2. Add parser tests for wins, ties, unknown labels, duplicates, and missing jobs.
3. Add aggregation tests for pass, veto, and human review.
4. Assert no numeric quality field is emitted.
5. Implement only generic comparison mechanics; do not import source-relative axes.
6. Run `$env:PYTHONPATH="src"; python -m pytest tests/test_quality_veto.py -q`.
7. Run the full suite.

## Gate

PASS only when fixtures prove blind balanced comparisons and stable handling of wins, losses, ties, and disagreement without producing a score or making a live call.

## Handoff

Record frozen agreement rules, fixture outcomes, agent-contract hash, and test output in `handoff/REVERSE-ENGINEERING-PHASE-9-PASSED.md`. Mark live reliability `UNPROVEN`; Phase 13 must run a bounded approved smoke before the full development experiment.

## Stop conditions

- Candidate identity or style evidence must enter a judge packet.
- The result becomes another weighted score.
- Existing pairwise behavior must change.
- A live call is proposed.
- Any focused or full-suite test fails.
