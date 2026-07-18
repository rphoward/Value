# Value

A teaching-first Cursor / agent skill for value-proposition design: one question at a time, durable session state, and product/UX brief artifacts.

## Install

```bash
npx skills add rphoward/Value
```

That installs the `value` skill into your agent skills directory. Useful variants:

```bash
# List what the package contains
npx skills add rphoward/Value -l

# Install globally (all projects)
npx skills add rphoward/Value -g -y

# Cursor only
npx skills add rphoward/Value -a cursor -y

# Pin a specific skill name (same package)
npx skills add rphoward/Value -s value -y
```

After install, in Cursor ask something like: *“Grill me on a value proposition for my scheduling app.”*

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
