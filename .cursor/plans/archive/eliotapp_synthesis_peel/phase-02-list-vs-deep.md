# Phase 02 — List vs deep

Back-link: [overview.md](overview.md)

## Goal

Dashboard list stays cheap. Deep snapshot loads once for decisions.

## Changes

- Add or formalize a cheap `RunCard` (or project `IndexedRun` into that role) for list endpoints.
- Deep path uses full `InspectedRun` / snapshot from phase 01.
- `run_status` becomes a projection over loaded facts, not a second filesystem crawler where avoidable.
- Touch `eliotapp/application/run_index.py` and callers that force full inspect per row.

## Data structures

- `RunCard`: slug + cheap status fields for index rows.
- Keep deep snapshot distinct from the card.

## Verification

**Static.** Pytest for run_index / presentation runs list.

**Runtime.** `control-ui` or TestClient: GET `/` or runs index lists without loading full inspect per row (assert via existing tests or a focused unit test on the list path).
