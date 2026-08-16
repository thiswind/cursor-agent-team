"""Tests for build_commands.py — single-source generation and drift check."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_scripts"))

import build_commands as bc  # noqa: E402


class TestSourceIntegrity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import yaml
        with open(bc.SOURCE_PATH, "r", encoding="utf-8") as f:
            cls.commands = yaml.safe_load(f)["commands"]

    def test_five_commands_defined(self):
        self.assertEqual(
            set(self.commands.keys()),
            {"discuss", "crew", "prompt_engineer", "spec_translator", "writer"},
        )

    def test_phase_lists_consistent_with_declared_phases(self):
        for name, cmd in self.commands.items():
            ns = [p["n"] for p in cmd["phase_list"]]
            self.assertEqual(ns, list(range(cmd["phases"])),
                             f"{name}: phase_list {ns} != 0..{cmd['phases']-1}")

    def test_platforms_are_known(self):
        for name, cmd in self.commands.items():
            for p in cmd["platforms"]:
                self.assertIn(p, {"cursor", "claude", "trae"}, f"{name}: unknown platform {p}")

    def test_trae_platforms_have_skills(self):
        for name, cmd in self.commands.items():
            if "trae" in cmd["platforms"]:
                self.assertIsNotNone(cmd.get("skill"), f"{name}: trae platform requires skill")

    def test_every_command_has_history_and_usage(self):
        for name, cmd in self.commands.items():
            self.assertTrue(cmd["history"], f"{name}: empty history")
            self.assertTrue(cmd["usage"], f"{name}: empty usage")
            self.assertTrue(cmd["hard_constraints"], f"{name}: empty hard_constraints")


class TestGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out_dir = cls.tmp.name
        cls.targets = dict(bc.all_targets(
            __import__("yaml").safe_load(open(bc.SOURCE_PATH))["commands"]))
        for rel, content in cls.targets.items():
            path = os.path.join(cls.out_dir, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_expected_artifact_matrix(self):
        # 5 cursor + 5 claude + 4 trae commands + 4 trae skills = 18
        self.assertEqual(len(self.targets), 18)
        self.assertIn("_cursor/commands/spec_translator.md", self.targets)
        self.assertIn("_claude/commands/spec_translator.md", self.targets)
        self.assertNotIn("_trae_solo/commands/spec_translator.md", self.targets)
        self.assertNotIn("_trae_solo/skills/cursor-agent-team-spec-translator/SKILL.md", self.targets)

    def test_all_artifacts_carry_generated_header(self):
        for rel, content in self.targets.items():
            self.assertIn("Generated from commands.yaml", content, f"{rel} missing header")

    def test_all_artifacts_embed_verification_step(self):
        for rel, content in self.targets.items():
            self.assertIn("verify_response.py", content, f"{rel} missing verification step")

    def test_all_artifacts_embed_marker_contract(self):
        for rel, content in self.targets.items():
            self.assertIn("phase_marker.py", content, f"{rel} missing marker contract")

    def test_cursor_and_trae_use_python_not_python3(self):
        for rel, content in self.targets.items():
            if rel.startswith(("_cursor/", "_trae_solo/")):
                self.assertNotIn("python3 ", content, f"{rel} should use `python`")
                self.assertIn("python ", content)

    def test_claude_uses_python3_and_arguments(self):
        for rel, content in self.targets.items():
            if rel.startswith("_claude/commands/"):
                self.assertIn("$ARGUMENTS", content)
                self.assertIn("python3 cursor-agent-team/_scripts/phase_marker.py 0 true", content)

    def test_claude_each_phase_has_end_marker_call(self):
        discuss = self.targets["_claude/commands/discuss.md"]
        for n in range(4):
            self.assertIn(f"phase_marker.py {n} true", discuss)

    def test_marker_counts_match_phase_counts(self):
        cases = {"discuss": 4, "crew": 4, "prompt_engineer": 5, "spec_translator": 5, "writer": 4}
        for name, n in cases.items():
            content = self.targets[f"_cursor/commands/{name}.md"]
            self.assertIn(f"must contain all {n} markers", content)

    def test_trae_frontmatter_present(self):
        for rel, content in self.targets.items():
            if rel.startswith("_trae_solo/commands/"):
                self.assertTrue(content.startswith("---\nname: "), f"{rel} missing frontmatter")


if __name__ == "__main__":
    unittest.main()
