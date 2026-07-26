(def-sop product-spine-cold-restart-open
  (context
    (target "fresh-session-agent")
    (optimization "prove-cold-restart-you-are-here-names-progress-so-far")
    (outcome OPEN)
    (opened 2026-07-25)
    (paste-block handoff/NEW-CHAT-PROMPT-PRODUCT-SPINE-COLD-RESTART.md)
    (mock-slug value-design)
    (prior-ship "product-spine progress-so-far in you-are-here — voice-only re-entry"))

  <central_idea>
  (center-of-gravity
    (invariant "Maya/Kai walks are continuous. This gate owns cold restart: new chat, only /product-spine, existing value-design notes — you-are-here must name progress so far in plain words before asking the human to hunt or paste. No fifth guide-turn beat. No spine session.json.")))

  (protocol-0-preconditions
    (tests "python -m pytest tests/test_product_spine_skill.py -v must be green before walk")
    (slug-exists "workproduct/value-proposition/value-design/session.json and milestone notes must already exist — do not wipe")
    (forbidden 'wipe-value-design 'invent-spine-session-json 'fifth-guide-turn-beat 'quote-status-stdout-to-user))

  (protocol-1-cold-restart
    (persona "returning vibecoder who closed the chat yesterday")
    (legs
      (reentry "new chat → invoke only /product-spine → score you-are-here for progress so far from --sections plain words")
      (no-hunt "fail if the turn asks the human to find, open, or paste profile/map/north-star when those files exist"))
    (voice "four-slot guide-turn only; claim adds files-im-using when phase is claim"))

  (protocol-2-success
    (walk-reaches "you-are-here with real progress so far before any file-hunt ask")
    (evidence handoff/decision-trails/product-spine-cold-restart.tsv)
    (pytest tests/test_product_spine_skill.py -v green)
    (close-as handoff/PRODUCT-SPINE-COLD-RESTART-PASSED.md or FAILED with one blocker))

  (protocol-3-next-owner
    (next "close this gate after one cold-restart walk; do not expand into full Maya/Kai re-runs")))
