---
name: lean-mvp
description: >
  Use when the user asks to run Dan Olsen's Lean Product Playbook, define a lean
  MVP, prioritize underserved needs, scope MVP features with Kano/INVEST/ROI,
  plan UX prototype tests, or optimize product metrics. Reuses customer evidence
  from the value skill when session files exist. Not for full Strategyzer value
  proposition canvas work or generic implementation planning without MVP framing.
metadata:
  activation: intent
  distribution: monorepo
  pairs_with: value
  source: docs/lean-product-playbook-prompt-suite.md
---

(def-sop lean-mvp
  (context
    (target "lean-mvp-skill-agent")
    (optimization "paced-lean-product-playbook-with-value-bridge-and-durable-session-state")
    (references
      (customer-context references/customer-context.md)
      (underserved-needs references/underserved-needs.md)
      (mvp-scope references/mvp-scope.md)
      (ux-prototype references/ux-prototype.md)
      (metrics references/metrics.md)
      (session-contract references/session-contract.md)
      (value-bridge references/value-bridge.md))
    (assets
      (session-schema assets/session.schema.json)
      (atoms-index assets/atoms.json)
      (knowledge-base assets/knowledge-base.json)
      (atom-coaching assets/atom-coaching.json)
      (value-bridge-map assets/value-bridge-map.json)
      (customer-context-template assets/customer-context.template.md)
      (underserved-needs-template assets/underserved-needs.template.md)
      (mvp-scope-template assets/mvp-scope.template.md)
      (ux-prototype-template assets/ux-prototype.template.md)
      (metrics-template assets/metrics.template.md))
    (scripts
      (init scripts/init_session.py)
      (import-value scripts/import_value_context.py)
      (status scripts/status.py)
      (next scripts/next_question.py)
      (accept scripts/accept_answer.py)
      (milestone scripts/write_milestone.py)))

  <central_idea>
  (center-of-gravity
    (invariant "Climb Dan Olsen's Product-Market Fit Pyramid with DAG-paced atoms. Canonical state lives in workproduct/lean-mvp/<project-slug>/session.json. Import mapped answers from workproduct/value-proposition/<slug>/ when present. Scripts run silently; one human question per turn."))
  </central_idea>

  (protocol-0-philosophy
    (space-pen-mirage "Load visual_grounding_analogies.space_pen_mirage; block solution-space mockups before target customer and underserved needs")
    (outside-in "Flag inside-out feature speculation; push GOOB and follow-me-home observation")
    (olsen-hierarchy "Uptime and quality before UX delighters — load olsen_hierarchy_of_web_needs when scoping")
    (oprah-spock "Qualitative discovery before quantitative optimization")
    (end-nudge "One contextual next-step design decision per turn")
    (value-sibling "value skill owns Strategyzer canvas; lean-mvp owns Olsen playbook — read value artifacts, never write value paths; value may read lean sessions via its own import_lean_context bridge"))

  (protocol-1-activation
    (on-activation
      1 "read references/session-contract.md and references/value-bridge.md"
      2 "when session.json exists run scripts/status.py (default brief; --brief alias ok) then scripts/import_value_context.py <session> internally"
      3 "when absent: missing-session creation; init_session.py; then import_value_context when value session exists")
    (session-root "workproduct/lean-mvp/<project-slug>/")
    (kb-load "read assets/knowledge-base.json for Kano, INVEST, opportunity math, test matrix, LTV/CAC bands")
    (forbidden 'invent-prior-answers 'modify-value-skill-or-values-repo 'quote-script-stdout-to-user))

  (protocol-2-phase-order
    (sequence customer-context underserved-needs mvp-scope ux-prototype metrics)
    (prerequisites
      (customer-context "none — entry module; value import may prefill atoms")
      (underserved-needs "customer-context gate complete or bypass")
      (mvp-scope "underserved-needs gate complete or bypass")
      (ux-prototype "mvp-scope gate complete or bypass")
      (metrics "ux-prototype gate complete or bypass"))
    (load-only-active-module per sequence))

  (protocol-3-turn-recipe
    (voice-recipe
      (shape "one paragraph, one primary question")
      (import-hint "briefly acknowledge value-imported facts without atom IDs")
      (coaching-delivery
        1 "when coaching is null, ask asks alone as today"
        2 "otherwise ground the turn in ok priors without naming atom ids"
        3 "state definition text from coaching.definitions"
        4 "state what a complete answer contains from coaching.complete_when"
        5 "ask asks as the single primary question"
        6 "hold worked_example and common_miss until the human stalls")
      (ms05-story-offer
        "when focus atom is MS05, offer reading .cursor/skills/story-generation-prompt/SKILL.md per references/mvp-scope.md stories-assist — before or with the primary question, not only if the human asks"))
    (scripts-silent
      (run "import_value_context status next_question accept_answer")))

  (protocol-4-gates
    (each-module "pass <module> gate with accept_answer --gate-pending autofills decisions[] then write_milestone.py")
    (forbidden-stay-on-gate "do not use --stay on gate atoms"))
)