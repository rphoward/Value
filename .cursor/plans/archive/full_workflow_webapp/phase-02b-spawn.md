# Phase 02b — Spawn + import fix

Back-link: [overview.md](overview.md)

## Goal

Subprocess spawn of `sdk-climb.py` with locator-aligned `--runs-base`. Fix `open_preference_job` missing import. Fixture tests prove spawn path without dual-writing scores from HTTP.

## Changes

- Job runner spawns SDK climb subprocess for `improve`
- Align `--runs-base` with `WorkProductLocator`
- Fix `open_preference_job` import in `tools/sdk-climb.py`
- Extend fixture tests

## Data structures

- Runner binds generation id + input revision from `JobRequest`
- Per-run ledger records spawn / exit events

## Verification

**Static.** Pytest for import fix + spawn dry/fixture path.

**Runtime.** Optional smoke: enqueue improve on fixture; ledger shows spawn; only SDK touches `scores.json`.
