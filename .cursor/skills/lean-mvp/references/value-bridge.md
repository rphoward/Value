(def-ref value-bridge
  (linked-from protocol-1 protocol-2 protocol-4)

  (section shared-slug
    (rule "lean-mvp and value skills use the same project slug under workproduct/")
    (value-root "workproduct/value-proposition/<slug>/")
    (lean-root "workproduct/lean-mvp/<slug>/"))

  (section detection
    (on-activation-after-session-exists
      1 "resolve slug from lean-mvp session.json project.slug"
      2 "if workproduct/value-proposition/<slug>/session.json exists run scripts/import_value_context.py <session-path> internally"
      3 "parse JSON stdout; never quote raw script output to the user unless user asks for import details")
    (on-activation-before-lean-session
      1 "during missing-session creation derive slug silently from display name"
      2 "after init_session.py if value session exists for same slug run import_value_context.py before first grill question"))

  (section mapping
    (bridge-asset assets/value-bridge-map.json)
    (atom_map
      (P01 C01 "segment")
      (P02 C06 "observation / situation trigger when present")
      (P03 U01 "primary problem-space benefit after customer-context gate")
      (P11 U01 "priority job merges into top benefit")
      (P07 U02 "pains inform second benefit comparison")
      (P08 U03 "gains inform laddering depth")
      (P09 MS01 "alternatives as competitors column")
      (V01 MS02 "offering boundary informs must-haves")
      (V07 MS03 "differentiation informs performance offense"))
    (import-behavior
      (skip "lean atoms that already have accepted answers")
      (provenance "value-import on imported answer records")
      (never "overwrite user-accepted lean answers with value imports")))

  (section artifacts
    (read "workproduct/value-proposition/<slug>/customer-profile.md for human-readable context only — do not treat as canonical over session.json")
    (write "workproduct/lean-mvp/<slug>/customer-context.md at customer-context gate"))

  (section sibling-bridge
    (reverse "value skill reads lean via its own assets/lean-bridge-map.json and scripts/import_lean_context.py — see value references/lean-bridge.md")
    (never "lean-mvp never writes workproduct/value-proposition paths or modifies value skill files"))

  (section forward-claim
    (after-mvp-scope "when mvp-scope gate is passed or bypassed, tell the human to invoke /product-spine for claim (INVEST + NotebookLM) or the next journey step — lean does not own the shareable pitch")
    (whole-path "when the human asks which skill, where to start, what is next, or feels lost on the vibecode-to-market path, tell them to invoke /product-spine — do not read product-spine/SKILL.md in a loop"))

  (check value-read-only "value skill files and Values repo are never modified by lean-mvp activation"))
