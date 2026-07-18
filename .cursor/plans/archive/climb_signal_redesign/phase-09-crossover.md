# Phase 09 — Crossover splice operator

Back-link: [overview.md](overview.md)

## Goal

Optional genetic merge of two drafts as a span-splice operator under the same pairwise accept. Not a new scalar.

## Changes

- CLI/SDK operator produces a spliced challenger draft from two parents.
- Challenger enters the same pairwise-vs-best + hard veto + ε path.
- Web exposure only if a new driver job kind is justified. Default is CLI-first.
- HTTP still never writes scores.

## Data structures

- Splice manifest (parent drafts, span map) beside the new draft file. AcceptDecision unchanged.

## Verification

- Static: splice → prefer job → accept/reject tests without live LLM where possible.
- Runtime: one dogfood splice on an existing multi-draft run.

## Principles

**Laziness Protocol**, **Experience First**, **Never Block on the Human** for reversible CLI spike.
