# Skill delta — candidate A (minimal)

## `.cursor/skills/product-spine/SKILL.md`

- **Add `protocol-2-guide-turn`** (after or nested under voice): mandate four slots on every activation — **You are here**, **Why this phase**, **This turn**, **Come back when** — with one-line definitions matching `usage-mocks.md` tone.
- **Extend `protocol-2-voice` `(forbidden ...)`** or add **`(illegal-replies ...)`** listing: stop after naming sibling on clarity/mvp; claim turn that only routes to story skill; lean before clarity-ready without explicit skip + stated cost; readiness from status brief; any sibling init/accept/import/refresh from spine.
- **Tighten `protocol-0-activation` step 5–6:** step 5 claim must **read and follow** story-generation-prompt **before** the turn ends; step 6 clarity/mvp must populate **This turn** with exactly `/value` or `/lean-mvp` plus leg purpose; forbid step 6 phrasing on claim phase.
- **Add one sentence under `protocol-1` claim phase:** “Claim turns execute story-generation-prompt inline; routing-only claim is forbidden.”
- **Optional:** in `protocol-1` `(return-after-learning ...)`, require **This turn** to name one sibling slash and why learning belongs there (no dual destinations).

## `.cursor/skills/product-spine/references/path.md`

- **`(section voice)`:** rename or extend slots to match guide-turn four fields; add **`(check guide-turn-complete "every activation emits all four slots")`**.
- **Add `(check illegal-claim-route "claim phase forbids 'open story-generation-prompt' without following SKILL in same turn")`** alongside existing `claim-exit`.
- **`(section reading-sibling-state)`:** one explicit line — “status brief = active module only; clarity-ready / mvp-ready = module_outcome completed|bypassed only.”
- **`(section maya-happy-path)`:** annotate each step with the four slot labels as a reference walk (no new steps).

## `skills/product-spine/` ship mirror

- Same edits as above after `.cursor` copy is stable (digest-match per repo convention).

## lean-mvp — `/product-spine` re-entry?

**Yes.** One line only, not a full spine reread every module.

- **Where:** `.cursor/skills/lean-mvp/SKILL.md` — in the **mvp-scope / MS05 / journey completion** prose (wherever “done with scope” or “what’s next after MVP scope” is already stated; if no such block, add a short **`(note spine-re-entry ...)`** under the skill’s central workflow exit, not on every atom).
- **Wording intent:** “When mvp-scope is done enough (or bypassed), invoke **`/product-spine`** to continue to claim (INVEST + NotebookLM) — lean does not own the shareable pitch.”
- **Forbidden in lean delta:** do not `read product-spine/SKILL.md` each turn; do not duplicate phase machine (pointer only).

## Explicitly out of scope for this delta

- Spine `session.json`, new scripts, walk harness changes.
- value skill edits (unless parent synthesis finds mock gap).
- story-generation-prompt body changes (spine obligation only).
