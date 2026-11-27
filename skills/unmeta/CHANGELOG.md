# Unmeta changelog

Versions apply only to this skill. The history below summarizes an earlier, undated entry in the [repository changelog](../../CHANGELOG.md); that entry was not a separate versioned release of Unmeta.

## 0.2.0 — 2026-11-27

- Extend the boundary to unrequested internal discovery context (CRM, call notes, internal chat) and agent-generated checklists or verification reminders (`verify X`, `confirm Y`, `TBD`).
- Explicitly cover visual and tabular customer-/public-facing artifacts (diagrams/SVGs, slide callouts, tables, spreadsheets) alongside prose and questionnaires.
- Add a diagram-callout leakage example and evaluation case (`id: 8`).

## 0.1.0 — 2026-11-03

Initial independent skill version.

- Rename `reader-facing` to `unmeta` and separate authoring instructions from the content being authored; ask when a remark's intended role is ambiguous.
- Add evaluation cases for omissions, ambiguity, explicit disclosures, and revisions.

### Migration from `reader-facing`

Install `unmeta` and retire the old `reader-facing` installation. Existing sessions may need to refresh their skill list or start a new session.
