#!/usr/bin/env python3
"""Read-only link helper and opt-in Herdr link-click handler (Python 3.9+)."""

import argparse
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PLUGIN_ID = "shepherd-navigation"
ID = r"[A-Za-z0-9][A-Za-z0-9_:-]{0,127}"
HEX = r"[a-f0-9]{64}"
URL = re.compile(
    r"shepherd://(?P<session>" + HEX + r")/(?:(?:pane/(?P<pane>" + ID
    + r")/(?P<occupant>" + HEX + r"))|(?:workspace/(?P<workspace>" + ID + r")))"
)


class NavigationError(Exception):
    pass


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":"),
                                     sort_keys=True).encode("utf-8")).hexdigest()


def inherited_socket():
    """Never discover a socket or take one from a URL/CLI argument."""
    path = os.environ.get("HERDR_SOCKET_PATH", "")
    if os.environ.get("HERDR_ENV") != "1" or not os.path.isabs(path):
        raise NavigationError("run inside the inherited Herdr session")
    info = os.stat(path)
    if not stat.S_ISSOCK(info.st_mode):
        raise NavigationError("inherited path is not a Unix socket")
    return path, info


def checkpoint_scope():
    """Restart-stable checkpoint namespace, not authority to act on saved IDs."""
    path, _ = inherited_socket()
    return digest(["shepherd-checkpoint-scope-v1", path])


def session_key():
    path, info = inherited_socket()
    return digest(["shepherd-navigation-v1", path, info.st_dev, info.st_ino])


def valid_id(value):
    if not isinstance(value, str) or re.fullmatch(ID, value) is None:
        raise NavigationError("invalid destination ID")
    return value


def herdr(*args):
    # The executable is trusted inherited configuration, never URL content.
    binary = os.environ.get("HERDR_BIN_PATH") or "herdr"
    completed = subprocess.run(
        [binary, *args], cwd=str(ROOT), env=os.environ.copy(),
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, timeout=10, check=False, shell=False,
    )
    if completed.returncode != 0:
        raise NavigationError("Herdr command failed (exit {})".format(completed.returncode))
    try:
        envelope = json.loads(completed.stdout)
    except ValueError:
        raise NavigationError("invalid Herdr JSON response") from None
    if (not isinstance(envelope, dict) or "error" in envelope
            or not isinstance(envelope.get("result"), dict)):
        raise NavigationError("Herdr returned no successful result")
    return envelope["result"]


def live_target(kind, target):
    valid_id(target)
    result = herdr(kind, "get", target)
    obj = result.get(kind)
    if not isinstance(obj, dict) or obj.get(kind + "_id") != target:
        raise NavigationError("destination is no longer live")
    if kind == "pane":
        terminal = obj.get("terminal_id")
        if not isinstance(terminal, str) or not terminal or len(terminal) > 512:
            raise NavigationError("pane has no verified terminal identity")
        # v0.9.5 has direct agent focus, but pane focus is directional only.
        agent = herdr("agent", "get", target).get("agent")
        if (not isinstance(agent, dict) or agent.get("pane_id") != target
                or agent.get("terminal_id") != terminal
                or agent.get("agent_session") != obj.get("agent_session")):
            raise NavigationError("pane no longer hosts the verified agent terminal")
    return obj


def occupant_key(pane):
    # Also invalidate when a reported agent session changes within a terminal.
    return digest([pane["terminal_id"], pane.get("agent_session")])


def check_session(expected):
    if not hmac.compare_digest(session_key(), expected):
        raise NavigationError("link belongs to another or restarted Herdr session")


def make_link(kind, target):
    if kind not in ("pane", "workspace"):
        raise NavigationError("unsupported destination kind")
    valid_id(target)
    key = session_key()
    obj = live_target(kind, target)
    check_session(key)
    suffix = "/" + occupant_key(obj) if kind == "pane" else ""
    return "shepherd://{}/{}/{}{}".format(key, kind, target, suffix)


def parse_url(url):
    # Full allowlist on raw text: no decoding/normalization, auth, port, query,
    # fragment, percent escapes, whitespace, alternate paths or extra slashes.
    match = URL.fullmatch(url) if isinstance(url, str) and len(url) <= 512 else None
    if match is None:
        raise NavigationError("invalid shepherd URL")
    return match.groupdict()


def handle_click():
    try:
        context = json.loads(os.environ.get("HERDR_PLUGIN_CONTEXT_JSON", ""))
    except ValueError:
        raise NavigationError("missing or invalid Herdr click context") from None
    if (not isinstance(context, dict)
            or context.get("invocation_source") != "link_click"
            or context.get("link_handler_id") != "destination"
            or os.environ.get("HERDR_PLUGIN_ID") != PLUGIN_ID
            or os.environ.get("HERDR_PLUGIN_ACTION_ID") != "focus"):
        raise NavigationError("focus requires this plugin's Herdr link_click invocation")
    dest = parse_url(context.get("clicked_url"))
    check_session(dest["session"])
    kind = "pane" if dest["pane"] else "workspace"
    target = dest[kind]
    obj = live_target(kind, target)
    if kind == "pane" and not hmac.compare_digest(occupant_key(obj), dest["occupant"]):
        raise NavigationError("stale link: pane terminal/session was replaced")
    check_session(dest["session"])
    # Only these two fixed commands can mutate state. Never shell/eval or input.
    herdr("agent" if kind == "pane" else "workspace", "focus", target)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    link = sub.add_parser("link", help="validate a live target and print a URL; never focus")
    link.add_argument("kind", choices=("pane", "workspace"))
    link.add_argument("target")
    sub.add_parser("scope", help="print restart-stable checkpoint scope; read-only")
    sub.add_parser("handle", help="handle Herdr's link_click context, not a URL argument")
    args = parser.parse_args(argv)
    try:
        if args.command == "link":
            print(make_link(args.kind, args.target))
        elif args.command == "scope":
            print(checkpoint_scope())
        else:
            handle_click()
    except (NavigationError, OSError, subprocess.SubprocessError) as exc:
        print("shepherd-navigation: {}".format(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
