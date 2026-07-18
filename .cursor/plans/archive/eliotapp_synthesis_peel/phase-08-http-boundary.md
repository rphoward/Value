# Phase 08 — HTTP boundary (optional)

Back-link: [overview.md](overview.md)

## Goal

Enforce what behavior already intends: presentation must not import hillclimb writers.

## Changes

- Add import-linter (or project equivalent) contracts: `eliotapp.presentation` ↛ hillclimb write modules under application.
- Skip this phase if tooling cost exceeds value; handoff marks it a synthesis nicety.

## Data structures

None. Lint contracts only.

## Verification

**Static.** Lint contract fails if a route imports a forbidden writer. Pytest still green.

**Runtime.** None beyond existing GET-only smoke.
