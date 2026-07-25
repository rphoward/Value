# Product-spine walk + thermos findings

## Fixed in this pass

- Dead `VALUE_THROUGH_VALUE_MAP` / `VALUE_GATES` removed from `walk_spine.py`.
- `last-walk.json` no longer written or committed.
- `regression: MS05 coaching omits story_assist` (+ key presence assert).
- `skills/product-spine/` ship mirror + digest test (thermos: shipped skills pointed at missing skill).
- Spine `no-session-mvp` prefers value unless explicit skip-value.
- Spine voice requires rationale + slug.
- MS05 turn-recipe defers to `coaching.story_assist` / `mvp-scope` (less duplicate policy text).

## Still open (intentional / later)

- Two-slash handoff before first atom (by design for slash-only spine; not auto-activating).
- NotebookLM leaves Cursor; story-only path has no session.
- MS05 paste tax (honest contract; no auto-accept).
- `import_value_context` repo-root resolution for non-default `--root` (pre-existing).
- Value gate `--records` ceremony (pre-existing).
- Walk `triage()` is still a second source of truth vs SKILL prose (acceptable for draft harness).

## Thermos reviewers

- [Thermo branch risk](1c020e9c-b3d4-40da-9741-ecd37793a3af)
- [Thermo code quality](bc94f3a0-dd78-4af2-a338-51ef47e74a7c)

## Rerun

```powershell
python tools/drafts/product-spine-walk/walk_spine.py
python -m pytest tests/test_product_spine_skill.py tests/test_lean_mvp_coaching.py tests/test_lean_mvp_skill_package.py -q
```
