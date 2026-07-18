# Phase 2 — Job board CLI

Back-link: [overview.md](overview.md)

## Goal

Give the parent agent one CLI surface for discrimination progress so chat and the future driver never invent ad-hoc verdict writers.

## Changes

- Extend `.cursor/skills/workflow/scripts/hillclimb_once.py` with:
  - `job-open` — run prepare (or accept existing trials path) + write job file
  - `job-trial` — append one verdict; update completed/pending (idempotent on same trial_id)
  - `job-score` — refuse if pending; call existing `discrimination_v2.py score`; mark scored
  - `job-record` — call existing `record_discrimination`; mark recorded
  - `job-status` — print active job JSON (or empty) for resume
- Wire helpers from phase 1 only. Forbidden: a second scoring implementation.
- Extend `tests/test_hillclimb.py` (or thin CLI tests) for subcommand happy path + score-while-pending refusal.

## Data structures

Reuse `DiscriminationJob`. CLI args name `--run-dir`, `--iteration`, optional `--seed-suffix`, paths already used by prepare/score.

## Verification

**Static.** `pytest tests/test_job_board.py tests/test_hillclimb.py` green.

**Runtime.** Via `control-cli`: on a throwaway copy of a run folder (or tmp fixture), `job-open` → one `job-trial` → `job-status` shows pending reduced → `job-score` fails while pending remains.
