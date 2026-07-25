# Rationale

## Rejected

**Derive `builds_on` from the DAG.** Zero maintenance, and it was my first instinct. It fails because
`requires` is a single-predecessor chain, so it yields exactly one prior atom per turn. MS05 needs
three, from three different modules (persona for the As-a clause, focus benefit for the so-that
clause, the delighter call the story must respect). The chain gives MS04 alone. Hand-authored
`builds_on` earns its place because the connective `why` clause is not derivable either.

**Widen `invest_user_story_rubric` in `knowledge-base.json`.** The grounding is right that widening
survives `test_story_card_invest_letters_match_lean_mvp_rubric`, which compares keys only. Rejected
anyway. The knowledge base is a shared fact table with a second reader in another skill, and the
guidance MS05 needs is turn-specific, not a fact about INVEST. It belongs in the coaching entry.

**Rewrite `MATCH_BOARD_ATOMS` in place for lean-mvp atoms.** That produces a second per-atom
prior-answer table next to `builds_on`, two structures with one job, and a maintainer who has to know
which one a given turn reads. The board's live half, pull prior answer text and skip ceremony rows,
is exactly what `_resolve_prior` does, for every atom instead of two.

**Put the resolver in `voice.py`.** `voice.py` is text shaping over an already-loaded session. The
resolver loads an asset, walks a JSON tree, and reads the session, so it spans `catalog`, `runtime`,
and `voice` and has no existing home. `coaching.py` is the only reader of `atom-coaching.json` and
the only writer of the `coaching` key, so the file boundary matches the asset boundary. This is the
weakest of my calls. If a reviewer rejects the new module, the six functions go at the bottom of
`voice.py` and nothing else changes.

**Return the raw knowledge-base subtree instead of flattened lines.** Cheaper resolver, but it moves
the four-shape problem into the agent's prompt every turn and makes payload readability depend on
which key an entry happened to cite. Flattening once, in one recursive function, is the trade.

**Omit the `coaching` key when there is no entry.** An agent that branches on key absence will
eventually forget. A total key with `status: "missing"` gives one render path and makes the fallback
to `asks` plus `accepts_summary` the same code path as a partially-resolved turn.

**Filter unresolved `kb_refs` out of the payload.** Hides a typo from anyone reading a live session.
The resolver reports, `SKILL.md` decides what is spoken, and the asset test catches the typo in CI.

**A `kind: "gate" | "content"` field on entries.** `atoms.json` already sets `gate: true`, and a
second source of truth for one fact is a drift bug waiting. Gate entries carry `kb_refs: []` instead.

**Run `builds_on` text through `split_sticky_items`, and cache the knowledge base.** The consumer is a
language model reading JSON, not a rendered card, so raw trimmed text skips a regex. And
`next_question.py` reads one payload and exits, so there is nothing to cache across.

**Front-load `common_miss`.** A warning about a mistake nobody has made yet turns a four-beat turn
into a lecture, and the operator who stalled 22 hours stalled on being overwhelmed, not underwarned.

## Sequencing

Two commits, not one. First a pure deletion of the value-shaped dead code in `voice.py` and
`constants.py`, behavior-preserving and proved by the suite's 100 current passes holding at 100.
Then the coaching layer on the smaller base. Folding them makes the coaching diff unreadable and
makes the deletion unreviewable.

## What I would cut to halve the diff

The `concepts` resolver, and with it `kb_refs`. It is most of `coaching.py` and all of the four-shape
handling. The remaining entry, `teach` plus `answer_shape` plus `worked_example` plus `common_miss`
plus `builds_on`, still fixes the MS05 stall on its own, because the operator was not blocked by the
absence of the six INVEST words. They were blocked by not knowing what a complete answer contained.
Hand-written `teach` text covers the vocabulary for the handful of atoms where it matters. What is
lost is the guarantee that the definition in the turn matches the definition in the knowledge base,
which is exactly the drift the resolver exists to prevent. Worth keeping if the budget allows,
first to go if it does not.

## The riskiest part

Not the code. It is that the whole layer rests on 32 hand-written prose entries whose quality no test
can grade. Every check I proposed asserts presence, resolution, and DAG ordering. None of them can
tell a `worked_example` that teaches from one that fills the field, and a payload that is structurally
perfect and full of mediocre prose delivers the same ambush the layer was built to stop, while
reporting `status: "ok"`. The failure is quiet and it degrades one entry at a time as maintainers add
atoms in a hurry. I chose an authored asset over a derived one deliberately, so this risk is mine.
The only real mitigation is to write and test-drive a handful of entries against a live session
before authoring the other twenty-something, rather than filling all 32 in one pass.
