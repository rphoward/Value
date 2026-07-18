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
      (accepted_at "ISO-8601 timestamp"))
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
    (shape claim criticality evidence_status)
    (criticality high medium low)
    (evidence_status supported partial unsupported unknown))

  (section decisions
    (shape decision reason source_atom)
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
    (on-conflict "append conflict note; ask which statement governs")
    (resolution "record governing decision with reason and source_atom")
    (forbidden 'silent-overwrite 'advance-without-resolution))

  (section resume-behavior
    (read "session.json and validate against schema")
    (report "last accepted decision in one sentence")
    (ask "current atom only")
    (forbidden 'repeat-completed-atoms 'invent-missing-state))

  (section milestone-writes
    (trigger "module gate_pending after final atom accepted")
    (source "accepted answers and labeled evidence for that module only")
    (product-brief "only from accepted facts, labeled inferences, decisions, unresolved assumptions")
    (ux-brief "only from accepted facts, labeled inferences, decisions, unresolved assumptions")
    (forbidden 'score-without-evidence 'full-canvas-before-atoms))

  (section phase-bypass-record
    (when "user requests a later phase before prerequisites are met")
    (require
      (decision "explicit bypass statement, e.g. bypass value-map gate")
      (reason "why the prerequisite is waived")
      (source_atom "atom id active when bypass was requested"))
    (position-update "set module and status to bypassed or next allowed atom per orchestrator decision")
    (forbidden 'silent-phase-jump))

  (section parking-lot
    (capture "premature solutions, orphan features, off-phase ideas")
    (store "assumptions or decisions with source_atom reference")
    (return "active atom after capture")))
