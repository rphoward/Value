# Phase 06a — Analyze job

Back-link: [overview.md](overview.md)

## Goal

Analyze job kind on the same queue protocol. Paste/upload fallback remains.

## Changes

- Queue kind `analyze` on existing job store/runner
- Wire analyze driver or existing analyze path as subprocess/worker
- Keep paste/upload path as fallback

## Data structures

- Same `JobRequest` with kind `analyze`

## Verification

**Static.** Pytest for analyze enqueue + terminal.

**Runtime.** control-ui: queue analyze; style block appears or paste fallback still works.
