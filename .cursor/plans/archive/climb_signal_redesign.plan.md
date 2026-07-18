---
name: Climb-signal redesign
overview: "Replace sole qualitative-mean climb accept with pairwise candidate-vs-best (style-block as constitution), excerpt/axis-local revise, hard Python + content-brief vetoes, gaming-visible Canvas, crossover as optional splice. Shipped phases 00–10 on feature/climb-signal-redesign."
todos:
  - id: phase-00-harness
    content: "Gaming regression fixture: mean can rise while pairwise-vs-best rejects (red first)"
    status: completed
  - id: phase-01-accept-types
    content: "Domain types for AcceptDecision, PatchScope, hard veto; no mean-as-ruler in new path"
    status: completed
  - id: phase-02-hard-veto
    content: "Wire SURFACE/PROSODY/CAST floors + content-brief as climb veto (CLI/SDK only)"
    status: completed
  - id: phase-03-pairwise-accept
    content: "Candidate vs current-best pairwise accept via preference job spine; qualitative → diagnostic"
    status: completed
  - id: phase-04-retire-mean-ruler
    content: "Migrate best/seed/stop off sole qualitative mean in one wave; ADR supersedes 003 default"
    status: completed
  - id: phase-05-revise-unit
    content: "Excerpt- and/or axis-local craft brief + revise-drafter contract"
    status: completed
  - id: phase-06-epsilon-band
    content: "Multi-objective accept: target ↑, non-target axes within ε"
    status: completed
  - id: phase-07-canvas-gaming-ux
    content: "Read-only Canvas: patch scope, accept reason, pairwise keep-best; HTTP still never writes scores"
    status: completed
  - id: phase-08-held-out-anticheat
    content: "Periodic prefer-vs-held-out genuine as optional anti-cheat under same accept rule"
    status: completed
  - id: phase-09-crossover
    content: "Optional span-splice operator under same pairwise accept (not a new scalar)"
    status: completed
  - id: phase-10-closeout
    content: "CONTEXT/ADR/STATE; dogfood one run; decision trail; archive when green"
    status: completed
isProject: false
---

# Climb-signal redesign

**PASS on branch `feature/climb-signal-redesign` (2026-07-17).** Gate: `handoff/CLIMB-SIGNAL-REDESIGN-PASSED.md`. Merge pending.

Sources: `handoff/CLIMB-SIGNAL-REDESIGN-HANDOFF.md`, `handoff/CLIMB-SIGNAL-RESEARCH-2026-07.md`, Exa refresh (July 2026 writing-RL / OpenRS / LitBench / rubric hacking), codebase explorers on accept / preference / revise / Canvas.

Phase detail: [climb_signal_redesign/](climb_signal_redesign/overview.md).

## Scope

**In:** pairwise candidate-vs-best accept; hard veto floors; excerpt/axis-local revise; ε-band; gaming-visible Canvas (read-only); held-out anti-cheat; crossover splice; ADR/vocab; prove-it harness; CLI/SDK scores ownership preserved.

**Out:** lab-scale writing RM training; co-evolving rubric generator as MVP; reweight qualitative axes as the fix; HTTP `scores.json` writers; reopen eliotapp homes / SYNTHESIS peel / full-workflow webapp gate.

## Alternatives (accept spine)

| Option | Verdict |
|--------|---------|
| A. Make `reference_preference_v1` the default | Rejected as sole answer. Shipped pairwise is real, but it is reference-window conditioned on held-out/source text, not style-block constitution climb. |
| B. New pairwise-vs-best accept; reuse preference job board; style-block as immutable meta-rubric | **Chosen.** Day-one shape if we had known Goodhart on mean. Migrate mean rulers then delete dual-truth. |
| C. Keep `style_fidelity` string; silently swap mean for pairwise | Rejected. Naming lie + dual-truth risk. Supersede ADR 003 with an explicit new default (or versioned metric id). |

## Phases (ordered)

1. [phase-00-harness](climb_signal_redesign/phase-00-harness.md) — red gaming fixture
2. [phase-01-accept-types](climb_signal_redesign/phase-01-accept-types.md)
3. [phase-02-hard-veto](climb_signal_redesign/phase-02-hard-veto.md)
4. [phase-03-pairwise-accept](climb_signal_redesign/phase-03-pairwise-accept.md)
5. [phase-04-retire-mean-ruler](climb_signal_redesign/phase-04-retire-mean-ruler.md)
6. [phase-05-revise-unit](climb_signal_redesign/phase-05-revise-unit.md)
7. [phase-06-epsilon-band](climb_signal_redesign/phase-06-epsilon-band.md)
8. [phase-07-canvas-gaming-ux](climb_signal_redesign/phase-07-canvas-gaming-ux.md)
9. [phase-08-held-out-anticheat](climb_signal_redesign/phase-08-held-out-anticheat.md)
10. [phase-09-crossover](climb_signal_redesign/phase-09-crossover.md)
11. [phase-10-closeout](climb_signal_redesign/phase-10-closeout.md)

See [testing.md](climb_signal_redesign/testing.md).

## Verification

```powershell
$env:PYTHONPATH="."
python -m pytest tests/ -q
```

Per phase: pytest green; no HTTP scores writes; after accept path ships, `control-cli` smoke on one existing run slug; after Canvas phase, `control-ui` smoke GET `/runs/<slug>`.

## Implementation guidance (after gate)

- **how** before editing climb_metrics / progression / preference jobs / Canvas.
- **interrogate** the AcceptDecision boundary before merge.
- **show-me-your-work** trail: `handoff/decision-trails/climb-signal-redesign.tsv`.
- `/deslop` before commit; **unslop** on prose/ADR.
- **babysit** after PR open.
- **migrate-callers-then-delete** mean-as-sole-ruler (no permanent dual climb truth).
