"""
Unit tests for _openclaw/install.py helpers (PLAN-OC-001 stage 6, optional).
Run: python -m pytest cursor-agent-team/_openclaw/tests/test_install_helpers.py
or: python -m unittest cursor-agent-team._openclaw.tests.test_install_helpers
"""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
INSTALL = REPO / "_openclaw" / "install.py"


def _load_install():
    spec = importlib.util.spec_from_file_location("openclaw_install", INSTALL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["openclaw_install"] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


class TestInstallHelpers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_install()

    def test_parse_openclaw_version(self):
        m = self.mod
        self.assertEqual(m.parse_openclaw_version("openclaw 2026.2.6 extra"), (2026, 2, 6))
        self.assertEqual(m.parse_openclaw_version("v2026.12.99-rc1"), (2026, 12, 99))
        self.assertIsNone(m.parse_openclaw_version("no version here"))

    def test_apply_placeholders(self):
        m = self.mod
        root = Path("/tmp/fake/cursor-agent-team")
        s = m.apply_placeholders(
            "python {{CURSOR_AGENT_TEAM_EXTENSION_ROOT}}/_scripts/x.py", root
        )
        self.assertIn(str(root.resolve()), s)
        self.assertNotIn("{{", s)

    def test_merge_idempotent(self):
        m = self.mod
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "AGENTS.md"
            body = "LINE1\nLINE2"
            a1 = m.merge_block_into_file(
                p, body, m.AGENTS_START, m.AGENTS_END, dry_run=False
            )
            self.assertIn(a1, ("create", "replace_block", "append_block"))
            t1 = p.read_text(encoding="utf-8")
            self.assertIn(m.AGENTS_START, t1)
            self.assertIn("LINE1", t1)
            body2 = "NEW"
            m.merge_block_into_file(
                p, body2, m.AGENTS_START, m.AGENTS_END, dry_run=False
            )
            t2 = p.read_text(encoding="utf-8")
            self.assertIn("NEW", t2)
            self.assertNotIn("LINE1", t2)


if __name__ == "__main__":
    unittest.main()
