# Updating skills in this repository

This repository (`github.com/mikemajara/skills`) is the source of truth for
its installable skills, even when a change is requested from another working
directory. Locate this checkout (or clone the repository if absent), read this
file, and run repo commands from its root before editing. Do not edit an
installed copy under `~/.agents/skills/` as the source. Confirm the requested
skill actually lives under `skills/<name>/`; if it belongs to another
repository, find that source instead of creating a duplicate here.

## Editing

- Work on `main` by default. Check the worktree before editing and preserve
  unrelated changes; coordinate if another agent is editing the same skill.
- Read the target `skills/<name>/SKILL.md` and the relevant references, scripts,
  assets, and tests before changing behavior. Keep `SKILL.md` thin and
  harness-agnostic; put depth in on-demand `references/` and use small,
  dependency-light scripts only where they help. Preserve the skill's name and
  `skills/<name>/SKILL.md` layout when updating it.
- Change the source skill rather than patching an installed copy. For skills
  not present here (for example, a locally installed mail-review skill), locate
  their owning repository and follow its instructions.
- Run focused checks for the touched skill (tests, scripts, or a realistic
  example), and inspect the diff for unrelated changes. Update `README.md` when
  adding or removing a skill; record meaningful behavior changes or migrations
  in `CHANGELOG.md` without rewriting historical entries.
- Avoid copying private source material into published skills. Extract reusable
  behavior and write fresh, synthetic examples. In particular, keep `publish`
  and `voice` free of real employers, customers, partners, coworkers, products,
  addresses, domains, links, identifiers, or recognizable combinations of
  private facts.

## Git

Work on `main` by default. When you make changes, **commit and push**. These
are tracking files: a push can be reverted.

Before you do it, check whether the action is **irreversible** (force-push,
hard reset, dropping published history, deleting a remote branch the team
uses, production-only side effects, leaking secrets). If it is, stop and
ask. If it is not, commit and push without waiting to be asked.

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
including references, scripts, and assets. When retiring a skill, check for a
stale installed copy too; adding the remaining skills does not uninstall it.
Report push and installation outcomes separately; a successful push with a
failed install is not complete local delivery. Do not install uncommitted edits
as though they were the published version.
