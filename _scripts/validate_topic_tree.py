#!/usr/bin/env python3
"""
Topic Tree Validation Script - Hard Constraint Checking
Validates whether LLM-generated topic tree updates comply with rules

Rule Description:
- R1: All historical topic IDs must be preserved (compare ID sets between old and new files)
- R2: Prohibit using "omit"/"..." to simplify history (keyword detection)
- R3: Must contain "Last Updated" field (field existence check)
- R4: Status values must be one of predefined values (enum validation, warning level)

Usage:
    python validate_topic_tree.py --old <old_file_path> --new <new_file_path>

Output Format (JSON):
    {
        "valid": true/false,
        "errors": ["error description 1", "error description 2"],
        "warnings": ["warning description 1"]
    }

Exit Codes:
    0 - Validation passed (valid=true)
    1 - Validation failed (valid=false)
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Valid topic status values
VALID_STATES = {
    "进行中", "已完成", "已关闭", "待讨论", "暂停",
    "✅ 已关闭", "✅ 已完成", "🔄 进行中", "⏸️ 暂停"
}

# Prohibited ellipsis markers
ELLIPSIS_PATTERNS = ["省略", "...", "…", "以上省略", "略", "omit", "omitted", "abbreviated"]


def extract_topic_ids(content: str) -> set:
    """
    Extract all topic IDs from topic tree
    
    Match ID column in tables, e.g., "| A |" or "| C-AB |" or "| AE |"
    ID format: One or more uppercase letters, optionally followed by "-" and more uppercase letters
    """
    # Match ID column in tables
    # Pattern: | ID | (ID is one or more uppercase letters, optionally with - and more letters)
    pattern = r'\|\s*([A-Z]+(?:-[A-Z]+)?)\s*\|'
    
    ids = set()
    for match in re.finditer(pattern, content):
        topic_id = match.group(1)
        # Exclude table headers (like "ID")
        if topic_id not in {"ID", "话题ID", "TOPIC"}:
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


def validate_topic_tree(old_path: str, new_path: str) -> dict:
    """
    Validate topic tree update
    
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
    
    return result


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Topic Tree Validation Script - Hard Constraint Checking",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Rules:
  R1: All historical topic IDs must be preserved (prevent topic loss)
  R2: Prohibit using "omit"/"..." markers to simplify history
  R3: Must contain "Last Updated" field
  R4: Status values must be one of predefined values (warning level)

Examples:
  python validate_topic_tree.py --old backup.md --new new_tree.md
        """
    )
    
    parser.add_argument(
        "--old",
        required=True,
        help="Path to old topic tree file (backup)"
    )
    parser.add_argument(
        "--new",
        required=True,
        help="Path to new topic tree file (to be validated)"
    )
    
    args = parser.parse_args()
    
    # Perform validation
    result = validate_topic_tree(args.old, args.new)
    
    # Output result
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # Return exit code
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
