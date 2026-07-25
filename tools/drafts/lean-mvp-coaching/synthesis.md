# Arena synthesis: the coaching layer design we are building

Base is candidate 2. Grafts from candidate 3. Corrections are mine, made against repo evidence
neither candidate had. Candidate 1 had not produced output when this was written; if it lands, it is
read and grafted before the diff is final.

## Where the candidates converged

Both independently reached the same four calls, which is the strongest signal in the run.

1. Delete `match_board_for_atom` and `MATCH_BOARD_ATOMS` rather than rewriting them. The value skill's
   parts-times-targets grid does not map onto lean-mvp's single-chain DAG, and a rewrite would keep
   the wrong vocabulary in a lean-mvp file.
2. Put coaching in a sidecar `assets/atom-coaching.json` rather than growing `atoms.json`. The
   scheduler asset stays a DAG; teaching evolves without touching unlock order.
3. Resolve `kb_refs` at runtime into text, so the payload carries definitions and never key names.
4. Soft-fail at the payload boundary. A missing entry, an unresolvable ref, or an unanswered prior
   must never stop the interview. A packaging miss that stalls the scheduler would recreate the exact
   failure this work exists to fix.

## Where they differed, and the call

| Fork | Candidate 2 | Candidate 3 | Chosen | Why |
|---|---|---|---|---|
| Where resolution lives | three functions added to `voice.py` | new `_session/coaching.py` | **new `coaching.py`** | `voice.py` says it holds "sticky labels, match board, outward pitch, trail crumbs". Coaching resolution is asset loading plus session lookup plus knowledge-base flattening. Putting it in `voice.py` makes that docstring a lie and turns the file into the grab-bag. One flat new file is one place to look. |
| Gate atoms | no discriminator, `gate` already on the atom | `kind: "content" \| "gate"` field | **no discriminator** | `atoms.json` already carries `gate: true`. A second field has to stay in sync with the first, which is the tell the domain was modelled twice. |
| Missing entry | `coaching: null` | `status: "fallback"` plus synthesized content | **`coaching: null`** | The agent's fallback is the turn it already gives today. Synthesizing a fake coaching block hides the packaging miss behind plausible output. |
| Definition shape | one flattened `text` string | `{heading, body_markdown}` blocks | **flattened `text`** | The agent writes its own paragraph. Shipping markdown it has to unwrap is work for no gain. |
| Payload test | JSON assets only, no subprocess | subprocess on `next_question.py` | **subprocess, grafted from 3** | The asset can be perfect while `payload["coaching"] = ...` is missing. The wiring is the likeliest silent break, and `demo_turn.py` already proves the subprocess path is cheap. |
| Naming | `reads`, `complete_when` | `builds_on`, `answer_checklist` | **`reads`, `complete_when`** | `reads` is the plan's word already. `complete_when` beats the plan's `slots`, which reads like form fields. |

## Corrections to both candidates

### 1. Widen `invest_user_story_rubric` from the source document

Both candidates rejected widening the knowledge base, and both were reasoning without the
provenance. `docs/lean-product-playbook-prompt-suite.md` lines 78-85 already carry the full
definitions:

```json
"invest_user_story_rubric": {
  "I": "Independent (overlap-free, implementable in any order)",
  "N": "Negotiable (not an explicit contract, open to discussion)",
  ...
}
```

The shipped `assets/knowledge-base.json` truncated those to bare words when it was compiled. So this
is restoring lost content from the upstream source, not inventing content, and it moves the asset
back toward the document rather than away from it.

It also decides the whole feature. `kb_refs: ["invest_user_story_rubric"]` against today's entry
flattens to `I: Independent. N: Negotiable. ...`, which is precisely the useless key dump the
coaching layer exists to replace. Restore the definition, add the one-line check of what to read in
the sentence (sourced from `references/invest-plus.md`, which already states it per letter), and the
resolved payload teaches something.

`tests/test_story_generation_prompt_skill.py:100` compares `set(rubric)`, keys only, so the shape
change is safe.

### 2. `reads` may not name a gate atom

`is_ceremony_answer` returns False for `"pass mvp-scope gate"`, because it only matches text
containing both "bypass" and "gate" (`runtime.py:133`). A gate atom listed in `reads` would therefore
surface the string `pass mvp-scope gate` to the human as if it were evidence they had given. Content
atoms read content atoms; a gate atom's coaching reads its own module's content atoms. Enforce it in
the test rather than in prose.

### 3. Cut the diagnostic channel

Candidate 2 proposed `skipped_kb_refs`, candidate 3 proposed `status` and `warnings`. Both are
runtime reports of a condition the coverage test makes impossible in a shipped tree, and nothing
reads them. Cut both. If a ref ever fails to resolve, the concept is simply absent from
`definitions`, and CI is where that gets caught.

## The design we build

### Asset `assets/atom-coaching.json`

Top-level object keyed by atom id. Exactly 32 keys. Six authored fields per entry, one shape for
every atom.

| Field | Type | Rule |
|---|---|---|
| `why_it_matters` | string | One or two sentences on what this turn decides. |
| `kb_refs` | string[] | Top-level keys of `knowledge-base.json`. May be empty. |
| `reads` | string[] | Prior content atom ids whose answers ground this turn. No gate atoms. Empty only for C01. |
| `complete_when` | string[] | What a complete answer contains. |
| `worked_example` | string | One concrete good answer. |
| `common_miss` | string | The stall pattern to name when the human freezes. |

### Resolved `coaching` block on the payload

```json
"coaching": {
  "why_it_matters": "...",
  "definitions": [{ "ref": "invest_user_story_rubric", "text": "I: Independent ..." }],
  "complete_when": ["...", "..."],
  "worked_example": "...",
  "common_miss": "...",
  "priors": [{ "atom_id": "MS04", "status": "ok", "answer": "Defer delighters to post-PMF." }]
}
```

`coaching` is always present and is `null` when no entry exists. `priors[].status` is `ok`,
`missing`, or `ceremony`; `answer` is the accepted text on `ok` and `null` otherwise.

### `scripts/_session/coaching.py`

```python
def load_atom_coaching() -> dict[str, dict[str, Any]]: ...
def flatten_kb_value(value: Any) -> str: ...
def coaching_for_atom(session: dict[str, Any], atom_id: str) -> dict[str, Any] | None: ...
```

`flatten_kb_value` handles every shape in `knowledge-base.json`: plain string, list of strings,
object of strings, and object of objects. Numbers are stringified.

### Everything else

`next_question.py` gains one line, `payload["coaching"] = coaching_for_atom(session, atom["id"])`,
and loses the board import and the board block. `constants.py` loses `MATCH_BOARD_ATOMS`, `voice.py`
loses `match_board_for_atom`, `__init__.py` loses both exports. `SKILL.md` registers the asset and
gains a delivery order in `protocol-3-turn-recipe`. Both trees stay byte-identical.
