# Phase 4. Poteto runbook and meta-skill

Back-link: [overview.md](./overview.md)

## Goal

Give a human a single entry point. Point Cursor at a pack file, name the source doc and slug, and have the agent run poteto-mode through a fixed recipe instead of improvising.

## Changes

- Add pack root `tools/prompt-suite-compile/FOR_AGENTS.md` (Benny-style entry, no Slack). Steps. enable pstack if needed → parse/scaffold via CLI → poteto Feature/authoring phases for atoms and SKILL.md → DAG sim → pressure scenarios → promote draft to `.cursor/skills/<slug>/` only after consent.
- Add meta-skill `.cursor/skills/scripted-skill-from-doc/SKILL.md` (create-skill) whose only job is. load FOR_AGENTS, require `/poteto-mode`, refuse to edit golden fixtures, call compile CLI for mechanical steps.
- Pack README. “Fresh repo. copy pack, drop doc, open FOR_AGENTS, say the slug.”

## Data structures

- Runbook checklist items as ordered protocols in FOR_AGENTS (not free prose).
- Meta-skill frontmatter triggers. “compile a prompt suite”, “scripted skill from doc”, “make a skill like value”.

## Verification

**Static.** Meta-skill frontmatter valid; FOR_AGENTS paths resolve; create-skill checklist items present.

**Runtime.** Dry-run. agent reads FOR_AGENTS and stops at first human gate after scaffold (documented expected stop). No need for full live curriculum in this phase.
