(def-ref author-matching-technical
  (linked-from register-detection routing technical)

  (section author-matching-technical
    (register technical)
    (description "Tutorial voice, pedagogy, and clarity-first nonfiction. Prefer authors who teach through concrete examples."))

  (section match-criteria
    (priority-order
      (1 "Pedagogical move matches payload SecondaryMovements or CoreThesis explanation style")
      (2 "Author dwells on mechanism, not metaphor, where payload DwellTargets demand precision")
      (3 "Compression targets align with what the author typically abbreviates (history, proofs, digressions)")
      (4 "Reader difficulty matches declared Difficulty spread across candidates")))

  (section per-author-required-fields
    (note "Same table as literary register:")
    (fields Author Work Location WhyThisStyle WhatTheyGrab WhatTheyIgnore Difficulty))

  (section diversity-rules
    (check "at least one approachable primer-style author")
    (check "at least one deep reference-style author")
    (check "vary subfield — language, systems, craft — when topic allows")
    (check "each author grabs a DIFFERENT facet of the payload"))

  (section owned-corpus-note
    (note "Modern technical books (Fowler, Butterfield, etc.) often lack public Exa excerpts.")
    (expect "Name author/work/location precisely; expect passage_resolution: needs_owned_corpus and catalog lookup per exa-discovery ref.")
    (load-order references/exa-discovery.md))

  (section examples
    (orientation-only t)
    (note "Donald Knuth (pedagogical density), Gerald Sussman (mechanism-first), Joachim von Braun essays on craft — adjust to topic.")))
