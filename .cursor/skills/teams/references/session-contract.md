(def-ref session-contract
  (linked-from protocol-1 protocol-3)

  (section canonical-fields
    (session-root "workproduct/teams/<project-slug>/")
    (canonical-file "session.json")
    (schema assets/session.schema.json)
    (atoms-index assets/atoms.json)
    (skill-config assets/skill-config.json))

  (section missing-session-creation
    (ask-first "what the user is working on — display name only")
    (wait-for "explicit consent before creating session.json")
    (init-command "scripts/init_session.py --name <display-name>"))

  (section scripts-silent
    (run "status --brief, next_question, accept_answer — parse JSON internally")
    (never "quote script stdout verbatim to the user"))

  (section gate-accept
    (gate-pending "accept_answer.py --gate-pending on gate atoms autofills decisions[] with canonical pass text")
    (refuse-stay "--stay is refused on gate atoms; leave unanswered or pass with --gate-pending")
    (bulk "accept_bulk refuses gate atoms; use accept_answer --gate-pending")))
