(def-ref path

  (linked-from protocol-0 protocol-1 protocol-2 protocol-3)

  (section phases
    (idea "vibecoded starting point — repo, docs, or bare concept")
    (clarity "value skill — customer profile and value map under workproduct/value-proposition/<slug>/")
    (mvp "lean-mvp skill — underserved needs through MVP scope under workproduct/lean-mvp/<slug>/")
    (claim "story-generation-prompt — INVEST sentence and NotebookLM generation / producer paste; spine loads saved notes first, names the paths, then follows story in the same turn")
    (return "after learning or kill-signal, spine sends human back into value or lean-mvp — siblings keep session.json; spine has no session of its own"))

  (section maya-happy-path
    (note "reference walk — other walks exist; catch edge cases with protocol-1 precedence")
    (step-1 "/product-spine → clarity guide-turn → open /value; done-enough profile + value-map")
    (step-2 "/product-spine → mvp guide-turn → open /lean-mvp; done-enough mvp-scope; lean bounce-back names /product-spine")
    (step-3 "/product-spine → claim → load saved notes + follow story-generation-prompt inline — not a third slash for story, not a paste homework for the human")
    (lost "any time → /product-spine again"))

  (section reading-sibling-state
    (sessions "workproduct/value-proposition/<slug>/session.json and workproduct/lean-mvp/<slug>/session.json")
    (status "run sibling scripts/status.py <session> read-only for module position; never --refresh, accept, init, or import from spine")
    (status-brief "active module / focus only — never treat as clarity-ready or mvp-ready")
    (clarity-ready "profile and value-map module_outcome completed or bypassed — or both milestone files exist on disk as written notes")
    (mvp-ready "mvp-scope module_outcome completed or bypassed")
    (forbidden "invent spine session.json; hand-edit sibling sessions"))

  (section claim-evidence-handoff
    (purpose "Claim must not dump the human at a file hunt. Spine opens the notes already saved for the project, lists the paths in plain words, and hands the contents to story.")
    (value-slug "folder name under workproduct/value-proposition/")
    (must-open-if-present
      "workproduct/value-proposition/<slug>/customer-profile.md"
      "workproduct/value-proposition/<slug>/value-map.md"
      "workproduct/value-proposition/<slug>/north-star-blurb.md")
    (optional-lean-same-slug
      "workproduct/lean-mvp/<slug>/customer-context.md"
      "workproduct/lean-mvp/<slug>/underserved-needs.md"
      "workproduct/lean-mvp/<slug>/mvp-scope.md")
    (guide-turn-files-im-using
      "After Why-this-phase, add a short list titled like Files I'm using (already saved — you do not need to open these)."
      "Bullet every relative path you actually read. Skip bullets for missing files.")
    (then-story "Follow story-generation-prompt in this turn using those file contents as evidence. Do not ask the human to paste profile, map, or north-star.")
    (example-claim-fragment
      "You are here: claim for value-design — you want a Discord pitch and NotebookLM prompt."
      "Why this phase: claim request wins; we use the notes already saved."
      "Files I'm using (already saved — you do not need to open these):"
      "- workproduct/value-proposition/value-design/customer-profile.md"
      "- workproduct/value-proposition/value-design/value-map.md"
      "- workproduct/value-proposition/value-design/north-star-blurb.md"
      "This turn: draft your one honest sentence from those notes, then the NotebookLM paste block.")
    (forbidden
      "Send the human into Explorer to find these files"
      "Ask them to copy-paste profile or map when the files exist"
      "Skip reading existing customer-profile.md or value-map.md for the chosen slug"))

  (section dual-session-precedence
    (claim-intent "pitch, showcase, NotebookLM, video, INVEST, shareable claim → claim phase wins; name what is skipped")
    (both-incomplete "prefer value until clarity-ready, else lean-mvp")
    (both-ready "claim phase — load notes then follow story-generation-prompt")
    (never "grill value or lean atoms from spine; never auto-accept"))

  (section sibling-paths
    (value ".cursor/skills/value/SKILL.md")
    (lean-mvp ".cursor/skills/lean-mvp/SKILL.md")
    (story-generation-prompt ".cursor/skills/story-generation-prompt/SKILL.md")
    (note "installed packs use the same relative .cursor/skills/<name>/ layout"))

  (section voice
    (you-are-here "phase + slug when known + one situation sentence")
    (why-this-phase "one plain sentence why this phase won")
    (files-im-using "claim only — exact paths; say already saved")
    (this-turn "one sibling slash, or claim inline story with a first story action from those files")
    (come-back-when "done-enough + /product-spine re-entry")
    (tone "plain words a teenage vibecoder can follow — no atom codes, no curriculum jargon"))

  (check no-spine-session "product-spine has no scripts/ of its own and no session.json")

  (check claim-exit "sessions complete or claim-intent must reach story-generation-prompt — not an endless value/lean loop")

  (check guide-turn-complete "every activation emits you-are-here, why-this-phase, this-turn, and come-back-when; claim also emits files-im-using when notes exist")

  (check claim-loads-notes "claim phase with a value slug must open customer-profile.md and value-map.md when present and list those paths before drafting")

  (check illegal-claim-route "claim phase forbids naming story-generation-prompt without following SKILL in the same turn")

  (check readiness-not-from-brief "clarity-ready and mvp-ready come from module_outcome or written milestone files, not status active module alone")

  (check no-circular-load "siblings may mention /product-spine for re-entry; they must not read product-spine/SKILL.md every turn"))
