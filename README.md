# Value

A teaching-first Cursor / agent skill for value-proposition design: one question at a time, durable session state, and product/UX brief artifacts.

## Install (recommended)

Use the minimal skill-only repo:

```bash
npx skills add rphoward/Values
```

- **Local (one project):** `npx skills add rphoward/Values`
- **Global (all projects):** `npx skills add rphoward/Values -g`

Ship repo: https://github.com/rphoward/Values

This monorepo (`rphoward/Value`) is for developing the skill plus optional spoke app. Prefer `Values` for distribution.

## Package layout

```
skills/value/                 # ship surface for npx skills / skills.sh
  SKILL.md
  references/
  assets/
  scripts/

.cursor/skills/value/         # same package for Cursor in this repo
```

## Develop in this repo

```powershell
pip install -e .
$env:PYTHONPATH = 'src'
python -m unittest discover -s tests -v
```

Remote: https://github.com/rphoward/Value.git
