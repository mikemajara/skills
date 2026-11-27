---
name: unmeta
metadata:
  version: "0.2.0"
description: >-
  Separate the authoring conversation and internal context from the authored
  work. Use whenever drafting, editing, or filling customer- or public-facing
  documents, drafts, emails, questionnaire answers, form comments, posts,
  slides, tables, spreadsheets, or diagrams/SVGs—especially after feedback,
  discovery, or agreement about what to include or omit. Apply even when the
  user does not ask for writing cleanup. Prevent instructions such as "no named
  course", unrequested internal research notes, or agent-side verification
  reminders ("verify X", "confirm Y", "TBD") from leaking into the artifact.
  When unsure whether a remark is guidance for you or content for the recipient,
  always ask the user before including or silently omitting it.
---

# Unmeta

Use the authoring conversation to shape the work. Do not turn that conversation
into the work. The user can discuss wording, scope, evidence, and decisions with
you without intending any of that discussion to appear in the artifact.

## Keep the boundary

Before drafting or editing, distinguish:

- **Authoring conversation and internal context:** instructions, corrections,
  questions, choices, rationale for edits, acknowledgments, internal discovery
  notes (CRM, call notes, internal chat), and agent-generated checklists or
  verification reminders (`verify X`, `confirm Y`, `TBD`) not requested for the
  reader.
- **Authored work:** the substantive artifact intended for its reader—prose,
  emails, questionnaires, slide callouts, diagram labels, or table cells—including
  facts, required explanations, limitations, and uncertainty.

For each relevant remark or finding, act according to its role:

1. **Clearly an authoring instruction or internal context:** apply or keep it
   in the authoring chat only. "Don't name a course" means omit the name, not
   announce that the answer omits one, and do not infer unsupported facts from
   it. Unrequested internal discovery notes and verification reminders
   (`verify X`, `confirm Y`, `TBD`) stay in chat—never slip them into prose,
   diagram labels, slide callouts, or table cells.
2. **Clearly intended content:** include its substance. A negative fact or scope
   boundary belongs when the user wants the recipient to know it.
3. **Unclear which:** always ask the user. Do not guess, silently drop the remark,
   or write a hedged version into the artifact. Ask a targeted question such as
   "Is that background for me, or something you want the recipient to read?"
   Hold the affected passage or field until clarified; leave existing text
   unchanged. Keep the question in the authoring conversation, not in the answer,
   document body, email, or questionnaire comment field. A request for only the
   finished draft does not settle an ambiguous remark.

## Examples

### Questionnaire clarification

- Agent asks: "Should I name a course in this answer?"
- User replies: "No named course for that reply."
- Wrong: "This response does not attach a course outline."
- Right: write the substantive answer without a course name or an announcement
  of the omission. The user did not assert that no course or outline exists.

### Editorial exclusion versus intended fact

- "Don't bring pricing into this email": leave pricing out; do not write
  "Pricing is outside the scope of this email."
- "Tell the customer that pricing is not included in this proposal": include
  that exclusion; it is information for the customer.

### Ambiguous follow-up

While drafting a training answer, the user says "We don't have a course outline."
Without context settling whether this is background or a disclosure for the
recipient, ask: "Should the answer say that no course outline is available, or
is that just background for me?" Do not fill the field while waiting.

### Separate fields

Response: "Not applicable." Comment: "The service does not store payment-card
data." Do not append "Therefore, this response is not applicable." The comment
supplies evidence, not narration of the selected label.

### Diagram or slide callout (internal discovery leakage)

- Context: Internal discovery notes flag an open question to check whether the
  customer's corporate gateway policy allows direct API routing. The user asks
  for a customer-facing architecture diagram with brief value callouts and does
  not ask to include that check.
- Wrong: "Multi-model access and usage caps (verify corporate gateway policy)."
- Right: "Multi-model access and usage caps." Keep the reminder to verify the
  gateway policy in the authoring chat only.

## Check before writing

- Remove announcements of compliance, omitted topics, drafting choices, and
  generic "This document outlines..." introductions that merely echo the brief.
- Strip unrequested internal discovery notes, CRM/chat context, and internal
  reminders (`verify X`, `confirm Y`, `TBD`) from customer- or public-facing
  prose, diagram labels, slide callouts, and table cells.
- Keep the actual explanation. Preserve facts, requirements, uncertainty, and
  limitations; do not weaken "requires an administrator" into "an administrator
  can do it" or invent facts to make the answer complete.
- Check neighboring fields and the thread before repeating context.
- If any sentence's intended role is still uncertain, ask before writing it.

This skill owns the conversation/content boundary, not voice, brevity, tool
mechanics, or permission to edit. Keep useful editorial discussion in its proper
channel and preserve required attribution. Do not strip substantive content just
because it is negative or explicitly discusses scope.
