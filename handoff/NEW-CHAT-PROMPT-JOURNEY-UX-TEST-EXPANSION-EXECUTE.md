# Fresh chat — Journey UX test expansion (EXECUTE)

Paste this block to start a new session.

---

## One-line mission

**Execute** the accepted plan in [`.cursor/plans/journey_ux_test_expansion_ff27e8a7.plan.md`](../.cursor/plans/journey_ux_test_expansion_ff27e8a7.plan.md) slice by slice. Prove day-one and day-two vibecoder paths still work after brand/teams/bmg joined the pack. Stop only for real blockers or human gates between heavy walk slices if needed.

---

## Preconditions (read first)

1. `handoff/JOURNEY-UX-TEST-EXPANSION-EXECUTE-OPEN.md` (this gate).
2. `.cursor/plans/journey_ux_test_expansion_ff27e8a7.plan.md` (accepted plan — source of truth for slices, Verify, slug policy).
3. `handoff/JOURNEY-UX-TEST-EXPANSION-PASSED.md` (plan acceptance evidence).
4. `handoff/STATE.md`.
5. Method lessons (do not redo as proof):
   - `handoff/PRODUCT-SPINE-MAYA-HAPPY-PATH-FAILED.md` — compressed bulk-accept ≠ happy PASS
   - `handoff/PRODUCT-SPINE-KAI-UNHAPPY-PATH-PASSED.md` — coaching stress done right
   - `handoff/PRODUCT-SPINE-COLD-RESTART-OPEN.md` — Slice 2 vehicle (value-only; do not dilate)

---

## Context (do not re-litigate)

| Fact | Detail |
|------|--------|
| Plan | Accepted 2026-08-01; poteto critique + day-two multi-leg edits applied |
| Brand + spine | Live; Product-Spine pack `e7a0a56` |
| Maya | FAIL on method — do not revive PASSED; appendix only if human asks |
| Slugs | Never wipe `shiftswap`, `cashclaw`, `value-design` |
| This chat | **Execute** — not another planning round |

---

## Required walk

1. Follow plan §4 slice order (S1 → S7). Update plan todos as each slice completes.
2. Slice 1 first: minimal needles + Maya encode lint; `pytest tests/test_product_spine_skill.py -v` green.
3. Slice 2: close value-only cold restart via `PRODUCT-SPINE-COLD-RESTART-OPEN` verbatim.
4. Slice 3: day-two multi-leg (`journey-day2`) — open incomplete brand/teams, done-enough bounce cold, warm where-am-I.
5. Continue S4–S7 per plan Verify commands and per-walk done-criteria template.
6. Appendix Maya only if human still wants it after S2–S4 — separate gate, not required for EXECUTE PASS.
7. Close `handoff/JOURNEY-UX-TEST-EXPANSION-EXECUTE-PASSED.md` (or FAILED with one blocker); update `handoff/STATE.md` + `handoff/README.md`.

---

## Done when

- Slices 1–7 complete with evidence (pytest + trails/WALK-EVIDENCE where the plan requires walks).
- Cold-restart gate closed (PASSED or FAILED) under Slice 2.
- EXECUTE gate closable as PASSED (or FAILED with one blocker).
- Historical slugs untouched.

---

## Out of scope unless asked

- Re-planning the coverage matrix
- Shared-runtime consolidation
- Solo Brand Identity GitHub repo
- Compiler / scripted-skill-from-doc authoring tests
- Reviving Maya PASSED or wiping historical dogfood slugs
