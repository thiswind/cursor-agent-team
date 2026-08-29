import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WriterReleaseTests(unittest.TestCase):
    def test_command_and_skill_inventory(self):
        self.assertTrue((ROOT / "_cursor/commands/writer.md").is_file())
        self.assertTrue((ROOT / "_claude/commands/writer.md").is_file())
        self.assertTrue((ROOT / "_claude/rules/crew_assistant.md").is_file())
        self.assertTrue((ROOT / "_claude/rules/writer_assistant.md").is_file())
        self.assertTrue((ROOT / "VERSION").is_file())
        self.assertTrue((ROOT / "_trae_solo/skills/cursor-agent-team-writer/SKILL.md").is_file())
        self.assertTrue((ROOT / "_trae_solo/commands/writer.md").is_file())
        self.assertTrue((ROOT / "commands.yaml").is_file())
        cursor = (ROOT / "_cursor/commands/writer.md").read_text()
        claude = (ROOT / "_claude/commands/writer.md").read_text()
        trae = (ROOT / "_trae_solo/commands/writer.md").read_text()
        for term in ("Draft", "Review", "Final", "scratchpad", "Phase 2",
                     "verify_response.py", "Generated from commands.yaml"):
            self.assertIn(term, cursor)
            self.assertIn(term, claude)
            self.assertIn(term, trae)

    def test_untagged_version_uses_authoritative_metadata(self):
        import sys
        sys.path.insert(0, str(ROOT / "_scripts"))
        import _install_utils as utils

        self.assertEqual(utils.get_version(str(ROOT)), "v0.21.0")

    def test_installers_list_writer(self):
        self.assertIn("_cursor/commands/writer.md", (ROOT / "install.py").read_text())
        self.assertIn("_cursor/rules/writer_assistant.mdc", (ROOT / "install.py").read_text())
        self.assertIn("_claude/commands/writer.md", (ROOT / "install_claude_code.py").read_text())
        self.assertIn("_claude/rules/writer_assistant.md", (ROOT / "install_claude_code.py").read_text())
        self.assertIn("cursor-agent-team-writer", (ROOT / "install_trae_solo.py").read_text())

    def test_install_uninstall_fixtures_all_platforms(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "project"
            source = project / "cursor-agent-team"
            project.mkdir()
            (project / ".git").mkdir()
            shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns(".git", "ai_workspace", "__pycache__", ".pytest_cache"))
            (project / "unrelated.txt").write_text("keep")
            (project / "AGENTS.md").write_text("user-owned")
            writer_skill = project / ".trae/skills/cursor-agent-team-writer"
            writer_skill.mkdir(parents=True)
            (writer_skill / "user-content.md").write_text("preserve me")
            for platform, installer in (("cursor", "install.py"), ("claude_code", "install_claude_code.py"), ("trae_solo", "install_trae_solo.py")):
                subprocess.run([sys.executable, str(source / installer)], cwd=project, check=True, capture_output=True, text=True)
                record = project / {"cursor": ".cursor", "claude_code": ".claude", "trae_solo": ".trae"}[platform] / ".cursor-agent-team-installed"
                data = json.loads(record.read_text())
                self.assertTrue(any("writer" in item for item in data["files"]))
                subprocess.run([sys.executable, str(source / installer)], cwd=project, check=True, capture_output=True, text=True)
                subprocess.run([sys.executable, str(source / "uninstall.py"), "--platform", platform, "--yes"], cwd=project, check=True, capture_output=True, text=True)
                self.assertFalse(record.exists())
                self.assertTrue((project / "unrelated.txt").exists())
                self.assertEqual((writer_skill / "user-content.md").read_text(), "preserve me")
                self.assertEqual((project / "AGENTS.md").read_text(), "user-owned")

    def test_uninstall_rejects_symlinked_recorded_path(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "project"
            outside = Path(td) / "outside"
            project.mkdir()
            outside.mkdir()
            (project / ".git").mkdir()
            source = project / "cursor-agent-team"
            shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns(".git", "ai_workspace", "__pycache__", ".pytest_cache"))
            (outside / "victim.txt").write_text("keep")
            (project / ".cursor").mkdir()
            (project / ".cursor" / "link").symlink_to(outside, target_is_directory=True)
            record = project / ".cursor" / ".cursor-agent-team-installed"
            record.write_text(json.dumps({"files": [".cursor/link/victim.txt"]}))
            subprocess.run(
                [sys.executable, str(source / "uninstall.py"), "--platform", "cursor", "--yes"],
                cwd=project, check=True, capture_output=True, text=True,
            )
            self.assertTrue((outside / "victim.txt").exists())

    def test_trae_conflicts_and_reinstall_preserve_ownership(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "project"
            project.mkdir()
            (project / ".git").mkdir()
            source = project / "cursor-agent-team"
            shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns(".git", "ai_workspace", "__pycache__", ".pytest_cache"))
            conflict = project / ".trae/skills/cursor-agent-team-discuss/SKILL.md"
            conflict.parent.mkdir(parents=True)
            conflict.write_text("user-owned")
            unrelated = project / "unrelated.txt"
            unrelated.write_text("unrelated")
            subprocess.run([sys.executable, str(source / "install_trae_solo.py")], cwd=project, check=True, capture_output=True, text=True)
            writer_skill = project / ".trae/skills/cursor-agent-team-writer/SKILL.md"
            writer_rel = ".trae/skills/cursor-agent-team-writer/SKILL.md"
            record = project / ".trae/.cursor-agent-team-installed"
            first_record = json.loads(record.read_text())
            self.assertIn(writer_rel, first_record["files"])
            self.assertNotIn(".trae/skills/cursor-agent-team-discuss/SKILL.md", first_record["files"])
            user_extra = writer_skill.parent / "extra.md"
            user_extra.write_text("extra")
            obsolete = project / ".trae/skills/cursor-agent-team-writer/obsolete.md"
            first_record["files"].append(".trae/skills/cursor-agent-team-writer/obsolete.md")
            record.write_text(json.dumps(first_record))
            subprocess.run([sys.executable, str(source / "install_trae_solo.py")], cwd=project, check=True, capture_output=True, text=True)
            self.assertEqual(conflict.read_text(), "user-owned")
            second_record = json.loads(record.read_text())
            self.assertIn(writer_rel, second_record["files"])
            self.assertNotIn(".trae/skills/cursor-agent-team-writer/obsolete.md", second_record["files"])
            obsolete.write_text("created after the obsolete record")
            subprocess.run([sys.executable, str(source / "uninstall.py"), "--platform", "trae_solo", "--yes"], cwd=project, check=True, capture_output=True, text=True)
            self.assertFalse(writer_skill.exists())
            self.assertTrue(user_extra.exists())
            self.assertTrue(conflict.exists())
            self.assertTrue(obsolete.exists())
            self.assertTrue(unrelated.exists())

    def test_trae_install_rejects_destination_symlink(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "project"
            outside = Path(td) / "outside"
            project.mkdir()
            outside.mkdir()
            (project / ".git").mkdir()
            source = project / "cursor-agent-team"
            shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns(".git", "ai_workspace", "__pycache__", ".pytest_cache"))
            (project / ".trae/skills").mkdir(parents=True)
            (project / ".trae/skills/cursor-agent-team-writer").symlink_to(outside, target_is_directory=True)
            result = subprocess.run([sys.executable, str(source / "install_trae_solo.py")], cwd=project, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((outside / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
