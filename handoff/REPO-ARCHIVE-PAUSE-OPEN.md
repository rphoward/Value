(def-sop repo-archive-pause-open
  (context
    (target "human-or-fresh-session-on-resume")
    (optimization "temporary-archive-pending-extensive-human-dogfood-elsewhere")
    (outcome OPEN)
    (opened 2026-08-02)
    (paste-block handoff/NEW-CHAT-PROMPT-RESUME-AFTER-HUMAN-DOGFOOD.md)
    (prior handoff/JOURNEY-UX-TEST-EXPANSION-EXECUTE-PASSED.md))

  <central_idea>
  (center-of-gravity
    (invariant "Value monorepo is pushed, mirrors verified, and pytest green. Human dogfood of /product-spine runs in a consumer repo. This gate stays OPEN until dogfood findings are triaged or the human explicitly resumes development here.")))

  (protocol-0-verified-before-pause
    (value-repo "https://github.com/rphoward/Value.git @ eb0fe92 — master matches origin/master; working tree clean")
    (product-spine-pack "https://github.com/rphoward/Product-Spine.git @ e7a0a56 — main matches origin/main; working tree clean")
    (values-pack "https://github.com/rphoward/Values.git @ e721eb8 — master matches origin/master; working tree clean")
    (pytest "python -m pytest tests/ -q → 179 passed (2026-08-02)")
    (journey-ux-spot "python -m pytest tests/test_product_spine_skill.py tests/test_teams_skill_package.py tests/test_bmg_skill_package.py tests/test_maya_happy_pass_lint.py -v → 30 passed"))

  (protocol-1-mirror-byte-equivalence
    (cursor-vs-skills-mirror "all seven skills byte-identical: product-spine (3), value (51), bmg (31), teams (31), brand-identity (31), lean-mvp (37), story-generation-prompt (13)")
    (standalone-product-spine "skills/* trees match value/skills/* except dev-only COMPILE-NOTES.md under bmg/ and teams/ — not shipped to Product-Spine pack by design")
    (forbidden 'wipe-shiftswap 'wipe-cashclaw 'wipe-value-design))

  (protocol-2-open-gates-at-pause
    (none "all product-spine journey UX execute gates closed PASS")
    (this-gate "repo archive pause — OPEN until resume"))

  (protocol-3-human-dogfood-elsewhere
    (where "consumer repo with npx skills add rphoward/Product-Spine (or sibling packs as installed)")
  (first-turns
      "fresh chat → /product-spine on value-design (cold restart; progress-so-far before hunt)"
      "same or new chat → day-two where-am-I; optional brand/teams legs if seeded")
    (prove "coaching voice + four-slot guide-turn in live Cursor chat — not agent simulation")
    (record "friction in consumer workproduct or a decision-trail TSV; do not wipe historical slugs here"))

  (protocol-4-resume
    (paste handoff/NEW-CHAT-PROMPT-RESUME-AFTER-HUMAN-DOGFOOD.md)
    (triage "dogfood findings → SKILL fixes, new needles, or FAILED walk close records")
    (close-as handoff/REPO-ARCHIVE-PAUSE-PASSED.md or FAILED with one blocker))

  (protocol-5-next-owner
    (next "human dogfood in consumer repo; reopen Value when findings land or explicit resume")))
