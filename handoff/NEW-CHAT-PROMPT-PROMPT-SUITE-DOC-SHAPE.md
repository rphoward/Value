# Fresh chat — Prompt-suite doc shape (generator prompt)

Paste this block to start a new session. Then attach or paste the **upstream prompt** you used to create the misshapen High-Impact Tools Suite.md so we can compare.

---

## One-line mission

Write a **reusable generator prompt** that produces prompt-suite markdown in the shape `scripted-skill-from-doc` already accepts (`parse_suite` / `compile.py`), so the next book/framework suite does not need a one-off normalizer.

**Do not** bend `compile.py` to accept broken exports as the default fix. **Do not** expand into branding, teams milestone templates, or verify-map work unless redirected.

---

## Preconditions (read first)

1. `handoff/PROMPT-SUITE-DOC-SHAPE-OPEN.md` (this gate).
2. Compiler contract (source of truth):
   - `.cursor/skills/scripted-skill-from-doc/scripts/compile.py` — `parse_suite`, heading regexes, `FENCE_JSON_RE` / `FENCE_MD_RE`
   - `.cursor/skills/scripted-skill-from-doc/references/for-agents.md`
3. Good exemplars (match these headings + fences):
   - `.cursor/skills/scripted-skill-from-doc/assets/fixtures/sample-prompt-suite.md`
   - `docs/value-proposition-prompt-suite (1).md`
   - `docs/lean-product-playbook-prompt-suite.md`
   - `docs/business-model-generation-prompt-suite.md`
4. Misshape → fixed target:
   - Current good: `docs/High-Impact Tools Suite.md` (normalized)
   - One-shot rescue (not the goal): `tools/normalize-teams-prompt-suite.py`
5. Proof command after any sample emit:

```text
python .cursor/skills/scripted-skill-from-doc/scripts/compile.py parse --source <path-to.md>
```

Expect non-empty `knowledge_base`, orchestrator `name` set, and modules with non-empty `prompt_markdown`.

---

## Context from prior session (do not re-litigate)

| Fact | Detail |
|------|--------|
| Symptom | Original Teams suite export parsed to `{}` KB, null orchestrator, `modules: []` |
| Root cause | Wrong heading level/wording, missing fences, Docs escapes, nested ```markdown, base64 images |
| Teams skill | Promoted to `.cursor/skills/teams/` + spine weave (tam-planner bounce like BMG canvas-mapper) |
| Verify map | `verify-value` expanded for `--skill value\|bmg\|teams\|lean-mvp` — **side path**; only use after a suite compiles if proving the skill |

---

## Required walk

1. Human supplies the **old generator prompt** (the one that made the misshapen doc).
2. Agent maps each misshape class to a missing or wrong instruction in that prompt.
3. Agent drafts a **new generator prompt** that forces:
   - `## Document Architecture` numbered list
   - `## 1. Central Reference Knowledge Base…` + ` ```json ` fence (valid JSON, no `\_` escapes)
   - `## 2. Master Orchestrator Prompt (\`Name\`)` + ` ```markdown ` fence (no nested triple-backticks)
   - `## N. Subskill K Prompt (\`Name\`)` + one ` ```markdown ` fence each
   - No base64 image embeds; plain text for formulas / “≤10 words”
4. Acceptance checklist attached to the prompt (human-facing): run `compile.py parse`; refuse to ship if modules empty.
5. Optional dry-run on a tiny topic; parse must succeed.
6. Close gate PASSED/FAILED with one blocker.

---

## Done when

- New generator prompt exists in-chat (and optionally under `docs/` or `handoff/` if the human asks to save it).
- Explicit comparison to the old prompt (what changed and why).
- At least one `compile.py parse` proof plan (or live dry-run) is named.
- Gate closed as PASSED or FAILED.

---

## Out of scope unless asked

- Filling teams milestone templates from suite STANDARDIZED TEMPLATE blocks
- `/create-verification-skill` / `/maintain-verification-skill` map work
- Promoting or shipping a new skill from a fresh suite
