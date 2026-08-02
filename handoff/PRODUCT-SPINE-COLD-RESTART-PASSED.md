(def-sop product-spine-cold-restart-passed
  (context
    (target "fresh-session-agent-or-human-reviewer")
    (optimization "cold-restart-you-are-here-names-progress-so-far")
    (outcome PASS)
    (closed 2026-08-01)
    (opened-as handoff/PRODUCT-SPINE-COLD-RESTART-OPEN.md)
    (mock-slug value-design)
    (prior-ship "product-spine progress-so-far in you-are-here — voice-only re-entry"))

  <central_idea>
  (center-of-gravity
    (invariant "Cold restart on value-design proved you-are-here names progress so far in plain words before any hunt or paste ask. Four-slot guide-turn only. No spine session.json. value-design was not wiped.")))

  (protocol-0-outcome
    (result PASS)
    (evidence handoff/decision-trails/product-spine-cold-restart.tsv)
    (tests "python -m pytest tests/test_product_spine_skill.py tests/test_maya_happy_pass_lint.py -v → green")
    (guide-turn-scored
      "You are here: continuing value for value-design — profile and value map are done; business-model Evolve still open (delivery and later Evolve bits not filled yet)."
      "Why this phase: open value session mid business-model; one-session continue (no claim, brand, teams, or bmg ask)."
      "This turn: open /value — pick up business-model where you left off."
      "Come back when: you finish enough Evolve work or want MVP or claim next; then invoke /product-spine again."))

  (protocol-1-what-was-proven
    (progress-so-far "translated from --sections / milestones; not raw strip symbols")
    (no-hunt "profile, map, and north-star already on disk; turn did not ask to paste")
    (four-slots "you-are-here, why-this-phase, this-turn, come-back-when — no fifth beat"))

  (protocol-2-not-proven
    (note "Not multi-leg day-two; that is Slice 3 journey-day2")
    (note "Mid-Evolve after clarity-ready has no dedicated phase label; one-session kept /value rather than mvp yank — wiring note only"))

  (protocol-3-next
    (next "Journey UX execute continues at Slice 3")
    (none-required-for-this-gate)))
