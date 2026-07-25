# Fresh chat — Story scenario suite (S01–S08)

Paste this block to start a new session.

---

## One-line mission

Walk **all eight** graded fixtures in `tools/drafts/story-scenario-suite/` against `/story-generation-prompt`. Score each case. Log pass/fail. Close the gate PASSED only if every case passes.

**Do not** skip cases. **Do not** invent evidence to force a pass. **Do not** edit shipped skills unless a FAIL blocker names one coaching hole.

---

## Preconditions (do first)

1. Confirm `python -m pytest tests/test_story_generation_prompt_skill.py -v` is green.
2. Read `handoff/STORY-SCENARIO-SUITE-OPEN.md` and `handoff/STATE.md`.
3. Read pack index: `tools/drafts/story-scenario-suite/README.md` + `MANIFEST.tsv`.
4. Read `.cursor/skills/story-generation-prompt/SKILL.md` (then case-named refs only).

---

## Required walk (blocking)

For **S01 → S08** in order:

1. Open `tools/drafts/story-scenario-suite/cases/<id>-*.md`.
2. Play **Input** as the human (one case at a time).
3. Respond as the skill contracts require.
4. Score **Pass check** → `pass` or `fail`.
5. Append one row to `handoff/decision-trails/story-scenario-suite.tsv`.

After all eight (or abort on human request):

6. Write `tools/drafts/story-scenario-suite/WALK-EVIDENCE.md` (short per-case: outcome + one quote of the key coaching move or miss).
7. Close `handoff/STORY-SCENARIO-SUITE-PASSED.md` if 8/8 pass, else `...-FAILED.md` with **one** primary blocker (first fail id + axis).
8. Re-run `python -m pytest tests/test_story_generation_prompt_skill.py -v`.

---

## Case map (do not reorder)

| ID | Band | Axis |
|----|------|------|
| S01 | typical | evidence → try-stage story |
| S02 | typical | repo-only → pass-1 first |
| S03 | adversarial | funnel inflate |
| S04 | adversarial | implementation in want |
| S05 | adversarial | demographic persona |
| S06 | adversarial | prompt→story missing cost |
| S07 | boundary | I/E/S empty honesty |
| S08 | adversarial | hype producer paste |

---

## Hard constraints

- Primary skill: story-generation-prompt. S08 may use `/product-spine` claim entry, then story inline.
- No value/lean session init unless a case explicitly requires it (none of S01–S08 do).
- No atom IDs to the simulated human.
- No commits unless user asks.

---

## Success looks like

- TSV has eight rows with pass/fail.
- WALK-EVIDENCE summarizes each case.
- Gate closed PASSED (8/8) or FAILED (named blocker).
- Story skill pytest still green.
