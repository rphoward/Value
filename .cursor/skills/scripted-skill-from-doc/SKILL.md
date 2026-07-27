---
name: scripted-skill-from-doc
description: >
  Use when the user asks to compile a prompt-suite markdown into a paced
  scripted Cursor skill, scaffold a skill from a book doc, or run
  prompt-suite-compile. Portable harness pack under this skill folder
  (scripts/, references/, assets/). Seeded atoms plus references/curriculum-synthesis.md
  for curriculum expansion; poteto-mode optional. Not for editing a protected golden skill named value, and not for Slack
  automations.
metadata:
  activation: intent
  pack: self-contained
  transports_with: .cursor
---

(def-sop scripted-skill-from-doc
  (context
    (target "prompt-suite-compile-orchestrator")
    (optimization "standard-skill-layout-plus-portable-compile-pack")
    (references
      (for-agents references/for-agents.md)
      (readme references/readme.md)
      (tutorial references/tutorial.md)
      (bootstrap references/bootstrap.md)
      (curriculum-synthesis references/curriculum-synthesis.md))
    (assets
      (session-runtime assets/session-runtime/)
      (sample-fixture assets/fixtures/sample-prompt-suite.md)
      (ir-schema assets/schema/prompt-suite.ir.schema.json)
      (pressure-tests assets/pressure-tests/pressure-tests.md))
    (scripts
      (compile scripts/compile.py)
      (audit scripts/audit_dag.py)
      (smoke scripts/smoke.py)
      (selftest scripts/selftest.py)
      (promote scripts/promote.py)))

  <central_idea>
  (center-of-gravity
    (invariant "This skill uses the standard scripts/references/assets layout. Read references/for-agents.md. Run scripts from scripts/. Expand curriculum via references/curriculum-synthesis.md. Never overwrite a skill named value."))
  </central_idea>

  (protocol-0-entry
    1 "read references/for-agents.md and references/readme.md"
    2 "require source path and slug from the user (slug must not be value)"
    3 "read references/curriculum-synthesis.md when expanding atoms (optional: /poteto-mode if installed)")

  (protocol-1-mechanical
    (cwd "repo root preferred so drafts/ and workproduct/ land correctly")
    (run "python .cursor/skills/scripted-skill-from-doc/scripts/compile.py scaffold --source ... --slug ... --out tools/drafts/skills")
    (then "python .cursor/skills/scripted-skill-from-doc/scripts/audit_dag.py tools/drafts/skills/<slug>"))

  (protocol-2-judgment
    (expand-stub-atoms "replace S##/G## placeholders with real curriculum")
    (verify "audit_dag standard ok before offering promote"))

  (protocol-3-promote
    (require "explicit human consent")
    (run "python .cursor/skills/scripted-skill-from-doc/scripts/promote.py tools/drafts/skills/<slug>")
    (overwrite "existing destination needs --force and --overwrite-slug <slug>"))

  (forbidden 'promote-slug-value 'promote-slug-scripted-skill-from-doc 'promote-without-consent 'modify-skills-value))
