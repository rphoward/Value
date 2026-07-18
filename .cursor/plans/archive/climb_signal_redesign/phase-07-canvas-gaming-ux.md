# Phase 07 — Canvas anti-gaming UX

Back-link: [overview.md](overview.md)

## Goal

Operator sees patch scope, accept reason, and pairwise keep-best without HTTP writing scores. Revert remains CLI/SDK or a control/job signal that does not mutate scores from presentation.

## Changes

- JobRail story reads latest `preference_outcome`, `decision.tsv` verdict/note, and PatchScope.
- Climb strip tooltips or labels distinguish diagnostic mean from accept outcome.
- Artifact tree surfaces preference sidecars and decision.tsv as first-class opens.
- Pick-best stays human override. No new scores writers in presentation.

## Data structures

- Read-only view models in `workspace_canvas` / climb strip. No new scores schema required beyond what phases 03–06 already write.

## Verification

- Static: `tests/test_workspace_canvas.py`, `tests/test_climb_strip.py`, `tests/test_presentation_runs.py` assert no scores touch.
- Runtime: `control-ui` smoke GET `/runs/<slug>` shows accept reason copy.

## Principles

**Experience First**, **Boundary Discipline**.
