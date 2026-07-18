# Phase 06b — Invent / write_seeds job

Back-link: [overview.md](overview.md)

## Goal

Invent / `write_seeds` job kind. Forbid `scores.json` until explicit climb start.

## Changes

- Queue kind `write_seeds` / invent
- Guard: no scores creation until improve/climb starts
- Seeds land as drafts in the tree

## Data structures

- Same `JobRequest` with kind `write_seeds`

## Verification

**Static.** Pytest that invent does not create scores; climb start may.

**Runtime.** control-ui: invent seeds → drafts in tree; no scores until Improve.
