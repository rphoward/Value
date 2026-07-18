---
name: value
description: >
  Value skill package (stub). Use when developing or invoking the Value skill
  distributed from this GitHub repo. Replace this description with concrete
  triggers once the workflow is defined. NOT for scaffold-init, Eliot style
  analysis, or unrelated repo tooling.
paths: .cursor/skills/value/**
disable-model-invocation: true
metadata:
  activation: explicit
  distribution: github
---

(def-sop value
  (context
    (target "value-skill-agent")
    (optimization "github-distributable-skill-package")
    (references
      (workflow references/workflow.md)))

  <central_idea>
  (center-of-gravity
    (invariant "This package is the ship surface for the Value skill. Keep SKILL.md focused; put deep material under references/; keep scripts thin."))
  </central_idea>

  (protocol-1-layout
    (enforce (skill-root ".cursor/skills/value/"))
    (dirs
      (SKILL.md "entry, triggers, workflow")
      (references/ "progressive disclosure")
      (scripts/ "thin helpers")
      (assets/ "templates and fixtures")))

  (protocol-2-authoring
    (follow 'skill-authoring.mdc)
    (follow 'skills-repo.mdc)
    (forbidden 'fat-scripts-with-domain-logic)
    (note "Replace this stub with the real workflow before distribution.")))
