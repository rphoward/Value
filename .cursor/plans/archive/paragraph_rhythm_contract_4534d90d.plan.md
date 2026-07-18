---
name: paragraph rhythm contract
overview: "Repair 15231dc REVISE blocker — qualitative paragraph_modes in block; numeric clone detection in scorer only. Step 0 must land before any product edit."
todos:
  - id: scope-step0
    content: "EXEC step 0 — replace poisoned .scope.json (no product edits before this)"
    status: completed
  - id: commit-1-python
    content: "EXEC commit 1 — Python revert + narrow scorer (5 files); first edit loop.py:133"
    status: completed
  - id: commit-2-contract
    content: "EXEC commit 2 — paragraph_modes + skill/agent docs (9 files)"
    status: completed
  - id: commit-3-tests
    content: "EXEC commit 3 — tests, cleanup, pytest green; close STATE.md gate"
    status: completed
isProject: false
---

# Paragraph rhythm contract

**Status: IMPLEMENTED (2026-07-08).** Forward fix landed; `init_run` no longer stamps; block uses `paragraph_modes:`.

## Final-review blocker (2026-07-08)

Master still ships the REVISE contract. Mechanical `dist %` in the style block plus `init_run` stamping. [`.scope.json`](.scope.json) acceptance explicitly requires that wrong behavior (`prepare writes paragraphs_line; init stamps style-block`).

**Do not touch product files until Step 0 replaces `.scope.json`.**

## Why agents keep re-proposing dist %

| Trap source | What it tells the agent |
|-------------|-------------------------|
| `.scope.json` | Automate stamp at init — **this IS 15231dc's wrong contract** |
| `paragraph_behavior.py` | `format_paragraphs_line` → `dist 1-4s(%)` |
| `loop.py:133` | `stamp_paragraphs_from_calibration` overwrites analyzer |
| ELIOT refs + tests | "distribution required"; assert `dist 1-4s(` is correct |

**Correct split:**

| Layer | Field | Content | Writer |
|-------|-------|---------|--------|
| Style block | `paragraph_modes:` | Qualitative opens/closes/arc variety; NO % | ELIOT analyzer |
| Style block | `paragraphs:` | Optional short prose; NEVER `dist …%` | Analyzer |
| `calibration.json` | counts, `paragraph_varies`, word range | Numeric facts for scorer | `prepare` |
| Scorer v2 | clone heuristics | sent-range + word-range; NO bucket L1 | Python |
| CADENCE axis | arc/length judgment | Read block prose | eval-audit |

---

## Step 0 — replace `.scope.json` (mandatory gate)

**No product edit before this file is written.**

Replace [`.scope.json`](.scope.json) entirely:

```json
{
  "prompt": "<hook-owned — do not edit>",
  "intent": "Separate paragraph emulation (qualitative paragraph_modes in block) from paragraph clone detection (numeric calibration + scorer heuristics). Remove init stamping and dist-% from block contract.",
  "decomposition": [
    "A: Python — delete stamp/format helpers; narrow scorer; fix is_single_template",
    "B: ELIOT + workflow docs — paragraph_modes contract; anti-dist-% traps",
    "C: Tests — invert assertions; delete smoke artifacts; pytest green"
  ],
  "files": [
    ".scope.json",
    "src/eliotwf_skills/workflow/loop.py",
    "src/eliotwf_skills/eliot/paragraph_behavior.py",
    "src/eliotwf_skills/evaluator/calibration.py",
    "src/eliotwf_skills/evaluator/score_draft_v2.py",
    "src/eliotwf_skills/eliot/scorecard.py",
    ".cursor/skills/eliot/references/workflows.md",
    ".cursor/skills/eliot/references/validation.md",
    ".cursor/skills/eliot/references/output-format.md",
    ".cursor/skills/eliot/references/examples-dostoevsky.md",
    ".cursor/skills/eliot/references/extensions.md",
    ".cursor/agents/emulate-drafter.md",
    ".cursor/skills/workflow/references/one-command.md",
    ".cursor/skills/evaluator/references/style-block-rubric.md",
    "src/eliotwf_skills/shapes/dense_style_block.py",
    "tests/test_hillclimb.py",
    "tests/test_prepare.py",
    "tests/test_paragraph_behavior.py"
  ],
  "acceptance": "style block has paragraph_modes (no dist %); init does not stamp paragraphs; calibration has no paragraphs_line; uniform rilke draft scores low on paragraph subscore; pytest green"
}
```

**Wrong acceptance (delete):** `prepare writes paragraphs_line; init stamps style-block`

---

## Commit 1 — Python (5 files)

**First product edit:** remove `stamp_paragraphs_from_calibration` at [`loop.py:133`](src/eliotwf_skills/workflow/loop.py).

1. [`src/eliotwf_skills/workflow/loop.py`](src/eliotwf_skills/workflow/loop.py) — remove stamp call; copy analyzer block unchanged
2. [`src/eliotwf_skills/eliot/paragraph_behavior.py`](src/eliotwf_skills/eliot/paragraph_behavior.py):
   - Delete: `format_paragraphs_line`, `stamp_paragraphs_line`, `stamp_paragraphs_from_calibration`, `paragraphs_line` on dataclass
   - Add: `has_paragraph_modes(block: str) -> bool`
   - Fix: `is_single_template_paragraphs` — remove dist-% bypass (lines 114–115)
   - Narrow: `paragraph_uniformity_score` — clone heuristics only; remove bucket L1 (lines 175–186)
3. [`src/eliotwf_skills/evaluator/calibration.py`](src/eliotwf_skills/evaluator/calibration.py) — remove `paragraphs_line`, `paragraph_bucket_shares` from contract
4. [`src/eliotwf_skills/evaluator/score_draft_v2.py`](src/eliotwf_skills/evaluator/score_draft_v2.py) — drop `source_bucket_shares` from call
5. [`src/eliotwf_skills/eliot/scorecard.py`](src/eliotwf_skills/eliot/scorecard.py) — check `paragraph_modes` not dist shares

---

## Commit 2 — Contract + prompts (9 files)

| File | Change |
|------|--------|
| `.cursor/skills/eliot/references/workflows.md` | Step 12b: emit `paragraph_modes:`; delete init-stamp |
| `.cursor/skills/eliot/references/validation.md` | FAIL on dist %; require `paragraph_modes` when source varies |
| `.cursor/skills/eliot/references/output-format.md` | `paragraph_modes:` not dist shares |
| `.cursor/skills/eliot/references/examples-dostoevsky.md` | Qualitative modes example |
| `.cursor/skills/eliot/references/extensions.md` | Remove `:compact "paragraphs: dist 1-4s…"` |
| `.cursor/agents/emulate-drafter.md` | Brief from `paragraph_modes` prose |
| `.cursor/skills/workflow/references/one-command.md` | Remove init-stamp line |
| `.cursor/skills/evaluator/references/style-block-rubric.md` | CADENCE trap |
| `src/eliotwf_skills/shapes/dense_style_block.py` | Skeleton shows `paragraph_modes:` |

**Doc trap (add explicitly):** `fingerprint:` numbers are sentence-level. `paragraph_modes:` is prose-only. Never copy calibration bucket shares into the block.

**Example `paragraph_modes` (Rilke, no percentages):**

```
  paragraph_modes: shapes as jobs — teller hedge / childhood house-swell / wandering digression /
    present-tense return scene / wordless refusal / quiet deferred close; length+internal
    rhythm match source; short declaratives stay inside paragraphs as departures
```

---

## Commit 3 — Tests + cleanup

| File | Change |
|------|--------|
| `tests/test_hillclimb.py` | `test_init_preserves_analyzer_block` — no dist % after init |
| `tests/test_prepare.py` | `paragraph_varies` + counts; no `paragraphs_line` |
| `tests/test_paragraph_behavior.py` | keep regression test; inline varied draft string |
| Delete | `tools/runs/rilke-paragraph-e2e/` entire tree |
| Delete | `tools/runs/eliot-compare/2026-07-06/scorecard.json` churn |

```powershell
cd C:\Projects\EliotWF
$env:PYTHONPATH="src"
pytest tests/ -q
```

Update [`handoff/STATE.md`](handoff/STATE.md) to close paragraph rhythm gate.

---

## What to keep from 15231dc

- `paragraph_uniformity_score` clone detection (narrowed)
- `test_regression_uniform_paragraph_draft_scores_low`
- `PROSODY_PARAGRAPH_WEIGHT = 0.2`
- Calibration: `paragraph_varies`, counts, word range

## Out of scope

- Full hillclimb convergence
- Web UI changes
- `git revert 15231dc` (forward-fix commits preferred)

## Agent discipline

1. Step 0 `.scope.json` before any product file
2. First product edit: `loop.py:133` remove stamp
3. Three commits in order; pytest between commits
4. Say "ACCEPT step N" after each commit
5. Do not start 14-file edit without explicit **execute the plan**

## Canonical handoff

Paste block and full context: [`handoff/NEW-CHAT-PROMPT-PARAGRAPH-RHYTHM.md`](handoff/NEW-CHAT-PROMPT-PARAGRAPH-RHYTHM.md)
