# Agent conversation changelog

Versions apply only to this skill.

## 0.1.0 — 2026-11-04

- Add a Herdr-backed conversation bridge for talking to a verified live agent, relaying follow-ups, and reporting unresolved disagreement.
- Require Herdr's official agent skill and an inherited Herdr pane; avoid implicit agent creation or unbounded exchanges.
- Allow guarded raw pane input when Herdr cannot recognize a known foreground agent, with identity/readiness checks and output-based verification; never use it to bypass a blocked recognized agent.
