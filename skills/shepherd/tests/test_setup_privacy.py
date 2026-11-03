"""Test the documented recipe, not a setup helper; Git runs only in temp repos.

Read the actual Markdown pattern blocks so tests cannot silently use safer rules
than the reference. No commits, harness access or real user configuration writes.
"""

import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


REFERENCE = Path(__file__).resolve().parents[1] / "references" / "setup.md"


class PrivacyBlocked(Exception):
    """The documented gate refused a write."""


@unittest.skipUnless(shutil.which("git"), "requires Git")
class SetupPrivacyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.repo = self.base / "repo"
        self.repo.mkdir()
        # Do not inherit Git redirection, injected config, global ignores or hooks.
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith("GIT_")}
        self.env.update(HOME=str(self.base), XDG_CONFIG_HOME=str(self.base / "xdg"),
                        GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_TERMINAL_PROMPT="0", LC_ALL="C")
        self.git("init", "-q", "--template=")
        self.write(self.exclude(self.repo), "")
        document = REFERENCE.read_text(encoding="utf-8")
        self.blocks = dict(zip(("local", "share"), re.findall(
            r"```gitignore\n(.*?)```", document, re.DOTALL)))
        self.assertEqual(set(self.blocks), {"local", "share"})

    def git(self, *args, cwd=None, check=True):
        directory = Path(cwd) if cwd is not None else self.repo
        # Every Git invocation, including negative/error checks, is sandboxed.
        directory.resolve().relative_to(self.base)
        return subprocess.run(["git", *args], cwd=directory, env=self.env,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              check=check)

    def root(self, prefix):
        root = self.repo / prefix
        root.mkdir(parents=True, exist_ok=True)
        return root

    def relative(self, root):
        return (root / ".shepherd").relative_to(self.repo).as_posix()

    def exclude(self, root):
        output = self.git("rev-parse", "--path-format=absolute", "--git-path",
                          "info/exclude", cwd=root).stdout
        path = Path(os.fsdecode(output).rstrip("\n"))
        self.assertTrue(path.is_absolute())
        path.resolve().relative_to(self.base)
        return path

    def write(self, path, content="synthetic\n"):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def precheck(self, root, mode):
        relative = self.relative(root)
        result = self.git("ls-files", "--cached", "--full-name", "-z", "--",
                          f":(top,literal){relative}")
        tracked = [os.fsdecode(path) for path in result.stdout.split(b"\0") if path]
        allowed = {relative + "/instructions.md"} if mode == "share" else set()
        blocked = set(tracked) - allowed
        if blocked:
            raise PrivacyBlocked("tracked: " + ", ".join(sorted(blocked)))
        return tracked

    def append_rules(self, root, mode):
        # Test-only transcription of the reference's append/escape recipe.
        prefix = root.relative_to(self.repo).as_posix()
        prefix = "" if prefix == "." else prefix + "/"
        if "\n" in prefix or "\r" in prefix:
            raise PrivacyBlocked("unrepresentable prefix")
        escaped = "".join("\\" + char if char in "\\*?[]" else char
                          for char in prefix)
        block = self.blocks[mode].replace("{prefix}", escaped).encode()
        path = self.exclude(root)
        before = path.read_bytes() if path.exists() else b""
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("ab") as stream:
            if before and not before.endswith(b"\n"):
                stream.write(b"\n")
            stream.write(block)
        return before

    def ignored(self, path):
        result = self.git("check-ignore", "--no-index", "-q", "--", path,
                          check=False)
        if result.returncode not in (0, 1):
            raise PrivacyBlocked(f"check-ignore error {result.returncode}: "
                                 + os.fsdecode(result.stderr))
        return result.returncode == 0

    def validate(self, root, mode):
        relative = self.relative(root)
        instructions = root / ".shepherd/instructions.md"
        if instructions.is_symlink() or instructions.is_dir():
            raise PrivacyBlocked("instructions must be a regular file")
        if self.ignored(relative + "/instructions.md") != (mode == "local"):
            raise PrivacyBlocked("instructions ignore mismatch")
        runtime = {"threads.json", "threads.lock", ".threads-probe.tmp",
                   "unknown-runtime", "unknown-dir/", "unknown-dir/child"}
        directory = root / ".shepherd"
        if directory.exists():
            for path in directory.rglob("*"):
                name = path.relative_to(directory).as_posix()
                if name != "instructions.md":
                    runtime.add(name + ("/" if path.is_dir() else ""))
        for name in runtime:
            if not self.ignored(relative + "/" + name):
                raise PrivacyBlocked("runtime not ignored: " + name)

    def gate(self, root, mode):
        self.precheck(root, mode)  # Before exclude edits or sensitive writes.
        self.append_rules(root, mode)
        self.validate(root, mode)  # Before any synthetic configuration is saved.

    def test_missing_exclude_and_parent_are_created_only_in_resolved_git_path(self):
        root = self.root("team/app")
        exclude = self.exclude(root)
        exclude.unlink()
        exclude.parent.rmdir()
        self.gate(root, "local")
        self.assertEqual(exclude.read_text(), "/team/app/.shepherd/\n")
        self.assertFalse((root / ".shepherd").exists())

    def test_reference_blocks_are_exact(self):
        self.assertEqual(self.blocks["local"], "/{prefix}.shepherd/\n")
        self.assertEqual(self.blocks["share"],
                         "!/{prefix}.shepherd/\n/{prefix}.shepherd/*\n"
                         "!/{prefix}.shepherd/instructions.md\n")

    def test_root_and_nested_both_modes_unknown_runtime_and_preservation(self):
        for prefix in ("", "team/app"):
            for mode in ("local", "share"):
                with self.subTest(prefix=prefix, mode=mode):
                    root = self.root(prefix)
                    exclude = self.exclude(root)
                    original = b"# unrelated rules\n*.keep-local\nmanual-rule"
                    exclude.write_bytes(original)
                    shared = self.repo / ".gitignore"
                    self.write(shared, "# shared rules are user-owned\n*.cache\n")
                    before = shared.read_bytes()
                    self.gate(root, mode)
                    # Only after the gate: synthetic, non-sensitive saved data.
                    for name in ("instructions.md", "threads.json", "threads.lock",
                                 ".threads-crash.tmp", "backup.json", "new-runtime",
                                 "future-directory/private.txt"):
                        self.write(root / ".shepherd" / name)
                    self.validate(root, mode)
                    self.assertTrue(exclude.read_bytes().startswith(original + b"\n"))
                    self.assertTrue(self.ignored("outside.keep-local"))
                    self.assertTrue(self.ignored("manual-rule"))
                    self.assertEqual(shared.read_bytes(), before)
                    self.assertFalse(self.ignored("other/.shepherd/threads.json"))
                    if prefix:
                        self.assertFalse(self.ignored(".shepherd/threads.json"))
                    self.assertEqual(self.precheck(root, mode), [])

    def test_tracked_precheck_blocks_without_even_appending_rules(self):
        for prefix in ("", "team/app"):
            for mode in ("local", "share"):
                for name in ("instructions.md", "threads.json", "threads.lock",
                             "unknown/deep.txt"):
                    with self.subTest(prefix=prefix, mode=mode, name=name):
                        # A fresh temporary repo per case; add BEFORE ignore rules.
                        with tempfile.TemporaryDirectory(dir=self.base) as directory:
                            old_repo = self.repo
                            self.repo = Path(directory)
                            try:
                                self.git("init", "-q", "--template=")
                                self.write(self.exclude(self.repo), "")
                                root = self.root(prefix)
                                path = root / ".shepherd" / name
                                self.write(path)
                                self.git("add", "--", str(path))
                                exclude = self.exclude(root)
                                before = exclude.read_bytes()
                                index = self.git("ls-files", "--stage", "-z").stdout
                                if mode == "share" and name == "instructions.md":
                                    self.gate(root, mode)
                                    self.assertFalse(self.ignored(
                                        self.relative(root) + "/instructions.md"))
                                else:
                                    with self.assertRaisesRegex(PrivacyBlocked, "tracked:"):
                                        self.gate(root, mode)
                                    self.assertEqual(exclude.read_bytes(), before)
                                    self.assertFalse((root / ".shepherd/new-config").exists())
                                self.assertEqual(self.git("ls-files", "--stage", "-z").stdout,
                                                 index)
                                self.assertEqual(path.read_text(), "synthetic\n")
                            finally:
                                self.repo = old_repo

    def test_no_index_checks_do_not_replace_tracked_precheck(self):
        root = self.root("team/app")
        path = root / ".shepherd/threads.json"
        self.write(path)
        self.git("add", "--", str(path))
        self.append_rules(root, "local")
        self.assertTrue(self.ignored(self.relative(root) + "/threads.json"))
        with self.assertRaisesRegex(PrivacyBlocked, "tracked:"):
            self.precheck(root, "local")

    def test_share_conflicting_shared_ignores_stop_before_config_writes(self):
        for prefix, rule in (("", ".shepherd/\n"),
                             ("team/app", ".shepherd/\n"),
                             ("team/app", "/team/\n")):
            with self.subTest(prefix=prefix, rule=rule):
                root = self.root(prefix)
                shared = self.repo / ".gitignore"
                self.write(shared, rule)
                before = shared.read_bytes()
                with self.assertRaisesRegex(PrivacyBlocked, "instructions ignore mismatch"):
                    self.gate(root, "share")
                self.assertFalse((root / ".shepherd").exists())
                self.assertEqual(shared.read_bytes(), before)

    def test_higher_priority_runtime_negation_blocks_both_modes(self):
        for prefix in ("", "team/app"):
            for mode in ("local", "share"):
                with self.subTest(prefix=prefix, mode=mode):
                    root = self.root(prefix)
                    relative = self.relative(root)
                    shared = self.repo / ".gitignore"
                    instruction_rule = (f"/{relative}/instructions.md\n"
                                        if mode == "local" else "")
                    self.write(shared, f"!/{relative}/\n" + instruction_rule
                               + f"!/{relative}/threads.json\n")
                    before = shared.read_bytes()
                    with self.assertRaisesRegex(PrivacyBlocked, "runtime not ignored"):
                        self.gate(root, mode)
                    self.assertFalse((root / ".shepherd").exists())
                    self.assertEqual(shared.read_bytes(), before)

    def test_existing_unknown_runtime_conflict_is_checked(self):
        root = self.root("team/app")
        path = root / ".shepherd/old-backup/private.txt"
        self.write(path)
        shared = self.repo / ".gitignore"
        self.write(shared, "!/team/app/.shepherd/\n"
                          "!/team/app/.shepherd/old-backup/\n"
                          "!/team/app/.shepherd/old-backup/private.txt\n")
        with self.assertRaisesRegex(PrivacyBlocked, "runtime not ignored"):
            self.gate(root, "share")
        self.assertFalse((root / ".shepherd/instructions.md").exists())
        self.assertEqual(path.read_text(), "synthetic\n")

    def test_literal_tracked_path_and_escaped_ignore_prefix(self):
        root = self.root("group[1]*?/app")
        neighbor = self.root("group1ZZx/app")
        self.write(neighbor / ".shepherd/threads.json")
        self.git("add", "--", str(neighbor / ".shepherd/threads.json"))
        self.assertEqual(self.precheck(root, "local"), [])
        for mode in ("local", "share"):
            with self.subTest(mode=mode):
                self.gate(root, mode)
                self.assertFalse(self.ignored(self.relative(neighbor) + "/threads.json"))
        path = root / ".shepherd/threads.json"
        self.write(path)
        # New temporary index entry is staged before rules for this root are restored.
        self.exclude(root).write_bytes(b"")
        self.git("add", "--", str(path))
        with self.assertRaisesRegex(PrivacyBlocked, "tracked:"):
            self.precheck(root, "share")

    def test_verbose_negation_is_not_an_ignore_boolean(self):
        root = self.root("")
        self.gate(root, "share")
        path = ".shepherd/instructions.md"
        diagnostic = self.git("check-ignore", "--no-index", "-v", "--", path)
        self.assertIn(b"!/.shepherd/instructions.md", diagnostic.stdout)
        self.assertFalse(self.ignored(path))

    def test_check_ignore_exit_codes_including_nonrepo_error(self):
        root = self.root("")
        self.gate(root, "share")
        for path, expected in ((".shepherd/threads.json", 0),
                               (".shepherd/instructions.md", 1)):
            result = self.git("check-ignore", "--no-index", "-q", "--", path,
                              check=False)
            self.assertEqual(result.returncode, expected)
        outside = self.base / "nonrepo"
        outside.mkdir()
        result = self.git("check-ignore", "--no-index", "-q", "--", ".shepherd/x",
                          cwd=outside, check=False)
        self.assertEqual(result.returncode, 128)
        self.assertFalse((outside / ".git").exists())
        self.assertFalse((outside / ".shepherd").exists())

    def test_shared_instructions_cannot_be_a_directory_or_symlink(self):
        root = self.root("")
        instructions = root / ".shepherd/instructions.md"
        instructions.mkdir(parents=True)
        self.append_rules(root, "share")
        with self.assertRaisesRegex(PrivacyBlocked, "regular file"):
            self.validate(root, "share")
        instructions.rmdir()
        target = self.base / "private"
        self.write(target)
        instructions.symlink_to(target)
        with self.assertRaisesRegex(PrivacyBlocked, "regular file"):
            self.validate(root, "share")
        self.assertEqual(target.read_text(), "synthetic\n")


if __name__ == "__main__":
    unittest.main()
