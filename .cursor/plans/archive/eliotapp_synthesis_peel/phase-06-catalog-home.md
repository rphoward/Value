# Phase 06 — Catalog home + UI copy

Back-link: [overview.md](overview.md)

## Goal

`workproduct/catalog.json` is the locked catalog home. UI copy no longer claims `tools/runs/` as the only home.

## Changes

- Ensure catalog writes/reads prefer `workproduct/catalog.json` via locator. Today neither that file nor `sources/catalog.json` exists on disk; create the locked home and point writers there.
- Shrink dual-read of legacy catalog paths to the shortest safe window; document remaining fallback in locator only.
- Update templates that still hardcode `tools/runs/` (`wizard.html`, `_done_stub.html`, `runs/index.html`, others found by grep). Note: live run trees still sit under `tools/runs/`; `workproduct/runs/` is essentially empty. Dual-read stays until a deliberate migrate of run dirs (out of band unless this phase explicitly moves a pilot set).
- Skill/CLI help that still teaches `tools/runs/<slug>` as canonical should match the locator story (can share work with phase 00 prose scrub if already done).

## Data structures

Catalog JSON schema unchanged. Locator `catalog_path()` is the single resolver.

## Verification

**Static.** Pytest catalog_store / pipeline wizard. Grep templates for stale `tools/runs` copy.

**Runtime.** TestClient or `control-ui`: GET `/` and wizard surfaces show workproduct-oriented paths; catalog load still works under dual-read if legacy file remains.
