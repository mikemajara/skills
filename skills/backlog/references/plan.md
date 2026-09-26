# Plan (product spec)

A plan is the product spec for **one issue**. It is what used to be called a PRD. It is **not** an implementation sequence and not generated code.

## Done when

A competent implementer would not invent **product behavior** or a **direction-locking** stack choice. In scope and out of scope are explicit. Acceptance criteria are testable. Open questions are listed or there are none.

Also on the issue (skip only with a note, typical for `type:nit`):

- **Touch** — rough map of files and/or repos involved. Enough to see overlap with other issues. Not a complete file list, not per-function edits.
- **Direction** — a library, store, or similar **only when leaving it open would fork the implementation** (e.g. Zustand vs Redux for client cart state). Do not list every helper the implementer might import. Prefer what `AGENTS.md` already standardizes.

**A plan does not include:** task order, function outlines, API/schema design as “how we will implement,” or sample code for the implementer to paste. If those appear, strip them — they are implementer’s job.

If the document is too big for one first change, it is not done: **split issues**.

## When to use a file

Prefer the **issue body** as the plan. Use `.backlog/plans/PLAN-[slug].md` only as a draft buffer when the spec is long; fold it into the issue (or leave a pointer) when refine finishes. After that, the issue is canonical.

Skip a separate plan when the issue already meets this bar (`plan skipped: <reason>`).

## Template

```markdown
---
slug: [slug]
title: [title]
status: draft
issue: [issue URL or blank]
created_at: [ISO-8601]
---

# [Title]

## Problem

## Goal

## In scope

## Out of scope

## Acceptance criteria

- [ ]

## Touch

- (paths / repos — rough)

## Direction

- (only if the spec would otherwise fork; else omit or `N/A`)

## Open questions
```

File statuses: `draft` → `ready` (folded into the issue) → delete or pointer. Pointer:

```markdown
---
slug: [slug]
status: promoted
issue: [issue URL]
promoted_at: [ISO-8601]
---

Canonical spec is GitHub Issue #[number].
```
