(def-sop product-spine-maya-happy-path-open
  (context
    (target "fresh-session-agent")
    (optimization "prove-maya-happy-path-with-real-grilling-no-bypasses")
    (outcome OPEN)
    (opened 2026-07-25)
    (paste-block handoff/NEW-CHAT-PROMPT-PRODUCT-SPINE-MAYA-HAPPY-PATH.md)
    (mock-slug shiftswap)
    (prior-gate handoff/PRODUCT-SPINE-UX-MOCK-PASSED.md)
    (ship-pack https://github.com/rphoward/Product-Spine))

  <central_idea>
  (center-of-gravity
    (invariant "UX guide-turn contract already shipped. This gate owns the real Maya happy path: genuine value + lean grilling to done-enough, then claim INVEST + NotebookLM — no gate bypasses, no compressed walk, no new coordinator.")))

  (protocol-0-preconditions
    (shipped "product-spine guide-turn + lean forward-claim — see PRODUCT-SPINE-UX-MOCK-PASSED.md")
    (tests "python -m pytest tests/test_product_spine_skill.py -v must be green before walk")
    (wipe-first
      "delete workproduct/value-proposition/shiftswap/ and workproduct/lean-mvp/shiftswap/ if present — prior sessions used gate bypasses and are not happy-path evidence")
    (forbidden 'reuse-bypassed-shiftswap-sessions 'skip-claim-exit 'invent-spine-session-json 'gate-bypass-as-happy-path))

  (protocol-1-happy-path
    (persona Maya ShiftSwap slug shiftswap)
    (legs
      (clarity "/product-spine → /value → profile + value-map done-enough with real answers")
      (mvp "/product-spine → /lean-mvp → mvp-scope done-enough with real answers; lean must cue /product-spine")
      (claim "/product-spine → follow story-generation-prompt same turn → INVEST sentence + NotebookLM producer paste when video wanted"))
    (voice "spine emits four-slot guide-turn; no atom IDs to Maya; one atom per sibling turn"))

  (protocol-2-when-walk-breaks
    (stop "fix skill contract (spine first, then sibling handoff)")
    (optional-poteto "only if a real UX hole appears — not a mandatory arena this gate")
    (forbidden 'paper-over-with-tutorial-only 'compress-via-bypass-gates))

  (protocol-3-success
    (walk-reaches INVEST-sentence-and-notebooklm-producer-paste)
    (evidence handoff/decision-trails/product-spine-maya-happy-path.tsv
              tools/drafts/product-spine-maya-happy-path/WALK-EVIDENCE.md)
    (pytest tests/test_product_spine_skill.py -v green)
    (close-as handoff/PRODUCT-SPINE-MAYA-HAPPY-PATH-PASSED.md or FAILED with one blocker))

  (protocol-4-next-owner
    (closed-as handoff/PRODUCT-SPINE-MAYA-HAPPY-PATH-FAILED.md)
    (next-gate handoff/PRODUCT-SPINE-KAI-UNHAPPY-PATH-OPEN.md)
    (note "do not re-open Maya PASS via bulk drivers; optional true chat retry later")))
