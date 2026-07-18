(def-ref eliot-mapping
  (linked-from protocol-2-phases phase-2)

  (step 2 eliot-mapping
    (goal "Translate extracted ideas into ELIOT-native structures inside (:ThematicPayload ...)."))

  (section derived-fields
    (ArchetypeActivation "GoverningTensions + TransformationArc. Primary: Duality / Cycle / Connection / Inquiry. Bind specific operations.")
    (DwellTargets "CoreThesis + EmotionalCore. 2–4 subjects to expand in emulation.")
    (CompressionTargets "What is NOT central. 2–3 subjects to keep minimal.")
    (NarrativeShape
      (from TransformationArc)
      (options "monologue-to-silence, accumulation-to-collapse, dialogue-as-combat, witness-testimony, descent-narrative, confrontation-without-resolution, parable, confession, inventory-of-evidence, slow-reveal, frame-story"))
    (SceneSeeds "3–4 concrete dramatic situations. Who is present, what is at stake, what cannot be resolved. Not philosophical summaries."))

  (section archetype-examples
    (example (tension "freedom/security") (archetype Duality) (binding BalanceExtremism))
    (example (tension "creation/decay") (archetype Cycle) (binding GrowthDecay))
    (example (tension "authentic/performed") (archetype Duality) (binding PatternAnomaly))
    (example (tension "individual/system") (archetype Duality) (binding HubrisNemesis)))

  (section payload-wrapper
    (require "Output MUST use (:ThematicPayload ...) S-expression format.")
    (template (load-order references/output-format.md))))
