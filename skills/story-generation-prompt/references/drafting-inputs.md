(def-ref drafting-inputs
  (linked-from protocol-1)

  (section what-drafting-means
    (definition "Drafting is writing the story sentence when the user does not have one yet — only evidence.")
    (note "At MS05 the operator usually holds Kano output and interview notes, not a sentence. The sentence can only be as honest as the input it came from, so rank the input before writing.")
    (order "so-that first, then want, then persona — benefit sets the ceiling, and the other two clauses have to fit under it."))

  (section input-yield-ranking
    (rank-1 observed-workaround "What the person already built or does by hand to cope. Highest yield: the workaround names the outcome, and the effort spent on it proves the cost is real.")
    (rank-2 verbatim-complaint-with-situation "A quoted complaint that says when it happened. The situation gives you the moment for the persona clause; the wording gives you the want clause.")
    (rank-3 jtbd-switch-moment "The account of the day someone switched tools or gave up. Names the trigger, the old way, and the new way in one telling.")
    (rank-4 tickets-and-search-logs "Support tickets and in-product search terms. Real language, but the situation is usually stripped out — ask for it before writing.")
    (rank-5 kano-plus-competitor-column "Kano categories set against what competitors already cover. Good for choosing which story to write next; too coarse to write the sentence from."))

  (section inputs-that-fail
    (feature-names
      (how-it-fails "A feature name in the input lands in the want clause, so the story fixes the implementation instead of the outcome.")
      (fix "Ask what the person would be able to do once the feature exists, and put that in the want clause."))
    (demographic-personas
      (how-it-fails "Age, role, and company size produce \"as a user\" — no moment, no pressure, no way to test the benefit.")
      (fix "Ask which situation the person is in when the need shows up, and name the persona from that situation."))
    (survey-scores
      (how-it-fails "A satisfaction score is a number with no observable outcome attached, so the T letter has nothing to hang on.")
      (fix "Ask what the respondent had just done before answering, and draft from that.")))

  (section three-ingredient-rule
    (actor "A specific actor in a specific moment.")
    (current-behaviour "What that actor currently does instead.")
    (cost "An observable cost of doing it that way — time, rework, an abandoned attempt, money.")
    (check "All three present before any sentence is written.")
    (on-missing "Ask one question for the missing ingredient and wait.")
    (sibling-workproduct "When a value slug is known, read workproduct/value-proposition/<slug>/customer-profile.md, value-map.md, and north-star-blurb.md if present before asking the human to paste — those files are the intake.")
    (forbidden "Filling an ingredient from imagination to complete the form.")
    (forbidden "Asking the human to re-paste profile, map, or north-star when those files already exist on disk."))

  (section negotiable-test
    (procedure "Swap the implementation you have in mind for a different one, then read the want clause again.")
    (pass "The sentence still makes sense, so the outcome is what is fixed and the implementation stays open.")
    (fail "The sentence collapses, so the implementation is sitting in the want clause — rewrite it as the outcome.")
    (example-fail "I want the repo run through FFmpeg")
    (example-pass "I want a short overview a peer can watch before opening the repo")))
