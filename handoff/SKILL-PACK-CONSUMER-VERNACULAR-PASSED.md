(def-sop skill-pack-consumer-vernacular-passed
  (context
    (target "handoff-reader")
    (optimization "immutable-gate-close-record")
    (outcome PASS)
    (closed 2026-07-30)
    (supersedes handoff/SKILL-PACK-CONSUMER-VERNACULAR-OPEN.md))

  <central_idea>
  (center-of-gravity
    (invariant "Installed Product-Spine and Values packs ship AGENTS.fragment assets, durable surface-promote / vernacular protocols, and dry-run-default promote_context.py so a consumer can lift CONTEXT.product.md into root CONTEXT.md without silent overwrite.")))
  </central_idea>

  (protocol-0-shipped
    (monorepo
      .cursor/skills/product-spine/assets/AGENTS.fragment.md
      .cursor/skills/value/assets/AGENTS.fragment.md
      .cursor/skills/value/scripts/promote_context.py
      skills/ mirrors digest-matched)
    (protocols
      "surface-promote in value SKILL.md"
      "protocol-4-vernacular in product-spine SKILL.md (seed path + BMG/lean gap with exact next move)"
      "CONTEXT.product.md in claim must-read-if-present")
    (docs docs/for-your-repo.md)
    (github
      (Product-Spine main 360af16)
      (Values master e721eb8)))

  (protocol-1-evidence
    (pytest "python -m pytest tests/test_product_spine_skill.py tests/test_value_skill_package.py tests/test_value_skill_scripts.py -q — 57 passed")
    (dry-run-default "omit write flags, or pass --dry-run; --dry-run wins over --apply/--agents")
    (apply-gated "--apply merges new terms only")
    (agents-gated "--agents is a separate explicit write to AGENTS.md")
    (dedupe "same provisional term name keeps the first draft only"))

  (protocol-2-scope-closed
    (in-v1 "Values seed + promote lever + spine cue when BMG/lean have no seed")
    (out-of-v1 "BMG/lean CONTEXT.product emitters — not an open gate; reopen only if the spine cue fails in real walks")
    (staging ".tmp-product-spine-ship/ already gitignored — local only, not unfinished work")
    (next none)))
