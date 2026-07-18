# Phase 05 — Excerpt / axis-local revise unit

Back-link: [overview.md](overview.md)

## Goal

One climb step targets one axis set or one excerpt set. Whole-draft revise stops being the only revise unit.

## Changes

- Extend craft-brief writer + revise-drafter contract with `PatchScope` fields (target axes and/or excerpt markers).
- Parent still writes the brief. Drafter still cannot read scores.json.
- Prefer local rewrites that stay inside scope. Output may remain a full `draft-vN.md` file with scoped intent recorded.
- SDK climb must author or require the scoped brief the same way it requires today's craft brief.
- Revisit even-iteration whole-draft PROSODY cadence pass in `one-command.md`. It conflicts with “only touch target axis” unless scoped or skipped when `PatchScope` is set.

## Data structures

- `PatchScope` on craft-brief metadata and/or `decision.tsv` `change` column.

## Verification

- Static: tests that scoped brief fields round-trip through `build_draft_inputs`.
- Runtime: one CLI revise step with axis-local brief; artifact shows scope on disk.

## Principles

**Experience First**, **Model the Domain**.
