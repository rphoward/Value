# Prompt-suite → scripted skill (portable)

## Context

Building `value` and `lean-mvp` showed a repeatable recipe. A structured book/prompt-suite markdown becomes a paced Cursor skill with `atoms.json`, session scripts, references, and workproduct state. That work was manual and repo-bound. The goal is a **rerunnable lever** you can drop into an empty repo with one sample doc, invoke via poteto-mode, and get a scripted skill without destroying existing golden skills.

## Scope

**In**

- Input contract for prompt-suite docs (Document Architecture + KB JSON + orchestrator + N subskill prompts).
- Deterministic extractor for KB, section inventory, and scaffold tree.
- Portable session-runtime template (stdlib scripts peeled from `value`, curriculum-agnostic).
- Poteto-mode runbook (`FOR_AGENTS.md`) that drives atom synthesis, DAG checks, SKILL.md authoring, and pressure tests.
- Golden fixture. Recompile `docs/value-proposition-prompt-suite (1).md` and diff against `skills/value/` (allowed deltas only).
- Standalone bootstrap for a fresh repo (pstack enabled, skill lands under `.cursor/skills/<slug>/`).

**Out**

- Benny / Slack automations.
- Mutating `skills/value/` or the Values distribution repo as part of the compiler.
- Auto-shipping to GitHub without a human gate.
- Guaranteeing book-quality judgment with zero review (atoms soft/hard, express spine, voice).
- PDF/OCR ingest (markdown prompt-suite only for v1).

## Constraints

- Target runtime is Cursor agent skills (`SKILL.md` + `references/` + `assets/` + `scripts/`).
- Scripts stay stdlib Python unless the host repo already has deps.
- Session root pattern. `workproduct/<skill-slug>/<project-slug>/session.json`.
- Source doc is authoring input only. Compiled assets are runtime truth (same as lean-mvp today).
- Prefer extract-and-template over a shared monorepo engine so a foreign repo does not need `eliotapp/`.
- **Reusable from value.** `_session/{catalog,runtime,render}.py`, CLI surface, `session.schema.json` top-level shape, `atoms.json` field set, workproduct layout.
- **Stay out of the template.** `voice.py` pitch helpers, build-pack/design-brief writers, fixed `workproduct/value-proposition/`, domain KB keys, atom ID vocabularies.
- **Portable pack must copy.** `def-sop` / `def-ref`, frontmatter rules, progressive disclosure, stdlib scripts (from `skill-authoring.mdc`).
- **Portable pack may relax.** Dual-tree mirror, `eliotapp` import rule (value already excepts package-local `_session`), value-only KB key asserts in tests.
- **lean-mvp proof.** Sibling skill is hand-copyable; only `import_value_context` / `value-bridge-map` couple to value. Compiler treats cross-skill bridges as optional add-ons, not core.

## Alternatives

1. **Agent-only meta-skill.** Paste doc, agent writes skill by hand each time. Rejected. No lever; quality drifts.
2. **Fully automatic compiler.** Doc → ship skill with no human gate. Rejected. Atom pacing and soft/hard labels need judgment; value's corrections prove this.
3. **Hybrid lever (chosen).** Deterministic extract + portable session template + poteto-mode curriculum pass + golden fixture + human ship gate. Matches how value actually got good.

## Applicable skills

- `/poteto-mode` (this runbook's outer shell)
- Cursor built-in `create-skill` when writing `SKILL.md`
- `how` before editing the session runtime
- `interrogate` before promoting the IR schema or express-spine rules
- `unslop` on all agent-facing prose
- `/deslop` before commit
- `show-me-your-work` for the decision trail across phases
- `babysit` after the PR that ships the pack

## Phases

0. **Start here if you are human:** [TUTORIAL.md](./TUTORIAL.md) (plain-language how to run this, today vs later).
1. [phase-1-ir-and-fixture.md](./phase-1-ir-and-fixture.md). Input IR + golden fixture contract.
2. [phase-2-extract-scaffold.md](./phase-2-extract-scaffold.md). Mechanical extractor CLI.
3. [phase-3-portable-session-runtime.md](./phase-3-portable-session-runtime.md). Curriculum-agnostic `_session` template.
4. [phase-4-poteto-runbook.md](./phase-4-poteto-runbook.md). `FOR_AGENTS.md` + meta-skill that calls poteto-mode.
5. [phase-5-atom-dag-lever.md](./phase-5-atom-dag-lever.md). Atom synthesis protocol + DAG coverage simulator.
6. [phase-6-standalone-bootstrap.md](./phase-6-standalone-bootstrap.md). Empty-repo install path.
7. [phase-7-verify-and-ship.md](./phase-7-verify-and-ship.md). Pressure tests + promote gate.

See also [testing.md](./testing.md).

## Verification (project-level)

```powershell
# From pack root or host repo after install
python -m unittest discover -s tests -p "test_prompt_suite_*.py" -v
python tools/prompt-suite-compile/compile.py --fixture value --check
```

Runtime surface is CLI (`control-cli`) for extractor and session scripts. Agent surface is Cursor chat following `FOR_AGENTS.md` (no browser control skill required).

## Implementation guidance

Implementer must apply

- **how** on the value `_session` package before peeling it.
- **interrogate** on IR schema and “what is soft vs hard” rules before locking them.
- **build-the-lever**. Every phase ends in a rerunnable script or check, not hand-edited trees.
- **laziness-protocol**. Do not invent a second session engine; peel and parameterize.
- **encode-lessons-in-structure**. Golden fixture + DAG sim replace tribal memory.
- **prove-it-works**. Fixture `--check` and curriculum sim before claiming done.
- **/deslop** and **unslop** before commit; **babysit** after PR.
- **show-me-your-work** decision trail for soft/hard and express-spine choices.
- **create-skill** when authoring the meta-skill `SKILL.md`.

Do not implement from this plan until the user says so.

## Principles that shaped this plan

- **Build the Lever.** Chose a compiler + runbook over repeating the lean-mvp hand port.
- **Laziness Protocol.** Reuse value's session scripts as a template instead of a new framework.
- **Foundational Thinking.** IR and session schema before agent prose.
- **Exhaust the Design Space.** Three alternatives; hybrid wins.
- **Sequence into Verifiable Units.** Small phases each ending in a check.
- **Encode Lessons in Structure.** Value golden fixture encodes the hard-won recipe.
- **Never Block on the Human.** Plan recommends hybrid and fixture location without waiting; one open preference left for pack home.
- **Guard the Context Window.** Portability facts gathered via [Explore skill portability](5ccc5437-84e9-4782-90ed-ac25f1642437); constraints above absorb that return.
