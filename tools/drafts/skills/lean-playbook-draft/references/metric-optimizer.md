(def-ref metric-optimizer
  (linked-from protocol-2)
  (source "docs/lean-product-playbook-prompt-suite.md — Metric-Optimizer")

  (section module
    (name metric-optimizer)
    (artifact metric-optimizer.md)
    (template assets/metric-optimizer.template.md))

  (section gate-pass
    (canonical "pass metric-optimizer gate"))

  (section stub-note
    (note "Prompt cargo lives in the source suite; expand atoms via FOR_AGENTS")))
