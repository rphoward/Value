(def-sop journey-ux-test-expansion-open
  (context
    (target "fresh-session-agent")
    (optimization "write-plan-only-for-end-user-ux-coverage-across-spine-and-siblings")
    (outcome OPEN)
    (opened 2026-08-01)
    (note "SUPERSEDED 2026-08-01 by handoff/JOURNEY-UX-TEST-EXPANSION-PASSED.md — plan accepted; execute closed PASS at JOURNEY-UX-TEST-EXPANSION-EXECUTE-PASSED.md")
    (paste-block handoff/NEW-CHAT-PROMPT-JOURNEY-UX-TEST-EXPANSION.md)
    (prior "Maya happy FAIL compressed walk; Kai unhappy PASS coaching stress; brand-identity + spine wire PASSED; Product-Spine pack e7a0a56 ships brand"))

  <central_idea>
  (center-of-gravity
    (invariant "End-user experience across /product-spine and every grilling sibling must be covered by an intentional mix of package/DAG/script tests and honest persona walks (happy + unhappy). Next session owns a written plan only — not implementing the suite until the human accepts the plan. Never treat compressed bulk-accept as a happy-path PASS (Maya lesson).")))

  (protocol-0-why-now
    (skills-grew "value, bmg, teams, brand-identity, lean-mvp, story-generation-prompt, product-spine — pack + monorepo live")
    (gap "automated tests are mostly package/DAG/script contracts; persona UX walks stopped at value→lean→claim (Maya FAIL method; Kai PASS). Optional legs teams + brand-identity + bmg + cold-restart + dual-intent routing lack a single coverage map")
    (goal "plan how to expand tests so a vibecoder’s path (guide-turn → sibling grill → bounce → claim) stays good across all siblings"))

  (protocol-1-inventory-do-not-reinvent
    (automated-tests-under-tests/
      "test_product_spine_skill.py — package contract / brand phase needles / ship digests"
      "test_value_skill_*.py + test_value_session_integrity.py — value package/DAG/scripts"
      "test_lean_mvp_*.py — lean package, gate UX, coaching, value import"
      "test_story_generation_prompt_skill.py + story scenario suite (PASSED)"
      "test_brand_identity_thermos_fixes.py — live brand runtime regressions"
      "test_prompt_suite_compile*.py — compiler (authoring; not end-user journey)"
      "test_skill_session_isolation.py")
    (persona-walks-and-gates
      (maya-happy "FAILED — compressed bulk-accept misdeclared PASS; see PRODUCT-SPINE-MAYA-HAPPY-PATH-FAILED.md; optional true one-atom retry later")
      (kai-unhappy "PASSED — coaching stress + express compression as stimulus; cashclaw evidence")
      (ux-mock "PASSED — guide-turn + lean bounce-back")
      (cold-restart "OPEN — PRODUCT-SPINE-COLD-RESTART-OPEN.md still open; fold into plan or keep separate")
      (story-scenarios "PASSED — S01–S08"))
    (evidence-slugs
      (shiftswap "Maya — leave as historical; do not revive PASSED")
      (cashclaw "Kai — leave as historical stress evidence")
      (value-design "local dogfood — leave alone unless plan says otherwise"))
    (ship-pack "https://github.com/rphoward/Product-Spine @ e7a0a56 — seven skills including brand-identity"))

  (protocol-2-coverage-dimensions-plan-must-name
    (siblings "value, bmg, teams, brand-identity, lean-mvp, story-generation-prompt")
    (spine-behaviors "guide-turn shape; intent routing; done-enough; bounce /product-spine; claim loads notes; optional-leg not required before mvp")
    (path-kinds
      (happy "honest one-question pacing; gates with real answers; claim exit")
      (unhappy "skim/compress/wrong-slash/early-claim/dual-intent; express as stimulus not silent PASS")
      (optional-legs "teams brand-intent and team-friction without inventing legs; brand + teams dual-intent precedence")
      (cold-reentry "progress-so-far in you-are-here; readiness from milestones not status brief"))
    (test-kinds-to-separate
      (automated "pytest package/DAG/script/smoke — fast regression")
      (dogfood-walk "chat persona with decision-trail TSV — proves coaching voice")
      (forbidden "bulk-accept drivers counted as happy-path PASS")))

  (protocol-3-next-session-deliverable
    (owns "write a plan only")
    (plan-home ".cursor/plans/ — or path human names; follow writing-plans / repo plan habits")
    (plan-must-include
      1 "coverage matrix: sibling × path-kind × test-kind (what exists vs missing)"
      2 "ordered build slices (smallest useful first — recommend spine routing + brand/teams optional legs before full Maya retry)"
      3 "persona/slug policy (reuse vs new; wipe rules)"
      4 "pass/fail rules learned from Maya FAIL + Kai PASS"
      5 "explicit out-of-scope (compiler authoring, shared-runtime rewrite, solo Brand Identity repo)"
      6 "verification commands per slice")
    (forbidden-this-session 'implementing-full-suite 'closing-PASSED-without-plan-acceptance 'reviving-Maya-PASSED)
    (after-plan "stop; wait for human to accept or edit the plan before implementation"))

  (protocol-4-success-for-this-gate
    (outcome "plan file exists and is accepted by human — then close this gate PASSED with path to plan; or FAILED with one blocker")
    (close-as "handoff/JOURNEY-UX-TEST-EXPANSION-PASSED.md or FAILED")
    (implementation "separate gate or same plan’s execute phase — only after human says go"))

  (protocol-5-next-owner
    (next "fresh session: paste NEW-CHAT-PROMPT-JOURNEY-UX-TEST-EXPANSION.md; inventory tests + prior walks; write plan; halt for acceptance")))
