# mikemajara/skills

Installable agent skills. Each skill lives under `skills/<name>/` with a
`SKILL.md` the harness loads. Most skills are self-contained there; only skills
that need a human Getting Started guide ship a `README.md` beside `SKILL.md`.

## Install

```bash
npx skills add mikemajara/skills --skill <name>
```

Examples:

```bash
npx skills add mikemajara/skills --skill backlog
npx skills add mikemajara/skills --skill sdlc-first-principles
npx skills add mikemajara/skills --skill conversation
npx skills add mikemajara/skills --skill brainstorm
npx skills add mikemajara/skills --skill google-docs
npx skills add mikemajara/skills --skill nightly-learn
```

See `CHANGELOG.md` for release notes and migrations.

## Skills

| Skill | What it is |
| ----- | ---------- |
| [`backlog`](skills/backlog/) | Capture work and move GitHub issues through research → refine → implement → qa. **Has a Getting Started README.** |
| [`sdlc-first-principles`](skills/sdlc-first-principles/) | Apply a five-step first-principles process lens to SDLC work. |
| [`conversation`](skills/conversation/) | Pressure-test a mostly formed idea (gaps, contradictions, edges). |
| [`brainstorm`](skills/brainstorm/) | Generate new angles and option catalogs. |
| [`google-docs`](skills/google-docs/) | Connector-agnostic Google Docs create / format / edit / review rules. |
| [`nightly-learn`](skills/nightly-learn/) | Promote sticky how-to from an agent’s own memory into skills (HITL for shared). |

## Contributing

Prefer thin, harness-agnostic skills. Shared source of truth is this repo; do not
treat a local harness install as canonical. Document breaking label or layout
changes in `CHANGELOG.md`.
