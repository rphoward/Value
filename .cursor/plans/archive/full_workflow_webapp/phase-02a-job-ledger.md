# Phase 02a — Job ledger types

Back-link: [overview.md](overview.md)

## Goal

Typed job request and driver ledger with atomic one-job-per-slug store under the run. No subprocess yet.

## Changes

- Application types: `JobRequest`, `DriverLedger` (and event append helper)
- Per-run store: job request file + `driver/events.jsonl`
- Atomic reject when a non-terminal job already exists
- Unit tests for enqueue / reject / terminal transition

## Data structures

- `JobRequest`: kind (`distill` | `analyze` | `write_seeds` | `improve`), status, generation id, input revision, timestamps
- `DriverLedger`: append-only events under the run
- Store ownership: HTTP writes job + ledger only; never `scores.json`

## Verification

**Static.** Pytest for atomic one-job invariant and ledger append.

**Runtime.** n/a until spawn (2b).
