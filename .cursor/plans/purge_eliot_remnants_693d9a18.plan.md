---
name: Purge ELIOT remnants
overview: Remove the dead ELIOT-project machinery left in .cursor/ (agents, command, hook, plans archive) and the EliotWF names in low-risk rules and scaffold docs. The scaffold write gate in repo-layout.mdc and thermonuclear.mdc is deliberately deferred to a separate job.
todos:
  - id: delete-agents-command
    content: Delete all ten .cursor/agents/*.md files and .cursor/commands/hillclimb.md
    status: completed
  - id: hooks
    content: Delete .cursor/hooks/validate_skills_module.py, remove its afterFileEdit entry from .cursor/hooks.json, and strip the sdk-climb block (lines 40-53) from run_tests_on_stop.py
    status: completed
  - id: canvas-path
    content: Fix the canvas mirror path in cursor-artifacts-scope.mdc from c-Projects-EliotWF to c-Projects-value
    status: completed
  - id: layer-globs
    content: Drop the eliotapp/<layer>/** prefix from the globs in core-domain, application-layer, infrastructure-wiring, and presentation-surface
    status: completed
  - id: plans
    content: Delete .cursor/plans/archive/ plus proto_shell_chrome and studio_chat_file_ui, then rewrite .cursor/plans/README.md to index the seven surviving Value plans
    status: completed
  - id: scaffold-docs
    content: Remove the EliotWF paragraph from .cursor/scaffold/INIT.md and the EliotWF note from .cursor/scaffold/README.md
    status: completed
  - id: stray-tree
    content: Pause for explicit approval, then delete tools/start-eliotwf.ps1 and the duplicate src/eliotwf/ tree
    status: completed
  - id: verify
    content: Run python -m pytest tests/ -q, then manually copy .cursor/ to a temp folder and read the rules as a fresh repo would; report both
    status: completed
isProject: false
---

# Purge ELIOT remnants from `.cursor/`

## What is wrong

This repo was cloned from EliotWF. The skills, tests, and `workproduct/` tree are real Value work, but a layer of ELIOT machinery came along and none of it resolves:

- `eliotapp/` does not exist (globbed `eliotapp/**/*.py`, zero files), yet 8 rule files name it.
- `.cursor/skills/eliot/`, `.cursor/skills/evaluator/`, `.cursor/skills/workflow/`, `tools/runs/`, and `hillclimb_once.py` are all absent, yet ten subagents and one command drive them.
- `cursor-artifacts-scope.mdc` grants a write exception to `~/.cursor/projects/c-Projects-EliotWF/canvases/` — another project's directory, always applied.

Nothing under `.cursor/skills/` is touched by this plan.

## Deliberately out of scope

`repo-layout.mdc` and `thermonuclear.mdc` are **not** touched in this pass. The reason is specific, not caution for its own sake.

`protocol-0-write-path-gate` in `repo-layout.mdc` resolves `eliot_home` and branches on it in five places (lines 20, 28, 34, 38, 39), and `protocol-1c` is what defines it. It is also a cross-file contract — `thermonuclear.mdc` reaches in by protocol name:

```
      (or (paths-under 'repo-layout.mdc eliot_home)
          (paths-under 'repo-layout.mdc product-home)
          (paths-under 'repo-layout.mdc skills_home)
```

Removing `eliot_home` and `skills_home` means rewriting the write gate that every repo you scaffold inherits, and updating both always-applied rules in lockstep. There is no fixture to test it against: `tests/fixtures/retarget_mini`, which `INIT.md` documents for a dry run, does not exist in this repo. That job gets its own pass.

Also left alone: `skills-repo.mdc` and `skill-authoring.mdc`, whose `eliotapp` module-home language depends on the same protocol names; and `pstack-models.mdc`, whose `hillclimb: composer-2.5` line may belong to the pstack plugin rather than the ELIOT command.

## Deletions

Whole files, each verified unreferenced by any test, `handoff/` doc, or `docs/` file:

- All ten [.cursor/agents/](.cursor/agents/) files — `content-adherence`, `corpus-fetch`, `discriminate`, `drift-audit`, `emulate-drafter`, `eval-audit`, `pair-judge`, `quality-judge`, `reference-preference`, `revise-drafter`.
- [.cursor/commands/hillclimb.md](.cursor/commands/hillclimb.md) — loads a missing `.cursor/skills/workflow/SKILL.md`, drives a missing `hillclimb_once.py`.
- [.cursor/hooks/validate_skills_module.py](.cursor/hooks/validate_skills_module.py) — returns early unless the path contains `eliotapp/`, so it is a no-op process launch on every Write and StrReplace.
- [.cursor/plans/archive/](.cursor/plans/archive/) — roughly 110 ELIOT-history files.
- [.cursor/plans/proto_shell_chrome_bea608af.plan.md](.cursor/plans/proto_shell_chrome_bea608af.plan.md) and [.cursor/plans/studio_chat_file_ui_c608ab83.plan.md](.cursor/plans/studio_chat_file_ui_c608ab83.plan.md) — ELIOT UI plans.
- [tools/start-eliotwf.ps1](tools/start-eliotwf.ps1) and `src/eliotwf/` — the script runs `uvicorn eliotwf.presentation.app:app`; the tree is a full duplicate of `src/value/`. Safe on paper: `pyproject.toml` builds the `value` package from `where = ["src"]` and the suite imports only `value.presentation.app`. Still structural, so I stop and ask before this step.

## Edits

`.cursor/hooks.json` — drop the `afterFileEdit` block that invoked the deleted hook; keep the `stop` pytest hook.

[.cursor/hooks/run_tests_on_stop.py](.cursor/hooks/run_tests_on_stop.py) — delete lines 40-53, the `tools/runs/.sdk-climb-last.json` progress reporter. The pytest half stays; `tests/` has 19 real test files.

`cursor-artifacts-scope.mdc` line 17 — `c-Projects-EliotWF` becomes `c-Projects-value`. This is the highest-value single fix here, because it is always applied and currently points at another project.

`core-domain.mdc`, `application-layer.mdc`, `infrastructure-wiring.mdc`, `presentation-surface.mdc` — each glob line drops the `eliotapp/<layer>/**,` prefix, leaving the `src/value/<layer>/**` half that retarget maintains. These four are safe because they are path-scoped globs only, with no protocol-name dependencies.

[.cursor/plans/README.md](.cursor/plans/README.md) — currently says "Cursor plan files for EliotWF", indexed 2026-07-17, lists one active plan and omits the seven real ones. Rewrite to index the survivors: `coaching_out-of-scope`, `ship_gate_presentation`, `values_skill_five_upgrades`, `value_skill_ide_export_pack`, `value_skill_user_voice_fresh`, `value_skill_dag_pacing`, `value_skill_recovery`, plus `prompt-suite-to-skill/`. Drop the archive and deferred sections that point at deleted files.

[.cursor/scaffold/INIT.md](.cursor/scaffold/INIT.md) line 5 and [.cursor/scaffold/README.md](.cursor/scaffold/README.md) line 5 — both open with an "EliotWF: Eliot code lives at root `eliotapp/`" note. Remove both paragraphs so the scaffold docs describe only the `src/<slug>/` workflow.

## Verification

Two steps, both reported with actual output:

1. `python -m pytest tests/ -q` from the repo root. Note that [tests/test_scaffold.py](tests/test_scaffold.py) is only a 15-line app-factory smoke test, not a retarget test, so the suite proves the `value` package still imports and the skills tests still pass — nothing more. No guard test is added in this pass, since the rules that carry the remaining `eliot` tokens are deliberately deferred and a guard would fail on them.
2. Copy `.cursor/` into a temp folder and read `repo-layout.mdc`, the layer rules, and the scaffold docs as a fresh repo would, confirming the remaining text is coherent for a new project.
