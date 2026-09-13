---
name: backlog
version: 2.1.0
description: |
  Lightweight project backlog: capture work, keep issues honest, and move them
  through research, refine, implement, and qa. Use when initializing `.backlog/`,
  capturing or promoting ideas, reviewing or triaging issues, refining a product
  plan, checking what to do next on an issue, catching up after time away,
  checking collision with other agents before starting, or consolidating
  `.backlog/memory.md` into `AGENTS.md` (coding agents). Default source of
  truth is GitHub Issues. Read references only for the current action.
---

# Backlog

Skill version **2.1.0**. Label schema **3**.

Issues are the source of truth (GitHub by default). Create the smallest artifact
that reduces ambiguity. Labels are a signal: audit them against the issue before
trusting them.

## What to do next

Returning, catching up, or checking collision before your own task: open
`references/catch-up.md` only. **Read-only** — do not continue into the
list below.

1. **Review** — claimed work (`status:doing`) first, then duplicates, then sort by phase.
2. **Triage** — pick unblocked work; prefer `priority:high`, then medium, then low.
3. **Audit** — labels vs body vs any plan file. Fix drift and say why. See `references/drift.md`.
4. **Claim** — `status:doing` (remove `status:open`).
5. **Act** — open the reference for the current `phase:*` (index below).
6. **Finish** — durable result on the issue; advance `phase:*` or `status:blocked`; restore `status:open` unless blocked. Clear `doing`.

Do not change `phase:*` unless that phase actually finished.

## Artifacts

```text
.backlog/
  inbox.md      # optional local scratch; the issue is the real inbox
  plans/        # product plans only, when the issue body is not enough
  memory.md     # transactional project log (decisions, facts, choices, gotchas)
```

| Artifact | Role |
| -------- | ---- |
| **Issue** | Canonical unit of work. One issue ≈ one coherent first change. |
| **Plan** | Product spec for that issue: problem, goal, in/out, AC. **No** files, APIs, or task order. |
| **Research brief** | Facts and questions before a plan. Not AC. Lives as an issue comment (file optional). |
| **Inbox** | Optional local line items until promoted. |
| **memory.md** | Transactional log for the repo. Promote lasting guidance into `AGENTS.md` — see `references/long-term-memory.md`. |
| **AGENTS.md** | Project soul for coding agents (outside `.backlog/`). |

Writing the plan **is refine**. If the work is too big, split into more issues. Do not keep a separate implementation-plan document.

## Label definition

Exactly one of each axis on an open issue this skill manages. Names live in `references/labels.json`.

**`type:*`** — `feat` | `fix` | `nit`

**`priority:*`** — `high` | `medium` | `low`

**`phase:*`** (pipeline)

| Label | Means |
| ----- | ----- |
| `phase:research` | Facts are thin |
| `phase:refine` | Shape the plan until it is done |
| `phase:implement` | Plan is done or skipped; make the change |
| `phase:qa` | Change exists; judge it against the plan |

**`status:*`** (claim overlay, not a phase)

| Label | Means |
| ----- | ----- |
| `status:open` | Available |
| `status:doing` | Claimed |
| `status:blocked` | Waiting on a human or dependency |
| `status:duplicate` | Same as another issue; close it |

Skip `phase:research` when facts are enough. Skip a plan *file* when the issue body already is a complete plan (`plan skipped: <reason>`). See `references/workflow.md`.

## References

Read only what the current action needs (one level from this file):

| When | Open |
| ---- | ---- |
| Unsure about skips or phases | `references/workflow.md` |
| `phase:research` | `references/research.md` |
| What a plan is / whether it is done | `references/plan.md` |
| `phase:refine` | `references/refine.md` |
| `phase:implement` | `references/implement.md` |
| `phase:qa` | `references/qa.md` |
| Labels look wrong | `references/drift.md` |
| Tracker is GitHub (`gh`, scripts) | `references/github.md` |
| Catch-up / collision recap (read-only) | `references/catch-up.md` |
| Consolidate memory → `AGENTS.md` | `references/long-term-memory.md` |

## Capture and promote

Capture: short inbox line, or create an issue immediately (`phase:research` or `phase:refine`, `status:open`).

Promote: shaped issue — title, goal, scope, AC as known, one label per axis. Never paste a plan dump into an unrelated issue. After promote, drop the inbox line or replace it with the issue URL.

Dedupe before add or promote (inbox, `plans/`, `memory.md`, issues). Helper: `backlog-dedupe.mjs` in `references/github.md`.

## Review and triage

Review does not pick the next task; triage does.

1. List `status:doing`. Resume or unblock before starting something new.
2. Dedupe overlapping open issues; close extras as `status:duplicate` with `Duplicate of #N`.
3. Sort remaining by `phase:*`. Confirm `status:blocked` still has a linked reason.
4. Optional: dirty-vs-main PR sweep — propose close vs rebase for open PRs behind
   the default branch (`references/implement.md`).

## Execute (`phase:implement`)

1. Read the issue (canonical) and the plan if one exists.
2. Keep the change inside that product scope. Do not invent behavior the plan left open — send back to `phase:refine` or `status:blocked`.
3. Follow PR/issue hygiene in `references/implement.md` (one active PR per
   concern; close superseded issue+PR in the same turn; no orphan drafts).
4. When a reviewable change exists, set `phase:qa` and `status:open` (clear `doing`).
5. Record durable decisions, facts, choices, and gotchas in `.backlog/memory.md`
   (transactional log — see `references/long-term-memory.md`).

## Long-term memory (coding agents)

When the user asks to consolidate backlog memory, promote to AGENTS, or work on
long-term memory, follow `references/long-term-memory.md`: move lasting
conventions / gotchas / critical decisions from `.backlog/memory.md` into
`AGENTS.md`, then prune memory. On merge conflicts in `memory.md`, keep all
entries.

## Setup

Prefer `scripts/backlog-setup.mjs` (idempotent): scaffold `.backlog/`, agent hint, upsert labels. Flags and `gh` recipes: `references/github.md`.

Optional snapshot: `scripts/backlog-sync.mjs` → `.backlog/issues.md` (generated, read-only).

## Migration

- `status:unknown` → `phase:refine` + `status:open`
- `status:ready` → `phase:implement` + `status:open`
- `status:needs-plan` → `phase:refine` (shaping is refine; there is no plan phase)
- `.backlog/prds/` → treat as plans or fold into issues; stop creating PRDs
- Implementation-sequence PLAN files → delete or ignore; sequencing is implementer’s job

Setup does not delete legacy labels. Rerun setup to stamp schema 3 names.

## Rules

- Smallest useful artifact.
- One active implement PR per concern; close superseded issue+PR when a
  merge folds older work (`references/implement.md`).
- Issues are canonical; do not keep a second editable copy of promoted work.
- A plan has no implementation details.
- Split oversized work into more issues; do not add a parent PRD.
- Never let a local markdown file override issue labels.
- When blocked, write the blocker on the issue.
- Preserve human-written memory.
- `.backlog/memory.md` is a log: on merge conflict, keep all changes (never drop entries).
