# Phase 08 — Interrogate + ship

Back-link: [overview.md](overview.md)

## Goal

Adversarial review on job boundary. Update handoff / WORKFLOW / WEB-UI gate. Open PR and babysit.

## Changes

- **interrogate** on contested job-boundary (HTTP vs SDK writers)
- Handoff docs: WORKFLOW, STATE, any WEB-UI gate record
- `/deslop` + **unslop**; PR via opening-a-pr; **babysit**

## Data structures

None new.

## Verification

**Static.** Full pytest suite green.

**Runtime.** control-ui end-to-end against done predicate from overview.

**Ship.** PR URL; babysit until merge-ready or clear blockers.
