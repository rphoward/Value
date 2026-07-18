# Phase 03 — IterationFact held_out_check_due

**Goal.** Progression sees cadence without Path I/O in core.

**Changes.** Add `held_out_check_due: bool` to `IterationFact`; load in infrastructure `run_snapshot` (default false).

**Verify.** Fixture load / run_state constructions of `IterationFact`.
