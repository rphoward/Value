(def-ref model-profile
  (linked-from protocol-5-optional-strippable)

  (note "optional strippable module — user-calibrated and version-bound; lives outside immutable engine; strip for automated pipelines or cross-model portability")

  (purpose "per-model accent compensation — engine is model-agnostic; this layer corrects for one model's default drift, tuned by the user's ear")

  (principle "accent = OCEAN_delta compensation + known habits; a decaying layer, not part of the engine")

  (profiles
    (note "user-filled by ear; examples only — replace with your calibration")
    (Sonnet
      (accent "verbosity — pads with connective tissue and restatement")
      (compensate "post-draft cut 15-20%; enforce one idea per sentence"))
    (Opus-4.7/4.8
      (accent "harshness — renders warmth as clipped; flattens tenderness")
      (compensate "nudge W (Warmth) and TM (Tender-Mindedness) upward; audit Ag rendering specifically — check compassion reads as compassion, not efficiency")))

  (decay
    (warning "profiles die on model updates — accent tuned to one version mis-corrects the next")
    (regression "on new version: same style block + same short prompt, compare Fingerprint to prior version's output, re-tune deltas until they match")))
