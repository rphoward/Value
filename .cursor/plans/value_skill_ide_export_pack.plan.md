---
name: Value skill IDE export pack
overview: Sift session.json into IDE-standard files via export lenses — CONTEXT.product, ADRs, UI copy/states, first-value, AGENTS.product. No Spec Kit.
todos:
  - id: filter-ceremony
    content: Skip bypass-ceremony answers in brief and export fills
    status: completed
  - id: templates-lenses
    content: Templates, section-map ide_exports, references/export-lenses.md
    status: completed
  - id: write-build-pack
    content: write_build_pack.py + fill_build_pack_file + ADR seeds
    status: completed
  - id: skill-tests-mirror
    content: SKILL + session-contract + tests; mirror both skill trees
    status: completed
isProject: false
---

# IDE export pack (shipped)

## Files written by `scripts/write_build_pack.py`

- `CONTEXT.product.md`
- `AGENTS.product.md`
- `ui-copy.md`
- `states-and-flows.md`
- `first-value.md`
- `docs/adr/NNNN-*.md` for hard decisions

## Lenses

See `references/export-lenses.md`.

## Verification

`python -m unittest discover -s tests -p "test_value*.py"` — 58 passed.
