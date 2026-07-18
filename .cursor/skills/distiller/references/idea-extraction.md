(def-ref idea-extraction
  (linked-from protocol-2-phases phase-1)

  (step 1 idea-extraction
    (critical "Input is rough idea capture. Extract the THINKING. Discard the phrasing."))

  (section extract-fields
    (CoreThesis "Central claim in 1–2 abstract sentences. No source vocabulary.")
    (SecondaryMovements "2–4 subordinate arguments or counter-currents.")
    (GoverningTensions "Productive oppositions as X/Y pairs (e.g. freedom/security). Map to ELIOT Archetype bindings.")
    (TransformationArc
      (types "descent-into, emergence-from, confrontation-without-resolution, accumulation-to-crisis, loss-of, discovery-of, inversion-of, corruption-of, return-to, refusal-of")
      (purely-argumentative "static-confrontation"))
    (EmotionalCore "What feeling POWERS the text beneath the logic.")
    (ImageField "Recurring images as concrete/abstract pairs (e.g. hollow-fruit-collapsing/emptiness-behind-surface). Preserve vehicle and tenor. Do not use source exact phrasing."))

  (section checks
    (check "no prose-texture analysis")
    (check "ImageField pairs are concrete enough for ELIOT DNA.images")
    (forbidden "source vocabulary in any extracted field"))

  (short-input "If input is too short or too abstract for a full payload, say so and ask for more."))
