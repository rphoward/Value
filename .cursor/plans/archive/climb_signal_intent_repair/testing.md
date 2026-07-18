# Climb-signal intent repair — testing

Back-link: [overview.md](overview.md)

## Required consumer contracts

These are the done predicate for this track. Full suite green without them is not enough.

```powershell
$env:PYTHONPATH="."
python -m pytest tests/test_climb_accept_consumer_contracts.py -q
```

Gate: `handoff/CLIMB-SIGNAL-INTENT-REPAIR-PASSED.md`.

## Full suite

```powershell
$env:PYTHONPATH="."
python -m pytest tests/ -q
```
