# Climb-signal intent repair — overview

Back-link: [climb_intent_repair_f2128c14.plan.md](../climb_intent_repair_f2128c14.plan.md)

## Context

Act-on interrogate fixes are already on `feature/climb-signal-redesign`. This track closes four **intent-blocking** gaps only (ε fail-closed, veto blocks preference, live held-out cadence, Canvas from `accept_decision`). Soft-fail Canvas and UI redesign stay out.

## Scope

**In:** phases 1–7 below.  
**Out:** soft-fail corrupt accept, delete flat `accept_*` dual-write, UI restyle, new climb metric.

## Phases

| Phase | Goal |
|-------|------|
| [01](phase-01-epsilon.md) | ε fail-closed on missing scores |
| [02](phase-02-veto-pref.md) | Veto blocks preference attach |
| [03](phase-03-iteration-fact.md) | `IterationFact.held_out_check_due` |
| [04](phase-04-progression.md) | Progression opens held-out preference |
| [05](phase-05-sdk-held-out.md) | SDK `--held-out` when due |
| [06](phase-06-canvas.md) | Canvas from `accept_decision` |
| [07](phase-07-closeout.md) | Suite + trail + STATE + plans index |

## Verification

```powershell
$env:PYTHONPATH="."; python -m pytest tests/test_climb_accept_consumer_contracts.py -q
$env:PYTHONPATH="."; python -m pytest tests/ -q
```

Consumer contracts are the done lock. See [testing.md](testing.md) and `handoff/CLIMB-SIGNAL-INTENT-REPAIR-PASSED.md`.
