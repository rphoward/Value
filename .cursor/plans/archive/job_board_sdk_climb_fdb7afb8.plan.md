---
name: Job board SDK climb
overview: "Resume-safe discrimination job board + thin Cursor SDK driver of existing protocol-2, so full-pipeline can finish with scores.json without chat memory. Phased plan: .cursor/plans/archive/job_board_sdk_climb/"
todos:
  - id: phase-1-job-board-types
    content: "Phase 1: DiscriminationJob schema + job_board.py + tests (no CLI yet)"
    status: completed
  - id: phase-2-job-cli
    content: "Phase 2: hillclimb_once job-* subcommands + CLI tests"
    status: completed
  - id: phase-3-resume-protocol
    content: "Phase 3: workflow SKILL / one-command / hillclimb.md job-status-first resume + seed-suffix jobs"
    status: completed
  - id: phase-4-sdk-spike
    content: "Phase 4: SDK spike A/B/C; handoff/SDK-CLIMB-SPIKE.md; defer cancels phase 5"
    status: completed
  - id: phase-5-sdk-driver
    content: "Phase 5: tools/sdk-climb.py + --init-if-missing + exit codes 0|1|2|3 (blocked on spike A/B)"
    status: cancelled
  - id: phase-6-pipeline-seam
    content: "Phase 6: pipeline skill + catalog + wizard copy + ADR 001 + STATE.md (or /hillclimb-only if deferred)"
    status: completed
isProject: false
---

# Job board + SDK climb driver

**Canonical phased plan:** [`.cursor/plans/archive/job_board_sdk_climb/overview.md`](job_board_sdk_climb/overview.md)

This file is the Cursor plan stub. Implementation detail lives in the directory above.

## Intent (corrected)

Bring the automation pipeline closer to SOTA **inside the Cursor harness** by closing two gaps:

1. **Mid-batch resume** for discrimination (the real crash hole).
2. **Unattended entry** that drives the loop we already have (not a Python reimplementation of draft/eval/discriminate).

## Locked defaults

- CLI-first. No wizard Start Climb button this spike.
- Job board covers discrimination batches only. Iteration resume stays `hillclimb_once.py status`.
- Seed-round resume (`v1a`/`v1b`/`v1c`) is part of the shared protocol (phase 3).
- SDK runtime is spike-gated (phase 4 options A/B/C). Defer driver if no parity.
- Driver (if not deferred) uses exit codes `0|1|2|3` and may `--init-if-missing`.
- Live full climbs are manual/cost-gated. CI tests job board + preflight only.

## Phases

See [overview.md](job_board_sdk_climb/overview.md). Ship 1→6 in order. Phase 5 is blocked on phase 4 go (A or B); cancelled on C.
