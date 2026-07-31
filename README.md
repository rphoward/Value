# Value

Monorepo for developing Cursor agent skills that help turn a vibecoded idea into something others value — then into a shippable cut, a business model, and an honest claim.

Day-to-day install uses the small ship repos (see below). This repo is for building and testing the packages.

## Start here (human guide)

Read **[docs/skill-journey.md](docs/skill-journey.md)** first.

It defines the shared words (slug, phase, gate, done enough), then builds from one skill → pairs → the full Product-Spine path in plain American English.

## Install (recommended)

| Need | Ship repo | Command |
|------|-----------|---------|
| Who / why (clarity) | [Values](https://github.com/rphoward/Values) | `npx skills add rphoward/Values` |
| Business Model Canvas | [BMG](https://github.com/rphoward/BMG) | `npx skills add rphoward/BMG` |
| Team alignment (TAM) | [Teams](https://github.com/rphoward/Teams) | `npx skills add rphoward/Teams` |
| Lean MVP cut | [MVP](https://github.com/rphoward/MVP) | `npx skills add rphoward/MVP` |
| Whole path guide + siblings (value, bmg, teams, lean-mvp, story) | [Product-Spine](https://github.com/rphoward/Product-Spine) | `npx skills add rphoward/Product-Spine --skill '*' -a cursor -y` |

Local vs global:

```bash
npx skills add rphoward/Values          # this project
npx skills add rphoward/Values -g       # all projects
```

## Package layout (this monorepo)

```
.cursor/skills/<name>/     # live skills while developing here
skills/<name>/             # digest-matched ship mirrors
workproduct/               # session notes per skill + slug
docs/skill-journey.md      # human start guide
```

## Develop in this repo

```powershell
pip install -e .
$env:PYTHONPATH = 'src'
python -m unittest discover -s tests -v
```

Agent map: [AGENTS.md](AGENTS.md)

Remote: https://github.com/rphoward/Value.git
