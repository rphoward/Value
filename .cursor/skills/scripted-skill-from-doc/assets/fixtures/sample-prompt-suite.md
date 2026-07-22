# Sample Prompt Suite: Demo Book
*A tiny fixture so you can try the compiler without another document.*

---

## Document Architecture
1. **Central Reference Knowledge Base (JSON)**
2. **Master Orchestrator Prompt (`Demo-Architect`)**
3. **Subskill 1 Prompt (`Context-Mapper`)**
4. **Subskill 2 Prompt (`Scope-Cutter`)**

---

## 1. Central Reference Knowledge Base (JSON)

```json
{
  "system_metadata": {
    "framework": "Demo Suite",
    "version": "0.1",
    "grounding_source": "fixtures/sample-prompt-suite.md"
  },
  "visual_grounding_analogies": {
    "build_before_learn": {
      "analogy": "Shipping features before you know who hurts.",
      "action": "Lock customer context before scope."
    }
  }
}
```

---

## 2. Master Orchestrator Prompt (`Demo-Architect`)

```markdown
You are Demo-Architect. Ask one question at a time. Keep a durable session. Finish context before scope.
```

---

## 3. Subskill 1 Prompt (`Context-Mapper`)

```markdown
You are Context-Mapper. Define the customer and their problem in plain language.
```

---

## 4. Subskill 2 Prompt (`Scope-Cutter`)

```markdown
You are Scope-Cutter. Cut the smallest useful slice that addresses the mapped context.
```
