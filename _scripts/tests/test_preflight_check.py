#!/usr/bin/env python3
"""
Test suite for preflight_check.py.

The preflight output is intentionally concise so role commands can read it
without adding unnecessary context noise.
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Get the project root directory (cursor-agent-team/)
PROJECT_ROOT = Path(__file__).parent.parent.parent
SCRIPT_PATH = PROJECT_ROOT / "_scripts" / "preflight_check.py"


def run_preflight_check():
    """Run preflight_check.py and capture output."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT)
    )
    return result.stdout, result.stderr, result.returncode


class TestPreflightCheckOutput:
    """Tests for the concise preflight output contract."""

    def test_output_includes_timestamp(self):
        """Output must include compact PREFLIGHT timestamp."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script failed with: {stderr}"

        assert stdout.startswith("PREFLIGHT "), \
            f"Output should start with PREFLIGHT marker. Got: {stdout}"

        current_year = str(datetime.now().year)
        assert current_year in stdout, \
            f"Output should include current year {current_year}. Got: {stdout}"

    def test_output_includes_workspace_status(self):
        """Output must include compact workspace status."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script failed with: {stderr}"

        assert "STATUS:" in stdout, \
            f"Output should include STATUS line. Got: {stdout}"
        assert "topics[" in stdout, \
            f"Output should include topics status. Got: {stdout}"
        assert "cards[" in stdout, \
            f"Output should include cards count. Got: {stdout}"
        assert "notes[" in stdout, \
            f"Output should include notes count. Got: {stdout}"

    def test_output_includes_script_reminders(self):
        """Output must include script reminders."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script failed with: {stderr}"

        assert "SCRIPTS:" in stdout, \
            f"Output should include SCRIPTS line. Got: {stdout}"
        assert "cleanup_ai_workspace.py" in stdout, \
            f"Output should mention cleanup script. Got: {stdout}"
        assert "create_card.py" in stdout, \
            f"Output should mention create_card script. Got: {stdout}"
        assert "draw_cards.py" in stdout, \
            f"Output should mention draw_cards script. Got: {stdout}"

    def test_output_includes_end_checklist(self):
        """Output must include end-of-command checklist reminder."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script failed with: {stderr}"

        assert "END_CHECKLIST:" in stdout, \
            f"Output should include END_CHECKLIST line. Got: {stdout}"
        assert "persona_output.py" in stdout, \
            f"Output should mention persona output script. Got: {stdout}"

    def test_output_includes_marker_contract(self):
        """Output must remind commands about phase markers."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script failed with: {stderr}"

        assert "OUTPUT_MARKERS:" in stdout, \
            f"Output should include OUTPUT_MARKERS line. Got: {stdout}"
        assert "[Phase N DONE]" in stdout, \
            f"Output should mention phase marker format. Got: {stdout}"

    def test_output_under_10_lines(self):
        """Output must stay concise."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script failed with: {stderr}"

        lines = [line for line in stdout.strip().split('\n') if line.strip()]
        assert len(lines) <= 10, \
            f"Output should be under 10 lines, got {len(lines)} lines: {stdout}"


class TestPreflightCheckExecution:
    """Tests for preflight_check.py execution behavior."""

    def test_script_exits_successfully(self):
        """Script should exit with code 0."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script should exit with code 0, got {code}. Stderr: {stderr}"

    def test_output_has_ready_footer(self):
        """Output should end with READY."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script failed with: {stderr}"

        assert stdout.strip().endswith("READY"), \
            f"Output should end with READY. Got: {stdout}"
