(def-ref source-fidelity
  (linked-from protocol-2 protocol-5 protocol-6 protocol-7)

  (section what-source-fidelity-is
    (definition "Source fidelity is the rule that every factual claim in produced copy must be traceable to operator-supplied sources — repo files, docs, tickets — not to narrative convenience.")
    (pairs-with funnel-honesty "Funnel honesty caps what benefit you may promise. Source fidelity caps what facts you may state. A prompt can satisfy the funnel and still fail fidelity by inventing file names, features, or causal links to smooth dialogue."))

  (section why-entertainment-hallucinates
    (pattern "Dual-host debate, skeptical Q&A, and 'AI code audit podcast' formats ask the model to sustain conflict and closure across many beats.")
    (failure-mode "When sources do not contain a clean arc, the model bridges gaps with plausible-sounding specifics — wrong paths, merged systems, skills that do not exist, overstated hook behavior.")
    (operator-signal "Production quality stays high while peers misunderstand purpose or repeat inaccuracies that are not in the repo."))

  (section producer-rules
    1 "Treat attached sources plus operator-confirmed positioning as the fact ledger. Anything outside both stays out of voiceover and on-screen text."
    2 "Prefer omission over invention. A gap in the story beats a fabricated detail."
    3 "Every named file, directory, skill slash-command, env var, or layer label must appear in sources or be marked unknown and cut from the script."
    4 "Separate structure from facts: ordered sections (problem, for whom, use, skip) are instructions; their fill must come from sources."
    5 "Entertainment is subordinate. Tone may be energetic; format may not force factual bridges — use narrator or single voice before multi-host banter in v1."
    6 "After draft, run an accuracy pass: list each factual claim with source path or delete the claim.")

  (section fidelity-is-labeled-provenance-not-silence
    (problem "Read strictly, the fact-ledger rule silences an overview built from a codebase, because a coder's README states mechanism and never states audience, positioning, or when to skip.")
    (rule "Fidelity means every line can name where it came from. A source file is one origin. The operator confirming a derived reading is another.")
    (mechanism-facts "Trace to a source file and cite it. No exceptions.")
    (positioning-lines "Derive them under references/positioning-inference.md, label them, and have the operator confirm before they enter produced copy.")
    (forbidden "Treating an unconfirmed inference as a source fact, or dropping a needed positioning line entirely when the operator could confirm it in one pass."))

  (section notebooklm-two-pass
    (pass-1 "Recon only — assets/notebooklm-recon.template.md question; output is fact ledger pasted into evidence intake.")
    (pass-2 "Amplify under skill contract — Producer paste block from generation prompt; same sources attached; no repo body in the instruction box.")
    (skill-role "Pass 1 output is evidence for protocol-1 or protocol-6; pass 2 input is protocol-2 output, not a rewritten script from pass 1."))

  (section tool-split
    (notebooklm "Sources hold the repo; the generation prompt stays short. Instructions demand cite-only-from-sources and no cross-file speculation.")
    (long-context-api "Bundle allowlisted files; require JSON or outline with per-beat source_path fields before TTS or video.")
    (forbidden "Embedding the whole repo inside the NotebookLM instruction box — attach sources there; keep the skill output as ceiling plus fidelity rules plus section order."))

  (section generation-prompt-fields
    (source-material "Explicit list of paths or uploads the producer must use.")
    (accuracy-pass "Instruction to reconcile every named artifact with sources or drop it.")
    (high-risk-formats "Flag dual-host debate and audit-podcast templates as high hallucination risk unless source_path per beat is required."))

  (section common-failures
    (forbidden "Inventing a hook or skill to answer a skeptic question")
    (forbidden "Merging USER-RULES and vernacular into one fictional layer name")
    (forbidden "Stating pre-commit behavior that install docs do not describe")
    (forbidden "Smooth transitions that assert causation the README never claims")))
