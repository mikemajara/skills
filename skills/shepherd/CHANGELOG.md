# Shepherd changelog

Versions apply to this skill and its bundled helpers, not the other skills in
this repository. Data-format versions are separate from skill versions.

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
