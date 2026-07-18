---
name: Def-ref conversion
overview: Convert 36 skill references that have a (def-ref …) stub plus markdown prose into real def-ref s-expressions per skill-authoring.mdc protocol-3b. Pattern already shipped in workflow one-command.md and playbook.md.
todos:
  - id: eliot-refs
    content: Convert 12 eliot/references/*.md (engine, output-format, workflows, …)
    status: completed
  - id: distiller-refs
    content: Convert 13 distiller/references/*.md (activation, exa-discovery, author-matching-*, …)
    status: completed
  - id: evaluator-refs
    content: Convert 11 evaluator/references/*.md (style-block-rubric last — largest)
    status: completed
  - id: verify
    content: "Run def-ref audit script; rg no ## prose blobs before artifact marker; pytest if any"
    status: completed
isProject: false
---

# Def-ref conversion — flat plan

Back-link: audit from 2026-07-09 chat; workflow refs already correct.

## Problem

36 files under `.cursor/skills/{eliot,distiller,evaluator}/references/` start with `(def-ref … (linked-from …))` then drop into markdown (`##` headings, numbered lists, bold labels). `skill-authoring.mdc` protocol-3b forbids unstructured prose blobs in references. Agents treat the stub as compliance while loading markdown rules.

**Already OK (do not touch):**

- `workflow/references/one-command.md`, `playbook.md`
- `design-taste-frontend/references/{appendices,preflight-checklist,protocols-layout-motion,motion-skeletons,appendices-artifacts}.md`
- `tool-ui-htmx/references/preflight-checklist.md`

## Conversion rules (one pattern)

1. **Keep** `(def-ref <name> (linked-from …))` — name must still match SKILL pointer.
2. **Replace** markdown sections with nested s-expressions: `(section …)`, `(check …)`, `(forbidden …)`, `(step N …)`, `(tier sharp|functional|soft|broken …)`, `(trap …)`, `(load-order …)`.
3. **Move** long literals (JSON schemas, fixture gold blocks, TSX/CSS snippets, report templates) to artifact tail: `;; --- artifacts ---` then `## <artifact-name>` + fenced block — same as `one-command.md`.
4. **Do not** convert `handoff/*.md`, `SKILL.md` bodies (stay `def-sop`), or `.cursor/commands/*.md`.
5. **Do not** change meaning — structural rewrite only.

**Reference shape:** `.cursor/skills/workflow/references/one-command.md`

## File checklist (36)

### ELIOT (12)

- [ ] `eliot/references/default-voice.md`
- [ ] `eliot/references/engine.md`
- [ ] `eliot/references/examples-dostoevsky.md` — gold block → artifact; keep INPUT path in def-ref
- [ ] `eliot/references/extensions.md`
- [ ] `eliot/references/input-detection.md`
- [ ] `eliot/references/model-profile.md`
- [ ] `eliot/references/ocean-facets.md`
- [ ] `eliot/references/output-format.md`
- [ ] `eliot/references/sloppy-source.md`
- [ ] `eliot/references/user-aids.md`
- [ ] `eliot/references/validation.md`
- [ ] `eliot/references/workflows.md`

### Distiller (13)

- [ ] `distiller/references/activation.md`
- [ ] `distiller/references/author-matching.md`
- [ ] `distiller/references/author-matching-essay.md`
- [ ] `distiller/references/author-matching-literary.md`
- [ ] `distiller/references/author-matching-technical.md`
- [ ] `distiller/references/eliot-mapping.md`
- [ ] `distiller/references/emulation-prompts.md`
- [ ] `distiller/references/engine.md`
- [ ] `distiller/references/exa-discovery.md`
- [ ] `distiller/references/idea-extraction.md`
- [ ] `distiller/references/output-format.md`
- [ ] `distiller/references/register-detection.md`
- [ ] `distiller/references/standing-rules.md`

### Evaluator (11)

- [ ] `evaluator/references/engine.md`
- [ ] `evaluator/references/extras.md`
- [ ] `evaluator/references/input-detection.md`
- [ ] `evaluator/references/lenses.md`
- [ ] `evaluator/references/modes.md`
- [ ] `evaluator/references/output-format.md`
- [ ] `evaluator/references/role.md`
- [ ] `evaluator/references/rubric.md`
- [ ] `evaluator/references/style-block-diff.md`
- [ ] `evaluator/references/style-block-rubric.md` — do last (~370 lines)
- [ ] `evaluator/references/workflows.md`

Suggested order within each skill: small files first (`standing-rules`, `role`, `modes`), then engine/output-format, then `style-block-rubric`.

## Verify (done when all checked)

```powershell
# Re-run audit — expect 0 violations outside OK list
python tools/audit_def_ref.py

# Or inline one-liner if script not committed yet:
# rg -l '^\(def-ref ' .cursor/skills/eliot/references .cursor/skills/distiller/references .cursor/skills/evaluator/references | % { ... }

# No Python behavior change expected; spot-check if nervous:
$env:PYTHONPATH="src"
python -m pytest tests/ -q --ignore=tests/test_presentation_runs.py
```

Pass: every file in checklist has lisp body before any `##` (except declared artifact tail); `linked-from` still matches parent SKILL; no new markdown prose sections in the body.

## Out of scope

- Rewriting SKILL.md protocol text
- Converting `hillclimb.md` command (imperative edge — separate if wanted)
- Changing evaluator Python or rubric semantics
- New linter hook (optional follow-up)
