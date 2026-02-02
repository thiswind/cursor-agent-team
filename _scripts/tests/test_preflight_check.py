#!/usr/bin/env python3
"""
Test suite for preflight_check.py

Uses TDD approach - these tests are written BEFORE the implementation.
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

# Get the project root directory (cursor-agent-team/)
PROJECT_ROOT = Path(__file__).parent.parent.parent
SCRIPT_PATH = PROJECT_ROOT / "_scripts" / "preflight_check.py"


def run_preflight_check():
    """Helper function to run preflight_check.py and capture output."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT)
    )
    return result.stdout, result.stderr, result.returncode


class TestPreflightCheckOutput:
    """Tests for preflight_check.py output format and content."""

    def test_output_includes_timestamp(self):
        """Output must include current time."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script failed with: {stderr}"
        
        # Check for time format pattern (e.g., "2026-02-02 23:20:00")
        assert "当前时间:" in stdout or "⏰" in stdout, \
            f"Output should include timestamp marker. Got: {stdout}"
        
        # Check for year pattern
        current_year = str(datetime.now().year)
        assert current_year in stdout, \
            f"Output should include current year {current_year}. Got: {stdout}"

    def test_output_includes_workspace_status(self):
        """Output must include workspace status section."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script failed with: {stderr}"
        
        # Check for workspace status markers
        assert "工作区状态" in stdout or "📋" in stdout, \
            f"Output should include workspace status section. Got: {stdout}"

    def test_output_includes_reminders(self):
        """Output must include operation reminders section."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script failed with: {stderr}"
        
        # Check for reminders section
        assert "操作约定" in stdout or "📌" in stdout, \
            f"Output should include reminders section. Got: {stdout}"
        
        # Check for key tool reminders
        assert "cleanup_ai_workspace.py" in stdout, \
            f"Output should mention cleanup script. Got: {stdout}"
        assert "create_card.py" in stdout, \
            f"Output should mention create_card script. Got: {stdout}"

    def test_output_under_20_lines(self):
        """Output must be concise, under 20 lines."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script failed with: {stderr}"
        
        lines = [line for line in stdout.strip().split('\n') if line.strip()]
        assert len(lines) <= 20, \
            f"Output should be under 20 lines, got {len(lines)} lines: {stdout}"

    def test_checks_discussion_topics(self):
        """Output must check for discussion_topics.md existence."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script failed with: {stderr}"
        
        # Should mention discussion_topics
        assert "discussion_topics" in stdout, \
            f"Output should check discussion_topics.md. Got: {stdout}"

    def test_counts_scatter_cards(self):
        """Output must count scatter cards."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script failed with: {stderr}"
        
        # Should mention cards with count
        assert "inspiration_capital" in stdout or "cards" in stdout, \
            f"Output should mention inspiration capital/cards. Got: {stdout}"

    def test_counts_notes(self):
        """Output must count notes."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script failed with: {stderr}"
        
        # Should mention notes
        assert "notes" in stdout, \
            f"Output should mention notes. Got: {stdout}"


class TestPreflightCheckExecution:
    """Tests for preflight_check.py execution behavior."""

    def test_script_exits_successfully(self):
        """Script should exit with code 0."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script should exit with code 0, got {code}. Stderr: {stderr}"

    def test_output_has_header_and_footer(self):
        """Output should have clear header and footer markers."""
        stdout, stderr, code = run_preflight_check()
        assert code == 0, f"Script failed with: {stderr}"
        
        # Check for boundary markers
        assert "Preflight Check" in stdout or "===" in stdout, \
            f"Output should have clear header. Got: {stdout}"
        assert "Ready" in stdout or "===" in stdout, \
            f"Output should have clear footer. Got: {stdout}"
