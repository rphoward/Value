(def-ref lenses
  (linked-from protocol-2-evaluation-references)

  (section lens-configuration-six-readers
    (purpose "Observe writing through six critical perspectives; each lens asks a fundamentally different question"))

  (lens aristotle-rhetorician
    (asks "Is the structure of persuasion sound?")
    (evaluates "logos (logic), ethos (credibility), pathos (emotion)")
    (tests "whether the text earns the reader's trust"))

  (lens george-orwell-clarity-enforcer
    (asks "Is the language honest, clean, and parseable?")
    (catches "vagueness, pretension, jargon-as-camouflage, dead metaphors")
    (evaluates "whether sentence-level mechanics serve or obstruct the reader"))

  (lens herbert-clark-cognitive-reader
    (asks "Can the reader's mind actually travel the path this text lays out?")
    (property load "Is working memory respected? Can the reader hold what's being asked at any point, or does the text pile up unintegrated concepts? (Sentence complexity, concept density, jargon burden.)")
    (property sequence "Is information ordered so each new idea attaches to something already established? Given-before-new. Does concept B arrive before concept A that it depends on?")
    (property expectation "Does the text set up predictions and then fulfill or deliberately subvert them? Are structural promises kept — opening questions answered, introduced threads resolved, tonal shifts earned?"))

  (lens kenneth-burke-motivist
    (asks "What is the writer trying to do, to whom?")
    (evaluates "purpose-alignment: relationship between writer's motive, audience's needs, and text's actual behavior"))

  (lens virginia-woolf-craftsperson
    (asks "Does this writing have a living voice?")
    (evaluates "rhythm, originality, aesthetic coherence, authenticity")
    (tests "whether the writing sounds like a human or a machine")
    (subsection voice-stratification-narrative-mode
      (when "text uses first-person or close-third narrator")
      (distinguish "author voice (craft shaping prose) vs narrator voice (consciousness reporting)")
      (note "separate instruments — narrator who cannot articulate what they feel is not author telling instead of showing; inarticulation IS the showing")
      (test "if narrator limitation consistent with established character and reader understands more than narrator, limitation is craft not failure")
      (trap "misidentifying narrator limitation as authorial weakness leads to fixes that violate voice")
      (check "when generating Refinement Advice for narrated fiction, verify all proposed changes speakable by narrator as established")))

  (lens constance-garnett-mediator
    (asks "Does the spirit survive the vessel?")
    (evaluates "tension between raw vitality and surface polish in all writing modes")
    (checks "whether text retains urgency, specificity, rough edges of original thought — or revision/convention/correctness sanded life out")
    (vitality-by-mode
      (argumentation "writer's conviction is felt, not just stated")
      (narrative "characters and scenes have texture, not just correctness")
      (exposition "subject's difficulty or strangeness comes through")
      (inquiry "genuine uncertainty of investigation is preserved")
      (documentation "precision hasn't become sterility; human stakes remain"))
    (note "for philosophical, religious, or translated works, this lens carries additional weight — those texts live or die by spirit retention")))
