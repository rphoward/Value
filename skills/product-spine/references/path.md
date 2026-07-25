(def-ref path
  (linked-from protocol-0 protocol-1 protocol-2)

  (section phases
    (idea "vibecoded starting point — repo, docs, or bare concept")
    (clarity "value skill — customer profile and value map under workproduct/value-proposition/<slug>/")
    (mvp "lean-mvp skill — underserved needs through MVP scope under workproduct/lean-mvp/<slug>/")
    (claim "story-generation-prompt — honest INVEST sentence and optional generation prompt; path .cursor/skills/story-generation-prompt/SKILL.md")
    (return "reopen value or lean-mvp; shared-slug import bridges carry accepted answers — no second spine session"))

  (section dual-session-precedence
    (both-present "resume the skill with an incomplete module gate")
    (both-incomplete "prefer value until profile and value-map gates done, else lean-mvp")
    (never "run status or import scripts from product-spine — the destination skill does that on activation"))

  (section sibling-paths
    (value ".cursor/skills/value/SKILL.md")
    (lean-mvp ".cursor/skills/lean-mvp/SKILL.md")
    (story-generation-prompt ".cursor/skills/story-generation-prompt/SKILL.md")
    (note "monorepo paths; ship-path portability deferred"))

  (section deferred
    (json-to-lisp "large atoms.json and session JSON stay as-is; Lisp pseudo for those surfaces is a later refactor if needed"))

  (section voice
    (rationale "one plain sentence why this destination won")
    (slug "say the shared slug when known"))

  (check no-scripts "product-spine has no scripts/ and no session.json")
  (check no-circular-load "siblings may mention /product-spine; they must not be told to read product-spine/SKILL.md every turn"))
