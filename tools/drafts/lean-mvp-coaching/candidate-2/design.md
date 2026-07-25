# lean-mvp coaching layer (design sketch)

Principles that drove concrete choices: **Subtract Before You Add** (delete dead match-board, then add coaching), **Laziness Protocol** (no new `_session` module), **Model the Domain** (registry + closed resolved shape), **Boundary Discipline** (soft-fail at the payload edge), **Encode Lessons in Structure** (import-free coverage test).

## 1. Caller usage (one real turn)

### 1.1 JSON `next_question.py` returns for MS05

Existing ten keys unchanged. New key `coaching` is always present (object or `null`).

```json
{
  "atom_id": "MS05",
  "module": "mvp-scope",
  "section": "Stories",
  "asks": "Write one INVEST user story for the top MVP feature chunk (As a … I want … so that …).",
  "accepts_summary": "Story plus brief INVEST pass/fail notes.",
  "soft": false,
  "gate": false,
  "gate_due": false,
  "pacing_mode": "standard",
  "position_status": "focus",
  "coaching": {
    "why_it_matters": "A story sentence turns the Kano chunk into something you can test with a customer; INVEST letters are how you check the sentence is worth writing down.",
    "definitions": [
      {
        "ref": "invest_user_story_rubric",
        "text": "I: Independent. N: Negotiable. V: Valuable. E: Estimable. S: Small. T: Testable."
      },
      {
        "ref": "kano_model_categories",
        "text": "must_haves: Table stakes; absence causes extreme dissatisfaction. Example: Seat belts in a car. | performance_features: More is better; satisfaction scales with fulfillment. Example: Fuel efficiency or page load speed. | delighters: Unexpected wow; absence does not dissatisfy. Example: GPS navigation in the 2000s. | migration_rule: Yesterday's delighters become today's performance features and tomorrow's must-haves."
      }
    ],
    "skipped_kb_refs": [],
    "complete_when": [
      "One story in As a / I want / so that form naming the top MVP chunk.",
      "Six INVEST letter notes. N, V, T must be pass or fail from the sentence. I, E, S may be pass, fail, or not answerable here when backlog, team, or sprint length is missing."
    ],
    "worked_example": "As a solo operator reviewing interview notes, I want one INVEST story for the must-have export chunk so that I can show a customer a testable win. Notes: N pass (want is outcome, not a stack). V pass (so-that is the operator's win). T pass (customer can say yes/no to the export). I/E/S not answerable here (no backlog or sprint length yet).",
    "common_miss": "Writing a feature wishlist with no so-that, or stamping all six letters pass with no note.",
    "priors": [
      {
        "atom_id": "MS02",
        "status": "ok",
        "answer": "Must-haves: offline draft save; one-click export to markdown."
      },
      {
        "atom_id": "MS03",
        "status": "ok",
        "answer": "Offense on export speed; cede fancy themes to incumbents."
      },
      {
        "atom_id": "MS04",
        "status": "ok",
        "answer": "Defer delighters to post-PMF; v1 is table stakes only."
      }
    ]
  }
}
```

No `match_board` / `match_prompt` keys. Dead board path is removed, not rewritten.

### 1.2 Paragraph the agent says from that JSON alone

> Your must-haves are offline draft save and one-click markdown export; you are playing offense on export speed and deferring delighters. INVEST means Independent, Negotiable, Valuable, Estimable, Small, Testable. A complete answer is one As-a / I-want / so-that story for that top chunk, plus letter notes (N/V/T from the sentence; I/E/S may be not answerable here without backlog context). Write one INVEST user story for the top MVP feature chunk (As a … I want … so that …).

(`worked_example` and `common_miss` stay in the payload for a stall follow-up; they are not required in the opening paragraph.)

---

## 2. Asset schema: `assets/atom-coaching.json`

Top level is an object keyed by atom id (all 32 ids from `atoms.json`).

### 2.1 Entry schema (authored)

| Field | Type | Rule |
|-------|------|------|
| `why_it_matters` | string | One or two sentences. Why this turn exists. |
| `kb_refs` | string[] | Top-level keys in `knowledge-base.json`. May be empty (gates, simple atoms). |
| `reads` | string[] | Prior atom ids whose accepted answers ground this turn. Empty only for true entry atoms (e.g. C01). |
| `complete_when` | string[] | What a complete answer contains. Replaces proposed `slots`. |
| `worked_example` | string | One concrete good answer (or gate decision). |
| `common_miss` | string | The stall pattern to name if the human freezes. |

Changes from the plan proposal `{why_it_matters, kb_refs, reads, slots, worked_example, common_miss}`:

- Rename `slots` → `complete_when` (agent-facing checklist, not form fields).
- No `role` / `kind` field. Gate vs content is already on the atom (`gate: true`); coaching stays one shape.
- Resolved payload adds `definitions`, `skipped_kb_refs`, `priors` (never authored).

### 2.2 Three filled entries

```json
{
  "C01": {
    "why_it_matters": "Every later atom hangs on who you are building for. A fuzzy segment makes Kano columns and stories drift.",
    "kb_refs": ["phase_module_map"],
    "reads": [],
    "complete_when": [
      "Names one target segment.",
      "States an exclusion boundary or labels the boundary unknown."
    ],
    "worked_example": "Segment: solo PMs shipping a first Cursor skill. Exclusion: agencies running multi-client delivery (unknown whether to park).",
    "common_miss": "Naming a market category (\"developers\") with no exclusion, then debating features anyway."
  },
  "MS05": {
    "why_it_matters": "A story sentence turns the Kano chunk into something you can test with a customer; INVEST letters are how you check the sentence is worth writing down.",
    "kb_refs": ["invest_user_story_rubric", "kano_model_categories"],
    "reads": ["MS02", "MS03", "MS04"],
    "complete_when": [
      "One story in As a / I want / so that form naming the top MVP chunk.",
      "Six INVEST letter notes. N, V, T must be pass or fail from the sentence. I, E, S may be pass, fail, or not answerable here when backlog, team, or sprint length is missing."
    ],
    "worked_example": "As a solo operator reviewing interview notes, I want one INVEST story for the must-have export chunk so that I can show a customer a testable win. Notes: N pass; V pass; T pass; I/E/S not answerable here.",
    "common_miss": "Writing a feature wishlist with no so-that, or stamping all six letters pass with no note."
  },
  "MS12": {
    "why_it_matters": "The gate locks MVP scope before UX work. Passing without a coherent story and ROI cut reopens later under worse pressure.",
    "kb_refs": [],
    "reads": ["MS01", "MS02", "MS03", "MS04", "MS05", "MS06"],
    "complete_when": [
      "Pass mvp-scope gate, or reopen a named conflict, or list blocking unknowns.",
      "Do not invent new feature content on the gate turn."
    ],
    "worked_example": "pass mvp-scope gate",
    "common_miss": "Re-asking Kano or story content on the gate turn instead of pass / reopen / unknowns."
  }
}
```

MS05 `complete_when` softens the all-pass wording in `references/mvp-scope.md` so the teaching turn matches INVEST-plus results (`pass` / `fail` / `not answerable here`) without editing that reference in this change set.

---

## 3. Resolved `coaching` object (runtime)

```text
coaching = null
  | {
      why_it_matters: str,
      definitions: [ { ref: str, text: str } ],
      skipped_kb_refs: [str],
      complete_when: [str],
      worked_example: str,
      common_miss: str,
      priors: [ { atom_id: str, status: "ok"|"missing"|"ceremony", answer: str|null } ]
    }
```

- `definitions[].text` is always a single string. Key names never appear alone as the teaching body.
- `priors[].answer` is the raw accepted answer text when `status == "ok"`, else `null`.
- `status`: `ok` usable content; `missing` no answers[] row; `ceremony` gate/bypass text via existing `is_ceremony_answer`.

### Boundary behavior (interview keeps running)

| Condition | Payload behavior |
|-----------|------------------|
| No coaching entry for atom | `"coaching": null`. Agent falls back to today's asks-only turn. |
| `kb_refs` key absent from KB | Omit from `definitions`; append key to `skipped_kb_refs`. |
| Prior in `reads` unanswered | Prior row with `status: "missing"`, `answer: null`. |
| Prior is ceremony | `status: "ceremony"`, `answer: null` (do not treat gate pass as customer evidence). |
| Coaching JSON file missing at runtime | Same as missing entry for every atom: `coaching: null`. Log nothing to stdout; stderr optional later. |

Never raise into `next_question.py`'s happy path for these cases.

---

## 4. KB shape flattening (`flatten_kb_value`)

Input is any `knowledge-base.json` value. Output is one teaching string.

| Shape | Example key | Rule |
|-------|-------------|------|
| plain string | (leaf under nested) | Use the string. |
| object with `definition` / `example` | `kano_model_categories.must_haves` | `"{definition} Example: {example}."` Extra sibling keys (e.g. `migration_rule` string) append as `"key: value"`. |
| list of strings | `mvp_test_matrix_2x2.qualitative_marketing` | Join with `"; "`. |
| nested object | `invest_user_story_rubric`, `validation_metrics`, `olsen_hierarchy_of_web_needs` | Walk keys in file order. String leaf → `"K: V"`. Dict leaf → recurse and join with `" | "`. List leaf → apply list rule then `"K: ..."`. |

Concrete outputs:

- `invest_user_story_rubric` → `I: Independent. N: Negotiable. ... T: Testable.`
- `opportunity_formulas` → `value_delivered: Importance × Satisfaction. opportunity_score: Importance × (1 − Satisfaction).`
- `mvp_test_matrix_2x2` → four `key: a; b; c` clauses joined by ` | `.
- `validation_metrics` → `nps: formula: % Promoters... | sean_ellis_pmf: question: ...; pmf_threshold: 0.4; target_answer: Very disappointed` (numbers `str()`'d).

`system_metadata` is a valid top-level key but coaching entries should not reference it; the test only checks refs that appear in entries.

---

## 5. Resolution signatures (live in `scripts/_session/voice.py`)

No new module. Replace `match_board_for_atom` in place. `next_question.py` stays a thin caller.

```python
def load_atom_coaching() -> dict[str, dict[str, Any]]:
    """Load assets/atom-coaching.json. Return {} if the file is absent."""
    raise NotImplementedError


def flatten_kb_value(value: Any) -> str:
    """Collapse any knowledge-base value shape to one teaching string."""
    raise NotImplementedError


def resolve_atom_coaching(
    session: dict[str, Any], atom_id: str
) -> dict[str, Any] | None:
    """Build the coaching object for atom_id, or None if no entry.

    Loads knowledge-base.json once per call (or accept optional kb dict in
    implementation). Skips missing kb_refs. Resolves reads via current_answer
    + is_ceremony_answer. Never raises for boundary cases in section 3.
    """
    raise NotImplementedError
```

`next_question.py` change (sketch):

```python
# drop match_board_for_atom import and board block
from _session import resolve_atom_coaching  # plus existing imports

payload["coaching"] = resolve_atom_coaching(session, atom["id"])
```

Delete: `MATCH_BOARD_ATOMS` in `constants.py`, `match_board_for_atom` body, re-exports in `__init__.py`. Leave other emptied value-trail helpers alone (out of scope).

---

## 6. `protocol-3-turn-recipe` delivery order

Replace the current voice-recipe block with:

```
(protocol-3-turn-recipe
  (voice-recipe
    (shape "one paragraph, one primary question")
    (delivery-order
      1 "when coaching is null: ask asks only (legacy)"
      2 "when priors status=ok: one clause grounding those answers, no atom IDs"
      3 "when definitions non-empty: teach definition text in one short clause"
      4 "state complete_when as what a complete answer contains"
      5 "ask asks as the single primary question"
      6 "hold worked_example and common_miss until the human stalls")
    (import-hint "briefly acknowledge value-imported facts without atom IDs"))
  (scripts-silent
    (run "import_value_context status next_question accept_answer")))
```

Also register the asset:

```
(atom-coaching assets/atom-coaching.json)
```

inside the existing `(assets ...)` list.

---

## 7. Machine-checkability (no `_session` import)

New file `tests/test_lean_mvp_atom_coaching.py` reads JSON only (same pattern as `tests/test_story_generation_prompt_skill.py`).

| Assertion | Against |
|-----------|---------|
| `set(coaching.keys()) == {a["id"] for a in atoms}` | `atom-coaching.json` vs `atoms.json` (both trees: `skills/` and `.cursor/skills/`) |
| every `kb_refs` entry ∈ top-level keys of `knowledge-base.json` | coaching vs KB |
| every `reads` id ∈ atom id set | coaching vs atoms |
| every `reads` id is a DAG predecessor of the entry atom | walk `requires` transitively; fail if a read is self, successor, or off-chain |
| every entry has non-empty `why_it_matters`, `complete_when`, `worked_example`, `common_miss` | coaching schema presence |
| byte-identical coaching file across canonical and cursor trees | extend or rely on existing mirror test once the file exists in both trees |

Do not import `_session`. Do not subprocess `next_question.py` for coverage (session fixtures would grow the diff).

---

## 8. Maintainer cost (33rd atom)

1. Add the atom to `assets/atoms.json` (both trees).
2. Add a same-id entry to `assets/atom-coaching.json` (both trees).
3. Run `tests/test_lean_mvp_atom_coaching.py`. Coverage mismatch fails with the missing id named.
4. If the atom needs teaching from the KB, add the top-level key name to `kb_refs` (invalid names fail the kb_refs test).

Forgetting the coaching entry is a red test, not a silent asks-only turn in CI. Runtime still soft-fails if someone ships atoms without coaching outside CI.

---

## 9. Module map

```
skills/lean-mvp/                         # canonical; mirror under .cursor/skills/lean-mvp/
  assets/
    atom-coaching.json                   # NEW — 32 entries, schema in §2
    knowledge-base.json                  # read by resolver; unchanged schema
    atoms.json                           # coverage oracle; unchanged
  scripts/
    next_question.py                     # thin: attach coaching, drop match_board
    _session/
      voice.py                           # +flatten_kb_value +load_atom_coaching
                                         # +resolve_atom_coaching; -match_board_for_atom
      constants.py                       # -MATCH_BOARD_ATOMS
      __init__.py                        # re-export swap
      catalog.py                         # unchanged (load_json already exists)
  SKILL.md                               # assets register + protocol-3 delivery-order
tests/
  test_lean_mvp_atom_coaching.py         # NEW — import-free JSON contracts
```

Net deletion: empty `MATCH_BOARD_ATOMS`, ~40-line `match_board_for_atom`, board keys in `next_question.py`. Net addition: coaching asset, three functions in `voice.py`, one protocol block, one test module.
