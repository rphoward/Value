# Fresh chat — Journey UX test expansion (plan only)

Paste this block to start a new session.

---

## One-line mission

**Write a plan** (not the suite yet) to expand end-user experience coverage across `/product-spine` and every grilling sibling — happy paths, unhappy paths, optional legs (teams, brand-identity, bmg), bounce/claim, and cold re-entry — so vibecoders get a good path. Stop when the plan is ready for human acceptance.

---

## Preconditions (read first)

1. `handoff/JOURNEY-UX-TEST-EXPANSION-OPEN.md` (this gate).
2. `handoff/STATE.md`.
3. Prior walk lessons (method, not redo):
   - `handoff/PRODUCT-SPINE-MAYA-HAPPY-PATH-FAILED.md` — compressed bulk-accept ≠ happy PASS
   - `handoff/PRODUCT-SPINE-KAI-UNHAPPY-PATH-PASSED.md` — coaching stress done right
   - `handoff/PRODUCT-SPINE-UX-MOCK-PASSED.md` — guide-turn contract
   - `handoff/PRODUCT-SPINE-COLD-RESTART-OPEN.md` — still open; fold or keep separate in the plan
4. Live siblings: `.cursor/skills/{product-spine,value,bmg,teams,brand-identity,lean-mvp,story-generation-prompt}/SKILL.md`
5. Current automated surface: `tests/test_*.py` (inventory; do not assume gaps without listing files).

---

## Context from prior work (do not re-litigate)

| Fact | Detail |
|------|--------|
| Brand + spine | Promoted; brand phase wired; Product-Spine pack `e7a0a56` ships `brand-identity` |
| Maya | FAIL on method (compressed walk). Optional true one-atom retry later — do not revive PASSED |
| Kai | PASS unhappy-path coaching stress (`cashclaw`) |
| Tests today | Strong on packages/DAGs/scripts; thin on full-journey UX across new siblings |
| This chat | **Plan only** — no implementing the expansion until human accepts the plan |

---

## Required walk

1. Inventory `tests/` and prior handoff walks; build a coverage matrix (sibling × path-kind × test-kind → exists / missing).
2. Propose ordered slices (smallest useful first). Prefer spine routing + optional brand/teams legs before a full Maya-style happy retry.
3. Name pass/fail rules (Maya/Kai lessons), persona/slug policy, wipe rules, and verification commands per slice.
4. Write the plan under `.cursor/plans/` (or ask once if another path is preferred).
5. Halt for human acceptance. Do **not** start implementing in this session unless the human explicitly says to execute after accepting.

---

## Done when

- A written plan exists with matrix + slices + rules + out-of-scope.
- Human can accept, edit, or reject it.
- Gate closable as PASSED (plan accepted) or left OPEN / FAILED with one blocker.

---

## Out of scope unless asked

- Implementing the full test/walk suite in the same chat as the plan
- Shared-runtime consolidation across paced skills
- Separate Brand Identity solo GitHub repo
- Compiler / scripted-skill-from-doc authoring tests (keep as adjacent, not journey UX)
