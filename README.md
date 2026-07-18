# Value

Cursor agent skill for GitHub distribution, with a layered spoke scaffold for local use.

## Skill package

```
.cursor/skills/value/
  SKILL.md
  references/
  scripts/
  assets/
```

## Spoke app

```
src/<slug>/
  core/
  application/
  infrastructure/
  presentation/
```

## Setup

```powershell
pip install -e .
$env:PYTHONPATH = 'src'
python -m unittest discover -s tests -v
```

Remote: https://github.com/rphoward/Value.git
