(def-ref path

  (linked-from protocol-0 protocol-1 protocol-2)



  (section phases

    (idea "vibecoded starting point — repo, docs, or bare concept")

    (clarity "value skill — customer profile and value map under workproduct/value-proposition/<slug>/")

    (mvp "lean-mvp skill — underserved needs through MVP scope under workproduct/lean-mvp/<slug>/")

    (claim "story-generation-prompt — INVEST sentence and NotebookLM generation / producer paste; spine reads and follows that skill on claim phase with a first story action in the same turn")

    (return "after learning or kill-signal, spine sends human back into value or lean-mvp — siblings keep session.json; spine has no session of its own"))



  (section maya-happy-path

    (note "reference walk — other walks exist; catch edge cases with protocol-1 precedence")

    (step-1 "/product-spine → clarity guide-turn → open /value; done-enough profile + value-map")

    (step-2 "/product-spine → mvp guide-turn → open /lean-mvp; done-enough mvp-scope; lean bounce-back names /product-spine")

    (step-3 "/product-spine → claim → follow story-generation-prompt inline (first action then INVEST + NotebookLM) — not a third slash for story")

    (lost "any time → /product-spine again"))



  (section reading-sibling-state

    (sessions "workproduct/value-proposition/<slug>/session.json and workproduct/lean-mvp/<slug>/session.json")

    (status "run sibling scripts/status.py <session> read-only for module position; never --refresh, accept, init, or import from spine")

    (status-brief "active module / focus only — never treat as clarity-ready or mvp-ready")

    (clarity-ready "profile and value-map module_outcome completed or bypassed")

    (mvp-ready "mvp-scope module_outcome completed or bypassed")

    (forbidden "invent spine session.json; hand-edit sibling sessions"))



  (section dual-session-precedence

    (claim-intent "pitch, showcase, NotebookLM, video, INVEST, shareable claim → claim phase wins; name what is skipped")

    (both-incomplete "prefer value until clarity-ready, else lean-mvp")

    (both-ready "claim phase — follow story-generation-prompt")

    (never "grill value or lean atoms from spine; never auto-accept"))



  (section sibling-paths

    (value ".cursor/skills/value/SKILL.md")

    (lean-mvp ".cursor/skills/lean-mvp/SKILL.md")

    (story-generation-prompt ".cursor/skills/story-generation-prompt/SKILL.md")

    (note "installed packs use the same relative .cursor/skills/<name>/ layout"))



  (section voice

    (you-are-here "phase + slug when known + one situation sentence")

    (why-this-phase "one plain sentence why this phase won")

    (this-turn "one sibling slash, or claim inline story with a first story action")

    (come-back-when "done-enough + /product-spine re-entry"))



  (check no-spine-session "product-spine has no scripts/ of its own and no session.json")

  (check claim-exit "sessions complete or claim-intent must reach story-generation-prompt — not an endless value/lean loop")

  (check guide-turn-complete "every activation emits you-are-here, why-this-phase, this-turn, and come-back-when")

  (check illegal-claim-route "claim phase forbids naming story-generation-prompt without following SKILL in the same turn")

  (check readiness-not-from-brief "clarity-ready and mvp-ready come from module_outcome only, not status active module")

  (check no-circular-load "siblings may mention /product-spine for re-entry; they must not read product-spine/SKILL.md every turn"))

