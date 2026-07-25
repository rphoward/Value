# Lean-MVP coaching layer — design sketch (candidate 3)

## 1. Caller usage

### 1.1 Example `next_question.py` stdout (MS05, prior answers present)

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
  "position_status": "in_progress",
  "coaching": {
    "status": "ok",
    "warnings": [],
    "why_it_matters": "A story sentence is the smallest testable promise about v1 scope; INVEST keeps it negotiable with the customer instead of a disguised spec.",
    "concepts": [
      {
        "heading": "INVEST (letter meanings)",
        "body_markdown": "- **I** — Independent\n- **N** — Negotiable\n- **V** — Valuable\n- **E** — Estimable\n- **S** — Small\n- **T** — Testable"
      },
      {
        "heading": "Scoring from one sentence (MS05)",
        "body_markdown": "Grade **N, V, T** pass/fail from the story text. Mark **I, E, S** as *not answerable here* unless the operator already named backlog, team, or sprint length in this session. Do not write pass for I, E, or S from the sentence alone."
      }
    ],
    "answer_checklist": [
      "One user story in As a / I want / so that form for the top MVP feature chunk you already chose.",
      "INVEST table: N, V, T with pass or fail plus a one-line note; I, E, S with not answerable here or pass only if prior context was given."
    ],
    "worked_example": {
      "context": "Top chunk: export monthly usage CSV for finance.",
      "sample": "As a finance admin I want … CSV … so that I can reconcile billing. INVEST table: N/V/T pass with notes; I/E/S not answerable here unless backlog, team, or sprint was stated."
    },
    "common_miss": "Treating all six letters as pass from grammar alone, or writing a feature spec ('build a CSV endpoint') instead of a customer outcome in so-that.",
    "prior_answers": [
      { "atom_id": "MS04", "section": "Kano", "label": "Delighter in/out for v1", "status": "answered", "text": "Defer predictive churn to post-PMF; v1 stops at export + seat accuracy." }
    ]
  }
}
```

`match_board` and `match_prompt` are **removed** from the payload (see §4).

### 1.2 Paragraph the agent says (derived from the JSON above)

You have already narrowed v1 to accurate seats plus CSV export and deferred the churn delighter. **INVEST** is a checklist for backlog items: Independent, Negotiable, Valuable, Estimable, Small, Testable. From a single story sentence you can honestly judge **N, V, and T**; mark **I, E, and S** as not answerable here unless you already named backlog order, who estimates, or sprint length. A complete answer is one As-a / I-want / so-that story for your top MVP chunk plus a short table with pass, fail, or not answerable here per letter. **Write one INVEST user story for the top MVP feature chunk (As a … I want … so that …).**

One paragraph, one primary question; teaching precedes the question.

---

## 2. Asset: `assets/atom-coaching.json`

### 2.1 File shape

```json
{
  "schema_version": 1,
  "entries": {
    "<atom_id>": { }
  }
}
```

Exactly **32** keys in `entries`, one per `atoms.json` id. `schema_version` bumps only on breaking entry-shape changes.

### 2.2 Entry schema (authoring)

| Field | Required | Purpose |
|-------|----------|---------|
| `kind` | yes | `"content"` or `"gate"` |
| `why_it_matters` | yes | One or two sentences; always copied into payload |
| `kb_refs` | content | Top-level keys in `knowledge-base.json`; resolved at runtime |
| `inline_concepts` | no | `{heading, body_markdown}[]` when KB is thin or policy is skill-local (MS05 INVEST-plus scoring) |
| `builds_on` | content | `{atom_id, label}[]` prior atoms to surface; order is display order |
| `answer_checklist` | yes | Bullet strings; expands `accepts_summary` for the human |
| `worked_example` | content | `{context?, sample}` strings |
| `common_miss` | content | One string |
| `gate_review` | gate | `{sections: [{section, atom_ids[]}], decision_prompt}` |

**Dropped from the plan proposal:** `reads` and `slots` — redundant with `builds_on` (prior text is hydrated from the session) and `answer_checklist` (slots for a complete answer). **Added:** `kind`, `inline_concepts`, structured `gate_review`, and `schema_version` on the file.

### 2.3 Filled examples (authoring source, before resolution)

**C02 (content)**

```json
"C02": {
  "kind": "content",
  "why_it_matters": "A named archetype plus a real quote keeps the segment from staying an abstract demographic blob.",
  "kb_refs": [],
  "builds_on": [
    { "atom_id": "C01", "label": "Target segment" }
  ],
  "answer_checklist": [
    "A short archetype name (not a job title alone).",
    "One quote in the customer's voice about what they care about most."
  ],
  "worked_example": {
    "context": "Segment: ops lead at growth-stage B2B SaaS.",
    "sample": "Archetype: \"Renewal firefighter Riley.\" Quote: \"I find out we overpaid for seats when finance asks, not when we're planning the renewal.\""
  },
  "common_miss": "Marketing tagline instead of a quote the persona would actually say."
}
```

**C12 (gate)**

```json
"C12": {
  "kind": "gate",
  "why_it_matters": "Gate turns six atoms into a committed customer-context artifact before needs work begins.",
  "gate_review": {
    "sections": [
      { "section": "Segment", "atom_ids": ["C01"] },
      { "section": "Persona", "atom_ids": ["C02", "C03"] },
      { "section": "Lifecycle", "atom_ids": ["C04"] },
      { "section": "Earlyvangelist", "atom_ids": ["C05"] },
      { "section": "Observation", "atom_ids": ["C06"] }
    ],
    "decision_prompt": "Pass the gate, reopen a section with a conflict note, or record blocking unknowns."
  },
  "answer_checklist": [
    "Explicit pass, reopen (name section + conflict), or blocking unknowns.",
    "If reopening, say which earlier answer is wrong or stale."
  ],
  "worked_example": {
    "sample": "Pass — segment, persona, and observation plan hang together; earlyvangelist ladder is weak on budget but labeled unknown, not hidden."
  },
  "common_miss": "Passing while a soft atom (C06) is still empty without calling it a blocking unknown."
}
```

**MS05 (content, compound INVEST)**

```json
"MS05": {
  "kind": "content",
  "why_it_matters": "A story sentence is the smallest testable promise about v1 scope; INVEST keeps it negotiable with the customer instead of a disguised spec.",
  "kb_refs": ["invest_user_story_rubric", "kano_model_categories"],
  "inline_concepts": [
    {
      "heading": "Scoring from one sentence (MS05)",
      "body_markdown": "Grade **N, V, T** pass/fail from the story text. Mark **I, E, S** as *not answerable here* unless backlog, estimating team, or sprint length was already stated. Do not write pass for I, E, or S from the sentence alone."
    }
  ],
  "builds_on": [
    { "atom_id": "MS01", "label": "One-sentence value proposition" },
    { "atom_id": "MS03", "label": "Must-have vs performance cut" },
    { "atom_id": "MS04", "label": "Delighter in/out for v1" }
  ],
  "answer_checklist": [
    "One user story in As a / I want / so that form for the top MVP feature chunk.",
    "INVEST notes: N, V, T pass/fail; I, E, S not answerable here unless context was given."
  ],
  "worked_example": {
    "context": "Top chunk: export monthly usage CSV for finance.",
    "sample": "As a finance admin I want to download a CSV of last month's seat usage so that I can reconcile billing without opening every account. (Plus INVEST table as in payload example §1.1.)"
  },
  "common_miss": "Rubber-stamping all six INVEST letters as pass from grammar alone."
}
```

Register `assets/atom-coaching.json` in SKILL.md `(assets ...)` beside `knowledge-base`.

---

## 3. Resolution logic (`scripts/_session/`)

Domain logic stays out of `next_question.py`. One new module is earned: **four KB shapes** plus session hydration do not belong in the CLI.

### 3.1 Types (sketch)

```python
# scripts/_session/coaching.py — ConceptBlock, PriorAnswer, CoachingPayload (TypedDicts as in §1.1 coaching key)

def load_coaching_index(assets_dir: Path) -> dict[str, dict[str, Any]]: raise NotImplementedError
def resolve_kb_ref(kb: dict[str, Any], key: str) -> list[ConceptBlock]: raise NotImplementedError
def resolve_kb_refs(kb, refs) -> tuple[list[ConceptBlock], list[str]]: raise NotImplementedError
def hydrate_prior_answers(session, builds_on, atoms_by_id) -> list[PriorAnswer]: raise NotImplementedError
def build_gate_prior_answers(session, gate_review, atoms_by_id) -> list[PriorAnswer]: raise NotImplementedError
def assemble_coaching_payload(session, atom, entry, kb, atoms_by_id) -> CoachingPayload: raise NotImplementedError
```

### 3.2 `resolve_kb_ref` behavior (all four shapes)

| KB shape | Example key | Resolved `body_markdown` |
|----------|-------------|---------------------------|
| Plain string map | `olsen_hierarchy_of_web_needs` | Numbered list of `key: value` lines |
| Object with `definition` / `example` children | `kano_model_categories` | One block per child object; heading = child key; body = definition + example |
| `dict[str, list[str]]` quadrants | `mvp_test_matrix_2x2` | One block; heading = quadrant key; body = bullet list |
| Nested object without uniform children | `invest_user_story_rubric` | One block "INVEST (letter meanings)" with `- **I** — Independent` lines |
| Nested metric objects | `validation_metrics` | One block per metric; flattened key/value lines |

Denylist unreferenced meta keys (`system_metadata`, analogies, `phase_module_map`) from `kb_refs`.

### 3.3 Boundary behavior

| Condition | `coaching.status` | Behavior |
|-----------|-------------------|----------|
| Entry missing for atom | `fallback` | `why_it_matters` from module phase string; `concepts` empty; `answer_checklist` = `[accepts_summary]`; `prior_answers` from atom `requires` chain if any; warning `missing_coaching_entry` |
| `kb_refs` key absent | `partial` or `ok` | Omit that concept; append warning `unresolved_kb_ref:<key>` |
| Prior atom unanswered | `ok` | `prior_answers[].status` = `missing`, `text` = `""` |
| Prior atom ceremony / import placeholder | `ok` | `status` = `ceremony`, `text` = `""` |
| Gate atom | `ok` | `prior_answers` from `gate_review.sections`; `concepts` may include `phase_module_map` slice for the module |

Interview never aborts; warnings are for agent logs only, not shown verbatim to the human.

### 3.4 `next_question.py` change (thin)

```python
from _session import assemble_coaching_payload, load_coaching_index, load_knowledge_base, ...

# After building base payload:
coaching_index = load_coaching_index(ASSETS_DIR)
kb = load_knowledge_base(ASSETS_DIR)
payload["coaching"] = assemble_coaching_payload(
    session, atom, coaching_index.get(atom["id"]), kb, atoms_by_id
)
# Delete match_board_for_atom import and the board branch entirely.
```

`load_knowledge_base` may be a five-line helper next to `load_atoms` in `io.py` (or inline in `coaching.py` if `io.py` does not exist yet).

---

## 4. Replace `match_board_for_atom`

**Choice: delete, do not rewrite.**

Evidence board was value-skill vocabulary (`V02`, `V03`, offering parts) and `MATCH_BOARD_ATOMS` is `{}`, so every call returns `None`. Coaching `prior_answers` subsumes the only lean-mvp need: remind the human what they already said.

**Remove:** `MATCH_BOARD_ATOMS`, `match_board_for_atom` (entire function in `voice.py`), re-exports in `__init__.py`, and `next_question.py` lines 85–95. Net line count drops ~45 lines of dead code.

Gate turns use `gate_review.sections` instead of a parts×targets grid.

---

## 5. `protocol-3-turn-recipe` (SKILL.md)

Replace the current voice block with an ordered recipe (still one question per turn):

Ordered delivery: (1) tie to answered `prior_answers` without atom ids, (2) `why_it_matters`, (3) ≤2 `concepts` blocks, (4) `answer_checklist`, (5) optional `worked_example.context` if stuck, (6) `asks` verbatim as the one question. Source line: teach only from `payload.coaching`, not a second KB read. `kb-load` in protocol-1 stays for module context and on-request story-generation.

---

## 6. Module map

| Module | Change |
|--------|--------|
| `assets/atom-coaching.json` | **New** — 32 entries |
| `scripts/_session/coaching.py` | **New** — load index, KB resolve, assemble payload |
| `scripts/_session/io.py` or `atoms.py` | Optional `load_knowledge_base` if not already present |
| `scripts/_session/voice.py` | **Delete** `match_board_for_atom` and value-only helpers used only by it (`_prefer_extreme_first` if unused elsewhere) |
| `scripts/_session/constants.py` | **Delete** `MATCH_BOARD_ATOMS` |
| `scripts/_session/__init__.py` | Export coaching API; drop `match_board_for_atom` |
| `scripts/next_question.py` | Add `coaching` key; remove board branch |
| `SKILL.md` | Register asset; replace protocol-3 as above |
| `tests/test_lean_mvp_coaching_assets.py` | **New** — JSON-only contract (§7) |

Mirror canonical `skills/lean-mvp/` and `.cursor/skills/lean-mvp/` byte-for-byte on ship.

---

## 7. Machine-checkable test (no `_session` import)

**File:** `tests/test_lean_mvp_coaching_assets.py`

| Test | Asserts |
|------|---------|
| `test_coaching_covers_every_atom` | `set(entries.keys()) == {a["id"] for a in atoms.json}` |
| `test_kb_refs_resolve` | For each entry's `kb_refs`, key exists in `knowledge-base.json` and is not in a denylist (`system_metadata`, …) |
| `test_builds_on_predecessor_closure` | Each `builds_on[].atom_id` appears in `atoms.json` and is an ancestor of the entry's atom along `requires` (walk predecessors) |
| `test_gate_entries_have_gate_review` | `kind == "gate"` iff atom `gate == true` in atoms.json |
| `test_next_question_stdout_includes_coaching` | Subprocess: `python next_question.py <fixture_session>` → JSON has `coaching` with required keys; MS05 fixture has non-empty `concepts` |

Subprocess fixture: `tests/fixtures/lean_mvp_ms05_session.json` or `tmp_path` session built with `json` only.

**33rd atom:** edit `atoms.json` + `atom-coaching.json`, run coaching asset tests, mirror both skill trees. Runtime `fallback` if entry forgotten.
