(def-ref validation
  (linked-from protocol-3-output)

  (when "before outputting analysis or emulation")

  (CompletenessGates
    (CAST
      (condition "source has characters/dialogue/interiority")
      (if-empty "FAIL — go back and enumerate; minimum: OCEAN_delta idiolect voice_sample function"))
    (ImageDeployment
      (condition "images inventory filled")
      (if-missing "FAIL — add deployment; describe what work images do"))
    (Prosody
      (condition "prosody section exists")
      (if-missing "FAIL — add sentence length variation departure internal-structure")
      (if-no-fingerprint "FAIL — add numbers; impressions are not verification targets"))
    (ParagraphBehavior
      (condition "PROSODY paragraph_modes field filled (qualitative prose only)")
      (if-single-template "FAIL — emit distinct paragraph shapes from source (length + internal rhythm + job); one archetype ('long spirals 5-12 sentences') when source shapes differ is invalid")
      (if-dist-percent "FAIL — paragraph_modes must be prose; dist …% bucket shares belong in calibration.json only, never in the style block")
      (if-missing "FAIL — describe paragraph shapes (opens, closes, jobs) when source shapes differ"))
    (Archetypes
      (condition "primary archetype identified")
      (if-missing "FAIL — identify >=1 active binding and >=1 crystallization target"))
    (Arc
      (condition "narrative or sustained argument")
      (if-missing "FAIL — derive shape per NarrativeArc :warning"))
    (Commits
      (condition "commits populated")
      (if-no-vice-in-output "FAIL — must show >=1 committed vice")
      (if-overdosed "FAIL — vice noticed on first read; dial to source frequency"))
    (Trajectory
      (condition "ENVIRONMENT filled")
      (if-missing "FAIL — static must be static-by-design, not unexamined"))
    (Compactness
      (if-over-budget "compress per OutputInstructions Compactness before output"))
    (EraConsistency
      (condition "historical or period text")
      (action "scan all fields for anachronistic vocabulary or concepts")))

  (ConfidenceSignals
    (principle "never silently skip a field")
    (InsufficientData "[Field] — insufficient source; need [X] to determine. Best guess: [Y] (low confidence)")
    (TwoReadings "[Field] — two readings: (A) [X] or (B) [Y]. Leaning [choice] because [reason]")
    (ThinSupport "[Field] (thin) — based on [limited evidence]. May shift with more source")
    (AmbiguousPrompt "ask: should analysis cover [X] or [Y]?"))

  (EmulationVerification
    (label "style block is contract not suggestion")
    (loop
      "RENDER first draft using style block"
      "VERIFY against EVERY field: sentence lengths match Prosody? departure function present? terminal stress patterns? dwell/compress targets correct? image deployment mode? intertextual neighborhood held? voice_samples in dialogue? OCEAN deltas audible? register matches era? lexical suspect-test clear? punctuation frequency? arc + resolution honored? space trajectory marking per spec? fingerprint numbers hit? tempo modes held? paragraph open/close modes? paragraph shape (length+internal rhythm) matches paragraph_modes / source? committed the author's vices, or sanded them off? any vice overdosed?"
      "REVISE failures — rewrite in author texture not just delete"
      "FINAL READ as author's scholar — plausibly theirs? AI-detectable? if wrong -> Step 3")
    (RhythmEnforcement
      (step 1 "count actual sentence lengths -> compare to Fingerprint -> if flattened rewrite")
      (step 2 "find departures -> are they doing what spec says?")
      (step 3 "simulate aloud -> does cadence match source? parallelism=parallelism surge=surge")
      (step 4 "terminal stress -> longest sentences end on monosyllable? if spec says so")
      (step 5 "paragraph shape -> length+internal rhythm match source (read paragraph_modes); if every paragraph shares the same arc+length -> UniformParagraphRhythm -> rewrite; if shape is faked with stacked 1–2 sentence paragraphs -> ShortParagraphGaming -> rewrite (put short declaratives inside paragraphs as sentence-level departures)")))

  (DriftTable
    (row "antagonist too soft" "failed BalanceExtremism derivation" "must claim center")
    (row "therapeutic idiom" "left ConceptualNeighborhood" "return to intertextual sources")
    (row "resolution where none belongs" "ignored avoids field" "check: does author resolve?")
    (row "environment as backdrop" "missed CompareContrast" "specify scale tension intrusions")
    (row "space static and unexamined" "Trajectory field ignored" "make spatial change (or chosen stasis) carry mood/time/power")
    (row "arc bends toward heros-journey" "AI attractor" "re-derive from source; test two alternative families; honor resolution field")
    (row "response answers argument" "wrong response type" "check: PatternAnomaly active?")
    (row "characters sound same" "CAST/voice_samples ignored" "render one character at a time against spec")
    (row "character overrides author" "Tier2 escaped Tier1" "reprocess through authorial engine")
    (row "text reads modern" "modernization drift" "audit vocabulary syntax idiom for era")
    (row "imagery flat" "deployment mode ignored" "make images do their specified work")
    (row "prose too clean OR vices parodied" "commits ignored / overdosed" "commit vices at source frequency — noticed on first read = overdosed")
    (row "rhythm flattened" "AI averaged to default" "count words force variation")
    (row "every paragraph same shape" "UniformParagraphRhythm / block template overfit" "match block paragraph_modes; length+internal rhythm match source shapes")
    (row "stacked one-line paragraphs as fake shape" "ShortParagraphGaming" "put short declaratives inside paragraphs; match medium/long body shapes from source")
    (row "tempo uniform" "TimeTrajectory ignored" "vary duration; scene only where spec earns it")
    (row "style block bloated" "field budgets ignored" "compress to spec-phrases; apply delete-Test")
    (row "literary categories forced on nonfiction" "GenreAdaptation skipped" "remap fields; drop what remaps to nothing")
    (row "discourse tell leaking (negation-pivot, over-cohesion, significance-inflation)" "modern AI defaults" "cut to source frequency; allow jump cuts + asyndeton")
    (row "AI voice leaking" "lexical suspects / discourse tells" "rewrite contaminated sentences")))
