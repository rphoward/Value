(def-ref metrics
  (linked-from protocol-2)
  (source "docs/lean-product-playbook-prompt-suite.md — Metric-Optimizer")

  (section module
    (name metrics)
    (playbook-step "Post-Launch: Lean Product Analytics Process")
    (artifact metrics.md)
    (template assets/metrics.template.md))

  (section rules
    (equation "Peel the onion — custom business equation with levers")
    (ltv-cac "Load assets/knowledge-base.json ltv_cac_ratio_bands")
    (aarrr "Acquisition Activation Retention Revenue Referral — retention before acquisition spend")
    (mtmm "One metric that matters most per optimization cycle"))

  (section gate-pass
    (canonical "pass metrics gate")))
