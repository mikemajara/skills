"""Offline only: subprocess, socket stat and inherited environment are mocked."""

import ast
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("navigation", ROOT / "navigation.py")
nav = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nav)


class NavigationTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {
            "HERDR_ENV": "1", "HERDR_SOCKET_PATH": "/tmp/synthetic-herdr.sock",
            "HERDR_BIN_PATH": "/opt/synthetic/herdr",
            "HERDR_PLUGIN_ID": "shepherd-navigation",
            "HERDR_PLUGIN_ACTION_ID": "focus",
        }, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)
        self.socket = SimpleNamespace(st_mode=stat.S_IFSOCK, st_dev=7, st_ino=42)
        self.stat = patch.object(nav.os, "stat", return_value=self.socket).start()
        self.addCleanup(patch.stopall)
        self.pane = {"pane_id": "w1:p2", "workspace_id": "w1",
                     "terminal_id": "terminal-0123", "agent_session": None}
        self.workspace = {"workspace_id": "w1"}
        self.run = patch.object(nav.subprocess, "run", side_effect=self.respond).start()

    def respond(self, argv, **kwargs):
        self.assertEqual(argv[0], "/opt/synthetic/herdr")
        self.assertFalse(kwargs["shell"])
        self.assertEqual(kwargs["cwd"], str(ROOT))
        self.assertEqual(kwargs["env"]["HERDR_SOCKET_PATH"], "/tmp/synthetic-herdr.sock")
        self.assertEqual(kwargs["stdin"], subprocess.DEVNULL)
        self.assertEqual(kwargs["timeout"], 10)
        commands = {
            ("pane", "get", "w1:p2"): {"pane": self.pane},
            ("agent", "get", "w1:p2"): {"agent": self.pane.copy()},
            ("workspace", "get", "w1"): {"workspace": self.workspace},
            ("agent", "focus", "w1:p2"): {"agent": self.pane},
            ("workspace", "focus", "w1"): {"workspace": self.workspace},
        }
        self.assertIn(tuple(argv[1:]), commands, "unexpected command")
        return SimpleNamespace(returncode=0, stdout=json.dumps({"result": commands[tuple(argv[1:])]}))

    def focus_calls(self):
        return [c.args[0] for c in self.run.call_args_list if "focus" in c.args[0][1:]]

    def click(self, url, **overrides):
        context = {"invocation_source": "link_click", "clicked_url": url,
                   "link_handler_id": "destination"}
        context.update(overrides)
        os.environ["HERDR_PLUGIN_CONTEXT_JSON"] = json.dumps(context)
        return nav.main(["handle"])

    def assert_rejected(self, url, **overrides):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.click(url, **overrides), 1)
        self.assertEqual(self.focus_calls(), [])

    def test_pane_link_is_read_only_and_opaque(self):
        url = nav.make_link("pane", "w1:p2")
        self.assertRegex(url, r"\Ashepherd://[a-f0-9]{64}/pane/w1:p2/[a-f0-9]{64}\Z")
        self.assertNotIn("synthetic-herdr", url)
        self.assertNotIn("terminal-0123", url)
        self.assertEqual(self.focus_calls(), [])
        self.assertEqual(len(self.run.call_args_list), 2)

    def test_workspace_link_is_read_only(self):
        nav.make_link("workspace", "w1")
        self.assertEqual(self.focus_calls(), [])
        self.run.assert_called_once()

    def test_explicit_pane_click_focuses_only_destination(self):
        url = nav.make_link("pane", "w1:p2")
        self.run.reset_mock()
        self.assertEqual(self.click(url), 0)
        self.assertEqual(self.focus_calls(), [["/opt/synthetic/herdr", "agent", "focus", "w1:p2"]])
        self.assertEqual(len(self.run.call_args_list), 3)

    def test_explicit_workspace_click_focuses_only_destination(self):
        url = nav.make_link("workspace", "w1")
        self.run.reset_mock()
        self.assertEqual(self.click(url), 0)
        self.assertEqual(self.focus_calls(), [["/opt/synthetic/herdr", "workspace", "focus", "w1"]])
        self.assertEqual(len(self.run.call_args_list), 2)

    def test_wrong_terminal_occupant(self):
        url = nav.make_link("pane", "w1:p2")
        self.pane["terminal_id"] = "replacement"
        self.assert_rejected(url)

    def test_changed_agent_session_same_terminal(self):
        url = nav.make_link("pane", "w1:p2")
        self.pane["agent_session"] = {"agent": "synthetic", "kind": "id", "value": "new"}
        self.assert_rejected(url)

    def test_missing_terminal_identity(self):
        self.pane.pop("terminal_id")
        with self.assertRaises(nav.NavigationError):
            nav.make_link("pane", "w1:p2")
        self.assertEqual(self.focus_calls(), [])

    def test_inconsistent_agent_identity(self):
        original = self.respond
        def changed(argv, **kwargs):
            if argv[1:3] == ["agent", "get"]:
                return SimpleNamespace(returncode=0, stdout=json.dumps({"result": {"agent": {
                    "pane_id": "w1:p2", "terminal_id": "replacement"}}}))
            return original(argv, **kwargs)
        self.run.side_effect = changed
        with self.assertRaises(nav.NavigationError):
            nav.make_link("pane", "w1:p2")
        self.assertEqual(self.focus_calls(), [])

    def test_session_changed_between_pane_and_agent_reads(self):
        original = self.respond
        def changed(argv, **kwargs):
            if argv[1:3] == ["agent", "get"]:
                agent = dict(self.pane, agent_session={"value": "replacement"})
                return SimpleNamespace(returncode=0, stdout=json.dumps({"result": {"agent": agent}}))
            return original(argv, **kwargs)
        self.run.side_effect = changed
        with self.assertRaises(nav.NavigationError):
            nav.make_link("pane", "w1:p2")
        self.assertEqual(self.focus_calls(), [])

    def test_pane_gone_before_click(self):
        url = nav.make_link("pane", "w1:p2")
        self.pane["pane_id"] = "w1:p3"
        self.assert_rejected(url)

    def test_link_generation_in_click_environment_still_read_only(self):
        os.environ["HERDR_PLUGIN_CONTEXT_JSON"] = json.dumps({
            "invocation_source": "link_click", "link_handler_id": "destination"})
        nav.make_link("pane", "w1:p2")
        nav.make_link("workspace", "w1")
        self.assertEqual(self.focus_calls(), [])

    def test_focus_failure_is_reported_without_retry(self):
        url = nav.make_link("workspace", "w1")
        self.run.reset_mock()
        original = self.respond
        def failed(argv, **kwargs):
            if argv[1:3] == ["workspace", "focus"]:
                return SimpleNamespace(returncode=1, stdout="")
            return original(argv, **kwargs)
        self.run.side_effect = failed
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.click(url), 1)
        self.assertEqual(len(self.focus_calls()), 1)
        self.assertEqual(len(self.run.call_args_list), 2)

    def test_wrong_sessions_restart_or_path(self):
        url = nav.make_link("pane", "w1:p2")
        for field, value in (("st_ino", 43), ("st_dev", 8)):
            with self.subTest(field=field):
                old = getattr(self.socket, field)
                setattr(self.socket, field, value)
                self.run.reset_mock()
                self.assert_rejected(url)
                self.run.assert_not_called()
                setattr(self.socket, field, old)
        os.environ["HERDR_SOCKET_PATH"] = "/tmp/other-session.sock"
        self.run.reset_mock()
        self.assert_rejected(url)
        self.run.assert_not_called()

    def test_session_stable_across_reads_and_panes(self):
        key = nav.session_key()
        os.environ["HERDR_PANE_ID"] = "w9:p7"
        self.assertEqual(nav.session_key(), key)
        self.assertEqual(len(key), 64)

    def test_no_herdr_or_inherited_socket(self):
        for env, value in (("HERDR_ENV", "0"), ("HERDR_SOCKET_PATH", ""),
                           ("HERDR_SOCKET_PATH", "relative.sock")):
            with self.subTest(env=env, value=value), patch.dict(os.environ, {env: value}):
                with self.assertRaises(nav.NavigationError):
                    nav.make_link("workspace", "w1")
        self.run.assert_not_called()

    def test_not_a_socket_or_missing_socket(self):
        self.socket.st_mode = stat.S_IFREG
        with self.assertRaises(nav.NavigationError):
            nav.make_link("workspace", "w1")
        self.stat.side_effect = FileNotFoundError("socket missing")
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(nav.main(["link", "workspace", "w1"]), 1)
        self.run.assert_not_called()

    def test_non_click_context_cannot_focus(self):
        url = nav.make_link("workspace", "w1")
        self.run.reset_mock()
        for source in (None, "action", "cli", "startup", "link_click "):
            self.assert_rejected(url, invocation_source=source)
        self.assert_rejected(url, link_handler_id="other")
        self.run.assert_not_called()

    def test_wrong_plugin_cannot_focus(self):
        url = nav.make_link("workspace", "w1")
        self.run.reset_mock()
        for key in ("HERDR_PLUGIN_ID", "HERDR_PLUGIN_ACTION_ID"):
            with patch.dict(os.environ, {key: "other"}):
                self.assert_rejected(url)
        self.run.assert_not_called()

    def test_invalid_context(self):
        for text in ("", "{", "null", "[]", "1", '"text"'):
            os.environ["HERDR_PLUGIN_CONTEXT_JSON"] = text
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(nav.main(["handle"]), 1)
        self.run.assert_not_called()

    def test_strict_raw_url_validation(self):
        good = nav.make_link("pane", "w1:p2")
        bad = [None, 42, "", good + "?x=1", good + "?", good + "#", good + "#x",
               good + "/", good + "\n", " " + good, good + " ", good + "\x00",
               good.replace("shepherd:", "SHEPHERD:"), good.replace("shepherd:", "https:"),
               good.replace("://", ":///"), good.replace("://", "://user@"),
               good.replace("/pane/", ":80/pane/"), good.replace("/pane/", "/pane//"),
               good.replace("/pane/", "/../pane/"), good.replace("/pane/", "/focus/"),
               good.replace("w1:p2", "w1%3Ap2"), good.replace("w1:p2", "w1%253Ap2"),
               good.replace("w1:p2", "w1:p2;id"), good.replace("w1:p2", "$(id)"),
               good.replace("w1:p2", "--session"), good.replace("w1:p2", "w1\\p2"),
               good.replace("w1:p2", "w1/evil"), good.replace("w1:p2", "é"),
               good.rsplit("/", 1)[0], good + "/extra", "x" * 513]
        self.run.reset_mock()
        for url in bad:
            with self.subTest(url=url):
                self.assert_rejected(url)
        self.run.assert_not_called()

    def test_bad_cli_ids_and_kinds_do_not_run_commands(self):
        for target in ("--session", "../w1", "w1;id", "w1?x", "", "x" * 129):
            with self.subTest(target=target), self.assertRaises(nav.NavigationError):
                nav.make_link("workspace", target)
        with self.assertRaises(nav.NavigationError):
            nav.make_link("command", "w1")
        self.run.assert_not_called()

    def test_bad_cli_options_are_not_accepted(self):
        with contextlib.redirect_stderr(io.StringIO()):
            for args in (["handle", "shepherd://anything"],
                         ["link", "workspace", "w1", "--socket", "/tmp/other"],
                         ["link", "pane", "w1:p2", "--command", "id"]):
                with self.assertRaises(SystemExit) as exc:
                    nav.main(args)
                self.assertEqual(exc.exception.code, 2)
        self.run.assert_not_called()

    def test_response_errors_and_missing_targets_fail_closed(self):
        url = nav.make_link("workspace", "w1")
        for text in ("bad JSON", "null", "[]", '{"error": {}}', '{"result": null}',
                     '{"result": {}}', '{"result": {"workspace": null}}',
                     '{"result": {"workspace": {"workspace_id": "w2"}}}',
                     '{"result": {}, "error": null}'):
            with self.subTest(text=text):
                self.run.return_value = SimpleNamespace(returncode=0, stdout=text)
                self.run.side_effect = None
                self.assert_rejected(url)

    def test_subprocess_failure_does_not_focus(self):
        url = nav.make_link("pane", "w1:p2")
        for failure in (subprocess.TimeoutExpired("herdr", 10), OSError("missing binary")):
            self.run.side_effect = failure
            self.assert_rejected(url)
        self.run.side_effect = None
        self.run.return_value = SimpleNamespace(returncode=1, stdout="")
        self.assert_rejected(url)

    def test_socket_replaced_during_validation(self):
        url = nav.make_link("workspace", "w1")
        before = SimpleNamespace(st_mode=stat.S_IFSOCK, st_dev=7, st_ino=42)
        after = SimpleNamespace(st_mode=stat.S_IFSOCK, st_dev=7, st_ino=43)
        self.stat.side_effect = [before, after]
        self.assert_rejected(url)

    def test_socket_replaced_during_link_creation(self):
        before = SimpleNamespace(st_mode=stat.S_IFSOCK, st_dev=7, st_ino=42)
        after = SimpleNamespace(st_mode=stat.S_IFSOCK, st_dev=7, st_ino=43)
        self.stat.side_effect = [before, after]
        with self.assertRaises(nav.NavigationError):
            nav.make_link("workspace", "w1")
        self.assertEqual(self.focus_calls(), [])

    def test_cli_link_prints_url_without_focus(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(nav.main(["link", "workspace", "w1"]), 0)
        self.assertIsNotNone(nav.URL.fullmatch(out.getvalue().rstrip("\n")))
        self.assertEqual(self.focus_calls(), [])

    def test_scope_is_restart_stable_but_click_key_is_not(self):
        scope = nav.checkpoint_scope()
        click_key = nav.session_key()
        self.socket.st_dev += 1
        self.socket.st_ino += 1
        self.assertEqual(nav.checkpoint_scope(), scope)
        self.assertNotEqual(nav.session_key(), click_key)
        self.assertRegex(scope, r"\A[a-f0-9]{64}\Z")
        self.assertNotEqual(scope, click_key)
        self.assertEqual(scope, nav.digest([
            "shepherd-checkpoint-scope-v1", "/tmp/synthetic-herdr.sock"]))
        self.run.assert_not_called()

    def test_scope_changes_with_socket_path_not_pane_or_cwd(self):
        scope = nav.checkpoint_scope()
        os.environ["HERDR_PANE_ID"] = "w9:p7"
        with patch.object(nav.os, "getcwd", return_value="/elsewhere"):
            self.assertEqual(nav.checkpoint_scope(), scope)
        os.environ["HERDR_SOCKET_PATH"] = "/tmp/another-session.sock"
        self.assertNotEqual(nav.checkpoint_scope(), scope)
        self.run.assert_not_called()

    def test_scope_cli_is_read_only_even_in_click_context(self):
        os.environ["HERDR_PLUGIN_CONTEXT_JSON"] = json.dumps({
            "invocation_source": "link_click", "link_handler_id": "destination"})
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(nav.main(["scope"]), 0)
        self.assertEqual(out.getvalue(), nav.checkpoint_scope() + "\n")
        self.run.assert_not_called()

    def test_scope_rejects_invalid_environment_or_socket(self):
        for key, value in (("HERDR_ENV", ""), ("HERDR_ENV", "0"),
                           ("HERDR_SOCKET_PATH", ""), ("HERDR_SOCKET_PATH", "relative.sock")):
            with self.subTest(key=key, value=value), patch.dict(os.environ, {key: value}):
                with contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(nav.main(["scope"]), 1)
        self.socket.st_mode = stat.S_IFREG
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(nav.main(["scope"]), 1)
        self.stat.side_effect = FileNotFoundError("socket missing")
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(nav.main(["scope"]), 1)
        self.run.assert_not_called()

    def test_scope_accepts_no_socket_or_session_overrides(self):
        for args in (["scope", "/tmp/other.sock"], ["scope", "--socket", "/tmp/other.sock"],
                     ["scope", "--session", "other"]):
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as exc:
                    nav.main(args)
                self.assertEqual(exc.exception.code, 2)
        self.run.assert_not_called()

    def test_manifest_contract_and_routing(self):
        text = (ROOT / "herdr-plugin.toml").read_text()
        for expected in ('id = "shepherd-navigation"', 'version = "0.1.0"',
                         '[[actions]]', '[[link_handlers]]', 'action = "focus"',
                         'command = ["python3", "navigation.py", "handle"]'):
            self.assertIn(expected, text)
        pattern = ast.literal_eval(next(line.split(" = ", 1)[1]
                                        for line in text.splitlines() if line.startswith("pattern = ")))
        for kind, target in (("pane", "w1:p2"), ("workspace", "w1")):
            self.assertIsNotNone(re.fullmatch(pattern, nav.make_link(kind, target)))
        self.assertNotIn("[[startup]]", text)
        self.assertNotIn("[[events]]", text)


if __name__ == "__main__":
    unittest.main()
