(def-ref register-detection
  (linked-from protocol-2-phases phase-3)

  (section register-detection
    (goal "Infer register from thematic payload and brainstorm signals before author matching."))

  (section registers
    (literary "Narrative shape, scene seeds, character tension, novelistic image field")
    (technical "Pedagogy, how-to, systems explanation, clarity-over-lyricism in rough input")
    (essay "Argument, spiritual register, philosophical claim without tutorial structure")
    (philosophical "Dialectical tension, abstract thesis with minimal scene machinery"))

  (section procedure
    (step 1 "Read rough-input.md or pasted topic for domain vocabulary (code, scripture, criticism, fiction).")
    (step 2 "Read payload NarrativeShape, GoverningTensions, SceneSeeds.")
    (step 3 "Pick one register. When literary and essay both fit, prefer literary if scene seeds dominate.")
    (step 4 "Emit one-line declaration before phase 3 prose: Register: <value> (because <short reason>).")
    (step 5 "Allow user override; re-run author matching if register changes."))

  (section routing
    (literary (load-order references/author-matching-literary.md))
    (technical (load-order references/author-matching-technical.md))
    (essay-or-philosophical (load-order references/author-matching-essay.md))))
