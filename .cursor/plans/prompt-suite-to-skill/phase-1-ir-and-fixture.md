# Phase 1. IR and golden fixture

Back-link: [overview.md](./overview.md)

## Goal

Define the prompt-suite intermediate representation and freeze `value` as the conformance fixture so later phases have a measurable target.

## Changes

- Add `tools/prompt-suite-compile/schema/prompt-suite.ir.schema.json` describing parsed suite shape (metadata, kb, orchestrator doctrines, modules[], cards[]).
- Add `tools/prompt-suite-compile/fixtures/value/` with pointers to `docs/value-proposition-prompt-suite (1).md` and expected digest allowlist for `skills/value/` (paths that may differ intentionally listed).
- Document the input markdown contract (required headings) in `tools/prompt-suite-compile/README.md`.

## Data structures

- `PromptSuiteIR`. Top-level object with `system_metadata`, `knowledge_base`, `orchestrator`, `modules[]` (each with `id`, `title`, `prompt_markdown`, `structural_requirements[]`).
- `FixtureManifest`. Source path, skill slug, allowed_delta_globs.

## Verification

**Static.** Schema validates sample IR JSON. Manifest paths exist.

**Runtime.** `python tools/prompt-suite-compile/validate_fixture.py value` exits 0.
