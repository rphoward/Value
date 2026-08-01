(def-ref path

  (linked-from protocol-0 protocol-1 protocol-2 protocol-3)

  (section phases
    (idea "vibecoded starting point — repo, docs, or bare concept")
    (clarity "value skill — customer profile and value map under workproduct/value-proposition/<slug>/")
    (business "bmg skill — classic Business Model Canvas through ambidexterity under workproduct/bmg/<slug>/")
    (teams "teams skill — Team Alignment Map first, then optional assessor, contract, conflict under workproduct/teams/<slug>/")
    (brand "brand-identity skill — Brand Brief first, then optional identity system, touchpoints, governance under workproduct/brand-identity/<slug>/")
    (mvp "lean-mvp skill — underserved needs through MVP scope under workproduct/lean-mvp/<slug>/")
    (claim "story-generation-prompt — INVEST sentence and NotebookLM generation / producer paste; spine loads saved notes first, names the paths, then follows story in the same turn")
    (return "after learning or kill-signal, spine sends human back into value, bmg, teams, brand-identity, or lean-mvp — siblings keep session.json; spine has no session of its own"))

  (section maya-happy-path
    (note "reference walk — other walks exist; catch edge cases with protocol-1 precedence")
    (step-1 "/product-spine → clarity guide-turn → open /value; done-enough profile + value-map")
    (step-1b "optional canvas-first or business-intent → /bmg; done-enough canvas-mapper (or canvas-mapper.md on disk); bmg bounce-back names /product-spine")
    (step-1c "optional team-friction-intent → /teams; done-enough tam-planner (or tam-planner.md on disk); teams bounce-back names /product-spine — not required before mvp")
    (step-1d "optional brand-intent → /brand-identity; done-enough brand-strategist (or brand-strategist.md on disk); brand bounce-back names /product-spine — not required before mvp")
    (step-2 "/product-spine → mvp guide-turn → open /lean-mvp; done-enough mvp-scope; lean bounce-back names /product-spine")
    (step-3 "/product-spine → claim → load saved notes + follow story-generation-prompt inline — not a third slash for story, not a paste homework for the human")
    (lost "any time → /product-spine again"))

  (section reading-sibling-state
    (sessions "workproduct/value-proposition/<slug>/session.json, workproduct/bmg/<slug>/session.json, workproduct/teams/<slug>/session.json, workproduct/brand-identity/<slug>/session.json, and workproduct/lean-mvp/<slug>/session.json")
    (status "run sibling scripts/status.py <session> --sections read-only for progress-so-far wording; keep readiness from session.json / milestones; never --refresh, accept, init, or import from spine")
    (status-brief "optional agent-internal position hint only — never treat as clarity-ready, business-ready, teams-ready, brand-ready, or mvp-ready; never quote brief or strip symbols to the human")
    (clarity-ready "profile and value-map module_outcome completed or bypassed — or both milestone files exist on disk as written notes")
    (business-ready "canvas-mapper module_outcome completed or bypassed — or workproduct/bmg/<slug>/canvas-mapper.md on disk")
    (teams-ready "tam-planner module_outcome completed or bypassed — or workproduct/teams/<slug>/tam-planner.md on disk")
    (brand-ready "brand-strategist module_outcome completed or bypassed — or workproduct/brand-identity/<slug>/brand-strategist.md on disk")
    (mvp-ready "mvp-scope module_outcome completed or bypassed")
    (forbidden "invent spine session.json; hand-edit sibling sessions"))

  (section claim-evidence-handoff
    (purpose "Claim must not dump the human at a file hunt. Spine opens the notes already saved for the project, lists the paths in plain words, and hands the contents to story.")
    (value-slug "folder name under workproduct/value-proposition/")
    (must-open-if-present
      "workproduct/value-proposition/<slug>/customer-profile.md"
      "workproduct/value-proposition/<slug>/value-map.md"
      "workproduct/value-proposition/<slug>/north-star-blurb.md"
      "workproduct/value-proposition/<slug>/CONTEXT.product.md")
    (must-read-note "when AGENTS.product.md exists beside the value session, honor Always / Ask first / Never product walls")
    (optional-lean-same-slug
      "workproduct/lean-mvp/<slug>/customer-context.md"
      "workproduct/lean-mvp/<slug>/underserved-needs.md"
      "workproduct/lean-mvp/<slug>/mvp-scope.md")
    (optional-bmg-same-slug
      "workproduct/bmg/<slug>/canvas-mapper.md"
      "workproduct/bmg/<slug>/pattern-innovator.md"
      "workproduct/bmg/<slug>/strategy-evaluator.md"
      "workproduct/bmg/<slug>/ambidextrous-execution-designer.md")
    (optional-teams-same-slug
      "workproduct/teams/<slug>/tam-planner.md"
      "workproduct/teams/<slug>/tam-assessor.md"
      "workproduct/teams/<slug>/team-contract-architect.md"
      "workproduct/teams/<slug>/psych-safety-conflict-resolver.md")
    (optional-brand-same-slug
      "workproduct/brand-identity/<slug>/brand-strategist.md"
      "workproduct/brand-identity/<slug>/identity-system-designer.md"
      "workproduct/brand-identity/<slug>/touchpoint-architect.md"
      "workproduct/brand-identity/<slug>/brand-governance-coach.md")
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

  (section vernacular-promote
    (seed "workproduct/value-proposition/<slug>/CONTEXT.product.md — Values build pack only in v1")
    (promote-script "python .cursor/skills/value/scripts/promote_context.py <session-or-CONTEXT.product.md> — dry-run default; --apply merges into repo-root CONTEXT.md")
    (agents-fragment ".cursor/skills/product-spine/assets/AGENTS.fragment.md — or .cursor/skills/value/assets/AGENTS.fragment.md for solo Values install")
    (when-seed-missing-but-bmg-or-lean-or-teams-or-brand "name the gap; say what the human does next (/value same slug, profile segment + trigger, then one pause) and what they get back (CONTEXT.product.md to promote) — no BMG, teams, brand, or lean glossary emitter in v1")

  (section dual-session-precedence
    (claim-intent "pitch, showcase, NotebookLM, video, INVEST, shareable claim → claim phase wins; name what is skipped")
    (brand-intent "logo, brand identity, brand brief, visual identity, Wheeler, Designing Brand Identity, mark topology, brand guidelines, STEPPS touchpoints, brand governance → brand → /brand-identity; do not invent without intent; do not auto-divert mid–value or mid–BMG without that ask")
    (team-friction-intent "team alignment, TAM, contract, psych safety, repo-crew friction → teams → /teams; do not invent without intent; do not auto-divert mid–BMG without that ask")
    (business-intent "BMG, canvas, business-model, canvas-first → business → /bmg; finish canvas-mapper before long-form teams or brand unless team-friction or brand-intent wins; name mid–value Evolve skip when leaving Evolve early")
    (open-bmg "bmg session not business-ready → continue /bmg unless claim, team-friction, brand-intent, or explicit clarity/mvp ask")
    (open-teams "teams session not teams-ready → continue /teams unless claim, brand-intent, or explicit clarity/business/mvp ask")
    (open-brand "brand-identity session not brand-ready → continue /brand-identity unless claim or explicit clarity/business/teams/mvp ask")
    (both-incomplete "prefer value until clarity-ready, else lean-mvp; no invented business, teams, or brand leg without intent or session")
    (both-ready "claim phase — load notes then follow story-generation-prompt")
    (never "grill value, bmg, teams, brand-identity, or lean atoms from spine; never auto-accept"))

  (section sibling-paths
    (value ".cursor/skills/value/SKILL.md")
    (bmg ".cursor/skills/bmg/SKILL.md")
    (teams ".cursor/skills/teams/SKILL.md")
    (brand-identity ".cursor/skills/brand-identity/SKILL.md")
    (lean-mvp ".cursor/skills/lean-mvp/SKILL.md")
    (story-generation-prompt ".cursor/skills/story-generation-prompt/SKILL.md")
    (note "installed packs use the same relative .cursor/skills/<name>/ layout"))

  (section voice
    (you-are-here "phase + slug when known + one situation sentence; when a session exists include progress so far in plain words from --sections — not a fifth beat")
    (why-this-phase "one plain sentence why this phase won")
    (files-im-using "claim only — exact paths; say already saved")
    (this-turn "one sibling slash (/value, /bmg, /teams, /brand-identity, or /lean-mvp), or claim inline story with a first story action from those files")
    (come-back-when "done-enough + /product-spine re-entry")
    (tone "plain words a teenage vibecoder can follow — no atom codes, no curriculum jargon, no status stdout or strip symbols")
    (notebooklm "when giving video steps: Do this → 1 upload folder 2 Chat Box A 3 Video Box B — never a wall of options")
    (example-clarity-reentry-fragment
      "You are here: clarity for value-design — progress so far: profile done; still on value-map pains."
      "Why this phase: value map is not done-enough yet."
      "This turn: open /value and finish the open value-map question."
      "Come back when: profile and value-map gates pass (or you are lost) — invoke /product-spine again.")
    (example-business-fragment
      "You are here: business for tlbmc — you asked for a classic Business Model Canvas first."
      "Why this phase: canvas-first business-intent wins."
      "This turn: open /bmg and map the nine blocks."
      "Come back when: canvas-mapper gate passes (or you are lost) — invoke /product-spine again.")
    (example-teams-fragment
      "You are here: teams for shiftswap — the repo crew is misaligned on who owns what."
      "Why this phase: team-friction intent wins."
      "This turn: open /teams and build the Team Alignment Map."
      "Come back when: tam-planner gate passes (or you are lost) — invoke /product-spine again.")
    (example-brand-fragment
      "You are here: brand for shiftswap — you asked for a brand brief and mark direction."
      "Why this phase: brand-intent wins."
      "This turn: open /brand-identity and build the Brand Brief."
      "Come back when: brand-strategist gate passes (or you are lost) — invoke /product-spine again."))

  (check no-spine-session "product-spine has no scripts/ of its own and no session.json")

  (check claim-exit "sessions complete or claim-intent must reach story-generation-prompt — not an endless value/bmg/teams/brand/lean loop")

  (check guide-turn-complete "every activation emits you-are-here, why-this-phase, this-turn, and come-back-when; when a session exists you-are-here carries progress so far; claim also emits files-im-using when notes exist")

  (check claim-loads-notes "claim phase with a value slug must open customer-profile.md and value-map.md when present and list those paths before drafting")

  (check illegal-claim-route "claim phase forbids naming story-generation-prompt without following SKILL in the same turn")

  (check readiness-not-from-brief "clarity-ready, business-ready, teams-ready, brand-ready, and mvp-ready come from module_outcome or written milestone files, not status active module alone")

  (check no-circular-load "siblings may mention /product-spine for re-entry; they must not read product-spine/SKILL.md every turn"))
