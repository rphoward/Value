# TLBMC canvas ingest (structure only)

**Status:** teaching-aid ingest for classic BMG skill pedagogy.  
**Sources:** `docs/screenshots/Screenshot 2026-07-29 215723.png`, `215739.png`, `215757.png`, `215826.png`.  
**Curriculum source of truth:** `docs/business-model-generation-prompt-suite.md` (classic BMG).  
**Rule:** sticky-note fills (coffee / capsule / machine world) are **worked teaching examples**, not throwaway noise. Geometry and block labels stay canonical. Example content stays as a teach aid: simple product → many block ramifications. Skill voice is heavily teaching-oriented.

---

## Stack

Three peer canvases, same outer shape, different layer semantics:

| Order | Layer | Color cue (in sources) | Center block |
|-------|--------|------------------------|--------------|
| 1 | Economic | blue | Value Proposition |
| 2 | Environmental | green | Functional Value |
| 3 | Social | yellow/orange | Social Value |

Shared outer frame: **five top columns** + **two bottom bands**. Column 1 and 5 are full-height; columns 2 and 4 are each **split into two stacked blocks**; column 3 is full-height (the layer’s “value” spine). Bottom: **left impact/cost band**, **right benefit/revenue band**.

---

## Layer 1 — Economic Business Model Canvas

Classic BMC block set (labels as on canvas):

| Position | Block |
|----------|--------|
| Col 1 full | Partners |
| Col 2 top | Activities |
| Col 2 bottom | Resources |
| Col 3 full | Value Proposition |
| Col 4 top | Customer Relationship |
| Col 4 bottom | Channels |
| Col 5 full | Customer Segments |
| Bottom left | Costs |
| Bottom right | Revenues |

---

## Layer 2 — Environmental (life-cycle) canvas

Same geometry; life-cycle / LCA-oriented blocks:

| Position | Block |
|----------|--------|
| Col 1 full | Supplies and Out-sourcing |
| Col 2 top | Production |
| Col 2 bottom | Materials |
| Col 3 full | Functional Value |
| Col 4 top | End-of-Life |
| Col 4 bottom | Distribution |
| Col 5 full | Use Phase |
| Bottom left | Environmental Impacts |
| Bottom right | Environmental Benefits |

**Reading hint from geometry:** left side leans supply/production; right side leans distribution, end-of-life, and use; center is the functional unit / functional value.

---

## Layer 3 — Social stakeholder canvas

Same geometry; stakeholder-oriented blocks:

| Position | Block |
|----------|--------|
| Col 1 full | Local Communities |
| Col 2 top | Governance |
| Col 2 bottom | Employees |
| Col 3 full | Social Value |
| Col 4 top | Societal Culture |
| Col 4 bottom | Scale of Outreach |
| Col 5 full | End-User |
| Bottom left | Social Impacts |
| Bottom right | Social Benefits |

---

## Coherence (fourth screenshot — the operator layer)

### Horizontal coherence

Within **each** layer alone: the blocks form a closed loop (infinity / cycle over that single canvas).  
Skill implication: a filled layer must make sense **as its own system** before cross-layer claims.

### Vertical coherence

Across the stack: corresponding columns/blocks align through all three layers (arrows piercing economic → environmental → social).  
Skill implication: center “value” blocks and paired cost/impact vs revenue/benefit bands are the primary vertical seams; left/right columns also stack as peer positions.

### Suggested vertical seams (by column position)

| Seam | Economic | Environmental | Social |
|------|----------|---------------|--------|
| Left full | Partners | Supplies and Out-sourcing | Local Communities |
| Mid-left top | Activities | Production | Governance |
| Mid-left bottom | Resources | Materials | Employees |
| Center | Value Proposition | Functional Value | Social Value |
| Mid-right top | Customer Relationship | End-of-Life | Societal Culture |
| Mid-right bottom | Channels | Distribution | Scale of Outreach |
| Right full | Customer Segments | Use Phase | End-User |
| Bottom left | Costs | Environmental Impacts | Social Impacts |
| Bottom right | Revenues | Environmental Benefits | Social Benefits |

---

## Pedagogy (user clarification)

- Screenshots are samples of how a classic canvas (and related views) look when filled.
- Coffee is the deliberately simple case. If someone can see partners, channels, costs, and knock-on effects on a coffee machine + capsules story, they can transfer that reading to a harder venture.
- Similar worked examples belong in the skill as teach aids (atoms, references, or knowledge-base grounding), not only as discarded placeholders.
- Multi-layer / coherence views still illustrate “one simple offer, many kinds of ramifications” and the spirit of peer-skill convergence (`bmg` / `value` / `lean-mvp` / `product-spine`). They do not replace the BMG prompt suite as the paced curriculum spine.

## Build stance (settled)

- Standalone paced skill from the BMG prompt suite.
- Sibling to `value` and `lean-mvp`; order of entry is project-dependent.
- Draft under `tools/drafts/skills/bmg/` (slug `bmg`). Promote only with explicit consent.
- Coffee teach aid lives in draft `assets/knowledge-base.json` → `teach_aids.coffee_capsule_example`.
