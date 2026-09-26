---
name: backlog
description: |
  Catch me up on this repo or project: where work left off, what is in
  flight, open issues and PRs, worktrees, leftover branches, collision
  with other agents. GitHub Issues backlog: capture, triage, research,
  refine, implement, qa, initialize `.backlog/`, promote memory into
  AGENTS.md. Use when the user says catch me up; or asks you to be the
  manager, product manager, or orchestrator for the backlog cycle (you
  only allocate: start phase workers in Herdr or cmux panes — never the
  Cursor Task tool, never in-chat subagents); or what to do next on an
  issue. Read references only for the current action.
---

# Backlog

Skill version **2.5.0**. Label schema **3**.

Issues are the source of truth (GitHub by default). Create the smallest artifact
that reduces ambiguity. Labels must track the work: audit artifacts and relabel
when they lag (`references/drift.md`). Until corrected, artifacts win.

## What to do next

Match **intent**, not a passphrase.

Returning, catching up, or checking collision **before** your own task: open
`references/catch-up.md` only. **Read-only** — do not continue into the
list below. If this chat is already the PM, skip catch-up — use
`references/pm.md`.

### Manager / product manager / orchestrator

They named that role (“be my PM”, “act as product manager”, “orchestrate”).
“Keep the work going” alone does **not** select this role.

1. **Do not** research, refine, implement, or QA in this chat.
2. **Do not** call Cursor `Task`, `best-of-n-runner`, explore/generalPurpose
   subagents, or any nested agent in this conversation. Those are not workers.
3. Probe the harness in the shell **before** any spawn (see
   `references/spawn.md`): `test "${HERDR_ENV:-}" = 1`, then `herdr pane current
   --current` or `cmux identify --json`.
4. Open `references/pm.md` and `references/spawn.md`. No time window → ping.
   A duration after this role is on (“keep going two hours”) → autonomous.
5. Allocate: claim the issue, spawn one pane worker for the current `phase:*`,
   wait for issue capture + ping. If Herdr and cmux are both missing, block —
   do not fall back to an in-chat agent.

### Solo (this chat does the craft)

They asked *this* chat to capture, triage, research, refine, implement, or QA.

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
| **Plan** | Product spec for that issue: problem, goal, in/out, AC, rough touch (files/repos), direction-locking libs when the spec would otherwise fork. **No** task order, function outlines, or generated code. |
| **Research brief** | Facts and questions before a plan. Not AC. Lives as an issue comment (file optional). |
| **Inbox** | Optional local line items until promoted. |
| **memory.md** | Transactional log for the repo. Promote lasting guidance into `AGENTS.md` — see `references/long-term-memory.md`. |
| **AGENTS.md** | Project context (architecture, stack, commands, policies). Not PM / QA / merge. |

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
| Manager / product manager / orchestrator | `references/pm.md` |
| How to start a phase worker (Herdr / cmux; unattended in-repo) | `references/spawn.md` |
| Consolidate memory → `AGENTS.md` | `references/long-term-memory.md` |
| Vercel Toolbar / preview comments | `references/vercel-toolbar.md` |

## Capture and promote

Capture: short inbox line, or create an issue immediately (`phase:research` or `phase:refine`, `status:open`).

Preview / Vercel Toolbar feedback: triage via `references/vercel-toolbar.md` before capture or promote.

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
4. When a reviewable change exists, set `phase:qa` and `status:open` (clear
   `doing`) **in the same turn**. Do not merge; the PM merges after QA.
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
- A plan has no implementation sequence or generated code. Touch and
  direction-locking choices are part of refine (`references/plan.md`).
- Split oversized work into more issues; do not add a parent PRD.
- Never let a local markdown file override issue labels.
- Keep `phase:*` / `status:*` current when a PR or verdict lands.
- When blocked, write the blocker on the issue.
- Preserve human-written memory.
- `.backlog/memory.md` is a log: on merge conflict, keep all changes (never drop entries).
