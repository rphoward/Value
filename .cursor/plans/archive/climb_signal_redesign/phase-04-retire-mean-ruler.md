# Phase 04 — Retire mean as sole ruler

Back-link: [overview.md](overview.md)

## Goal

New runs default to pairwise-vs-best accept. Qualitative mean stops being sole best/seed/stop ruler. Migrate callers then delete dual-truth. ADR 003 kept as history; new ADR records the default.

## Changes

- `init_run` default climb metric → new pairwise-vs-best id.
- `_best_record`, seed promotion, early-stop / retry projection migrate for that id.
- `decision.tsv` tracks accept reasons aligned with pairwise, not total/mean delta alone.
- Climb strip may keep plotting qualitative mean as a *diagnostic* sparkline, labeled as diagnostic, not “the climb signal.”
- Legacy `style_fidelity` / `indistinguishability` / `reference_preference_v1` remain readable for old folders.

## Data structures

- No dual accept rule on one run. One climb_metric, one ruler.

## Verification

- Static: phase-00 harness green; tests that mean-up / pairwise-reject cannot become best under new default.
- Runtime: dogfood init on a throwaway slug; inspect shows pairwise next_actions.

## Principles

**Migrate Callers Then Delete Legacy APIs**, **Outcome-Oriented Execution**, **Subtract Before You Add**.
