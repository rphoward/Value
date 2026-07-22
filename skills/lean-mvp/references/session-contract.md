(def-ref session-contract
  (linked-from protocol-1 protocol-3 protocol-4)

  (section canonical-fields
    (session-root "workproduct/lean-mvp/<project-slug>/")
    (canonical-file "session.json")
    (schema assets/session.schema.json)
    (atoms-index assets/atoms.json)
    (knowledge-base assets/knowledge-base.json)
    (value-bridge assets/value-bridge-map.json)
    (required-top-level
      schema_version
      project
      position
      ledger
      answers
      evidence
      assumptions
      decisions
      unknowns
      artifacts)
    (optional-top-level pacing_mode value_import)
    (project-fields slug name created_at updated_at)
    (module-enum customer-context underserved-needs mvp-scope ux-prototype metrics)
    (position-fields module atom_id status))

  (section missing-session-creation
    (ask-first "what the user is working on — display name only; derive slug silently from name")
    (wait-for "explicit consent before creating session.json")
    (init-command "scripts/init_session.py --name <display-name> [--slug <slug>]")
    (init-root "defaults to <repo>/workproduct/lean-mvp when skill is under the repo — not cwd under the skill tree")
    (after-init "run scripts/import_value_context.py <session-path> when value session exists for same slug")
    (forbidden 'ask-user-for-slug 'invent-prior-answers))

  (section evidence-kinds
    (fact "supplied by the user or observed in evidence")
    (inference "reasoned from facts; labeled as inference")
    (hypothesis "unvalidated statement that requires a test")
    (decision "explicit choice with reason")
    (unknown "required information not yet established"))

  (section answer-record
    (shape atom_id answer kind accepted_at)
    (optional provenance source_atom reopen conflict_note)
    (provenance-value-import "answer copied from value skill; do not re-ask unless user reopens"))

  (section gate-pass
    (canonical-phrase "pass <module> gate — see CANONICAL_GATE_PASS in scripts/_session/constants.py")
    (cli "scripts/accept_answer.py --atom-id <gate> --answer <phrase-or-reason> --kind decision --gate-pending")
    (autofill "lean-mvp synthesizes the decisions[] row and holds gate_pending when --gate-pending is set, or when --answer matches the canonical phrase — no --records sidecar required for the happy path")
    (sidecar-optional "scripts/accept_answer.py --records path.json still appends evidence assumptions decisions unknowns artifacts when needed")
    (milestone "scripts/write_milestone.py --module <module> after gate_pending + pass decision")
    (forbidden-stay "--stay is refused on gate atoms; leave the gate unanswered to pause, or pass then write the milestone")
    (status-values gate_pending "final atom accepted; milestone write due"))

  (section scripts-silent
    (status "scripts/status.py — default brief one-liner; --brief is a no-op alias; --operator full ledger; --sections strip")
    (run "status, next_question, accept_answer, import_value_context — parse JSON internally")
    (never "quote script stdout verbatim to the user unless user asks for import details")))
