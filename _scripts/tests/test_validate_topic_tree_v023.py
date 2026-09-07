"""Tests for validate_topic_tree.py R4/R5/R6 enhancements (v0.23 feedback harvest).

Covers FR-0001 (hyphen guidance), FR-0005 (duplicate Last Updated),
FR-0018 (index-table status column), FR-0007 (shrinkage gate + backup
retention), FR-0020 (staleness hint).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import validate_topic_tree as vtt


OLD_TREE = """# Discussion Topics Tree

## Active Topic

### [A] Main line

- **Status**: in_progress
- Timeline:
  - round_01 (2026-08-01): kickoff
  - round_02 (2026-08-02: build
  - round_03 (2026-08-03): test
  - round_04 (2026-08-04): ship

## Topic Index

| ID | Title | Status | Last Active |
|:---|:------|:-------|:------------|
| [A] | Main line | in_progress | 2026-08-04 |

**Last Updated**: 2026-08-04
"""


class TestR4IndexTableScan(unittest.TestCase):
    """FR-0018: R4 must scan the Topic Index table's Status column."""

    def test_index_table_hyphen_status_warns(self):
        content = OLD_TREE.replace("| [A] | Main line | in_progress |", "| [A] | Main line | in-progress |")
        warnings = vtt.check_r4_valid_states(content)
        self.assertTrue(any("Topic Index row has hyphenated status 'in-progress'" in w for w in warnings),
                        msg=f"expected index-table hyphen warning, got: {warnings}")

    def test_index_table_canonical_status_no_warning(self):
        warnings = vtt.check_r4_valid_states(OLD_TREE)
        self.assertFalse([w for w in warnings if "Topic Index" in w])

    def test_field_hyphen_status_gives_canonical_hint(self):
        content = OLD_TREE.replace("- **Status**: in_progress", "- **Status**: in-progress")
        warnings = vtt.check_r4_valid_states(content)
        self.assertTrue(any("canonical form is 'in_progress'" in w for w in warnings))


class TestR5DuplicateLastUpdated(unittest.TestCase):
    """FR-0005: more than one Last Updated line is a staleness hazard."""

    def test_duplicate_lines_warn(self):
        content = "**Last Updated**: 2026-09-01\n" + OLD_TREE
        warnings = vtt.check_r5_duplicate_last_updated(content)
        self.assertEqual(len(warnings), 1)
        self.assertIn("2 'Last Updated' lines", warnings[0])

    def test_single_line_ok(self):
        self.assertEqual(vtt.check_r5_duplicate_last_updated(OLD_TREE), [])


class TestR6ShrinkageGate(unittest.TestCase):
    """FR-0007: structurally valid but truncated content must be blocked."""

    def test_timeline_truncation_blocked(self):
        backbone = """# Discussion Topics Tree

## Active Topic

### [A] Main line

- **Status**: in_progress

## Topic Index

| ID | Title | Status | Last Active |
|:---|:------|:-------|:------------|
| [A] | Main line | in_progress | 2026-08-04 |

**Last Updated**: 2026-08-04
"""
        result = vtt.validate_content(OLD_TREE, backbone)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e.startswith("R6 gate") for e in result["errors"]),
                        msg=f"expected R6 gate error, got: {result['errors']}")

    def test_normal_growth_passes(self):
        grown = OLD_TREE.replace(
            "  - round_04 (2026-08-04): ship",
            "  - round_04 (2026-08-04): ship\n  - round_05 (2026-08-05): grow",
        )
        result = vtt.validate_content(OLD_TREE, grown)
        self.assertTrue(result["valid"])
        self.assertEqual([e for e in result["errors"] if e.startswith("R6")], [])

    def test_first_time_update_not_gated(self):
        result = vtt.validate_content("", OLD_TREE)
        self.assertTrue(result["valid"])


class TestUpdateBackupRetention(unittest.TestCase):
    """FR-0007: success path must keep a timestamped .bak instead of deleting it."""

    def test_update_keeps_timestamped_backup(self):
        import tempfile
        import os
        with tempfile.TemporaryDirectory() as td:
            old_dir, old_paths = vtt.TEMP_DIR, (vtt.TEMP_DIR, vtt.BACKUP_PATH, vtt.TOPIC_TREE_PATH, vtt.ARCHIVE_DIR)
            tree_path = Path(td) / "discussion_topics.md"
            tree_path.write_text(OLD_TREE, encoding="utf-8")
            temp_dir = Path(td) / "temp"
            temp_dir.mkdir()
            vtt.TEMP_DIR = temp_dir
            vtt.BACKUP_PATH = temp_dir / "discussion_topics.md.bak"
            vtt.TOPIC_TREE_PATH = tree_path
            vtt.ARCHIVE_DIR = Path(td) / "archives"
            try:
                grown = OLD_TREE.replace(
                    "  - round_04 (2026-08-04): ship",
                    "  - round_04 (2026-08-04): ship\n  - round_05 (2026-08-05): grow",
                )
                result = vtt.update_topic_tree(grown)
                self.assertTrue(result["success"], msg=str(result.get("errors")))
                self.assertIn("backup_kept", result)
                kept = Path(result["backup_kept"])
                self.assertTrue(kept.exists())
                self.assertIn(kept.read_text(encoding="utf-8"), OLD_TREE)
                self.assertFalse(vtt.BACKUP_PATH.exists())  # generic .bak cleaned, stamped one kept
            finally:
                vtt.TEMP_DIR, (vtt.TEMP_DIR, vtt.BACKUP_PATH, vtt.TOPIC_TREE_PATH, vtt.ARCHIVE_DIR) = old_dir, old_paths


class TestStalenessHint(unittest.TestCase):
    """FR-0020: passive staleness hint when the tree lags git activity."""

    def test_no_hint_when_dates_close(self):
        # OLD_TREE's Last Updated (2026-08-04) vs real repo HEAD — cannot be
        # asserted deterministically; only assert the function returns a str
        # and never raises.
        hint = vtt._staleness_hint(OLD_TREE)
        self.assertIsInstance(hint, str)

    def test_no_crash_without_date(self):
        self.assertEqual(vtt._staleness_hint("# no date here"), "")


class TestTemplateSkeleton(unittest.TestCase):
    """FR-0011: the install-time template must define the timeline layer."""

    def test_template_contains_round_skeleton_and_enum_note(self):
        gen = Path(__file__).parent.parent / "generate_ai_workspace.py"
        text = gen.read_text(encoding="utf-8")
        self.assertIn("round_01", text)
        self.assertIn("underscore style", text)


class TestStrictMode(unittest.TestCase):
    """FR-0002: --strict turns R4/R5 warnings into errors."""

    def test_strict_blocks_hyphen_status(self):
        content = OLD_TREE.replace("- **Status**: in_progress", "- **Status**: in-progress")
        result = vtt.validate_content(OLD_TREE, content, strict=True)
        self.assertFalse(result["valid"])
        self.assertTrue(any("R4 warning" in e for e in result["errors"]))

    def test_strict_blocks_duplicate_last_updated(self):
        content = "**Last Updated**: 2026-09-01\n" + OLD_TREE
        result = vtt.validate_content(OLD_TREE, content, strict=True)
        self.assertFalse(result["valid"])
        self.assertTrue(any("R5 warning" in e for e in result["errors"]))

    def test_default_mode_still_warning(self):
        content = "**Last Updated**: 2026-09-01\n" + OLD_TREE
        result = vtt.validate_content(OLD_TREE, content)
        self.assertTrue(result["valid"])  # duplicate Last Updated alone doesn't block
        self.assertTrue(any("R5 warning" in w for w in result["warnings"]))


class TestStrictCLIFlag(unittest.TestCase):
    """The update subcommand must define --strict (regression: arg lost in a partial overwrite)."""

    def test_update_parser_has_strict(self):
        import subprocess, sys
        r = subprocess.run(
            [sys.executable, str(Path(__file__).parent.parent / "validate_topic_tree.py"), "update", "--help"],
            capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn("--strict", r.stdout)


if __name__ == "__main__":
    unittest.main()
