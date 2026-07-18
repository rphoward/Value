# Job board + SDK climb — overview

**For.** Operators who want full-pipeline to finish with `scores.json` without babysitting chat memory. Maintainers who inherit a resume-safe discrimination contract and a thin unattended driver.

**Why now.** The climb loop is good enough to optimize. The remaining SOTA gap inside the Cursor harness is not a better scorer. It is unattended, crash-safe orchestration of the loop we already have.

## Context

Today `/hillclimb` works in chat. Discrimination is parent-orchestrated with ad-hoc `trials-vN.json` / `verdicts-vN.json` and **no mid-batch job file**. If the session dies mid-batch, `hillclimb_once.py status` only sees `scores.json` (iteration may lack `indistinguishability`). The web wizard stops at `prepare` and never calls `init`, so `scores.json` does not exist after prepare. Pipeline skill step-4 documents the loop but nothing invokes it unattended. `STATE.md` already lists hooks + automation as the next deliverable. Architecture says automation drives the existing loop; logic stays in skills.

## Scope

**In**

1. Filesystem discrimination job board (`discrimination-job-v{n}.json`) + `job-*` CLI on `hillclimb_once.py`.
2. Resume-safe parent protocol (chat `/hillclimb` and future driver share one order).
3. Thin Cursor SDK driver (`tools/sdk-climb.py`) that runs protocol-7 / protocol-2 via the runtime the spike chooses (local multi-turn or cloud). Does **not** reimplement draft, eval, or discriminate in Python. Deferred entirely if spike chooses option C.
4. Pipeline / catalog / wizard copy / ADR 001 / `STATE.md` seam so full-pipeline completion names the driver.
5. Optional `--init-if-missing` on the driver when `source.txt` + `style-block.md` exist but `scores.json` does not (closes the wizard prepare gap without a Start Climb button).

**Out (this spike)**

- Wizard Start Climb button / server-side Task API
- Weakness-mining / ACE playbook curator / Self-Harness / Meta-Harness
- Changing climb metric, scorer, or default `discrimination_n`
- Auto held-out Exa fetch inside the Python driver (stays agent/protocol-7)
- Cloud automation schedule (driver is the lever; cloud schedule is a later phase)
- Replacing chat `/hillclimb` (driver is a second entry, same protocol)

## Constraints

- Product code stays under `src/eliotwf/`; skill support under `src/eliotwf_skills/`; orchestration entrypoints under `tools/`.
- `cursor-sdk` is an optional/runtime dep for the driver only. Never import it from web layers.
- `CURSOR_API_KEY` required for live driver runs. Never hardcode.
- Discrimination scoring path stays `discrimination_v2.py` + `record_discrimination`. Job board wraps progress; it does not invent a second scorer.
- Live full climbs are manual/cost-gated. CI tests preflight + job board only.
- SDK runtime is **spike-gated** (phase 4). Do not assume local `Agent.prompt()` has IDE Task/subagent parity. If the spike finds no parity, defer the driver (option C) and keep `/hillclimb` canonical; still ship the job board.
- Driver exit codes are fixed as `0|1|2|3` (see phase 5). Seed-round resume is part of the shared protocol (see phase 3).

## Alternatives

| Approach | Verdict |
|----------|---------|
| **A. Job board + thin local SDK driver** (chosen) | Matches ARCHITECTURE ("automation drives existing loop"). Smallest change that closes resume + unattended gaps. |
| **B. Reimplement protocol-2 in Python** | Rejected. Duplicates agent work; fights skill/subagent design; high reader load. |
| **C. Cloud-only automation first** | Deferred. Cloud is better for fire-and-forget later; local proves the prompt + job board against the working tree first. |
| **D. Wizard Start Climb only** | Rejected for this spike. UI without a resume-safe board still loses mid-batch; CLI-first is the lever. |

## Applicable skills

- `poteto-mode` / multi-phase plan (this document)
- `how` before touching unfamiliar SDK or discrimination CLI surfaces
- `control-cli` for job-* and `sdk-climb.py` runtime checks
- Cursor built-in `create-skill` when editing workflow/pipeline `SKILL.md`
- `unslop` on all prose surfaces (skills, handoff, ADR)
- `/deslop` before commit; `babysit` after PR
- `show-me-your-work` if the spike runs across sessions
- `interrogate` only if the SDK spike surfaces a contested runtime choice (local vs cloud)

## Phases

1. [phase-1-job-board-types.md](phase-1-job-board-types.md) — schema + module API
2. [phase-2-job-cli.md](phase-2-job-cli.md) — `job-*` subcommands on `hillclimb_once.py`
3. [phase-3-resume-protocol.md](phase-3-resume-protocol.md) — skill/command resume order
4. [phase-4-sdk-spike.md](phase-4-sdk-spike.md) — prove local agent can run one discriminate Task
5. [phase-5-sdk-driver.md](phase-5-sdk-driver.md) — `tools/sdk-climb.py` + preflight tests
6. [phase-6-pipeline-seam.md](phase-6-pipeline-seam.md) — pipeline/catalog/wizard/ADR/STATE
7. [testing.md](testing.md) — project-level verification matrix

## Verification (project-level)

```powershell
$env:PYTHONPATH="src"
python -m pytest tests/test_job_board.py tests/test_hillclimb.py tests/test_sdk_climb_preflight.py -q
```

Manual gates in [testing.md](testing.md). Do not claim unattended climb works until a prepared slug shows `job-status` progress across an intentional interrupt.

## Implementation guidance

- Run **how** on `discrimination_v2.py` and Cursor Python SDK before coding phases 1 and 4.
- Name the data shape (`DiscriminationJob`) before any CLI or driver code (**foundational-thinking**).
- Prefer idempotent `job-trial` / `job-score` (**make-operations-idempotent**).
- Keep the driver a prompt assembler + exit-code checker (**laziness-protocol**, **build-the-lever**).
- Ship phases in order; each ends with its own check (**sequence-verifiable-units**).
- `/deslop` each diff; **unslop** skill/docs prose; **babysit** after PR.
- Decision trail via **show-me-your-work** if implementation spans more than one session.
