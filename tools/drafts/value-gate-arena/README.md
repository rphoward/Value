# Value-map gate presentation arena

Throwaway mocks for V08 gate review on `value-design` session.

**Consumer:** operator resuming at value-map gate (not every turn).

**Failure criteria (from session evidence):**
- Text wall / not understandable
- Monolithic Mermaid could not show whole picture
- Tables and dense prose in chat
- cognitive_murder violation (too much abstract info at once)

**Success criteria:**
- Answer "does this map pass?" in under two minutes
- Progressive disclosure; one primary question per turn at gate
- Honest weak/conditional fit labels (no fake tight links)

| Mock | Strategy | File |
|------|----------|------|
| A | Three-beat disclosure (who → box → links one-at-a-time) | `mock-a-three-beat.md` |
| B | Ad-lib pitch first, diagram optional on ask | `mock-b-adlib-first.md` |
| C | Split stickies + inline fit strength (no matrix table) | `mock-c-split-stickies.md` |
| D | Gate_Review_Lens (strip + quoted gate brief, drill on ask) | `mock-d-gate-lens.md` |

## Pick (recorded)

**Dogfood first:** Mock C inline — `mock-c-dogfood.md` ([Architecture judge](ececb3ee-90e2-4d95-80d7-c4289199ee23): smallest SKILL-only diff).

**Fallback if C still dense:** D+A composite — `mock-winner-d-plus-a-drill.md` ([Rubric judge](c6e9c132-b957-4157-a1e3-38617d3d724f) ranked D first).

**Voice reference:** [Prose judge](ec7a2a82-c2e0-4416-81f0-f3cf447b8559) ranked A first for peer who+freeze rhythm. Borrow into C/D turns, not B ad-lib wall.
