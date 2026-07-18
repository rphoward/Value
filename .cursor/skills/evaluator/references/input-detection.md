(def-ref input-detection
  (linked-from protocol-1-workflow-entry)

  (section input-modes
    (mode StyleBlockDiff
      (input "{draft, style_block}")
      (use-when "hillclimb, emulate-then-evaluate, fidelity check against ELIOT block"))
    (mode DraftOnly
      (input "draft prose only")
      (use-when "legacy UWE critique without a target style block")))

  (section detection-rules
    (rule 1 "user supplies both draft and Dense Style Block (fenced or path) → StyleBlockDiff")
    (rule 2 "user supplies only prose to evaluate → DraftOnly")
    (rule 3 "user says hillclimb, score against block, or style-block diff → StyleBlockDiff even if block is in a prior turn"))

  (section style-block-diff-load-order
    (load-order 1 references/style-block-diff.md)
    (load-order 2 references/workflows.md :branch StyleBlockDiff)
    (load-order 3 references/modes.md references/lenses.md references/engine.md :on-demand)
    (load-order 4 references/rubric.md references/output-format.md :before-scoring-output))

  (section draft-only-load-order
    (load-order 1 references/workflows.md :branch DraftOnly)
    (load-order 2 "same on-demand references as UWE v2.8 monolith")))
