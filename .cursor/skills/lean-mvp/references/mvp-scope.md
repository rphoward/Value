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
    (invest "Load invest_user_story_rubric; every v1 story passes INVEST gate")
    (roi "High return + low effort first; delete bucket 8/9 waste"))

  (section gate-pass
    (canonical "pass mvp-scope gate")))
