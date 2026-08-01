(def-sop brand-identity-promote-spine-open
  (context
    (target "fresh-session-agent")
    (optimization "promote-brand-identity-wire-product-spine-retest-then-thermos")
    (outcome SUPERSEDED-BY-PASSED)
    (closed 2026-08-01)
    (passed-record handoff/BRAND-IDENTITY-PROMOTE-SPINE-PASSED.md)
    (opened 2026-08-01)
    (paste-block handoff/NEW-CHAT-PROMPT-BRAND-IDENTITY-PROMOTE-SPINE.md)
    (prior-chat "scripted-skill-from-doc Designing Brand Identity suite → draft + thermos fixes; promote never ran"))

  <central_idea>
  (center-of-gravity
    (invariant "brand-identity is finished as a draft under tools/drafts/skills/brand-identity/ only. It is not a live Cursor skill until promote. Next session owns promote → product-spine wire (teams-like optional brand phase) → retest wired siblings → optional thermos of .cursor/skills excluding scripted-skill-from-doc, story-generation-prompt, and verify-value.")))

  (protocol-0-where-things-are
    (draft "tools/drafts/skills/brand-identity/ — SKILL.md, atoms, scripts, thermos fixes applied")
    (live-missing ".cursor/skills/brand-identity/ — DOES NOT EXIST; /brand-identity will not appear")
    (ship-missing "skills/brand-identity/ — optional --also-skills")
    (source-suite "docs/designing-brand-identity-prompt-suite.md")
    (compile-fix-already-on-master "extract_fenced_block in .cursor/skills/scripted-skill-from-doc/scripts/compile.py — nested ``` inside ```markdown")
    (session-runtime-template "scripted-skill-from-doc/assets/session-runtime/ — authoring cookie only; NOT part of Product-Spine npx pack")
    (confusion "thermos hit the draft tree; human looked for live skill and found nothing"))

  (protocol-1-already-done-do-not-redo
    (suite-scaffold-expand "curriculum 19 atoms; audit_dag both ok; smoke ok")
    (thermos-functional-fixes
      "express init parks on spine S04"
      "ready_atoms requires prior module completed|bypassed for all atoms"
      "can_accept refuses unschedulable focus"
      "resolve_repo_root walks tools/drafts/skills → repo root"
      "milestone Unknowns scoped by source_atom module"
      "Values CLI strings scrubbed; voice slimmed; template synced")
    (tests "tests/test_brand_identity_thermos_fixes.py + compile/gate-ux suite passed when last run")
    (not-done "promote; product-spine brand phase; skill-journey/AGENTS mentions; live /brand-identity; post-promote thermos"))

  (protocol-2-ordered-walk
    1 "Re-audit draft: python .cursor/skills/scripted-skill-from-doc/scripts/audit_dag.py tools/drafts/skills/brand-identity --mode both; smoke.py same path"
    2 "Human consent already implied by this handoff — promote: python .cursor/skills/scripted-skill-from-doc/scripts/promote.py tools/drafts/skills/brand-identity (add --also-skills if ship mirror wanted)"
    3 "Wire product-spine like teams: optional brand phase + brand-intent; done-enough = brand-strategist gate or brand-strategist.md on disk; bounce after brand-strategist; claim optional notes; update .cursor/skills/product-spine/SKILL.md + references/path.md; mirror skills/product-spine/ if digest-matched"
    4 "Update docs/skill-journey.md + AGENTS.md rows for brand-identity sibling"
    5 "Retest: pytest brand thermos + compile tests; smoke live .cursor/skills/brand-identity; cold guide-turn checks that /product-spine can route brand-intent → /brand-identity and return cue"
    6 "Optional thermos on .cursor/skills after wire — EXCLUDE scripted-skill-from-doc, story-generation-prompt, verify-value (not spine-wired grilling siblings). INCLUDE product-spine, brand-identity, value, bmg, teams, lean-mvp")

  (protocol-3-spine-wire-spec
    (pattern "copy teams optional-leg pattern — not a required gate before mvp")
    (session "workproduct/brand-identity/<slug>/session.json")
    (brand-intent "logo, brand identity, brand brief, visual identity, Wheeler, Designing Brand Identity, mark topology, brand guidelines, STEPPS touchpoints, brand governance")
    (brand-ready "brand-strategist module_outcome completed or bypassed — or workproduct/brand-identity/<slug>/brand-strategist.md on disk")
    (bounce "brand-identity SKILL.md after-brand-strategist-gate already names /product-spine")
    (claim-optional "optional-brand-if-present milestone md files under same slug")
    (forbidden 'require-brand-before-mvp 'auto-divert-mid-value-or-bmg-without-brand-intent))

  (protocol-4-success
    (live-skill ".cursor/skills/brand-identity/SKILL.md exists; /brand-identity loadable")
    (spine "product-spine lists brand-identity sibling; brand phase + intent + done-enough; guide-turn can emit /brand-identity")
    (evidence "commands + paths named in PASSED close")
    (close-as "handoff/BRAND-IDENTITY-PROMOTE-SPINE-PASSED.md or FAILED with one blocker"))

  (protocol-5-next-owner
    (next "fresh session: paste NEW-CHAT-PROMPT-BRAND-IDENTITY-PROMOTE-SPINE.md; promote; wire; retest; optional scoped thermos")))
