# Phase 08 — Held-out anti-cheat

Back-link: [overview.md](overview.md)

## Goal

Periodic prefer-vs-held-out author text as anti-cheat, not only vs prior self. Same AcceptDecision rule family.

## Changes

- Optional cadence (every N accepts or on operator request) opens a preference (or discrimination) check against `held-out.txt`.
- Failures surface as veto or repair, not as a new scalar climb metric.
- Reuse held-out gate + genuine path resolution already shipped.

## Data structures

- AcceptDecision flag `vs_held_out`. No separate climb_metric.

## Verification

- Static: fixture with held-out preference fail blocks best promotion.
- Runtime: CLI path on a run that already has held-out attached.

## Principles

**Laziness Protocol** (reuse held-out + pref), **Prove It Works**.
