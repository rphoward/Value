# Candidate B — Bounce-back guide-turn (lean re-entry + readiness rules)

**Emphasis:** Fix the post-lean orphan and stop agents confusing `status.py` active module with done-enough. Claim stays inlined; do not overbuild claim choreography.

## Problem

Maya can name a door and still get lost: lean-mvp never points her back to `/product-spine`, spine replies can sound like triage-and-abandon, and agents may treat status brief “active module” as readiness. She needs a phase machine with a fixed guide-turn shape and a sibling bounce-back line — not a fifth coordinator or a spine ledger.

## Usage (caller's view)

Maya invokes `/product-spine` whenever she starts, finishes a leg, or is lost. Every spine reply uses the same four beats: you-are-here, one destination, done-enough, return cue. On clarity/mvp she opens `/value` or `/lean-mvp` and comes back when that leg’s done-enough holds. On claim, spine does not dump her — it reads and follows `story-generation-prompt` in that turn. After lean mvp-scope is done-enough (or she is lost mid-lean), lean itself tells her to return to `/product-spine`.

## Shape

### Guide-turn utterance contract (spine)

Fixed order, short prose, no atom IDs, no status stdout:

1. **You-are-here** — phase name + one plain sentence why this phase won (precedence + readiness).
2. **Destination** — exactly one: `/value`, `/lean-mvp`, or “following story-generation-prompt now.”
3. **Done-enough** — what must be true before the next `/product-spine` (or claim done-enough).
4. **Return cue** — when done-enough or lost, invoke `/product-spine` again (omit only while already inside claim work in this turn).

### Readiness derivation (spine-only rules)

| Flag | Rule |
|------|------|
| `clarity-ready` | value `profile` and `value-map` `module_outcome` are each `completed` or `bypassed` |
| `mvp-ready` | lean `mvp-scope` `module_outcome` is `completed` or `bypassed`, **or** human explicitly skips lean and asks to claim |
| status brief | read-only hint for which module is open — **never** a readiness input |
| missing session | that leg is not ready |

Phase choice still follows existing precedence: claim-intent wins; else prefer value until clarity-ready; else lean; claim when both ready or repo-claim ask.

### Sibling bounce-back (minimal lean edit)

When lean hits mvp-scope done-enough, or the human is lost / asks where next, lean closes with one line naming `/product-spine` as the next guide turn (claim or return-after-learning). Optional mirror on value when profile+value-map done-enough — only if mocks show the same orphan after clarity.

### Data

Journey phases `{clarity, mvp, claim, return-after-learning}` + sibling sessions under shared slug. No spine `session.json`. No new ledger.

## Tradeoffs accepted

- Two-slash tax stays: spine names the sibling, sibling does the grilling.
- Lean gets a tiny re-entry sentence; spine does not absorb lean pacing.
- Claim is “follow story skill now,” not a multi-beat story orchestra inside spine.
- Agents must open `session.json` (or outcomes via status + session) for readiness — brief alone is insufficient by design.

## Alternatives considered (rejected)

| Alternative | Why reject |
|-------------|------------|
| Fifth coordinator / subagent | Violates grounding; adds handoff tax Maya does not need |
| Spine `session.json` | Duplicates sibling truth; invents a ledger we forbade |
| Tips-list / receptionist triage | Names a door, orphans her; fails Experience first |
| Heavy claim inline choreography (multi-step story machine in spine) | Overbuilt vs gap #1; story skill already owns INVEST/NotebookLM |
| Readiness from status “active module” | Confuses position with gates; known UX gap #4 |
| Auto-init / accept from spine | Forbidden; siblings own atoms |

## Open questions and risks

- Does value need the same bounce-back line, or is lean the only proven orphan?
- If sessions exist under several slugs, one clarifying question still required — bounce-back does not fix multi-slug ambiguity.
- Claim-intent while lean mid-module: spine must say what is skipped; human may feel whiplash if bounce-back and claim-intent fire in the same weekend.

## Next implementation step

Patch `.cursor/skills/product-spine/SKILL.md` protocol-2 (+ path.md voice) to mandate the four-beat guide-turn and the readiness-from-`module_outcome` rule; add one lean-mvp exit sentence pointing to `/product-spine`; digest-match `skills/product-spine/`.

## Synthesis decision

(filled by parent)
