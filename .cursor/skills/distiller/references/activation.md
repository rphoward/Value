(def-ref activation
  (linked-from protocol-1-input)

  (section triggers
    (load-when
      (paste "brainstorm notes, rough idea capture, Pierce transcript export, or a topic sentence")
      (ask "find an author or work for a theme")
      (ask "source passage before ELIOT analyze")
      (say "distill, thematic payload, idea extraction, register routing, or upstream workflow")
      (declare "ready to distill after a multi-turn brainstorm or Pierce session")))

  (section input-artifacts
    (artifact rough-input.md "Single paste or exported transcript in distiller run folder")
    (artifact pierce-chat-export "Save as rough-input.md; Pierce stays in eliotworkflow/ reference")
    (artifact topic-only "Inline or rough-input.md with one paragraph")
  (note "Multi-turn transcripts are valid input. Extract ideas across the thread; do not require a single paste."))

  (section open-prompt
    (when-text-present "I'll distill the ideas from this and find styles to carry them.")
    (when-no-text "Paste the rough text, transcript, or idea capture you want to work with. I'll strip the style, keep the ideas, and find authors whose voices could carry them."))

  (section mode-boundary
    (in-scope
      (extract "thinking, discard phrasing")
      (map "to (:ThematicPayload ...)")
      (suggest "authors + locate or resolve passage")
      (emit "emulation prompts (phase 4)"))
    (out-of-scope
      (forbidden "analyze prose texture (ELIOT skill)")
      (forbidden "emulate or score drafts")
      (forbidden "full hillclimb loop (workflow / pipeline skills)")
      (forbidden "port Pierce app into product"))))
