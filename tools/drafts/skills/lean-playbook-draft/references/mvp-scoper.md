(def-ref mvp-scoper
  (linked-from protocol-2)
  (source "docs/lean-product-playbook-prompt-suite.md — MVP-Scoper")

  (section module
    (name mvp-scoper)
    (artifact mvp-scoper.md)
    (template assets/mvp-scoper.template.md))

  (section gate-pass
    (canonical "pass mvp-scoper gate"))

  (section stub-note
    (note "Prompt cargo lives in the source suite; expand atoms via FOR_AGENTS")))
