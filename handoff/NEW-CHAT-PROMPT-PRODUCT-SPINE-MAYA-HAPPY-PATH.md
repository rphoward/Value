# Fresh chat — Product-Spine Maya happy path (full grill)

Paste this block to start a new session.

---

## One-line mission

Play **Maya / ShiftSwap** through the **happy path**: `/product-spine` → real `/value` grilling (profile + value-map) → `/product-spine` → real `/lean-mvp` grilling (through mvp-scope) → `/product-spine` → **claim** with INVEST sentence + NotebookLM producer paste. No gate bypasses. No compressed walk.

**Do not** reuse the prior bypassed `shiftswap` sessions. **Do not** invent a spine `session.json`. **Do not** skip the claim/NotebookLM exit.

---

## Preconditions (do first)

1. Confirm `python -m pytest tests/test_product_spine_skill.py -v` is green.
2. **Wipe prior mock sessions** (they used bypasses):
   - `workproduct/value-proposition/shiftswap/`
   - `workproduct/lean-mvp/shiftswap/` (if present)
3. Read `handoff/PRODUCT-SPINE-MAYA-HAPPY-PATH-OPEN.md` and `handoff/STATE.md`.
4. Read `.cursor/skills/product-spine/SKILL.md` + `references/path.md` (guide-turn contract already shipped).

---

## Read next (in order)

1. `.cursor/skills/value/SKILL.md` — clarity leg
2. `.cursor/skills/lean-mvp/SKILL.md` + `references/value-bridge.md` — MVP leg + `/product-spine` bounce-back
3. `.cursor/skills/story-generation-prompt/SKILL.md` + `references/tutorial.md` — claim exit
4. Prior gate (context only): `handoff/PRODUCT-SPINE-UX-MOCK-PASSED.md`

---

## Mock persona

| Field | Value |
|-------|--------|
| Human | **Maya** |
| Project | **ShiftSwap** — weekend vibecode so restaurant servers trade shifts without group-chat chaos |
| Slug | `shiftswap` |
| Success | Honest INVEST pitch + NotebookLM producer paste without getting lost |

Do not use `value-design` as the mock slug.

---

## Required walk (blocking)

Play Maya in chat. Operator invokes skills as she would:

1. Maya: vibecode idea, feels lost → `/product-spine` → **clarity** guide-turn → open `/value`
2. `/value` — one atom per turn, real answers, no atom IDs to Maya — until **profile + value-map** done-enough (pass or honest bypass only if Maya would truly skip; prefer pass)
3. `/product-spine` → **mvp** guide-turn → open `/lean-mvp`
4. `/lean-mvp` — real answers through **mvp-scope** done-enough; after that gate lean must cue `/product-spine`
5. `/product-spine` → **claim** → read and follow `story-generation-prompt` **this turn** (first story action, then INVEST + NotebookLM producer paste)
6. Log friction in `handoff/decision-trails/product-spine-maya-happy-path.tsv` and write `tools/drafts/product-spine-maya-happy-path/WALK-EVIDENCE.md`

If the walk breaks, **stop and fix the skill contract**, then resume.

---

## Workflow note

Guide-turn arena already closed under the UX mock gate. This session is **dogfood**, not another architect/arena by default. Use `/poteto-mode` only if a real hole appears mid-walk.

---

## Hard constraints

- Spine carries phase / destination / done-enough / claim exit.
- Siblings own grilling and `session.json`.
- Spine may run `status.py` read-only; never init/accept/import from spine.
- No commits unless user asks.
- No fifth coordinator.

---

## Success looks like

- Maya reaches INVEST + NotebookLM paste with real session evidence (no bypass-only walk).
- Friction log + walk evidence written.
- `pytest tests/test_product_spine_skill.py -v` still green.
- Gate closed as `handoff/PRODUCT-SPINE-MAYA-HAPPY-PATH-PASSED.md` (or FAILED with one blocker).
