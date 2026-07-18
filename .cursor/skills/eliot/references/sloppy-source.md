(def-ref sloppy-source
  (linked-from pipeline protocol-2-sloppy-source eliot analyze)

  (context "owned-corpus and OCR exports often arrive as messy markdown; ELIOT analyze still works when prose texture is present")

  (accept
    "missing or inconsistent heading levels"
    "line-break artifacts from PDF or EPUB conversion"
    "occasional OCR character substitutions if rhythm and diction remain readable"
    "front matter or chapter labels above the excerpt body")

  (focus-analyze-on
    "sentence rhythm and length variation"
    "diction register and figurative habit"
    "argument or narrative flow in continuous prose"
    "dialogue tag patterns when dialogue is present")

  (de-emphasize
    "table of contents blocks"
    "page numbers and running headers"
    "bullet lists unless they dominate the author's voice (then apply GenreAdaptation)")

  (minimum-size
    (resolve_passage "200–2000 words; recommended 800–1200 for dense style-block quality")
    (prepare "800+ words when hillclimb calibration is needed")))
