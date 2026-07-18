(def-ref engine
  (linked-from protocol-2-evaluation-references)

  (section domain-knowledge
    (artifact domain-knowledge-schema)
    (note "the rhythms of culture"))

  (section physics-schema-evaluation-metrics
    (purpose "Writing Modes crystallize into measurable Physics — internal checklist")
    (artifact physics-schema)))

;; --- artifacts ---

## domain-knowledge-schema

```
(:Domain_Knowledge
 (:config
  (Framework
   ;; "the rhythms of culture"
   (Culture
    (Archetypes
     (Duality :binds
      (ConflictResolution
       CompareContrast
       BalanceExtremism))
     (Cycle :binds
      (GrowthDecay
       IterationRefinement
       HubrisNemesis))
     (Connection :binds
      (InclusionExclusion
       GeneralizationSpecialization
       WarningAttraction))
     (Inquiry :binds
      (CauseEffect
       PatternAnomaly
       HypothesisExperiment))
     ;; THE PHYSICS (The Consequences/Laws)
     ;; The rules below exist BECAUSE of the patterns above.
     (:crystallizes_into
      (Physics
       (Embeddings :binds
        (Proximity
         ConceptualNeighborhoods
         Polysemy
         Synonymy))
       (RelationalVectors :binds
        (AnalogicalReasoning
         ConceptualTransformation
         CrossLingualIsomorphism))
       (ContextualAttention :binds
        (Disambiguation
         NuanceTone
         CoreferenceResolution)))))))))
```

## physics-schema

```
(:Writing_Analysis
 (:crystallizes_into
  (Physics
   (SemanticPrecision :binds
    (TermRichness
     ConceptualNeighborhoods
     Polysemy
     Specificity))
   (LogicalArchitecture :binds
    (ArgumentFlow
     ConceptualTransformation
     InternalConsistency))
   (PurposeClarity :binds
    (IntentSignaling
     AudienceAlignment
     ToneCohesion))
   (SurfaceMechanics :binds
    (SentenceArchitecture
     LexicalAccessibility
     StructuralRhythm))
   (CognitivePathway :binds
    (LoadManagement
     InformationSequence
     ExpectationFulfillment))
   (VitalTexture :binds
    (SpiritRetention
     AuthenticUrgency
     EmotionalTexture)))))
```
