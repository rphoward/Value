# Job board doc fix — plan

Back-link: shipped code in [job_board_sdk_climb/](../job_board_sdk_climb/) (phases 1–3 done; phase 5 cancelled).

## Problem

Job board + `job-*` CLI shipped and tests green (`31 passed`). Final review **REVISE** because protocol docs still disagree on the discrimination path. A parent following **New-run sequence** in `one-command.md` can skip the job board and lose mid-batch resume.

Secondary: skill `references/` were written as markdown prose. Repo convention (`skill-authoring.mdc` protocol-3b) wants `def-ref` pseudo-Lisp for machine-programmed surfaces. `conduct.mdc` only asserts skill-authoring on `SKILL.md`, not `references/` or `.cursor/commands/`.

## Scope

**In**

1. Align all workflow discrimination protocol text to `job-open` → `job-trial` → `job-score` → `job-record`.
2. Convert `one-command.md` and `playbook.md` bodies from markdown prose to `def-ref` (keep scoreboard/results templates as artifacts if needed).
3. Tighten rule globs so `references/` and commands get the same authoring gate as `SKILL.md`.
4. Re-run final-review checklist; update `handoff/STATE.md` gate when docs pass.

**Out**

- No Python changes unless a doc fix reveals a real CLI bug.
- No `sdk-climb.py` (spike C stands).
- No wholesale rewrite of human handoff prose (`handoff/*.md` except this gate note).
- No commit in this plan-only session.

## Phases

### Phase 1 — Unblock final review (surgical)

| File | Line / section | Change |
|------|----------------|--------|
| `.cursor/skills/workflow/references/one-command.md` | 136 | Replace `discriminate … → record-discrimination` with same `job-*` chain as lines 109–113 |
| `.cursor/skills/workflow/references/one-command.md` | 12 | `indist` / `Δind` from `job-record` (wraps `record_discrimination`), not legacy subcommand name |
| `.cursor/commands/hillclimb.md` | 33 | "skip `job-record` after spot trials" (not `record-discrimination`) |

**Verify:** `rg 'record-discrimination' .cursor/skills/workflow .cursor/commands` — only allowed in "legacy" notes or CLI help text, not as the happy path.

### Phase 2 — Grep contract (no contradictions)

Run and fix any remaining drift:

```powershell
rg "record-discrimination|discrimination_v2\.py prepare" .cursor/skills/workflow .cursor/commands
rg "job-open|job-record|job-status" .cursor/skills/workflow .cursor/commands
```

Expected after phase 1:

- New-run, subagent loop, resume checklist, SKILL step-4, playbook parent sequence all name the same four `job-*` steps.
- `record-discrimination` appears only as legacy alias (playbook frozen harness) or in `hillclimb_once.py` subcommand list.

### Phase 3 — Pseudo-Lisp conversion (references)

Per `skill-authoring.mdc` protocol-3b:

| File | Current | Target |
|------|---------|--------|
| `references/one-command.md` | `def-ref` header + markdown sections | Full `def-ref` with `(scoreboard-line …)`, `(new-run-sequence …)`, `(resume-order …)`; move literal templates to `one-command-artifacts.md` tail or fenced artifact block |
| `references/playbook.md` | `def-ref` header + markdown body | Convert Role, Metric, Frozen harness, Loop discipline to `def-ref` forms; link from SKILL unchanged |

**Do not** convert human handoff (`handoff/STATE.md`, `SDK-CLIMB-SPIKE.md`) — those stay markdown.

### Phase 4 — Rule globs (prevent recurrence)

| File | Change |
|------|--------|
| `.cursor/rules/conduct.mdc` protocol-4 | Widen `(when (editing …))` from `SKILL.md` only to `.cursor/skills/**` and `.cursor/commands/**` for skill-authoring assertion |
| `.cursor/rules/skill-authoring.mdc` protocol-3 | Remove or narrow `"imperative markdown OK when no protocols"` — references must be `def-ref` or artifacts per 3b |
| Optional | Add `.cursor/commands/**` to `skill-authoring.mdc` globs if commands are treated as skill edges |

### Phase 5 — Gate + handoff close

1. `pytest tests/test_job_board.py tests/test_hillclimb.py -q` — still green (no code change expected).
2. Manual dry-read: new-run step 4 matches subagent loop step 4.
3. Update `handoff/STATE.md` — move "doc fix" from open to shipped, or add sub-bullet under job-board gate.
4. Final review axes 2 and 7 should PASS.

## Verification matrix

| Check | Pass |
|-------|------|
| `one-command.md:136` uses `job-*` | |
| `rg record-discrimination` — no happy-path hits in workflow/commands docs | |
| `one-command.md` / `playbook.md` are `def-ref` not prose blobs | |
| `conduct.mdc` covers `references/` edits | |
| `31 passed` pytest | |

## Locked facts (do not change)

- `result_path` = `discrimination-score-vN.json`; attach sidecar = `discrimination-vN.json` via `job-record`.
- SDK driver deferred; canonical entry = `/hillclimb`.
- `record-discrimination` CLI remains for backward compatibility; not the documented parent path.
