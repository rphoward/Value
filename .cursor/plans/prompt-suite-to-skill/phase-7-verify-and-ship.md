# Phase 7. Verify and ship

Back-link: [overview.md](./overview.md)

## Goal

Close the loop with pressure-test templates and a promote gate so draft skills do not silently become ship surface.

## Changes

- Add `tools/prompt-suite-compile/templates/pressure-tests.md` patterned on `docs/value-skill-pressure-tests.md` (missing session, one-question pacing, no invent, resume, gate).
- Add `promote.py` that copies `tools/drafts/skills/<slug>/` → `.cursor/skills/<slug>/` (and optional `skills/<slug>/`) only when audit_dag + package mirror checks pass.
- Fixture `--check` for value. mechanical extract of KB must match `skills/value/assets/knowledge-base.json` within documented tolerances; atom digests are **not** required to match (judgment layer).

## Data structures

- Promote report. checks passed, paths written, fences hit.

## Verification

**Static.** Promote refuses when audit fails.

**Runtime.** Promote of a known-good draft succeeds; promote of a draft missing a gate atom fails closed.
