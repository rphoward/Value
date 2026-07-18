# Phase 05b — Climb strip

Back-link: [overview.md](overview.md)

## Goal

Style-fidelity sparkline plus cooperative pause / resume / step when `scores.json` exists.

## Changes

- Climb strip UI (Cockpit graft)
- Cooperative pause/resume/step signals to the driver (ledger or control file; HTTP still never writes scores)
- Sparkline from scores history

## Data structures

- Climb strip view model from scores (read-only) + pause control owned by job/ledger

## Verification

**Static.** Pytest for pause signal + sparkline data helper.

**Runtime.** control-ui: pause/resume/step while improve runs (or simulated).
