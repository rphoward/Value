# Arena task: design the lean-mvp coaching layer

Produce a **design sketch**, not an implementation. Types, JSON schemas with two or three filled
example entries, function signatures with `raise NotImplementedError` bodies, a module map, and prose
rationale. Do not author all 32 coaching entries and do not edit any file under
`.cursor/skills/` or `skills/`.

Read `tools/drafts/lean-mvp-coaching/grounding.md` first, in full. It is verified against the repo.
Read the real files it names before you design; do not design from the grounding summary alone.

## What the layer has to do

`.cursor/skills/lean-mvp/scripts/next_question.py` prints one JSON payload per interview turn. An
agent reads that payload and asks the human one question. Today the payload teaches nothing, so the
human gets ambushed by a compound question whose vocabulary was never defined, even though the
definitions ship in `assets/knowledge-base.json`.

Design a coaching layer so that a single `next_question.py` invocation returns everything the agent
needs to deliver a teaching turn: what the concept means, what a complete answer contains, a worked
example, the common mistake, and the prior answers this question builds on. The agent must not need
a second file read to compose the turn.

Concretely, in scope for your sketch:

1. A new asset `assets/atom-coaching.json`, keyed by atom id, covering all 32 atoms. Design the entry
   schema. The plan that preceded you proposed
   `{why_it_matters, kb_refs, reads, slots, worked_example, common_miss}`. Treat that as a starting
   proposal to improve, not a fixed contract. Show two or three real filled entries: one content atom,
   one gate atom, and MS05 (the compound INVEST-story atom that caused the original stall).
2. Where the resolution logic lives and its signature. `kb_refs` names existing top-level
   `knowledge-base.json` keys; the payload must carry the resolved content, not the key names. Note
   that knowledge-base values come in four different shapes (plain string, object with
   `definition`/`example`, list of strings, nested object) and your resolver has to survive all of
   them.
3. What replaces the dead `match_board_for_atom` / `MATCH_BOARD_ATOMS` machinery. It is verifiably
   dead in lean-mvp and still speaks the value skill's vocabulary. Deleting it and building an
   evidence board from the coaching entry's prior-answer list is one option; rewriting it in place is
   another. Argue your choice.
4. The exact `coaching` key shape added to the `next_question.py` payload, written as a JSON example
   of a real turn.
5. The `protocol-3-turn-recipe` delivery order in `SKILL.md` that makes the agent actually use it.
   Keep one question per turn.

Out of scope: splitting MS05 into two atoms, fixing the `_session` `sys.modules` collision, authoring
all 32 entries, any change under `skills/story-generation-prompt/`.

## Graded on

1. **Turn-completeness of the payload.** Could an agent holding only this JSON deliver the teaching
   turn, with real definition text rather than key names, and with the prior answers' actual text?
2. **Placement and subtraction.** Resolution logic lives in `scripts/_session/` and
   `next_question.py` stays a thin entrypoint (`.cursor/rules/skills-repo.mdc` forbids fat scripts).
   Net lines removed counts in your favor. A new module under `_session/` must be argued for, not
   assumed.
3. **Boundary behavior.** What the payload does when a coaching entry is missing, a `kb_refs` key does
   not resolve, or a prior-answer atom is unanswered or holds a ceremony answer. The interview has to
   keep running.
4. **Machine-checkability.** A test can validate coverage, `kb_refs` validity, and prior-answer DAG
   ordering **without importing `_session`** (see the collision in the grounding). Say what the test
   asserts against what.
5. **Maintainer cost.** What a person does to add a 33rd atom, and what tells them they forgot the
   coaching entry.

## Deliverables, written to your assigned output directory

- `design.md`: the sketch. Caller usage first (the JSON a real turn returns, and the paragraph the
  agent would say to the human from it), then schemas, then signatures with
  `raise NotImplementedError`, then the module map.
- `rationale.md`: alternatives you considered and rejected, and why. Name what you would cut if
  forced to halve the diff.

Both files stay under 400 lines total. Be concrete. A sketch that hand-waves the resolver's handling
of the four knowledge-base value shapes fails criterion 1.
