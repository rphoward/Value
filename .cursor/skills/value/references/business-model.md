(def-ref business-model
  (linked-from protocol-2 protocol-3 protocol-4)
  (purpose "Describe how the accepted value map is delivered, funded, operated, scaled, and defended.")
  (score-policy "A 0–10 score is only a discussion aid accompanied by reasons and evidence. Store unknown when evidence cannot support a score.")

  (atom
    (id B01)
    (name "delivery channel")
    (teaches "A channel is how the segment discovers, evaluates, buys, receives, and uses the offering. Delivery comes first because the accepted value map has no business effect unless it can reach the customer.")
    (asks "Through which concrete channel path will the accepted segment discover, buy, receive, and use this offering?")
    (accepts "Describes the applicable channel stages and labels untested stages as hypotheses or unknowns; does not infer customer behavior from the design alone.")
    (writes "append one answers record for B01; append untested channel claims to assumptions with source_atom B01 and missing stages to unknowns; set project.updated_at; set position to business-model/B02/in_progress")
    (unlocks B02))

  (atom
    (id B02)
    (name "customer relationship")
    (teaches "The customer relationship describes the human or automated support required before, during, and after delivery. It follows the channel so relationship work is tied to actual customer contact points.")
    (asks "What relationship must the business maintain with this segment across the accepted channel path?")
    (accepts "Names required acquisition, onboarding, service, retention, or exit interactions and who performs them; marks unestablished requirements unknown.")
    (writes "append one answers record for B02; append unsupported relationship requirements to assumptions and unresolved ownership to unknowns; set project.updated_at; set position to business-model/B03/in_progress")
    (unlocks B03))

  (atom
    (id B03)
    (name "revenue behavior")
    (teaches "Revenue behavior covers who pays, what they commit, whether payment repeats, and whether cash arrives before or after delivery costs. It comes after channels and relationships because those choices shape both willingness to pay and collection timing.")
    (asks "What observed or hypothesized payment behavior will fund this offering, including payer, recurrence, and timing against costs?")
    (accepts "States payer, exchange, recurrence, and cash timing with evidence labels; any 0–10 discussion score includes a reason and source, otherwise remains unknown.")
    (writes "append one answers record for B03; append observed payment behavior to evidence, untested revenue claims to assumptions with source_atom B03, and absent scoring evidence to unknowns; set project.updated_at; set position to business-model/B04/in_progress")
    (unlocks B04))

  (atom
    (id B04)
    (name "key activities and resources")
    (teaches "Key activities are the work the model must perform, and key resources are the assets or capabilities that work consumes. Identifying them now translates the promised delivery and relationship into operational requirements.")
    (asks "Which activities and resources are indispensable to deliver the accepted value map through this model?")
    (accepts "Names indispensable work and assets, identifies whether the business, customers, or partners perform the work, and labels unverified capacity unknown.")
    (writes "append one answers record for B04; append unsupported capacity and others-do-the-work claims to assumptions with source_atom B04; append missing ownership to unknowns; set project.updated_at; set position to business-model/B05/in_progress")
    (unlocks B05))

  (atom
    (id B05)
    (name "partners and costs")
    (teaches "Partners supply work or resources the business does not provide alone, while costs reveal what those choices require. This follows internal operations so partner dependence and structural cost claims can be compared with the actual delivery model.")
    (asks "Which partners and principal cost drivers are required, and what evidence supports any claimed cost advantage?")
    (accepts "Names required partners, dependencies, and principal costs; a claimed cost advantage or 0–10 discussion score includes reasons and evidence, otherwise remains unknown.")
    (writes "append one answers record for B05; append observed cost facts to evidence, untested partner or cost claims to assumptions with source_atom B05, and unsupported cost advantage to unknowns; set project.updated_at; set position to business-model/B06/in_progress")
    (unlocks B06))

  (atom
    (id B06)
    (name "scale constraints")
    (teaches "Scale depends on where demand increases scarce labor, capital, inventory, support, or partner capacity. Examining constraints after activities and costs shows what grows linearly and what can be reused.")
    (asks "As demand grows, which resource or activity becomes the first binding constraint, and what evidence supports that view?")
    (accepts "Names at least one likely constraint and its growth behavior with a labeled basis; any scalability score is reasoned evidence-backed discussion, otherwise unknown.")
    (writes "append one answers record for B06; append observed constraints to evidence, projected constraints to assumptions with source_atom B06, and missing capacity evidence to unknowns; set project.updated_at; set position to business-model/B07/in_progress")
    (unlocks B07))

  (atom
    (id B07)
    (name "switching and defensibility")
    (teaches "Switching behavior and defensibility describe why customers might stay and why competitors cannot quickly erase the model's advantage. They come last in the model analysis because credible protection must arise from accepted delivery, relationship, revenue, resource, or partner choices.")
    (asks "What evidenced switching behavior or hard-to-copy model advantage could protect this business?")
    (accepts "Names a concrete switching factor or defensibility mechanism and its evidence, or records none established; any 0–10 discussion score includes reasons and a source, otherwise unknown.")
    (writes "append one answers record for B07; append observed switching or protection claims to evidence, untested claims to assumptions with source_atom B07, and absent support to unknowns; set project.updated_at; set position to business-model/B08/in_progress")
    (unlocks B08))

  (atom
    (id B08)
    (name "business-model gate")
    (teaches "The business-model gate checks that delivery, relationships, revenue behavior, operations, partners, costs, constraints, and protection are explicit. Passing means the model is testable; unknown scores and assumptions remain visible rather than becoming invented precision.")
    (asks "Should this business model pass its gate now, or should one named atom be reopened?")
    (accepts "Records an explicit pass or reopen decision with a reason and target atom; pass requires every model area to contain accepted content or an explicit unknown.")
    (writes "append one decision-kind answers record for B08; append a decisions record with source_atom B08 and the chosen resulting position; on pass set position to business-model/B08/gate_pending and set business-model.md artifact status pending; on reopen set position to business-model/<chosen-atom>/in_progress; set project.updated_at")
    (unlocks "business-model gate: write business-model.md from accepted business-model state, set its artifact status final, mark business-model completed, then set position to experiments/E01/in_progress")))
