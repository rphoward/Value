(def-ref craft-ask
  (linked-from protocol-0b-invent-session)

  (section purpose
    (title "Evocative craft ask before first seed draft")
    (goal "Capture feel, example, storyline, seed count, and register only when the originating prompt left them out.")
    (forbidden 're-ask-what-prompt-already-stated 'form-checklist-tone 'generic-pastiche-defaults))

  (section gap-scan
    (check feel "How should the piece feel when finished? (mood, pace, aftertaste)")
    (check example "Is there a short example of the ending or beat they want? (e.g. flash-fiction close that makes people reread)")
    (check storyline "Do they already have a storyline or scene spine in mind?")
    (check content "Are content requirements stated (what must happen / must not)? If missing, stop and ask creatively before write_content_contract")
    (check seed-count "N seeds — from prompt, else ask")
    (check register "literary / technical / essay — from prompt or distiller, else ask")
    (check length-band "Passage/seed length band — from prompt, else ask (still respect 200–2000 resolve_passage bounds)"))

  (section ask-shape
    (when "one or more gaps")
    (style "one plain evocative ask covering only the missing pieces — not a multi-field form")
    (persist
      (content "stated content constraints → write_content_contract / content-brief.md; halt if content still missing")
      (craft "feel, example, storyline, register, length texture → write_craft_brief → craft-brief-v1.md")))

  (section skip
    (when "originating prompt already answers every gap-scan item")
    (action "do not re-ask; write briefs from the prompt + payload and proceed to seeds")))
