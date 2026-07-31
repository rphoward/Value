# Product-Spine

A Cursor skill pack for taking a vibecoded idea through clarity, business model, team alignment, lean MVP scope, and an honest marketable claim.

Six skills install together:

| Skill | Role |
|-------|------|
| `product-spine` | One slash entry that names the phase and the sibling to open |
| `value` | Customer profile and value-map coaching (`workproduct/value-proposition/`) |
| `bmg` | Classic Business Model Canvas through ambidexterity (`workproduct/bmg/`) |
| `teams` | Team Alignment Map first, then optional assessor/contract/conflict (`workproduct/teams/`) |
| `lean-mvp` | Underserved needs through MVP scope (`workproduct/lean-mvp/`) |
| `story-generation-prompt` | INVEST-plus story and optional NotebookLM generation prompt |

**Start guide:** [docs/skill-journey.md](docs/skill-journey.md)  
**Standalone + your repo:** [docs/for-your-repo.md](docs/for-your-repo.md)  
**Paste into your AGENTS.md:** [docs/AGENTS.fragment.md](docs/AGENTS.fragment.md)

Developed in the [Value](https://github.com/rphoward/Value) monorepo; this repo is the minimal install surface for `npx skills add`.

## Install

```bash
npx skills add rphoward/Product-Spine --skill '*' -a cursor -y
```

Global:

```bash
npx skills add rphoward/Product-Spine -g -a cursor -y
```

Skills land under `.cursor/skills/` (project) or `~/.cursor/skills/` (global). They work **without** cloning this monorepo.

### Useful options

```bash
npx skills add rphoward/Product-Spine -l
npx skills add rphoward/Product-Spine -s product-spine -a cursor -y
npx skills add rphoward/Product-Spine -s bmg -a cursor -y
npx skills add rphoward/Product-Spine -s teams -a cursor -y
```

## Standalone progress

Sessions and milestones save under **your project**:

- `workproduct/value-proposition/<slug>/`
- `workproduct/bmg/<slug>/`
- `workproduct/teams/<slug>/`
- `workproduct/lean-mvp/<slug>/`

Use the same **slug** across skills. You need Python 3 on the PATH for session scripts.

Root `CONTEXT.md` / `AGENTS.md` are **not** auto-written. Values can emit `CONTEXT.product.md` and `AGENTS.product.md` into the session folder; promote stable terms into your repo glossary so coding agents keep that vernacular. See [docs/for-your-repo.md](docs/for-your-repo.md).

## After install

> `/product-spine` — where should I begin on this vibecoded project?

Or open a sibling when you know the phase:

- `/value` — who is this for, and why would they care?
- `/bmg` — classic Business Model Canvas
- `/teams` — Team Alignment Map and optional team tools
- `/lean-mvp` — honest MVP feature set
- `/story-generation-prompt` — shareable claim / NotebookLM prompt (also used on claim turns)

Product-Spine routes; siblings grill. Teams is optional business-side alignment, not a product gate. On claim, Product-Spine opens saved notes — you should not hunt folders.

## Package layout

```
docs/skill-journey.md
docs/for-your-repo.md
docs/AGENTS.fragment.md
skills/product-spine/
skills/value/
skills/bmg/
skills/teams/
skills/lean-mvp/
skills/story-generation-prompt/
README.md
```

## Solo ship repos

| Skill | Repo |
|-------|------|
| Values | https://github.com/rphoward/Values |
| BMG | https://github.com/rphoward/BMG |
| Teams | https://github.com/rphoward/Teams |
| MVP | https://github.com/rphoward/MVP |

## License

Add a license file here if you want to clarify reuse terms.
