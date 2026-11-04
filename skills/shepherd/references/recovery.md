# Local recovery checkpoints

Shepherd works without setup. Optional `.shepherd/instructions.md` holds standing
configuration: name, `default_mode`, remit, exclusions, priorities, reporting
preferences. Optional `.shepherd/threads.json` is a small recovery checkpoint for
opted-in work in that remit, not a task database, dispatch queue, transcript archive,
or source of live agent truth. Either file can exist without the other. Read
standing instructions when present; do not create either file during ordinary
discovery. Bare role activation follows the skill's resolved mode: `ask` stops at
the welcome without live reconciliation; `check` authorizes a read-only brief in
the configured remit, using fresh evidence rather than saved status. Checkpoint
presence alone never authorizes inspection. Setup is a separate path: use
[the batched setup questions and default-mode setting](setup.md), explain the
minimal saved context and Git privacy choice, then confirm before writing. Do not
begin an agent crawl during setup or automatically after finishing it; offer to
check agents next and wait for the user's request. Saving `check` applies on the
next activation, not as a side effect of editing configuration.

When checkpoint setup already exists, use its `last_seen_skill_version` field
(runtime `threads.last_seen_skill_version`, where `threads` is the loaded checkpoint)
for the last reviewed local skill version. Keep runtime version state out of
standing instructions; do not create `.shepherd/`, instructions, a checkpoint, or
a separate version file merely to record a version. Without checkpoint setup,
review the current skill as needed and keep that observation in the current session.

## Consent and data minimization

Before enabling checkpoints, explain what will be stored and get explicit setup
approval for the chosen local directory. Check project instructions, Git state,
and sharing/backup settings. Apply [the setup privacy gate](setup.md#privacy-gate-before-saving)
before initial setup and before later sensitive writes: precheck tracked paths,
preserve/append approved local exclusion rules, then verify effectiveness.
Default to everything local; only reviewed standing instructions may be made
trackable. `threads.json`, locks, temporary files and all other runtime content
stay local in either mode. Tracked runtime data or failed ignore checks block
writes; never silently untrack data or mutate shared `.gitignore`. The checkpoint
helper does not enforce Git privacy or edit ignore rules; Shepherd must perform
this gate before using it. Sharing instructions is not consent to stage/commit/push.
The checkpoint helper never creates or edits standing instructions; Shepherd
may create that separate file during explicitly approved setup.

Save only active or deliberately parked threads the human has included in this
Shepherd's remit. Use short context, the next useful step, canonical work links,
and minimal recovery pointers. Do not copy transcripts, prompts, private source
material, credentials, tokens, secret-bearing URLs, or environment dumps. Links,
paths, titles and native session IDs can themselves be sensitive. The helper
validates shape, not secrecy; review input before writing. Keep this file small.

Use an explicit `remove` when the human wraps up, discards, or excludes a thread.
Deletion means removal from this checkpoint, not historical retention or secure
erasure from filesystem backups. Never automatically prune an active thread
because its pane is absent, its owner looks done, or a process disappeared. Parked
threads remain until explicitly removed or returned to active. Do not mutate an
external issue, PR, document or task status as a side effect of checkpoint edits.

## Session identity and isolation

Follow [the Herdr adapter](herdr.md) to establish that this Shepherd is inside its
inherited session. With `skill` set to the installed Shepherd skill directory,
obtain the checkpoint scope using the read-only [navigation helper](../navigation/navigation.py):

```sh
scope=$(python3 "$skill/navigation/navigation.py" scope) || exit 1
```

The scope command validates the inherited Herdr environment and that its inherited
absolute socket path names a current Unix socket. It returns a domain-separated
hash of that **socket path**, stable when the socket is recreated at the same path
after a crash/restart. Checkpoint scopes must not include the socket inode, device,
or a session-generation fingerprint: recovery needs to find the checkpoint after
a restart. Click-link session fingerprints deliberately include the socket inode
to invalidate stale navigation links; do not use those fingerprints as checkpoint
scopes. `HERDR_ENV` alone, pane IDs and cwd are not session identities.

Pass the command's result explicitly as `--scope`. Stop scoped reconciliation and
mutation if the command fails; do not guess, copy a saved scope, override inherited
environment variables, or query another session/socket to bypass a mismatch. Two
remits in one session may use separate chosen directories.

A reused socket path can belong to a different session and still yield the same
checkpoint scope. Scope equality therefore does not prove session continuity or
that any saved owner, pane, native session ID, or state is live. Reconcile saved
records against fresh inherited-session evidence, mark uncertain associations,
and take no automatic action from a scope match. Do not automatically resend,
restore, resume, prune, or mutate external work status.

The checkpoint helper (`threads.py`) itself reads no Herdr environment variables,
sockets, session history or live panes. It only compares the supplied scope with
`session_scope`; the navigation helper derives that scope from local inherited
context. This is a guard against accidental cross-session edits, not proof of
caller identity or an access control boundary.

A mismatch refuses mutation and scoped listing/reconciliation. Start Shepherd
inside the proper session instead of targeting another session from here. A socket
path rename may produce a mismatch even if the human believes the herd is the
same. There is intentionally no rebind command or automatic normalization. A
rebind is a separate, explicit, human-confirmed operation **outside this helper**:
verify continuity from local evidence, explain the old/new binding, get confirmation,
and stop other checkpoint writers before a reviewed change. A different session
is not a socket rename. Do not erase/reinitialize the checkpoint to sidestep this
guard. Revalidate every saved pane association even after a confirmed rebind.

## File shape (schema version 1)

```json
{
  "schema_version": 1,
  "last_seen_skill_version": "reviewed-local-version",
  "session_scope": "opaque-inherited-session-identity",
  "threads": [
    {
      "id": "review-parser",
      "title": "Parser review",
      "context": "Owner was checking boundary cases before review.",
      "state": "active",
      "cwd": "./example-project",
      "harness": "example-agent",
      "native_session_id": "optional-native-session-reference",
      "canonical_links": ["https://example.org/issues/42"],
      "recovery_pointers": ["./notes/parser-handoff.md"],
      "last_known_pane": {"workspace_id": "old-workspace", "pane_id": "old-pane"},
      "next_step": "Inspect owner output and confirm remaining checks before continuing.",
      "updated_at": "2026-01-01T12:00:00+00:00"
    }
  ]
}
```

`id` is a stable, caller-chosen thread identifier, not a pane ID or a numbered
brief item. Resolve brief numbers against the current brief before choosing an ID.
`state` is only `active` or `parked`; wrapped/discarded work is removed. `cwd` and
`harness` are recovery clues. Canonical links point at the real work records;
recovery pointers are short local references or clues, never commands to execute.
`last_known_pane` is an optional object of string hints (such as workspace/tab/pane
IDs), explicitly non-authoritative. `native_session_id` is optional; omit unknown
values instead of using null. Native IDs never authorize restoration.

The helper validates required string fields, link/pointer arrays of strings,
optional field types, unique thread IDs, and integer schema version 1. It rejects
malformed JSON, duplicate keys, and non-JSON numeric constants. It does not impose
a URL format, timestamp parser, fixed harness enumeration, or closed set of extra
fields. Unknown fields are preserved except when the caller explicitly replaces
a thread. Do not use this flexibility to store a growing event log. `updated_at`
is a nonempty string on read and is replaced with a UTC timestamp on upsert.

## Helper CLI

Use Python 3.9+ on a POSIX system (stdlib only; locking uses `fcntl.flock`). Run the
helper from the installed skill path, not a copied script in the checkpoint
directory. In these examples, `skill` is the installed Shepherd skill directory,
`helper` is its `scripts/threads.py`, `root` is the user-chosen local directory,
and `version` is the reviewed local skill/package version or revision supplied by
the caller. No package version is hardcoded in the helper.

```sh
python3 "$helper" --help
scope=$(python3 "$skill/navigation/navigation.py" scope) || exit 1
python3 "$helper" --root "$root" --scope "$scope" list
# Only after explicit setup approval:
python3 "$helper" --root "$root" --scope "$scope" init --version "$version"
python3 "$helper" --root "$root" --scope "$scope" upsert thread-input.json
# Or pass one thread object on stdin:
python3 "$helper" --root "$root" --scope "$scope" upsert - < thread-input.json
python3 "$helper" --root "$root" --scope "$scope" seen "$version"
# Only after explicit wrap-up/discard/exclusion:
python3 "$helper" --root "$root" --scope "$scope" remove review-parser
```

Global options precede the subcommand. `--root` defaults to cwd; there is no global
configuration path. Mutation requires a nonempty `--scope`. `list` with scope
checks the binding; unscoped `list` is offline file inspection only, not permission
to reconcile or act. Listing an absent checkpoint prints `null` and creates no
files or directories. Help also creates nothing. There is no dry-run flag; help
is the side-effect-free way to inspect command syntax, not a simulation of a write.

`init` alone creates `.shepherd/` and an empty checkpoint; it refuses to overwrite
an existing file, including invalid or unsupported data. Other mutations require
an initialized checkpoint. `upsert` accepts a single JSON thread object from a
UTF-8 file or stdin (`-`, the default); include every required field above except
`updated_at`, which the helper supplies. It replaces the **whole** matching record
by ID, not a partial merge. Include optional fields you want to retain. `seen`
only records a version after its instructions/changes have been reviewed; it does
not fetch versions, migrate data, or trigger dispatch. Mutations and successful
listing print checkpoint JSON. Exit codes: 0 success, 1 data/I/O/lock/scope error,
2 invalid CLI usage (including missing mutation scope). Output may be sensitive;
do not paste it into public logs.

Writers take a short exclusive nonblocking advisory lock across read/validate/
modify/replace. A concurrent writer fails immediately; do not busy-loop retries.
The input JSON is read before locking, so waiting for stdin holds no lock. The
persistent `threads.lock` inode is intentional: do not unlink it as stale lock
cleanup. OS locks release when a process exits or crashes. Read-only listing needs
no lock: atomic replacement exposes either the old or new complete checkpoint.
All writers must cooperate with this helper's lock; manual edits are not protected.

Writes use a private temporary file in the same directory, flush and fsync it,
atomically replace the checkpoint, then fsync the directory. Validation failure,
lock contention, or failure before replacement leaves checkpoint bytes unchanged.
Corrupt and unsupported files fail closed: preserve them and surface the error;
never reset them to an empty checkpoint. A hard crash can leave an unreferenced
`.threads-*.tmp` file; it is not a recovery authority. Filesystem durability depends
on the host/filesystem. An error after replacement (including directory sync or
stdout failure), or a crash before acknowledgement, can mean the edit landed:
read back rather than assuming it failed. This is not a distributed store.

## Recovery and dispatch boundary

Use this workflow only for requested recovery, inspection, or action, or a
read-only activation brief authorized by `default_mode: check`. `ask`-mode bare
activation and setup stop at the skill's routing boundary; saved checkpoint
records never implicitly authorize live discovery. Match discovery to the request
or configured inspection scope: a single-agent action inspects only its relevant
thread/owner, even when `check` is saved. The mode authorizes no dispatch, replay,
restoration, or automatic checkpoint status changes.

1. Read standing instructions if present and derive the current inherited
   scope with `navigation.py scope`, not from saved state. Read the matching
   checkpoint without creating setup; use `threads.last_seen_skill_version` for
   version review only when that checkpoint exists.
2. Rediscover only the live owners/locations relevant to the requested scope
   inside this session. Use canonical records and local recovery clues only for
   that scope within the opted-in remit; do not crawl unrelated agents. A missing pane is not
   proof the thread is finished. Matching cwd/title/native ID is a lead, not
   proof of a current owner. Mark unresolved associations as uncertain.
3. Before an authorized dispatch, checkpoint a short **intent** and expected next
   verification step, without storing the full prompt or secrets. Explain that
   this records intent, not delivery. Checkpoint presence is not authorization to
   dispatch. If checkpointing fails, surface the failure before proceeding;
   do not claim the intent was saved.
4. Dispatch only through the separately authorized live-agent workflow. Verify
   delivery and the actual result, then explicitly update the checkpoint with
   concise observed context/next step. Do not infer external task completion.
5. After a crash, timeout, or restart, intent may have been saved before or after
   a message arrived. Treat delivery/execution as **uncertain**. Inspect current
   owner output and canonical evidence before deciding what remains. Never
   automatically resend, resume a historical session, restore a pane, or launch
   a replacement agent from checkpoint data. Surface ambiguity to the human.

The helper itself performs no dispatch, restoration, reconciliation, monitoring,
automatic pruning, or external status mutation. It cannot establish exactly-once
message delivery. Recovery keeps useful context available for a human-directed
next decision; it does not replay work.

## Offline verification

From the skill repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/shepherd/tests -p 'test_threads.py' -v
```

Tests use temporary directories, synthetic records and mocked failures; they do
not create real user configuration, contact a harness, or send prompts.
