# Testing — SYNTHESIS peel

Back-link: [overview.md](overview.md)

## Project suite (every phase)

```powershell
$env:PYTHONPATH="."
python -m pytest tests/ -q
```

## Surface checks by phase

| Phase | Surface | Check |
|-------|---------|-------|
| 00 | disk / git | no `EliotWF` gitlink; no egg-info residue |
| 01 | CLI / SDK | inspect next-action matches prior on fixture |
| 02 | HTTP | runs list cheap path covered by test |
| 03 | CLI | hillclimb_cli or `eliotapp.cli` import path works |
| 04 | CLI / score | scorecard or adherence write still lands |
| 05–06 | HTTP | TestClient or control-ui GET `/` and `/runs/<slug>` |
| 07 | CLI | `python -m eliotapp.cli --help` + one inspect |
| 08 | lint | import-linter contract (if added) |
| 09 | docs | STATE + gate record match reality |

## Definition of done for the track

- All overview phases complete or explicitly skipped with reason.
- `loop.py` gone.
- No Path I/O under `eliotapp/core/`.
- Catalog resolved under `workproduct/` (dual-read only inside locator if still needed).
- Root no longer shows orphan `EliotWF/` or egg-info as “extra Eliot homes.”
