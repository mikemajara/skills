---
name: google-docs
description: >-
  Use when creating, editing, formatting, reviewing, commenting on, or
  suggesting changes in Google Docs. Connector-agnostic: works with whatever
  Docs tools the current harness exposes.
---
# Google Docs

Thin operating rules for Google Docs across harnesses. Use the Docs tools available in this
session.

## Defaults

- For a standalone draft, prefer **Markdown** for reports and long text, then
  convert it into the Doc once the substance is settled. When collaborating
  in an existing Doc, use `collaboration` and work in that Doc and its threads
  instead of drafting a parallel version in chat.
- One Doc = one coherent artifact. Prefer a clear title over a generic
  "Untitled document".
- Do not invent templates unless the user asks for one.

## Create

1. Confirm title (and folder/parent if the user named one).
2. Create the Doc with the harness Docs tools.
3. Put the body in next — headings and lists from the Markdown draft.
4. Return the Doc URL (or id) so the user can open it.

## Format

Map common Markdown to Docs structure:

| Markdown | Doc |
| -------- | --- |
| `#` / `##` / `###` | Heading 1 / 2 / 3 |
| lists | Bulleted or numbered lists |
| `**bold**` / `*italic*` | Bold / italic |
| links | Named links, not raw URLs when a label exists |
| tables | Native Doc tables when the tool supports them; otherwise keep simple lists |

Keep formatting light. Do not decorate for its own sake.

## Edit

- Prefer editing the existing Doc the user pointed at over creating a duplicate.
- Preserve written content you were not asked to change.

## Comments and suggestions

- **Comments** — questions, review notes, blockers. Not a dumping ground for
  the main body.
- **Suggestions** — proposed wording/structure changes for the owner to accept
  or reject.
- Reply within the requested review or collaboration scope; do not clear
  others' threads unasked.
- Before posting or editing a comment, read `collaboration`'s
  `references/comment-limits.md` for Google constraints. Count the final signed
  text; use its conservative 3,500-unit budget unless a stricter limit applies.
  Do not assume Drive API anchors appear as native text-selection anchors.
- Sign every agent-authored comment and reply with a truthful agent identity
  (for example, `— fx (AI assistant)`), even if native attribution shows the
  user's account. For ongoing collaboration, follow `collaboration`.

## Review

When asked to review a Doc:

1. Read the current Doc (not a stale local copy).
2. Check structure, clarity, and whether it matches the brief.
3. Leave comments or suggestions. For standalone review, summarize the top
   issues in chat. In collaboration, keep the discussion in the threads and
   give a brief status with links and decisions needing input.
