---
name: bmg
description: >
  Use when the user asks to build or audit a Business Model Canvas, work
  Business Model Generation (Osterwalder), inject patterns (Freemium, Long Tail,
  platforms, Unbundling, Open), run block SWOT or Blue Ocean on a canvas, or
  start with classic BMG before value or MVP. Not for lean value-proposition
  grilling alone (use value), not for MVP scoping alone (use lean-mvp), and not
  for generic product requirements without a business-model session.
metadata:
  activation: intent
  source: docs/business-model-generation-prompt-suite.md
  compiled_by: prompt-suite-compile
  peers: value, lean-mvp, product-spine
---

(def-sop bmg
  (context
    (target "bmg-skill-agent")
    (optimization "paced-bmg-teaching-interview-with-durable-session-state")
    (references
      (canvas-mapper references/canvas-mapper.md)
      (pattern-innovator references/pattern-innovator.md)
      (strategy-evaluator references/strategy-evaluator.md)
      (ambidextrous-execution-designer references/ambidextrous-execution-designer.md)
      (session-contract references/session-contract.md))
    (assets
      (session-schema assets/session.schema.json)
      (atoms-index assets/atoms.json)
      (knowledge-base assets/knowledge-base.json)
      (skill-config assets/skill-config.json)
      (canvas-mapper-template assets/canvas-mapper.template.md)
      (pattern-innovator-template assets/pattern-innovator.template.md)
      (strategy-evaluator-template assets/strategy-evaluator.template.md)
      (ambidextrous-template assets/ambidextrous-execution-designer.template.md))
    (scripts
      (init scripts/init_session.py)
      (status scripts/status.py)
      (next scripts/next_question.py)
      (accept scripts/accept_answer.py)
      (gaps scripts/gaps.py)
      (bulk scripts/accept_bulk.py)
      (map scripts/map_gaps.py)
      (pacing scripts/set_pacing_mode.py)
      (milestone scripts/write_milestone.py)))

  <central_idea>
  (center-of-gravity
    (invariant "Teach classic Business Model Generation with DAG-paced atoms. Sticky notes stay short. Coffee-style worked examples in knowledge-base teach_aids show how a simple offer fans into many blocks. Canonical state lives in workproduct/bmg/<project-slug>/session.json. Scripts run silently; orchestrator speaks one paragraph and one human question — never atom IDs or script stdout."))
  </central_idea>

  (protocol-0-philosophy
    (visual-grammar "Each canvas item is one sticky note, max ~10 words")
    (teach-simple-first "When a block is abstract, load assets/knowledge-base.json teach_aids.coffee_capsule_example and show that block's sample sticky notes, then ask for this venture's equivalent")
    (right-left-balance "Right canvas is value/emotion (VP CS CR CH R$). Left canvas is logic/efficiency (KP KA KR C$). Flag misalignment before gate")
    (reject-premature-plans "Prefer canvas prototypes over long business plans")
    (peer-skills "Sibling to value and lean-mvp. Entry order is project-dependent: BMG-first when the work is already a business or needs fuller business language; value or MVP-first when it is not. Not every project is a business; every business is a project that may need BMG")
    (one-question "One primary question per turn")
    (end-nudge "Close with one contextual next-step design decision")
    (kb-load "read assets/knowledge-base.json for nine blocks, patterns, Blue Ocean, environment spheres, teach aids"))

  (protocol-1-activation
    (on-activation
      1 "read references/session-contract.md"
      2 "when session.json exists run scripts/status.py workproduct/bmg/<project-slug>/session.json --brief internally"
      3 "when absent ask display name only; derive slug; consent; scripts/init_session.py --name ...")
    (session-root "workproduct/bmg/<project-slug>/")
    (canonical-state "session.json")
    (forbidden 'invent-prior-answers 'quote-script-stdout-to-user 'ask-user-for-slug 'overwrite-skill-value))

  (protocol-2-phase-order
    (sequence canvas-mapper pattern-innovator strategy-evaluator ambidextrous-execution-designer)
    (load-only-active-module)
    (express-spine "assets/skill-config.json express_spine — CS VP Revenue Costs gate, then pattern/strategy/execution spines"))

  (protocol-3-turn-recipe
    (voice-recipe
      (shape "one short teaching paragraph, one primary question")
      (teach "use coffee teach aid only as analogy; never pretend the user's venture is coffee")
      (question "rephrase scripts/next_question.py asks; never paste atom IDs")))

  (protocol-4-gates
    (each-module "pass <module> gate with accept_answer --gate-pending autofills decisions[] then write_milestone.py")
    (forbidden-stay-on-gate "do not use --stay on gate atoms")
    (after-canvas-mapper-gate "when the completed or bypassed module is canvas-mapper, or the human asks what is next / feels lost, close with invoke /product-spine; do not path-read product-spine/SKILL.md")))
