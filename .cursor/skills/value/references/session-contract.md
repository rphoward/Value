(def-ref session-contract
  (linked-from protocol-1 protocol-4 protocol-6 protocol-7)

  (section canonical-fields
    (session-root "workproduct/value-proposition/<project-slug>/")
    (canonical-file "session.json")
    (schema assets/session.schema.json)
    (required-top-level
      schema_version
      project
      position
      answers
      evidence
      assumptions
      decisions
      unknowns
      artifacts)
    (project-fields slug name created_at updated_at)
    (position-fields module atom_id status)
    (module-enum profile value-map business-model experiments)
    (status-enum in_progress gate_pending completed bypassed))

  (section missing-session-creation
    (ask-first "project slug and display name only")
    (wait "for the user's project identity answer")
    (ask-consent "one primary question: create workproduct/value-proposition/<project-slug>/session.json?")
    (wait-for "explicit consent before creating session.json")
    (initial-document
      (schema_version "1.0")
      (project
        (slug "confirmed project slug")
        (name "confirmed display name")
        (created_at "current RFC 3339 timestamp")
        (updated_at "same timestamp as created_at"))
      (initial-position profile P01 in_progress)
      (initial-arrays answers evidence assumptions decisions unknowns artifacts :empty t)
      (initial-timestamps created_at updated_at :rfc3339 t :same-value t))
    (write "complete schema-valid session.json immediately after consent")
    (forbidden 'create-before-consent 'ask-curriculum-question-with-project-identity))

  (section evidence-kinds
    (fact "supplied by the user or observed in evidence")
    (inference "reasoned from facts; must be labeled as inference in answer or evidence")
    (hypothesis "unvalidated statement that requires a test")
    (decision "explicit choice with reason recorded")
    (unknown "required information not yet established — never convert to inference"))

  (section answer-record
    (shape
      (atom_id "stable atom identifier from active module reference")
      (answer "accepted text for this atom")
      (kind "one of fact inference hypothesis decision unknown")
      (accepted_at "RFC 3339 timestamp"))
    (project-write "set project.updated_at to accepted_at on every accepted answer")
    (append-only "new acceptance appends; reopening a decision adds a superseding record and notes conflict resolution"))

  (section position-shape
    (module "current curriculum module enum")
    (atom_id "active atom id from the loaded module reference")
    (status
      (in_progress "working the current atom")
      (gate_pending "final atom accepted; milestone artifact write due")
      (completed "module gate artifact written")
      (bypassed "module skipped by explicit bypass decision")))

  (section evidence-records
    (shape claim kind source strength)
    (strength "behavioral commitment rank when applicable; spoken feedback remains weak evidence"))

  (section assumptions
    (shape claim criticality evidence_status source_atom)
    (criticality high medium low)
    (evidence_status supported partial unsupported unknown))

  (section decisions
    (shape decision reason source_atom resulting_module resulting_atom resulting_status)
    (resulting-position resulting_module resulting_atom resulting_status)
    (use "bypass records, conflict resolutions, and explicit tradeoffs"))

  (section unknowns
    (shape question blocking)
    (blocking "true when the unknown blocks the current atom or gate"))

  (section artifacts
    (shape path status)
    (status pending draft final)
    (milestones
      customer-profile.md
      value-map.md
      business-model.md
      experiment-plan.md
      product-design-brief.md
      ux-brief.md))

  (section conflict-handling
    (on-conflict "append a blocking unknown with the conflicting statements; preserve both accepted answers")
    (resolution "append a decision naming the governing statement, reason, source_atom, and resulting position; remove the blocking unknown")
    (forbidden 'silent-overwrite 'advance-without-resolution))

  (section resume-behavior
    (read "session.json and validate against schema")
    (report "last accepted decision in one sentence")
    (ask "current atom only")
    (forbidden 'repeat-completed-atoms 'invent-missing-state))

  (section milestone-writes
    (trigger "module gate_pending after final atom accepted")
    (source "accepted answers and labeled evidence for that module only")
    (brief-prerequisite "all four module gates are completed or explicitly bypassed")
    (product-brief "only from accepted facts, labeled inferences, decisions, unresolved assumptions")
    (ux-brief "only from accepted facts, labeled inferences, decisions, unresolved assumptions")
    (forbidden 'score-without-evidence 'full-canvas-before-atoms))

  (section phase-bypass-record
    (when "user requests a later phase before prerequisites are met")
    (require
      (decision "explicit bypass statement, e.g. bypass value-map gate")
      (reason "why the prerequisite is waived")
      (source_atom "atom id active when bypass was requested")
      (resulting_module "requested target phase")
      (resulting_atom "first atom id in the target module")
      (resulting_status in_progress))
    (position-update "set position.module, position.atom_id, and position.status exactly to the decision's resulting_module, resulting_atom, and resulting_status")
    (forbidden 'silent-phase-jump))

  (section parking-lot
    (capture "premature solutions, orphan features, off-phase ideas")
    (store "assumptions or decisions with source_atom reference")
    (return "active atom after capture")))
