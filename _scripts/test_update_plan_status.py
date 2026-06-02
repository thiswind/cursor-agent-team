#!/usr/bin/env python3
"""
Tests for update_plan_status.py.

Run with:
    python -m pytest test_update_plan_status.py -v
    python test_update_plan_status.py
"""

import tempfile
from pathlib import Path

import pytest

from update_plan_status import normalize_plan_id, update_plan_status


INDEX_CONTENT = """# Plans Index

| Plan | Topic | Summary | Status | Source |
|:-----|:------|:--------|:-------|:-------|
| [PLAN-B-001](PLAN-B-001.md) | [B] Test | Test plan | pending | /discuss |
"""


def make_workspace(plan_content: str, index_content: str | None = INDEX_CONTENT):
    tmp = tempfile.TemporaryDirectory()
    workspace = Path(tmp.name) / "ai_workspace"
    plans = workspace / "plans"
    plans.mkdir(parents=True)
    (plans / "PLAN-B-001.md").write_text(plan_content, encoding="utf-8")
    if index_content is not None:
        (plans / "INDEX.md").write_text(index_content, encoding="utf-8")
    return tmp, workspace


class TestPlanIdNormalization:
    def test_normalize_short_plan_id(self):
        assert normalize_plan_id("B-001") == "PLAN-B-001"

    def test_normalize_full_plan_id(self):
        assert normalize_plan_id("PLAN-B-001") == "PLAN-B-001"


class TestUpdatePlanStatus:
    def test_updates_plan_status_and_index(self):
        tmp, workspace = make_workspace("""# PLAN-B-001: Test Plan

- Status: pending
- Last Updated: 2026-01-01 10:00
""")
        with tmp:
            result = update_plan_status("PLAN-B-001", "completed", workspace)
            plan = (workspace / "plans" / "PLAN-B-001.md").read_text(encoding="utf-8")
            index = (workspace / "plans" / "INDEX.md").read_text(encoding="utf-8")

        assert result["success"] is True
        assert "- Status: completed" in plan
        assert "- Last Updated: 2026-01-01 10:00" not in plan
        assert "| [PLAN-B-001](PLAN-B-001.md) | [B] Test | Test plan | completed | /discuss |" in index

    def test_inserts_missing_metadata(self):
        tmp, workspace = make_workspace("""# PLAN-B-001: Test Plan

Some description.
""")
        with tmp:
            result = update_plan_status("B-001", "completed", workspace)
            plan = (workspace / "plans" / "PLAN-B-001.md").read_text(encoding="utf-8")

        assert result["success"] is True
        assert "- Status: completed" in plan
        assert "- Last Updated:" in plan
        assert "Some description." in plan

    def test_appends_session_record(self):
        tmp, workspace = make_workspace("""# PLAN-B-001: Test Plan

- Status: pending
""")
        session = "cursor-agent-team/ai_workspace/crew/sessions/session_20260602_103000"
        with tmp:
            result = update_plan_status(
                "PLAN-B-001",
                "completed",
                workspace,
                session=session,
                note="Implemented and verified",
            )
            plan = (workspace / "plans" / "PLAN-B-001.md").read_text(encoding="utf-8")

        assert result["success"] is True
        assert "## Execution Records" in plan
        assert session in plan
        assert "Implemented and verified" in plan

    def test_does_not_duplicate_session_record(self):
        session = "cursor-agent-team/ai_workspace/crew/sessions/session_20260602_103000"
        tmp, workspace = make_workspace(f"""# PLAN-B-001: Test Plan

- Status: pending

## Execution Records

- 2026-06-02 10:30 — completed — `{session}`
""")
        with tmp:
            result = update_plan_status("PLAN-B-001", "completed", workspace, session=session)
            plan = (workspace / "plans" / "PLAN-B-001.md").read_text(encoding="utf-8")

        assert result["success"] is True
        assert plan.count(session) == 1

    def test_missing_index_row_warns_but_succeeds(self):
        tmp, workspace = make_workspace(
            """# PLAN-B-001: Test Plan

- Status: pending
""",
            index_content="# Plans Index\n\n| Plan | Topic | Summary | Status | Source |\n|:-----|:------|:--------|:-------|:-------|\n",
        )
        with tmp:
            result = update_plan_status("PLAN-B-001", "completed", workspace)
            plan = (workspace / "plans" / "PLAN-B-001.md").read_text(encoding="utf-8")

        assert result["success"] is True
        assert "- Status: completed" in plan
        assert any("Plan not found in plans/INDEX.md" in warning for warning in result["warnings"])

    def test_missing_plan_file_fails(self):
        tmp = tempfile.TemporaryDirectory()
        workspace = Path(tmp.name) / "ai_workspace"
        (workspace / "plans").mkdir(parents=True)
        with tmp:
            result = update_plan_status("PLAN-B-001", "completed", workspace)

        assert result["success"] is False
        assert any("Plan file not found" in error for error in result["errors"])

    def test_invalid_status_fails(self):
        tmp, workspace = make_workspace("""# PLAN-B-001: Test Plan

- Status: pending
""")
        with tmp:
            result = update_plan_status("PLAN-B-001", "done", workspace)

        assert result["success"] is False
        assert any("Invalid status" in error for error in result["errors"])

    def test_dry_run_does_not_write_files(self):
        plan_content = """# PLAN-B-001: Test Plan

- Status: pending
- Last Updated: 2026-01-01 10:00
"""
        tmp, workspace = make_workspace(plan_content)
        with tmp:
            result = update_plan_status("PLAN-B-001", "completed", workspace, dry_run=True)
            plan = (workspace / "plans" / "PLAN-B-001.md").read_text(encoding="utf-8")
            index = (workspace / "plans" / "INDEX.md").read_text(encoding="utf-8")

        assert result["success"] is True
        assert result["dry_run"] is True
        assert plan == plan_content
        assert index == INDEX_CONTENT
        assert result["updated"]


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
