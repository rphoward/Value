---
name: scaffold-init
description: >
  Initialize a new repo from the Twins .cursor scaffold: copy .cursor/, AI-scaffold
  src/tests/pyproject, run scaffold-init.ps1 with -ProductSlug. Use when the user says
  scaffold, new repo, init project, retarget slug, or duplicate Twins layout. Forbid
  manual glob edits — use .cursor/scaffold/retarget-paths.json. NOT for editing Twins
  product code or redesigning presentation UI.
disable-model-invocation: false
metadata:
  activation: intent
  paths: .cursor/scaffold/manifest.json,.cursor/scaffold/scaffold-init.ps1,.cursor/scaffold/**
---

(def-sop scaffold-init
  (context
    (target "scaffold-init-agent")
    (optimization "cursor-first-then-retarget-no-manual-glob-guessing")
    (references
      (human-doc ".cursor/scaffold/INIT.md")
      (quick-start ".cursor/scaffold/README.md")
      (retarget-paths ".cursor/scaffold/retarget-paths.json")))

  <central_idea>
  (center-of-gravity
    (invariant "Copy .cursor/ first; AI scaffolds code with twins paths; scaffold-init retargets slug; never hand-edit rule globs."))
  </central_idea>

  (protocol-1-workflow
    (steps
      (copy-bundle ".cursor/ into empty folder (exclude plans/ optional)")
      (ai-scaffold "src/twins/, tests/, pyproject.toml from repo-layout + layer rules")
      (init ".\.cursor\scaffold\scaffold-init.ps1 -ProductSlug <slug> [-InitGit] [-GitHubRemote url]")
      (verify "pip install -e . && PYTHONPATH=src python -m unittest discover -s tests -v")))

  (protocol-2-forbidden
    (forbidden 'manual-glob-placeholder-edits-in-mdc)
    (forbidden 'copying-full-twins-src-as-template)
    (enforce (retarget-via .cursor/scaffold/retarget.py :list .cursor/scaffold/retarget-paths.json)))

  (protocol-3-manifest-note
    (note "Copied manifest.json still says twins until init — expected; pass -ProductSlug, do not require pre-copy manifest edits")))
