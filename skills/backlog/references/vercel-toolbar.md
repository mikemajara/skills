# Vercel Toolbar comments

Intake path for **Vercel Toolbar / preview comment threads** into the backlog.
Most frontend apps here ship on Vercel, so this sits next to capture — not as a
separate skill.

There is usually no reliable public “new Toolbar comment” webhook. Polling or
Slack Comments bridges are harness-local. This file is **triage judgment** when
you are already acting on a batch of threads.

## Hard rules

1. **Do not default to one issue per thread.** Evaluate each comment: it may be
   a nit for a batch, part of an existing issue, part of a wider problem, or
   genuinely its own issue. One comment → one issue is allowed when that is the
   right call after evaluation — it is just not the default mapping.
2. Use the harness’s Vercel Toolbar **CLI or MCP** (list / get / reply / resolve /
   react), whichever is available. **Not** a browser, headless browser, or
   computer GUI.
3. Prefer **unresolved** threads. Resolve or reply when triage is done so the
   queue shrinks.
4. Stay inside the **team / project / branch** the human named (or the current
   repo’s Vercel project).

## Read path

1. List unresolved threads for the team (filter by project, branch, or page when
   known).
2. Open a thread only when the list line is not enough (full messages + context).
3. Group threads **before** writing issues (see Triage).

## Triage

Classify every thread in the batch into **exactly one** bucket:

| Bucket | When | Action |
| ------ | ---- | ------ |
| **Ignore** | Duplicate, obsolete (already on main), spam, or not actionable | Resolve (or one-line reply) — no new issue |
| **Batch nit** | Cosmetic / copy / spacing / tiny UI polish that can ship together | One backlog item (or existing nit issue) with a checklist of thread links; reply on each thread |
| **Issue** | Clear bug or product ask that stands alone after evaluation | Capture/promote (`phase:research` or `phase:refine`); link the issue on the thread |
| **Refine existing** | Same concern as an open issue | Comment on that issue; reply on the thread with the link — no duplicate |
| **Need human** | Ambiguous product call or security/privacy | Reply asking; leave unresolved or blocked — do not invent scope |

### Batching

- Same page / component / “feel” nits → **one** issue with thread links or quoted
  one-liners.
- Distinct user-visible failures → separate issues when evaluation says so.
- Dedupe against open issues before promoting (see `SKILL.md` / `github.md`).

## Write path

1. Create or update backlog artifacts **first**.
2. Reply on each thread with outcome + issue URL (or won’t-fix / already-fixed).
3. Resolve threads that are fully handled.
4. Optional emoji react only if the team uses that as a signal — not instead of a reply.

## Done when

Every thread in the batch has a bucket and a reply (or ignore+resolve), and real
work lives in the **smallest useful** set of backlog issues.
