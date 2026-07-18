# Phase 03 — Read-only Document Canvas

Back-link: [overview.md](overview.md)

## Goal

Workspace shell: ArtifactTree + ActiveDoc + empty JobRail from disk. HTMX center swap. Works without `scores.json`.

## Changes

- Redesign `GET /runs/{slug}` toward canvas layout (not tabs-only)
- Left tree from run artifacts; center doc swap; right empty rail
- Application helpers for tree/doc models (thin)

## Data structures

- `ArtifactTree` / `ArtifactNode` / `ActiveDoc` / `JobRail` (rail may be empty)

## Verification

**Static.** Presentation pytest for canvas render without scores.

**Runtime.** control-ui: open a run, click tree nodes, center swaps.
