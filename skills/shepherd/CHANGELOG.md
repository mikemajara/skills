# Shepherd changelog

Versions apply to this skill and its bundled helpers, not the other skills in
this repository. Data-format versions are separate from skill versions.

## Unreleased

- Add optional `default_mode: check` in local standing instructions, or an explicit
  per-run mode in a runner invocation, to go straight to a read-only attention
  brief on activation without repeating the welcome question. `ask` remains the
  fallback for absent, invalid, or conflicting settings; current requests override
  saved defaults. Existing setups need no migration unless opting into `check`.
- Include the mode in batched setup and document recurring/unattended checks.
  Saving the preference does not inspect agents, create a schedule or checkpoint,
  authorize dispatch, or change task status. Add routing regression scenarios.
- Navigation plugin and checkpoint schema are unchanged.

## 0.2.0 — 2026-11-04

- Herd-wide briefs now use one continuously numbered roster: attention items
  first, then one-line FYI items for every other recognized live agent. Each item
  shows the live pane ID for navigation and follow-up by number.
- Current pane and conversation evidence take precedence over saved recovery
  state. A previously parked follow-up is not described as a parked live agent
  after new work; missing panes are recovery leads, not live roster entries.
- Add regression scenarios for a crowded herd and a stale parked checkpoint.

## 0.1.3 — 2026-11-03

- Bare activation distinguishes first-time setup from an existing setup: returning
  users can check agents or change setup instead of being offered setup again.
  The welcome is the first substantive answer; a harness-required neutral progress
  line may precede it, but must not promise an unrequested herd scan. Version-change
  notes remain brief and user-facing, without exposing saved thread details.
- Account for every in-scope recognized agent by pane, including multiple owners
  in the same workspace/cwd. Keep numbered items actionable, and name settled,
  parked or unreviewed owners in a compact Also checked line rather than hiding
  them behind a count.
- Prefer a meaningful pane name, then displayed title, as navigation label; fall
  back to pane ID. Disambiguate duplicates with IDs; target identity and link
  validation remain ID-based and unchanged.
- Live two-directory smoke test: configured and unconfigured panes each chose the
  correct welcome; the follow-up presented existing choices together or a native
  multi-question setup form. No herd brief or setup write was requested.

## 0.1.2 — 2026-11-03

- Bare role activation runs only lightweight access/local-setup/navigation checks,
  presents two plain-language choices, then stops; it does not crawl the herd.
- Explicit briefs bypass the welcome; specific-agent requests stay targeted.
- Setup batches independent unanswered choices into a supported questionnaire or
  one compact message, with discoverable defaults and follow-ups only for dependent
  ambiguity. No jargon-heavy welcome or automatic summary after setup.
- Add Git privacy choices: everything local by default, or share reviewed standing
  instructions only. Runtime files always stay local. Resolve Git's `info/exclude`,
  preserve existing rules, check already-tracked files and validate ignores before
  sensitive writes. No automatic untracking, staging, commit, push or shared-ignore edits.
- Add temporary-repository regression tests for root/nested paths, both privacy
  modes, tracked-file conflicts and ineffective ignores. The navigation plugin and
  checkpoint schema remain unchanged.

## 0.1.1 — 2026-11-02

- Check navigation registration at startup; offer consent-based setup or repair
  of the installed bundle instead of silently omitting clickable pane IDs.
- Make briefs self-contained: describe the actual problem and change in Context,
  put progress/test evidence in a separate Status line, and inspect earlier
  evidence when the latest output only contains issue numbers or QA handoff.
- Add regression scenarios for subject-level context and missing navigation setup.
- The bundled navigation plugin remains at 0.1.0; this patch changes the skill's
  reporting and setup workflow, not its handler code or checkpoint schema.

## 0.1.0 — 2026-11-02

Initial versioned Shepherd release, replacing `chief-of-staff`.

### Included

- Human-directed coordination of existing agents in the inherited Herdr session;
  empty shells and saved session history are recovery clues, not live agents.
- A numbered, context-first attention brief with navigation on the pane ID.
- Optional `shepherd-navigation` Herdr plugin for Ctrl-click pane/workspace links;
  URLs are generated read-only and checked against the current socket and target.
- Optional `.shepherd/instructions.md` for standing preferences and
  `.shepherd/threads.json` for active/parked recovery checkpoints. Atomic,
  scope-checked helper writes; wrapped or discarded threads are removed.
- Visible startup version and a change summary when an existing checkpoint's
  last-seen version differs. No setup is created merely to remember a version.
- Offline regression tests for navigation and checkpoint storage.

### Boundaries

No automatic dispatch/replay, historical-session restore, scheduler, team
spawning, implementation takeover, or automatic deletion of work. Checkpoints
are recovery context, not a record of exactly-once delivery. Click links expire
when their socket or reported target identity changes; validation/focus are not
an atomic transaction. Python helpers currently require POSIX (macOS/Linux).

### Migration

Install `shepherd` and remove the obsolete installed `chief-of-staff` package.
Reload the harness's skill list or open a fresh agent session. Navigation and
checkpoint setup are separately opt-in. No migration of old home files or saved
sessions is performed automatically. Preview `SHEPHERD.md` was never a released
configuration format; standing instructions now belong in
`.shepherd/instructions.md`.
