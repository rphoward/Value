# Phase 02 — Veto blocks preference

**Goal.** Hard veto outranks soft preference; no sidecar; no preference_tie stop on vetoed rows.

**Changes.** `record_preference`: if `accept_status == "vetoed"`, raise before writing sidecar / before soft `should_stop`.

**Verify.** `tests/test_hard_veto.py`: vetoed + record_preference → no sidecar; accept stays vetoed.
