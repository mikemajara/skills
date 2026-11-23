---
name: nightly-learn
metadata:
  version: "0.2.0"
description: >-
  Review your own memories, separate pure facts from reusable processes, and
  emit one short proposal card per skill-worthy finding. Use on scheduled
  nightly runs or when asked to clean up memory into skills.
---

# Nightly learn

Audit your own memories and promote reusable procedures into skills.

## Gate: memory vs. skill

- **Keep in memory:** facts, preferences, names, one-off decisions, or temporary state.
- **Promote to a skill:** recurring steps, rules ("always/never when doing X"), formats, or checklists that should apply every time the task runs.

## Steps

1. **Inspect your own memories** (never other agents' private memories).
2. **Classify each entry** with the gate above. Skip pure facts and rules already covered by the owning skill.
3. **Pick one target per finding:**
   - Existing skill owns the domain → minimal patch.
   - No owner and reusable → new thin skill.
4. **Emit one independent card per finding** to the configured review destination (or chat if none is configured). One run may produce several cards, or zero if nothing qualifies. Keep every card short and scannable:
   - **Title & one-line summary** of the change.
   - **Target skill** and the **exact minimal edit**.
   - **Brief reason** (the memory or pattern it came from).
5. **Wait for approval** before editing shared skills or deleting memory. Once approved, apply the edit and replace or remove the duplicated memory with a short pointer to the skill.
