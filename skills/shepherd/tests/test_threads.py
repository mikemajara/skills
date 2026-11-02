"""Offline tests; all checkpoint/config paths live in temporary directories."""

from contextlib import redirect_stderr, redirect_stdout
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "threads.py"
SPEC = importlib.util.spec_from_file_location("shepherd_threads", SCRIPT)
threads = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(threads)


class ThreadsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.directory = self.root / ".shepherd"
        self.path = self.directory / "threads.json"
        self.scope = "synthetic-inherited-session"

    def cli(self, *args, stdin=""):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err), mock.patch(
                "sys.stdin", io.StringIO(stdin)):
            try:
                code = threads.main(["--root", str(self.root)] + list(args))
            except SystemExit as exc:
                code = exc.code
        return code, out.getvalue(), err.getvalue()

    def init(self):
        return threads.mutate(self.root, self.scope, "init", version="reviewed-local")

    def record(self, **changes):
        result = {"id": "thread-stable", "title": "Synthetic work",
                  "context": "Review a small local change", "state": "active",
                  "cwd": "./example", "harness": "example-agent",
                  "canonical_links": ["https://example.org/issues/1"],
                  "recovery_pointers": ["./notes/handoff.md"],
                  "last_known_pane": {"pane_id": "old-pane", "workspace_id": "old-workspace"},
                  "next_step": "Check owner output before proposing a continuation"}
        result.update(changes)
        return result

    def upsert(self, **changes):
        return threads.mutate(self.root, self.scope, "upsert", record=self.record(**changes))

    def assert_unchanged(self, action):
        before = self.path.read_bytes()
        with self.assertRaises((threads.CheckpointError, ValueError, OSError)):
            action()
        self.assertEqual(before, self.path.read_bytes())

    def test_missing_list_and_help_create_nothing(self):
        code, out, _ = self.cli("list")
        self.assertEqual((code, json.loads(out)), (0, None))
        for command in ((), ("init",), ("upsert",), ("remove",), ("seen",), ("list",)):
            code, _, _ = self.cli(*command, "--help")
            self.assertEqual(code, 0)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_explicit_init_and_no_implicit_setup(self):
        for command, kwargs in (("upsert", {"record": self.record()}),
                                ("seen", {"version": "v2"}),
                                ("remove", {"thread_id": "thread-stable"})):
            with self.assertRaises(threads.CheckpointError):
                threads.mutate(self.root, self.scope, command, **kwargs)
        self.assertFalse(self.directory.exists())
        code, out, _ = self.cli("--scope", self.scope, "init", "--version", "local-release")
        self.assertEqual(code, 0)
        document = json.loads(out)
        self.assertEqual(document, {"schema_version": 1, "session_scope": self.scope,
                                   "last_seen_skill_version": "local-release", "threads": []})
        self.assertFalse((self.directory / "instructions.md").exists())
        self.assert_unchanged(self.init)

    def test_missing_and_empty_scope_refuse_without_setup(self):
        for prefix in ([], ["--scope", ""], ["--scope", "  "]):
            code, _, _ = self.cli(*prefix, "init", "--version", "v1")
            self.assertNotEqual(code, 0)
        self.assertFalse(self.directory.exists())

    def test_upsert_stable_id_full_replacement_and_generated_timestamp(self):
        self.init()
        result = self.upsert(native_session_id="saved-session", updated_at="old")
        first = result["threads"][0]
        self.assertNotEqual(first["updated_at"], "old")
        self.assertTrue(first["updated_at"].endswith("+00:00"))
        result = self.upsert(title="Changed", state="parked")
        self.assertEqual(len(result["threads"]), 1)
        self.assertEqual(result["threads"][0]["title"], "Changed")
        self.assertNotIn("native_session_id", result["threads"][0])
        self.assertEqual(result["last_seen_skill_version"], "reviewed-local")

    def test_file_and_stdin_input(self):
        self.init()
        source = self.root / "input.json"
        source.write_text(json.dumps(self.record()), encoding="utf-8")
        for input_args, stdin in (((str(source),), ""), (("-",), json.dumps(self.record())),
                                  ((), json.dumps(self.record()))):
            code, out, err = self.cli("--scope", self.scope, "upsert", *input_args, stdin=stdin)
            self.assertEqual(code, 0, err)
            self.assertEqual(len(json.loads(out)["threads"]), 1)

    def test_remove_is_explicit_and_seen_only_updates_version(self):
        self.init()
        self.upsert()
        before = threads.read_checkpoint(self.path)
        code, out, err = self.cli("--scope", self.scope, "seen", "next-reviewed-version")
        self.assertEqual(code, 0, err)
        expected = copy.deepcopy(before)
        expected["last_seen_skill_version"] = "next-reviewed-version"
        self.assertEqual(json.loads(out), expected)
        self.assert_unchanged(lambda: threads.mutate(self.root, self.scope, "remove", thread_id="absent"))
        code, out, err = self.cli("--scope", self.scope, "remove", "thread-stable")
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["threads"], [])
        self.assertFalse(any("history" in path.name for path in self.directory.iterdir()))

    def test_scope_mismatch_all_mutations_and_scoped_read(self):
        self.init()
        self.upsert()
        for command, kwargs in (("init", {"version": "v2"}),
                                ("upsert", {"record": self.record()}),
                                ("seen", {"version": "v2"}),
                                ("remove", {"thread_id": "thread-stable"})):
            with self.subTest(command=command):
                self.assert_unchanged(lambda: threads.mutate(self.root, "other-session", command, **kwargs))
        code, _, err = self.cli("--scope", "other-session", "list")
        self.assertEqual(code, 1)
        self.assertIn("scope mismatch", err)
        self.assertEqual(self.cli("list")[0], 0)  # Offline inspection only.

    def test_corrupt_and_unsupported_checkpoints_preserved_for_every_command(self):
        valid = self.init()
        invalid_documents = ["{truncated", "[]", "null", "{\"schema_version\":1,\"schema_version\":1}",
                             json.dumps(dict(valid, schema_version=2)),
                             json.dumps(dict(valid, schema_version=True)),
                             json.dumps(dict(valid, threads={})),
                             json.dumps(dict(valid, session_scope=5)),
                             json.dumps(dict(valid, last_seen_skill_version=None))]
        for content in invalid_documents:
            self.path.write_text(content, encoding="utf-8")
            for command in (("list",), ("init", "--version", "v2"), ("seen", "v2"),
                            ("remove", "thread-stable"), ("upsert",)):
                with self.subTest(content=content, command=command):
                    code, _, _ = self.cli("--scope", self.scope, *command,
                                          stdin=json.dumps(self.record()))
                    self.assertEqual(code, 1)
                    self.assertEqual(self.path.read_text(encoding="utf-8"), content)

    def test_invalid_record_types_preserve_checkpoint(self):
        self.init()
        for key, bad in (("id", ""), ("title", 1), ("context", None),
                         ("cwd", []), ("harness", False), ("next_step", {}),
                         ("state", "wrapped"), ("state", "discarded"),
                         ("canonical_links", "url"), ("canonical_links", [2]),
                         ("recovery_pointers", {}), ("native_session_id", 1),
                         ("last_known_pane", []), ("last_known_pane", {"pane_id": 1})):
            with self.subTest(key=key, bad=bad):
                self.assert_unchanged(lambda: self.upsert(**{key: bad}))
        for bad in ([], None, "string"):
            self.assert_unchanged(lambda: threads.mutate(self.root, self.scope, "upsert", record=bad))
        record = self.record()
        del record["title"]
        self.assert_unchanged(lambda: threads.mutate(self.root, self.scope, "upsert", record=record))

    def test_bad_stored_thread_duplicate_ids_and_timestamp_types(self):
        self.init()
        good = self.upsert()
        malformed = []
        duplicate = copy.deepcopy(good)
        duplicate["threads"].append(copy.deepcopy(duplicate["threads"][0]))
        malformed.append(duplicate)
        for key, value in (("updated_at", 1), ("state", "done"), ("title", None)):
            changed = copy.deepcopy(good)
            changed["threads"][0][key] = value
            malformed.append(changed)
        for document in malformed:
            self.path.write_text(json.dumps(document), encoding="utf-8")
            self.assert_unchanged(lambda: threads.mutate(self.root, self.scope, "seen", version="v2"))

    def test_unknown_extension_fields_are_preserved(self):
        document = self.init()
        document["future_note"] = {"small": "extension"}
        self.path.write_text(json.dumps(document), encoding="utf-8")
        self.upsert(extra_hint="small")
        updated = threads.mutate(self.root, self.scope, "seen", version="v2")
        self.assertEqual(updated["future_note"], document["future_note"])
        self.assertEqual(updated["threads"][0]["extra_hint"], "small")

    def test_lock_contention_fails_without_wait_or_checkpoint_change(self):
        self.init()
        with threads.exclusive_lock(self.directory):
            self.assert_unchanged(lambda: self.upsert())
            # Read-only readers need no lock and observe a complete snapshot.
            self.assertEqual(self.cli("--scope", self.scope, "list")[0], 0)
        self.upsert()  # No stale lock after holder exits.

    def test_failed_replace_and_flush_preserve_original_and_clean_temp(self):
        self.init()
        for target in ("replace", "fsync"):
            with self.subTest(target=target), mock.patch.object(
                    threads.os, target, side_effect=OSError("synthetic failure")):
                self.assert_unchanged(lambda: self.upsert())
            self.assertEqual(list(self.directory.glob(".threads-*.tmp")), [])
            self.upsert()  # Lock was released after failure.

    def test_atomic_replace_is_same_directory_and_private_file(self):
        self.init()
        original_replace = threads.os.replace
        observed = []

        def replace(source, destination):
            observed.append((Path(source).parent, Path(destination)))
            self.assertEqual(threads.read_checkpoint(destination)["threads"], [])
            original_replace(source, destination)

        with mock.patch.object(threads.os, "replace", side_effect=replace):
            self.upsert()
        self.assertEqual(observed, [(self.directory, self.path)])
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(len(threads.read_checkpoint(self.path)["threads"]), 1)

    def test_invalid_input_json_utf8_and_constants_fail_closed(self):
        self.init()
        before = self.path.read_bytes()
        for payload in ("{", "[]", '{"id":"first","id":"second"}', '{"id":NaN}'):
            self.assertEqual(self.cli("--scope", self.scope, "upsert", stdin=payload)[0], 1)
            self.assertEqual(self.path.read_bytes(), before)
        self.path.write_bytes(b"\xff")
        self.assertEqual(self.cli("--scope", self.scope, "seen", "v2")[0], 1)
        self.assertEqual(self.path.read_bytes(), b"\xff")

    def test_failure_after_replace_requires_readback_not_assumed_rollback(self):
        self.init()
        original_fsync = threads.os.fsync
        calls = []

        def fsync(fd):
            calls.append(fd)
            if len(calls) == 2:  # Directory sync, after replacement.
                raise OSError("synthetic directory sync failure")
            return original_fsync(fd)

        with mock.patch.object(threads.os, "fsync", side_effect=fsync):
            code, _, err = self.cli("--scope", self.scope, "upsert",
                                    stdin=json.dumps(self.record()))
        self.assertEqual(code, 1)
        self.assertIn("directory sync failure", err)
        self.assertEqual(len(threads.read_checkpoint(self.path)["threads"]), 1)
        self.assertEqual(list(self.directory.glob(".threads-*.tmp")), [])
        self.upsert()  # Failure still released the lock.

    def test_invalid_stdin_cannot_initialize_checkpoint(self):
        code, _, _ = self.cli("--scope", self.scope, "upsert", stdin="{broken")
        self.assertEqual(code, 1)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_unscoped_listing_does_not_prune_or_refresh_stale_panes(self):
        self.init()
        self.upsert()
        before = self.path.read_bytes()
        code, out, err = self.cli("list")
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["threads"][0]["state"], "active")
        self.assertEqual(self.path.read_bytes(), before)

    def test_dangling_symlink_is_not_replaced(self):
        self.directory.mkdir()
        self.path.symlink_to(self.directory / "missing.json")
        with self.assertRaises(threads.CheckpointError):
            self.init()
        self.assertTrue(self.path.is_symlink())
        self.assertFalse((self.directory / "missing.json").exists())

    def test_no_environment_identity_or_external_session_discovery(self):
        with mock.patch.dict("os.environ", {"HERDR_ENV": "1", "HERDR_SOCKET": "other"}, clear=True):
            self.assertNotEqual(self.cli("init", "--version", "local")[0], 0)
            self.init()
            self.assertEqual(threads.read_checkpoint(self.path)["session_scope"], self.scope)

    def test_missing_checkpoint_inside_existing_directory_still_needs_init(self):
        self.directory.mkdir()
        self.assertEqual(self.cli("list")[0], 0)
        self.assertEqual(list(self.directory.iterdir()), [])
        with self.assertRaises(threads.CheckpointError):
            self.upsert()
        self.assertFalse(self.path.exists())


if __name__ == "__main__":
    unittest.main()
