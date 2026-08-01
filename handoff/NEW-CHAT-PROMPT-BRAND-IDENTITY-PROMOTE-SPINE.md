# Fresh chat — Brand-identity promote + product-spine wire

Paste this block to start a new session.

---

## One-line mission

**Promote** `tools/drafts/skills/brand-identity/` into `.cursor/skills/brand-identity/`, **wire** it into product-spine (teams-like optional brand leg), **retest**, then optionally **/thermos** the live `.cursor/skills` tree while skipping `scripted-skill-from-doc`, `story-generation-prompt`, and `verify-value`.

---

## Preconditions (read first)

1. `handoff/BRAND-IDENTITY-PROMOTE-SPINE-OPEN.md` (this gate).
2. Draft root: `tools/drafts/skills/brand-identity/` — **this is the only brand-identity skill today**. Live `.cursor/skills/brand-identity/` does not exist yet.
3. Source suite: `docs/designing-brand-identity-prompt-suite.md`.
4. Promote / audit CLIs: `.cursor/skills/scripted-skill-from-doc/references/for-agents.md`.
5. Spine pattern to copy: how `teams` is woven in `.cursor/skills/product-spine/SKILL.md` + `references/path.md` (optional intent, done-enough = first module gate, bounce to `/product-spine`).

---

## Context from prior session (do not re-litigate)

| Fact | Detail |
|------|--------|
| Why missing from `/` palette | Never promoted — draft only under `tools/drafts/skills/brand-identity/` |
| Compile nested fences | Fixed via `extract_fenced_block` in compile.py (already on master) |
| Thermos on draft | Functional hazards fixed (express spine park, prior-module ready, drafts repo root, scoped Unknowns, Values CLI scrub); template under scripted-skill-from-doc synced |
| Session-runtime template | Authoring cookie for scaffolds only — **not** installed by Product-Spine npx pack |
| Structural debt left | Shared ~833-line runtime.py fork across paced skills — do not block promote on a full shared-runtime rewrite |

---

## Required walk

1. Re-run audit + smoke on the **draft** path; fix only if broken.
2. Promote (human already asked via this handoff):

```text
python .cursor/skills/scripted-skill-from-doc/scripts/promote.py tools/drafts/skills/brand-identity
```

Add `--also-skills` only if a `skills/brand-identity/` ship mirror is wanted.

3. Wire product-spine:
   - Sibling `brand-identity`
   - Optional `brand` phase + `brand-intent`
   - `brand-ready` = brand-strategist gate / `brand-strategist.md`
   - Discover `workproduct/brand-identity/*/session.json`
   - Claim optional brand milestones
   - Update `docs/skill-journey.md` + `AGENTS.md`
   - Keep digest mirror `skills/product-spine/` in sync if that is how this repo ships

4. Retest:
   - `python -m pytest tests/test_brand_identity_thermos_fixes.py tests/test_prompt_suite_compile.py tests/test_prompt_suite_compile_gate_ux.py -q`
   - Smoke **live** `.cursor/skills/brand-identity`
   - Spot-check product-spine guide-turn for brand-intent → `/brand-identity` + Come-back-when `/product-spine`

5. Optional thermos: scope `.cursor/skills/{product-spine,brand-identity,value,bmg,teams,lean-mvp}` only. **Skip** `scripted-skill-from-doc`, `story-generation-prompt`, `verify-value`.

6. Close gate PASSED/FAILED with one blocker.

---

## Done when

- `.cursor/skills/brand-identity/SKILL.md` exists and is the promoted skill.
- Product-spine routes brand-intent and lists the sibling.
- Retest evidence named (pytest / smoke / spine spot-check).
- Gate closed as PASSED or FAILED.

---

## Out of scope unless asked

- Shared-runtime consolidation across value/bmg/teams/lean
- Shipping a separate GitHub Brand Identity pack / npx name
- Reworking story-generation-prompt or verify-value
- Rewriting scripted-skill-from-doc beyond what promote needs
