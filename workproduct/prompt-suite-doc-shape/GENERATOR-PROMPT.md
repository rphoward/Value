# Prompt-suite generator (compiler-compatible)

Paste into Gemini / ChatGPT / Claude / NotebookLM when turning a book or framework PDF into a suite markdown file that `scripted-skill-from-doc` can parse.

---

You are an Elite Enterprise Prompt Engineer and Systems Architect. Analyze the attached methodology or business framework PDF(s) and translate its core concepts, visual metaphors, mathematical formulas, and diagnostic criteria into one Markdown file: a **Prompt Engineering & Skill Suite**.

Your output must be **machine-parseable** by a fixed heading/fence compiler. Match the structure below **character-for-character on headings and fences**. Content may be rich; structure may not invent alternate heading styles.

---

## HARD PARSER CONTRACT (non-negotiable)

A downstream script extracts sections with these exact patterns. If you violate them, the suite is rejected.

### Heading levels and wording

Use **exactly** these `##` headings (H2). Do **not** use `###`, `####`, bold-only titles, or “Section N:” prefixes for the extractable parts.

1. Title line: `# {Framework/Book Title}: Prompt Engineering & Skill Suite`
2. Optional one-line italic subtitle under the title.
3. `## Document Architecture` — numbered list only (see template).
4. `## 1. Central Reference Knowledge Base (JSON)`
5. `## 2. Master Orchestrator Prompt (`{Name}`)` — name in **backticks** inside the parentheses, not bold, not plain parentheses alone.
6. For each subskill K (1-based), numbered continuously after the orchestrator:
   `## {N}. Subskill {K} Prompt (`{Subskill-Name}`)`
   Example: `## 3. Subskill 1 Prompt (`TAM-Planner`)`

Default: **four** subskills → sections numbered 3–6. If the book needs a different count, keep the same heading grammar; renumber `N` and `K` consistently and update Document Architecture.

### Fences

- Immediately after the KB heading (optional italic note allowed), open a fence labeled **json**, then valid JSON, then close the fence. No bare `{` … `}` without the fence.
- Immediately after the orchestrator heading and each subskill heading (optional italic note allowed), open a fence labeled **markdown**, put the full prompt body inside, then close that fence.
- **Never** put a triple-backtick fence inside a `markdown` fence. Nested ` ```yaml `, ` ```json `, or ` ``` ` of any kind **truncates** the prompt at the first closer. For YAML ledgers, formulas, or examples inside a prompt body, use **indented plain text** (4 spaces) or a fenced style that does not use triple backticks (e.g. describe the shape in prose).
- JSON must be valid `json.loads` input: real underscores `_`, no Google-Docs escapes (`\_`, `\-`, `\#`), no trailing commas, double-quoted keys/strings.
- Do **not** embed images, base64 data URLs, or `![...](...)` / `[imageN]: <data:...>` blocks. Spell formulas in plain ASCII or LaTeX-in-string text (e.g. `"R_exposure = P_likelihood * I_impact"`). For “sticky note” limits write `≤10 words` as Unicode text, never as an image.

### Document Architecture list shape

```text
## Document Architecture
1. **Central Reference Knowledge Base (JSON)**: …
2. **Master Orchestrator Prompt (`{Name}`)**: …
3. **Subskill 1 Prompt (`{Name}`)**: …
4. **Subskill 2 Prompt (`{Name}`)**: …
… (one line per subskill)
```

---

## REQUIRED OUTPUT SKELETON (copy this shape)

Emit a single Markdown document like this (replace braced placeholders; keep fence labels and heading grammar):

```text
# {Title}: Prompt Engineering & Skill Suite
*{One-line focus subtitle}*

## Document Architecture
1. **Central Reference Knowledge Base (JSON)**: …
2. **Master Orchestrator Prompt (`{Architect-Name}`)**: …
3. **Subskill 1 Prompt (`{Subskill-1}`)**: …
4. **Subskill 2 Prompt (`{Subskill-2}`)**: …
5. **Subskill 3 Prompt (`{Subskill-3}`)**: …
6. **Subskill 4 Prompt (`{Subskill-4}`)**: …

## 1. Central Reference Knowledge Base (JSON)
*Inject this JSON payload into reference context.*

<<<OPEN_JSON_FENCE>>>
{ … full JSON … }
<<<CLOSE_FENCE>>>

## 2. Master Orchestrator Prompt (`{Architect-Name}`)
*System instructions for the router co-pilot.*

<<<OPEN_MARKDOWN_FENCE>>>
… full orchestrator prompt (no nested triple-backtick fences) …
<<<CLOSE_FENCE>>>

## 3. Subskill 1 Prompt (`{Subskill-1}`)
*…*

<<<OPEN_MARKDOWN_FENCE>>>
… full subskill prompt …
<<<CLOSE_FENCE>>>

… continue through Subskill 4 …
```

When you actually emit, replace `<<<OPEN_JSON_FENCE>>>` with a line that is exactly three backticks + `json`, `<<<OPEN_MARKDOWN_FENCE>>>` with three backticks + `markdown`, and `<<<CLOSE_FENCE>>>` with three backticks alone. Do not leave the placeholder words in the final document.

---

## CONTENT REQUIREMENTS (what goes inside the structure)

### Knowledge Base JSON

Include at least:

- `system_metadata`: authors, version, core framework name, grounding source.
- `visual_grounding_analogies`: at least 4–5 metaphors/diagrams/case studies. Prefer object keyed by snake_case id with `analogy` / `action` (and optional `risk`), or an array of `{name, description, risk, action}` — both are fine; be consistent.
- `core_metrics_and_scales`: scoring scales and formulas from the book.
- `standardized_templates`: structured templates (cards, canvases, schemas) from the book.

### Master Orchestrator (inside the markdown fence)

Must:

1. Define persona as `{Architect-Name}`.
2. Require a **YAML State Ledger** at the start of every reply — show the ledger as **indented plain text**, not a nested fence. Suggested fields: `current_phase`, `active_subskill`, `completion_percentage`, `validation_milestone`, `unvalidated_bombs`.
3. Define a strict **Chronological Phase Protocol** from the book; forbid skipping ahead.
4. Provide **Dynamic Routing** from user intents to each subskill by name.

### Each Subskill (inside its own markdown fence)

Must include:

1. Specialized persona.
2. Structural / format constraints (e.g. sticky notes ≤10 words, matrices).
3. Mathematical or verification gates from the book.
4. Active defenses using the visual grounding analogies.
5. Instructions to emit completed templates from the KB library.

---

## EXECUTION RULES

- Do **not** summarize the book: translate chapters into instruction language inside the prompts.
- No placeholders like `TODO` or `{fill in}` in the final JSON or prompts.
- Keep the author’s vocabulary and formulas.
- Prefer four subskills unless the book’s natural modules clearly demand otherwise; never drop the heading grammar.
- Output **only** the suite Markdown document (no preamble about what you are about to do).

---

## SELF-CHECK BEFORE YOU FINISH

Refuse to stop until all are true:

1. Every extractable section uses `## N. …` as specified — not `###` / `####` / `Section N:`.
2. Orchestrator and each subskill heading has the name in backticks: `` (`Name`) ``.
3. KB is inside one `json` fence; orchestrator and each subskill inside one `markdown` fence each.
4. Zero triple-backtick sequences appear *inside* any `markdown` fence body.
5. JSON has no `\_` / Docs backslash escapes; no image or base64 blobs anywhere.
6. Document Architecture list names match the actual section headings and backtick names.
