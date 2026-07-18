# Phase 04 — Path peel from core

Back-link: [overview.md](overview.md)

## Goal

`eliotapp/core/` has no `Path` I/O. File load/write lives in infrastructure (or thin application compose).

## Changes

Move Path helpers out of (handoff list):

- `eliotapp/core/eliot/scorecard.py`
- `eliotapp/core/distiller/style_blocks.py`
- `eliotapp/core/evaluator/calibration.py`
- `eliotapp/core/evaluator/cast_aliases.py`
- `eliotapp/core/evaluator/content_adherence.py`

Leave pure parsing/math in core. Callers that need files go through store or infra adapters.

## Data structures

Keep domain result types in core. Infra functions take `Path` at the boundary only.

## Verification

**Static.** Grep `pathlib` / `Path` under `eliotapp/core/` is empty (or limited to type-only if unavoidable; prefer empty). Pytest for scorecard, style blocks, calibration, aliases, content adherence.

**Runtime.** Score or style-block write path still produces the same on-disk artifact for a fixture run.
