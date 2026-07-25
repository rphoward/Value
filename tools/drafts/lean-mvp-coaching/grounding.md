# Grounding: lean-mvp coaching layer

Everything below was read directly from the repo at commit `240bdbe` and verified. Trust this
document over the plan file; several plan claims were wrong and are marked.

## The user-visible problem

`lean-mvp` interviews a solo operator one question per turn. The scheduler emits a question with
scheduling metadata and no teaching. The operator hits a compound question such as MS05 ("Write one
INVEST user story ... plus INVEST pass/fail notes") with no definition of INVEST in front of them,
no statement of what a complete answer contains, and no reminder of the prior answers the question
builds on. One real session stalled 22 hours on MS01. The definitions were already shipped in
`assets/knowledge-base.json`; nothing in the package said to deliver them.

## Files that matter

Two identical trees. Canonical is `skills/lean-mvp/`, mirror is `.cursor/skills/lean-mvp/`.
`tests/test_lean_mvp_skill_package.py::test_canonical_tree_mirrors_cursor_tree` compares SHA-256
across all 35 non-pyc files in both directions, so every change lands twice, byte for byte.

### `scripts/next_question.py` (100 lines, thin CLI)

Loads the session, calls `schedule_next_atom`, prints one JSON payload. The payload has exactly ten
keys today.

```python
payload = {
    "atom_id": atom["id"],
    "module": atom["module"],
    "section": atom.get("section"),
    "asks": atom["asks"],
    "accepts_summary": atom["accepts_summary"],
    "soft": atom.get("soft", False),
    "gate": atom.get("gate", False),
    "gate_due": gate_due,
    "pacing_mode": pacing_mode(session),
    "position_status": position["status"],
}
board = match_board_for_atom(session, atom["id"])
if board is not None:
    payload["match_board"] = {...}
    payload["match_prompt"] = board["match_prompt"]
```

Only `asks` and `accepts_summary` carry anything explanatory. Nothing validates this payload
against a schema, so adding a key is additive.

### The dead board machinery (verified dead, not just suspected)

`scripts/_session/constants.py:39` is `MATCH_BOARD_ATOMS: dict[str, tuple[str, str, str]] = {}`,
an empty dict. `scripts/_session/voice.py:123` defines `match_board_for_atom`, which returns `None`
on its first line when `atom_id not in MATCH_BOARD_ATOMS`, so it returns `None` for every atom in
lean-mvp. The body below that early return is a verbatim copy of the value skill's version and still
speaks the value skill's vocabulary:

- line 128 reads `current_answer(session, "V02")` for "offering parts"
- line 140 has `if atom_id == "V03": targets = _prefer_extreme_first(targets)`
- the returned shape is `parts` / `targets` / `part_labels` / `target_labels`
- `match_prompt` renders the literal string `"Offering parts:"`

`V02` and `V03` are not in lean-mvp's DAG. `match_board_for_atom` has exactly one caller,
`next_question.py:85`. `MATCH_BOARD_ATOMS` has exactly one reader, that function. Both are
re-exported from `scripts/_session/__init__.py`.

Sibling dead value-shaped code in the same file, out of scope but worth knowing: `VALUE_TRAIL_CRUMBS`,
`DESIGN_BRIEFS`, and `BUILD_PACK_FILES` are also emptied, and `fill_value_trail` /
`fill_north_star_blurb` in `voice.py` read `value-trail.template.md` and
`north-star-blurb.template.md`, which do not exist under lean-mvp's `assets/`.

### `assets/atoms.json`

32 atoms. `customer-context` 7 (C01-C06, C12), `underserved-needs` 6 (U01-U05, U12), `mvp-scope` 7
(MS01-MS06, MS12), `ux-prototype` 6 (UX01-UX05, UX12), `metrics` 6 (MT01-MT05, MT12). Each atom
carries `id`, `module`, `asks`, `accepts_summary`, `unlocks` (single id or null), `gate`, `requires`
(list), `section`, `soft`. The DAG is a single chain: every atom's `requires` is its predecessor and
`unlocks` points at its successor, crossing module boundaries at the gate atoms (C12 unlocks U01,
and so on). MT12 unlocks null.

The five gate atoms (C12, U12, MS12, UX12, MT12) are review turns, not content questions.

### `assets/knowledge-base.json`

Top-level keys: `system_metadata`, `visual_grounding_analogies`, `pmf_pyramid_hierarchy`,
`phase_module_map`, `olsen_hierarchy_of_web_needs`, `kano_model_categories`,
`invest_user_story_rubric`, `opportunity_formulas`, `ux_iceberg_layers`, `mvp_test_matrix_2x2`,
`validation_metrics`, `ltv_cac_ratio_bands`.

`invest_user_story_rubric` is six letter-to-word pairs and nothing else:
`{"I": "Independent", "N": "Negotiable", "V": "Valuable", "E": "Estimable", "S": "Small", "T": "Testable"}`.

`tests/test_story_generation_prompt_skill.py::test_story_card_invest_letters_match_lean_mvp_rubric`
compares `set(rubric)`, keys only, so widening the values survives that test.

Note the depth mismatch across the file. Some values are plain strings (`olsen_hierarchy_of_web_needs`),
some are objects with `definition` and `example` (`kano_model_categories`), some are lists
(`mvp_test_matrix_2x2`), some are nested objects (`validation_metrics`). Any resolver that reads
`kb_refs` has to survive all of these shapes.

### `SKILL.md`

`(assets ...)` block registers `session-schema`, `atoms-index`, `knowledge-base`, `value-bridge-map`
and the five module templates. `protocol-3-turn-recipe` is:

```
  (protocol-3-turn-recipe
    (voice-recipe
      (shape "one paragraph, one primary question")
      (import-hint "briefly acknowledge value-imported facts without atom IDs"))
    (scripts-silent
      (run "import_value_context status next_question accept_answer")))
```

`protocol-1-activation` already carries `(kb-load "read assets/knowledge-base.json for Kano, INVEST,
opportunity math, test matrix, LTV/CAC bands")`. So the package already tells the agent to read the
knowledge base; what is missing is any instruction to put it in front of the human.

**Plan claim corrected.** The plan says leaving a new asset out of the `(assets ...)` block "would be
the kind of dangling pointer the story-generation-prompt test exists to catch." That test only covers
`.cursor/skills/story-generation-prompt/`. lean-mvp has no equivalent test, and
`assets/section-map.json` is already unregistered in lean-mvp's SKILL.md today with nothing catching
it. Registering the new asset is still correct, but it is not currently test-enforced.

### `references/mvp-scope.md`

Line 13 is `(invest "Load invest_user_story_rubric; every v1 story passes INVEST gate")`.
MS05's `accepts_summary` is `"Story plus brief INVEST pass/fail notes."` Both demand an all-pass
shape that `.cursor/skills/story-generation-prompt/references/invest-plus.md` explicitly forbids:
that file sets `(default-result "not answerable here")` for I, E, and S, and
`(forbidden "Writing pass for I, E, or S from the sentence alone.")`. Its
`(results-allowed pass fail "not answerable here")` is the closed set today.

### Test baseline, measured

`python -m pytest tests -q` at commit `240bdbe`, before any change: **15 failed, 100 passed**.
The 15 are a pre-existing cluster, all in the value skill and prompt-suite tests:

```
tests/test_prompt_suite_compile_gate_ux.py  5 failures
tests/test_value_session_integrity.py       3 failures
tests/test_value_skill_contracts.py         1 failure
tests/test_value_skill_dag.py               6 failures
```

Root cause, confirmed by the failure text (`KeyError: 'P12'`, a value-skill atom id absent from
lean-mvp's `atoms.json`): four test files each insert a different skill's `scripts/` directory on
`sys.path` and then `import _session` by bare name. Whichever loads first wins `sys.modules` for the
whole run, so value-skill tests end up driving lean-mvp's `_session`. Fixing that collision is out
of scope. The consequence for this work is a hard constraint: **the new test must not import
`_session`**, or it inherits the same order dependence.

Two import-free patterns already used in the repo: read the JSON assets directly with `json.load`
(`tests/test_story_generation_prompt_skill.py`), or run the script as a subprocess and parse stdout
(`tests/test_value_skill_scripts.py`).

## Repo rules that constrain the design

- `.cursor/rules/skills-repo.mdc`: `scripts/` holds thin CLI entrypoints, stdlib only.
  `forbidden 'fat-scripts-with-domain-logic`. So resolution logic belongs in `scripts/_session/`,
  not inline in `next_question.py`.
- `.cursor/rules/thermonuclear.mdc` applies to all Python here: subtract complexity, no unrequested
  abstractions, no new file or module unless the split is earned, no ad-hoc boolean or special-case
  branch.
- Always-on workspace rule: imports go at the top of the module, no inline imports.
  (`next_question.py:40` already violates this inside the `--gaps` branch; pre-existing.)
- `.cursor/rules/test-engineering.mdc`: DAMP tests, assert public outputs, each case names the
  failure it guards.
