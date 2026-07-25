(def-sop product-spine-kai-unhappy-path-open
  (context
    (target "fresh-session-agent")
    (optimization "discover-coaching-holes-when-human-skips-compresses-and-chases-million-dollar-vibecode")
    (outcome OPEN)
    (opened 2026-07-25)
    (paste-block handoff/NEW-CHAT-PROMPT-PRODUCT-SPINE-KAI-UNHAPPY-PATH.md)
    (mock-slug cashclaw)
    (prior-gates handoff/PRODUCT-SPINE-UX-MOCK-PASSED.md
                 handoff/PRODUCT-SPINE-MAYA-HAPPY-PATH-FAILED.md)
    (ship-pack https://github.com/rphoward/Product-Spine))

  <central_idea>
  (center-of-gravity
    (invariant "This gate owns the less-happy path: a teenage vibecoder who wants a million from AI, barely knows value or coding, disobeys pacing, compresses or jumps legs, and needs coaching. Success is surfacing and fixing skill coaching holes — not proving a clean Maya walk. Compression and wrong turns are expected stimuli, not automatic FAIL.")))

  (protocol-0-preconditions
    (shipped "product-spine guide-turn + lean forward-claim — see PRODUCT-SPINE-UX-MOCK-PASSED.md")
    (maya-fail "PRODUCT-SPINE-MAYA-HAPPY-PATH-FAILED.md — compressed bulk-accept walk is prior stimulus; do not treat as happy-path PASS")
    (tests "python -m pytest tests/test_product_spine_skill.py -v must be green before walk")
    (wipe-first
      "delete workproduct/value-proposition/cashclaw/ and workproduct/lean-mvp/cashclaw/ if present"
      "do not reuse shiftswap — that slug is Maya evidence only")
    (forbidden 'invent-spine-session-json 'fifth-coordinator 'treating-kai-compression-as-maya-retry))

  (protocol-1-unhappy-path
    (persona Kai CashClaw slug cashclaw)
    (human-traits
      "teen vibecoder; million-dollar AI fantasy; thin product sense; weak coding patience"
      "skips or skims instructions; asks for full app / pitch / video early"
      "may compress grilling, bypass gates, or dump brain-dumps that skip atoms"
      "needs plain coaching without atom IDs or curriculum dumps")
    (legs-still-named
      (clarity "/product-spine → /value — expect wrong starts and coaching")
      (mvp "/product-spine → /lean-mvp — expect feature-first jumps")
      (claim "/product-spine → story inline — expect hype ceiling fights"))
    (stimulus-ok
      "compression, gate bypass attempts, skill-skipping, early claim intent, solution-first asks"
      "agent must stay in skill contracts while coaching Kai back — log every recovery or miss"))

  (protocol-2-when-hole-appears
    (stop "if skill contract cannot coach Kai without inventing a fifth coordinator or spine session.json — record FAIL blocker")
    (optional-poteto "only when a real coaching hole needs design — not a mandatory arena")
    (forbidden 'paper-over-with-tutorial-only 'declare-pass-while-ignoring-logged-misses))

  (protocol-3-success
    (primary "friction log shows wrong turns + what coaching recovered or failed")
    (secondary "Kai reaches an honest claim ceiling or an explicit FAILED blocker naming one coaching gap")
    (evidence handoff/decision-trails/product-spine-kai-unhappy-path.tsv
              tools/drafts/product-spine-kai-unhappy-path/WALK-EVIDENCE.md)
    (pytest tests/test_product_spine_skill.py -v green)
    (close-as handoff/PRODUCT-SPINE-KAI-UNHAPPY-PATH-PASSED.md or FAILED with one blocker))

  (protocol-4-next-owner
    (fresh-session "paste NEW-CHAT-PROMPT-PRODUCT-SPINE-KAI-UNHAPPY-PATH.md; wipe cashclaw; run unhappy path")
    (this-session "handoff authored only — do not start the grill here")))
