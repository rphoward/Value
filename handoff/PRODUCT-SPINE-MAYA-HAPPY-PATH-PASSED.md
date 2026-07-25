(def-sop product-spine-maya-happy-path-passed
  (context
    (target "fresh-session-agent-or-human-reviewer")
    (optimization "prove-maya-happy-path-with-real-grilling-no-bypasses")
    (outcome PASS)
    (superseded-by handoff/PRODUCT-SPINE-MAYA-HAPPY-PATH-FAILED.md)
    (note "MIS-CLOSE — compressed bulk-accept walk; treat FAILED as authoritative")
    (closed 2026-07-25)
    (opened-as handoff/PRODUCT-SPINE-MAYA-HAPPY-PATH-OPEN.md)
    (mock-slug shiftswap)
    (prior-gate handoff/PRODUCT-SPINE-UX-MOCK-PASSED.md))

  <central_idea>
  (center-of-gravity
    (invariant "Real Maya grilling reached INVEST + NotebookLM without gate bypasses, spine session.json, or a fifth coordinator. Guide-turn + lean bounce-back held under dogfood.")))

  (protocol-0-outcome
    (result PASS)
    (walk-evidence tools/drafts/product-spine-maya-happy-path/WALK-EVIDENCE.md)
    (friction handoff/decision-trails/product-spine-maya-happy-path.tsv)
    (sessions workproduct/value-proposition/shiftswap/session.json
             workproduct/lean-mvp/shiftswap/session.json)
    (readiness "value profile+value-map completed; lean mvp-scope completed")
    (tests "python -m pytest tests/test_product_spine_skill.py -v → 9 passed"))

  (protocol-1-claim-artifacts
    (invest-sentence "As a restaurant server who needs to trade a shift tonight, I want to post a request and get an explicit confirm from a coworker so that coverage is locked without group-chat chaos.")
    (notebooklm-producer-paste "present in WALK-EVIDENCE.md")
    (note "E/I/S marked reasoned from scope from mvp-scope — not pass-from-sentence-alone"))

  (protocol-2-friction
    (windows-atomic-save "intermittent WinError 5 on session.json.tmp replace during rapid accepts — driver retries; not a spine contract hole")
    (no-skill-orphan "lean forward-claim cued /product-spine; claim followed story inline"))

  (protocol-3-next
    (optional "sync Product-Spine GitHub ship pack when ready")
    (optional "harden value/lean save_session Windows replace if dogfood hits the lock again")))
