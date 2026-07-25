(def-sop product-spine-ux-mock-open
  (context
    (target "fresh-session-agent")
    (optimization "prove-spine-guide-carries-human-to-claim-and-notebooklm")
    (outcome OPEN)
    (opened 2026-07-25)
    (paste-block handoff/NEW-CHAT-PROMPT-PRODUCT-SPINE-UX-MOCK.md)
    (mock-slug shiftswap)
    (ship-pack https://github.com/rphoward/Product-Spine))

  <central_idea>
  (center-of-gravity
    (invariant "Product-spine was rewritten as a journey guide. Fresh work owns a full Maya UX mock plus poteto architect/arena so the guide actually delivers valuable → marketable (INVEST + NotebookLM), not another map of skills the human cannot walk."))
  </central_idea>

  (protocol-0-problem
    (failure "Prior triage-only spine dumped humans after naming a door; claim/NotebookLM exit missing once sessions existed; tutorials carried UX weight spine was expected to carry")
    (rewrite-landed
      (cursor .cursor/skills/product-spine/)
      (ship-mirror skills/product-spine/)
      (github Product-Spine f23e56b)
      (note "Value monorepo may still have uncommitted spine + AGENTS.md — verify git status")))

  (protocol-1-must-complete-mock-walk
    (persona Maya ShiftSwap slug shiftswap)
    (legs clarity→value mvp→lean-mvp claim→story-generation-prompt)
    (forbidden 'triage-and-abandon 'skip-claim-exit 'spine-session-json 'paper-over-with-tutorial-only))

  (protocol-2-poteto-and-arena
    (mode "/poteto-mode Feature — full UX mock; architect + arenas before shipping guide fixes")
    (arena
      (path tools/drafts/product-spine-ux-arena/)
      (deliverables "2–4 throwaway guide-turn mocks at clarity/mvp/claim")
      (pick-record handoff/decision-trails/product-spine-ux-mock.tsv))
    (model-lock
      (agents-runners composer-2.5 cursor-grok-4.5-high)
      (judge-only claude-4.6-opus-low-thinking :user-said "opus 4.5 low for broader training not reasoning")
      (forbidden gpt-5.6-sol-high fable other-unlisted-runners)))

  (protocol-3-success
    (walk-reaches INVEST-sentence-and-notebooklm-producer-paste)
    (pytest tests/test_product_spine_skill.py -v green)
    (close-as handoff/PRODUCT-SPINE-UX-MOCK-PASSED.md or FAILED with one blocker))

  (protocol-4-next-owner
    (fresh-session "paste NEW-CHAT-PROMPT-PRODUCT-SPINE-UX-MOCK.md; run poteto Feature + Maya walk")
    (this-session "handoff authored; rewrite already on Product-Spine — do not re-litigate receptionist vs guide")))
