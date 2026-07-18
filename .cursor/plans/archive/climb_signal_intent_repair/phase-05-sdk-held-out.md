# Phase 05 — SDK --held-out when due

**Goal.** Autonomous SDK path applies prefer-vs-held-out.

**Changes.** `tools/sdk_climb_lib.py`: when latest has `held_out_check_due`, pass `--held-out` to `pref-job-record`. Explicit flag only.

**Verify.** Focused unit/SDK test that record args include `--held-out` when due.
