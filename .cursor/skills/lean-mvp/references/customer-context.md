(def-ref customer-context
  (linked-from protocol-2)
  (source "docs/lean-product-playbook-prompt-suite.md — Need-Prioritizer §1 Target Customer")

  (section module
    (name customer-context)
    (playbook-step "Step 1: Determine Target Customer")
    (artifact customer-context.md)
    (template assets/customer-context.template.md))

  (section doctrines
    (space-pen-mirage "No solution-space features until target customer is mapped")
    (follow-me-home "Prefer behavioral observation plans over survey-only discovery")
    (earlyvangelist "Steve Blank five-rung ladder for early adopter fit"))

  (section gate-pass
    (canonical "pass customer-context gate")))
