(def-sop journey-ux-test-expansion-passed
  (context
    (target "fresh-session-agent")
    (optimization "plan-accepted-suite-not-yet-built")
    (outcome PASS)
    (closed 2026-08-01)
    (supersedes handoff/JOURNEY-UX-TEST-EXPANSION-OPEN.md)
    (paste-block handoff/NEW-CHAT-PROMPT-JOURNEY-UX-TEST-EXPANSION.md)
    (execute-next handoff/JOURNEY-UX-TEST-EXPANSION-EXECUTE-OPEN.md)
    (execute-paste handoff/NEW-CHAT-PROMPT-JOURNEY-UX-TEST-EXPANSION-EXECUTE.md))

  <central_idea>
  (center-of-gravity
    (invariant "Human accepted the Journey UX Test Expansion plan. Closing this gate means the plan exists and is accepted — not that the suite is built. Execution is a separate gate.")))

  (protocol-0-evidence
    (plan .cursor/plans/journey_ux_test_expansion_ff27e8a7.plan.md)
    (critique "poteto-agent accept-with-edits — Experience First + Prove It Works; day-two multi-leg slice added after human ask")
    (plan-owns
      "coverage matrix; pass/fail + Maya encode lint; slug policy; slices 1–7 + appendix Maya; first-hour + day-two checklist; out-of-scope"))

  (protocol-1-accepted-slice-order
    (s1 "minimal spine needles + Maya encode lint")
    (s2 "value-only cold restart — PRODUCT-SPINE-COLD-RESTART-OPEN")
    (s3 "day-two / warm multi-leg re-entry — journey-day2")
    (s4 "first-hour no-session + short claim-exit — journey-first")
    (s5 "optional-leg brand/teams/dual walks through claim")
    (s6 "thin teams + bmg package tests")
    (s7 "BMG happy + unhappy walks")
    (appendix "optional Maya one-atom — own gate; not critical path"))

  (protocol-2-next-or-none
    (next "fresh session: paste NEW-CHAT-PROMPT-JOURNEY-UX-TEST-EXPANSION-EXECUTE.md; execute plan slices in order")
    (forbidden 'treating-this-PASSED-as-suite-built)))
