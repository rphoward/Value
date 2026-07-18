# Phase 3 — Machine discrimination

Back to [overview](overview.md). Prerequisite: [phase-2-authorprint.md](phase-2-authorprint.md) done.

## Goal

Automate the human blind read. T trials per evaluation: spot the genuine passage, name one tell, compute indistinguishability.

## Changes

| File | Change |
|------|--------|
| `src/eliotwf_skills/evaluator/discrimination.py` | Trials, verdict parsing, indist math, tell collection |
| `.cursor/agents/discriminate.md` | Fresh-context spot-the-real subagent |
| `.cursor/skills/evaluator/scripts/discrimination_v2.py` | `prepare` / `score` mirroring `pairwise_v2.py` |
| `tests/test_scorer_v2.py` | Indist math, slicing, randomization, parsing, tells |

## Data structures

- `DiscriminationTrial`: `trial_id`, `passage_a`, `passage_b`, `genuine_side` (answer key, hidden from judge).
- `SpotVerdict`: `trial_id`, `genuine` ("A"|"B"), `tell` (one sentence).
- `DiscriminationResult`: `detection_rate`, `indistinguishability`, `tells: tuple[str, ...]`.

Formula: `INDISTINGUISHABILITY = 1 - max(0, 2*(detection_rate - 0.5))`.

## Verification

- Coin-flip detection_rate → indist 1.0; always-caught → 0.0; monotonic in between.
- `discrimination_v2.py prepare` + mock verdicts round-trip via `score`.
- Length-matched slices; seeded side randomization reproducible.
- Suite count grows; ruff clean.

## Paste into new chat

```text
/poteto-mode Phase 3 of scorer v2 final phases (discrimination module).

Read in order:
1. .cursor/plans/archive/scorer-v2-final-phases/phase-3-discrimination.md (this file)
2. src/eliotwf_skills/evaluator/pairwise.py (mirror this pattern)
3. .cursor/agents/pair-judge.md (mirror for discriminate.md)
4. .cursor/skills/evaluator/scripts/pairwise_v2.py (mirror for discrimination_v2.py)

Prerequisite: widened corpus from phase 1.

Do NOT touch EvaluatorScore or the gate harness yet.

Task: Ship Phase 4 discrimination scaffolding only.
- discrimination.py: DiscriminationTrial, SpotVerdict, DiscriminationResult, build_trials, parse_verdicts, aggregate, indistinguishability math.
- discriminate.md subagent: pick genuine passage + one tell; JSON output only.
- discrimination_v2.py CLI: prepare / score.
- Tests: indist math, length-matched slicing, side randomization, bad-input rejection, tell collection.
- Run: $env:PYTHONPATH="src"; python -m unittest discover -s tests -q

Stop when phase 3 verification passes. Do not run real judge smoke or gate yet.
```
