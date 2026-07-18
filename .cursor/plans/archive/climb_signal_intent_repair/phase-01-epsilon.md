# Phase 01 — ε fail-closed

**Goal.** Missing qualitative scores cannot soft-pass the ornament-gaming guard.

**Changes.** `eliotapp/core/shapes/accept.py` `evaluate_epsilon_band`: missing incumbent/challenger for any named target → fail; missing non-target → band failure. Empty `target_axes` stays no-op.

**Verify.** `tests/test_epsilon_band.py`: partial targets reject; missing non-target rejects.
