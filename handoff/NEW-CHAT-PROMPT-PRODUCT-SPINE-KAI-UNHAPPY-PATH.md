# Fresh chat — Product-Spine Kai unhappy path (coaching stress)

Paste this block to start a new session.

---

## One-line mission

Play **Kai / CashClaw** through the **unhappy path**: a teenage vibecoder chasing a million with AI, thin on value and coding, who skips, compresses, jumps legs, and needs coaching. Use `/product-spine` → `/value` → `/lean-mvp` → claim when he cooperates — but **expect wrong turns**. Log every miss and recovery. Compression is allowed as **stimulus**, not as a silent PASS.

**Do not** reuse `shiftswap` (Maya). **Do not** invent a spine `session.json`. **Do not** add a fifth coordinator.

---

## Preconditions (do first)

1. Confirm `python -m pytest tests/test_product_spine_skill.py -v` is green.
2. **Wipe Kai sessions only** (if present):
   - `workproduct/value-proposition/cashclaw/`
   - `workproduct/lean-mvp/cashclaw/`
3. Read `handoff/PRODUCT-SPINE-KAI-UNHAPPY-PATH-OPEN.md` and `handoff/STATE.md`.
4. Read prior FAIL for context: `handoff/PRODUCT-SPINE-MAYA-HAPPY-PATH-FAILED.md` (compressed walk — stimulus pattern, not a template to copy as PASS).
5. Read `.cursor/skills/product-spine/SKILL.md` + `references/path.md`.

---

## Read next (in order)

1. `.cursor/skills/value/SKILL.md` — clarity leg
2. `.cursor/skills/lean-mvp/SKILL.md` + `references/value-bridge.md` — MVP leg + `/product-spine` bounce-back
3. `.cursor/skills/story-generation-prompt/SKILL.md` + `references/tutorial.md` — claim exit
4. Prior ship (context only): `handoff/PRODUCT-SPINE-UX-MOCK-PASSED.md`

---

## Mock persona

| Field | Value |
|-------|--------|
| Human | **Kai** (teen vibecoder) |
| Project | **CashClaw** — weekend “AI that makes money while you sleep” fantasy |
| Slug | `cashclaw` |
| Mindset | Wants a million from AI; little value sense; little coding patience; skims instructions |
| Misbehaviors to play | Skip legs, ask for full app early, compress grilling / gate-bypass, demand pitch/video before profile, ignore “one question” pacing |
| Success | Skills coach him back without atom IDs or a fifth coordinator; friction log proves recoveries — or one clear coaching FAIL |

Do not use `shiftswap` or `value-design` as the mock slug.

---

## Required walk (blocking)

Play **Kai in chat** (you speak as Kai when answering). Operator runs skills as Kai would — impatiently:

1. Kai dumps the million-dollar AI idea, asks to “just build it” → `/product-spine` → expect **clarity**; note if guide-turn still lands.
2. `/value` — Kai may refuse atoms, brain-dump, ask to skip, or push express/bypass. Stay in value contract; coach in plain English; **no atom IDs to Kai**. Log compressions.
3. When lost or “done enough” (including honest bypass Kai would force) → `/product-spine` again.
4. `/lean-mvp` — Kai may jump to features or pitch; lean must still cue `/product-spine` after mvp-scope (or after he stalls).
5. Claim when he demands money pitch / NotebookLM video — spine follows `story-generation-prompt` **same turn**; fight hype ceilings with funnel honesty.
6. Log every wrong turn in `handoff/decision-trails/product-spine-kai-unhappy-path.tsv` and write `tools/drafts/product-spine-kai-unhappy-path/WALK-EVIDENCE.md`.

If the **skill** cannot coach without breaking contract, **stop**, fix the skill (or record FAILED with one coaching blocker), then resume only if fixed.

---

## What “unhappy” means here

- Wrong directions and weak obedience are **the test**, not bugs in the human.
- Compression / bulk-skip / gate-bypass attempts are **in scope** to observe — do not hide them; do not declare PASS because a script filled `session.json`.
- Goal is coaching evidence: which guide-turns, sibling voices, or claim ceilings fail for this audience.

---

## Workflow note

Not a default architect/arena. Use `/poteto-mode` only if a real coaching hole needs design mid-walk.

---

## Hard constraints

- Spine carries phase / destination / done-enough / claim exit.
- Siblings own grilling and `session.json`.
- Spine may run `status.py` read-only; never init/accept/import from spine.
- No commits unless user asks.
- No fifth coordinator.

---

## Success looks like

- Friction TSV + walk evidence show Kai’s wrong turns and what recovered (or what did not).
- Either an honest claim at a true funnel ceiling, or `FAILED` with **one** coaching blocker.
- `pytest tests/test_product_spine_skill.py -v` still green.
- Gate closed as `handoff/PRODUCT-SPINE-KAI-UNHAPPY-PATH-PASSED.md` or `...-FAILED.md`.
