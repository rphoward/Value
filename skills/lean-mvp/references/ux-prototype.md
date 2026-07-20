(def-ref ux-prototype
  (linked-from protocol-2)
  (source "docs/lean-product-playbook-prompt-suite.md — UX-Designer")

  (section module
    (name ux-prototype)
    (playbook-step "Steps 5–6: MVP Prototype & Customer Test")
    (artifact ux-prototype.md)
    (template assets/ux-prototype.template.md))

  (section rules
    (iceberg "Bottom-up: conceptual → IA → interaction → visual last")
    (test-matrix "Load assets/knowledge-base.json mvp_test_matrix_2x2")
    (ramen "Think-aloud, no-help rule, Sean Ellis PMF wrap-up")
    (usability-vs-pmf "Separate ease-of-use findings from value-created findings"))

  (section gate-pass
    (canonical "pass ux-prototype gate")))
