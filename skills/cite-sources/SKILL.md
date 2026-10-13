---
name: cite-sources
description: >-
  Use whenever you report on, summarize, quote, or reference a specific email,
  thread, doc, sheet, page, file, PDF, task, issue, or PR. Link every object
  you mention inline to its own URL and cite your sources. Meant to be always
  on; works with any agent tool or connector.
---
# Cite sources

Every specific object you mention gets an inline markdown link to that object's
own URL. The reader should reach the source in one click.

**Always on.** Skills load only when matched, so harnesses should reference this
skill from `AGENTS.md` or always-loaded memory, e.g.:
"Always link any object you mention to its own URL; see `cite-sources`."

## Rules

1. Link inline at first mention: `[Q3 budget thread](<url>)`, not a bare URL or
   a footnote dump at the end.
2. Use the object's own URL. Never a search results page, an inbox, a folder,
   a workspace homepage, or a repo root when you mean a specific item.
3. Build the URL from the ID your tool returned. Do not guess or invent IDs.
4. Cite what you relied on. When you summarize, compare, or answer from
   sources, link each one you used.
5. No URL available? Say so plainly: "(no link available: the tool returned no
   thread ID)". Do not leave it silently unlinked and do not fake one.
6. Use a short, human link label (subject, title, task name, `#123`), not the
   raw ID.

## URL patterns

| Object | URL |
| ------ | --- |
| Gmail thread | `https://mail.google.com/mail/u/0/#all/<threadId>` |
| Notion page | The page URL the tool returns (`https://www.notion.so/<slug>-<pageId>`) |
| Google Doc | `https://docs.google.com/document/d/<id>/edit` |
| Google Sheet | `https://docs.google.com/spreadsheets/d/<id>/edit` |
| Drive PDF or file | `https://drive.google.com/file/d/<id>/view` |
| Todoist task | `https://app.todoist.com/app/task/<id>` |
| GitHub PR | `https://github.com/<owner>/<repo>/pull/<number>` |
| GitHub issue | `https://github.com/<owner>/<repo>/issues/<number>` |

For other sources, prefer the canonical permalink the tool or app returns.
Gmail `u/0` assumes the first signed-in account; adjust if the account index is
known.

## Examples

Good:

- "Ana confirmed the date in [Venue contract — final](https://mail.google.com/mail/u/0/#all/18f2a…)."
- "The numbers come from [Q3 forecast](https://docs.google.com/spreadsheets/d/1AbC…/edit), tab *Summary*."
- "Fixed in [#42](https://github.com/acme/app/pull/42); closes [#40](https://github.com/acme/app/issues/40)."
- "Ana mentioned a signed PDF, but it isn't in Drive, so there's no link available."

Bad:

- "Ana confirmed the date in her email." (no link)
- "See [your inbox](https://mail.google.com/)." (homepage, not the thread)
- "Found it in [Drive search](https://drive.google.com/drive/search?q=forecast)." (search page)
- "Here: https://docs.google.com/document/d/1AbC…/edit" (bare URL, no label)
