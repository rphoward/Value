# Phase 06 — Canvas from AcceptDecision

**Goal.** AcceptDecision is Canvas source of truth when present.

**Changes.** `parse_latest_accept`: prefer `accept_decision` → `AcceptDecision.from_dict` → `LatestAccept` (+ `held_out`); else flat legacy.

**Verify.** `tests/test_canvas_accept.py`: decision-only, flat legacy, decision wins on conflict.
