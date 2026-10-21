---
name: prompt-schema-authoring
description: Author or update LLM prompts in this repo using the standard <role>/<task>/<input>/<output> structure.
---

# prompt-schema-authoring — global-data

Same as the cross-repo skill (see CityCatalyst). Used here for any LLM-driven helper inside `cc-mage/prompts/` or experimental notebooks.

## Required structure

```md
<role>...</role>
<task>...</task>
<input>JSON object with: - field (type): purpose</input>
<tools>...</tools>          <!-- only if tools exist -->
<output>...</output>
<example_output>...</example_output>
```

Keep prompts under 300 lines. Split by responsibility if longer. Pair every prompt change with the matching Pydantic / dataclass model in code.
