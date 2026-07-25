(def-ref examples
  (linked-from protocol-1 protocol-2 protocol-5 protocol-6)

  (section mvp-design-showcase-artifacts
    (note "From operator dogfood; illustrates story vs brief vs prompt."))

  (section example-story
    (text "As a vibecoder who just finished a side project, I want to paste my repo (or docs) and get back a short shareable video-style overview, so that I can drop one link in Discord showcase and peers get the problem, stack, killer feature, and when it is worth using without opening the repo first."))

  (section example-brief-verbatim
    (text "Highlight the core problem, tech stack, and killer feature for vibe coders. Keep the tone energetic and developer-focused."))

  (section example-test-hook
    (text "Three showcase peers can each restate problem, stack, and use-when or skip-when after watching."))

  (section example-v1-skill-outcome
    (text "Story-to-prompt skill plus NotebookLM two-pass (recon ledger, then producer paste block) — integrated repo scan or timed video JSON is v1.1."))

  (section example-evidence-to-story
    (note "Same dogfood material, worked forward from the notes instead of backward from the sentence.")
    (intake-actor "A vibecoder on the evening he finishes a side project and opens the Discord showcase channel.")
    (intake-current-behaviour "Pastes the repo link with a two-line summary typed from memory.")
    (intake-cost "No replies. Three days later he re-posts with a longer summary and still gets no questions about the stack.")
    (funnel-ceiling "understand — the evidence shows peers not taking the project in, not peers failing to adopt it.")
    (step-1-so-that "so that peers get the problem, stack, and when it is worth using without opening the repo")
    (step-2-want "I want a short shareable overview I can drop in the channel")
    (step-3-persona "As a vibecoder who just finished a side project")
    (negotiable-test "Swap NotebookLM for a screen recording and the sentence still holds, so the outcome is what is fixed.")
    (grounding "Two showcase posts with no replies, plus the re-post.")
    (kill-signal "Three peers watch the overview and still ask what the project is for.")
    (invest-plus-reading "N pass, V pass, T pass; I, E, and S not answerable here — no backlog, estimating team, or sprint length was supplied."))

  (section example-showcase-inaccuracy
    (note "Second bottleneck after understand: polished video with wrong specifics.")
    (symptom "Peers watched but could not say what it was for; operator also noticed wrong file names and invented hook behavior.")
    (cause "Dual-host audit podcast prompt prioritized conflict and closure over the source ledger.")
    (fix "Problem-first section order plus source-fidelity rules and per-claim path check; defer debate format to v1.1 with source_path per beat.")
    (kill-signal-extended "Factual claim in the overview that README or install docs contradict."))

  (section example-non-story-claim
    (draft-claim "Ship your side project overview in one click — teams adopt faster.")
    (what-is-wrong "adopt is two stages above what the evidence reaches, and the reader is a solo poster, not a team.")
    (funnel-ceiling "understand")
    (held-claim "Paste a repo, get a short overview a peer can watch before opening the code.")
    (grounding "The same two showcase posts with no replies.")
    (note "A release note is not a story, and it still carries the funnel ceiling. Fill funnel stage and grounding; skip the rest of the card.")))
