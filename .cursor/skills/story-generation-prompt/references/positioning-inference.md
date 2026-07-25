(def-ref positioning-inference
  (linked-from protocol-6 protocol-7)

  (section why-this-exists
    (problem "A codebase states mechanism, not positioning. README files written by coders say what to install and how to run it. They rarely say who the tool is for, which situation it belongs in, or who should skip it.")
    (bad-outcome "A recon pass that asks a codebase for audience and when-to-skip returns \"not in sources\" for every row the overview actually needs, and the operator is back to writing marketing copy from memory.")
    (resolution "Split the ledger in two. Mechanism facts come from sources and stay facts. Positioning is derived here, carries a label, and needs operator confirmation before it may enter produced copy.")
    (note "This is the same discipline the value skill applies with its evidence kinds — fact, inference, hypothesis, decision, unknown — applied to a repo instead of an interview."))

  (section labels
    (fact "Stated in a source. Cite the filename.")
    (inference "Derived from mechanism the sources do show. State the mechanism it rests on in the same line.")
    (hypothesis "Plausible and useful, but the mechanism does not settle it. Needs the operator.")
    (unknown "No mechanism points either way. Leave it and say so.")
    (forbidden "An unlabeled positioning line. Without a label the reader cannot tell an install command from a guess."))

  (section derivation-moves
    (note "Each move reads mechanism the sources do contain and produces one positioning line with its label.")
    (install-preconditions "Read the install and run instructions. Whoever already has that toolchain, editor, or runtime is the audience precondition. Someone who does not is a skip candidate.")
    (integration-points "Read imports, adapters, config keys, and hook points. They name the workflow the tool sits inside, which is the situation clause of the persona.")
    (defaults-and-opinions "Read defaults, strict modes, and refusals. An opinionated default is the author asserting that the old way was a problem; that assertion is the problem statement in solution-space words.")
    (absence-as-skip "Read what the code will not do — required dependencies, unsupported platforms, no onboarding path. When-to-skip is almost never written down; it is the shadow of what the code requires.")
    (readme-claims "A claim in the README is a fact about what the author intended, not proof that users get it. Label it fact-of-claim, and do not promote it to validated benefit.")
    (test-and-fixture-names "Test names and fixtures often describe the failure the author kept hitting. That failure is candidate evidence for the cost clause."))

  (section lean-mvp-frames
    (source "assets/knowledge-base.json in the lean-mvp skill; load the named entry rather than paraphrasing from memory.")
    (space-pen-mirage "Separate What from How before writing the problem line. Mechanism vocabulary — hooks, autoload, rules layers — is How. The problem line has to land in the operator's world.")
    (pmf-pyramid "pmf_pyramid_hierarchy splits problem space (target customer, underserved needs) from solution space (value proposition, feature set, UX). A codebase gives you solution space almost entirely; every problem-space row you produce here is inference or hypothesis, never fact.")
    (kano "kano_model_categories separates must-haves from delighters. Use it to tell the core problem from the nice extra, so the overview leads with the must-have rather than the most fun feature.")
    (earlyvangelist "earlyvangelist_ladder asks whether the person has the problem, is aware of it, is searching, has cobbled a workaround, and has budget. The workaround rung is the strongest one a repo can speak to — code that replaces a hand-rolled script names the workaround it displaces.")
    (adoption-lifecycle "adoption_lifecycle says to name one segment as a hypothesis until adoption evidence confirms it. Audience rows derived here are hypotheses by that rule."))

  (section lean-mvp-owns-these-questions
    (principle "Nearly every positioning row already belongs to a lean-mvp atom. This skill derives a draft reading so the story sentence is not blocked; it does not run the interview that settles the row.")
    (audience-of-this-section "Agent-internal. The map below tells you where a row gets settled so you do not re-run that interview here. It is not a script to read out.")
    (ownership
      (audience "C01 segment, C02 persona archetype and quote, C04 adoption lifecycle position")
      (problem "U01 and U02 benefits in action-verb form, U03 one-why laddering")
      (which-problem-leads "U04 importance and satisfaction, U05 opportunity score")
      (must-have-core "MS02 must-have table stakes; MS04 decides whether a delighter belongs in v1")
      (workaround-displaced "MS01 competitors and manual workarounds; C05 earlyvangelist workaround rung")
      (when-to-skip "No atom asks this directly. MS03 offense versus defense is the nearest, since ceding a benefit to a competitor is a skip signal. Say so rather than implying an atom owns it."))
    (session-truth "lean-mvp records answers in its own session.json through accept_answer. This skill writes nothing there and never auto-accepts an atom.")
    (forbidden "Re-running the customer-context or underserved-needs interview here."))

  (section voice
    (why "The operator is thinking about their product, not about a curriculum. Atom codes, protocol numbers, and words like ledger or table pull them out of that and into tooling talk. The sibling skills already forbid this — value lists atom IDs under forbidden-user-facing, and lean-mvp says to ground a turn in priors without naming atom ids. This skill holds the same line.")
    (say-instead
      (defer "we can pin down who this is for when you are back in the session")
      (confirmed "you have said this yourself, so the overview can state it")
      (derived "this is read off how the project installs and what it refuses to do — correct it if it is wrong"))
    (forbidden "Speaking an atom code — C01, U05, MS02, and the rest — to the operator."
               "Naming protocols, references, or file paths in the flow of a working turn."
               "Curriculum vocabulary where a plain sentence works."))

  (section confirmation-loop
    (emit "A short table the operator can scan: what the reading is, how sure it is, and what it rests on. Plain column headers; no atom column and no code in any cell.")
    (ask "Show it once. Ask only for what the sentence being written needs now, and offer the rest in one plain sentence — the session will come back to them later.")
    (on-confirm "A confirmed row becomes grounding with the operator as its source. Record that in the Grounding row of the story card.")
    (on-correct "Take the operator wording over the derived wording. They know the market; the code only knows itself.")
    (on-defer "A row the operator would rather settle in the session stays labeled and stays out of the producer prompt. That is a normal outcome, not a gap to nag about.")
    (on-return "When the operator comes back with a settled answer for a row, treat it as confirmed and replace the derived wording.")
    (forbidden "Sending an unconfirmed inference into the generation prompt as though it were a fact from sources."
               "Holding the story sentence hostage until every row is confirmed."))

  (section what-still-comes-from-the-operator
    (note "Inference closes the positioning gap. It does not close the observation gap.")
    (actor-and-moment "Which person, in which moment, is under pressure.")
    (current-behaviour "What they do instead today.")
    (cost "What that costs them — the reply that never came, the re-post, the abandoned attempt.")
    (rule "Derive positioning; ask for observation. A repo cannot tell you that peers watched the video and still could not say what it was for.")))
