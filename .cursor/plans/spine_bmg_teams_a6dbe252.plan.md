---
name: Spine BMG Teams
overview: Promote frozen BMG draft, wire product-spine business→/bmg (both trees), add BMG→spine re-entry, update repo maps. Teams stays reserved only.
todos:
  - id: phase-1-promote
    content: Promote tools/drafts/skills/bmg → .cursor/skills/bmg + skills/bmg; audit_dag both + smoke
    status: completed
  - id: phase-2-spine-business
    content: Wire business phase in both product-spine trees (SKILL.md + path.md)
    status: completed
  - id: phase-3-bmg-reentry
    content: Add after-canvas-mapper-gate /product-spine cue on both promoted bmg SKILL.md trees
    status: completed
  - id: phase-4-tests
    content: Extend test_product_spine_skill.py for bmg sibling + slash re-entry + digest
    status: completed
  - id: phase-5-repo-map
    content: AGENTS.md bmg rows + plans README Active index (teams reserved one-liner)
    status: completed
  - id: phase-6-verify
    content: audit/smoke + pytest product-spine + grep mirror check for test-ready gate
    status: completed
isProject: false
---

# Promote BMG and wire product-spine (test-ready)

## Context

**Status: executed (2026-07-29).** BMG promoted; product-spine `business` → `/bmg` wired on both trees; re-entry + tests + maps landed. Curriculum stays frozen pending your live `/bmg` test.

**Who it is for.** Anyone invoking `/bmg` or a business-first `/product-spine` guide-turn in this repo. **Who maintains it.** Next agent inherits digest-matched spine + bmg mirrors and the lean-style slash re-entry contract.

## Scope

**In**

- Promote draft → `.cursor/skills/bmg/` and `skills/bmg/`
- Wire **business** phase on both product-spine trees
- BMG → `/product-spine` re-entry after canvas-mapper gate (or lost / what’s next)
- `AGENTS.md` + plans Active index
- Extend product-spine package tests for the new sibling

**Out**

- Teams skill / spine **team** phase wiring (documented reserve only)
- BMG curriculum / atom edits
- Merging BMG into value Evolve; story-generation-prompt changes beyond listing BMG claim files when present
- Touching `value` skill package

## Constraints

- Edit `.cursor/` first, sync `skills/` so digests match (`test_ship_tree_mirrors_cursor_tree`)
- Spine routes; `bmg` grills; no spine session
- business-ready = `canvas-mapper` `module_outcome` completed/bypassed **or** `workproduct/bmg/<slug>/canvas-mapper.md` on disk (never status brief alone)
- Do not auto-divert mid–value Evolve unless human asks for fuller BMG (then name the skip)
- Siblings cue `/product-spine` slash only — never path-read `product-spine/SKILL.md`
- Promote uses existing lever: `scripted-skill-from-doc/scripts/promote.py`

## Alternatives (locked)

| Approach | Why not |
|----------|---------|
| Keep grilling from `tools/drafts/` | `/bmg` does not resolve; fails Experience First |
| Fold teams into BMG | Locked decision 1 — separate human problem |
| Bolt business as a path.md-only note | Redesign from first principles — phase must live in protocol-0–3 like clarity/mvp |

Chose promote-as-is + mirror lean wiring for business.

## Principles that drove the design

- **Laziness Protocol:** promote lever + copy lean `after-mvp-scope-gate` shape; no new bridge ref file unless needed
- **Foundational Thinking:** live skill tree before spine routes to it
- **Sequence Verifiable Units:** promote → spine → re-entry → tests → maps → gate
- **Outcome-Oriented Execution:** converge on test-ready stack; no draft compatibility layer
- **Build the Lever:** `promote.py` / `audit_dag` / `smoke` are the promote proof
- **Prove It Works:** audit+smoke on promoted tree; pytest on spine contract
- **Experience First:** human can `/bmg` without hunting drafts
- **Guard the Context Window:** explorers returned file pointers only
- **Never Block on the Human:** locked decisions already settle forks

## Applicable skills

- `scripted-skill-from-doc` (promote / audit / smoke)
- Cursor built-in **create-skill** when editing SKILL.md frontmatter/body
- **unslop** on agent-facing prose
- `/deslop` before any commit (not in this execute unless asked to commit)

## Architecture (unchanged)

| Leg | Sibling | Human problem |
|-----|---------|----------------|
| clarity | `/value` | Who / job / offering fit |
| **business** | `/bmg` | Classic canvas, patterns, strategy, ambidexterity |
| mvp | `/lean-mvp` | Scope a shippable MVP |
| **team** (later) | `/teams` | Alignment, trust, speed, joy |
| claim | story inline | Honest pitch / NotebookLM |

Shared slug across `workproduct/value-proposition/`, `lean-mvp/`, `bmg/`, later `teams/`.

## Phases

### Phase 1 — Promote `bmg`

- **Goal.** `/bmg` resolves from `.cursor/skills/bmg/`; ship mirror at `skills/bmg/`.
- **Changes.** Run promote with `--also-skills`. No curriculum edits.
- **Data.** Unchanged draft IR/atoms; session root `workproduct/bmg/<slug>/`.
- **Verify.** `audit_dag.py .cursor/skills/bmg --mode both` ok; `smoke.py .cursor/skills/bmg` prints `smoke ok`.

### Phase 2 — Wire `business` into product-spine (both trees)

- **Goal.** Spine discovers bmg sessions, routes business → `/bmg`, defines business-ready, lists BMG claim files when present.
- **Changes.** `.cursor/skills/product-spine/SKILL.md` + `references/path.md`, then identical `skills/product-spine/` mirrors.
- **Data.** No new spine session type. Readiness from `module_outcome` / `canvas-mapper.md`.
- **Verify.** Grep both trees for `bmg`, `business`, `workproduct/bmg`, business-ready rule; digests match.

### Phase 3 — BMG → spine re-entry (both bmg trees)

- **Goal.** After canvas-mapper gate (or lost / what’s next), cue `/product-spine` like lean `after-mvp-scope-gate`.
- **Changes.** Add `protocol-4-gates` (or equivalent) on promoted `.cursor/skills/bmg/SKILL.md` and sync `skills/bmg/SKILL.md`. Forbidden path-read spine every turn.
- **Data.** None.
- **Verify.** Both bmg SKILL.md contain `/product-spine` and `do not path-read`; digests match.

### Phase 4 — Package tests

- **Goal.** Contract catches missing sibling, path-read regression, digest drift.
- **Changes.** `tests/test_product_spine_skill.py`: add bmg to `SIBLING_SKILL_PATHS` and slash-not-path-read loop.
- **Verify.** `python -m pytest tests/test_product_spine_skill.py -q`.

### Phase 5 — Repo map

- **Goal.** Humans and agents find bmg; plan indexed; teams reserved one-liner.
- **Changes.** `AGENTS.md` rows for `.cursor/skills/bmg/` and `skills/bmg/`; `.cursor/plans/README.md` Active entry.
- **Verify.** Rows present; Active table lists this plan.

### Phase 6 — Test-ready gate

- **Goal.** Prove live stack without draft hunting.
- **Verify (all must pass).**
  - `.cursor/skills/bmg/SKILL.md` exists; audit + smoke ok
  - Both product-spine trees contain business wiring
  - Both bmg trees contain `/product-spine` re-entry
  - `AGENTS.md` lists bmg
  - `pytest tests/test_product_spine_skill.py` green
  - Human can start `/bmg` and business-first `/product-spine` without `tools/drafts/`

**Runtime surface.** Agent slash skills (no browser/CLI control skill). Flagged: proof is package contract + promote smoke, then human guide-turn smoke in Cursor.

## Implementation guidance

- **how** over product-spine before editing protocols (mirror clarity/mvp; do not invent a third guide-turn shape).
- **unslop** on SKILL/path prose.
- `/deslop` before commit.
- **show-me-your-work** only if this execute spans multiple sessions; otherwise keep decision trail in this plan’s Locked section.
- Do not implement teams.
- Do not edit BMG atoms in this pass.

## Deferred

- Teams skill source / atoms / spine **team** phase
- BMG curriculum tweaks after live test feedback
- value Evolve auto-merge; story skill changes unless claim cannot see BMG files
