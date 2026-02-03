#!/usr/bin/env python3
"""
Topic Tree Validation and Update Script

This script provides two main functions:
1. validate: Validate topic tree updates against rules
2. update: One-step update with automatic backup, validation, and commit/rollback

Rule Description:
- R1: All historical topic IDs must be preserved (compare ID sets between old and new files)
- R2: Prohibit using "omit"/"..." to simplify history (keyword detection)
- R3: Must contain "Last Updated" field (field existence check)
- R4: Status values must be one of predefined values (enum validation, warning level)

Usage:
    # Validate mode (original behavior)
    python validate_topic_tree.py validate --old <old_file_path> --new <new_file_path>
    
    # Update mode (new one-step update)
    python validate_topic_tree.py update --content "new content..."
    python validate_topic_tree.py update --file /path/to/new_content.md
    cat new_content.md | python validate_topic_tree.py update --stdin
    
    # Update mode options
    python validate_topic_tree.py update --stdin --dry-run    # Preview only
    python validate_topic_tree.py update --stdin --force      # Skip validation (dangerous!)

Output Format (JSON):
    # Validate mode
    {
        "valid": true/false,
        "errors": ["error description 1", "error description 2"],
        "warnings": ["warning description 1"]
    }
    
    # Update mode (success)
    {
        "success": true,
        "message": "Topic tree updated successfully"
    }
    
    # Update mode (failure)
    {
        "success": false,
        "errors": ["R1 violation: ..."],
        "warnings": [],
        "hint": "Please ensure new content includes all historical topic IDs: A, B",
        "old_ids": ["A", "B"],
        "new_ids": ["B"],
        "missing_ids": ["A"]
    }

Exit Codes:
    0 - Success (validation passed or update completed)
    1 - Failure (validation failed or update failed)
"""

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Valid topic status values
VALID_STATES = {
    "in_progress", "completed", "closed", "pending", "paused", "active"
}

# Prohibited ellipsis markers
ELLIPSIS_PATTERNS = ["省略", "...", "…", "以上省略", "略", "omit", "omitted", "abbreviated"]

# Default paths (relative to script location)
SCRIPT_DIR = Path(__file__).parent
WORKSPACE_ROOT = SCRIPT_DIR.parent / "ai_workspace"
TOPIC_TREE_PATH = WORKSPACE_ROOT / "discussion_topics.md"
TEMP_DIR = WORKSPACE_ROOT / "temp"
BACKUP_PATH = TEMP_DIR / "discussion_topics.md.bak"
NEW_CONTENT_PATH = TEMP_DIR / "new_topic_tree.md"

# Auto-compress settings
ARCHIVE_COOLDOWN_DAYS = 3  # Archive completed topics after 3 days
ARCHIVE_DIR = WORKSPACE_ROOT / "topic_archives"


def extract_topic_ids(content: str) -> set:
    """
    Extract all topic IDs from topic tree
    
    Supports multiple formats:
    1. Table format: "| A |" or "| A.1 |"
    2. Bracket format: "[A]" or "[A.1]" or "### [A] topic name"
    
    ID format: 
    - Single letter: A, B, C
    - Letter with dot notation: A.1, A.1.1
    - Letter with dash: A-BC (legacy support)
    """
    ids = set()
    
    # Pattern 1: Table format - | ID |
    # Supports: A, A.1, A.1.1, A-BC
    table_pattern = r'\|\s*([A-Z](?:\.[0-9]+)*(?:-[A-Z]+)?)\s*\|'
    for match in re.finditer(table_pattern, content):
        topic_id = match.group(1)
        # Exclude table headers
        if topic_id not in {"ID", "TOPIC"}:
            ids.add(topic_id)
    
    # Pattern 2: Bracket format - [A] or [A.1] or [A-BC]
    bracket_pattern = r'\[([A-Z](?:\.[0-9]+)*(?:-[A-Z]+)?)\]'
    for match in re.finditer(bracket_pattern, content):
        topic_id = match.group(1)
        ids.add(topic_id)
    
    return ids


def check_r1_id_preservation(old_content: str, new_content: str) -> list:
    """
    R1: All historical topic IDs must be preserved
    
    Returns:
        list: Error messages (empty if passed)
    """
    old_ids = extract_topic_ids(old_content)
    new_ids = extract_topic_ids(new_content)
    
    missing_ids = old_ids - new_ids
    
    if missing_ids:
        return [f"R1 violation: The following topic IDs are missing: {sorted(missing_ids)}"]
    
    return []


def check_r2_no_ellipsis(content: str) -> list:
    """
    R2: Prohibit using "omit"/"..." markers to simplify history
    
    Returns:
        list: Error messages (empty if passed)
    """
    errors = []
    
    for pattern in ELLIPSIS_PATTERNS:
        if pattern in content:
            # Locate the position (line number)
            for i, line in enumerate(content.split("\n"), 1):
                if pattern in line:
                    errors.append(f"R2 violation: Found prohibited marker '{pattern}' at line {i}")
                    break
    
    return errors


def check_r3_last_updated(content: str) -> list:
    """
    R3: Must contain "Last Updated" field
    
    Returns:
        list: Error messages (empty if passed)
    """
    # Check for "Last Updated" in various formats
    patterns = [
        r"Last Updated",
        r"最后更新",
        r"\*\*Last Updated\*\*",
    ]
    
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return []
    
    return ["R3 violation: Missing 'Last Updated' field"]


def check_r4_valid_states(content: str) -> list:
    """
    R4: Status values must be one of predefined values (warning level)
    
    Returns:
        list: Warning messages (empty if passed)
    """
    warnings = []
    
    # Find status fields
    # Pattern: **状态**: value or **Status**: value
    pattern = r'\*\*(?:状态|Status)\*\*:\s*(.+?)(?:\n|$)'
    
    for match in re.finditer(pattern, content):
        state = match.group(1).strip()
        if state and state not in VALID_STATES:
            warnings.append(f"R4 warning: Unknown status value '{state}', valid values are: {VALID_STATES}")
    
    return warnings


def validate_content(old_content: str, new_content: str) -> dict:
    """
    Validate topic tree update using content strings directly
    
    Args:
        old_content: Old topic tree content
        new_content: New topic tree content
    
    Returns:
        dict: Validation result with valid, errors, warnings, and diagnostic info
    """
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "old_ids": [],
        "new_ids": [],
        "missing_ids": []
    }
    
    # Extract IDs for diagnostics
    old_ids = extract_topic_ids(old_content)
    new_ids = extract_topic_ids(new_content)
    missing_ids = old_ids - new_ids
    
    result["old_ids"] = sorted(list(old_ids))
    result["new_ids"] = sorted(list(new_ids))
    result["missing_ids"] = sorted(list(missing_ids))
    
    # R1: ID preservation check
    r1_errors = check_r1_id_preservation(old_content, new_content)
    result["errors"].extend(r1_errors)
    
    # R2: Ellipsis check
    r2_errors = check_r2_no_ellipsis(new_content)
    result["errors"].extend(r2_errors)
    
    # R3: Last Updated check
    r3_errors = check_r3_last_updated(new_content)
    result["errors"].extend(r3_errors)
    
    # R4: Status value check (warning level)
    r4_warnings = check_r4_valid_states(new_content)
    result["warnings"].extend(r4_warnings)
    
    # Determine overall validity
    result["valid"] = len(result["errors"]) == 0
    
    # Add hint if validation failed
    if not result["valid"] and result["missing_ids"]:
        result["hint"] = f"Please ensure new content includes all historical topic IDs: {', '.join(result['missing_ids'])}"
    
    return result


def validate_topic_tree(old_path: str, new_path: str) -> dict:
    """
    Validate topic tree update (file-based, original interface)
    
    Args:
        old_path: Path to old topic tree file
        new_path: Path to new topic tree file
    
    Returns:
        dict: Validation result with valid, errors, warnings fields
    """
    result = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Read files
    try:
        old_content = Path(old_path).read_text(encoding="utf-8")
    except Exception as e:
        result["valid"] = False
        result["errors"].append(f"Cannot read old file: {e}")
        return result
    
    try:
        new_content = Path(new_path).read_text(encoding="utf-8")
    except Exception as e:
        result["valid"] = False
        result["errors"].append(f"Cannot read new file: {e}")
        return result
    
    # Use validate_content for actual validation
    content_result = validate_content(old_content, new_content)
    
    # Copy results (keep original interface without diagnostic info)
    result["valid"] = content_result["valid"]
    result["errors"] = content_result["errors"]
    result["warnings"] = content_result["warnings"]
    
    return result


def update_topic_tree(new_content: str, dry_run: bool = False, force: bool = False) -> dict:
    """
    One-step topic tree update with automatic backup, validation, and commit/rollback
    
    This function:
    1. Backs up the current topic tree
    2. Validates the new content against the backup
    3. If valid (or force=True): commits the new content
    4. If invalid: returns detailed error info for AI to fix
    
    Args:
        new_content: New topic tree content to write
        dry_run: If True, only validate without writing
        force: If True, skip validation and write directly (dangerous!)
    
    Returns:
        dict: Result with success status and detailed info
    """
    result = {
        "success": False,
        "dry_run": dry_run
    }
    
    # Ensure temp directory exists
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Read current content
    try:
        if TOPIC_TREE_PATH.exists():
            old_content = TOPIC_TREE_PATH.read_text(encoding="utf-8")
        else:
            # First time use - no validation needed against old content
            old_content = ""
    except Exception as e:
        result["errors"] = [f"Cannot read current topic tree: {e}"]
        return result
    
    # Step 2: Backup current content
    try:
        if old_content:
            BACKUP_PATH.write_text(old_content, encoding="utf-8")
    except Exception as e:
        result["errors"] = [f"Cannot create backup: {e}"]
        return result
    
    # Step 3: Validate (unless force=True or first-time use)
    if not force and old_content:
        validation = validate_content(old_content, new_content)
        
        if not validation["valid"]:
            # Return detailed error info for AI to fix
            result["success"] = False
            result["errors"] = validation["errors"]
            result["warnings"] = validation["warnings"]
            result["old_ids"] = validation["old_ids"]
            result["new_ids"] = validation["new_ids"]
            result["missing_ids"] = validation["missing_ids"]
            if "hint" in validation:
                result["hint"] = validation["hint"]
            
            # Clean up temp files on failure
            _cleanup_temp_files()
            return result
        
        # Copy warnings even on success
        result["warnings"] = validation["warnings"]
    
    # Step 4: Commit (unless dry_run)
    if dry_run:
        result["success"] = True
        result["message"] = "Validation passed (dry-run mode, no actual write)"
        _cleanup_temp_files()
        return result
    
    try:
        # Write new content
        TOPIC_TREE_PATH.write_text(new_content, encoding="utf-8")
        result["success"] = True
        result["message"] = "Topic tree updated successfully"
        
        # Auto-compress after successful update (silent, won't break main flow)
        _auto_compress_if_needed()
        
        # Clean up temp files on success
        _cleanup_temp_files()
        
    except Exception as e:
        # Rollback on write failure
        result["success"] = False
        result["errors"] = [f"Write failed, attempting rollback: {e}"]
        
        try:
            if old_content and BACKUP_PATH.exists():
                TOPIC_TREE_PATH.write_text(old_content, encoding="utf-8")
                result["errors"].append("Rollback successful - original content restored")
        except Exception as rollback_e:
            result["errors"].append(f"Rollback also failed: {rollback_e}")
        
        _cleanup_temp_files()
    
    return result


def _cleanup_temp_files():
    """Clean up temporary files used during update"""
    try:
        if BACKUP_PATH.exists():
            BACKUP_PATH.unlink()
        if NEW_CONTENT_PATH.exists():
            NEW_CONTENT_PATH.unlink()
    except Exception:
        pass  # Ignore cleanup errors


# ============================================================
# Auto-Compress Feature
# ============================================================

def parse_topic_metadata(content: str, topic_id: str) -> dict:
    """
    Parse metadata from a topic block
    
    Args:
        content: Full topic tree content
        topic_id: ID of topic to parse (e.g., "A", "A.1")
    
    Returns:
        dict with keys: id, title, status, created, last_active, block
    """
    # Find the topic block
    escaped_id = re.escape(topic_id)
    pattern = rf'### \[{escaped_id}\] (.+?)(?=\n### \[|\n---|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return {"id": topic_id}
    
    block = match.group(0)
    title_match = re.search(rf'\[{escaped_id}\] ([^\n]+)', block)
    title = title_match.group(1).strip() if title_match else ""
    
    metadata = {
        "id": topic_id,
        "title": title,
        "block": block
    }
    
    # Parse metadata fields
    status_match = re.search(r'- Status: (\w+)', block)
    if status_match:
        metadata["status"] = status_match.group(1)
    
    created_match = re.search(r'- Created: ([\d\-: ]+)', block)
    if created_match:
        metadata["created"] = created_match.group(1).strip()
    
    last_active_match = re.search(r'- Last Active: ([\d\-: ]+)', block)
    if last_active_match:
        metadata["last_active"] = last_active_match.group(1).strip()
    
    return metadata


def should_archive_topic(metadata: dict) -> bool:
    """
    Check if topic meets archive conditions
    
    Conditions:
    - Status is 'completed'
    - Last active is older than ARCHIVE_COOLDOWN_DAYS
    """
    if metadata.get("status") != "completed":
        return False
    
    last_active = metadata.get("last_active", "")
    if not last_active:
        return False
    
    try:
        # Parse date (handle both "YYYY-MM-DD HH:MM" and "YYYY-MM-DD HH:MM:SS")
        last_active_dt = datetime.strptime(last_active[:16], "%Y-%m-%d %H:%M")
        cooldown_threshold = datetime.now() - timedelta(days=ARCHIVE_COOLDOWN_DAYS)
        return last_active_dt < cooldown_threshold
    except ValueError:
        return False


def compress_topic_to_index(metadata: dict) -> str:
    """
    Generate index table row for a topic
    
    Returns:
        str: Table row like "| A | Topic Name | completed | 2026-02-01 |"
    """
    last_active = metadata.get("last_active", "")[:10]  # Just date part
    return f"| {metadata['id']} | {metadata['title']} | {metadata['status']} | {last_active} |"


def generate_archive_content(topic_block: str, metadata: dict) -> str:
    """
    Generate archive file content
    
    Returns:
        str: Full markdown content for archive file
    """
    return f"""# Topic [{metadata['id']}] - {metadata['title']}

> Archived: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> Original Status: {metadata['status']}

{topic_block}
"""


def auto_compress_topic_tree(content: str, archive_dir: Path = None) -> tuple:
    """
    Auto-compress topic tree by archiving old completed topics
    
    This function:
    1. Identifies topics that should be archived
    2. Generates archive content for each
    3. Replaces full topic blocks with index rows
    4. Adds/updates Topic Index section
    
    Args:
        content: Current topic tree content
        archive_dir: Directory for archive files (default: ARCHIVE_DIR)
    
    Returns:
        tuple: (compressed_content, archives_dict)
            - compressed_content: New topic tree with archived topics as index rows
            - archives_dict: {topic_id: archive_file_content}
    """
    if archive_dir is None:
        archive_dir = ARCHIVE_DIR
    
    # Extract all topic IDs
    all_ids = extract_topic_ids(content)
    
    # Parse and check each topic
    topics_to_archive = []
    topics_to_keep = []
    
    for topic_id in sorted(all_ids):
        metadata = parse_topic_metadata(content, topic_id)
        # Only process topics that have a block (i.e., full detail in the file)
        if "block" in metadata and metadata.get("block"):
            if should_archive_topic(metadata):
                topics_to_archive.append(metadata)
            else:
                topics_to_keep.append(metadata)
    
    # If nothing to archive, return unchanged
    if not topics_to_archive:
        return content, {}
    
    # Generate archives
    archives = {}
    for metadata in topics_to_archive:
        archive_content = generate_archive_content(metadata.get("block", ""), metadata)
        archives[metadata["id"]] = archive_content
    
    # Build new content
    # 1. Keep header (everything before "## Topic Tree" or first topic)
    header_match = re.search(r'^(.*?)(## Topic Tree|## Active Topics|### \[)', content, re.DOTALL)
    if header_match:
        header = header_match.group(1)
    else:
        header = content.split("###")[0]
    
    # 2. Build Topic Index section
    index_lines = ["## Topic Index", "", "| ID | Title | Status | Last Active |", "|:---|:------|:-------|:------------|"]
    for metadata in topics_to_archive:
        index_lines.append(compress_topic_to_index(metadata))
    index_section = "\n".join(index_lines) + "\n\n"
    
    # 3. Build Active Topics section (keep full detail)
    active_section = "## Active Topics\n\n"
    for metadata in topics_to_keep:
        block = metadata.get("block", "")
        if block:
            active_section += block + "\n---\n\n"
    
    # 4. Combine
    compressed = header + index_section + active_section
    
    # Update Last Updated
    compressed = re.sub(
        r'(> Last Updated: )[\d\-: ]+',
        f'\\g<1>{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        compressed
    )
    
    return compressed, archives


def _auto_compress_if_needed():
    """
    Called after successful update to auto-compress old topics
    
    This is the hook into update_topic_tree(). It runs silently and
    won't break the main flow even if it fails.
    """
    try:
        content = TOPIC_TREE_PATH.read_text(encoding="utf-8")
        compressed, archives = auto_compress_topic_tree(content)
        
        if archives:
            # Write archive files
            month_dir = ARCHIVE_DIR / datetime.now().strftime("%Y-%m")
            month_dir.mkdir(parents=True, exist_ok=True)
            
            for topic_id, archive_content in archives.items():
                # Replace dots with dashes in filename (A.1 -> A-1)
                safe_id = topic_id.replace(".", "-")
                archive_path = month_dir / f"{safe_id}.md"
                archive_path.write_text(archive_content, encoding="utf-8")
            
            # Rewrite main file with compressed content
            TOPIC_TREE_PATH.write_text(compressed, encoding="utf-8")
    except Exception:
        pass  # Silent failure - don't break main flow


def main():
    """Main function with subcommands"""
    parser = argparse.ArgumentParser(
        description="Topic Tree Validation and Update Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Rules:
  R1: All historical topic IDs must be preserved (prevent topic loss)
  R2: Prohibit using "omit"/"..." markers to simplify history
  R3: Must contain "Last Updated" field
  R4: Status values must be one of predefined values (warning level)

Examples:
  # Validate mode
  python validate_topic_tree.py validate --old backup.md --new new_tree.md
  
  # Update mode
  python validate_topic_tree.py update --content "# Topic Tree\\n..."
  python validate_topic_tree.py update --file new_content.md
  cat new_content.md | python validate_topic_tree.py update --stdin
  python validate_topic_tree.py update --stdin --dry-run
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Validate subcommand
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate topic tree update (original behavior)"
    )
    validate_parser.add_argument(
        "--old",
        required=True,
        help="Path to old topic tree file (backup)"
    )
    validate_parser.add_argument(
        "--new",
        required=True,
        help="Path to new topic tree file (to be validated)"
    )
    
    # Update subcommand
    update_parser = subparsers.add_parser(
        "update",
        help="One-step update with automatic backup, validation, and commit/rollback"
    )
    content_group = update_parser.add_mutually_exclusive_group(required=True)
    content_group.add_argument(
        "--content",
        help="New topic tree content as string"
    )
    content_group.add_argument(
        "--file",
        help="Path to file containing new topic tree content"
    )
    content_group.add_argument(
        "--stdin",
        action="store_true",
        help="Read new content from stdin"
    )
    update_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview only, don't actually write"
    )
    update_parser.add_argument(
        "--force",
        action="store_true",
        help="Skip validation and write directly (dangerous!)"
    )
    
    args = parser.parse_args()
    
    # Handle no command (backward compatibility: treat as validate if --old and --new provided)
    if args.command is None:
        # Check if using old-style arguments
        if len(sys.argv) > 1 and sys.argv[1].startswith("--"):
            # Old-style usage: python validate_topic_tree.py --old X --new Y
            # Re-parse with validate subcommand
            sys.argv.insert(1, "validate")
            args = parser.parse_args()
        else:
            parser.print_help()
            sys.exit(1)
    
    if args.command == "validate":
        # Perform validation
        result = validate_topic_tree(args.old, args.new)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["valid"] else 1)
    
    elif args.command == "update":
        # Get new content
        if args.content:
            new_content = args.content
        elif args.file:
            try:
                new_content = Path(args.file).read_text(encoding="utf-8")
            except Exception as e:
                print(json.dumps({
                    "success": False,
                    "errors": [f"Cannot read file: {e}"]
                }, ensure_ascii=False, indent=2))
                sys.exit(1)
        elif args.stdin:
            new_content = sys.stdin.read()
        else:
            print(json.dumps({
                "success": False,
                "errors": ["No content provided"]
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
        
        # Perform update
        result = update_topic_tree(
            new_content,
            dry_run=args.dry_run,
            force=args.force
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
