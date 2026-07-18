# Phase 00 — Root hygiene

Back-link: [overview.md](overview.md)

## Goal

Remove accidental Eliot-named roots and scrub agent-facing prose that still teaches old homes, so the intentional map is obvious: `eliotapp/` + `workproduct/` + reference `eliotworkflow/`.

## Changes

- Remove git index entry for orphan `EliotWF/` (mode `160000`, no `.gitmodules`). Delete the nested working tree from disk only after the human confirms nothing needed is trapped there (see open question in overview).
- Delete `eliotwf.egg-info/` and `src/eliotwf.egg-info/` residue.
- Scrub `.cursor/skills/**` (and similar agent-facing prose) that still cite `src/eliotwf_skills` as an import home. Point at `eliotapp`.
- Keep `eliotworkflow/` as reference markdown. Do not treat it as a product home.

## Data structures

None. This phase deletes residue and updates prose; it does not introduce types.

## Verification

**Static.** `git ls-files -s EliotWF` empty. No `*egg-info*` at repo root or under `src/`. Grep for `src/eliotwf_skills` in `.cursor/skills` is clean or only historical. `pytest` still green.

**Runtime.** None required beyond confirming the working tree still imports `eliotapp` if packaging metadata was touched.
