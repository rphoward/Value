# Plan audit: `lean-mvp coaching layer`

What the plan at `.cursor/plans/lean-mvp_coaching_layer_a9e65afa.plan.md` got right, what it got
wrong, and what it left out. Every verdict below was checked against the repo at commit `240bdbe`
before any code was written. The plan file itself lives outside this workspace, so it was not edited;
this file is the correction record.

## Verdicts at a glance

| # | Plan claim | Verdict |
|---|---|---|
| 1 | `next_question.py` emits ten fields, only two explanatory | **Verified** |
| 2 | 32 atoms, split 7 / 6 / 7 / 6 / 6 across five modules | **Verified** |
| 3 | `MATCH_BOARD_ATOMS` is empty, so `match_board_for_atom` is dead in lean-mvp | **Verified, and confirmed at runtime** |
| 4 | `voice.py` line 128 hardcodes `V02`, line 140 branches on `V03` | **Verified** |
| 5 | `invest_user_story_rubric` is six letter-to-word pairs with no definitions | **Verified** |
| 6 | The story-generation test compares `set(rubric)`, so widening values is safe | **Verified** |
| 7 | 35 files per tree, SHA-256 mirror parity enforced | **Verified** |
| 8 | 15 pre-existing test failures from the `_session` collision | **Verified by re-measuring** |
| 9 | `mvp-scope.md` line 13 and MS05's `accepts_summary` demand an all-pass INVEST | **Verified** |
| 10 | `story-elements.md` claims the KB entry "holds the pairs and nothing else" | **Verified** |
| 11 | An unregistered asset is caught by the story-generation-prompt test | **Wrong** |
| 12 | Widening INVEST means authoring new definitions | **Wrong, and it made the work harder than it is** |
| 13 | `reads` is a flat list of prior atom ids | **Too weak to produce a good turn** |
| 14 | `kb_refs` names top-level knowledge-base keys | **Too coarse** |
| 15 | Gate atoms | **Not mentioned at all** |
| 16 | Express pacing | **Not mentioned at all** |
| 17 | Suggested MS05 `reads` of `C01, C02, C06, U01, MS02, MS03` | **Partly wrong** |

## The corrections that mattered

### 11. The dangling-pointer justification does not hold for lean-mvp

The plan justified registering `atom-coaching.json` in `SKILL.md` by saying an unregistered asset
"would be the kind of dangling pointer the story-generation-prompt test exists to catch." That test,
`tests/test_story_generation_prompt_skill.py::test_declared_references_and_assets_exist_on_disk`, is
scoped to `.cursor/skills/story-generation-prompt/` only. lean-mvp has no equivalent, and
`assets/section-map.json` sits unregistered in lean-mvp's `SKILL.md` today with nothing catching it.

Registering the asset is still right. The reason given was not. The fix was to make the claim true:
the new test now asserts that every `references/`, `assets/`, and `scripts/` path declared in
lean-mvp's `SKILL.md` exists on disk. That check runs in the direction that matters, catching a
declared path with no file. It deliberately does not run the reverse direction, which would have
required registering `section-map.json` and widened the diff for no behavioral gain.

### 12. The INVEST definitions were never missing, only dropped

The plan framed step 2 as authoring definitions. `docs/lean-product-playbook-prompt-suite.md` lines
78 to 85 already carry them:

```json
"I": "Independent (overlap-free, implementable in any order)",
"N": "Negotiable (not an explicit contract, open to discussion)",
```

The shipped `assets/knowledge-base.json` truncated each value to a bare word when it was compiled
from that document. So the work is restoring content from the upstream source, not inventing it, and
it moves the asset back toward the document rather than away from it. That removes the drift risk a
hand-written widening would have created, and it removes the invention risk entirely.

This also turned out to decide the whole feature. Against today's entry, `kb_refs:
["invest_user_story_rubric"]` resolves to `I: Independent. N: Negotiable. ...`, which is exactly the
useless key dump the coaching layer exists to replace. Had the plan been built as written, MS05 would
have shipped a coaching block that taught nothing, and the 22-hour stall would have repeated with
more JSON around it.

### 13 and 14. The entry schema the plan proposed cannot produce the turn it describes

The plan's `reads: ["C01", "C02", ...]` gives the agent a list of atom ids and their raw answer text
and nothing about how they connect. The plan's own goal sentence asks for "a board of the prior
answers the question builds on", and a bare list is not a board.

Two changes fix it. Each prior carries a `why` clause naming what that answer contributes to this
question, so the agent can write "you told me your persona is X, and the benefit you picked to lead
on is Y" instead of reciting rows. Each prior also carries a human label resolved through the
existing `atom_provenance_label` helper, so the agent has a name for the answer and never has to
speak an atom id, which `SKILL.md` already forbids.

Separately, `kb_refs` as bare top-level keys is too coarse. C06 needs one analogy,
`visual_grounding_analogies.follow_me_home`, and a top-level ref would drag all five analogies into
the payload as noise. Refs are dotted paths.

### 15. Gate atoms are a fifth of the DAG and the plan never mentions them

C12, U12, MS12, UX12, and MT12 are review turns, not content questions. The plan's entry shape has no
answer for what `worked_example` or `common_miss` mean on a turn whose only valid answers are pass,
reopen, or blocking unknowns. Both arena candidates raised this independently. The resolution is that
gate atoms use the same six fields with no discriminator field, because `atoms.json` already carries
`gate: true` and a second field would have to be kept in sync with the first.

### 16. Express pacing would have made the plan's test flaky

`EXPRESS_SPINE["mvp-scope"]` is `("MS01", "MS05", "MS12")`. Under express pacing the interview jumps
from MS01 to MS05, so MS05's prior MS04 is never answered. Any test asserting that a coaching entry's
priors carry text at runtime passes under standard pacing and fails under express. Unanswered priors
are therefore normal, are marked `missing`, and the agent skips them without narrating the gap.

### 17. `reads` must not name a gate atom, and the plan's MS05 list is off

The plan proposed MS05 should read `C01, C02, C06, U01, MS02, MS03`. C06 is the follow-me-home
observation plan, which is not something a story sentence is built from. More importantly, nothing in
the plan stopped a coaching entry from naming a gate atom in `reads`, and that would have been a
live defect: `is_ceremony_answer` at `runtime.py:249` only filters text containing both "bypass" and
"gate", so the canonical gate answer `pass mvp-scope gate` passes straight through and would have
been surfaced to the human as evidence they had supplied. `reads` may not name a gate atom, and the
test enforces it.

## What the plan got right that mattered most

The instruction not to import `_session` in the new test. Four existing test files insert a different
skill's `scripts/` directory on `sys.path` and then `import _session` by bare name, so whichever
loads first wins `sys.modules` for the whole run. That is the entire 15-failure cluster. A new test
importing `_session` would have inherited the order dependence and made the suite's behavior depend
on file naming. The plan named the hazard, named two safe patterns already in the repo, and told the
reader to re-measure the baseline rather than trust its own number. That instruction was followed and
the number was confirmed at 15 failed, 100 passed.

The plan was also right to keep MS05 whole rather than splitting it, right that the sidecar asset
belongs outside `atoms.json`, and right that the payload change is additive because nothing validates
it against a schema.
