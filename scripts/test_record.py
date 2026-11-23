#!/usr/bin/env python3
"""Tests for the record helper. Standard library only; no network."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import tempfile
import unittest
from pathlib import Path

HELPER = Path(__file__).resolve().parent.parent / "skills" / "yoinker" / "scripts" / "record.py"
spec = importlib.util.spec_from_file_location("record", HELPER)
record = importlib.util.module_from_spec(spec)
spec.loader.exec_module(record)

REPO = "https://github.com/example-org/example-tool"


def run(*argv: str) -> tuple[int, str]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        code = record.main(list(argv))
    return code, out.getvalue().strip()


class RecordTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name).resolve()
        self.project = base / "project"
        (self.project / ".git").mkdir(parents=True)
        (self.project / "src").mkdir()
        self.loose = base / "loose"
        self.loose.mkdir()
        self.store = base / "data" / "yoinker"
        saved = {key: os.environ.get(key) for key in ("XDG_DATA_HOME", "YOINKER_HOME")}
        self.addCleanup(lambda: [self._restore(key, value) for key, value in saved.items()])
        os.environ["XDG_DATA_HOME"] = str(base / "data")
        os.environ.pop("YOINKER_HOME", None)

    @staticmethod
    def _restore(key: str, value: str | None) -> None:
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value

    def test_records_go_in_the_project_from_any_subdirectory(self) -> None:
        code, out = run("where", "--project", str(self.project / "src"))
        self.assertEqual(code, 0)
        self.assertEqual(Path(out), self.project / "docs" / "yoinker")

    def test_without_a_project_records_go_in_the_per_user_store(self) -> None:
        if record.project_root(self.loose) is not None:
            self.skipTest("temporary directory sits inside a git work tree")
        _, out = run("where", "--project", str(self.loose))
        self.assertEqual(Path(out), self.store / "records")

    def test_yoinker_home_overrides_the_xdg_location(self) -> None:
        os.environ["YOINKER_HOME"] = str(self.loose / "elsewhere")
        _, out = run("where", "--project", str(self.project), "--shared")
        self.assertEqual(Path(out), self.loose / "elsewhere" / "records")

    def test_new_writes_one_stable_record_and_refuses_a_duplicate(self) -> None:
        code, out = run("new", REPO + "/tree/main/docs", "--no-pin", "--project", str(self.project))
        self.assertEqual(code, 0)
        path = Path(out)
        self.assertEqual(path.name, "github-example-org-example-tool.md")
        text = path.read_text(encoding="utf-8")
        self.assertIn("- Source: " + REPO, text)
        self.assertIn("not pinned", text)
        self.assertIn("## Transfer decisions", text)
        self.assertIn("## Outcome log", text)
        code, again = run("new", REPO, "--no-pin", "--project", str(self.project))
        self.assertEqual(code, 2)
        self.assertEqual(Path(again), path)

    def test_a_record_is_found_from_another_project_through_the_index(self) -> None:
        _, out = run("new", REPO, "--no-pin", "--project", str(self.project))
        other = Path(self.tmp.name).resolve() / "other"
        (other / ".git").mkdir(parents=True)
        code, found = run("find", "example-tool", "--project", str(other))
        self.assertEqual(code, 0)
        self.assertIn(out, found)
        self.assertIn("indexed from another project", found)
        code, _ = run("find", "something-never-assessed", "--project", str(other))
        self.assertEqual(code, 1)

    def test_a_question_becomes_a_shared_record_without_a_revision_line(self) -> None:
        _, out = run("new", "How do these approaches differ?", "--shared")
        path = Path(out)
        self.assertEqual(path.parent, self.store / "records")
        self.assertTrue(path.name.startswith("question-how-do-these"))
        text = path.read_text(encoding="utf-8")
        self.assertIn("- Question: How do these approaches differ?", text)
        self.assertNotIn("Pinned revision", text)

    def test_only_plain_https_forge_repositories_are_pinned(self) -> None:
        for hostile in (
            "ext::sh -c id",
            "https://github.com/--upload-pack=touch/x",
            "ssh://github.com/a/b",
            "https://example.com/a/b",
            "file:///etc/passwd",
        ):
            self.assertIsNone(record.forge_repo(hostile), hostile)
            revision, note = record.pin_revision(hostile)
            self.assertIsNone(revision)
            self.assertIn("not pinned", note)
        self.assertEqual(
            record.forge_repo(REPO + ".git"), ("github.com", "example-org", "example-tool")
        )


if __name__ == "__main__":
    unittest.main()
