# Phase 05 — Locator authority in presentation

Back-link: [overview.md](overview.md)

## Goal

Routes never invent dual-read path math. They call `WorkProductLocator.resolve_run_dir` / `iter_run_dirs` (or store wrappers) only.

## Changes

- Delete or collapse `_extra_run_bases` / `_resolve_run_dir` in `eliotapp/presentation/routes/runs.py`.
- Keep test injection via bound locator on app state / request state (already started in `app.py`).
- Presentation `paths.py` stays a thin locator facade if useful; no second oracle.

## Data structures

Reuse `WorkProductLocator`. No parallel base-tuple helpers in routes.

## Verification

**Static.** Pytest presentation runs. Grep routes for `tools/runs` path joins outside locator.

**Runtime.** TestClient or `control-ui`: GET runs index and one run detail still resolve legacy `tools/runs` via locator dual-read.
