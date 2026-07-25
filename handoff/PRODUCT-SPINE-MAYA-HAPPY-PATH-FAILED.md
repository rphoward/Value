(def-sop product-spine-maya-happy-path-failed
  (context
    (target "fresh-session-agent-or-human-reviewer")
    (optimization "honest-close-after-compressed-walk-misdeclared-pass")
    (outcome FAIL)
    (closed 2026-07-25)
    (opened-as handoff/PRODUCT-SPINE-MAYA-HAPPY-PATH-OPEN.md)
    (supersedes handoff/PRODUCT-SPINE-MAYA-HAPPY-PATH-PASSED.md)
    (mock-slug shiftswap)
    (prior-gate handoff/PRODUCT-SPINE-UX-MOCK-PASSED.md))

  <central_idea>
  (center-of-gravity
    (invariant "Maya happy-path required one-atom-per-turn chat dogfood with no compressed walk. Closing PASSED after bulk accept-driver scripts violated that contract even though session.json had non-bypass answers.")))

  (protocol-0-outcome
    (result FAIL)
    (blocker "Gate closed PASSED after compressed bulk-accept walk (drive_value_leg.py / drive_lean_leg.py); OPEN and paste forbid no-compressed-walk and Play-Maya-in-chat one-atom-per-turn")
    (evidence tools/drafts/product-spine-maya-happy-path/WALK-EVIDENCE.md
              tools/drafts/product-spine-maya-happy-path/drive_value_leg.py
              tools/drafts/product-spine-maya-happy-path/drive_lean_leg.py)
    (tests "python -m pytest tests/test_product_spine_skill.py -v → 9 passed — tests green; walk method failed the gate"))

  (protocol-1-what-still-counts
    (note "Non-bypass session answers under shiftswap remain useful raw evidence for coaching gaps")
    (note "Compression-as-misbehavior is owned by the Kai unhappy-path gate — not re-run as Maya PASS"))

  (protocol-2-next
    (opened-next handoff/PRODUCT-SPINE-KAI-UNHAPPY-PATH-OPEN.md)
    (paste handoff/NEW-CHAT-PROMPT-PRODUCT-SPINE-KAI-UNHAPPY-PATH.md)
    (maya-retry "optional later — only as true one-atom chat walk; do not revive PASSED")))
