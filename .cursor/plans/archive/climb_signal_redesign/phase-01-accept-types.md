# Phase 01 — Accept domain types

Back-link: [overview.md](overview.md)

## Goal

Encode climb accept in structures, not scattered mean comparisons. Name the types later phases fill in.

## Changes

- Add pure core types for `AcceptDecision`, `PatchScope`, and `HardVeto` (names may match repo tone).
- Keep them Path-free under `eliotapp/core/`.
- Application compose stays empty or thin wrappers only. No behavior change to `_best_record` yet.

## Data structures

- `AcceptDecision`: status, reason codes, incumbent draft id, challenger draft id, optional held-out flag.
- `PatchScope`: kind (whole | axis | excerpt), target axes, optional span markers.
- `HardVeto`: which floor failed; content-brief hash fail.

## Verification

- Static: unit tests construct/round-trip types; full suite still green.
- Runtime: N/A.

## Principles

**Model the Domain**, **Foundational Thinking**.
