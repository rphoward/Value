(def-ref workflows
  (linked-from protocol-1-workflow-entry)

  (section internal-processing-logic
    (instruction "execute this workflow visibly in a code block titled PRE-COMPUTATION LOG before generating final response")
    (step 1 mode-identification "Detect Primary and Secondary modes")
    (step 2 physics-analysis
      "Analyze text against all 6 Physics dimensions. Write observations first, then derive tier and score from observations."
      (always "Analyze CognitivePathway (Clark) for all texts")
      (always "Analyze VitalTexture (Garnett) for all texts, with additional weight for philosophical, religious, or translated works")
      (narrative-first-or-close-third "apply Voice Stratification (Woolf). Identify narrator limitations and verify not misattributed to author. Log which lines are narrator-voice vs author-craft before scoring"))
    (step 3 gap-analysis "Compare text to Gold Standard ideal. State explicitly what ideal version would do differently")
    (step 4 fix-validation "Test all Refinement Advice against voice profile established during analysis. Flag or rewrite any fix introducing elements outside text's identified register"))

  (section style-block-diff-branch
    (when "input is {draft, style_block}")
    (see (load-order references/input-detection.md))
    (step 1 "Run deterministic primary score via scripts/score_fixture.py or eliotapp.core.evaluator.score_draft")
    (step 2 "Emit EvaluatorScore JSON (primary, total, vector)")
    (step 3 "Optionally run INTERNAL PROCESSING LOGIC steps 1-4 on draft with style block as Gold Standard context")
    (step 4 "Gap Analysis must cite specific block fields (SURFACE, PROSODY fingerprint, CAST) not generic ideals"))

  (section draft-only-branch
    (when "input is draft prose only")
    (step 1 "Execute steps 1-4 in INTERNAL PROCESSING LOGIC on draft")
    (step 2 (load-order references/output-format.md "for evaluation report and Final Score table"))))
