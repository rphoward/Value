(def-ref workflows
  (linked-from protocol-1-workflow-entry)

  (Analysis
    (step 1 "check InputDetection — analyze or write? nonfiction -> GenreAdaptation remap")
    (step 2 "if WriteMode -> use DefaultVoice; skip to step 11")
    (step 3 "if AnalyzeMode -> read source closely — count Fingerprint (sentence buckets, punct per-100w); count ParagraphBehavior: sentence-count per paragraph, single-line paragraphs, open mode and close mode per paragraph or by type — never collapse to one template")
    (step 4 "populate OCEAN — facet-level granularity where voice depends on it")
    (step 5 "map ENVIRONMENT — container, scale tension, Trajectory (what changes, what shifts mark)")
    (step 6 "DEIXIS + tempo — narrator orientation; duration handling (TimeTrajectory)")
    (step 7 "enumerate CAST — who speaks? whose interiority? populate OCEAN_delta idiolect voice_sample function BEFORE worldview/archetype (characters = core data); apply CastBudget")
    (step 8 "ARCHETYPE MAPPING — which universal patterns organize thought?")
    (step 9 "derive ARC — shape movement resolution scale (per NarrativeArc :warning)")
    (step 10 "DNA + WORLDVIEW — deep generators")
    (step 11 "DIALOGUE DYNAMICS — how voices interact? what can responses weigh?")
    (step 12 "orchestration — how CAST members interact")
    (step 12b "compile PROSODY paragraph_modes from Extensions ParagraphBehavior (canonical); if source shapes differ, block must name them; one archetype paragraph is FAIL; NEVER emit dist …% (calibration only); init copies analyzer block unchanged")
    (step 13 "run Validation — completeness gates + Compactness + confidence signals before output")
    (step 14 "OUTPUT — follow OUTPUT INSTRUCTIONS: brief explanation (2-4 sentences) THEN style block in SEPARATE code fence; style block must be standalone copy-pasteable artifact"))

  (Emulation
    (step 1 "Tier1 first — does prose sound like author wrote it? does whole move in ARC shape?")
    (step 2 "derive don't invent — stances from WORLDVIEW + active bindings")
    (step 3 "stay in ConceptualNeighborhood — leaving = drift")
    (step 4 "let silence work — not every argument needs counter-argument")
    (step 5 "verify terminal stress — hard stops after long builds are load-bearing")
    (step 6 "audit scale contrast + trajectory — space presses against scope; shifts mark per spec")
    (step 7 "CAST against Tier1 — each character sounds like THIS author writing THAT character")
    (step 8 "run EmulationVerification loop — render->verify->revise->final-read; outputs beyond ~600w verify per-section not only at end (drift accumulates with length); paragraph shape -> length+internal rhythm match source (and block paragraph_modes); if every paragraph shares the same arc and similar length, rewrite (UniformParagraphRhythm); if shape is faked by stacking 1–2 sentence paragraphs while body paras stay same-shaped, rewrite (ShortParagraphGaming — bad writing, not fidelity); strongest audit = fresh session (or different model), style block only, no source or draft-history")
    (step 9 "run DriftSuppression audit — lexical suspect tests + punctuation + discourse tells + modernization + vices + arc")
    (step 10 "extrapolation (lost-chapter, foreign subject): author's image inventory must DIGEST new content, not sit beside it — render it through the DNA images or it isn't the author"))

  (InventEmulation
    (when "pipeline invent session already running (thematic material + suited author + a few unscored drafts or a new piece in that voice)")
    (inputs "style block + content-brief.md + craft-brief-vN.md; parent passes output_path=draft-v1a.md (etc.) to emulate-drafter")
    (default "new seed draft carrying Distiller thematic payload + user craft direction under the chosen voice")
    (forbidden 'default-lost-chapter 'default-pastiche-of-source-plot)
    (allow-pastiche "only when the user explicitly asks for lost-chapter or pastiche")
    (modules
      "eliotapp/application/workflow/draft_inputs.py"
      "eliotapp/application/workflow/content_contracts.py")
    (note "Still run Emulation steps 1–10 for fidelity; invent changes the subject posture, not the style gates")))
