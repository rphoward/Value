(def-ref output-format
  (linked-from protocol-3-output)

  (section output-order
    (note "Prose context first. Copy-paste artifact last."))

  (section 1 style-candidates
    (format "Prose entry per author (3–5).")
    (per-entry "Author, Work, Location, WhyThisStyle, WhatTheyGrab, WhatTheyIgnore, Difficulty"))

  (section 2 emulation-prompts
    (format "Numbered list per emulation-prompts ref.")
    (load-order references/emulation-prompts.md)
    (one-per-author t))

  (section 3 thematic-payload
    (position last)
    (format "Fenced code block with (:ThematicPayload ...) S-expression.")
    (required-top-level-keys
      CoreThesis SecondaryMovements GoverningTensions TransformationArc EmotionalCore
      ImageField ArchetypeActivation DwellTargets CompressionTargets NarrativeShape SceneSeeds))

  (section smoke-json
    (optional-sidecar "When recording a discovery run, write discovery.json validated by discover_format.py.")
    (sidecars "Optional thematic-payload.sexp and emulation-prompts.json per docs/adr/001-run-persistence.md.")))
