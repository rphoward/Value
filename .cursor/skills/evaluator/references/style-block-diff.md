(def-ref style-block-diff
  (linked-from protocol-2-style-block-diff)
  (contract eliotapp/core/shapes/score.py)

  (section style-block-diff-mode
    (input "{draft, style_block}")
    (purpose "score draft fidelity to frozen Dense Style Block")
    (invariant "every block section is an axis; hillclimb needs numeric comparable Score with same vector shape and stable total run-to-run"))

  (section thirteen-axes
    (note "one axis per block section, in block order")
    (axis 1 OCEAN (kind qualitative) (measures "narrating temperament matches author row"))
    (axis 2 SURFACE (kind deterministic) (measures "draft echoes SURFACE keyword signals"))
    (axis 3 ENVIRONMENT (kind qualitative) (measures "place performs stated function and weight"))
    (axis 4 DEIXIS (kind qualitative) (measures "vantage, narrator cadence, and tempo obey block"))
    (axis 5 PROSODY (kind deterministic) (measures "sentence-bucket, punctuation, dialogue-ratio physics"))
    (axis 6 CADENCE (kind qualitative) (measures "rhythm-as-heard matches block PROSODY prose (cadence, stress, closes)"))
    (axis 7 DNA (kind qualitative) (measures "signature moves, images, avoids, voice_sample at clause level"))
    (axis 8 WORLDVIEW (kind qualitative) (measures "draft enacts block metaphysics and values"))
    (axis 9 "ARCHETYPE MAPPING" (kind qualitative) (measures "primary archetype and bindings actually operate"))
    (axis 10 ARC (kind qualitative) (measures "shape, movement, and resolution match"))
    (axis 11 "DIALOGUE DYNAMICS" (kind qualitative) (measures "speech distribution and response form match"))
    (axis 12 CAST (kind deterministic) (measures "CAST character names present in draft"))
    (axis 13 ORCHESTRATION (kind qualitative) (measures "characters embody ideas; opposition given real force")))

  (section split
    (deterministic-three "SURFACE, PROSODY, CAST — computed from draft text by eliotapp/core/evaluator/score_draft.py; CLI scripts/score_fixture.py; reproducible run-to-run")
    (qualitative-ten "the rest — scored by agent applying references/style-block-rubric.md, ideally fresh-context eval-audit subagent so no emulation history colors judgment; agent emits JSON array validated by parse_qualitative_scores in score.py"))

  (section blend
    (formula "total = 0.5 * mean(deterministic) + 0.5 * mean(qualitative)")
    (qualitative-absent "total is deterministic mean alone")
    (vector "fixed 14-slot: one slot per section in block order, plus total last; unscored sections hold sentinel -1.0")
    (hillclimb "same shape every run so delta(score) across iterations"))

  (section reproducibility
    (command artifact reproducibility-command)
    (tolerance "same inputs produce same deterministic vector within 0.01"))

  (load-order references/style-block-rubric.md "scoring territory"))

;; --- artifacts ---

## reproducibility-command

```powershell
$env:PYTHONPATH="src"; python .cursor/skills/evaluator/scripts/score_fixture.py --draft <path> --block <path> --repeat 3
```
