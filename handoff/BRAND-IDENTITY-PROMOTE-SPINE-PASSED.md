(def-sop brand-identity-promote-spine-passed
  (context
    (target "fresh-session-agent")
    (optimization "brand-identity-live-and-product-spine-routes-brand-intent")
    (outcome PASS)
    (closed 2026-08-01)
    (supersedes handoff/BRAND-IDENTITY-PROMOTE-SPINE-OPEN.md)
    (paste-block handoff/NEW-CHAT-PROMPT-BRAND-IDENTITY-PROMOTE-SPINE.md))

  <central_idea>
  (center-of-gravity
    (invariant "brand-identity is promoted under .cursor/skills/brand-identity/ (ship mirror skills/brand-identity/). Product-spine lists the sibling, optional brand phase, brand-intent, brand-ready = brand-strategist gate or brand-strategist.md, claim optional brand milestones, and bounce cue /product-spine. Retest passed.")))

  (protocol-0-evidence
    (promote "python .cursor/skills/scripted-skill-from-doc/scripts/promote.py tools/drafts/skills/brand-identity --also-skills → .cursor/skills/brand-identity + skills/brand-identity")
    (draft-preflight "audit_dag --mode both ok; smoke.py ok on tools/drafts/skills/brand-identity")
    (live-smoke "smoke.py + audit_dag --mode both ok on .cursor/skills/brand-identity")
    (pytest "python -m pytest tests/test_brand_identity_thermos_fixes.py tests/test_prompt_suite_compile.py tests/test_prompt_suite_compile_gate_ux.py tests/test_product_spine_skill.py -q → 22+ compile/gate cases green; product-spine 22 passed including brand phase contract")
    (spine-spot-check "path.md example-brand-fragment: brand-intent → /brand-identity → Come back when brand-strategist + /product-spine; SKILL.md optional-brand-if-present + brand-ready")
    (docs "docs/skill-journey.md §2c Brand; AGENTS.md rows for .cursor/skills/brand-identity and skills/brand-identity")
    (thermos "RAN scoped — high: thermos tests retargeted to live skill; Values dead paths stripped from brand render/voice; spine optional-leg table rewrite deferred as accepted debt; pack-publish of spine alone still blocked until brand ships")
    (pytest "python -m pytest tests/test_brand_identity_thermos_fixes.py tests/test_product_spine_skill.py -q → 22 passed after thermos follow-ups"))

  (protocol-1-deliverables
    (live-skill .cursor/skills/brand-identity/SKILL.md)
    (ship-mirror skills/brand-identity/)
    (spine-wire
      ".cursor/skills/product-spine/SKILL.md"
      ".cursor/skills/product-spine/references/path.md"
      ".cursor/skills/product-spine/assets/AGENTS.fragment.md"
      "skills/product-spine/ digest-synced"))

  (protocol-2-next-or-none
    (next "none for this gate")
    (optional "scoped thermos on .cursor/skills/{product-spine,brand-identity,value,bmg,teams,lean-mvp}; separate Brand Identity npx pack when human asks")))
