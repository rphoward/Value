# Scorer v2 — final phases (split plan)

Back to [plans index](../../README.md). Monolithic stub: [scorer-v2_final_phases_589276ee.plan.md](../scorer-v2_final_phases_589276ee.plan.md).

## Context

Phases 1–3 of scorer v2 are shipped (66 tests green). What remains is corpus widen, AUTHORPRINT wiring, machine discrimination (Phase 4), validation gate (Phase 5), and a live judge smoke test. The work was one large plan; it is split here so **each phase is one chat session** under a ~200k context budget.

## Scope

**In:** corpus pull, AUTHORPRINT 0–100 diagnostic axis, discrimination test, gate harness, smoke, cleanup.

**Out:** frozen style block, ELIOT skill, v1/v2 deterministic scorer, `EvaluatorScore` shape. No emulation climbing until `SCORER-V2-PASSED.md`.

## Locked decisions

- Headline metric: **INDISTINGUISHABILITY** (`1 - max(0, 2*(detection_rate - 0.5))`).
- Pairwise win-rate and AUTHORPRINT are **diagnostic only**, never averaged into one number.
- Corpus cap ~2.5–3k words held-out Dostoevsky; stop early when AUTHORPRINT margins are comfortable.
- Gate ranking: indistinguishability DESC, pairwise win-rate vs source as tie-break.
- ACCEPT iff human order **II > IV ≈ III > I** (II first and I last are hard).

## Constraints

- Judges: fresh context, `composer-2.5-fast`, blind, seeded A/B, results on disk (see [shared.md](shared.md)).
- Python modules under `src/eliotwf_skills/evaluator/`; thin CLIs under `.cursor/skills/evaluator/scripts/`.
- Subagents under `.cursor/agents/`.

## Phases (one session each)

| # | Session | Read first | Delivers |
|---|---------|------------|----------|
| 1 | [Corpus widen](phase-1-corpus.md) | `handoff/STATE.md`, [shared.md](shared.md) | `corpus/dostoevsky/*.txt`, `corpus-fetch.md`, margins.json |
| 2 | [AUTHORPRINT wire](phase-2-authorprint.md) | phase 1 output, `authorprint.py` | `authorprint_v2.py`, 0–100 mapping, tests |
| 3 | [Discrimination](phase-3-discrimination.md) | `pairwise.py` (mirror pattern) | `discrimination.py`, `discriminate.md`, `discrimination_v2.py`, tests |
| 4 | [Validation gate](phase-4-gate.md) | blind-read packet + answer-key | `gate_v2.py`, ranking unit tests |
| 5 | [Smoke + ship](phase-5-smoke.md) | all prior CLIs | real judges, gate ACCEPT, `SCORER-V2-PASSED.md` |

Run in order. Each phase ends green before the next starts.

## Verification (every phase)

```powershell
cd C:\Projects\EliotWF
$env:PYTHONPATH="src"
python -m unittest discover -s tests -q
```

Test count must grow or hold; never shrink below 66 until phase 3+ adds discrimination tests.

## Implementation guidance

- `/poteto-mode` with subagent dispatch for corpus fetch and judge smoke only.
- Mirror Phase 3 shapes (`ComparisonJob` → `DiscriminationTrial`; `pairwise_v2.py` → `discrimination_v2.py`).
- On gate fail: log to `tools/runs/scorer-v2/findings.md`; do not half-adopt.
