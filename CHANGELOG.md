# Changelog

## Unreleased

### Changed

- Docs: slim top-level `README.md` to a skills catalog (what each skill is +
  install). Agents follow `SKILL.md` / `references/` — not per-skill READMEs.
  Optional `skills/<name>/README.md` is a brief skills.sh / listing blurb only
  (backlog: one-liner + install). No separate Getting Started guide.

### Removed

- `voice-miguel`: not shipped in this repo (Grok-local / personal only). Do not
  add it here.

### Added

- `backlog`: coding-agents long-term memory flow — promote conventions /
  gotchas / critical decisions from `.backlog/memory.md` into `AGENTS.md`
  (`references/long-term-memory.md`); prune memory after promote; on
  `memory.md` merge conflicts keep all entries. Triggers: consolidate backlog
  memory / promote to AGENTS / work on long-term memory.

### Added

- `nightly-learn`: periodic memory→skill consolidation (per-agent routine;
  harness-agnostic; HITL for shared skill rewrites).

- Rewrote `conversation` as a gap-check for a mostly formed idea: find
  missing constraints, contradictions, and edge cases without inventing a
  new direction.
- Added `brainstorm`, a generative skill for new angles and option catalogs.
  Handoff to `conversation` when an idea is picked and needs pressure-testing.

- `google-docs`: connector-agnostic create/format/edit/comment/suggest/review
  rules; Markdown draft default; no connector lock-in.

- Backlog skill **v2.0.0** (label schema **3**): `phase:research`,
  `phase:refine`, `phase:implement`, `phase:qa` plus `status:open`,
  `status:doing`, `status:blocked`, `status:duplicate`. Version in
  `SKILL.md` frontmatter and `references/version.json`.
- On-demand references: workflow, research, plan (product spec + done-when),
  refine, qa, drift, and GitHub/`gh` helpers.
- `backlog-setup.mjs --check` prints skill version and `label_schema`.

### Changed

- `SKILL.md` is a router: how to proceed on an issue. `gh` recipes moved to
  `references/github.md`.
- A **plan** is the product spec for one issue (former PRD). No implementation
  sequencing artifact. Writing the plan is refine (`phase:refine`).
- Default `.backlog/` scaffold is `inbox.md`, `plans/`, `memory.md` (no `prds/`).
- Setup no longer creates `prds/`. Existing `prds/` is reported as legacy.

### Migration Notes

Label mapping for existing issues:

1. `status:unknown` → `phase:refine` + `status:open`
2. `status:ready` → `phase:implement` + `status:open`
3. `status:needs-plan` → `phase:refine` + `status:open`
4. Keep `status:doing`, `status:blocked`, `status:duplicate` as status only
   (add a `phase:*` if missing).
5. Rerun `backlog-setup.mjs` to stamp new labels. Legacy labels are not deleted.
6. Fold `.backlog/prds/` into issue bodies or `plans/`; treat old implementation
   PLAN files as obsolete.

The important invariant is: if an item has an issue, the issue owns status
and phase.

### Added

- `backlog-setup.mjs` now injects a marked agent hint into `AGENTS.md` and/or
  `CLAUDE.md` (creating `AGENTS.md` when neither exists) so agents read
  `.backlog/memory.md` and check the inbox before starting work. Use
  `--skip-agent-hint` to opt out; `--check` verifies the hint is present and
  current.

### Changed

- Clarified `backlog` artifact roles: GitHub Issues are implementable units;
  PRDs are product umbrellas that link to shaped issues (not issue body dumps);
  plans are per-issue sequencing with an explicit reference-only rule for
  umbrella roadmaps. Promote and Refine flows now require classifying artifact
  type before creating or updating work.

### Removed

- Removed `todoist-api` as out of scope for this repository.

### Added

- Added `skills/backlog/scripts/backlog-setup.mjs`, an idempotent project setup
  helper that creates missing `.backlog/` scaffold files and upserts the
  canonical GitHub label set from `references/labels.json`.
- Added `skills/backlog/scripts/backlog-sync.mjs`, an optional helper that
  regenerates `.backlog/issues.md` from GitHub Issues via `gh issue list`.
- Added dedupe guidance to `backlog`: verify local `.backlog/` artifacts and
  GitHub Issues before adding inbox items, PRDs, plans, or promoted issues;
  includes overlap signals and resolution rules for exact duplicates, related
  work, and superseded items.
- Added `sdlc-first-principles`, a workflow skill that applies Elon Musk's
  five-step process improvement algorithm to SDLC requirements, planning, code
  review, CI/CD, release, incident, testing, and automation processes.

### Changed

- Simplified `backlog` by removing the local GitHub Issues mirror and sync
  helper; promoted work should be checked in GitHub directly. The optional
  `backlog-sync.mjs` helper was restored for projects that want a generated
  read-only snapshot at `.backlog/issues.md`.

### Changed

- Simplified promoted-issue types and GitHub labels: `nitpick`/`chore`/`research`
  are now `type:nit`; status labels are `status:unknown`, `status:ready`, and
  `status:blocked` (replacing `needs-refinement` and `agent-ready`).
- Updated the install target after the repository transfer:

```bash
npx skills add mikemajara/skills --skill backlog
```

- GitHub Issues are now canonical for promoted work. `.backlog/` remains the
  local project memory layer, not a competing task tracker.
- The default backlog structure is now:

```text
.backlog/
  inbox.md
  prds/
  plans/
  memory.md
```

- `.backlog/inbox.md` replaces `.backlog/backlog.md` for rough ideas and tasks
  that are not yet promoted to GitHub Issues.
- `.backlog/memory.md` replaces `.backlog/notes.md` for curated decisions,
  conventions, blockers, gotchas, and durable agent context.
- PRD and plan templates now include an optional `issue` frontmatter field.
- Local PRDs are drafting buffers before GitHub promotion; after promotion,
  delete them or keep a tiny pointer file. GitHub Issues own the canonical
  title, body, status, labels, and discussion—do not maintain duplicate
  editable copies in `.backlog/`.

### Migration Notes

For projects already using an older `.backlog/` layout:

1. Create the new files if they do not exist:

```text
.backlog/inbox.md
.backlog/memory.md
```

2. Rename `.backlog/notes.md` to `.backlog/memory.md` and keep the existing
   human-written content. Add a `## Gotchas` section if it would help future
   agents.
3. Review `.backlog/backlog.md`:
   - Move rough, unpromoted items into `.backlog/inbox.md` under `## Inbox`.
   - Promote trackable work to GitHub Issues.
   - Preserve links from related PRDs and plans to their GitHub Issues.
4. Remove `.backlog/issues.md` if it was only a generated GitHub Issues mirror.
5. Stop manually maintaining `.backlog/backlog.md` once GitHub Issues are
   canonical. Remove or archive it only after confirming its content has moved
   to the inbox, GitHub Issues, PRDs, plans, or memory.

The important invariant is: if an item has a GitHub Issue, GitHub owns its
status.

## 2026-05-23

### Changed

- Updated the install instructions during repository cleanup.
- Documented that this repository publishes a single installable skill named
  `backlog`.
- Kept the repository focused on the `backlog` skill and its minimal
  documentation.

### Removed

- Removed the previous portable agent framework, slash commands, setup script,
  global installer, root backlog scaffold files, and unrelated personal skills.
