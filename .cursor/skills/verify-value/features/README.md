# Value journey verification map

This directory is the maintained source for verifying user-facing behavior of the Value monorepo **journey skill CLIs** (Values, BMG, Teams, lean-mvp) plus optional spoke `/health`. Read this index before driving, then use the matching feature file as the recipe.

`/product-spine` is routing-only in Cursor. It is **not** mapped here. Prove sibling scripts instead.

## Baseline preconditions

- Work from the Value repo root (`C:\Projects\value` or the current clone).
- `pip install -e .` and `PYTHONPATH=src` already done for this shell.
- Create a disposable run with `control-value.py prepare` and use only that `RUN_ID`.
- Never drive sessions under the live repo `workproduct/` tree.
- Never attach to a spoke on port 8000 that a human started with `tools/start-value.ps1`.
- Run `control-value.py doctor --run-id <RUN_ID>` and require `doctor ok`.

## Driving conventions

- Start every recipe from a fresh prepare unless its preconditions say otherwise.
- Run skill scripts only through `control-value.py cli --run-id <RUN_ID> [--skill …] -- …`.
- Default `--skill` is `value`. Pass `--skill bmg`, `--skill teams`, or `--skill lean-mvp` for siblings.
- Treat every command as literal. Keep slug names and flags unchanged.
- Session paths are relative to the run directory (for example `workproduct/teams/verify-demo/session.json`).
- Restore nothing into live `workproduct/`. Cleanup removes this run's entire `workproduct/` tree.

## Proof and skip reporting

- Capture the user action and the resulting state, not only the final stdout line.
- CLI proof includes command, stdout, stderr, exit code, and the transcript path printed as `TRANSCRIPT=…`.
- Mutation proof includes a second read of the written file (`session.json`, milestone `.md`, `CONTEXT.product.md`, or run-local `CONTEXT.md`).
- Dry-run proof includes an observation that the write target is absent or unchanged.
- Record the feature ID with every artifact note.
- Report an unreachable path with the attempted command and unmet precondition.

## Feature entry contract

Each feature file starts with an H1 title and one paragraph describing the user-visible behavior. It then uses exactly four H2 sections in this order: `Sub-features`, `How to get to it (user POV)`, `Driving it with control-value`, `Gotchas`.

## Features

### Values

- [Start a Values session](./session-init.md) covers isolated init and status strip.
- [Ask and accept the next atom](./next-question-and-accept.md) covers next_question + accept_answer.
- [Emit the product seed](./build-pack-seed.md) covers write_build_pack --force and CONTEXT.product.md.
- [Promote vernacular](./promote-context.md) covers dry-run and gated --apply.

### BMG / Teams / lean-mvp

- [Start a BMG session](./bmg-session-init.md) covers canvas skill init + status under `workproduct/bmg/`.
- [Start a Teams session](./teams-session-init.md) covers teams init + status under `workproduct/teams/`.
- [Start a lean-mvp session](./lean-mvp-session-init.md) covers lean init + status under `workproduct/lean-mvp/`.

### Spoke

- [Spoke health](./spoke-health.md) covers the optional Starlette `/health` smoke.
