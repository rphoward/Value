# Phase 3. Portable session runtime

Back-link: [overview.md](./overview.md)

## Goal

Peel a curriculum-agnostic session engine template from `skills/value/scripts/_session/` so any compiled skill can copy it and only replace constants, atoms, and templates.

## Changes

- Add `tools/prompt-suite-compile/templates/session-runtime/` containing parameterized `_session` package plus thin CLIs (`init_session`, `status`, `next_question`, `accept_answer`, `write_milestone`).
- Replace hard-coded module names with values loaded from `assets/skill-config.json` (module order, phases, gate pass phrases, express spine, workproduct root).
- Strip value-only voice/pitch helpers from the template (or gate them behind empty config).
- `scaffold` copies this template into the draft skill `scripts/`.

## Data structures

- `skill-config.json`. `workproduct_root`, `module_order`, `module_phase`, `gate_artifacts`, `canonical_gate_pass`, `express_spine`, `express_requires`, `module_brief_labels`.
- Session schema stays closed; atom id pattern becomes configurable regex.

## Verification

**Static.** Template imports with a minimal config and lean-mvp-shaped atoms.

**Runtime.** Init → accept spine → milestone sim (same style as the DAG coverage sim) exits clean on a toy curriculum of three atoms.
