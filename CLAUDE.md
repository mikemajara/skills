# CLAUDE.md

## Repository Purpose

This repository publishes installable skills.

```bash
npx skills add mikemajara/skills --skill backlog
npx skills add mikemajara/skills --skill sdlc-first-principles
npx skills add mikemajara/skills --skill conversation
npx skills add mikemajara/skills --skill brainstorm
```

Keep the repository focused on small, self-contained skills. Do not reintroduce
the previous portable agent framework, slash commands, global installer, or
project scaffold files unless explicitly requested.

## Current Shape

```text
README.md
CHANGELOG.md
AGENTS.md
CLAUDE.md
docs/backlog-skill-plan.md
skills/backlog/SKILL.md
skills/backlog/assets/
skills/backlog/references/
skills/backlog/scripts/
skills/sdlc-first-principles/SKILL.md
skills/conversation/SKILL.md
skills/brainstorm/SKILL.md
```

`backlog` is one skill. Phase depth lives in `references/` and is read on demand.

Default structure created by the skill:

```text
.backlog/
  inbox.md
  plans/
  memory.md
```

## Design Decisions

- Skill name must remain `backlog`.
- Prefer a thin `SKILL.md` plus `references/`; keep scripts optional, small, and
  dependency-free.
- Encode judgment, not ceremony.
- Issues are canonical (GitHub by default). `gh` recipes live in
  `references/github.md`.
- A plan is a product spec for one issue. No parallel PRD. No implementation plan.
- `.backlog/inbox.md` is optional local scratch.
- `.backlog/memory.md` is curated context future agents should remember.

## Cleanup History

The repo previously contained reusable agents, commands, settings, an installer,
root backlog scaffold files, and unrelated personal skills.

## Development Notes

- Before changing a skill, read its `SKILL.md` and keep it concise.
- Preserve `skills/<name>/SKILL.md` layout.
- Update `CHANGELOG.md` when changing `.backlog/` structure, labels, or workflow
  semantics.
- Do not add generated project `.backlog/` files to this repository.
