(def-ref author-matching
  (linked-from protocol-2-phases phase-3)

  (step 3 author-matching
    (goal "Suggest 3–5 authors whose styles naturally carry the thematic payload."))

  (section register-routing
    (required t)
    (step 1 (load-order references/register-detection.md) "declare register before prose candidates")
    (step 2 "Load exactly one specialized ref:"
      (literary (load-order references/author-matching-literary.md))
      (technical (load-order references/author-matching-technical.md))
      (essay-or-philosophical (load-order references/author-matching-essay.md)))
    (step 3 "Follow that ref's match criteria, per-author fields, and diversity rules."))

  (after-prose-candidates
    (run (load-order references/exa-discovery.md) "to pick one PassageCandidate for ELIOT analyze")))
