(def-ref need-prioritizer
  (linked-from protocol-2)
  (source "docs/lean-product-playbook-prompt-suite.md — Need-Prioritizer")

  (section module
    (name need-prioritizer)
    (artifact need-prioritizer.md)
    (template assets/need-prioritizer.template.md))

  (section gate-pass
    (canonical "pass need-prioritizer gate"))

  (section stub-note
    (note "Prompt cargo lives in the source suite; expand atoms via FOR_AGENTS")))
