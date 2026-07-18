---
name: One-command hillclimb automation
overview: Turn the manual hillclimb run into a single chat command (/hillclimb) with friendly progress reporting, accepting source texts from outside the repo, built on the existing loop.py engine so the future web UI can reuse it.
todos:
  - id: prepare-module
    content: Build prepare.py intake (external source copy, validation, calibration) + CLI subcommand
    status: completed
  - id: prepare-tests
    content: Add tests/test_prepare.py for intake validation and overwrite guard
    status: completed
  - id: command-skill
    content: Create /hillclimb command file and one-command session protocol in workflow skill (resume, score-only, auto slug/topic)
    status: completed
  - id: dry-run
    content: "End-to-end dry run: /hillclimb on the Rilke source, verify scoreboard and results card"
    status: completed
  - id: app-seam
    content: Add application/hillclimb_runs.py list_runs/run_detail read seam + tests
    status: completed
  - id: handoff
    content: Update handoff/STATE.md with the new automation entry
    status: completed
isProject: false
---

# One-command hillclimb from chat

**Status:** shipped 2026-07-07 — see `.cursor/commands/hillclimb.md` and workflow protocol-7.

## What you get

You type one line in chat — e.g.

```
/hillclimb C:\Downloads\needham-rilke.txt
```

and the agent does everything you watched me do by hand: copy the source in, build the Dense Style Block, self-calibrate the scorer, run the emulate → eval → record loop, and finish with a scoreboard and the best draft. External files, URLs, or pasted text all work as the source. Per-iteration progress shows in chat as a compact scoreboard (total, delta, two weakest axes, verdict).

## How it fits what exists

- Engine stays in Python: `src/eliotwf_skills/workflow/loop.py` (init_run, record_iteration, run_status, append_decision) is untouched and already tested.
- Subagents stay as-is: `.cursor/agents/emulate-drafter.md` and `eval-audit.md` do drafts and qualitative scoring, exactly like today.
- Persistence stays file-based per `docs/adr/001-run-persistence.md` — one new file per run (`source.txt`, `calibration.json`) inside the same `tools/runs/<slug>/` layout.
- The future web UI wraps the same `prepare`/`record`/`status` functions through an application use case; no decision on a web LLM engine is needed now.

## Pieces to build

### 1. `prepare` step — external source intake (Python)

New module `src/eliotwf_skills/workflow/prepare.py` + a `prepare` subcommand on `.cursor/skills/workflow/scripts/hillclimb_once.py`:

- Input: `--source <path>` (any absolute path, inside or outside the repo) or stdin text. URL fetching stays agent-side (Exa) — the agent saves fetched text to a temp file and passes the path.
- Validates: nonempty, plausible prose length (>= ~800 words for calibration), UTF-8.
- Writes into the run folder: `source.txt` (canonical copy) and `calibration.json` (via existing `evaluator/calibration.py`).
- One-eyed safety: refuses to overwrite an existing run unless `--force` (same guard as `init`).

### 2. `/hillclimb` command + skill upgrade

- `.cursor/commands/hillclimb.md` — the trigger. Takes freeform args: source (path/URL/pasted), optional `slug`, `topic`, `iterations` (default 3), `min-delta` (default 1.5).
- Workflow skill (`.cursor/skills/workflow/SKILL.md`) gains a "one-command session" protocol:
  1. Resolve source (external path → prepare; URL → Exa fetch → temp file → prepare; pasted text → temp file → prepare).
  2. Build Dense Style Block from `source.txt` using the ELIOT skill (this was manual before). If a topic isn't given, derive one from the source and confirm it in one line — the only question the flow ever asks.
  3. `init` → loop: spawn `emulate-drafter` → spawn `eval-audit` → `record` → `decision`. After each iteration print the scoreboard line.
  4. Finish with a results card: best draft, per-iteration table, score_v2 totals vs calibration, and paths.

### 3. Smoothness and flexibility (the pizazz)

- **Resume:** `/hillclimb resume <slug>` — reads `run_status()`, continues where it stopped (retry=true), or reports the final card if stopped.
- **Score-only:** `/hillclimb score <slug>` — re-emit the results card without running anything.
- **Sensible defaults everywhere:** slug auto-derived from source filename; topic auto-derived; 3 iterations; only ask when derivation is genuinely ambiguous.
- **Keep-best discipline:** retry briefs auto-target the two weakest qualitative axes from the last eval (this is what produced the +17 jump in the Rilke run); a regressing final iteration never overwrites the best-draft pointer.

### 4. Web-UI seam (thin, deferred wiring)

- `src/eliotwf/application/hillclimb_runs.py` — read-only use cases: `list_runs()`, `run_detail(slug)` over `tools/runs/` (scan `scores.json` files). This is all the web dashboard needs on day one, and it forces no LLM decision.
- Actual browser pages come with the Web UI phase (deliverable #3 in `handoff/STATE.md`), using the `tool-ui-htmx` skill.

## Tests

- `tests/test_prepare.py` — intake validation (empty, short, non-UTF8, overwrite guard, calibration written).
- Extend `tests/test_hillclimb.py` if record/status contracts grow.
- `list_runs`/`run_detail` get small fixture tests.

## Order of work

Prepare module → CLI subcommand → tests → command file + skill protocol → dry-run the whole flow on the Rilke source end-to-end → application read seam → update `handoff/STATE.md`.