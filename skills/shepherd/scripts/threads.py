#!/usr/bin/env python3
"""Optional local recovery checkpoints; no harness access or dispatch."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import sys
import tempfile


class CheckpointError(ValueError):
    pass


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise CheckpointError(label + " must be a nonempty string")


def validate_thread(record):
    if not isinstance(record, dict):
        raise CheckpointError("each thread must be an object")
    for key in ("id", "title", "context", "state", "cwd", "harness",
                "next_step", "updated_at"):
        text(record.get(key), "thread." + key)
    if record["state"] not in ("active", "parked"):
        raise CheckpointError("thread.state must be active or parked; remove finished work")
    for key in ("canonical_links", "recovery_pointers"):
        values = record.get(key)
        if not isinstance(values, list):
            raise CheckpointError("thread." + key + " must be an array of strings")
        for value in values:
            text(value, "thread." + key + " entry")
    if "native_session_id" in record:
        text(record["native_session_id"], "thread.native_session_id")
    if "last_known_pane" in record:
        pane = record["last_known_pane"]
        if not isinstance(pane, dict) or any(
                not isinstance(key, str) or not isinstance(value, str)
                for key, value in pane.items()):
            raise CheckpointError("thread.last_known_pane must be an object of strings")


def validate(document):
    if not isinstance(document, dict):
        raise CheckpointError("checkpoint must be an object")
    if type(document.get("schema_version")) is not int or document["schema_version"] != 1:
        raise CheckpointError("unsupported schema_version (expected integer 1)")
    text(document.get("session_scope"), "session_scope")
    text(document.get("last_seen_skill_version"), "last_seen_skill_version")
    if not isinstance(document.get("threads"), list):
        raise CheckpointError("threads must be an array")
    ids = set()
    for record in document["threads"]:
        validate_thread(record)
        if record["id"] in ids:
            raise CheckpointError("duplicate thread id: " + record["id"])
        ids.add(record["id"])
    return document


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CheckpointError("duplicate JSON key: " + key)
        result[key] = value
    return result


def invalid_constant(value):
    raise CheckpointError("invalid JSON constant: " + value)


def load_json(stream):
    return json.load(stream, object_pairs_hook=unique_object,
                     parse_constant=invalid_constant)


def read_checkpoint(path):
    try:
        with path.open(encoding="utf-8") as stream:
            return validate(load_json(stream))
    except FileNotFoundError:
        # A dangling symlink is not an absent checkpoint to initialize over.
        if path.is_symlink():
            raise CheckpointError("checkpoint is a dangling symlink")
        return None


def check_scope(document, scope):
    if scope is not None:
        text(scope, "--scope")
        if document is not None and document["session_scope"] != scope:
            raise CheckpointError("session scope mismatch; start Shepherd in the proper session")


@contextmanager
def exclusive_lock(directory):
    # Keep the lock inode: unlinking it would allow two locks on different inodes.
    with (directory / "threads.lock").open("a", encoding="utf-8") as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise CheckpointError("checkpoint busy; concurrent mutation refused") from exc
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def atomic_write(path, document):
    validate(document)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                         dir=path.parent, prefix=".threads-",
                                         suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(document, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
        # Persist the directory entry as well as the file contents on POSIX.
        fd = os.open(str(path.parent), os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    finally:
        if temporary is not None:
            temporary.unlink()


def mutate(root, scope, command, *, version=None, record=None, thread_id=None):
    text(scope, "--scope")
    directory = Path(root) / ".shepherd"
    if command == "init":
        text(version, "version")
        directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    elif not directory.is_dir():
        raise CheckpointError("checkpoint not initialized; use init explicitly")
    path = directory / "threads.json"
    with exclusive_lock(directory):
        document = read_checkpoint(path)
        check_scope(document, scope)
        if command == "init":
            if document is not None:
                raise CheckpointError("checkpoint already initialized; no changes made")
            document = {"schema_version": 1, "last_seen_skill_version": version,
                        "session_scope": scope, "threads": []}
        else:
            if document is None:
                raise CheckpointError("checkpoint not initialized; use init explicitly")
            if command == "upsert":
                if not isinstance(record, dict):
                    raise CheckpointError("upsert input must be a thread object")
                record = dict(record)
                record["updated_at"] = datetime.now(timezone.utc).isoformat()
                validate_thread(record)
                for index, old in enumerate(document["threads"]):
                    if old["id"] == record["id"]:
                        document["threads"][index] = record
                        break
                else:
                    document["threads"].append(record)
            elif command == "remove":
                if not any(item["id"] == thread_id for item in document["threads"]):
                    raise CheckpointError("unknown thread id: " + str(thread_id))
                document["threads"] = [item for item in document["threads"]
                                       if item["id"] != thread_id]
            elif command == "seen":
                text(version, "version")
                document["last_seen_skill_version"] = version
            else:
                raise CheckpointError("unknown mutation: " + command)
        atomic_write(path, document)
    return document


def parser():
    result = argparse.ArgumentParser(
        description="Local recovery checkpoint only; never dispatches or restores agents.",
        epilog="No dry-run mode. --help never reads/writes checkpoint files. "
               "Only init creates setup. Mutation requires caller-verified --scope; "
               "no environment/session discovery or rebind is performed.")
    result.add_argument("--root", type=Path, default=Path("."),
                        help="chosen local directory containing .shepherd (default: cwd)")
    result.add_argument("--scope", help="opaque inherited-session identity; required for mutations, "
                        "checked when supplied to list; never copy from saved state")
    commands = result.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="explicitly create an empty checkpoint; never overwrite")
    init.add_argument("--version", required=True, help="reviewed local skill version")
    commands.add_parser("list", help="print checkpoint JSON, or null if absent; creates nothing")
    upsert = commands.add_parser("upsert", help="replace full thread by stable id (not a field merge)")
    upsert.add_argument("input", nargs="?", default="-", help="JSON thread file, or - for stdin (default)")
    remove = commands.add_parser("remove", help="explicitly delete wrapped/discarded/out-of-remit thread")
    remove.add_argument("id", help="stable thread id, not attention-brief item number")
    seen = commands.add_parser("seen", help="record a reviewed skill version; does not migrate data")
    seen.add_argument("version")
    return result


def main(argv=None):
    cli = parser()
    args = cli.parse_args(argv)
    if args.command != "list" and args.scope is None:
        cli.error("--scope is required for mutation")
    try:
        if args.command == "list":
            document = read_checkpoint(args.root / ".shepherd" / "threads.json")
            check_scope(document, args.scope)
        else:
            record = None
            if args.command == "upsert":
                if args.input == "-":
                    record = load_json(sys.stdin)
                else:
                    with Path(args.input).open(encoding="utf-8") as stream:
                        record = load_json(stream)
            document = mutate(args.root, args.scope, args.command,
                              version=getattr(args, "version", None), record=record,
                              thread_id=getattr(args, "id", None))
        print(json.dumps(document, indent=2, ensure_ascii=False))
        return 0
    except (CheckpointError, OSError, ValueError) as exc:
        print("threads: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
