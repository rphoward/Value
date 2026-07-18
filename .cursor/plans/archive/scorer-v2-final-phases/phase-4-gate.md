# Phase 4 — Validation gate harness

Back to [overview](overview.md). Prerequisite: [phase-3-discrimination.md](phase-3-discrimination.md) done.

## Goal

CLI that ranks the four blind-read samples using the full v2 diagnostic stack. Unit-test the ranking math with fixture verdicts. No live judges in this session.

## Changes

| File | Change |
|------|--------|
| `src/eliotwf_skills/evaluator/gate.py` | Ranking logic, ACCEPT criteria, sample report shape |
| `.cursor/skills/evaluator/scripts/gate_v2.py` | Orchestrate score_v2 + ingest prepared pairwise/discrimination JSON |
| `tests/test_scorer_v2.py` | Gate ranking unit tests with fixture inputs |

## Data structures

- `SampleReport`: per-sample `indistinguishability`, `pairwise_mean`, `authorprint_score`, `deterministic_axes`.
- `GateResult`: `ranking: list[str]`, `accept: bool`, `reason: str`, `reports: dict[str, SampleReport]`.

ACCEPT iff order II > IV ≈ III > I (II first, I last hard); source deterministic axes >= 95.

## Verification

- `gate_v2.py` dry-run with fixture verdicts reproduces expected ranking math.
- Deterministic axes for source excerpt still >= 95.
- Suite green; ruff clean.
- No real subagent calls in this phase.

## Paste into new chat

```text
/poteto-mode Phase 4 of scorer v2 final phases (gate harness only).

Read in order:
1. .cursor/plans/archive/scorer-v2-final-phases/phase-4-gate.md (this file)
2. .cursor/plans/archive/scorer-v2-final-phases/shared.md (ranking rules)
3. tools/runs/emulation-ceiling/blind-read/packet.md and answer-key.md
4. Existing CLIs: score_v2.py, pairwise_v2.py, discrimination_v2.py, authorprint_v2.py

Prerequisites: phases 1-3 shipped (corpus, authorprint_v2, discrimination_v2).

Do NOT dispatch real judges in this session. Use fixture/mock verdict JSON only.

Task: Ship gate_v2.py harness + ranking unit tests.
- gate.py: SampleReport, GateResult, rank_samples (indist-led, pairwise tie-break).
- gate_v2.py CLI: ingest per-sample diagnostic JSON, emit results.json + ranking.json.
- Tests: ranking order with fixture inputs; ACCEPT/REJECT edge cases.
- Run: $env:PYTHONPATH="src"; python -m unittest discover -s tests -q

Stop when phase 4 verification passes. Live judge smoke is phase 5.
```
