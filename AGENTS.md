# Agents map — Value

## Purpose

Develop and distribute a Cursor agent skill from this GitHub repo. The layered spoke under `src/` is the optional host app; the skill package is the primary ship surface.

## Layout

| Path | Role |
|------|------|
| `skills/value/` | Ship package for `npx skills add rphoward/Value` |
| `.cursor/skills/value/` | Same skill for Cursor while developing this repo |
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

Follow `.cursor/rules/skill-authoring.mdc` and `.cursor/rules/skills-repo.mdc`. Write the skill under `.cursor/skills/value/`. Do not put new skill packages only under `tools/drafts/` at ship time.
