---
name: Value skill user voice pass
overview: Separate operator telemetry from user-facing coach voice. Scripts stay JSON-first; orchestrator re-voices questions with known→unknown continuity. No Bloom metadata.
todos:
  - id: scripts-quiet
    content: "Add status.py --brief and --operator; default brief for agents. Trim next_question JSON to agent-only fields (drop embedded ledger duplication if redundant)."
    status: pending
  - id: slug-silent
    content: "Missing-session asks name only; derive slug in init_session or orchestrator before init_session.py --slug ..."
    status: pending
  - id: skill-voice
    content: "Rewrite SKILL.md protocol-1/3/6 and central_idea — scripts run silently; forbid quoting stdout; voice recipe known→edge→question"
    status: pending
  - id: contract-voice
    content: "Update session-contract.md missing-session + surface rules; optional voice-hint in profile.md for P01-P03 as pilot"
    status: pending
  - id: tests-mirror
    content: "Update smoke tests for --brief/--operator; sync .cursor/skills/value and skills/value; push Value + Values"
    status: pending
isProject: false
---

# Handoff: user voice + quiet scripts (fresh session)

## Why this exists

Prior session shipped **DAG pacing**, **section gap-fill**, and **express `pacing_mode`**. User feedback in the same arc: live turns feel like a **dashboard** (ledger, section strip, atom IDs every turn) and **mechanical** copy pasted from `atoms.json` `asks`. Python stdout telemetry does not help the model — it already gets JSON from `next_question.py`. Quoting script output to the user adds noise only.

User explicitly **declined Bloom taxonomy** in atoms/schema. They noticed learning hierarchy organically; want **Panksepp-shaped curiosity** in orchestrator voice only (known pocket → edge of unknown → one question), not labels or extra metadata.

## Already shipped (do not redo)

| Commit | Repo | What |
|--------|------|------|
| `58a3c45` | [Value](https://github.com/rphoward/Value) | DAG scheduler, requires/section/soft, gaps/accept_bulk/map_gaps, section strip, draft-map protocol |
| `9208d67` | Value | express pacing_mode, set_pacing_mode.py, init --pacing-mode |
| `0a67a6d` / `47fd193` | [Values](https://github.com/rphoward/Values) | Mirrors of above |

**Tests:** `python -m unittest discover -s tests -p "test_value*.py"` — 55 passed at last run.

**Dual tree rule:** every skill change in **both** `.cursor/skills/value/` and `skills/value/`, then sync to `c:\Projects\Values\skills\value\` before Values push.

**Untracked locally:** `workproduct/value-proposition/value-design/` (live session at P08 gains) — do not commit unless user asks.

## Root cause (confirmed)

1. **SKILL.md protocol-3** requires ledger line + section strip + orientation + question every turn (`central_idea` says "surfaces ledger and section strip each turn").
2. **session-contract.md** missing-session asks **slug and display name** → users hear "plug"; slug is filesystem detail.
3. **`format_status_line`** in `_session.py` prints operator telemetry (`Ledger: phase=… atom=P08 … bombs=…`).
4. **`next_question.py`** returns JSON the model often reads aloud; `asks` is a **contract anchor**, not finished prose.
5. Tension with **protocol-0 `avoid-cognitive-murder`** — unfixed.

## Target architecture

```text
Python (operator)          Orchestrator (user)
─────────────────          ───────────────────
session.json               one connected paragraph
next_question.json         known → edge → question
status --brief (resume)    canvas section names only
status --operator (debug)  never atom IDs / ledger keys
accept_answer, gaps, …     teach on tap; express = shorter bridge
```

## Voice recipe (orchestrator only — put in SKILL.md)

One turn, one paragraph, one primary question:

1. **Known** — phrase from last accepted answer or section strip semantics ("Segment locked: …").
2. **Edge** — what is missing now and why it matters for the next design move (curiosity, not taxonomy jargon).
3. **Question** — rephrase `asks` from `next_question.py`; do not paste JSON or `accepts_summary` unless user asks what counts as an answer.

**Forbidden user-facing:** `Ledger:`, `atom=`, `P08`, `bombs=`, `ready_count`, `focus_atom`, slug/path unless debugging.

**When to show progress strip:** resume, user asks "where am I?", or after a module gate — not every turn.

**Express pacing:** skip warm bridge; still one human question.

## Script changes (concrete)

### `status.py`

- `--brief` (default for agent docs): human one-liner, e.g. `Customer profile · Jobs in progress · question: gains`
- `--operator`: current `format_status_line` (keep for tests/debug)
- `--sections`: unchanged; orchestrator uses on resume only

Implement `format_brief_status(session, atoms)` in `_session.py` using `section_status` + module phase — no atom IDs.

### `next_question.py`

- Keep JSON stdout for agent parsing.
- Consider removing duplicate `ledger` blob from payload if agent can run `status --operator` when needed (optional trim).
- Document in session-contract: **JSON is agent-internal; never echo to user.**

### `init_session.py`

- Accept `--name` required; `--slug` optional (derive from name: lowercase, hyphenate, strip unsafe chars per `SLUG_RE`).
- SKILL + contract: first turn = "What are you working on?" + consent in plain English.

### References (pilot, optional)

Add `(voice-hint "…")` to 2–3 profile atoms (P01, P03, P08) — one line curiosity angle for orchestrator, not user-visible metadata in JSON.

## Files to touch

| Path | Change |
|------|--------|
| `.cursor/skills/value/scripts/_session.py` | `format_brief_status`, slug derive helper |
| `.cursor/skills/value/scripts/status.py` | `--brief` / `--operator` |
| `.cursor/skills/value/scripts/init_session.py` | optional slug derive |
| `.cursor/skills/value/SKILL.md` | central_idea, protocol-1/3/6, voice recipe |
| `.cursor/skills/value/references/session-contract.md` | missing-session, surface rules |
| `.cursor/skills/value/references/profile.md` | optional voice-hint pilot |
| `tests/test_value_skill_package.py` | `--operator` in smoke; brief format test |
| `skills/value/**` | mirror |
| `docs/value-skill-pressure-tests.md` | note user-voice expectation for Scenario A |

## Verification

```powershell
cd c:\Projects\value
python -m unittest discover -s tests -p "test_value*.py" -v
python .cursor/skills/value/scripts/status.py workproduct/.../session.json --brief
python .cursor/skills/value/scripts/next_question.py workproduct/.../session.json
```

Manual: fresh agent turn with skill loaded — no ledger line, no slug question, question reads as connected prose.

## Explicitly out of scope

- Bloom levels in atoms.json or scheduler
- UI / canvas app
- Changing DAG or express spine logic (voice only layers on top)
- Committing `workproduct/` sessions

## Open choice for implementer

**Default `status.py` when no flag:** recommend `--brief` as default so agents that run bare `status.py` get human output; tests switch to `--operator`. Alternative: default stays operator, SKILL mandates `--brief` only — easier test diff, easier for agents to slip.

Recommend **default brief, explicit --operator** — matches "quiet by default."

## Related docs

- Prior plan (done): `.cursor/plans/value_skill_dag_pacing_f9ed875e.plan.md`
- Design spec: `docs/superpowers/specs/2026-07-18-value-skill-design.md`
- Pressure tests: `docs/value-skill-pressure-tests.md`

## Fresh session starter prompt

```text
Implement .cursor/plans/value_skill_user_voice_fresh.plan.md — quiet scripts (status --brief/--operator), name-first session creation with derived slug, SKILL voice recipe (known→edge→question, no telemetry to user). Sync both skill trees, run tests, commit and push Value + Values unless I say otherwise.
```
