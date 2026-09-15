# Long-term memory (coding agents)

For **coding agents** on a backlog-using repo. Not for chat-desk agents
(Grok Bot personas, etc.) unless the user says otherwise.

Same *idea* as consolidating short-term notes into durable project guidance —
but the surfaces are repo files: `.backlog/memory.md` → `AGENTS.md`.

## Roles

| File | Role |
| ---- | ---- |
| `.backlog/memory.md` | **Transactional** project log: decisions, facts, choices, blockers, conventions-in-progress, gotchas. Entries may later become irrelevant. Append-oriented. |
| `AGENTS.md` | Project context for coding agents: architecture, stack, commands, policies, gotchas. **Not** PM / refine / QA / merge — that stays in this skill. |

Day to day, coding agents should **write** into `memory.md` when they learn
something the repo should not forget: key decisions, facts, product/tech
choices, and gotchas — not only after implement.

## When to run this procedure

When the user asks along these lines (wording may vary):

- "consolidate backlog memory"
- "promote to AGENTS"
- "work on your long-term memory"

No cron is required; the harness or human triggers it.

## Procedure

1. Read `.backlog/memory.md` (and current `AGENTS.md`).
2. Select candidates to promote: **project conventions**, **gotchas**, and
   **critical / medium-term decisions** that should bind future coding agents.
   Skip ephemeral blockers and one-off notes that are already done or obsolete.
3. Fold each candidate into `AGENTS.md` in the right section (or add a short
   section). Prefer durable, imperative guidance over chatty log tone. Do not
   invent policy that was not in memory or already agreed in the repo. Do
   **not** promote backlog workflow (phases, labels, merge authority, spawn)
   into `AGENTS.md`.
4. **Prune** the promoted entries from `memory.md` so the two files do not
   duplicate. Leave a one-line pointer only if useful (`promoted to AGENTS.md
   on YYYY-MM-DD`); otherwise remove the entry.
5. Leave remaining transactional items in `memory.md`.
6. Summarize what moved and what stayed.

## Merge safety for `memory.md`

Treat `.backlog/memory.md` as a **log**: on merge conflict, **keep all
changes** from both sides. Never resolve by dropping entries. Losing a log
line is worse than a messy duplicate (duplicates can be pruned on the next
consolidation).

`AGENTS.md` conflicts are normal: resolve thoughtfully; do not auto-keep-all.

## Out of scope

- Chat-agent memory → skills (`nightly-learn`).
- Inventing new project policy during consolidation.
- Rewriting issue bodies or plans as a substitute for this pass.
