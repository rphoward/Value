---
name: teams
description: >
  Use when the user asks for team alignment, Team Alignment Map / TAM,
  joint objectives and commitments, team contract IN/OUT norms, psychological
  safety, Fact Finder, or conflict repair on a working team — especially
  friction on a product or repo team that is hurting delivery. Paced interview
  with durable session state under workproduct/teams/. Not for customer value
  canvases (/value), Business Model Canvas (/bmg), or lean MVP scoping
  (/lean-mvp); bounce to /product-spine after the tam-planner gate.
metadata:
  activation: intent
  source: docs/High-Impact Tools Suite.md
  compiled_by: prompt-suite-compile
  peers: value, bmg, lean-mvp, product-spine
---

(def-sop teams
  (context
    (target "teams-skill-agent")
    (optimization "paced-curriculum-interview-with-durable-session-state")
    (references
      (tam-planner references/tam-planner.md)
      (tam-assessor references/tam-assessor.md)
      (team-contract-architect references/team-contract-architect.md)
      (psych-safety-conflict-resolver references/psych-safety-conflict-resolver.md)
      (session-contract references/session-contract.md))
    (assets
      (session-schema assets/session.schema.json)
      (atoms-index assets/atoms.json)
      (knowledge-base assets/knowledge-base.json)
      (skill-config assets/skill-config.json))
    (scripts
      (init scripts/init_session.py)
      (status scripts/status.py)
      (next scripts/next_question.py)
      (accept scripts/accept_answer.py)
      (milestone scripts/write_milestone.py)))

  <central_idea>
  (center-of-gravity
    (invariant "Teach High-Impact Tools for Teams with DAG-paced atoms. First useful loop is the Team Alignment Map (tam-planner). Deeper modules stay available after bounce. Canonical state lives in workproduct/teams/<project-slug>/session.json. Scripts run silently; one human question per turn. Never invent prior answers or quote atom IDs to the human."))
  </central_idea>

  (protocol-0-philosophy
    (one-question "One primary question per turn")
    (end-nudge "Close with one contextual next-step design decision")
    (kb-load "read assets/knowledge-base.json when applying suite rubrics")
    (sticky-notes "TAM entries stay ten words or less"))

  (protocol-1-activation
    (on-activation
      1 "read references/session-contract.md"
      2 "when session.json exists run scripts/status.py workproduct/teams/<project-slug>/session.json --brief internally"
      3 "when absent ask display name only; derive slug; consent; scripts/init_session.py --name ... — reuse the same project slug as value/bmg/lean-mvp when the human already has one")
    (session-root "workproduct/teams/<project-slug>/")
    (canonical-state "session.json")
    (forbidden 'invent-prior-answers 'quote-script-stdout-to-user 'ask-user-for-slug 'overwrite-skill-value))

  (protocol-2-phase-order
    (sequence tam-planner tam-assessor team-contract-architect psych-safety-conflict-resolver)
    (load-only-active-module)
    (express-spine "assets/skill-config.json express_spine — mission then tam-planner gate, then later module spines"))

  (protocol-3-turn-recipe
    (voice-recipe
      (shape "one short teaching paragraph, one primary question")
      (question "rephrase scripts/next_question.py asks; never paste atom IDs")))

  (protocol-4-gates
    (each-module "pass <module> gate with accept_answer --gate-pending autofills decisions[] then write_milestone.py")
    (forbidden-stay-on-gate "do not use --stay on gate atoms")
    (after-tam-planner-gate "when the completed or bypassed module is tam-planner, or the human asks what is next / feels lost, close with invoke /product-spine; do not path-read product-spine/SKILL.md — deeper teams modules stay available when they reopen /teams later")))
