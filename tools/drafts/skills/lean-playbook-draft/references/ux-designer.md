(def-ref ux-designer
  (linked-from protocol-2)
  (source "docs/lean-product-playbook-prompt-suite.md — UX-Designer")

  (section module
    (name ux-designer)
    (artifact ux-designer.md)
    (template assets/ux-designer.template.md))

  (section gate-pass
    (canonical "pass ux-designer gate"))

  (section stub-note
    (note "Prompt cargo lives in the source suite; expand atoms via FOR_AGENTS")))
