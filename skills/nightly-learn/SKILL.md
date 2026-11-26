---
name: nightly-learn
metadata:
  version: "0.2.0"
  learning: active
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

## Continuous learning

This skill is actively evolving. Default to silence—most sessions need no change.
After finishing the task, suggest a skill amendment only if this session hit a real gap: a wrong/stale rule, a missing step that caused a wrong guess, a recurring user correction, or user frustration with the skill's flow or output. Never suggest wording polish, hypothetical edge cases, or one-off facts.
Format as one brief footnote at the end of your reply: what failed (1 line), the exact 1–3 line diff, and `Reply "apply" to update this skill.`
Never edit silently; on approval, apply the minimal diff to the canonical skill (or route to your skill-owner agent if your instructions delegate skill edits).
