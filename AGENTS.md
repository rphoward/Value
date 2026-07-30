# Agents map — Value

## Purpose

Develop and distribute a Cursor agent skill from this GitHub repo. The layered spoke under `src/` is the optional host app; the skill package is the primary ship surface.

## Layout

| Path | Role |
|------|------|
| `skills/value/` | Ship package for `npx skills add rphoward/Values` |
| `skills/lean-mvp/` | Lean MVP skill (pairs with value; dev in monorepo) |
| `skills/bmg/` | Ship package for `npx skills add rphoward/BMG` (digest-matched to `.cursor/skills/bmg/`) |
| `tools/prompt-suite-compile/` | Thin shims → `.cursor/skills/scripted-skill-from-doc/` |
| `.cursor/skills/product-spine/` | Human guide for vibecode → valuable → marketable: invoke `/product-spine` to carry phase, next sibling, and claim/NotebookLM exit |
| `skills/product-spine/` | Ship-tree mirror of product-spine (digest-matched to `.cursor/skills/product-spine/`) |
| `.cursor/skills/value/` | Same skill for Cursor while developing this repo |
| `.cursor/skills/lean-mvp/` | Lean MVP skill for Cursor in this repo |
| `.cursor/skills/bmg/` | BMG skill for Cursor in this repo (canvas → patterns → strategy → ambidexterity) |
| `.cursor/skills/story-generation-prompt/` | Evidence → story → generation prompt, INVEST-plus rubric (pairs with lean-mvp MS05) |
| `.cursor/skills/scripted-skill-from-doc/` | Portable compile pack in standard skill layout (`scripts/`, `references/`, `assets/`) |
| `src/value/` | Layered spoke product (retargeted at init) |
| `tests/` | Unittest / pytest suite |
| `tools/` | Local scripts (`start-*.ps1`) |
| `.cursor/rules/` | Always-on and path-scoped agent rules |
| `.cursor/scaffold/` | Init / retarget tooling |

## Commands

```powershell
.\.cursor\scaffold\scaffold-init.ps1 -ProductSlug value
pip install -e .
$env:PYTHONPATH = 'src'
python -m unittest discover -s tests -v
.\tools\start-value.ps1
```

## Skill authoring

Follow `.cursor/rules/skill-authoring.mdc` and `.cursor/rules/skills-repo.mdc`. Write the skill under `.cursor/skills/<name>/`. Do not put new skill packages only under `tools/drafts/` at ship time.
