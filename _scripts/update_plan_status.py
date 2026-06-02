#!/usr/bin/env python3
"""
Update plan status and plan index bookkeeping.

This helper is intended for /crew wrap-up. It performs deterministic updates
that are easy to forget in a long shared-context workflow.

Usage:
    python update_plan_status.py PLAN-B-001 --status completed
    python update_plan_status.py B-001 --status completed --dry-run
    python update_plan_status.py PLAN-B-001 --status completed --session path/to/session --note "Verified"
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

VALID_STATES = {
    "pending", "in_progress", "completed", "paused", "closed", "active"
}

SCRIPT_DIR = Path(__file__).parent
WORKSPACE_ROOT = SCRIPT_DIR.parent / "ai_workspace"

TOPIC_UPDATE_HINT = "Review discussion_topics.md and update topic status if this plan completes the topic."

STATUS_PATTERNS = [
    re.compile(r"^(?P<prefix>\s*-\s*Status:\s*)(?P<value>\S+)(?P<suffix>.*)$", re.MULTILINE),
    re.compile(r"^(?P<prefix>\s*\*\*Status\*\*:\s*)(?P<value>\S+)(?P<suffix>.*)$", re.MULTILINE),
    re.compile(r"^(?P<prefix>\s*Status:\s*)(?P<value>\S+)(?P<suffix>.*)$", re.MULTILINE),
]

LAST_UPDATED_PATTERNS = [
    re.compile(r"^(?P<prefix>\s*-\s*Last Updated:\s*)(?P<value>.+)$", re.MULTILINE),
    re.compile(r"^(?P<prefix>\s*\*\*Last Updated\*\*:\s*)(?P<value>.+)$", re.MULTILINE),
    re.compile(r"^(?P<prefix>\s*Last Updated:\s*)(?P<value>.+)$", re.MULTILINE),
]


def normalize_plan_id(plan_id: str) -> str:
    """Normalize PLAN-B-001 and short B-001 forms."""
    plan_id = plan_id.strip().upper()
    if plan_id.startswith("PLAN-"):
        return plan_id
    return f"PLAN-{plan_id}"


def replace_first(patterns, content: str, replacement: str) -> tuple[str, bool]:
    """Replace the first matching metadata line."""
    for pattern in patterns:
        if pattern.search(content):
            return pattern.sub(replacement, content, count=1), True
    return content, False


def insert_metadata_after_title(content: str, status: str, timestamp: str) -> str:
    """Insert metadata after the first Markdown heading."""
    lines = content.splitlines()
    metadata = [f"- Status: {status}", f"- Last Updated: {timestamp}"]

    if lines and lines[0].startswith("#"):
        insert_at = 1
        if len(lines) > 1 and lines[1].strip() == "":
            insert_at = 2
        return "\n".join(lines[:insert_at] + metadata + [""] + lines[insert_at:]) + ("\n" if content.endswith("\n") else "")

    return "\n".join(metadata + ["", content])


def update_metadata(content: str, status: str, timestamp: str) -> str:
    """Update or insert Status and Last Updated metadata."""
    original = content

    content, has_status = replace_first(
        STATUS_PATTERNS,
        content,
        lambda match: f"{match.group('prefix')}{status}{match.group('suffix')}",
    )
    content, has_last_updated = replace_first(
        LAST_UPDATED_PATTERNS,
        content,
        lambda match: f"{match.group('prefix')}{timestamp}",
    )

    if has_status and has_last_updated:
        return content

    if not has_status and not has_last_updated:
        return insert_metadata_after_title(original, status, timestamp)

    lines = content.splitlines()
    insert_at = 1 if lines and lines[0].startswith("#") else 0
    if len(lines) > insert_at and lines[insert_at].strip() == "":
        insert_at += 1

    additions = []
    if not has_status:
        additions.append(f"- Status: {status}")
    if not has_last_updated:
        additions.append(f"- Last Updated: {timestamp}")

    return "\n".join(lines[:insert_at] + additions + lines[insert_at:]) + ("\n" if content.endswith("\n") else "")


def append_execution_record(content: str, status: str, timestamp: str, session: str | None, note: str | None) -> str:
    """Append an execution record unless the same session is already recorded."""
    if not session:
        return content

    if session in content:
        return content

    record = f"- {timestamp} — {status} — `{session}`"
    if note:
        record += f" — {note}"

    if "## Execution Records" not in content:
        separator = "" if content.endswith("\n") else "\n"
        return f"{content}{separator}\n## Execution Records\n\n{record}\n"

    pattern = re.compile(r"(^## Execution Records\s*$)", re.MULTILINE)
    match = pattern.search(content)
    if not match:
        return content

    insert_at = match.end()
    after = content[insert_at:]
    if after.startswith("\n\n"):
        insert_at += 2
    elif after.startswith("\n"):
        insert_at += 1
    else:
        record = "\n" + record

    return content[:insert_at] + record + "\n" + content[insert_at:]


def update_plan_content(content: str, status: str, timestamp: str, session: str | None, note: str | None) -> str:
    """Update plan metadata and optional execution record."""
    content = update_metadata(content, status, timestamp)
    return append_execution_record(content, status, timestamp, session, note)


def update_index_content(content: str, plan_id: str, status: str) -> tuple[str, bool]:
    """Update a Markdown table row in plans/INDEX.md."""
    lines = content.splitlines()
    changed = False
    for i, line in enumerate(lines):
        if plan_id not in line or "|" not in line:
            continue
        cells = line.split("|")
        # A normal five-column table has leading/trailing empty cells:
        # ['', plan, topic, summary, status, source, '']
        if len(cells) >= 6:
            cells[4] = f" {status} "
            lines[i] = "|".join(cells)
            changed = True
            break
    return "\n".join(lines) + ("\n" if content.endswith("\n") else ""), changed


def update_plan_status(plan_id: str, status: str, workspace: Path, session: str | None = None,
                       note: str | None = None, dry_run: bool = False) -> dict:
    """Update plan status and index. Returns JSON-serializable result."""
    normalized_plan_id = normalize_plan_id(plan_id)
    result = {
        "success": False,
        "plan_id": normalized_plan_id,
        "status": status,
        "updated": [],
        "warnings": [],
        "errors": [],
        "dry_run": dry_run,
    }

    if status not in VALID_STATES:
        result["errors"].append(
            f"Invalid status '{status}'. Valid statuses: {', '.join(sorted(VALID_STATES))}"
        )
        return result

    plans_dir = workspace / "plans"
    plan_path = plans_dir / f"{normalized_plan_id}.md"
    index_path = plans_dir / "INDEX.md"

    if not plan_path.exists():
        result["errors"].append(f"Plan file not found: {plan_path}")
        return result

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        plan_content = plan_path.read_text(encoding="utf-8")
    except Exception as exc:
        result["errors"].append(f"Cannot read plan file: {exc}")
        return result

    new_plan_content = update_plan_content(plan_content, status, timestamp, session, note)
    if new_plan_content != plan_content:
        result["updated"].append(str(plan_path))

    index_content = None
    new_index_content = None
    if index_path.exists():
        try:
            index_content = index_path.read_text(encoding="utf-8")
            new_index_content, index_changed = update_index_content(index_content, normalized_plan_id, status)
            if index_changed:
                result["updated"].append(str(index_path))
            else:
                result["warnings"].append("Plan not found in plans/INDEX.md; index was not updated")
        except Exception as exc:
            result["warnings"].append(f"Cannot update plans/INDEX.md: {exc}")
    else:
        result["warnings"].append("plans/INDEX.md not found; index was not updated")

    if not dry_run:
        try:
            if new_plan_content != plan_content:
                plan_path.write_text(new_plan_content, encoding="utf-8")
            if index_content is not None and new_index_content is not None and new_index_content != index_content:
                index_path.write_text(new_index_content, encoding="utf-8")
        except Exception as exc:
            result["success"] = False
            result["errors"].append(f"Write failed: {exc}")
            return result

    result["success"] = True
    result["topic_update_hint"] = TOPIC_UPDATE_HINT
    return result


def main():
    parser = argparse.ArgumentParser(description="Update cursor-agent-team plan status bookkeeping")
    parser.add_argument("plan_id", help="Plan ID, e.g. PLAN-B-001 or B-001")
    parser.add_argument("--status", required=True, choices=sorted(VALID_STATES), help="New plan status")
    parser.add_argument("--session", help="Optional crew session path to record")
    parser.add_argument("--note", help="Optional execution note")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    parser.add_argument("--json", action="store_true", help="Output JSON (default)")
    parser.add_argument("--workspace", help="Path to ai_workspace (default: cursor-agent-team/ai_workspace)")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve() if args.workspace else WORKSPACE_ROOT
    result = update_plan_status(
        args.plan_id,
        args.status,
        workspace,
        session=args.session,
        note=args.note,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
