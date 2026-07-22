# Phase 2. Mechanical extract and scaffold

Back-link: [overview.md](./overview.md)

## Goal

Ship a stdlib CLI that turns a conforming prompt-suite markdown file into a skill scaffold under a draft path without inventing atoms or voice.

## Changes

- Add `tools/prompt-suite-compile/compile.py` with subcommands `parse`, `scaffold`, `check`.
- `parse` extracts fenced KB JSON and splits subskill sections into IR.
- `scaffold` writes `tools/drafts/skills/<slug>/` with stub `SKILL.md`, `assets/knowledge-base.json`, empty `atoms.json` placeholder, module reference stubs, and templates inferred from card blocks when present.
- Never write into `skills/value/` or `.cursor/skills/value/`.

## Data structures

- CLI args. `--source`, `--slug`, `--out`, `--fixture`.
- Scaffold tree matches skill-authoring layout (`SKILL.md`, `references/`, `assets/`, `scripts/` stub).

## Verification

**Static.** Unit tests for parse of value suite and lean-product suite.

**Runtime.** `compile.py scaffold --source docs/lean-product-playbook-prompt-suite.md --slug lean-mvp-recompile --out tools/drafts/skills/` creates a tree; `compile.py check` reports missing atoms as expected incomplete.
