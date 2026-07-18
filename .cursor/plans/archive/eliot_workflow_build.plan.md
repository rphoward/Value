---
name: ELIOT Workflow Build
overview: Wire the three existing engines (ELIOT v5.7, Idea Distiller, Universal Writing Evaluator) into one repo-scoped skill pipeline with a cold-audit subagent and a measured hillclimb loop, plus a served front end. Supersedes handoff/PLAN.md, which stays as history.
status: completed
todos:
  - id: phase0-freeze-shapes
    content: "Phase 0: freeze Dense Style Block + EvaluatorScore shapes"
    status: completed
  - id: phase1-eliot-skill
    content: "Phase 1: ELIOT skill split + 3-way compare gate (Run C)"
    status: completed
  - id: phase3-evaluator-skill
    content: "Phase 3: evaluator v3 — 12-axis block scoring, eval-audit subagent, reproducible CLI"
    status: completed
  - id: phase5-loop
    content: "Phase 5: hillclimb loop — workflow skill + loop.py + hillclimb_once.py + tests"
    status: completed
  - id: phase2-drift-subagent
    content: "Phase 2: cold drift-audit subagent (style block + draft only)"
    status: completed
  - id: phase4-distiller-skill
    content: "Phase 4: Idea Distiller skill + exa MCP + phase 4 emulation prompts"
    status: completed
  - id: phase-pipeline
    content: "Pre-UI pipeline: catalog, owned corpus, passage bounds, pipeline skill"
    status: completed
  - id: phase6-service
    content: "Phase 6: presentation surface (Starlette + HTMX)"
    status: completed
  - id: phase7-automation
    content: "Phase 7 (optional): Cursor Automation drives loop unattended — superseded by hooks + SDK climb (HOOKS-SDK-PASSED)"
    status: completed
isProject: true
---

# ELIOT Workflow Build

Classical-literature analyzer and emulator. Read `handoff/WORKFLOW.md` for the pipeline
in the owner's words. **Living state:** `handoff/STATE.md`. This plan is archived;
phases 0–6 shipped, phase 7 superseded by `handoff/HOOKS-SDK-PASSED.md`.

## Decisions already made (do not re-litigate)

- **Slug is `eliotwf`.** Scaffold has run. `src/eliotwf/{core,application,infrastructure,presentation}/`
  exist, `pyproject.toml` names the package, Starlette health app is in `presentation/app.py`.
- **ELIOT is a skill**, the **cold drift audit is a subagent**, no permanent custom chat
  agent, and an automation only drives the loop. See `handoff/ARCHITECTURE.md`.
- **A served front end is in scope.** `presentation/app.py` stays and grows (Phase 6).
- **IRIS and Pierce are out of scope.** They stay co-located in `eliotworkflow/` as
  reference, not part of this product.
- **Skills are repo-scoped** under `.cursor/skills/` with Python modules in
  `src/eliotwf_skills/`, per `skill-authoring.mdc` and `skills-repo.mdc`.
- **Web and corpus search uses the `exa` MCP**, already installed in this workspace.

## Data shapes (frozen — Phase 0 complete)

1. **Dense Style Block** — `src/eliotwf_skills/shapes/dense_style_block.py`; gold in
   `.cursor/skills/eliot/references/examples-dostoevsky.md`.
2. **EvaluatorScore** — `src/eliotwf_skills/shapes/score.py`; 12 section axes, 13-slot
   vector, deterministic SURFACE/PROSODY/CAST + qualitative nine via rubric.

## Phases

### Phase 0. Freeze the shapes — DONE
See `src/eliotwf_skills/shapes/`. Gate: `ELIOT-GATE-PASSED.md`, `EVALUATOR-GATE-PASSED.md`.

### Phase 1. ELIOT as a repo-scoped skill — DONE
`.cursor/skills/eliot/`. Compare gate: `tools/runs/eliot-compare/2026-07-06/`.

### Phase 2. Cold drift-audit subagent — DONE
`.cursor/agents/drift-audit.md` ships the cold worker.

### Phase 3. Evaluator as a skill — DONE (v3)
`.cursor/skills/evaluator/`, `eval-audit` subagent, `score_fixture.py`. StyleBlockDiff +
DraftOnly modes. Record: `EVALUATOR-GATE-PASSED.md`.

### Phase 4. Distiller for the upstream phases — DONE
`.cursor/skills/distiller/` v1.1: phases 1–4, register routing, owned corpus (ADR 002),
passage bounds 200–2000. Exa MCP for web provenance.

### Phase 4b. Pre-UI pipeline contracts — DONE
`handoff/PIPELINE-UI-CATALOG.md`, `.cursor/skills/pipeline/SKILL.md`,
`handoff/PIPELINE-SMOKE-PASSED.md`.

### Phase 5. The loop — DONE
Thin orchestrator skill: emulate, eval-audit, record, compare delta, stop or retry.

### Phase 6. Served front end — DONE (v1)
`presentation/app.py` serves hillclimb runs via HTMX. Stack stays Starlette + Jinja + HTMX.

### Phase 7. Optional automation
If unattended runs are wanted, a Cursor Automation drives the Phase 5 loop. The automation is
the driver; the logic stays in the skills.

## Verification bar

- Phase 0: the two reference files exist and each field is named.
- Phase 1/3: each engine run is checked against a pinned fixture and an expected shape.
- Phase 3/5: the Score is reproducible and comparable across runs.
- Phase 6: `pip install -e .` then the app serves the pipeline end to end.
