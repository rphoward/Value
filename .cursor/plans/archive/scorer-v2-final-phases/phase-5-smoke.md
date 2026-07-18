# Phase 5 — Smoke + ship

Back to [overview](overview.md). Prerequisite: [phase-4-gate.md](phase-4-gate.md) done.

## Goal

Run real pair-judge and discriminate subagents over the four samples, aggregate via CLIs, drive the gate. On ACCEPT write `SCORER-V2-PASSED.md`. On fail log `findings.md`.

## Changes

| File | Change |
|------|--------|
| `tools/runs/scorer-v2/pairwise/*` | Jobs + verdicts per sample |
| `tools/runs/scorer-v2/discrimination/*` | Trials + verdicts + tells per sample |
| `tools/runs/scorer-v2/gate/results.json` | Full diagnostic report |
| `handoff/SCORER-V2-PASSED.md` | On gate pass |
| `handoff/STATE.md` | Mark phases 4–5 done |
| `tools/runs/scorer-v2/findings.md` | On gate fail only |

Cleanup: remove `tools/runs/scorer-v2/rilke/_phase3-smoke/`.

## Session flow

0. Phase 4 carryover checks (even if not listed below):
   - `gate_v2.py dry-run` ACCEPT with fixture ranking II > IV > III > I
   - `score_v2.py` on source-excerpt: every deterministic axis >= 95
   - `python -m unittest discover -s tests -q` green; ruff clean on touched modules
1. `python tools/runs/scorer-v2/run_phase5_smoke.py verify` then `prepare`
2. Rilke draft vs source pairwise sanity (Phase 3 regression). 25 pair-judge jobs.
3. For each blind-read sample I–IV: `pairwise_v2.py prepare` → dispatch pair-judge jobs in background → write `pairwise/<ID>/verdicts/*.json` → `score`
4. For each sample: `discrimination_v2.py prepare` with `--genuine corpus/dostoevsky/held-out.txt` (never source-excerpt) → dispatch discriminate trials → `score`; log `tells.json`
5. Run `authorprint_v2.py score` per sample (deterministic; manifest needs it)
6. Run `python tools/runs/scorer-v2/run_phase5_smoke.py aggregate` (or `gate_v2.py run` directly)
7. ACCEPT → `SCORER-V2-PASSED.md` + STATE update. FAIL → `findings.md`.

Orchestrator: `tools/runs/scorer-v2/run_phase5_smoke.py`. Handoff paste block: `handoff/NEW-CHAT-PROMPT-SCORER-V2-PHASE5.md`.

## Verification

- All subagent verdicts on disk; parent context stayed lean.
- Gate ACCEPT reproduces II > IV ≈ III > I.
- Suite green; ruff clean; `_phase3-smoke/` removed.

## Paste into new chat

```text
/poteto-mode Phase 5 of scorer v2 final phases (smoke + ship).

Read in order:
1. .cursor/plans/archive/scorer-v2-final-phases/phase-5-smoke.md (this file)
2. .cursor/plans/archive/scorer-v2-final-phases/shared.md (dispatch prompts)
3. handoff/NEW-CHAT-PROMPT-SCORER-V2-PHASE5.md (orchestrator + phase-4 carryover)
4. handoff/STATE.md

Prerequisites: phases 1-4 all shipped. All CLIs exist and unit tests green.

Task: Full-package smoke only. No new scoring modules unless a bug blocks aggregation.
- Pairwise: Rilke sanity + four blind-read samples via pair-judge subagents (background, one job each).
- Discrimination: T trials per sample via discriminate subagents (background, one trial each).
- Aggregate with pairwise_v2.py score, discrimination_v2.py score, gate_v2.py.
- On ACCEPT: handoff/SCORER-V2-PASSED.md + update STATE.md.
- On FAIL: tools/runs/scorer-v2/findings.md (which sample broke order and why).
- Remove tools/runs/scorer-v2/rilke/_phase3-smoke/.
- Run: $env:PYTHONPATH="src"; python -m unittest discover -s tests -q

This is the ship gate. Do not half-adopt on fail.
```
