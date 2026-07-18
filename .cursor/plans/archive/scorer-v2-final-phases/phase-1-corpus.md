# Phase 1 — Corpus widen

Back to [overview](overview.md). Shared: [shared.md](shared.md).

## Goal

Pull held-out Dostoevsky (and optional Rilke top-up) into `tools/runs/scorer-v2/corpus/`, re-measure AUTHORPRINT margins, stop when comfortable. No Python scoring code yet beyond a margin check script or inline probe.

## Changes

| File | Change |
|------|--------|
| `.cursor/agents/corpus-fetch.md` | New readonly subagent; exa MCP; returns paths + word counts only |
| `tools/runs/scorer-v2/corpus/dostoevsky/*.txt` | Garnett Grand Inquisitor continuation; NOT source-excerpt |
| `tools/runs/scorer-v2/corpus/rilke/*.txt` | Optional top-up toward parity |
| `tools/runs/scorer-v2/authorprint/margins.json` | Record margin after each chunk |
| `tests/test_scorer_v2.py` | Repoint `DOSTOEVSKY_CORPUS_PATH` to widened corpus |

## Data structures

`margins.json`: `{dost_to_dost, dost_to_rilke, rilke_to_rilke, rilke_to_dost, word_counts, timestamp}` per measurement.

## Verification

- Dostoevsky total words in 2500–3000 cap (or stop early on margin).
- Both-direction margins positive in `margins.json`.
- `AuthorprintTests` still pass with new corpus path.
- Suite still 66+ OK.

## Paste into new chat

```text
/poteto-mode Phase 1 of scorer v2 final phases.

Read in order:
1. handoff/STATE.md
2. .cursor/plans/archive/scorer-v2-final-phases/overview.md
3. .cursor/plans/archive/scorer-v2-final-phases/shared.md
4. .cursor/plans/archive/scorer-v2-final-phases/phase-1-corpus.md (this file)

Do NOT touch the frozen style block, ELIOT skill, v1/v2 scorer, or EvaluatorScore.

Task: Ship corpus widen only.
- Create .cursor/agents/corpus-fetch.md (readonly, exa MCP).
- Delegate corpus-fetch subagent using the paste-in prompt in shared.md.
- Write chunks to tools/runs/scorer-v2/corpus/dostoevsky/*.txt; cap ~2500-3000 words.
- Record margins in tools/runs/scorer-v2/authorprint/margins.json after each chunk; stop early when both directions are comfortably positive.
- Repoint DOSTOEVSKY_CORPUS_PATH in tests/test_scorer_v2.py to the widened corpus.
- Run: $env:PYTHONPATH="src"; python -m unittest discover -s tests -q

Stop when phase 1 verification passes. Do not start AUTHORPRINT wiring or discrimination.
```
