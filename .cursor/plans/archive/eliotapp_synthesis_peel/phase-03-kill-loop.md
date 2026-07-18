# Phase 03 — Kill loop.py

Back-link: [overview.md](overview.md)

## Goal

Delete `eliotapp/application/workflow/loop.py` in the same wave as every importer rewrite. No permanent shim.

## Changes

- Grep is authoritative for `eliotapp.application.workflow.loop` importers (tests, hillclimb_cli scripts, `run_index`, `hillclimb_runs`, tools, hooks validate).
- Point each import at the real owning module (shapes, run_state, climb commands, etc.).
- Delete `loop.py` when the last importer is gone.
- Update `.cursor/hooks/validate_skills_module.py` if it still smoke-imports `loop`.

## Data structures

None new. Re-exports collapse to their home modules.

## Verification

**Static.** `rg workflow.loop` empty under active tree (ignore nested residue if any). Full `pytest`.

**Runtime.** One hillclimb_cli smoke command that previously imported through `loop` (record or inspect help path).
