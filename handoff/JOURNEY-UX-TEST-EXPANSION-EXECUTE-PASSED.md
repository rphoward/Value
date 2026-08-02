(def-sop journey-ux-test-expansion-execute-passed
  (context
    (target "fresh-session-agent-or-human-reviewer")
    (optimization "execute-accepted-journey-ux-plan-slice-by-slice")
    (outcome PASS)
    (closed 2026-08-01)
    (opened-as handoff/JOURNEY-UX-TEST-EXPANSION-EXECUTE-OPEN.md)
    (accepted-plan .cursor/plans/journey_ux_test_expansion_ff27e8a7.plan.md)
    (prior-gate handoff/JOURNEY-UX-TEST-EXPANSION-PASSED.md))

  <central_idea>
  (center-of-gravity
    (invariant "Slices 1–7 of the Journey UX Test Expansion plan are done with pytest green and walk trails. Compressed accept drivers were never counted as happy PASS. Historical slugs shiftswap, cashclaw, and value-design were not wiped. Appendix Maya was skipped.")))

  (protocol-0-outcome
    (result PASS)
    (evidence handoff/decision-trails/journey-ux-test-expansion-execute.tsv
              handoff/PRODUCT-SPINE-COLD-RESTART-PASSED.md
              tools/drafts/product-spine-journey-day2/WALK-EVIDENCE.md
              tools/drafts/product-spine-journey-first/WALK-EVIDENCE.md
              tools/drafts/product-spine-journey-optional-legs/WALK-EVIDENCE.md
              tools/drafts/product-spine-journey-bmg/WALK-EVIDENCE.md)
    (tests "python -m pytest tests/test_teams_skill_package.py tests/test_bmg_skill_package.py tests/test_product_spine_skill.py tests/test_maya_happy_pass_lint.py -v → 30 passed"))

  (protocol-1-slices
    (s1 PASS "dual-intent, open-session, optional-leg needles + Maya encode lint")
    (s2 PASS "value-only cold restart on value-design")
    (s3 PASS "day-two multi-leg cold/warm on journey-day2*")
    (s4 PASS "first-hour empty slate + claim-exit")
    (s5 PASS "brand/teams/dual + unhappy stimuli")
    (s6 PASS "thin teams + bmg package tests")
    (s7 PASS "BMG happy + unhappy")
    (appendix SKIP "human did not ask"))

  (protocol-2-wiring-notes
    (note "Mid-Evolve after clarity-ready has no dedicated phase label; one-session kept /value on cold restart — noted, not a FAIL")
    (note "SKILL.md not edited; needles and walks held against live tree"))

  (protocol-3-next
    (optional "human dogfood turn on cold restart / day-two in a real new chat")
    (optional "Appendix Maya one-atom if still wanted — own gate")
    (none-required-for-this-gate)))
