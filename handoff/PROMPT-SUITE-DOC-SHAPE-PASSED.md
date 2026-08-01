(def-sop prompt-suite-doc-shape-passed
  (context
    (target "fresh-session-agent")
    (optimization "reusable-generator-prompt-matches-parse_suite-contract")
    (outcome PASS)
    (closed 2026-07-31)
    (supersedes handoff/PROMPT-SUITE-DOC-SHAPE-OPEN.md)
    (prior-prompt "Gemini webapp generator — #### Section N headings, weak fence rules")
    (new-prompt workproduct/prompt-suite-doc-shape/GENERATOR-PROMPT.md)
    (dry-run workproduct/prompt-suite-doc-shape/tiny-dry-run-suite.md))

  <central_idea>
  (center-of-gravity
    (invariant "A pasteable generator prompt now forces ## numbered headings, ```json / ```markdown fences, backtick names, no nested triple-backticks, no Docs escapes or base64 images — so the next book suite need not use tools/normalize-teams-prompt-suite.py.")))

  (protocol-0-evidence
    (proof-command "python .cursor/skills/scripted-skill-from-doc/scripts/compile.py parse --source workproduct/prompt-suite-doc-shape/tiny-dry-run-suite.md")
    (result "non-empty knowledge_base (4 keys); orchestrator name Tiny-Architect; modules Context-Mapper + Gate-Keeper with non-empty prompt_markdown")
    (compare-table
      (misshape "###/**Section N:** / #### headings" → "forced ## N. … grammar")
      (misshape "bare JSON / Docs \\_ escapes" → "```json fence + valid JSON rule")
      (misshape "name in parentheses not backticks / Section 2: prefix" → "`## 2. Master Orchestrator Prompt (`Name`)`")
      (misshape "one blob for all subskills" → "per-subskill `## N. Subskill K Prompt (`Name`)`")
      (misshape "nested ```yaml inside ```markdown" → "indented plain YAML only; zero nested fences")
      (misshape "base64 image embeds" → "forbid images/data URLs; ≤10 words as text")))

  (protocol-1-deliverables
    (generator-prompt workproduct/prompt-suite-doc-shape/GENERATOR-PROMPT.md)
    (acceptance "compile.py parse; refuse ship if modules empty / orch null / KB {}")
    (note "Promote prompt to docs/ only if human asks; workproduct holds session draft"))

  (protocol-2-next-or-none
    (next "none for this gate — human pastes GENERATOR-PROMPT into Gemini/NotebookLM for the next book")
    (optional "save or tweak prompt under docs/ on request")))
