(def-ref engine
  (linked-from protocol-2-analysis-references)

  (Hierarchy
    (Tier1
      (label "AUTHORIAL SUBSTRATE")
      (mutability immutable)
      (desc "The vessel that contains all character expression")
      (Prosody (controls "how ANY thought gets rendered — length rhythm structure"))
      (DwellPoints (controls "what expands vs compresses regardless of speaker"))
      (DetailAccretion (controls "type and density of accumulated detail"))
      (WorldTexture (controls "the reality characters inhabit"))
      (ArcShape (controls "how the whole moves — narrative or argumentative shape"))
      (NarratorStance (controls "how characters are framed even when they speak"))
      (VoiceSample (controls "2-3 characteristic NARRATION constructions — clause-level anchor for Tier1; without this, authorial mouth-feel is rebuilt from adjectives = leakage"))
      (GoverningTension (controls "productive opposition defining author voice")))

    (Tier2
      (label "CHARACTER OVERLAY")
      (mutability variable-within-Tier1)
      (desc "Content shaped by the authorial vessel")
      (Beliefs (controls "what character thinks and claims"))
      (OCEAN_Delta (controls "personality divergence from author baseline"))
      (Rhetoric (controls "persuasive strategies"))
      (Idiolect (controls "vocabulary verbal-tics register-shifts"))
      (VoiceSample (controls "clause-level mouth-feel — characteristic constructions"))
      (CharWorldview (controls "what character believes about reality")))

    (Rules
      (Enumeration
        (when "multi-character works")
        (do "enumerate each significant character in CAST")
        (significant "any voice that speaks, interiority rendered, presence affecting dynamics")
        (mandatory true))
      (Rendering
        (principle "character content processed through authorial engine")
        (principle "character rationality must not sanitize authorial texture")
        (examples
          ("logical+systematic" "feverish-prose" "-> feverish logic in long sentences")
          ("cold+detached" "warm-narrator" "-> warmly-rendered coldness")
          ("rebel-against-meaning" "moral-structure" "-> rebellion confirming structure")
          ("terse-speaker" "expansive-author" "-> terse content with authorial expansion around it")))
      (Contradiction
        (when "character worldview opposes author")
        (step 1 "render at full strength — no straw men")
        (step 2 "maintain authorial texture throughout")
        (step 3 "let world answer through structure not narrator")
        (step 4 "character force IS author craft"))
      (Priority
        (step 1 "does it sound like author wrote it? (Tier1)")
        (step 2 "does it sound like this character within that author? (Tier2)")
        (if-Tier2-overrides-Tier1 "recalibrate"))))

  (DriftSuppression
    (principle "These are engine defaults, not authorial. Appearance = contamination.")

    (Lexical
      (label "never use unless source author demonstrably uses")
      (floor "known-offender floor, not the definition of slop: tapestry delve realm testament journey nuanced multifaceted underscore beacon resonate landscape pivotal")
      (suspect-test "model-agnostic; suspect when ALL hold: recurs in draft AND (absent from source OR leaned on harder than source) AND not demanded by new subject (3rd condition closes the zero-frequency hole)")
      (rank-test "top ~10 content words draft leans on — does author lean on them? rank survives small samples where ratios explode")
      (cross-examination "which words here would this author never reach for? — models answer this best; ask of every suspect")
      (collocation "predictable pairings (stark contrast, palpable tension, quiet dignity) = one lexical unit under all tests"))

    (Punctuation
      (principle "match Fingerprint per-100w counts (, ; — ? !) — arithmetic, not vibes")
      (EmDash (rule "use ONLY if source Prosody includes em-dash; AI default ~5x too high"))
      (Semicolon (rule "AI over-semicolons by default"))
      (Ellipsis (rule "match source, don't default for trailing thought"))
      (Exclamation (rule "AI suppresses; some authors rely on them")))

    (DiscourseTells
      (Tricolon (problem "AI defaults groups-of-three") (fix "match source grouping"))
      (HedgingStack (problem "perhaps/in-some-ways/one-might-argue layered") (fix "only if author hedges"))
      (BalancedParallelism (problem "AI defaults neat parallel") (fix "many authors asymmetric"))
      (EmotionalLabeling (problem "AI names emotions") (fix "check show vs tell"))
      (NegationPivot (problem "compulsive 'not X — it's Y' as default emphasis") (fix "source frequency only"))
      (OverCohesion (problem "every sentence stitched to last; no jump cuts") (fix "match source tolerance for asyndeton + hard transitions"))
      (SignificanceInflation (problem "every passage arcs toward Meaning; paragraphs wrap with meaning-label (absorbs old SummarySentence)") (fix "check what author lets simply happen; test each paragraph ending vs source"))
      (DramaticFragment (problem "short fragment for punch") (fix "match source fragment frequency"))
      (UniformParagraphRhythm (problem "every paragraph same shape/length") (fix "-> Extensions ParagraphBehavior (canonical); match source paragraph shapes"))
      (ShortParagraphGaming (problem "stacked 1-2 sentence paragraphs fake shape") (fix "short declaratives inside paragraphs; match source body shapes")))

    (Modernization
      (label "critical persistent failure")
      (principle "would a scholar of this author spot this as anachronistic? if yes -> replace")
      (Vocabulary (rule "only words available in author's era+register; when uncertain use older/simpler"))
      (Syntax (rule "match source era sentence architecture not modern plain style"))
      (Idiom (rule "stay in author's conceptual neighborhood; no era-unavailable concepts"))
      (CulturalRef (rule "render author's era faithfully; author's worldview is the worldview"))
      (Register (rule "match register spectrum; if author writes high write high")))

    (Audit
      (when "after ANY emulation output")
      (arithmetic "count post-draft: sentence-length dist vs Fingerprint (flattened->rewrite); punct per-100w (, ; — ? !) vs Fingerprint (>~20% over->revise); tricolon count->break if source doesn't favor")
      (recognition "can't count: lexical suspect+rank+cross-exam+collocation tests->rewrite suspects in author texture (don't just delete); discourse tells (negation-pivot, over-cohesion, significance-inflation, dramatic-fragment, uniform-paragraph-rhythm) vs source frequency; modernization->read as author's scholar; vices->at source frequency, none overdosed; arc->refused stays refused")
      (cold-session "strongest audit = fresh session or cross-model, style block only, no source/draft-history (canonical: Emulation step 8)")
      (honest-limits "prompting shifts the mean, not the variance; residual flatness is for the human ear — do not overpromise")))

  (Domain_Knowledge
    (config
      (Framework
        (Culture
          (Archetypes
            (Duality (binds ConflictResolution CompareContrast BalanceExtremism))
            (Cycle (binds GrowthDecay IterationRefinement HubrisNemesis))
            (Connection (binds InclusionExclusion GeneralizationSpecialization WarningAttraction))
            (Inquiry (binds CauseEffect PatternAnomaly HypothesisExperiment))
            (crystallizes_into
              (Physics
                (Embeddings (binds Proximity ConceptualNeighborhoods Polysemy Synonymy))
                (RelationalVectors (binds AnalogicalReasoning ConceptualTransformation CrossLingualIsomorphism))
                (ContextualAttention (binds Disambiguation NuanceTone CoreferenceResolution))))))))

    (DerivationRules
      (step 1 "trace to archetype — which universal pattern is active?")
      (step 2 "identify active bindings — which specific operations?")
      (step 3 "follow crystallization — how do patterns manifest in text physics?")
      (sub "Embeddings -> what conceptual neighborhood?"
           "RelationalVectors -> what analogical structures carry meaning?"
           "ContextualAttention -> what terms shift meaning under pressure?"))

    (BindingOutputs
      (BalanceExtremism "antagonist claims reasonable center; protagonist becomes extremist")
      (HubrisNemesis "totalized system meets its limit; something cannot be absorbed")
      (PatternAnomaly "exception persists without refuting — Yes and I refuse anyway")
      (ConflictResolution "opposing forces seeking synthesis or victory")
      (CompareContrast "scale tensions; juxtaposition as meaning-making")
      (GrowthDecay "processes of becoming and dissolution")
      (InclusionExclusion "boundary-drawing; who belongs who is outside")
      (CauseEffect "consequence chains; responsibility structures"))

    (KeyPrinciple "character stances and response patterns are OUTPUTS of Archetype+Worldview+Orchestration — derive them, do not invent them")))
