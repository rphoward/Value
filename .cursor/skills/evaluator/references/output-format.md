(def-ref output-format
  (linked-from protocol-3-scoring)

  (section output-format
    (step 1 code-block
      "Generate PRE-COMPUTATION LOG containing mode detection, per-dimension observations, tier assignments, and scores. Observations drive scores — not the reverse.")
    (step 2 evaluation-report
      (format "standard markdown prose — no code blocks in this section")
      (part 1 introduction "Briefly describe work, identify Primary Writing Mode, state apparent audience and purpose")
      (part 2 evaluation-body
        "Critique using Physics dimensions; draw on Lenses"
        (dimension semantic-precision "Aristotle / Orwell")
        (dimension logical-architecture "Aristotle")
        (dimension purpose-clarity "Burke")
        (dimension surface-mechanics "Orwell")
        (dimension cognitive-pathway "Clark")
        (dimension vital-texture "Garnett"))
      (part 3 craft-assessment-woolf "Holistic paragraph on voice, rhythm, originality, aesthetic coherence")
      (part 4 crystallization-verdict
        (gold-standard-definition "State specifically what Perfect Version does — concrete differences from current version, not general terms")
        (refinement-advice "Specific actionable instructions to close gap; prioritized by impact")
        (fix-validation
          "Before finalizing Refinement Advice, test each proposed change against voice and mode identified during analysis"
          (ask "Could this fix exist inside the voice I just described?")
          (contamination "If analysis identifies flat declarative prose and fix introduces simile, lyrical imagery, or emotional labeling absent from established register — fix is contaminated")
          (remedy "Rewrite within voice, or flag conflict explicitly")
          (note "correct diagnosis with incompatible prescription is net negative")))
      (part 5 final-score (artifact final-score-table)))
    (status "SYSTEM ONLINE. Awaiting input text."))

;; --- artifacts ---

## final-score-table

| Dimension | Tier | Score |
| :---- | :---- | :---- |
| Mode Alignment (Is the intent sound?) | [Tier] | [0–100] |
| Structural Physics (Is execution clean?) | [Tier] | [0–100] |
| Cognitive Clarity (Can it be followed?) | [Tier] | [0–100] |
| Craft & Vitality (Does it live?) | [Tier] | [0–100] |
| Total Score | [Tier] | [0–100] |
