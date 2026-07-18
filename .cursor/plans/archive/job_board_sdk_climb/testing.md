# Testing matrix

Back-link: [overview.md](overview.md)

## Automated (every phase that touches Python)

```powershell
$env:PYTHONPATH="src"
python -m pytest tests/test_job_board.py tests/test_hillclimb.py tests/test_sdk_climb_preflight.py -q
```

Expect green before claiming a phase done. Full `tests/` before merge.

## Manual gates

| Gate | When | Pass criteria |
|------|------|---------------|
| Mid-batch resume | After phase 2 | Fake `in_progress` job on a copy of a run folder; `job-status` lists pending; completing remaining trials → `job-record` attaches `indistinguishability` |
| Seed-suffix resume | After phase 2–3 | `job-open` with `v1a` (and peers); mid-batch resume; all three seed jobs completable before winner `record` |
| Protocol dry-read | After phase 3 | `/hillclimb` resume checklist matches job-status-first order **and** seed-round steps |
| SDK spike | After phase 4 | `handoff/SDK-CLIMB-SPIKE.md` names A/B/C; if A or B, evidence of isolated workers; if C, phase 5 cancelled in STATE/pipeline docs |
| Unattended resume | After phase 5 (if not deferred) | Interrupt `sdk-climb.py` mid-batch; job file shows pending; second invoke finishes; exit **0**; preflight failures exit **1**; agent error **2**; incomplete climb **3** |
| Seam copy | After phase 6 | Pipeline skill + catalog + prepare copy + ADR + STATE agree on driver entry (or `/hillclimb` only if deferred) |

## Cost policy

- No full 5-iter live climb in CI.
- Prefer fixture slugs under `tools/runs/` with existing drafts for discrimination-only resumes.
- Live SDK calls require human-present API key; never commit secrets.

## Definition of done (spike)

1. Job board module + CLI + tests green.
2. Chat and driver share the same resume order in docs.
3. Spike note proves A or B, or explicitly chooses C (defer driver).
4. If not deferred: `tools/sdk-climb.py` preflight-tested with exit codes `0|1|2|3`; one manual resume smoke recorded.
5. Pipeline/ADR/STATE point at the driver (or `/hillclimb` only if deferred).
6. Out-of-scope items remain out (no Start Climb button, no scorer changes).
7. Seed-round resume contract present in phase 3 docs.
