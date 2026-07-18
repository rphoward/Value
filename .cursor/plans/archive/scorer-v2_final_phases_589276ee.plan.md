---
name: scorer-v2 final phases
overview: "Finish scorer v2 in five session-sized phases (corpus, AUTHORPRINT, discrimination, gate, smoke). Split plan lives in scorer-v2-final-phases/."
todos:
  - id: phase-1
    content: "Phase 1: corpus widen — corpus-fetch subagent, margins.json, fixture migration"
    status: completed
  - id: phase-2
    content: "Phase 2: AUTHORPRINT 0-100 diagnostic wire + authorprint_v2.py + tests"
    status: completed
  - id: phase-3
    content: "Phase 3: discrimination.py + discriminate.md + discrimination_v2.py + tests"
    status: completed
  - id: phase-4
    content: "Phase 4: gate_v2.py harness + ranking unit tests (fixture dry-run only)"
    status: completed
  - id: phase-5
    content: "Phase 5: live judge smoke, gate ACCEPT, SCORER-V2-PASSED.md or findings.md"
    status: completed
isProject: false
---

# Scorer v2 — final phases (pointer)

**This plan was split for ~200k context limits.** One chat per phase.

## Start here

Read [overview.md](scorer-v2-final-phases/overview.md), then open the phase file for your session:

| Session | File |
|---------|------|
| 1 — Corpus | [phase-1-corpus.md](scorer-v2-final-phases/phase-1-corpus.md) |
| 2 — AUTHORPRINT | [phase-2-authorprint.md](scorer-v2-final-phases/phase-2-authorprint.md) |
| 3 — Discrimination | [phase-3-discrimination.md](scorer-v2-final-phases/phase-3-discrimination.md) |
| 4 — Gate harness | [phase-4-gate.md](scorer-v2-final-phases/phase-4-gate.md) |
| 5 — Smoke + ship | [phase-5-smoke.md](scorer-v2-final-phases/phase-5-smoke.md) |

Shared dispatch prompts and artifact tree: [shared.md](scorer-v2-final-phases/shared.md).

Each phase file has a **paste into new chat** block. Run phases in order; verify green before advancing.
