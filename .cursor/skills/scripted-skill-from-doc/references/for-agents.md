# Prompt suite → paced skill (for agents)

The human pointed you at this file. Follow it. Do not invent a different process.

## What they want

They want a paced Cursor skill built from one prompt-suite markdown file. Mechanical extract and scaffold use the CLIs under **this skill’s `scripts/`**. Curriculum expansion follows **references/curriculum-synthesis.md** (poteto-mode optional if installed). Do not touch a skill named `value`, and do not write into `skills/value/` or `.cursor/skills/value/`.

## Pack location

**Skill root:** `.cursor/skills/scripted-skill-from-doc/`

Standard layout: `SKILL.md`, `scripts/`, `references/`, `assets/`. It travels with the `.cursor` harness. Prefer commands relative to the **target repo root**.

Legacy shims under `tools/prompt-suite-compile/` forward to `scripts/` if present.

## Inputs they will give

- Source path to a prompt-suite markdown file (Document Architecture, knowledge-base JSON, orchestrator, and subskill prompts).
- Skill slug (lowercase with hyphens). Never `value`.
- Whether to stop at a draft folder or promote after checks.

## Steps

1. Read `references/curriculum-synthesis.md` before expanding atoms (optional: `/poteto-mode` if installed).
2. From the target repo root, run scaffold:

```text
python .cursor/skills/scripted-skill-from-doc/scripts/compile.py scaffold --source <doc> --slug <slug> --out tools/drafts/skills
```

3. Read the draft `COMPILE-NOTES.md` and `ir.json`.
4. Expand seeded or stub atoms into a shippable curriculum under `assets/atoms.json` per curriculum-synthesis. Update `section-map.json`, templates, and module references. Keep one primary question per atom. Promote refuses stub-ask placeholders.
5. Run:

```text
python .cursor/skills/scripted-skill-from-doc/scripts/audit_dag.py tools/drafts/skills/<slug> --mode both
```

Fix until standard mode reports `"ok": true`.

6. Smoke:

```text
python .cursor/skills/scripted-skill-from-doc/scripts/smoke.py tools/drafts/skills/<slug>
```

7. Stop and ask before promote. On explicit yes:

```text
python .cursor/skills/scripted-skill-from-doc/scripts/promote.py tools/drafts/skills/<slug>
```

If the live skill already exists, also pass `--force --overwrite-slug <slug>`. Pass `--also-skills` only if they ask for a ship surface under `skills/<slug>/`. Pass `--repo` if promote should target a different repo root.

## Fences

- Never overwrite `value` or `scripted-skill-from-doc`.
- Never invent prior session answers in pressure tests.
- Never quote script JSON atom IDs to the end user in skill voice.
- Gate accept autofills `decisions[]` when `--gate-pending` or the canonical pass phrase is used; do not soft-lock waiting for a separate records flag.

## Done looks like

Draft under `tools/drafts/skills/<slug>/` with expanded atoms, audit ok, smoke ok, and promote only after the human said yes.
