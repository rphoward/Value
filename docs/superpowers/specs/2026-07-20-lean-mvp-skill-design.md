# Lean MVP skill design

## Goal

Ship a sibling Cursor skill that teaches lean MVP practice with the same paced-interview model as `value`. Chapter 1 customer context should reuse evidence from an existing value-proposition session when files exist. Otherwise the skill grills through atoms and scripts like `value`.

## Package boundary

One skill at `skills/lean-mvp/` (mirrored to `.cursor/skills/lean-mvp/`). Do not modify `skills/value/`, `.cursor/skills/value/`, or the Values distribution repo.

## Shared project identity

Both skills use the same project slug.

```text
workproduct/value-proposition/<slug>/session.json
workproduct/value-proposition/<slug>/customer-profile.md
workproduct/lean-mvp/<slug>/session.json
workproduct/lean-mvp/<slug>/customer-context.md
```

Lean MVP reads value artifacts. Value never reads lean-mvp artifacts.

## Value bridge (chapter 1)

On lean-mvp session init or resume, run `scripts/import_value_context.py` internally when `workproduct/value-proposition/<slug>/session.json` exists.

Mapping lives in `assets/value-bridge-map.json`. Imported answers are recorded with `provenance: value-import` and satisfy the matching lean-mvp atoms. Remaining atoms are grilled normally.

If no value session exists, chapter 1 runs from atom C01 with no import.

## Session state

Canonical file: `workproduct/lean-mvp/<slug>/session.json`. Schema: `assets/session.schema.json`. Atom index: `assets/atoms.json`.

Optional top-level `value_import` records source path, import timestamp, and which atoms were prefilled.

## Modules (v1)

v1 ships one module only: `customer-context` (prompt-suite chapter 1 equivalent). Additional modules land when the lean MVP source doc is ingested.

Source prompt suite: `docs/lean-product-playbook-prompt-suite.md` (Dan Olsen, Lean Product Playbook).

## Modules (ingested)

| Module | Playbook step | Subskill |
|--------|---------------|----------|
| `customer-context` | Step 1 Target Customer | Need-Prioritizer §1 |
| `underserved-needs` | Step 2 Underserved Needs | Need-Prioritizer §2–3 |
| `mvp-scope` | Steps 3–4 Value Prop & Features | MVP-Scoper |
| `ux-prototype` | Steps 5–6 Prototype & Test | UX-Designer |
| `metrics` | Post-launch | Metric-Optimizer |

## Verification

1. Value skill tests remain green (unchanged).
2. Lean-mvp package mirror test: `skills/lean-mvp/` digest matches `.cursor/skills/lean-mvp/`.
3. `import_value_context.py` fixture test: value session answers map to lean atoms without overwriting newer lean answers.

## Deferred

- Full prompt-suite compiler from `docs/lean-mvp-prompt-suite.md`
- Additional lean-mvp modules beyond customer-context
- Values repo ship surface for lean-mvp (separate repo or combined — decide at ship time)
