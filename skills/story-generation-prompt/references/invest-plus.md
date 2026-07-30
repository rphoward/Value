(def-ref invest-plus
  (linked-from protocol-4)

  (section what-invest-plus-is
    (definition "INVEST-plus is the ordinary INVEST rubric split by what one story sentence can actually answer, with two extra rows a delivery rubric does not carry.")
    (why "INVEST was written to judge backlog items on a team that has a sprint length and a backlog to compare against. Applying it at a validation moment, to a sentence drafted from interview notes, leaves three of the six letters with nothing to read. Marking those three pass is a rubber stamp, and a rubber stamp is worse than an empty cell because it looks like a check.")
    (note "Keep the letters. The lean-mvp gate still asks for INVEST, and the letter-to-word pairs are unchanged."))

  (section checkable-from-this-sentence
    (N "Negotiable — read the want clause. Swap the implementation; if the sentence collapses, N fails.")
    (V "Valuable — read the so-that clause. If the benefit lands on the team rather than the actor, V fails.")
    (T "Testable — read the test hook. If no observation would settle it either way, T fails."))

  (section needs-backlog-and-team
    (I "Independent — depends on what else is in the backlog and what ships before this.")
    (E "Estimable — depends on who is estimating and what that team has built before.")
    (S "Small — depends on sprint length and team capacity.")
    (default-result "not answerable here")
    (when-answerable "The user supplied the backlog, the estimating team, or the sprint length. Name which one you used in the Note column.")
    (when-reasoned-from-scope "No backlog, no team, no sprint, but the scope in front of a solo operator settles the letter honestly. Result is reasoned from scope, and the Note column names the concrete basis it rests on, for example one repo, one brief, one link.")
    (forbidden "Writing pass for I, E, or S from the sentence alone.")
    (forbidden "Writing reasoned from scope without a named basis in the Note column; that letter stays not answerable here."))

  (section extra-rows
    (grounding "Which observation this story came from — the workaround, the quoted complaint, the ticket. A story with an empty Grounding row is a guess wearing story grammar.")
    (kill-signal "What result would drop this story. If no result would drop it, the story is not a bet, and T is weaker than the sentence makes it look."))

  (section reporting
    (row-shape "Letter | Result | Note")
    (results-allowed pass fail "not answerable here" "reasoned from scope")
    (on-fail "State the fail and give one question that would fix it.")
    (on-not-answerable "Name the missing context — backlog, estimating team, or sprint length.")
    (on-reasoned-from-scope "Name the basis in the Note column, for example one repo, one brief, one link. An unnamed basis is not a result; the letter goes back to not answerable here.")
    (forbidden "Collapsing the two blocks back into one flat table.")))
