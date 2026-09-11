# backlog

Getting started for humans. Agents follow `SKILL.md` and the files under
`references/` for the current action.

## Install

```bash
npx skills add mikemajara/skills --skill backlog
```

Then from a project:

```bash
node path/to/skills/backlog/scripts/backlog-setup.mjs
```

Idempotent: scaffolds `.backlog/`, upserts GitHub labels (schema **3**), injects
an agent hint into `AGENTS.md` / `CLAUDE.md`. Use `--check` to print skill
version and `label_schema`. Use `--skip-agent-hint` to opt out of the hint.

Optional snapshot of open issues:

```bash
node path/to/skills/backlog/scripts/backlog-sync.mjs
```

Writes a generated read-only `.backlog/issues.md`.

## What you get

GitHub Issues are the source of truth. Local files are scratch and memory, not
a second tracker.

```text
.backlog/
  inbox.md      # optional local scratch until promoted
  plans/        # product plans when the issue body is not enough
  memory.md     # transactional project log (decisions, facts, gotchas)
```

| Piece | Role |
| ----- | ---- |
| **Issue** | Canonical unit of work |
| **Plan** | Product spec for one issue (what / why / in-out / AC). No implementation sequence |
| **memory.md** | Append-oriented log. Promote lasting guidance into `AGENTS.md` |
| **AGENTS.md** | Project soul for coding agents (outside `.backlog/`) |

Pipeline labels: `phase:research` → `phase:refine` → `phase:implement` →
`phase:qa`. Claim overlay: `status:open` | `doing` | `blocked` | `duplicate`.

## Common prompts

```text
Use the backlog skill to initialize this project.
Use the backlog skill to capture this task.
Use the backlog skill to refine the next issue.
Use the backlog skill to review / triage open work.
Consolidate backlog memory
Promote to AGENTS
```

## Day-to-day flow

1. **Capture** — inbox line or create an issue (`phase:research` or
   `phase:refine`, `status:open`).
2. **Refine** — shape the plan (issue body and/or `plans/`) until AC are
   checkable; then `phase:implement`.
3. **Implement** — change stays inside the plan; record durable notes in
   `memory.md`; when reviewable, `phase:qa`.
4. **QA** — judge the change against the plan (`references/qa.md`).

Always dedupe before adding work. Prefer the smallest artifact that removes
ambiguity.

## Long-term memory (coding agents)

Not a cron. When you ask to consolidate / promote / work on long-term memory:

1. Move lasting conventions, gotchas, and critical decisions from
   `.backlog/memory.md` → `AGENTS.md`.
2. Prune what you promoted from `memory.md`.
3. On `memory.md` merge conflicts, **keep all entries**.

Details: `references/long-term-memory.md`.

This is separate from chat-agent `nightly-learn` (memory → skills).

## Layout of this skill

| Path | Purpose |
| ---- | ------- |
| `SKILL.md` | Router agents load |
| `references/` | On-demand depth (workflow, plan, refine, qa, github, LTM, …) |
| `assets/` | Scaffold templates (`inbox.md`, `memory.md`, agent hint) |
| `scripts/` | `backlog-setup.mjs`, `backlog-sync.mjs`, helpers |

## Migration (label schema 3)

- `status:unknown` → `phase:refine` + `status:open`
- `status:ready` → `phase:implement` + `status:open`
- `status:needs-plan` → `phase:refine` + `status:open`
- Keep `status:doing` / `blocked` / `duplicate`; add a `phase:*` if missing
- Rerun setup to stamp new labels; legacy labels are not deleted
- Treat old `.backlog/prds/` as plans or fold into issues

Full notes: repo root `CHANGELOG.md`.
