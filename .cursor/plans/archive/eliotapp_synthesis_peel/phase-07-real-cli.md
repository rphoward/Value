# Phase 07 — Real eliotapp/cli

Back-link: [overview.md](overview.md)

## Goal

`python -m eliotapp.cli …` runs hillclimb + inspect operators. Skill scripts become thin wrappers.

## Changes

- Replace stub `eliotapp/cli/__main__.py` with real subcommands (record, inspect, and the operators SYNTHESIS already lists).
- Move or wrap logic from `.cursor/skills/workflow/scripts/hillclimb_cli` so the package owns the operator surface.
- Keep skill prose pointing at the package entry; scripts stay thin.

## Data structures

CLI parses args → calls application commands with locator. No Path built by humans beyond optional file args for drafts/scorecards.

## Verification

**Static.** Pytest or CLI unit tests for parse + dispatch. Full suite green.

**Runtime.** `control-cli`: `python -m eliotapp.cli --help` and one non-mutating inspect (or dry) command against a fixture run.
