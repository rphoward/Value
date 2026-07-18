# Climb-signal redesign — overview

Back-link: [climb_signal_redesign.plan.md](../climb_signal_redesign.plan.md)

## Context

Scalar `style_fidelity` qualitative-mean climb invites Goodhart. Revisers ornament axes that move the mean while voice and prose lag. Mid-2026 writing training already prefers pairwise rewards, requirement-fine rubrics, and hard verifiable floors (Writing-RL, OpenRS PAMR, WEval/WRL, LitBench). Rubric-based RL still hacks presence checklists when the soft judge is the only stop ruler.

Eliot's 2027 gap is not a better frontier judge. Labs will commodity pairwise APIs, auto-rubrics, and Elo boards. They will still underserve durable author style-blocks, operator-steerable excerpt revise, gaming spans the human can see, and run-folder truth. Crossover is one splice operator under the same accept rule, not a separate product track.

Layout peel and Document Canvas are closed. This plan owns accept/reject and revise unit only.

## Niche durability (check, 2026-07-17)

**Style-block as sole differentiator is fragile.** By mid-2026 the *container* is commodity: Claude Styles/Skills, Custom GPT/Project voice docs, Gemini Gems, Sudowrite Story Bible style samples, Atom-style voice DNA extractors. Labs and products already ingest prose samples or style guides. Academic lines (GRPO author-style rewards, AuthorMix LoRAs, WriterAgent imitation) compress “sound like author X” further through 2027. A Dense Style Block remains a *good input format*, not a moat.

**What can still hold ~12–18 months (into ~2027-07) if we ship this plan:**

1. Operator process climb (excerpt/axis-local, pause, revert, pairwise-vs-best) vs overnight policy training.
2. Hard verifiable floors + content-brief veto that soft judges cannot override.
3. Gaming-visible run-folder + Canvas (cheat spans, accept reasons) vs leaderboard cells.
4. Held-out genuine in the accept loop for *this* author over months.

**What dies first:** “we have compiled style IP others lack.” Treat the block as constitution *for a run*, not as product moat. If the plan ships only a better style-block and keeps mean climb, the niche closes early. If it ships accept + veto + visible process, the niche is process infrastructure, not the markdown file.

**Horizon.** Do not plan past mid-2027 on style-block uniqueness. Re-evaluate niche after phases 03–07 land; if Sudowrite-class or Claude Skills absorb process climb, narrow further to run-folder truth + countable floors only.

## Scope

**Included**

1. Pairwise candidate vs current-best accept (optional vs held-out genuine).
2. Qualitative vector as diagnostic → craft brief, not sole stop ruler.
3. Excerpt- and/or axis-local revise with multi-objective ε-band.
4. Hard veto: Python SURFACE/PROSODY/CAST + content-brief.
5. Gaming-visible Canvas (patch scope, accept reason, revert display) without HTTP score writes.
6. Optional crossover span-splice under the same accept rule.
7. ADR + CONTEXT vocab; gaming regression harness; one dogfood run.

**Excluded**

- Train a lab writing RM.
- Co-evolve rubric generator as MVP.
- Reweight qualitative axes as the fix.
- HTTP writers of `scores.json`.
- Reopen eliotapp homes, SYNTHESIS peel, or full-workflow webapp gate.

## Constraints

- Scores ownership stays CLI/SDK (`climb_recording`, `scores_io`, sdk-climb). Presentation reads + queues jobs only.
- Prefer reuse of `reference_preference` job board + ab/ba side-swap over a third pairwise family.
- Style-block is an immutable meta-rubric for a run. Adaptive criteria instances may come from draft-diff only, not mid-run weight fiddling.
- Migrate mean-as-sole-ruler then delete dual-truth in one wave.
- Small phases; CLI/SDK accept before Canvas polish; crossover last among product operators.
- Decision trail when executing: `handoff/decision-trails/climb-signal-redesign.tsv`.

## Research anchors (July 2026 → 2027 gap)

| Signal | Source | Eliot implication |
|--------|--------|-------------------|
| Pairwise > pointwise for writing rewards | Writing-RL (ACL 2026); UniCreative AC-GenRM | Accept = candidate vs best, not mean delta |
| Pointwise ties hide selection signal | "When LLM Judge Scores Look Good but Best-of-N Decisions Fail" (2026) | Climb is a selection problem; pairwise recovers direction |
| Adaptive criteria from pair diff | OpenRS PAMR | Diff-conditioned criteria instance OK; do not co-evolve generator day one |
| Static rubrics saturate / hack | EvoRubric; Reward Hacking in Rubric-Based RL | Mean of fixed 10 axes will keep gaming |
| Requirement-fine BT | WEval/WRL | Content-brief + axis-local revise beat holistic quality number |
| Creative pairwise ceiling ~73–78% human agree | LitBench | Do not chase ~80 mean ceiling; treat noise as physics |
| Verifiable floors + soft judgment | OpenRS PVR split | SURFACE/PROSODY/CAST + content-brief as veto |

## Alternatives (accept spine)

| Option | Shape | Verdict |
|--------|-------|---------|
| A | Default to existing `reference_preference_v1` | Partial reuse only. Wrong product default for style-block climbs. |
| B | New pairwise-vs-best accept; reuse pref job spine; style-block constitution | **Chosen.** |
| C | Silent semantic swap under `style_fidelity` name | Rejected. Dual-truth and operator confusion. |

## Data shapes (foundational)

- `AcceptDecision` — accepted | rejected | vetoed; reason; challenger; incumbent; optional held-out outcome.
- `PatchScope` — whole_draft | axis | excerpt; target axis ids; span markers when excerpt.
- `HardVeto` — deterministic floor fail and/or content-brief fail; soft judge cannot override.
- Qualitative vector remains on the iteration for craft briefs and Canvas diagnostics.

## Applicable skills / non-negotiables

- **how** before unfamiliar subsystems.
- **interrogate** AcceptDecision before merge.
- **prove-it-works** on fixtures + dogfood artifact, not compile-only.
- **model-the-domain** (AcceptDecision / PatchScope, not more if/else on mean).
- **experience-first** (operator sees cheat spans).
- **laziness-protocol** (reuse preference board; no third pairwise stack).
- **sequence-verifiable-units** (harness red → accept green → retire mean).
- **show-me-your-work** decision trail on execute.
- `/deslop`; **unslop**; **babysit** after PR.
- **control-cli** / **control-ui** for surface smoke.

## Phases

1. [phase-00-harness.md](phase-00-harness.md)
2. [phase-01-accept-types.md](phase-01-accept-types.md)
3. [phase-02-hard-veto.md](phase-02-hard-veto.md)
4. [phase-03-pairwise-accept.md](phase-03-pairwise-accept.md)
5. [phase-04-retire-mean-ruler.md](phase-04-retire-mean-ruler.md)
6. [phase-05-revise-unit.md](phase-05-revise-unit.md)
7. [phase-06-epsilon-band.md](phase-06-epsilon-band.md)
8. [phase-07-canvas-gaming-ux.md](phase-07-canvas-gaming-ux.md)
9. [phase-08-held-out-anticheat.md](phase-08-held-out-anticheat.md)
10. [phase-09-crossover.md](phase-09-crossover.md)
11. [phase-10-closeout.md](phase-10-closeout.md)

[testing.md](testing.md)

## Verification (project-level)

```powershell
$env:PYTHONPATH="."
python -m pytest tests/ -q
```

Done predicate for the *plan*: this directory exists and covers handoff protocol-3 items. Done for *implementation*: harness green; mean retired as sole ruler; dogfood run shows pairwise accept reasons on disk; HTTP still never writes `scores.json`.

## Open questions (human preference only)

1. New metric id name (`pairwise_style_v1` vs superseding `style_fidelity` with an ADR version bump). Recommendation: new id + migrate init default.
2. Deterministic floor thresholds per SURFACE/PROSODY/CAST (fixed numbers vs relative ε from incumbent). Recommendation: relative ε from incumbent first; absolute floors only if dogfood demands.
3. Whether crossover ships in the first merge PR or a stacked follow-up. Recommendation: stacked after Canvas UX so accept path stays reviewable.
