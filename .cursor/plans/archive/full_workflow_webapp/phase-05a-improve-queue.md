# Phase 05a — Improve queue + JobRail story

Back-link: [overview.md](overview.md)

## Goal

`POST` improve job + JobRail story poll mapped from `decide()`. No pause yet.

## Changes

- `POST /runs/{slug}/jobs` with kind `improve`
- JobRail HTMX poll showing human story headlines from `next_action`
- Atomic reject if non-terminal job exists

## Data structures

- JobRail story mapping from progression `decide()` / inspect

## Verification

**Static.** Route + job_runner pytest.

**Runtime.** control-ui: start improve on fixture; rail shows story; new draft appears when SDK finishes (or fixture stub).
