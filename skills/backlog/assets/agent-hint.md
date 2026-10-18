<!-- backlog-skill:agent-hint:start -->
## Backlog (deprecated)

The `backlog` skill is deprecated. Use **mstack**
([mikemajara/mstack](https://github.com/mikemajara/mstack)): move `.backlog/`
to `.mstack/` and prefer `/mstack` over `/backlog`. Do not start new work
with this skill.

Until that migration finishes, read `.backlog/memory.md` (or `.mstack/memory.md`)
for recent decisions, facts, choices, blockers, conventions, and gotchas, and
`AGENTS.md` for project context. Do not put merge or phase workflow in
`AGENTS.md`.
Backlog skill v2.8 (deprecated).

## Git

Work on `main` by default. When you make changes, **commit and push**. These
are tracking files: a push can be reverted.

Before you do it, check whether the action is **irreversible** (force-push,
hard reset, dropping published history, deleting a remote branch the team
uses, production-only side effects, leaking secrets). If it is, stop and
ask. If it is not, commit and push without waiting to be asked.
<!-- backlog-skill:agent-hint:end -->
