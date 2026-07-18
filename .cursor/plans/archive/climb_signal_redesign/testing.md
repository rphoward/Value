# Climb-signal redesign — testing

Back-link: [overview.md](overview.md)

## Project suite

```powershell
$env:PYTHONPATH="."
python -m pytest tests/ -q
```

## Phase map

| Phase | Static | Runtime |
|-------|--------|---------|
| 00 harness | Red/xfail fixture for mean vs pairwise disagree | N/A |
| 01 types | Construct/round-trip AcceptDecision family | N/A |
| 02 hard veto | Mean↑ + floor fail → not best | CLI record shows veto |
| 03 pairwise accept | Pref job → preference_outcome; harness turns green | CLI pref-job chain |
| 04 retire mean | Init default; seed/best/stop on new metric | Inspect on throwaway slug |
| 05 revise unit | PatchScope in craft brief inputs | One scoped revise step |
| 06 ε-band | Target↑ neighbors crash → reject | CLI reject reason |
| 07 Canvas UX | canvas/climb_strip/presentation tests; no scores write | control-ui GET run canvas |
| 08 held-out | Held-out fail blocks promotion | CLI on held-out run |
| 09 crossover | Splice → same accept path | Dogfood splice |
| 10 closeout | Full suite + docs | Dogfood + human gate |

## Locks to preserve

- `tests/test_presentation_runs.py` and climb-strip tests: HTTP never writes `scores.json`.
- Existing `reference_preference_v1` path remains valid for old runs.
- `pick_best` remains human marker only.
- **Consumer contracts (required for any climb-accept PASS):** `tests/test_climb_accept_consumer_contracts.py`. Writer-only phase green is not enough. See `handoff/CLIMB-SIGNAL-INTENT-REPAIR-PASSED.md`.

```powershell
$env:PYTHONPATH="."
python -m pytest tests/test_climb_accept_consumer_contracts.py -q
```

| Contract | Guards |
|----------|--------|
| ε fail-closed | Missing non-target / partial target scores reject |
| Veto × preference | No preference sidecar on vetoed rows |
| Held-out cadence | `held_out_check_due` → preference next_action, not draft |
| Canvas AcceptDecision | Nested decision wins over flat keys |
| SDK `--held-out` | Record args include flag when cadence due |

## Surfaces

- CLI/SDK: `control-cli` or existing `hillclimb_once` / `python -m eliotapp.cli`.
- Browser: `control-ui` after phase 07.
- No live `CURSOR_API_KEY` climb required for unit phases. Dogfood once before closeout.
