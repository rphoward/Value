(def-ref input-detection
  (linked-from protocol-1-workflow-entry)

  (purpose "distinguish source-to-analyze from prompt-to-write")

  (rules
    (AnalyzeMode
      (triggers
        "prose passage 200+ words after resolve_passage (recommended 800–1200)"
        "has identifiable style markers (rhythm, diction, structure)"
        "author attribution present or inferable"
        "narrative or argumentative flow"))
    (WriteMode
      (triggers
        "bulleted outline or list"
        "short instructions (<100 words)"
        "imperative phrasing (write about, create, describe)"
        "no distinctive style — reads like generic prompt"))
    (GenreDetection
      (if "nonfiction/technical/journalistic")
      (action "apply GenreAdaptation remap"))
    (Safeguard
      (condition "input looks like AI-generated outline or template")
      (action "use DefaultVoice — do NOT analyze outline as style source")
      (reason "analyzing AI text would contaminate with AI-default patterns")))

  (disambiguation
    (if-uncertain "ask: Is this a style sample to analyze, or a topic to write about?")
    (default "if input < 150 words and no clear style markers, assume WriteMode")))
