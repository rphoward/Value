# Phase 00 — Gaming regression harness

Back-link: [overview.md](overview.md)

## Goal

Prove the Goodhart failure is measurable before changing accept. A fixture must show qualitative mean can rise while pairwise-vs-best would reject (or the reverse). Land red, then later phases turn it green.

## Changes

- Add a small pytest fixture under `tests/` with two draft score packages plus a pairwise outcome that disagrees with mean ranking.
- Document the intended AcceptDecision predicate the fixture asserts once phase 03 lands.
- Do not change production accept yet.

## Data structures

- Fixture scores + preference outcome only. No new production types yet.

## Verification

- Static: new test fails (or xfail with explicit redesign marker) until phase 03/04.
- Runtime: N/A (fixture-only).

## Principles

**Prove It Works**, **Sequence Verifiable Units**.
