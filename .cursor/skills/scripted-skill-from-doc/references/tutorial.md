# Tutorial: prompt suite to paced skill

This tutorial stays inside `.cursor/skills/scripted-skill-from-doc/`. Copy that whole skill folder (or the whole `.cursor` tree) into another repo to take the harness with you.

## Goal

Start with one book-shaped prompt-suite markdown file. End with a draft paced Cursor skill that can ask one question at a time and store answers in a session file. Promote that draft into `.cursor/skills/<slug>/` only when you choose to.

## Step 1. Confirm the pack works

From your repo root:

```text
python .cursor/skills/scripted-skill-from-doc/scripts/compile.py check
python .cursor/skills/scripted-skill-from-doc/scripts/selftest.py
```

Both should succeed. Thin shims under `tools/prompt-suite-compile/` still work if present; prefer the skill `scripts/` path.

## Step 2. Choose a source document

Use your own suite markdown, or the sample:

```text
.cursor/skills/scripted-skill-from-doc/assets/fixtures/sample-prompt-suite.md
```

A suite needs a Document Architecture section, a Central Reference Knowledge Base JSON fence, a Master Orchestrator Prompt, and one or more Subskill prompts. Headings should match the patterns the parser expects. See the sample file for a minimal shape.

## Step 3. Scaffold

Pick a slug that is not `value`. Example:

```text
python .cursor/skills/scripted-skill-from-doc/scripts/compile.py scaffold --source .cursor/skills/scripted-skill-from-doc/assets/fixtures/sample-prompt-suite.md --slug demo-suite --out tools/drafts/skills
```

Open `tools/drafts/skills/demo-suite/`. You should see `SKILL.md`, `assets/`, `scripts/`, `references/`, `COMPILE-NOTES.md`, and `ir.json`.

Stub atoms use ids like `S01` and `G01`. They are placeholders. They are good enough for audit and smoke. They are not a finished curriculum.

## Step 4. Expand the curriculum

Point Cursor at `references/for-agents.md`. Activate `/poteto-mode` if you have it. Ask the agent to replace stub atoms with real questions, soft and hard labels, unlocks, and module voice.

Keep one primary question per atom. Do not invent answers for pressure tests.

## Step 5. Audit and smoke

```text
python .cursor/skills/scripted-skill-from-doc/scripts/audit_dag.py tools/drafts/skills/demo-suite --mode both
python .cursor/skills/scripted-skill-from-doc/scripts/smoke.py tools/drafts/skills/demo-suite
```

Standard mode must be ok. Smoke should print an atom id and `smoke ok`.

## Step 6. Promote when you say so

```text
python .cursor/skills/scripted-skill-from-doc/scripts/promote.py tools/drafts/skills/demo-suite
```

If that slug already exists under `.cursor/skills/`, add `--force --overwrite-slug demo-suite`. Add `--also-skills` only if you also want `skills/demo-suite/` as a ship folder.

## What success looks like

- `compile.py check` and `selftest.py` pass under `scripts/`.
- The draft runs `init_session` and `next_question` through smoke.
- The skill slug is never `value`.
- Promote happened only after you asked for it.

## What this pack does not do

It does not write finished judgment for you. Soft versus hard atoms, question wording, and skill voice stay human or poteto-mode work. It also does not replace an existing Values skill named `value`.
