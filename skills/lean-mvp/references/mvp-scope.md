(def-ref mvp-scope
  (linked-from protocol-2)
  (source "docs/lean-product-playbook-prompt-suite.md — MVP-Scoper")

  (section module
    (name mvp-scope)
    (playbook-step "Steps 3–4: Value Proposition & MVP Feature Set")
    (artifact mvp-scope.md)
    (template assets/mvp-scope.template.md))

  (section rules
    (kano "Load assets/knowledge-base.json kano_model_categories; must-haves before delighters")
    (invest "Load invest_user_story_rubric; every v1 story records one result per letter, each pass, fail, not answerable here, or reasoned from scope with a named basis")
    (roi "High return + low effort first; delete bucket 8/9 waste"))

  (section stories-assist
    (on-request "When the user asks for help writing, sharpening, or converting the INVEST story, read .cursor/skills/story-generation-prompt/SKILL.md and follow it")
    (returns "A story card, an INVEST-plus reading, and on request a generation prompt — all chat output for the user to read")
    (forbidden 'auto-accept-atom-from-that-skill))

  (section gate-pass
    (canonical "pass mvp-scope gate")))
