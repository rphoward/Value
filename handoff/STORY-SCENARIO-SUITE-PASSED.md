(def-sop story-scenario-suite-passed
  (context
    (target "fresh-session-agent-or-human-reviewer")
    (optimization "graded-story-fixtures-walked-without-silent-pass-or-invented-evidence")
    (outcome PASS)
    (closed 2026-07-25)
    (opened-as handoff/STORY-SCENARIO-SUITE-OPEN.md)
    (pack tools/drafts/story-scenario-suite/)
    (skill .cursor/skills/story-generation-prompt/SKILL.md)
    (prior-gates handoff/PRODUCT-SPINE-KAI-UNHAPPY-PATH-PASSED.md
                 handoff/PRODUCT-SPINE-UX-MOCK-PASSED.md))

  <central_idea>
  (center-of-gravity
    (invariant "All eight graded story fixtures (typical, boundary, adversarial) passed against story-generation-prompt — funnel honesty, negotiable want, situational persona, pass-1-first recon, empty I/E/S honesty, and hype-resistant producer paste held without inventing evidence or editing shipped skills.")))

  (protocol-0-outcome
    (result PASS)
    (score "8/8")
    (evidence handoff/decision-trails/story-scenario-suite.tsv
              tools/drafts/story-scenario-suite/WALK-EVIDENCE.md)
    (tests "python -m pytest tests/test_story_generation_prompt_skill.py -v → 12 passed after walk")
    (note "No FAIL blocker; no shipped skill edit in this walk"))

  (protocol-1-what-was-proven
    (S01 "observed workaround → try-stage INVEST sentence")
    (S02 "repo-only → pass-1 recon before draft")
    (S03 "funnel inflate → understand ceiling")
    (S04 "implementation in want → negotiable rewrite")
    (S05 "demographic persona → actor in a moment + try")
    (S06 "prompt→story → one question for missing cost")
    (S07 "no backlog/team → I/E/S not answerable or reasoned-from-scope")
    (S08 "hype video ask → try claim ceiling + do-not list"))

  (protocol-2-not-proven
    (note "Pack remains under tools/drafts/ — promote only if desired")
    (note "Did not open value/lean sessions; none of S01–S08 require them"))

  (protocol-3-next
    (optional "promote story-scenario-suite pack out of drafts when wanted")
    (optional "sync story-generation-prompt ship tree if walk findings later drive edits")
    (none-required-for-this-gate)))
