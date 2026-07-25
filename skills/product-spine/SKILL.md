---
name: product-spine
description: >
  Use when the user asks which skill to open, where to start on a vibecoded
  project, how to turn an idea into something valuable and marketable, which
  of value / lean-mvp / story-generation-prompt to run next, or how to resume
  across those three. Triages once, names the destination skill, then stops.
  Not for Strategyzer canvas grilling, Dan Olsen lean-mvp pacing, INVEST story
  drafting, or NotebookLM generation prompts — hand those to the named sibling.
metadata:
  activation: explicit
  distribution: monorepo
  pairs_with: value, lean-mvp, story-generation-prompt
disable-model-invocation: true
---

(def-sop product-spine
  (context
    (target "product-spine-skill-agent")
    (optimization "one-human-entry-that-triages-into-value-lean-mvp-or-story")
    (references
      (path references/path.md))
    (siblings
      (value .cursor/skills/value/SKILL.md)
      (lean-mvp .cursor/skills/lean-mvp/SKILL.md)
      (story-generation-prompt .cursor/skills/story-generation-prompt/SKILL.md)))

  <central_idea>
  (center-of-gravity
    (invariant "One slash entry for vibecode to valuable to marketable. Triage names the sibling skill and stops. Value and lean-mvp own their sessions and import bridges. Story stays slash-or-path-read. This skill never runs value or lean scripts and never invents a second session."))
  </central_idea>

  (protocol-0-activation
    (on-activation
      1 "read references/path.md"
      2 "ask at most one clarifying question only when triage cannot choose among the rules below"
      3 "name the destination skill path and the human next move in one short paragraph"
      4 "stop — do not grill canvas atoms, do not draft stories, do not run sibling scripts")
    (forbidden 'run-value-or-lean-scripts 'invent-session-json 'auto-accept-sibling-atoms 'reload-this-skill-after-handoff))

  (protocol-1-triage
    (shared-slug "value and lean-mvp use the same project slug under workproduct/")
    (value-session "workproduct/value-proposition/<slug>/session.json")
    (lean-session "workproduct/lean-mvp/<slug>/session.json")
    (rules
      (both-sessions
        "prefer the skill whose module gate is still incomplete"
        "if both incomplete, prefer value until profile and value-map gates are done, else lean-mvp"
        "tell the human to open that skill; its own activation resumes and imports")
      (one-session "open the skill that owns that session.json")
      (no-session-repo-claim
        "finished repo or docs needing an honest shareable claim → read .cursor/skills/story-generation-prompt/SKILL.md and follow its NotebookLM recon or draft-story path")
      (no-session-idea
        "bare idea or weak customer clarity → open .cursor/skills/value/SKILL.md")
      (no-session-mvp
        "MVP feature ask with no session → open value first; lean still needs customer context. Open lean-mvp only when the human explicitly confirms skip-value and accepts re-grilling segment in lean"))
    (voice
      (shape "one paragraph, one named destination, no atom IDs")
      (rationale "one plain sentence why this destination won — e.g. value profile done lean scope open, or no session so start value")
      (slug "when a slug is known or derivable, say it once so the human can find workproduct paths")
      (optional-slash "siblings may be invoked by the human later; this turn only names the path to read or the skill to open")))

  (protocol-2-return
    (note "Import bridges already move answers between value and lean. After MVP learning, experiment results, or a story kill-signal, tell the human to reopen value or lean-mvp; do not invent a spine learn-loop engine.")
    (when-retriage "if the human is lost again, they invoke /product-spine — do not instruct siblings to read this SKILL.md in a loop"))
)
