# Shared reference (all phases)

Back to [overview](overview.md).

## Frozen (do not touch)

Style block, ELIOT skill, v1 scorer, `EvaluatorScore`, `score_draft_v2.py` deterministic axes.

## Current state

- Phase 3: `pairwise.py`, `pair-judge.md`, `pairwise_v2.py` — 66 tests green.
- Scoring source: `tools/runs/emulation-ceiling/source-excerpt.md` (Sample II).
- Gate fixtures: `tools/runs/emulation-ceiling/blind-read/packet.md`, `answer-key.md`.
- Human order: II > IV > III > I.
- Cruft to remove in phase 5: `tools/runs/scorer-v2/rilke/_phase3-smoke/`.

## Artifact tree

```
tools/runs/scorer-v2/
├── corpus/dostoevsky/*.txt     # phase 1
├── corpus/rilke/               # existing + optional top-up
├── authorprint/margins.json    # phase 1–2
├── discrimination/             # phase 3–5
├── pairwise/                   # phase 5 smoke
├── gate/results.json           # phase 4–5
└── findings.md                 # on gate fail only
```

## Fixture migration (after phase 1)

`tests/test_scorer_v2.py` sets `DOSTOEVSKY_CORPUS_PATH` to `.cursor/skills/eliot/assets/dostoevsky-source.txt`. Point it at `tools/runs/scorer-v2/corpus/dostoevsky/` after widen. Do not edit the ELIOT asset file.

## Subagent defaults

Every `Task` call: `subagent_type: "poteto-agent"`, `model: "composer-2.5-fast"`, `run_in_background: true`. Parent reads summaries only; scores come from CLIs on disk.

## Dispatch prompts

### corpus-fetch

```
Full Repository Path: C:\Projects\EliotWF
Task: Pull held-out Dostoevsky corpus for scorer v2 AUTHORPRINT.
- Use exa MCP to fetch public-domain Garnett Brothers Karamazov (Grand Inquisitor continuation). Do NOT overlap tools/runs/emulation-ceiling/source-excerpt.md.
- Write chunks to tools/runs/scorer-v2/corpus/dostoevsky/*.txt. Cap ~2500-3000 words total Dostoevsky.
- Optionally top up tools/runs/scorer-v2/corpus/rilke/*.txt toward parity.
- Return ONLY: {"paths": [...], "word_counts": {...}, "total_dost_words": N}. No inlined passage text.
subagent_type: poteto-agent, model: composer-2.5-fast, run_in_background: true
```

### pair-judge (one job)

```
Read .cursor/agents/pair-judge.md. Judge this blind comparison only.
passage_a: <from jobs.json blind view>
passage_b: <from jobs.json blind view>
question: <axis question from jobs.json>
Return JSON: {"job_id": "<id>", "winner": "A"|"B", "evidence": "one sentence"}
subagent_type: poteto-agent, model: composer-2.5-fast, run_in_background: true, readonly: true
```

### discriminate (one trial)

```
Read .cursor/agents/discriminate.md. Spot-the-real-one trial only.
trial_id: <from trials.json>
passage_a: <from blind trial>
passage_b: <from blind trial>
Return JSON: {"trial_id": "<id>", "genuine": "A"|"B", "tell": "one sentence"}
subagent_type: poteto-agent, model: composer-2.5-fast, run_in_background: true, readonly: true
```

## gate_v2.py ranking (locked)

Per sample: `indistinguishability` (headline), `pairwise_win_rate_vs_source` (tie-break), `authorprint_score` and `deterministic_axes` (diagnostic). Sort indist DESC, then pairwise DESC.
