# Phase 06 — Multi-objective ε-band

Back-link: [overview.md](overview.md)

## Goal

Accept when the target improves and non-target qualitative axes stay within ε of the incumbent, subject to hard vetoes. Stops single-axis ornament gaming.

## Changes

- After pairwise preference (or as part of AcceptDecision), compare non-target axis scores incumbent vs challenger.
- Reject when non-target drop exceeds ε even if pairwise soft-wins (policy choice: ε veto after pairwise, or soft signal into craft brief only — prefer hard ε for the named target axis set).
- Record ε failures as accept reasons.

## Data structures

- ε config on run init or HillclimbConfig. Per-axis deltas on AcceptDecision.

## Verification

- Static: fixture where target axis ↑, neighbor axes crash → reject.
- Runtime: CLI climb step prints/logs ε reject reason.

## Principles

**Fix Root Causes** (ornament gaming), **Prove It Works**.
