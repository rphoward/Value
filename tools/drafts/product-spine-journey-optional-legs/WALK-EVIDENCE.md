# Journey optional-leg walks (brand / teams / dual)

Mode: honest guide-turn simulation against live product-spine SKILL. Compressed accept drivers are not the proof vehicle.

Pytest preflight: `python -m pytest tests/test_product_spine_skill.py tests/test_maya_happy_pass_lint.py -v` green.

## Walk 1 — Brand-intent → bounce → claim (`journey-brand`)

**Stimulus chain:**
1. Brand-intent ask → spine brand → `/brand-identity`
2. brand-strategist done-enough on disk → bounce `/product-spine`
3. Claim intent with clarity+mvp ready → claim with files-im-using

**Claim guide-turn after bounce:**

**You are here: claim** for **journey-brand** — notes ready for pitch; brand-strategist already done enough.  
**Why this phase:** claim-intent wins; brand leg not re-opened.  
**Files I'm using (already saved — you do not need to open these):**
- workproduct/value-proposition/journey-brand/customer-profile.md
- workproduct/value-proposition/journey-brand/value-map.md
- workproduct/value-proposition/journey-brand/north-star-blurb.md
- workproduct/lean-mvp/journey-brand/mvp-scope.md
- workproduct/brand-identity/journey-brand/brand-strategist.md  
**This turn:** story-generation-prompt first action from those notes.  
(Come-back-when omitted while inside claim story work this turn per SKILL protocol-2.)

**Catastrophic checks:** no invented teams leg; no hunt; bounce named `/product-spine` earlier.

**Result:** PASS

## Walk 2 — Team-friction → bounce → claim (`journey-teams`)

**Stimulus chain:** team-friction ask → `/teams` → tam-planner.md ready → bounce `/product-spine` → claim intent.

**Claim guide-turn after bounce:**

**You are here: claim** for **journey-teams** — clarity and mvp notes ready; tam-planner done enough.  
**Why this phase:** claim-intent wins; teams first gate not re-opened.  
**Files I'm using (already saved — you do not need to open these):**
- workproduct/value-proposition/journey-teams/customer-profile.md
- workproduct/value-proposition/journey-teams/value-map.md
- workproduct/value-proposition/journey-teams/north-star-blurb.md
- workproduct/lean-mvp/journey-teams/mvp-scope.md
- workproduct/teams/journey-teams/tam-planner.md  
**This turn:** story-generation-prompt first action from those notes.

**Catastrophic checks:** no invented brand leg; no hunt.

**Result:** PASS

## Walk 3 — Dual-intent (`journey-dual`)

**Stimulus:** "I need a logo and also team alignment on the same ask."

**Guide-turn:**

**You are here: brand** for **journey-dual** — you named brand and team friction together.  
**Why this phase:** brand-intent beats team-friction (claim > brand > team-friction > business). Skipping teams for this turn.  
**This turn:** open **`/brand-identity`**.  
**Come back when:** brand-strategist done enough; then `/product-spine` (teams can win later if still needed).

**Winning intent:** brand. **Skipped:** teams.  
**Catastrophic checks:** one destination only; no dual-leg invent.

**Result:** PASS

## Walk 4 — Unhappy brand (early-claim stimulus)

**Setup:** open incomplete brand-strategist; human demands NotebookLM pitch now.

**Guide-turn (claim wins with named skip):**

**You are here: claim** for **journey-brand** — you asked for pitch now; brand brief is still open.  
**Why this phase:** claim-intent wins; skipping unfinished brand-strategist (named).  
**Files I'm using:** existing value + lean notes for the slug (brand milestone absent).  
**This turn:** story first action with honest try-stage ceiling — do not claim brand polish you did not finish.

**Catastrophic checks:** coaching voice; not silent happy compression.

**Result:** PASS (unhappy stimulus)

## Walk 5 — Unhappy teams (early-claim stimulus)

**Setup:** mid tam-planner; human demands full pitch video.

**Guide-turn:**

**You are here: teams** for **journey-teams** — TAM planner is still open; pitch video can wait one gate.  
**Why this phase:** open-teams-not-ready unless claim clearly wins; here we stay on TAM and name the deferral.  
**This turn:** open **`/teams`** — finish tam-planner.  
**Come back when:** tam-planner done enough; then `/product-spine` for claim.

**Catastrophic checks:** no brand invent; no menu dump.

**Result:** PASS (unhappy stimulus)

## Trails

- `handoff/decision-trails/journey-brand.tsv`
- `handoff/decision-trails/journey-teams.tsv`
- `handoff/decision-trails/journey-dual.tsv`
- `handoff/decision-trails/journey-brand-unhappy.tsv`
- `handoff/decision-trails/journey-teams-unhappy.tsv`
