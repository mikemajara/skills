# Opt-in Shepherd navigation 0.1.0

The bundled [plugin manifest](../navigation/herdr-plugin.toml) registers a real
`shepherd://` handler **inside Herdr**, not an OS/browser protocol. It implements
[Herdr's link-handler contract](https://herdr.dev/tui/docs/plugins/#link-handlers):
Ctrl-click with `ui.mouse_capture` enabled invokes a fixed argv action. No OS
scheme registration, background service, startup hook, or automatic setup.

## Startup check and consent-based setup

Requires Herdr 0.9.5+, Python 3.9+ on `PATH`, and a local Unix socket (macOS/Linux).
Check availability on activation after establishing inherited Herdr access:

```sh
herdr plugin list
herdr plugin action list --plugin shepherd-navigation
```

Check that registration is enabled, points to this installed bundle's navigation
directory, and exposes its expected `focus` action/handler. If listing does not
show the path/handler, inspect the registered plugin manifest locally using the
location returned by Herdr; never infer readiness from the skill being installed.
A missing/disabled/different registration is not a working navigation setup.
For bare role activation, note readiness only; ask the skill's two-choice welcome
and wait. Do not generate a brief or add a technical setup questionnaire. Include
click-to-jump in [the setup questionnaire](setup.md) with the other unanswered
independent choices, not in another turn when already answered. After an explicitly
requested brief, offer once in plain language if still unanswered:
"Would you like to click an agent's name in my summaries to jump straight to it?"
Before installation, explain that this enables the feature on this machine across
Herdr sessions. Refusal/no answer keeps any requested brief usable with plain IDs;
do not repeatedly prompt. Explicit standing setup permission can authorize this
registration, but never an unrelated inspection of all agents. Completing link
setup does not authorize a herd-wide brief; ask and wait before starting one.

With approval, review the [handler](../navigation/navigation.py) and link the
**installed navigation directory**, not the skill directory or an unpublished
source checkout:

```sh
herdr plugin link /absolute/path/to/installed/shepherd/navigation
herdr plugin action list --plugin shepherd-navigation
herdr plugin list
```

For a disabled registration already pointing to the same installed bundle, use
`herdr plugin enable shepherd-navigation` after confirming installed CLI help.
Do not overwrite or unlink another copy without explaining and obtaining approval
for that replacement. Path-only linking defaults to enabled; omit enable flags
to avoid the installed CLI's path-parsing bug. Recheck the enabled state, root,
manifest and action before generating links; do not claim registration or click
support on a failed/partial setup. Report permission/prerequisite blockers plainly.
Neither linking nor verifying setup requires focus or an OS protocol registration.
To remove registration: `herdr plugin unlink shepherd-navigation`.

Enable `ui.mouse_capture` in Herdr settings. Without capture, the outer terminal
may handle hyperlinks instead; this plugin does not supply an external URL
opener. Display links through a renderer that preserves custom-scheme terminal
hyperlinks (Markdown/OSC 8); raw-text auto-detection varies by terminal. Ctrl-click
is used on macOS too. Do not open candidate links to validate read-only triage.

## Generate a live link without focusing

Run inside the intended Herdr pane, using only its inherited `HERDR_SOCKET_PATH`:

```sh
python3 /absolute/path/to/skills/shepherd/navigation/navigation.py link pane 'w1:p2'
python3 /absolute/path/to/skills/shepherd/navigation/navigation.py link workspace w1
```

IDs above are synthetic: replace them with exact live inventory IDs. The helper
checks the socket and retrieves the destination before printing its URL. It
accepts no socket, session, machine, executable, or command flags. Both commands
are read-only; neither invokes focus, sends input, or creates plugin registration.
The script resolves its root through `__file__`, not the caller's cwd or
`HERDR_PLUGIN_ROOT`.

Use the returned URL verbatim as the link target on the pane ID itself:
`[w1:p2](<returned-pane-url>)`. Keep the workspace name/ID visible; for a
workspace-only destination, link its ID instead. Generate a fresh link when the
destination or session changes. If setup or identity validation is unavailable,
show a copyable focus command instead; never invent a URI or use an issue URL as
a pane destination. See the [Herdr adapter](herdr.md) for triage boundaries.

Herdr 0.9.5's [direct agent focus](https://herdr.dev/tui/docs/cli-reference/)
accepts agent-hosting pane IDs, not arbitrary shell panes or terminal IDs.
Accordingly, pane links require matching `pane get` and `agent get` terminal
identities; ordinary shells fail closed. Use a workspace link for those locations.
The plugin never substitutes directional pane focus, zoom, or terminal input.

## Restart-stable checkpoint scope

```sh
python3 /absolute/path/to/skills/shepherd/navigation/navigation.py scope
```

This read-only command requires `HERDR_ENV=1` and an inherited absolute
`HERDR_SOCKET_PATH` that exists as a Unix socket. It prints a SHA-256 hash of
`["shepherd-checkpoint-scope-v1", <inherited-path>]`, using compact JSON encoding.
It takes no arguments, runs no subprocess, and never focuses or registers a
plugin. The socket check verifies filesystem presence/type, not server health.

Use this opaque value to namespace checkpoints. Unlike click-link session keys,
it deliberately excludes socket device/inode, so server restarts at the same
path retain the checkpoint scope. Different inherited paths produce different
scopes, regardless of pane, cwd, or socket inode. The literal inherited path is
hashed without resolving aliases.

Path reuse can associate old checkpoints with an unrelated replacement session.
Before using saved entries for an explicitly requested inspection or action,
reconcile the relevant targets with fresh live identity, especially after restart.
This does not authorize inventory or reconciliation during bare activation or
setup. Scope equality never authorizes automatic action, proves occupant
continuity, or makes old click links valid. Do not dispatch, resume, or focus from
checkpoints automatically.

## Validation and limits

Wire formats (placeholders, not usable links):

```text
shepherd://<session-sha256>/pane/<pane-id>/<occupant-sha256>
shepherd://<session-sha256>/workspace/<workspace-id>
```

- The opaque session key hashes a v1 domain tag, inherited absolute socket path,
  socket device and inode. The path must stat as a Unix socket. A different path,
  device, or inode invalidates a link, even when Herdr reuses public IDs. Socket
  replacement during validation also fails closed. No path is read from a URL.
- A pane's occupant hash binds its `terminal_id` and reported `agent_session`
  (when present). Changed/missing terminal identity or a changed reported session
  invalidates the link. It does not prove process continuity when another agent
  starts inside the same terminal without reporting a different session.
- The handler validates the entire raw URL against an ASCII allowlist. It rejects
  queries (even empty), fragments, auth, ports, percent encodings, whitespace,
  extra/missing path segments, option-like IDs and other schemes. No URL decoding,
  shell, eval, external sockets, arbitrary commands or raw pane input.
- Focus requires this plugin's `HERDR_PLUGIN_CONTEXT_JSON` with
  `invocation_source="link_click"`, `link_handler_id="destination"`, and
  `clicked_url`, plus the matching inherited plugin/action IDs. The URL comes only
  from that context; `handle` takes no URL argument. CLI action invocation alone
  is rejected. These environment fields are a cooperative host boundary, not
  protection against local code forging its own environment.
- On a valid click, the handler rechecks the session and live target, verifies the
  pane occupant, rechecks the socket, then runs only `herdr agent focus <pane-id>`
  or `herdr workspace focus <workspace-id>` as an argv list, using inherited
  `HERDR_BIN_PATH` (or `herdr` on `PATH`). Focus can mark an agent as seen.
- Socket inode replacement normally invalidates links after restart, but this is
  not a server-issued nonce: inode reuse, or a handoff that retains the same
  socket inode, can preserve a key. Replacing the socket without a restart also
  invalidates links. Workspace identity is the live ID within that socket scope;
  it has no separate creation nonce.
- CLI validation and focus are separate requests, not an atomic compare-and-focus.
  A terminal/session/socket replacement in the final check-to-focus interval
  cannot be excluded by this v1 implementation. Do not treat these links as
  authentication tokens or a transactional guarantee. A server-side conditional
  focus API and server nonce would be needed for those guarantees.

## Offline verification

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/shepherd/navigation -p 'test_*.py' -v
python3 skills/shepherd/navigation/navigation.py --help
```

The [tests](../navigation/test_navigation.py) mock environment, socket stat and
all subprocess calls: wrong session/restart, replaced occupant, malformed URLs,
missing click context, CLI read-only behavior and intended-destination focus.
Scope tests cover restart stability, path separation, invalid environment/socket,
read-only execution and rejection of socket/session overrides.
They perform no real Herdr inspection, focus, plugin linking or OS registration.
Actual click dispatch and renderer hyperlink support need an explicitly
authorized manual integration check after setup; offline tests do not prove them.
