# After you install Product-Spine in *your* project

## Does `npx skills add` work standalone?

**Yes for the skills themselves.** With:

```bash
npx skills add rphoward/Product-Spine --skill '*' -a cursor -y
```

you get five skills under `.cursor/skills/` (or `~/.cursor/skills/` if you used `-g`). They do not need the Value monorepo.

**Progress saves in your project**, not in GitHub:

| Skill | Session folder |
|-------|----------------|
| Values | `workproduct/value-proposition/<slug>/` |
| BMG | `workproduct/bmg/<slug>/` |
| lean-mvp | `workproduct/lean-mvp/<slug>/` |

Milestones (`customer-profile.md`, `canvas-mapper.md`, `mvp-scope.md`, …) land next to `session.json`. Same **slug** across skills.

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
2. **Promote language when it stabilizes.** Copy or tighten terms from `CONTEXT.product.md` into root `CONTEXT.md` (Term / _Avoid_ form). That is how vernacular grows the same way this pack’s own CONTEXT grew from the skill journey.
3. **Point `AGENTS.md` at the path.** Add a short “Product-Spine / Values work” section so agents look at the notes and the glossary. Paste from [AGENTS.fragment.md](AGENTS.fragment.md) if you want a ready block.
4. **Do not treat `workproduct/` as implementation.** It is customer and product language; code still lives in your normal source tree.

### Tiny checklist

1. Install the pack in the project you are building.  
2. Lock a slug; run `/product-spine` or a sibling.  
3. Let sessions and milestones accumulate under `workproduct/`.  
4. After clarity (or when language feels stable), refresh `CONTEXT.product.md` / `AGENTS.product.md`.  
5. Lift the useful terms into root `CONTEXT.md`; add the AGENTS fragment so later agents keep using those words.
