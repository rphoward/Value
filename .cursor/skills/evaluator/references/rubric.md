(def-ref rubric
  (linked-from protocol-3-scoring)

  (section scoring-rubric
    (purpose "Each Physics dimension scored using named tiers to anchor evaluation and prevent score inflation")
    (tier sharp
      (range "85-100")
      (meaning "Every element is load-bearing. No wasted moves. This dimension is operating at or near its ceiling for this mode."))
    (tier functional
      (range "60-84")
      (meaning "Solidly working but contains 2-3 identifiable weaknesses. Competent, not exceptional."))
    (tier soft
      (range "35-59")
      (meaning "Noticeable problems that impede the text's purpose. Key elements are vague, misordered, or inconsistent."))
    (tier broken
      (range "0-34")
      (meaning "This dimension is actively working against the text. Fundamental failures in logic, clarity, sequencing, or intent."))
    (rule "name the tier first, then assign the number — tier is the anchor; number is precision within it")))
