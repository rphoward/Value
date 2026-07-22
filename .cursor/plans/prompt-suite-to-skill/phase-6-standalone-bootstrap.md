# Phase 6. Standalone bootstrap

Back-link: [overview.md](./overview.md)

## Goal

Prove the pack works outside this monorepo. One empty folder, one sample doc, pstack, poteto-mode, compiled skill.

## Changes

- Add `tools/prompt-suite-compile/bootstrap.md` with copy-paste steps for a foreign repo.
- Merge snippet for `.cursor/settings.json` enabling pstack (same pattern as Benny, no Slack).
- Document dual-tree policy as optional. host may use only `.cursor/skills/<slug>/` until they want an `skills/` ship surface.
- Fence. never overwrite an existing skill directory without `--force` and explicit consent line in the runbook.

## Data structures

- Bootstrap checklist (markdown). source doc path, slug, out dir, pstack enable, poteto invocation phrase.

## Verification

**Static.** Bootstrap doc links to FOR_AGENTS and compile CLI.

**Runtime.** Manual or scripted smoke in a temp directory. copy pack → scaffold from lean playbook fixture → init session → next_question returns first atom. Prefer a small PowerShell/posix smoke script under `tools/prompt-suite-compile/smoke-standalone.ps1`.
