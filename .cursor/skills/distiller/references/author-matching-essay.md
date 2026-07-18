(def-ref author-matching-essay
  (linked-from register-detection routing essay philosophical)

  (section author-matching-essay
    (register "essay / philosophical")
    (description "Argument-driven prose, spiritual writing, and philosophical essay traditions."))

  (section match-criteria
    (priority-order
      (1 "Central argument structure mirrors payload CoreThesis and GoverningTensions")
      (2 "Author's typical compression matches CompressionTargets")
      (3 "Emotional core and image field align without requiring novelistic scene machinery")
      (4 "Archetype activation maps to author's habitual moral or metaphysical stance")))

  (section per-author-required-fields
    (note "Same table as literary register:")
    (fields Author Work Location WhyThisStyle WhatTheyGrab WhatTheyIgnore Difficulty))

  (section diversity-rules
    (check "at least one spiritual or contemplative voice when topic allows")
    (check "at least one skeptical or polemical voice")
    (check "vary tradition and century")
    (check "each author grabs a DIFFERENT facet of the payload"))

  (section examples
    (orientation-only t)
    (note "Camus, Weil, James Baldwin essays, Seneca letters — specific essay or letter, not collected-works title alone.")))
