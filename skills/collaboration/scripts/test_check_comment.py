"""Deterministic size-check regressions; no live connector calls."""

import json
from pathlib import Path
import subprocess
import sys
import unittest

from check_comment import measure


SCRIPT = Path(__file__).with_name("check_comment.py")


class CheckCommentTests(unittest.TestCase):
    def run_cli(self, text, *args):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            input=text, text=True, capture_output=True, check=False,
        )
        return result

    def test_default_budget_boundary(self):
        for length, status in ((3500, 0), (3501, 1)):
            with self.subTest(length=length):
                result = self.run_cli("a" * length)
                self.assertEqual(result.returncode, status)
                self.assertEqual(json.loads(result.stdout)["length"], length)

    def test_final_signature_counts(self):
        body = "a" * 3490
        self.assertEqual(self.run_cli(body).returncode, 0)
        self.assertEqual(self.run_cli(body + "\n\n— fx (AI assistant)").returncode, 1)

    def test_astral_emoji_counts_as_two_utf16_units(self):
        result = self.run_cli("😀" * 1750)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["length"], 3500)
        self.assertEqual(self.run_cli("😀" * 1751).returncode, 1)

    def test_explicit_ceiling(self):
        self.assertEqual(self.run_cli("a" * 4000, "--limit", "4000").returncode, 0)
        self.assertEqual(self.run_cli("a" * 4001, "--limit", "4000").returncode, 1)

    def test_counting_units_are_distinct(self):
        text = "é😀"
        self.assertEqual(measure(text, "codepoints"), 2)
        self.assertEqual(measure(text, "utf16"), 3)
        self.assertEqual(measure(text, "utf8"), 6)

    def test_whitespace_links_and_labels_count(self):
        text = "Part 1/2\nSee https://example.test/review\n\n— AI assistant\n"
        self.assertEqual(measure(text, "utf16"), len(text))
        self.assertEqual(json.loads(self.run_cli(text).stdout)["length"], len(text))

    def test_lower_connector_budget(self):
        result = self.run_cli("a" * 2001, "--limit", "2000", "--units", "codepoints")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["units"], "codepoints")

    def test_invalid_limit_rejected(self):
        for limit in ("0", "-1", "not-a-number"):
            with self.subTest(limit=limit):
                self.assertEqual(self.run_cli("text", "--limit", limit).returncode, 2)

    def test_invalid_units_rejected(self):
        self.assertEqual(self.run_cli("text", "--units", "words").returncode, 2)

    def test_output_does_not_disclose_comment_content(self):
        result = self.run_cli("PRIVATE COMMENT")
        self.assertNotIn("PRIVATE COMMENT", result.stdout + result.stderr)
        self.assertEqual(set(json.loads(result.stdout)), {"fits", "length", "limit", "units"})


if __name__ == "__main__":
    unittest.main()
