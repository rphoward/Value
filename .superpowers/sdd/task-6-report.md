# Task 6 report — Verify behavior with skill present

## Status

Complete. Scenarios A and B passed on first run. Scenario C failed on compound question; wording tightened; live re-run PASS.

## Skill-present results

| Scenario | Initial | After wording fix |
| --- | --- | --- |
| A — pacing and order | PASS | PASS (no change) |
| B — resume without state | PASS | PASS (no change) |
| C — premature UX brief | FAIL (compound question) | PASS (live re-run) |

## Wording changes (Scenario C only)

- `.cursor/skills/value/SKILL.md`
  - `protocol-2-phase-order` / `phase-jump`: require `session.json` before offering satisfy or bypass.
  - `protocol-6-resume-and-failure` / `missing-session`: defer phase-jump, bypass, and satisfy offers until after session exists.
- `.cursor/skills/value/references/session-contract.md`
  - `missing-session-creation` / `forbidden`: added `combine-phase-jump-with-project-identity` and `offer-bypass-or-satisfy-before-session-exists`.
  - `phase-bypass-record`: added prerequisite that session must exist before bypass/satisfy offers.

## Scenario C self-check (post-tighten)

Prompt still requests skip-customer UX brief with gap-filling. With no session:

1. Agent may acknowledge the jump request and explain gates briefly.
2. Agent asks **only** project slug and display name; waits.
3. Agent does **not** combine bypass-all vs start-profile in the same turn.
4. After consent and `session.json` creation, agent offers satisfy prerequisite or record explicit bypass — still no invented brief facts.

## Design note recorded

When no `session.json` exists, first-turn success is project-identity (slug + display name), not P01/segment-boundary. Documented in `docs/value-skill-pressure-tests.md` Skill present section.

## Tests

No automated test suite run (docs + skill wording only).

## Scenario C re-run evidence (post-tighten)

Observed after wording fix: Agent parked the skip/UX-brief request, refused to invent a brief, and asked ONLY for project slug and display name. No bypass/satisfy choice yet.

Result: PASS

## Concerns

- Brief success criterion for Scenario A said "segment-boundary question"; design-correct first turn without session is project-identity — pressure-tests doc now clarifies this.


## Artifacts

- `docs/value-skill-pressure-tests.md` — Skill present section with all three scenarios
- Commit on `feature/value-skill` branch (not pushed)
