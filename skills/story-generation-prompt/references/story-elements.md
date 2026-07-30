(def-ref story-elements
  (linked-from protocol-0 protocol-1 protocol-2 protocol-3)

  (section what-a-user-story-is
    (definition "One negotiable promise of value in a single sentence — not a UX flow, feature list, or implementation plan.")
    (shape "As a [persona], I want [capability/outcome], so that [benefit].")
    (not-the-same-as
      (user-flow "Step sequence across screens; one flow may contain many stories.")
      (feature "Roadmap chunk; often larger than one story.")
      (epic "Theme holding many stories (e.g. showcase adoption).")
      (job-story "When [situation], I want [motivation], so I can [outcome] — valid alternative shape.")))

  (section story-parts
    (persona "Who is under pressure or has the need right now? One primary actor per story.")
    (want "Observable outcome or capability — what changes in the world, not how you build it.")
    (so-that "Benefit tied to a funnel stage; must be honest about what is validated (see funnel).")
    (acceptance-criteria "Separate from the story: how you know done; includes generation briefs, tone, must-include fields.")
    (generation-brief "Instructions for an AI or human producer (video, copy, mockup) — never substitute for persona/outcome/benefit."))

  (section funnel-honesty
    (stages "post → seen → understand → try → adopt")
    (rule "The so-that clause must match the slice you can test in v1 — do not claim adoption if you only validated understanding.")
    (ladder "Each stage is a separate observation. Reaching one does not give you the next.")
    (examples
      (post "The thing exists somewhere a peer could find it.")
      (seen "Peer opens or watches it — a view, a click, a reply.")
      (understand "Peers can restate problem, stack, and when to use or skip without opening the repo.")
      (try "Peer runs demo, clone, or one command within 24h of the post.")
      (adopt "Peer integrates the project into their own workflow or ships something built on it.")))

  (section invest-constraints
    (source "The six letters come from lean-mvp assets/knowledge-base.json invest_user_story_rubric, where each letter now carries its word, a one-sentence definition, and a one-line check of what to read or what context is missing. The two-block split, the extra rows, and the allowed results are not in that entry; they come from references/invest-plus.md, which is what you apply when you report.")
    (rubric references/invest-plus.md)
    (I "Independent — shippable without another story blocking it.")
    (N "Negotiable — outcome fixed; implementation (NotebookLM, custom engine, etc.) open.")
    (V "Valuable — user outcome, not a tech task.")
    (E "Estimable — team can size days vs weeks; if not, slice smaller.")
    (S "Small — one sprint / thin MVP slice.")
    (T "Testable — observable pass/fail (e.g. three peers paraphrase after watching).")
    (on-convert "When story → prompt, preserve funnel stage and do not inflate benefit in the prompt."))

  (section non-story-claims
    (definition "A non-story claim is a sentence that promises a reader something without using story grammar — a release note, a launch post, a changelog line, the first line of a README.")
    (same-ceiling "The funnel rule applies unchanged. A release note that says teams ship faster is claiming adopt from a change that only reached understand.")
    (procedure
      1 "Name the reader and the moment they read it."
      2 "Name the highest funnel stage the change can actually reach."
      3 "Rewrite the claim so it stops at that stage."
      4 "Keep the grounding line next to the claim so the next editor can see where the ceiling came from.")
    (note "There is no full story card here. Fill the funnel stage and grounding rows and leave the rest."))

  (section common-failures
    (forbidden "so that peers adopt — when only explainer is in scope")
    (forbidden "want integrate FFmpeg — implementation in want clause")
    (forbidden "persona everyone — split poster vs peer into two stories")
    (forbidden "merge generation brief into want — keep brief in acceptance / prompt block")
    (forbidden "entertainment-first prompts that invent files or behaviors to sustain banter — see references/source-fidelity.md"))

  (section pairs-with-lean-mvp
    (atom MS05 "INVEST user story for top MVP chunk")
    (atom MS06 "ROI uses story slice; v1 may be story-to-prompt skill plus manual tool run")
    (note "This skill does not write session.json; operator pastes output into accept_answer or NotebookLM.")))
