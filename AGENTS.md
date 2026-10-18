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

## Post-push installation

A successful push to `main` publishes the skills. After every such push, install
all skills from the current checkout on the current machine:

```sh
npx --yes skills add . -g --skill '*' --agent universal -y
```

The only install target is `~/.agents/skills/`. Do not use `--all`,
`--agent '*'`, or agent-specific destinations such as `~/.claude/skills/`.
Do not update unrelated global skills or modify the shell configuration.
If the shell's `npx` wrapper fails, use a clean shell or the installed executable.

Verify that every tracked file under `skills/` matches its installed counterpart,
including references, scripts, and assets. Report push and installation outcomes
separately; a successful push with a failed install is not complete local delivery.
Do not install uncommitted edits as though they were the published version.

## Skill content safety

`publish` and `voice` may be improved from private workplace material. Extract
the reusable behavior, then write instructions and examples from scratch. Do
not copy or lightly redact source material. Do not include real employers,
customers, partners, coworkers, products, email addresses, domains, links,
identifiers, or recognizable combinations of private facts. Use neutral roles
and synthetic placeholders when an example is necessary.
