# Maya / ShiftSwap UX walk evidence (compressed)

Slug: `shiftswap`
Mode: compressed gate bypasses after guide-turn dogfood (full canvas grilling deferred; phase machine + claim exit proven)

## Leg 1 — clarity (no prior session)

**Spine guide-turn (winning A+grafts voice):**

You are building ShiftSwap — servers trading shifts without group-chat chaos — and you have not started the value canvases yet. **You are here: clarity** (no value session under `shiftswap` yet). Value comes first so lean MVP features sit on a named customer and problem, not on vibe alone. **This turn:** open **`/value`** once; work through customer profile and value map at your own pace. **Come back when:** profile and value map are done enough (passed or bypassed), or you are lost; then run **`/product-spine`** again.

**Friction:** none on destination. Two-slash tax felt once (expected).

**Session action:** init value `shiftswap`; bypass profile + value-map for speed (`module_outcome` = bypassed both).

## Leg 2 — mvp (clarity-ready)

**Spine guide-turn:**

**You are here: mvp** for **shiftswap** — value profile and value map are done enough, and lean MVP scope is still open. **This turn:** open **`/lean-mvp`** (same slug). **Come back when:** mvp-scope is done enough, or you stall; invoke **`/product-spine`** again for claim.

**Session action:** init lean `shiftswap`; bypass customer-context, underserved-needs, mvp-scope.

**Lean bounce-back check:** `references/value-bridge.md` `forward-claim` now tells Maya to invoke `/product-spine` after mvp-scope.

## Leg 3 — claim (mvp-ready + pitch/NotebookLM intent)

**Spine guide-turn opening into story (first action):**

**You are here: claim** for **shiftswap** — clarity and MVP scope are done enough, and you want an honest pitch plus NotebookLM. I am following **story-generation-prompt** in this thread, not sending you to another slash.

**First story action:** In one breath, what does ShiftSwap do for a restaurant server trading a shift, and what must stay true for that to be honest? (NotebookLM pass-1 style)

**Maya (mock answer):** Servers trade open shifts with coworkers without drowning the group chat; honest only if it still works when the manager is offline and nobody wants a new payroll system.

### Claim artifacts (story-to-prompt order)

**User story (one sentence)**  
As a restaurant server who needs to trade a shift tonight, I want to post and claim open shifts with coworkers without flooding the group chat, so that coverage is clear without buying a new tablet workflow for the manager.

**Generation prompt**  
Produce a 3–5 minute overview for restaurant servers and shift leads about ShiftSwap: a weekend tool for posting and claiming open shifts with coworkers so trades stay out of chaotic group chats. Stay honest: manager can stay offline; no payroll or scheduling-system replacement. Stress the pain of missed trades and unread chat threads. Avoid inventing analytics, POS integrations, or multi-location HQ features.

**Producer paste block (NotebookLM pass 2)**  
```
Audience: restaurant servers and shift leads who trade shifts by text/group chat.
Core job: post and claim an open shift with a coworker without chat chaos.
Must stay true: works when the manager is offline; not a payroll or full schedule system.
Tone: practical, weekend-built, no enterprise pitch.
Length: short overview (about 3–5 minutes).
Do not invent: POS, payroll, multi-site HQ dashboards, or unvalidated ROI numbers.
```

**INVEST-plus (honest for mock):** Independent yes · Negotiable yes · Valuable yes (stated pain) · Estimable thin (gates bypassed) · Small yes · Testable yes (one trade without chat). Kill signal: if servers still paste trades into the group chat after two busy weekends.

## Friction log
- Compressed walk skipped real grilling — claim evidence is persona-stated; full grill would harden Estimable.
- No orphan “which skill?” after lean thanks to forward-claim.
- Claim did not dump to a third slash.

## Tests
`python -m pytest tests/test_product_spine_skill.py -v` → 9 passed
