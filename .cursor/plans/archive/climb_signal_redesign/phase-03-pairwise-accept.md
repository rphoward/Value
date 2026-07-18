# Phase 03 — Pairwise candidate-vs-best accept

Back-link: [overview.md](overview.md)

## Goal

Climb accept becomes pairwise challenger vs current-best. Reuse the preference job board spine (ab/ba, incumbent/challenger). Style-block is the constitution in the judge framing. Qualitative scores feed craft briefs only on this path.

## Changes

- Wire candidate draft vs `best_draft` / incumbent through preference open→score→record (or a thin fork that shares `aggregate_pair`).
- Progression `decide` must allow preference jobs on the new climb metric (today preference on `style_fidelity` is repair).
- Today every `record_iteration` appends. Pairwise accept must add challenger-lost / rejected semantics so history can keep the draft file while `_best_record` ignores losers.
- Style-block is the constitution. Do not require held-out reference windows for the default accept path (that stays `reference_preference_v1` / phase 08).
- Judge family stays ≠ drafter; keep position swap.
- Turn phase-00 harness green for pairwise-vs-mean disagreement.
- Do not yet delete mean-based `_best_record` for old metric ids (phase 04).

## Data structures

- `AcceptDecision` filled from preference outcome.
- Metric id for the new default (see overview open question). Init path starts writing it on new runs only until phase 04.

## Verification

- Static: extend `tests/test_hillclimb.py` / preference smoke for challenger-vs-best under the new metric.
- Runtime: CLI pref-job chain on a fixture; `scores.json` shows `preference_outcome`; HTTP still unread-write for scores.

## Principles

**Laziness Protocol** (reuse pref board), **Redesign from First Principles**, **Separate Before Serializing Shared State** (SDK sole writer).
