# Phase 04 — Progression held-out preference gate

**Goal.** After primary pairwise binds, cadence does not jump to `draft` while due.

**Changes.** `progression.decide`: pairwise + binding + `held_out_check_due` → preference open/continue/record with issue `held_out_overlay_due`.

**Verify.** `tests/test_run_state.py` + `tests/test_held_out_accept.py`.
