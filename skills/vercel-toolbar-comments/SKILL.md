---
name: vercel-toolbar-comments
description: >
  Use when triaging Vercel Toolbar / preview comment threads into product work —
  batch nits, open or refine issues, ignore noise. Not one comment → one issue.
  Prefer Toolbar API/MCP or `vercel comments` CLI; never drive the browser for this.
---

# Vercel Toolbar comments

Operating rules for **acting on** Vercel Toolbar comment threads (preview /
deployment feedback). Pair with **backlog** when work should become an issue.

This skill is about **triage judgment**, not about wiring push notifications.
There is no reliable public “new Toolbar comment” webhook for most harnesses —
polling or Slack Comments bridges are harness-local routines, not this file.

## Hard rules

1. **Never** open one GitHub issue per thread by default.
2. **Never** use a browser / desktop GUI to read or reply — use the harness’s
   Vercel Toolbar tools (list / get / reply / resolve / react) or the
   `vercel comments` CLI (Threads API). Discover tool names in-session; do not
   invent a connector.
3. Prefer **unresolved** threads. Resolve or reply when triage is done so the
   queue shrinks.
4. Stay inside the **team / project / branch** the human named (or the current
   repo’s Vercel project). Do not roam other teams.

## Read path

1. List unresolved threads for the team (filter by `projectId`, `branch`, or
   `page` when known).
2. Open a thread only when the list line is not enough (full messages + context).
3. Group threads **before** writing issues (see Triage).

## Triage (required)

For each batch of threads, classify every thread into **exactly one** bucket:

| Bucket | When | Action |
| ------ | ---- | ------ |
| **Ignore** | Duplicate, obsolete (already on main), spam, or not actionable | Resolve (or leave with a one-line reply) — **no** issue |
| **Batch nit** | Cosmetic / copy / spacing / tiny UI polish that can ship together | Collect into **one** backlog item (or one existing nit issue); reply on each thread with the issue link |
| **Issue** | Clear bug or product ask with distinct AC | Capture/promote via **backlog** (`phase:research` or `phase:refine`); link the issue on the thread |
| **Refine existing** | Same concern as an open issue | Comment on that issue; reply on the thread with the link — **do not** open a duplicate |
| **Need human** | Ambiguous product call or security/privacy | Reply asking; leave unresolved or mark blocked — do not invent scope |

### Batching rules

- Same page / same component / same “feel” nits → **one** issue with a checklist
  of thread links (or quoted one-liners).
- Distinct user-visible failures → separate issues.
- If backlog dedupe finds an overlap, merge into the existing issue.

## Write path (after classification)

1. Create or update backlog artifacts **first** (issue body with AC when you open
   something).
2. Reply on each thread with: bucket outcome + issue URL (or “won’t fix / already
   fixed” reason).
3. Resolve threads that are fully handled (ignore, batched, fixed, or tracked).
4. Optional: emoji react only when the harness and team use that as a signal —
   never as a substitute for the reply.

## Out of scope

- Auto-filing every new thread on a cron without triage.
- Harness-specific notify wiring (Slack bridge, poll routine) — document those
  outside this skill.
- Implementing the UI fix (that is **backlog** → implement / issue-kickoff).

## Done when

Every thread in the batch has a bucket, a reply (or explicit ignore+resolve),
and any real work lives in **at most** the smallest useful set of backlog
issues — never a 1:1 thread→issue dump.
