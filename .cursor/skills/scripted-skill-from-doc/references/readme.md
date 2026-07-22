# scripted-skill-from-doc (portable pack)

This Cursor skill is the complete prompt-suite-compile toolkit in standard skill layout (`SKILL.md`, `scripts/`, `references/`, `assets/`). Copy or sync the whole `.cursor` tree and the harness travels with you.

It turns a prompt-suite markdown file into a draft paced Cursor skill. You expand the question tree with judgment. Then you promote the draft when ready.

## What you need

- Python 3.10 or newer on your PATH
- A prompt-suite markdown file, or use `assets/fixtures/sample-prompt-suite.md`
- Cursor for `/scripted-skill-from-doc` and `/poteto-mode` curriculum work

Stdlib only. No pip packages.

## Self-check (from repo root)

```text
python .cursor/skills/scripted-skill-from-doc/scripts/compile.py check
python .cursor/skills/scripted-skill-from-doc/scripts/selftest.py
```

## Commands (repo root)

```text
python .cursor/skills/scripted-skill-from-doc/scripts/compile.py scaffold --source path/to/suite.md --slug my-skill --out tools/drafts/skills
python .cursor/skills/scripted-skill-from-doc/scripts/audit_dag.py tools/drafts/skills/my-skill --mode both
python .cursor/skills/scripted-skill-from-doc/scripts/smoke.py tools/drafts/skills/my-skill
python .cursor/skills/scripted-skill-from-doc/scripts/promote.py tools/drafts/skills/my-skill
```

Never scaffold or promote a skill named `value` or `scripted-skill-from-doc`. Overwriting an existing live skill requires `--force --overwrite-slug <slug>`.

## Agent entry

Open `references/for-agents.md`. Prefer `/poteto-mode` for expanding atoms.

More detail: `references/bootstrap.md` and `references/tutorial.md`.

## Legacy path

`tools/prompt-suite-compile/` may still contain thin shims that forward into `scripts/` for old docs and scripts.
