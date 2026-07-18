# Phase 5 — SDK climb driver

Back-link: [overview.md](overview.md)

## Goal

Ship a thin unattended entrypoint that runs the same protocol-7 resume/loop the chat command uses, exiting on filesystem truth (`scores.json` + job board), not chat memory. **Blocked on phase 4 go (option A or B).** If phase 4 chose C, skip this phase.

## Changes

- Add `tools/sdk-climb.py` (repo `tools/`, not product home).
- Optional dep: document `pip install cursor-sdk` (or `pyproject` optional extra). Never import from `src/eliotwf`.
- Requires `CURSOR_API_KEY`.
- Args: `--slug <slug> [--mode climb|resume] [--init-if-missing] [--topic TEXT] [--model <id>] [--cwd repo-root]`
  - `climb` (default): start or continue protocol-2 until stop
  - `resume`: alias for `climb` (same resume order); kept for docs compatibility
  - `--init-if-missing`: when `scores.json` absent but `style-block.md` + `source.txt` exist, run `hillclimb_once init` using `--topic` or `discovery.json` → `topic` field
  - Refuse with clear error if `style-block.md` or topic missing (driver does not replace analyze/distiller)

**Init handoff (closes wizard gap)**

```text
prepare (wizard) → source.txt + calibration.json
analyze (wizard) → style-block.md
sdk-climb --init-if-missing → hillclimb_once init → scores.json shell
sdk-climb → protocol-2 loop
```

- Preflight (no API): verify run dir, topic resolution, prompt assembly, exit-code mapping.
- Build one protocol-7 prompt that includes the phase-3 resume order (including seed-round rules) and forbids inventing scorers.
- **Agent invocation:** Per spike outcome — cloud `Agent.create` with subagents **or** local multi-turn `send`/`resume`. Do not assume `Agent.prompt()` one-shot is sufficient.
- Print final `run_status()` JSON to stdout on exit 0.
- Add `tests/test_sdk_climb_preflight.py` (prompt assembly + missing-key / missing-slug / init-if-missing / exit-code mapping). No live API in CI.

**Exit codes (fixed)**

| Code | Meaning |
|------|---------|
| 0 | `run_status()["stopped"]` is true, **or** `retry` is false after at least one iteration with recorded discrimination |
| 1 | Preflight failure (missing run dir, topic, style-block, API key) |
| 2 | Agent run ended in error (`result.status === error`) |
| 3 | Agent finished but climb incomplete (`retry` true and not stopped, or zero iterations) |

## Data structures

Driver config is a small argparse namespace. Prompt is assembled from slug + mode + absolute run path. Exit codes above are the public contract.

## Verification

**Static.** Preflight tests green without `cursor-sdk` installed (mock or skip-import path). Assert exit-code mapping for the four cases. Full suite still green.

**Runtime.** Via `control-cli` (manual, cost-gated): `python tools/sdk-climb.py --slug <prepared> --init-if-missing` (or `--mode resume` when already inited). Interrupt mid-discrimination once; confirm `discrimination-job-vN.json` shows pending; second invoke finishes remaining trials; process exits 0 with ≥1 recorded discrimination.
