"""Tests for commit_workspace.py (FR-0008/0009/0010 closing helper)."""
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

SCRIPT = Path(__file__).parent.parent / "commit_workspace.py"


def make_host(tmp: Path, nested_ignore: bool = True) -> Path:
    """Scaffold a fake host: git repo + nested CAT dir with the production ignore rules."""
    host = tmp / "host"
    (host / "cursor-agent-team" / "ai_workspace" / "notes").mkdir(parents=True)
    subprocess.run(["git", "init", "-q"], cwd=str(host), check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=str(host), check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=str(host), check=True)
    if nested_ignore:
        (host / "cursor-agent-team" / ".gitignore").write_text("ai_workspace/**\n")
    note = host / "cursor-agent-team" / "ai_workspace" / "notes" / "note_x.md"
    note.write_text("# note\n")
    # baseline commit (gitignore tracked like production install)
    subprocess.run(["git", "add", "-A"], cwd=str(host), check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=str(host), check=True)
    return host


class TestCommitWorkspace(unittest.TestCase):

    def test_silent_ignore_trapped_and_fixed(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            host = make_host(Path(td))
            note_rel = "cursor-agent-team/ai_workspace/notes/note_x.md"
            # plain git add + commit would silently drop the note (dir-add exit 0)
            env = {**__import__("os").environ, "CAT_HOST_ROOT": str(host)}
            r = subprocess.run(
                [sys.executable, str(SCRIPT), note_rel, "-m", "closing"],
                cwd=str(host), capture_output=True, text=True, env=env)
            self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
            log = subprocess.run(["git", "log", "--name-only", "--oneline", "-1"],
                                 cwd=str(host), capture_output=True, text=True).stdout
            self.assertIn("note_x.md", log)

    def test_check_only_detects_untracked(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            host = make_host(Path(td))
            note_rel = "cursor-agent-team/ai_workspace/notes/note_x.md"
            env = {**__import__("os").environ, "CAT_HOST_ROOT": str(host)}
            r = subprocess.run(
                [sys.executable, str(SCRIPT), note_rel, "--check-only"],
                cwd=str(host), capture_output=True, text=True, env=env)
            self.assertEqual(r.returncode, 1, msg=r.stdout + r.stderr)
            self.assertIn("NOT tracked", r.stdout)

    def test_missing_path_fails_loudly(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            host = make_host(Path(td))
            r = subprocess.run(
                [sys.executable, str(SCRIPT), "cursor-agent-team/ai_workspace/notes/ghost.md", "-m", "x"],
                cwd=str(host), capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
            self.assertIn("does not exist", r.stdout)

    def test_non_git_host_exit_2(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            fake = Path(td) / "host"
            (fake / "cursor-agent-team" / "_scripts").mkdir(parents=True)
            env = {**__import__("os").environ, "CAT_HOST_ROOT": str(fake)}
            r = subprocess.run([sys.executable, str(SCRIPT), "some/path.md", "-m", "x"],
                               cwd=str(td), capture_output=True, text=True, env=env)
            self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
