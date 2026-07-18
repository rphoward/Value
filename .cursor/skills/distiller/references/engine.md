(def-ref engine
  (linked-from distiller-skill central_idea)

  (section engine-map
    (title "ELIOT Idea Distiller v1.2 — engine map")
    (source-of-truth "eliotworkflow/ELIOT_DISTILLER_v1_2_1.md"))

  (section phases
    (phase 1 (load-order references/idea-extraction.md) "Strip brainstorm style, keep structural argument")
    (phase 2 (load-order references/eliot-mapping.md) "Map to ELIOT-native ThematicPayload")
    (phase 3
      (load-order references/author-matching.md)
      (load-order references/exa-discovery.md)
      "Style candidates + passage lookup")
    (phase 4 deferred "Emulation prompts per author"))

  (section pipeline-context
    (flow
      "user brainstorms → Distiller (phases 1–3) → user chooses author →"
      "ELIOT analyzes source passage → ELIOT emulates using payload →"
      "evaluator scores → optional drift audit"))

  (section consumer
    (primary "ELIOT v5.2+ emulation constraints")
    (also-compatible "downstream image generation if the user reaches that stage")))
