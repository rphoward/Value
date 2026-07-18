# Phase 02 — Hard veto floors

Back-link: [overview.md](overview.md)

## Goal

Python SURFACE/PROSODY/CAST and content-brief become climb vetoes. Soft qualitative judge cannot override a veto.

## Changes

- Plug veto into CLI/SDK record/accept path (`climb_recording` / post-record accept), not HTTP.
- Content-brief hash already blocks draft inputs; extend so a failed coverage/hash state cannot become climb-best.
- Deterministic floors today are diagnostic/tie-break only under ADR 003. Change that for the new accept path.
- Leave Canvas read-only.
- Optional reuse later: `eliotapp/core/evaluator/quality_veto.py` (finalist blind incumbent-vs-candidate) as a pattern, not a day-one dependency.

## Data structures

- Use `HardVeto` from phase 01. Persist veto reason on the iteration or decision log (`decision.tsv`).

## Verification

- Static: tests that a rising qualitative mean still loses when CAST (or content-brief) vetoes.
- Runtime: `control-cli` record path on a fixture run shows veto reason on disk.

## Principles

**Boundary Discipline**, **Prove It Works**.
