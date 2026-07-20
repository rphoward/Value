(def-sop value-gate-presentation-passed
  (context
    (target "handoff-reader")
    (optimization "immutable-gate-close-record")
    (outcome PASS)
    (closed 2026-07-20)
    (session-slug value-design)
    (session-root workproduct/value-proposition/value-design/))

  <central_idea>
  (center-of-gravity
    (invariant "Value-map gate presentation ships Mock C inline stickies with Fit links or Differentiation on ask; comprehension fix is in SKILL orchestration only — map content unchanged."))
  </central_idea>

  (protocol-0-pick
    (winner "Mock C dogfood — inline three stickies; links/diff on ask only")
    (arena-trail handoff/decision-trails/value-gate-presentation.tsv)
    (reference-mock tools/drafts/value-gate-arena/mock-c-dogfood.md)
    (fallback-documented "D+A Gate_Review_Lens — not shipped; promote only if C still dense in practice"))

  (protocol-1-shipped
    (skill-block "value-map-gate-review in skills/value/SKILL.md protocol-3")
    (atom-ref "V08 presentation rules in skills/value/references/value-map.md")
    (contract "one-line pointer in skills/value/references/session-contract.md")
    (tests "test_value_map_gate_presentation_contract in tests/test_value_skill_contracts.py"))

  (protocol-2-evidence
    (pytest "python -m pytest tests/test_value_skill_contracts.py -v -k gate_presentation — passed"))
    (session-scripts "accept_answer.py V08 --gate-pending; write_milestone.py --module value-map on value-design session"))

  (protocol-3-next
    (none "business-model B01 resumes on value-design session")))
