(def-ref underserved-needs
  (linked-from protocol-2)
  (source "docs/lean-product-playbook-prompt-suite.md — Need-Prioritizer §2–3")

  (section module
    (name underserved-needs)
    (playbook-step "Step 2: Identify Underserved Needs")
    (artifact underserved-needs.md)
    (template assets/underserved-needs.template.md))

  (section rules
    (action-verbs "Every benefit uses verb-led grammar in problem space")
    (laddering "One why depth by default — not mandatory five-whys")
    (opportunity-math "Load assets/knowledge-base.json opportunity_formulas; rank by Importance × (1 − Satisfaction)"))

  (section gate-pass
    (canonical "pass underserved-needs gate")))
