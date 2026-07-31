# From a vibecode idea to something others value

Plain guide for Cursor skills that work together: **Values**, **BMG**, **Teams**, **MVP** (lean-mvp), and **Product-Spine**.

Read the word list first. The rest of this doc uses those words on purpose.

---

## Words we use (keep these)

| Word | Plain meaning |
|------|----------------|
| **Skill** | A slash command and coaching pack the agent loads on request. |
| **Slash** | How you open a skill in Cursor, for example `/value` or `/product-spine`. |
| **Slug** | Short folder name for one project. Same slug across skills. Example: `shiftswap`. |
| **Session** | Saved progress for one skill under `workproduct/…/<slug>/session.json`. |
| **Atom** | One coaching question in a skill. You answer; the skill moves on. |
| **Gate** | Check at the end of a module. Pass it (or bypass it on purpose) before the next module. |
| **Milestone** | Written notes the skill saves when a gate passes (for example `value-map.md`). |
| **Phase** | Where Product-Spine says you are on the path: clarity, business, teams, mvp, or claim. |
| **Sibling** | A grilling skill Product-Spine points you into. Spine routes; siblings grill. |
| **Done enough** | The finish line for that phase so you can come back to Product-Spine. |
| **Clarity** | Phase for “who is this for, and why would they care?” Owned by Values (`/value`). |
| **Business** | Phase for a classic Business Model Canvas and related work. Owned by BMG (`/bmg`). |
| **Teams** | Optional business-side leg for Team Alignment Map, contracts, and psych safety. Owned by Teams (`/teams`). Not a product gate. |
| **MVP** | Phase for a lean, shippable feature cut. Owned by lean-mvp (`/lean-mvp`). |
| **Claim** | Phase for an honest pitch and optional NotebookLM video prompt. Product-Spine runs this with your saved notes. |
| **Guide-turn** | What Product-Spine always says: where you are, why, what to open this turn, when to come back. |

You do not need atom IDs. Talk in plain words. The agent runs the scripts.

---

## Four kinds of value these skills make

Start with the kind you need today. You can add the others later. Keep the same **slug**.

### 1. Clarity value — who cares, and why

**Skill:** Values (`/value`)  
**Saves under:** `workproduct/value-proposition/<slug>/`  
**You get:** customer profile, value map, north-star blurb you can say out loud.

Open this when you can ship but freeze on “why would anyone else care?”

**Try saying:**

> Grill me on a value proposition for my scheduling app.

**Done enough:** profile and value-map gates passed (or bypassed on purpose). Then you have notes you can reuse in every later phase.

### 2. Business value — how the model holds together

**Skill:** BMG (`/bmg`)  
**Saves under:** `workproduct/bmg/<slug>/`  
**You get:** nine-block canvas, then optional patterns, strategy, and ambidextrous execution notes.

Open this when you need classic Osterwalder language: segments, value prop, channels, revenue, costs, partners, and so on. Sticky notes stay short on purpose.

**Try saying:**

> Build a Business Model Canvas for my scheduling app.

**Done enough for the first business return:** canvas-mapper gate passed, or `canvas-mapper.md` on disk. You can keep going into patterns and strategy later.

### 2b. Team alignment value — how the crew stays together

**Skill:** Teams (`/teams`)  
**Saves under:** `workproduct/teams/<slug>/`  
**You get:** a Team Alignment Map first (mission, objectives, commitments, resources, risks). Optional later: assessment, team contract, conflict repair.

Open this when the people building the product are misaligned — not when you need a customer canvas or an MVP cut. Same slug as Values / BMG / lean-mvp.

**Try saying:**

> Our repo team is stepping on each other. Help us align on who owns what.

**Done enough for the first teams return:** tam-planner gate passed, or `tam-planner.md` on disk. Then come back to `/product-spine`. Deeper modules stay available when you reopen `/teams`.

### 3. MVP value — the smallest useful ship

**Skill:** lean-mvp (`/lean-mvp`)  
**Saves under:** `workproduct/lean-mvp/<slug>/`  
**You get:** underserved needs, scoped MVP features, and a path toward tests and metrics.

Open this when clarity is good enough and you need a feature cut that can learn in the market. If Values already has the same slug, lean-mvp can reuse that evidence.

**Try saying:**

> Run the lean MVP playbook for my scheduling app.

**Done enough:** mvp-scope gate passed (or bypassed). Then you are ready to claim or to keep building.

### 4. Claim value — something honest you can share

**Guide:** Product-Spine (`/product-spine`)  
**Uses notes from:** Values, and optionally BMG, Teams, and lean-mvp, under the same slug  
**You get:** an INVEST-style story sentence and, when you want video, a paste block for NotebookLM.

Open this when you want a Discord pitch, showcase write-up, or video prompt. Product-Spine opens your saved notes for you. You should not hunt folders or paste files back into chat.

**Try saying:**

> I want a pitch and NotebookLM prompt for this project.

---

## Small start: one skill only

Pick one kind of value. Install that ship repo. Use one slash. Finish done enough before you add another skill.

| If you need… | Install | Open |
|--------------|---------|------|
| Who / why | `npx skills add rphoward/Values` | `/value` |
| Classic canvas | `npx skills add rphoward/BMG` | `/bmg` |
| Lean MVP cut | `npx skills add rphoward/MVP` | `/lean-mvp` |

Habits that pay off even with one skill:

1. **Name the project once.** Agree the slug early. Reuse it forever for that idea.
2. **Answer one question at a time.** Short sticky-note answers beat essays.
3. **Pass or bypass gates on purpose.** Do not skip by ignoring them.
4. **Leave the notes on disk.** Profile, map, canvas, and MVP files are the durable product of the session.

---

## Medium start: two skills that share a slug

Common pairs:

| Pair | Why |
|------|-----|
| Values → lean-mvp | Clarity first, then a shippable cut from the same customer. |
| Values → BMG | Outward value first, then a fuller business model when you need classic canvas language. |
| BMG alone, then Values | Canvas-first when the work is already “a business,” then tighten who / why. |
| Either grilling skill → Product-Spine claim | Use saved notes for a pitch without rewriting them. |

Rule: **same slug.** Different folder names under `workproduct/` are fine; the project name in each folder should match.

When you feel lost mid-skill, say so. Values, BMG, and lean-mvp can point you back to `/product-spine` after a major gate (or when you ask what is next).

---

## Full path: Product-Spine as the guide

Install the pack when you want one entrance for the whole journey (includes Product-Spine, Values, BMG, lean-mvp, and story):

```bash
npx skills add rphoward/Product-Spine --skill '*' -a cursor -y
```

That pack already carries BMG with the business phase. You can still install BMG alone from [rphoward/BMG](https://github.com/rphoward/BMG) if you only want the canvas skill.

Then open:

```text
/product-spine
```

Product-Spine does **not** grill canvas or lean atoms. It names the phase, names one sibling slash, and tells you when to come back.

### Happy path (one walk among many)

1. `/product-spine` → clarity → `/value` until profile + value map are done enough.  
2. Optional: business → `/bmg` until canvas-mapper is done enough (or you asked for canvas first).  
2b. Optional: team friction → `/teams` until tam-planner is done enough (not required before MVP).  
3. `/product-spine` → mvp → `/lean-mvp` until mvp-scope is done enough.  
4. `/product-spine` → claim → honest story (and NotebookLM paste if you want video).

Lost at any time: `/product-spine` again.

### What “come back when” means

Every clarity / business / mvp guide-turn ends with a return cue. Finish that leg’s done enough (or get stuck), then invoke `/product-spine` again. That is how small legs stack into the larger path without losing your place.

---

## How to get the most out of them quickly

**Match the freeze to the skill.**  
Showcase with no traction → Values.  
Need a board-ready canvas → BMG.  
Need crew alignment → Teams.  
Need a feature cut → lean-mvp.  
Need a pitch or video prompt → Product-Spine claim.

**Do not mix jobs in one turn.**  
Spine routes. Siblings grill. Claim uses notes. Keep those jobs separate and the path stays short.

**Prefer ask over invent.**  
If you already have notes on disk, ask the agent to use them. Product-Spine on claim is built for that.

**Bypass is a decision, not a shortcut you hide.**  
Say you are skipping a module when you skip it. Later skills can still run; you just know what you skipped.

**Keep language outward.**  
Values and claim care what someone else gets. BMG cares how the model works. lean-mvp cares what you ship to learn. Name which hat you are wearing.

**Install only what you will open this week.**  
One skill is enough to start. Product-Spine is for when the path has more than one leg.

---

## Install cheat sheet

| Ship repo | Install | Slash / entry |
|-----------|---------|----------------|
| [Values](https://github.com/rphoward/Values) | `npx skills add rphoward/Values` | `/value` |
| [BMG](https://github.com/rphoward/BMG) | `npx skills add rphoward/BMG` | `/bmg` |
| [MVP](https://github.com/rphoward/MVP) | `npx skills add rphoward/MVP` | `/lean-mvp` |
| [Product-Spine](https://github.com/rphoward/Product-Spine) | `npx skills add rphoward/Product-Spine --skill '*' -a cursor -y` | `/product-spine` (plus siblings in the pack) |

This monorepo ([Value](https://github.com/rphoward/Value)) is where the skills are developed. Prefer the ship repos above for day-to-day install.

### Cursor-only, non-interactive examples

```bash
npx skills add rphoward/Values -a cursor -y
npx skills add rphoward/BMG -a cursor -y
npx skills add rphoward/MVP -a cursor -y
npx skills add rphoward/Product-Spine --skill '*' -a cursor -y
```

---

## What each skill is not for

| Skill | Not for |
|-------|---------|
| Values | Generic requirements lists with no customer / value session. |
| BMG | Lean value-proposition grilling alone, or MVP scoping alone. |
| lean-mvp | Full Strategyzer value canvas work without MVP framing. |
| Product-Spine | Running canvas or lean atoms itself; it only routes and, on claim, follows story with your notes. |

---

## Tiny checklist before you build

1. Pick the **kind of value** you need today (clarity, business, MVP, or claim).  
2. Install that ship repo (or the Product-Spine pack if you want the guide).  
3. Lock a **slug**.  
4. Open the matching **slash**.  
5. Reach **done enough**.  
6. Come back to `/product-spine` when the path has another leg — or stay in one skill if that was enough.

Small ideas first. Same words all the way up.

---

## Standalone install and your own repo

`npx skills add rphoward/Product-Spine --skill '*' -a cursor -y` works without this monorepo. Progress saves under **your** project’s `workproduct/` folders.

Skills do **not** auto-write root `CONTEXT.md` or `AGENTS.md`. Values can emit `CONTEXT.product.md` and `AGENTS.product.md` into the session folder; you promote stable terms into the repo glossary so coding agents keep the same vernacular.

See [for-your-repo.md](for-your-repo.md) and the paste-ready [AGENTS.fragment.md](AGENTS.fragment.md).

