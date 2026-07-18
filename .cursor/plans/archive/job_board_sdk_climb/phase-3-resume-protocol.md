# Phase 3 — Resume-safe parent protocol

Back-link: [overview.md](overview.md)

## Goal

Make chat `/hillclimb resume` and the future SDK driver share one mandatory resume order that finishes mid-batch discrimination (including best-of-n seed jobs) before starting a new draft.

## Changes

- Update `.cursor/skills/workflow/SKILL.md` protocol-2 step-4 to require `job-*` instead of ad-hoc verdict file writes, including seed jobs.
- Update `.cursor/skills/workflow/references/one-command.md` resume rules + best-of-n job files (one job file per seed suffix; only winner is recorded into `scores.json`).
- Update `.cursor/commands/hillclimb.md` resume checklist.
- Use Cursor built-in **create-skill** habits when editing SKILL.md (progressive disclosure, no duplicate protocol text).

**Resume order (mandatory)**

1. `hillclimb_once.py status --run-dir tools/runs/<slug>`
2. `hillclimb_once.py job-status --run-dir tools/runs/<slug>`
3. If any job `in_progress` with pending trials → spawn only remaining `discriminate` Tasks → `job-trial` each → `job-score` → `job-record` (per job) → decision when all seed jobs done
4. Else if latest iteration has draft in `scores.json` but `indistinguishability` missing → `job-open` then full batch
5. Else if iter 1 seed drafts exist (`draft-v1a.md`, …) without winner recorded → resume seed discrimination jobs (step 3 per suffix)
6. Else if `retry` → revise from `best_draft` (unchanged)
7. Else results card

**Seed-round resume (iter 1, `seeds: 3`)**

1. `job-status` may list `discrimination-job-v1a.json`, `v1b`, `v1c` independently.
2. Finish pending trials on **each** open seed job before promoting a winner.
3. Only after all seed jobs are `recorded` (or scored and compared) → pick winner → single `hillclimb_once record` for `draft-v1.md`.
4. Loser drafts stay sidecars; their job files remain for audit but are not re-opened.

Parent still never inlines spot verdicts; still never edits scorer mid-run.

## Data structures

No new types. Protocol text must name `DiscriminationJob` statuses and seed-suffix jobs. `active_discrimination_job` / `job-status` may surface multiple non-terminal seed jobs.

## Verification

**Static.** Skill/docs mention `job-status` before new draft work; seed-round steps 1–4 present; grep for forbidden "write verdicts by hand" guidance removed or redirected.

**Runtime.** No new binary. Manual dry-read of `/hillclimb resume` checklist against a folder with a fake `in_progress` job and against three seed-suffix job files. Flag: control-cli N/A for docs-only phase.
