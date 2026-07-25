# Rationale

## Decision: delete match-board, do not rewrite it

`MATCH_BOARD_ATOMS` is `{}`. `match_board_for_atom` returns `None` on its first line for every lean-mvp atom. The dead body still reads value-skill atoms `V02` / `V03` and renders `"Offering parts:"`. Rewriting that function into an evidence board would keep a value-shaped name and a parts×targets API the lean-mvp DAG does not use.

**Chosen:** delete the constant, the function, the exports, and the `next_question.py` board block. Prior answers come from each coaching entry's `reads` list and appear on the payload as `priors`.

**Rejected:** keep `match_board_for_atom` and feed it from coaching. That preserves a wrong abstraction (two labeled columns) and teaches maintainers the wrong vocabulary.

## Decision: resolve inside `voice.py`, no new module

skills-repo forbids fat scripts; thermonuclear forbids unearned new files. Coaching resolution is the same job the dead match-board claimed: turn session answers plus static config into agent-facing strings. That already lived in `voice.py`.

**Chosen:** three functions in `voice.py` (`load_atom_coaching`, `flatten_kb_value`, `resolve_atom_coaching`).

**Rejected:** `scripts/_session/coaching.py`. A second module earns its keep only when voice.py cannot absorb the replacement. Here the replacement deletes more lines than it adds in that file's match-board region.

**Rejected:** inline resolution in `next_question.py`. That would violate the thin-CLI rule.

## Decision: rename `slots` → `complete_when`; one entry shape

Proposed `slots` reads like form fields. The agent needs a checklist of what a complete answer contains. Gate and content atoms share the same six authored fields. Gate-ness is already `atom.gate` on the scheduler payload.

**Rejected:** a `kind: content|gate` discriminator with different required fields. Two schemas double the test surface for no payload gain.

**Rejected:** putting teaching prose only in `references/*.md`. The brief requires one `next_question` invocation to carry the turn; a second file read fails turn-completeness.

## Decision: soft-fail boundaries

A missing coaching entry, a bad `kb_ref`, or a missing prior must not stop the interview. One real session already stalled 22 hours on missing teaching; hard-failing the scheduler would stall it again for a packaging miss.

**Chosen:** `coaching: null` or partial `definitions` / `priors` with explicit status. CI catches packaging misses via the import-free coverage test.

**Rejected:** raise / exit non-zero when coaching is incomplete. That couples scheduling to authoring completeness at runtime.

## Decision: flatten all four KB shapes to one `text` string

The agent needs definition text in the paragraph, not a typed union to reinterpret. Four shapes become one string via `flatten_kb_value` so the payload stays boring.

**Rejected:** shipping raw KB subtrees under `definitions`. That re-exports key names and nested objects and forces the agent to re-parse shapes the package already knows.

**Rejected:** widening `invest_user_story_rubric` values in the KB as part of this work. Letter keys alone satisfy the story-generation-prompt test; coaching teaches from the existing pairs plus `complete_when` notes for I/E/S.

## Decision: MS05 teaches INVEST-plus results without editing story-generation-prompt

`mvp-scope.md` still says every v1 story passes INVEST. INVEST-plus forbids pass on I/E/S from the sentence alone. Out of scope to edit either skill package reference. Coaching `complete_when` carries the honest results set so the human is not told to rubber-stamp six passes.

## Alternatives considered for the payload key

| Option | Why rejected |
|--------|----------------|
| Keep `match_board` / `match_prompt` names | Wrong domain language; empty today |
| Top-level flat keys (`why_it_matters`, …) | Pollutes the ten-key scheduler envelope; harder to null as a unit |
| `coaching` omit-when-null | Agent cannot tell "old script" from "missing entry"; always emit the key |

## If forced to halve the diff

Cut, in order:

1. Do not delete value-trail / north-star dead helpers (already out of scope; keep that cut).
2. Ship coaching entries only for the express spine (C01, C05, C12, U01, U05, U12, MS01, MS05, MS12, UX01, UX04, UX12, MT01, MT04, MT12) plus any atom with non-empty `kb_refs` in a starter set; keep the coverage test as "every atom has an entry" but allow stub entries that are `why_it_matters` + empty refs + `complete_when: [accepts_summary]` copied from the atom. That halves authoring, not structure.
3. Drop `worked_example` from the authored schema and from delivery-order step 6; keep `common_miss` only.
4. Last resort: leave `match_board_for_atom` as a three-line `return None` stub instead of deleting exports (saves churn in `__init__.py` / tests that string-match the name). Prefer full delete if the half-diff budget allows.

Do not cut: resolved `definitions` text, `priors` with status, soft-fail, import-free coverage test, or thin `next_question.py`.
