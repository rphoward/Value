# After you install Product-Spine in *your* project

## Does `npx skills add` work standalone?

**Yes for the skills themselves.** With:

```bash
npx skills add rphoward/Product-Spine --skill '*' -a cursor -y
```

you get seven skills under `.cursor/skills/` (or `~/.cursor/skills/` if you used `-g`). They do not need the Value monorepo.

**Progress saves in your project**, not in GitHub:

| Skill | Session folder |
|-------|----------------|
| Values | `workproduct/value-proposition/<slug>/` |
| BMG | `workproduct/bmg/<slug>/` |
| Teams | `workproduct/teams/<slug>/` |
| Brand Identity | `workproduct/brand-identity/<slug>/` |
| lean-mvp | `workproduct/lean-mvp/<slug>/` |

Milestones (`customer-profile.md`, `canvas-mapper.md`, `tam-planner.md`, `brand-strategist.md`, `mvp-scope.md`, …) land next to `session.json`. Same **slug** across skills.

**You need:**

- Cursor (or another agent that loads those skills)
- Python 3 on the PATH (session scripts are stdlib-only)
- Consent when a skill creates the first session for a slug

**Outside the pack:**

- NotebookLM (or similar) only if you want the video claim path
- This `docs/` folder is for humans reading the ship repo; `npx skills add` installs the skills, not a copy of every doc into your tree

**Not automatic:**

- Root `CONTEXT.md` / `AGENTS.md` in your app repo
- Committing `workproduct/` (your choice; many teams commit the notes)

## Carry the work into coding agents (like CONTEXT.md)

Skills save customer and product language under `workproduct/`. Coding agents often only read root `CONTEXT.md` and `AGENTS.md`. Bridge them on purpose.

### What Values already writes

When you run Values far enough (or force a build pack), `write_build_pack.py` can emit into the session folder:

- `CONTEXT.product.md` — customer-domain glossary (terms only)
- `AGENTS.product.md` — Always / Ask first / Never product walls

Those files are the seed. They are not yet your repo’s root glossary.

### What to put in *your* repo

1. **Keep `workproduct/`.** That is the durable session record.
2. **Promote language when it stabilizes.** Run `python .cursor/skills/value/scripts/promote_context.py workproduct/value-proposition/<slug>/session.json` (dry-run default) to draft Term / _Avoid_ lines; pass `--apply` when ready to merge into root `CONTEXT.md`.
3. **Point `AGENTS.md` at the path.** Add a short “Product-Spine / Values work” section so agents look at the notes and the glossary. After install, paste from `.cursor/skills/product-spine/assets/AGENTS.fragment.md` (or `.cursor/skills/value/assets/AGENTS.fragment.md` for a solo Values install). The ship-repo copy lives at [AGENTS.fragment.md](AGENTS.fragment.md) for human reading only.
4. **Do not treat `workproduct/` as implementation.** It is customer and product language; code still lives in your normal source tree.

### Tiny checklist

1. Install the pack in the project you are building.  
2. Lock a slug; run `/product-spine` or a sibling.  
3. Let sessions and milestones accumulate under `workproduct/`.  
4. After clarity (or when language feels stable), refresh `CONTEXT.product.md` / `AGENTS.product.md`.  
5. Lift the useful terms into root `CONTEXT.md`; add the AGENTS fragment so later agents keep using those words.
