(def-sop prompt-suite-doc-shape-open
  (context
    (target "fresh-session-agent")
    (optimization "author-a-reuseable-prompt-that-emits-compiler-compatible-prompt-suite-markdown")
    (outcome OPEN)
    (opened 2026-07-31)
    (paste-block handoff/NEW-CHAT-PROMPT-PROMPT-SUITE-DOC-SHAPE.md)
    (prior-chat "teams skill from High-Impact Tools Suite — normalize, promote, spine weave, verify map expand")
    (human-will-supply "the upstream prompt used to generate the misshapen High-Impact Tools Suite.md"))

  <central_idea>
  (center-of-gravity
    (invariant "Next session owns one deliverable: a prompt (first draft) that turns book/framework source material into markdown that scripted-skill-from-doc parse_suite accepts without a one-off normalizer. Discuss against the human's prior generator prompt. Do not expand into branding skill, milestone-template polish, or verify-map maintenance unless the human redirects.")))

  (protocol-0-why-this-exists
    (symptom "Google-Docs / alternate generator export of High-Impact Tools Suite.md parsed to empty KB, null orchestrator, zero modules")
    (fix-applied-once "reshape docs/High-Impact Tools Suite.md to suite contract; scaffold+promote teams; weave into product-spine")
    (gap "no durable upstream prompt yet — next suite will misshape again without one")
    (not-the-goal "rewriting compile.py to accept broken exports"))

  (protocol-1-compiler-contract-must-match
    (source ".cursor/skills/scripted-skill-from-doc/scripts/compile.py parse_suite")
    (headings
      (kb "^##\\s+\\d+\\.\\s+Central Reference Knowledge Base")
      (orchestrator "^##\\s+\\d+\\.\\s+Master Orchestrator Prompt\\s+\\(`Name`\\)\\s*$")
      (subskill "^##\\s+\\d+\\.\\s+Subskill\\s+\\d+\\s+Prompt\\s+\\(`Name`\\)\\s*$"))
    (fences
      (kb "```json ... ``` immediately after KB heading")
      (orchestrator-and-each-subskill "```markdown ... ``` — no nested triple-backtick blocks inside; parser stops at first closing fence"))
    (exemplars
      ".cursor/skills/scripted-skill-from-doc/assets/fixtures/sample-prompt-suite.md"
      "docs/value-proposition-prompt-suite (1).md"
      "docs/lean-product-playbook-prompt-suite.md"
      "docs/business-model-generation-prompt-suite.md"
      "docs/High-Impact Tools Suite.md — now normalized (working target shape)")
    (proof-command "python .cursor/skills/scripted-skill-from-doc/scripts/compile.py parse --source <doc> → non-empty knowledge_base, named orchestrator, N modules with prompt_markdown"))

  (protocol-2-misshape-lessons-from-prior-session
    (wrong "### **Section N:** headings, bold, Google bookmark TOC")
    (wrong "bare { JSON with \\_ escapes, no ```json fence")
    (wrong "orchestrator name in parentheses not backticks")
    (wrong "subskills as escaped \\#\\#\\# text inside broken nested fences")
    (wrong "trailing base64 image data URLs")
    (one-shot-helper "tools/normalize-teams-prompt-suite.py — format reshape only; not a substitute for a good generator prompt")
    (bias "Laziness: fix generator prompt / doc shape; do not bend the compiler for one export"))

  (protocol-3-verify-create-maintain-relevance
    (create-verification-skill "expanded .cursor/skills/verify-value/ for value|bmg|teams|lean-mvp CLI drive — useful for proving a compiled skill later; NOT the primary artifact for this prompt-authoring session")
    (maintain-verification-skill "upkeep loop only; produced no suite-doc contract docs")
    (use-from-verify-if-needed "after a new suite compiles and scaffolds, drive via control-value.py --skill <slug>; skip unless human asks to prove the skill"))

  (protocol-4-success
    (deliverable "draft prompt text the human can paste into their doc generator (ChatGPT/Claude/etc.) plus a short checklist of acceptance tests via compile.py parse")
    (compare "diff the human-supplied prior prompt against the new prompt; name which instructions prevent each misshape class")
    (optional "one dry-run: apply new prompt guidance to a tiny sample topic and parse with compile.py")
    (close-as "handoff/PROMPT-SUITE-DOC-SHAPE-PASSED.md or FAILED with one blocker")
    (forbidden 'promote-without-consent 'rewrite-compile-parser-as-default-fix 'scope-creep-into-branding-or-teams-templates))

  (protocol-5-next-owner
    (next "fresh session: paste NEW-CHAT-PROMPT; human attaches prior generator prompt; author new prompt; prove with parse")))
