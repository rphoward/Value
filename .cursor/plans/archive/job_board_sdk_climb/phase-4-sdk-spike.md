# Phase 4 — SDK capability spike

Back-link: [overview.md](overview.md)

## Goal

Prove how an unattended driver invokes the same isolated workers as IDE `/hillclimb` (`emulate-drafter`, `eval-audit`, `discriminate`). Do not build the full driver until this gate passes. Prefer a one-trial `discriminate` probe first; expand only if that path works.

## Known constraint (verify, do not assume)

Cursor SDK advanced docs have stated that `agents:` custom sub-agents are **cloud-only at v1** and that a local executor may silently drop them. IDE Task tool is not available to a bare `Agent.prompt()` one-shot. Python SDK docs also claim project `.cursor/agents/*.md` pickup and nested subagents. **The spike settles which claim is true for this repo.** Do not ship `sdk-climb.py` until the handoff note documents the chosen path.

## Changes

- Add a disposable probe under `tools/drafts/` (prefer drafts until the gate passes).
- Document findings in `handoff/SDK-CLIMB-SPIKE.md`.

**Spike options (pick one path; document in handoff)**

| Option | When to choose | Risk |
|--------|----------------|------|
| **A. Cloud agent + `customSubagents` / project agents** | Unattended CI / no local IDE | Needs cloud runtime, repo clone, cost |
| **B. Local `Agent.create` + `send` / `resume` multi-turn** | Single machine, API key only | One agent must follow protocol-2; may inline work unless Task/subagent parity exists |
| **C. Defer SDK driver** | Spike shows no parity | Ship job board only; chat `/hillclimb` stays canonical |

**Spike acceptance**

One recorded iteration on a prepared fixture slug (`source.txt` + `style-block.md` + `scores.json` from init), with evidence that emulate/eval/discriminate ran as isolated workers (cloud subagents or documented equivalent). Minimum bar for a go on phase 5 is at least one real `discriminate` verdict via the chosen runtime, plus a written path for emulate/eval.

**Defer rule.** If spike fails option A and B, **cancel phase 5 (sdk-driver)** and update pipeline docs (phase 6) to point at `/hillclimb` only. Job board phases 1–3 still ship.

## Data structures

Spike prompt is a string. No new run artifacts required beyond reading an existing `trials-vN.json` (and writing the handoff note).

## Verification

**Static.** Spike script imports `cursor_sdk` only when `CURSOR_API_KEY` is set; otherwise exits with a clear preflight message.

**Runtime.** Live call(s) per chosen option. Record evidence in `handoff/SDK-CLIMB-SPIKE.md` (runtime chosen, whether `.cursor/agents/discriminate.md` loaded, `setting_sources` needs, nesting/Task behavior, cost/wall time). Use `control-cli` for the probe invocation.

**Stop rule.** No phase 5 until handoff says go (A or B) or explicitly chooses C (defer driver).
