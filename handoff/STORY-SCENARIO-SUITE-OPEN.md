(def-sop story-scenario-suite-open
  (context
    (target "fresh-session-agent")
    (optimization "walk-graded-story-fixtures-typical-and-adversarial-without-silent-pass")
    (outcome OPEN)
    (opened 2026-07-25)
    (paste-block handoff/NEW-CHAT-PROMPT-STORY-SCENARIO-SUITE.md)
    (pack tools/drafts/story-scenario-suite/)
    (prior-gates handoff/PRODUCT-SPINE-KAI-UNHAPPY-PATH-PASSED.md
                 handoff/PRODUCT-SPINE-UX-MOCK-PASSED.md)
    (skill .cursor/skills/story-generation-prompt/SKILL.md))

  <central_idea>
  (center-of-gravity
    (invariant "This gate walks eight graded story fixtures (typical, boundary, adversarial) against story-generation-prompt. Success is pass/fail per case with a friction log — not shipping a new skill and not rubber-stamping hype.")))

  (protocol-0-preconditions
    (pack-ready "tools/drafts/story-scenario-suite/README.md + MANIFEST.tsv + cases/S01–S08")
    (tests "python -m pytest tests/test_story_generation_prompt_skill.py -v must be green before walk")
    (optional-spine "python -m pytest tests/test_product_spine_skill.py -v green if claim entry via /product-spine is used on S08")
    (forbidden 'edit-shipped-skills-during-walk-unless-fail-blocker 'invent-evidence-to-force-pass 'skip-cases))

  (protocol-1-walk
    (order S01 S02 S03 S04 S05 S06 S07 S08)
    (per-case
      "read case md"
      "play Input as human"
      "respond as story-generation-prompt (S08 may enter via /product-spine claim)"
      "score Pass check"
      "append one row to handoff/decision-trails/story-scenario-suite.tsv")
    (evidence tools/drafts/story-scenario-suite/WALK-EVIDENCE.md)
    (on-fail "log fail with one blocker axis; finish remaining cases unless human aborts; close FAILED if any case failed"))

  (protocol-2-success
    (primary "all eight cases PASS with TSV + WALK-EVIDENCE")
    (secondary "FAILED with first failing case id + one coaching blocker if skill cannot hold the axis")
    (close-as handoff/STORY-SCENARIO-SUITE-PASSED.md or FAILED.md)
    (pytest tests/test_story_generation_prompt_skill.py -v green))

  (protocol-3-next-owner
    (fresh-session "paste NEW-CHAT-PROMPT-STORY-SCENARIO-SUITE.md; run S01→S08")
    (this-session "pack + open handoff authored — do not start the walk here")))
