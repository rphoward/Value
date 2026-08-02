# Fresh chat — Resume Value repo after human dogfood

Paste this block when returning from consumer-repo `/product-spine` dogfood.

---

## One-line mission

**Triage human dogfood findings** from live `/product-spine` grilling in a consumer repo. Fix real UX holes in `.cursor/skills/product-spine/SKILL.md` (and siblings if needed), sync ship mirrors, re-run pytest, close `handoff/REPO-ARCHIVE-PAUSE-OPEN.md`.

---

## Preconditions (read first)

1. `handoff/REPO-ARCHIVE-PAUSE-OPEN.md` (this pause gate).
2. `handoff/STATE.md`.
3. `handoff/JOURNEY-UX-TEST-EXPANSION-EXECUTE-PASSED.md` (automated + simulated walks already PASS).
4. Your dogfood notes (decision trail, friction log, or plain prose of what broke).

---

## Context at pause (do not re-litigate)

| Fact | Detail |
|------|--------|
| Value repo | `eb0fe92` on master — journey UX execute committed and pushed |
| Product-Spine pack | `e7a0a56` on main — byte-synced with `skills/product-spine/` |
| Mirrors | `.cursor/skills/*` ↔ `skills/*` byte-identical for all seven skills |
| Tests | 179 passed full suite; 30 passed journey UX spot set |
| Simulation ≠ proof | Execute walks were honest simulations; your live chat is the authority now |
| Historical slugs | Never wipe `shiftswap`, `cashclaw`, `value-design` |

---

## Required walk

1. Read human dogfood notes. Separate **voice/UX bugs** from **preference**.
2. If SKILL wiring holes: minimal fix under `.cursor/skills/`, sync `skills/` mirror, run mirror digest tests.
3. Add or adjust needles only for regressions walks would hit (see plan Slice 1 budget).
4. Re-run: `python -m pytest tests/test_product_spine_skill.py tests/test_maya_happy_pass_lint.py -v` at minimum; full `python -m pytest tests/ -q` if broad changes.
5. Push Product-Spine standalone if spine or sibling ship trees changed.
6. Close `handoff/REPO-ARCHIVE-PAUSE-PASSED.md` (or FAILED with one blocker); update `handoff/STATE.md` + `handoff/README.md`.

---

## Done when

- Dogfood findings triaged (fixed, deferred with dated note, or recorded as acceptable debt).
- Pytest green on touched areas.
- Mirrors and GitHub packs pushed if skill trees changed.
- Archive pause gate closable.

---

## Out of scope unless asked

- Re-running full journey UX execute slices without new evidence
- Appendix Maya one-atom gate
- Wiping journey fixtures or historical dogfood slugs
