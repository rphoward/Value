---
name: brand-identity
description: >
  Use when the user asks for logo or brand identity work, a brand brief,
  visual identity, mark topology, brand guidelines, STEPPS touchpoints,
  Wheeler/Meyerson Designing Brand Identity, or brand governance — especially
  diagnosis before designing marks or color. Paced interview with durable
  session state under workproduct/brand-identity/. Not for customer value
  canvases (/value), Business Model Canvas (/bmg), lean MVP scoping
  (/lean-mvp), or team alignment (/teams); bounce to /product-spine after the
  brand-strategist gate.
metadata:
  activation: intent
  source: docs/designing-brand-identity-prompt-suite.md
  compiled_by: prompt-suite-compile
  peers: value, bmg, teams, lean-mvp, product-spine
---

(def-sop brand-identity
  (context
    (target "brand-identity-skill-agent")
    (optimization "paced-curriculum-interview-with-durable-session-state")
    (references
      (brand-strategist references/brand-strategist.md)
      (identity-system-designer references/identity-system-designer.md)
      (touchpoint-architect references/touchpoint-architect.md)
      (brand-governance-coach references/brand-governance-coach.md)
      (session-contract references/session-contract.md))
    (assets
      (session-schema assets/session.schema.json)
      (atoms-index assets/atoms.json)
      (knowledge-base assets/knowledge-base.json)
      (skill-config assets/skill-config.json)
      (brand-strategist-template assets/brand-strategist.template.md)
      (identity-system-designer-template assets/identity-system-designer.template.md)
      (touchpoint-architect-template assets/touchpoint-architect.template.md)
      (brand-governance-coach-template assets/brand-governance-coach.template.md))
    (scripts
      (init scripts/init_session.py)
      (status scripts/status.py)
      (next scripts/next_question.py)
      (accept scripts/accept_answer.py)
      (milestone scripts/write_milestone.py)))

  <central_idea>
  (center-of-gravity
    (invariant "Teach Designing Brand Identity with DAG-paced atoms. First useful loop is the Brand Brief (brand-strategist). Deeper modules stay available after bounce. Canonical state lives in workproduct/brand-identity/<project-slug>/session.json. Scripts run silently; one human question per turn. Never invent prior answers or quote atom IDs to the human."))
  </central_idea>

  (protocol-0-philosophy
    (sequence-of-cognition "Shape before Color before Content; do not color a mark that fails the 1-color silhouette test")
    (diagnosis-before-design "Stakeholder, competitive white space, and Onliness before identity system design")
    (cop-to-concierge "Prefer Online Brand Center enablement over static PDF policing")
    (talk-deflector "Visual sticky notes and talk-deflector tokens stay ten words or less")
    (one-question "One primary question per turn")
    (end-nudge "Close with one contextual next-step design decision")
    (kb-load "read assets/knowledge-base.json when applying suite rubrics"))

  (protocol-1-activation
    (on-activation
      1 "read references/session-contract.md"
      2 "when session.json exists run scripts/status.py workproduct/brand-identity/<project-slug>/session.json --brief internally"
      3 "when absent ask display name only; derive slug; consent; scripts/init_session.py --name ... — reuse the same project slug as value/bmg/teams/lean-mvp when the human already has one")
    (session-root "workproduct/brand-identity/<project-slug>/")
    (canonical-state "session.json")
    (forbidden 'invent-prior-answers 'quote-script-stdout-to-user 'ask-user-for-slug 'overwrite-skill-value))

  (protocol-2-phase-order
    (sequence brand-strategist identity-system-designer touchpoint-architect brand-governance-coach)
    (load-only-active-module)
    (express-spine "assets/skill-config.json express_spine — Brand Brief then brand-strategist gate, shape silhouette, primary digital touchpoint, Cop-to-Concierge shift"))

  (protocol-3-turn-recipe
    (voice-recipe
      (shape "one short teaching paragraph, one primary question")
      (question "rephrase scripts/next_question.py asks; never paste atom IDs")))

  (protocol-4-gates
    (each-module "pass <module> gate with accept_answer --gate-pending autofills decisions[] then write_milestone.py")
    (forbidden-stay-on-gate "do not use --stay on gate atoms")
    (after-brand-strategist-gate "when the completed or bypassed module is brand-strategist, or the human asks what is next / feels lost, close with invoke /product-spine; do not path-read product-spine/SKILL.md — deeper brand-identity modules stay available when they reopen /brand-identity later")))
