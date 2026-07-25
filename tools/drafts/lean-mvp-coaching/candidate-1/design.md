# lean-mvp coaching layer, design sketch

## 1. What one turn returns

`python scripts/next_question.py <session>` at MS05, standard pacing. Ten keys today, eleven after.
`match_board` and `match_prompt` are gone.

```json
{
  "atom_id": "MS05", "module": "mvp-scope", "section": "Stories",
  "asks": "Write one INVEST user story for the top MVP feature chunk (As a … I want … so that …).",
  "accepts_summary": "Story plus brief INVEST pass/fail notes.",
  "soft": false, "gate": false, "gate_due": false,
  "pacing_mode": "standard", "position_status": "in_progress",
  "coaching": {
    "status": "ok",
    "teach": "An INVEST story is one sentence naming who, what they want, and the payoff, plus a short reading of whether the sentence holds up. Six letters grade it. Only three can be read off the sentence itself.",
    "concepts": [
      {
        "ref": "invest_user_story_rubric",
        "title": "Invest user story rubric",
        "status": "ok",
        "lines": [
          { "term": "I", "text": "Independent" }, { "term": "N", "text": "Negotiable" },
          { "term": "V", "text": "Valuable" },    { "term": "E", "text": "Estimable" },
          { "term": "S", "text": "Small" },       { "term": "T", "text": "Testable" }
        ]
      }
    ],
    "answer_shape": [
      "The sentence: As a <persona>, I want <capability>, so that <payoff>.",
      "N, V, and T each marked pass or fail, naming the clause you read.",
      "I, E, and S each marked \"not answerable here\" unless you give me the backlog, the estimating team, or the sprint length.",
      "One question that would fix any fail."
    ],
    "worked_example": "As a night-shift dispatcher, I want the late-delivery list on one screen, so that I stop calling drivers to find out who is behind. N pass, swap the screen for a text digest and the sentence survives. V pass, the payoff lands on the dispatcher. T pass, count calls placed per shift. I, E, S not answerable here, no backlog or team given.",
    "common_miss": "Marking I, E, and S pass from the sentence alone. Independent, Estimable, and Small are judgments about a backlog and a team, not about a sentence, so a pass there is a rubber stamp.",
    "builds_on": [
      { "atom_id": "C02", "label": "Target customer — Persona", "status": "answered",
        "why": "the persona that fills the As a clause",
        "text": "The Shop Lead. \"I can tell you which van is going to bite us next, but I can't prove it to the owner.\"" },
      { "atom_id": "U05", "label": "Underserved needs — Opportunity", "status": "answered",
        "why": "the focus benefit that fills the so that clause",
        "text": "Cut the time to prove a repair pattern to the owner. Importance 90%, satisfaction 20%, opportunity 72, highest of the three." },
      { "atom_id": "MS04", "label": "MVP scope — Kano", "status": "answered",
        "why": "the delighter call the story has to respect",
        "text": "No delighter in v1. Defer the predictive alert to post-PMF; the must-haves and the offense vector eat the whole build." }
    ]
  }
}
```

`label` comes from the existing `atom_provenance_label`, so the agent has a human name for each prior
answer and never has to speak an atom ID.

## 2. What the agent says from it

One paragraph, one question, no second file read.

> You told me your Shop Lead can see which van will fail next but can't prove it to the owner, and the
> benefit you picked to lead on is cutting the time to prove a repair pattern. You also ruled the
> predictive alert out of v1, so the story sits inside that. An INVEST story is one sentence saying who,
> what they want, and the payoff, then a short reading of whether it holds up. The six letters are
> Independent, Negotiable, Valuable, Estimable, Small, Testable. A complete answer is the sentence, then
> N, V, and T marked pass or fail with the clause you read, then I, E, and S marked "not answerable
> here" unless you tell me your backlog, your estimating team, or your sprint length, and one question
> that would fix anything that failed. From another product it looks like this. "As a night-shift
> dispatcher, I want the late-delivery list on one screen, so that I stop calling drivers to find out
> who is behind. N pass, swap the screen for a text digest and the sentence survives. V pass, the payoff
> lands on the dispatcher. T pass, count calls per shift." Write one INVEST story for your top chunk.

`common_miss` is held back. It goes out only if the answer trips it.

## 3. The asset

`assets/atom-coaching.json`, one entry per atom id, 32 entries, shape
`{ "coaching": { "<atom_id>": { ... } } }`.

| Field | Type | Meaning |
|---|---|---|
| `teach` | string | One or two sentences. What the concept is, in the operator's language. |
| `kb_refs` | list of string | Dotted paths into `knowledge-base.json`. Resolved into `concepts` in the payload. |
| `answer_shape` | list of string | What a complete answer contains, one item per required part. |
| `worked_example` | string | A filled answer from a different product, so it cannot be copied. |
| `common_miss` | string | The one mistake, phrased as the correction. |
| `builds_on` | list of `{atom, why}` | Prior atoms whose text this turn needs. `why` is the connective clause. |

Changes from the prior plan's `{why_it_matters, kb_refs, reads, slots, worked_example, common_miss}`.
`why_it_matters` folds into `teach`. `slots` becomes `answer_shape`, because "slots" reads like
template variables and the field is prose. `reads` is dropped, since a "go read this file" field is
the exact thing the one-invocation requirement forbids. `builds_on` is new. Refs are dotted paths,
not bare top-level keys, because C06 needs `visual_grounding_analogies.follow_me_home` and would
otherwise carry all five analogies as noise.

### Three filled entries

MS05's resolved form is section 1. Its authored entry is the same five prose fields verbatim, plus:

```json
"MS05": {
  "kb_refs": ["invest_user_story_rubric"],
  "builds_on": [
    { "atom": "C02", "why": "the persona that fills the As a clause" },
    { "atom": "U05", "why": "the focus benefit that fills the so that clause" },
    { "atom": "MS04", "why": "the delighter call the story has to respect" }
  ]
}
```

A content atom and a gate atom in full:

```json
"U04": {
  "teach": "Opportunity is not importance alone. A benefit everyone cares about and everyone already gets served on is a bad bet. The gap between how much it matters and how well it is met is the part worth building into.",
  "kb_refs": ["opportunity_formulas"],
  "answer_shape": [
    "Importance as a percentage, 0 to 100.",
    "Current satisfaction as a percentage, 0 to 100, judged against the workaround they use today.",
    "One line per number saying whether it is a fact, an estimate, or a guess."],
  "worked_example": "Importance 85%, fact, all nine shops I called raised it unprompted. Satisfaction 30%, estimate, they get partway with a shared spreadsheet. Opportunity 85 × 0.7 = 59.5.",
  "common_miss": "Rating satisfaction against your product instead of against what they do today. Satisfaction measures how well the current workaround serves them, and the workaround is usually a spreadsheet or a phone call.",
  "builds_on": [
    { "atom": "U01", "why": "the benefit you are scoring" },
    { "atom": "U03", "why": "the motivation underneath it, which usually moves the importance number" }]
},
"MS12": {
  "teach": "This is a review turn, not a new question. You are deciding whether the MVP scope holds together well enough to build against, or whether something upstream has to reopen first.",
  "kb_refs": [],
  "answer_shape": [
    "One of three: pass the gate, reopen a named section with the conflict you found, or record a blocking unknown.",
    "If you pass, one sentence naming the bet you are making.",
    "If you reopen, which section and what changed your mind."],
  "worked_example": "Reopen Kano. The offense vector assumes the owner reads the report, but the persona quote says the Shop Lead reads it. Fix the must-have list before the story stands.",
  "common_miss": "Passing the gate because every question has an answer. The gate asks whether the answers agree with each other, not whether the boxes are full.",
  "builds_on": [
    { "atom": "MS02", "why": "the must-haves v1 has to match" },
    { "atom": "MS04", "why": "the delighter call" },
    { "atom": "MS05", "why": "the story those two have to support" },
    { "atom": "MS06", "why": "the version cut you are gating" }]
}
```

MS12 carries no `kb_refs`, and the resolver returns `concepts: []` without a gate-specific branch.
No `kind` discriminator, because `atoms.json` already sets `gate: true`.

MS05's entry is also where the INVEST contradiction gets settled. `invest_user_story_rubric` is six
letter-to-word pairs, so the resolved concept teaches vocabulary and nothing more. The rest of the
load sits in `answer_shape` and `common_miss`, which follow
`story-generation-prompt/references/invest-plus.md` rather than `references/mvp-scope.md`'s "every
v1 story passes INVEST gate". Neither of those files is edited. `SKILL.md` gains one precedence line
so the agent knows which shape to state.

## 4. Resolving `kb_refs` across the four shapes

Every subtree flattens to the same `lines` list of `{term, text}`. One recursive function, three
Python type cases, no per-shape branch. A scalar (`str`, `int`, `float`, `bool`) becomes one line
carrying the accumulated prefix as `term` and `str(value)` as `text`. A `list` becomes one line per
item, all sharing the current prefix. A `dict` concatenates its children in insertion order,
extending the prefix with the humanized key. `_humanize` swaps underscores for spaces and uppercases
the lead character; prefix segments join with `" / "`. The ref's own name goes in `title`, not into
`term`, so the prefix starts empty.

| Ref | JSON shape | Resolved `lines` |
|---|---|---|
| `kano_model_categories.migration_rule` | plain string | 1 line, term `""`, text `"Yesterday's delighters become today's performance features and tomorrow's must-haves."` |
| `mvp_test_matrix_2x2.quantitative_product` | list of strings | 3 lines, term `""`, texts `"Fake door tests"`, `"Product analytics"`, `"Product A/B testing"` |
| `invest_user_story_rubric` | dict of strings | 6 lines, terms `"I"` through `"T"`, texts `"Independent"` through `"Testable"` |
| `kano_model_categories` | dict of objects plus a string sibling | 7 lines, terms `"Must haves / definition"`, `"Must haves / example"`, `"Performance features / definition"`, `"Performance features / example"`, `"Delighters / definition"`, `"Delighters / example"`, `"Migration rule"` |
| `validation_metrics.sean_ellis_pmf` | nested dict holding a float | 3 lines, terms `"Question"`, `"Pmf threshold"` (text `"0.4"`), `"Target answer"` |

`"Pmf threshold"` and `"5 ux design"` are the ugly end of `_humanize`. An acronym lookup would fix
them and does not earn a dict, since the agent restates every line in its own words anyway.

## 5. Boundary behavior

The interview keeps running in every case. The `coaching` key is always present, so the agent has one
render path and never branches on key absence.

| Condition | Payload | Agent |
|---|---|---|
| No entry for the atom, or `atom-coaching.json` absent | `status` is `"missing"`, every field empty | Falls back to `asks` plus `accepts_summary`, today's behavior |
| `kb_refs` path does not resolve, or resolves to an empty object or list | Concept present, `status` `"unresolved"`, `lines: []` | Skips it, says nothing about it |
| `builds_on` atom never answered, or skipped by express pacing | `status` `"unanswered"`, `text` `""` | Skips the row silently |
| `builds_on` answer is a gate pass or bypass row | `status` `"ceremony"`, `text` `""` | Skips the row silently |

`unanswered` is normal, not a defect. `EXPRESS_SPINE["mvp-scope"]` is `("MS01", "MS05", "MS12")`, so
in express pacing MS05's `builds_on` on MS04 has no text. That is why no test can assert prior answers
exist at runtime, and why missing rows are dropped in silence rather than narrated. Unresolved refs
stay in the payload rather than being filtered out, because the resolver reports what it found and
`SKILL.md` decides what gets spoken. A typo is caught by the asset test, not by hiding it.

## 6. Signatures

New file, `scripts/_session/coaching.py`. Imports `ASSETS_DIR`, `atom_provenance_label`, `load_json`
from `.catalog` and `current_answer`, `is_ceremony_answer` from `.runtime`. Module-level
`EMPTY_COACHING` holds the `"missing"` shape.

```python
def coaching_for_atom(session: dict[str, Any], atom_id: str) -> dict[str, Any]:
    """Turn-ready coaching: resolved knowledge-base text plus prior-answer text.
    Total over every atom id. An atom with no entry returns EMPTY_COACHING, so
    next_question.py always emits the key and the agent has one render path."""
    raise NotImplementedError

def _load_coaching() -> dict[str, Any]:
    """Read atom-coaching.json. A missing file yields {}, not an ended interview."""
    raise NotImplementedError

def _resolve_concept(knowledge_base: dict[str, Any], ref: str) -> dict[str, Any]:
    """One concept block for a dotted path. status is "ok" when the path reaches at least
    one non-empty text line, "unresolved" otherwise. Never raises on a bad path or shape."""
    raise NotImplementedError

def _flatten_kb_node(node: Any, term: str) -> list[dict[str, str]]:
    """Flatten any knowledge-base subtree to {"term", "text"} lines. Scalar yields one line,
    list one per item at the same term, dict concatenates children with term extended."""
    raise NotImplementedError

def _resolve_prior(session: dict[str, Any], entry: dict[str, str]) -> dict[str, Any]:
    """One builds_on block. Label from atom_provenance_label, text from the session. status
    is "answered", "ceremony" (gate or bypass row), or "unanswered" (never answered, or
    skipped by express pacing). text is "" unless answered."""
    raise NotImplementedError

def _humanize(key: str) -> str:
    """knowledge-base key to spoken term: underscores to spaces, lead character up."""
    raise NotImplementedError
```

`coaching_for_atom` loads `knowledge-base.json` once per invocation and passes it down. No cache,
because `next_question.py` is a one-shot CLI that exits after one payload.

`next_question.py` keeps its thin shape. The import list loses `match_board_for_atom` and gains
`coaching_for_atom`, and the eleven-line board block collapses to one payload line.

```python
        "position_status": position["status"],
        "coaching": coaching_for_atom(session, atom["id"]),
    }
    print(json.dumps(payload, indent=2))
```

## 7. What gets deleted

`match_board_for_atom` and `MATCH_BOARD_ATOMS` go. `MATCH_BOARD_ATOMS` is `{}`, the function returns
`None` on its first line for every lean-mvp atom, and the body below it reads `V02` and `V03`, which
are not in this DAG. `builds_on` resolution does the live half of that function's job, pulling prior
answer text and skipping ceremony rows, for every atom instead of two.

About 57 lines out. Roughly 40 from `match_board_for_atom` in `voice.py`, one from `constants.py`,
four from `__init__.py`, twelve from `next_question.py`. Against roughly 95 lines of `coaching.py`
the Python is net positive by about 40. `_prefer_extreme_first`, `split_sticky_items`, and
`sticky_label` keep other callers in `voice.py` and stay. The sibling dead code the grounding names
(`VALUE_TRAIL_CRUMBS`, `fill_value_trail`, `fill_north_star_blurb`, and the two templates absent from
lean-mvp's `assets/`) is roughly 130 more lines, and belongs in its own commit ahead of this one,
provable by the suite's 100 passes holding. `DESIGN_BRIEFS` and `BUILD_PACK_FILES` have readers in
`render.py` that I did not read, so I am not claiming those.

## 8. `SKILL.md`

One line into `(assets ...)`, reading `(atom-coaching assets/atom-coaching.json)`.
`protocol-3-turn-recipe` replaced.

```
  (protocol-3-turn-recipe
    (voice-recipe
      (shape "one paragraph, one primary question")
      (import-hint "briefly acknowledge value-imported facts without atom IDs"))
    (coaching-order
      1 "connect: one sentence from coaching.builds_on rows with status answered, spoken by label and text, never atom IDs"
      2 "define: coaching.concepts lines with status ok, restated in the operator's words; skip when they already used the vocabulary this module"
      3 "shape: coaching.answer_shape as what a complete answer contains"
      4 "example: coaching.worked_example, named aloud as an example from another product"
      5 "ask: the atom's asks, unchanged, one question")
    (hold-back "coaching.common_miss — deliver only after an answer trips it, never as a preemptive warning")
    (coaching-skips
      (missing "coaching.status missing — fall back to asks plus accepts_summary and keep going")
      (partial "skip any concepts or builds_on row whose status is not ok or answered; never narrate the gap")
      (express "pacing_mode express — deliver 1, 3, 5 only; concepts and worked_example on request"))
    (acceptance "coaching.answer_shape is the shape you state to the human; accepts_summary stays the scheduler's short label")
    (scripts-silent
      (run "import_value_context status next_question accept_answer")))
```

Holding `common_miss` is the one delivery call worth defending. A warning about a mistake the
operator has not made yet turns a four-beat turn into a lecture. Held, it becomes the second half of
a coaching loop.

## 9. The test

`tests/test_lean_mvp_coaching_asset.py`, `json` and `pathlib` only. No `import _session`, so it sits
outside the `sys.modules` collision the grounding documents. It reads the canonical tree
`skills/lean-mvp/`; `test_lean_mvp_skill_package.py` already proves the mirror is byte-identical, so
asserting against both would be duplicate coverage.

| Case | Asserts | Failure it guards |
|---|---|---|
| `test_every_atom_has_a_coaching_entry` | atom ids from `atoms.json` equal coaching keys, both directions | A 33rd atom shipping with a silent teaching hole; a renamed atom leaving an orphan entry nothing reads |
| `test_entry_fields_are_present_and_populated` | six required keys; `teach`, `worked_example`, `common_miss` non-empty strings; `answer_shape` a non-empty list of non-empty strings | A half-authored entry that reports `status: "ok"` and delivers a blank turn, worse than `missing` because the fallback never fires |
| `test_kb_refs_resolve_to_readable_text` | each dotted ref walks `knowledge-base.json` and reaches at least one non-empty string leaf | The original stall, a payload promising a definition and carrying an empty list |
| `test_builds_on_atoms_are_dag_ancestors` | `requires` edges from `atoms.json` give each atom's ancestor set; every `builds_on.atom` is a strict ancestor | Coaching promising prior text that is structurally impossible to hold yet, so the turn cites an answer the human was never asked for |
| `test_builds_on_rows_are_unique_and_not_self` | no atom lists itself, no duplicate atom inside one `builds_on` | A turn that quotes its own question back at the operator |
| `test_skill_md_registers_the_coaching_asset` | `assets/atom-coaching.json` appears inside the `(assets ...)` block | The dangling pointer the grounding shows nothing currently catches for lean-mvp, the same class as the unregistered `section-map.json` |

Ancestry against standard `requires` is correct under express pacing too. `EXPRESS_REQUIRES`
short-circuits the chain, `MS05` requiring `MS01` instead of `MS04`, and every express predecessor is
already a standard ancestor. The standard graph is the safe superset, so the test never needs
`constants.py`.

## 10. Module map and the 33rd atom

```
skills/lean-mvp/                   canonical; .cursor/skills/lean-mvp/ is a byte-identical mirror
  SKILL.md                         +1 asset line, protocol-3 replaced
  assets/atom-coaching.json        NEW, 32 entries    (atoms.json, knowledge-base.json unchanged)
  scripts/next_question.py         -12 +1, still a thin entrypoint
  scripts/_session/coaching.py     NEW, one public function
  scripts/_session/voice.py -40    constants.py -1    __init__.py -4 +2
tests/test_lean_mvp_coaching_asset.py    NEW, no _session import
```

`coaching.py` imports `catalog` and `runtime` and is imported by `__init__` after `runtime`.
`voice.py` already imports `runtime`, so the layering is unchanged and there is no cycle.

To add a 33rd atom, a maintainer edits `atoms.json`, adds the matching entry to `atom-coaching.json`,
and mirrors both trees. Forgetting the entry fails `test_every_atom_has_a_coaching_entry` with the
atom id in the message and nothing else breaks, because the runtime returns `status: "missing"` and
the interview keeps running. A forgotten entry is a red CI check, never a broken session. Forgetting
the mirror fails the existing package test. The standing tax is that byte-identical mirroring, which
this work grows from one asset file to two.
