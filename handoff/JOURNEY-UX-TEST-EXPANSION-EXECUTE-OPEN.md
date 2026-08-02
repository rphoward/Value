(def-sop journey-ux-test-expansion-execute-open
  (context
    (target "fresh-session-agent")
    (optimization "execute-accepted-journey-ux-plan-slice-by-slice")
    (outcome OPEN)
    (opened 2026-08-01)
    (paste-block handoff/NEW-CHAT-PROMPT-JOURNEY-UX-TEST-EXPANSION-EXECUTE.md)
    (accepted-plan .cursor/plans/journey_ux_test_expansion_ff27e8a7.plan.md)
    (prior-gate handoff/JOURNEY-UX-TEST-EXPANSION-PASSED.md))

  <central_idea>
  (center-of-gravity
    (invariant "Execute the accepted Journey UX Test Expansion plan in order. Prove vibecoder delight with walks that work. Never count compressed bulk-accept as happy PASS. Do not wipe shiftswap, cashclaw, or value-design.")))

  (protocol-0-preconditions
    (read
      ".cursor/plans/journey_ux_test_expansion_ff27e8a7.plan.md"
      "handoff/JOURNEY-UX-TEST-EXPANSION-PASSED.md"
      "handoff/STATE.md"
      "handoff/PRODUCT-SPINE-MAYA-HAPPY-PATH-FAILED.md"
      "handoff/PRODUCT-SPINE-KAI-UNHAPPY-PATH-PASSED.md"
      "handoff/PRODUCT-SPINE-COLD-RESTART-OPEN.md")
    (pytest-baseline "python -m pytest tests/test_product_spine_skill.py -v must be green before walks"))

  (protocol-1-slice-order
    (s1 "minimal spine needles + Maya encode lint")
    (s2 "value-only cold restart on value-design — close PRODUCT-SPINE-COLD-RESTART-*")
    (s3 "day-two multi-leg warm/cold — journey-day2")
    (s4 "first-hour + claim-exit — journey-first")
    (s5 "optional-leg walks through claim — journey-brand/teams/dual")
    (s6 "thin teams + bmg package tests")
    (s7 "BMG happy + unhappy — journey-bmg")
    (appendix "Maya one-atom only if human still wants it — separate gate"))

  (protocol-2-success
    (slices "S1–S7 done with Verify commands green and walk trails where required")
    (evidence "handoff/decision-trails/ + tools/drafts/product-spine-journey-* WALK-EVIDENCE")
    (close-as handoff/JOURNEY-UX-TEST-EXPANSION-EXECUTE-PASSED.md or FAILED with one blocker)
    (note "Appendix Maya is optional and does not block EXECUTE PASS"))

  (protocol-3-forbidden
    (forbidden 'wipe-shiftswap 'wipe-cashclaw 'wipe-value-design
               'bulk-accept-as-happy-PASS 'revive-Maya-PASSED
               'dilate-value-only-cold-gate-into-multileg))

  (protocol-4-next-owner
    (next "fresh session: paste NEW-CHAT-PROMPT-JOURNEY-UX-TEST-EXPANSION-EXECUTE.md; start Slice 1")))
