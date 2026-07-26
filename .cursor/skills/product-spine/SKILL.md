---
name: product-spine
description: >
  Use when the user asks where to start on a vibecoded project, how to turn an
  idea into something valuable and marketable, how to resume across value /
  lean-mvp / story-generation-prompt, or wants a guide from idea through an
  honest pitch or NotebookLM video prompt. Carries the whole journey: names
  the phase, the sibling to open, what "done enough" means, and the claim exit.
  Not for Strategyzer canvas grilling, Dan Olsen lean-mvp atom pacing, or
  drafting INVEST/NotebookLM copy itself — those stay in the named sibling;
  this skill routes and stays with the human until the path is clear.
metadata:
  activation: explicit
  distribution: github
  pairs_with: value, lean-mvp, story-generation-prompt
disable-model-invocation: true
---

(def-sop product-spine
  (context
    (target "product-spine-skill-agent")
    (optimization "one-human-guide-from-vibecode-to-valuable-to-marketable")
    (references
      (path references/path.md))
    (siblings
      (value .cursor/skills/value/SKILL.md)
      (lean-mvp .cursor/skills/lean-mvp/SKILL.md)
      (story-generation-prompt .cursor/skills/story-generation-prompt/SKILL.md)))

  <central_idea>
  (center-of-gravity
    (invariant "One slash entry carries the human from vibecode to valuable to marketable. Spine owns phase, next move, and done-enough. Value and lean-mvp own session.json and grilling. Story owns INVEST and NotebookLM prompts. Spine never invents its own session — it reads sibling sessions (and may run status.py read-only). When the phase is claim, spine reads story-generation-prompt and follows it so the human is not dumped at the last door."))
  </central_idea>

  (protocol-0-activation
    (on-activation
      1 "read references/path.md"
      2 "discover project slug: look under workproduct/value-proposition/*/session.json and workproduct/lean-mvp/*/session.json; prefer a value slug when claiming; if several value slugs, ask one clarifying question (name the project in plain words)"
      3 "when a session exists, run that skill's scripts/status.py <session> --sections read-only for progress-so-far wording; keep readiness from session.json / milestone files — optional brief is agent-internal only; do not --refresh, accept, init, or import from spine"
      4 "choose phase with protocol-1; speak protocol-2 voice"
      5 "if phase is claim: run protocol-3 claim-evidence-handoff — read the slug's saved notes from disk, list every path in the guide-turn, then read .cursor/skills/story-generation-prompt/SKILL.md and follow it in this turn using those files as evidence — open with a first story action, not a pointer to another slash and not a request that the human hunt or paste the notes"
      6 "if phase is clarity or mvp: fill guide-turn This-turn with exactly /value or /lean-mvp plus leg purpose; stop grilling — the sibling owns atoms on the next leg"
      7 "close guide-turn Come-back-when: when that leg's done-enough is met (or you are lost), invoke /product-spine again")
    (forbidden 'invent-spine-session-json 'accept-or-init-sibling-atoms 'grill-canvas-or-lean-atoms 'quote-status-stdout-atom-ids-to-user 'ask-human-to-find-or-paste-profile-map-or-north-star-when-those-files-exist)
    (allowed 'read-sibling-session-json 'read-sibling-milestone-md 'run-status-py-read-only 'read-and-follow-story-skill-on-claim-phase))

  (protocol-1-journey
    (shared-slug "value and lean-mvp use the same project slug under workproduct/")
    (value-session "workproduct/value-proposition/<slug>/session.json")
    (lean-session "workproduct/lean-mvp/<slug>/session.json")
    (clarity-ready "value profile and value-map module_outcome each completed or bypassed — never infer from status.py brief active module alone")
    (mvp-ready "lean mvp-scope module_outcome completed or bypassed — or human explicitly skips lean and asks to claim; status brief is position hint only")
    (claim-intent "human asks for pitch, showcase, engagement, INVEST story, NotebookLM, video overview, generation prompt, or shareable claim")
    (phases
      (clarity
        "no value session, or value profile/value-map still open"
        "destination /value — .cursor/skills/value/SKILL.md"
        "done-enough: profile and value-map gates passed or bypassed, then return to /product-spine")
      (mvp
        "clarity-ready and lean incomplete (or human asks MVP features with clarity-ready)"
        "destination /lean-mvp — .cursor/skills/lean-mvp/SKILL.md"
        "done-enough: mvp-scope gate passed or bypassed (MS05 story may use story skill inside lean), then return to /product-spine")
      (claim
        "claim-intent, or clarity-ready and mvp-ready, or no session but finished repo/docs needing an honest shareable claim"
        "destination: protocol-3 then follow .cursor/skills/story-generation-prompt/SKILL.md now — claim turns execute story inline with saved notes; routing-only claim is forbidden"
        "done-enough: human has story sentence and, when they want video, producer paste block for NotebookLM pass 2")
      (return-after-learning
        "after experiment results, prototype learning, or story kill-signal → reopen value or lean-mvp for the module that must absorb learning; say which and why"))
    (precedence
      (claim-intent-wins "if the human clearly wants pitch/video/claim, choose claim even when a value or lean session is still open — say what they are skipping")
      (both-sessions-incomplete "prefer value until clarity-ready, else lean-mvp")
      (one-session "continue that skill's open module unless claim-intent wins")
      (no-session-idea "clarity → /value")
      (no-session-mvp-ask "clarity first → /value; open lean-mvp only when human confirms skip-value and accepts re-grilling segment in lean")
      (no-session-repo-claim "claim → follow story-generation-prompt")))

  (protocol-2-voice
    (guide-turn
      (you-are-here "phase label + project slug when known + one plain sentence of situation; when a session exists, that sentence includes progress so far in plain words translated from --sections section names — e.g. profile done; still on value-map pains; no session means no fake progress line; claim may add at most one short readiness clause such as notes ready for pitch")
      (why-this-phase "one precedence sentence — why this phase won")
      (files-im-using "claim only: bullet the exact relative paths you opened — say you are using the notes already saved; the human does not hunt folders or paste files")
      (this-turn "clarity/mvp/return: exactly one sibling slash and what happens there; claim: follow story-generation-prompt with a first story action in this turn, drafted from Files-im-using")
      (come-back-when "done-enough for that leg + explicit /product-spine re-entry — omit only while already inside claim story work this turn"))
    (shape "short guide-turn in that order — no atom IDs, no script stdout, no section-strip symbols; keep words simple enough for a first-time vibecoder")
    (slug "say the project slug when known")
    (carry "the human should feel guided, not sorted into a queue; spine is the entrance and the re-entrance until claim work is in hand")
    (notebooklm-directions "when claim emits video/NotebookLM steps, follow story-generation-prompt Human how-to: numbered Do this — one upload folder, Chat box = Box A, Video/Studio = Box B; forbidden: long essays or two upload plans")
    (illegal-replies
      "clarity or mvp turn that names a slash without done-enough and /product-spine return cue"
      "claim turn that only routes to story-generation-prompt without reading and following it"
      "claim turn with no first story action (pass-1 question or draft ask)"
      "claim turn that tells the human to find, open, or paste profile, value-map, or north-star when those files exist on disk"
      "claim turn that skips reading existing customer-profile.md or value-map.md for the chosen slug"
      "claim turn that explains NotebookLM in a long essay instead of numbered Do this + Box A + Box B"
      "lean before clarity-ready without explicit skip-value and stated re-grilling cost"
      "treating status.py brief active module as clarity-ready or mvp-ready"
      "quoting status.py stdout, --brief, or section-strip symbols to the user as the guide-turn answer"
      "any sibling init, accept, import, or --refresh from spine"))

  (protocol-3-claim-evidence-handoff
    (when "phase is claim and a value slug is known (or the human just named one)")
    (must-read-if-present
      "workproduct/value-proposition/<slug>/customer-profile.md"
      "workproduct/value-proposition/<slug>/value-map.md"
      "workproduct/value-proposition/<slug>/north-star-blurb.md")
    (optional-lean-if-present
      "workproduct/lean-mvp/<slug>/customer-context.md"
      "workproduct/lean-mvp/<slug>/underserved-needs.md"
      "workproduct/lean-mvp/<slug>/mvp-scope.md")
    (slug-mismatch "value and lean may use different folder names; load value notes for the chosen value slug; only add lean files under that same slug, or skip lean notes — do not invent a merge")
    (missing-profile-or-map "if neither customer-profile.md nor value-map.md exists, say so in plain words and either open /value first or draft from what the human just typed — never pretend the notes exist")
    (hand-to-story "pass the file contents into story-generation-prompt as evidence; story must not ask the human to re-paste those files")
    (see references/path.md section claim-evidence-handoff))
)
