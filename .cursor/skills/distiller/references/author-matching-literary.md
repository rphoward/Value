(def-ref author-matching-literary
  (linked-from register-detection routing literary)

  (section author-matching-literary
    (register literary)
    (description "Classical and literary prose. Default when narrative scene machinery dominates the payload."))

  (section match-criteria
    (priority-order
      (1 "Governing tension overlaps payload GoverningTensions")
      (2 "Dwell points align with DwellTargets")
      (3 "Narrative shape matches TransformationArc")
      (4 "Worldview engages same philosophical territory")))

  (section per-author-required-fields
    (Author "Full name")
    (Work "Specific novel, essay collection, or story")
    (Location "Chapter, section, or scene — not title alone")
    (WhyThisStyle "1–2 sentences connecting to ELIOT fields")
    (WhatTheyGrab "Which payload facet this author seizes")
    (WhatTheyIgnore "What compresses or vanishes in this style")
    (Difficulty "beginner / intermediate / advanced"))

  (section diversity-rules
    (check "at least one unexpected or non-obvious match")
    (check "vary era, tradition, and prose texture")
    (check "at least one beginner-accessible author")
    (check "each author grabs a DIFFERENT facet of the payload"))

  (section examples
    (orientation-only t)
    (note "Dostoevsky, Rilke, Woolf, Morrison — works with identifiable chapters and public-domain or excerpt-friendly editions when possible.")))
