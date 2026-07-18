# Phase 07 — Pick best + UX polish

Back-link: [overview.md](overview.md)

## Goal

Best draft pick writes a human choice marker / `best-draft.md` copy. Empty/error/loading states per tool-ui-htmx. Cursor handoff is not the happy path.

## Changes

- Pick-best action (marker + copy; does not rewrite score history)
- Empty / error / loading polish on canvas rail and tree
- Soften Cursor-eject messaging to secondary path

## Data structures

- Best-draft marker / `best-draft.md` under the run

## Verification

**Static.** Pytest for pick-best marker.

**Runtime.** control-ui: pick best; marker visible; empty states teach next action.
