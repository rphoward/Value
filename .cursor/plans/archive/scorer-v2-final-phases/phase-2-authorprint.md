# Phase 2 — AUTHORPRINT wire

Back to [overview](overview.md). Prerequisite: [phase-1-corpus.md](phase-1-corpus.md) done.

## Goal

Add a 0–100 AUTHORPRINT diagnostic score. Source scores high on its own profile vs the contrast author. Keep OUT of `EvaluatorScore`.

## Changes

| File | Change |
|------|--------|
| `src/eliotwf_skills/evaluator/authorprint.py` | Add `margin_to_score()` or equivalent 0–100 mapping |
| `.cursor/skills/evaluator/scripts/authorprint_v2.py` | Thin CLI: `measure` (margins) and `score` (draft vs profiles) |
| `tests/test_scorer_v2.py` | Extend `AuthorprintTests`: own-profile threshold, widened-corpus margins |

## Data structures

`AuthorprintScore`: `{score: float, delta_to_own: float, delta_to_other: float, author: str}` — diagnostic only, not in `EvaluatorScore`.

## Verification

- `authorprint_v2.py measure` writes/updates `margins.json`.
- Dostoevsky source scores high on own profile; Rilke source ditto.
- Both-direction margin tests pass on widened corpus.
- Suite count > 66; ruff clean on new files.

## Paste into new chat

```text
/poteto-mode Phase 2 of scorer v2 final phases.

Read in order:
1. handoff/STATE.md
2. .cursor/plans/archive/scorer-v2-final-phases/phase-2-authorprint.md (this file)
3. src/eliotwf_skills/evaluator/authorprint.py
4. tools/runs/scorer-v2/authorprint/margins.json (from phase 1)

Prerequisite: phase 1 corpus exists under tools/runs/scorer-v2/corpus/dostoevsky/.

Do NOT touch EvaluatorScore, score_draft_v2.py deterministic axes, style block, or ELIOT skill.

Task: Wire AUTHORPRINT as a 0-100 diagnostic axis only.
- Add score mapping in authorprint.py (margin- or ratio-based; decide in impl).
- Add authorprint_v2.py CLI (measure + score).
- Extend AuthorprintTests: source above threshold on own profile; margins positive both directions.
- Run: $env:PYTHONPATH="src"; python -m unittest discover -s tests -q

Stop when phase 2 verification passes. Do not start discrimination.py.
```
