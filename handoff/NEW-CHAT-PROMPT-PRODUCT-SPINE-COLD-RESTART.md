# Fresh chat — Product-Spine cold restart (progress so far)

Paste this block to start a new session.

---

## One-line mission

Prove **cold restart**: close any prior chat, open a **new** chat, invoke only `/product-spine` against the existing **`value-design`** notes. Pass if **You are here** names **progress so far** in plain words before asking the human to hunt or paste files.

**Do not** wipe `value-design`. **Do not** invent a spine `session.json`. **Do not** add a fifth guide-turn beat.

---

## Preconditions (do first)

1. Confirm `python -m pytest tests/test_product_spine_skill.py -v` is green.
2. Confirm notes exist (do not delete):
   - `workproduct/value-proposition/value-design/session.json`
   - prefer also `customer-profile.md` / `value-map.md` when present
3. Read `handoff/PRODUCT-SPINE-COLD-RESTART-OPEN.md` and `handoff/STATE.md`.
4. Read `.cursor/skills/product-spine/SKILL.md` + `references/path.md` (progress-so-far contract).

---

## Mock persona

| Field | Value |
|-------|--------|
| Human | Returning vibecoder (closed chat yesterday) |
| Project | Existing **value-design** workproduct |
| Slug | `value-design` |
| Ask | Only `/product-spine` — no dump, no paste homework |
| Success | Guide-turn you-are-here includes **progress so far**; no status stdout / strip symbols; no file hunt |

---

## Required walk (blocking)

1. New chat. Invoke `/product-spine` once.
2. Score the first guide-turn:
   - **PASS signal:** You-are-here names phase + slug + **progress so far** in plain words (translated from `--sections`, not raw strip).
   - **FAIL signal:** Amnesiac phase-only line; asks human to find/paste profile/map; quotes status stdout; invents a fifth beat.
3. Log friction in `handoff/decision-trails/product-spine-cold-restart.tsv`.
4. Close as PASSED or FAILED with one blocker.

---

## Done when

- Cold-restart turn carries progress so far without file hunt, **or** one clear FAIL with blocker.
- `pytest tests/test_product_spine_skill.py -v` still green.
