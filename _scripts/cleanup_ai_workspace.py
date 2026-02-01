#!/usr/bin/env python3
"""
AI Workspace Safe Deletion Script - Restricted File Cleanup Tool

This script allows agents to safely delete files within the ai_workspace/ directory,
while ensuring no files outside the directory can be deleted.

Safety Mechanisms:
  - Hardcoded path: Can only operate on ../ai_workspace/ directory
  - Path validation: All target paths must resolve within ai_workspace/
  - Protected files: Certain critical files cannot be deleted (unless using --force)
  - Logging: All operations recorded to ai_workspace/temp/cleanup.log

Usage:
    python cleanup_ai_workspace.py [options]

Options:
    --file <path>       Delete specified file (relative to ai_workspace/)
    --dir <path>        Delete specified directory (recursive)
    --pattern <glob>    Delete by pattern (e.g., *.bak, *.tmp)
    --older-than <days> Delete files older than N days
    --dry-run           Preview mode, don't actually delete
    --quiet             Silent mode, no terminal output (still writes to log)
    --force             Force delete (including protected files, use with caution)
    --help              Show help information

Output Format (JSON):
    {
        "success": true/false,
        "deleted": ["file1.md", "temp/file2.txt"],
        "skipped": [],
        "protected": ["README.md"],
        "errors": [],
        "dry_run": false,
        "log_file": "ai_workspace/temp/cleanup.log"
    }

Exit Codes:
    0 - Success
    1 - Failure (parameter error, permission issues, etc.)
    2 - Partial failure (some files failed to delete)
"""

import argparse
import fnmatch
import json
import os
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Set


# Protected files (hardcoded, these files cannot be deleted by default)
PROTECTED_FILES: Set[str] = {
    "README.md",
    "crew/README.md",
    "plans/README.md",
    "plans/INDEX.md",
    "prompt_engineer/README.md",
    "discussion_topics.md",
}

# ai_workspace directory path relative to script location
WORKSPACE_DIR_RELATIVE = "../ai_workspace"


def get_workspace_dir() -> Path:
    """Get absolute path to ai_workspace directory"""
    script_dir = Path(__file__).parent.resolve()
    workspace_dir = (script_dir / WORKSPACE_DIR_RELATIVE).resolve()
    return workspace_dir


def get_log_file(workspace_dir: Path) -> Path:
    """Get log file path"""
    temp_dir = workspace_dir / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir / "cleanup.log"


def write_log(log_file: Path, message: str):
    """Write to log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    # Ensure directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)


def is_path_safe(target_path: Path, workspace_dir: Path) -> bool:
    """
    Check if target path is safe (within ai_workspace directory)
    
    Prevents path escape attacks (e.g., ../../../etc/passwd)
    """
    try:
        # Resolve to absolute path
        resolved_target = target_path.resolve()
        resolved_workspace = workspace_dir.resolve()
        
        # Check if target path is within workspace directory
        # Use is_relative_to (Python 3.9+) or manual check
        try:
            resolved_target.relative_to(resolved_workspace)
            return True
        except ValueError:
            return False
    except Exception:
        return False


def is_protected(relative_path: str, force: bool = False) -> bool:
    """
    Check if file is in protected list
    
    Args:
        relative_path: Path relative to ai_workspace
        force: Whether force mode (ignore protection)
    
    Returns:
        True if file is protected and not force mode
    """
    if force:
        return False
    
    # Normalize path separators
    normalized = relative_path.replace("\\", "/")
    return normalized in PROTECTED_FILES


def delete_file(
    file_path: Path,
    workspace_dir: Path,
    dry_run: bool,
    force: bool,
    log_file: Path
) -> dict:
    """
    Delete a single file
    
    Returns:
        dict: {"status": "deleted"|"protected"|"skipped"|"error", "path": str, "message": str}
    """
    try:
        relative_path = str(file_path.relative_to(workspace_dir))
    except ValueError:
        relative_path = str(file_path)
    
    # Check path safety
    if not is_path_safe(file_path, workspace_dir):
        write_log(log_file, f"REJECTED: {relative_path} (path escape attempt)")
        return {
            "status": "error",
            "path": relative_path,
            "message": "Path escape rejected: target not within ai_workspace/ directory"
        }
    
    # Check if file exists
    if not file_path.exists():
        write_log(log_file, f"SKIPPED: {relative_path} (not found)")
        return {
            "status": "skipped",
            "path": relative_path,
            "message": "File not found"
        }
    
    # Check if protected
    if is_protected(relative_path, force):
        write_log(log_file, f"PROTECTED: {relative_path}")
        return {
            "status": "protected",
            "path": relative_path,
            "message": "File is in protected list, use --force to delete"
        }
    
    # Execute deletion
    if dry_run:
        write_log(log_file, f"DRY-RUN: Would delete {relative_path}")
        return {
            "status": "deleted",
            "path": relative_path,
            "message": "Preview mode: would be deleted"
        }
    else:
        try:
            if file_path.is_dir():
                shutil.rmtree(file_path)
            else:
                file_path.unlink()
            write_log(log_file, f"DELETED: {relative_path}")
            return {
                "status": "deleted",
                "path": relative_path,
                "message": "Deleted"
            }
        except Exception as e:
            write_log(log_file, f"ERROR: Failed to delete {relative_path}: {e}")
            return {
                "status": "error",
                "path": relative_path,
                "message": f"Delete failed: {e}"
            }


def delete_directory(
    dir_path: Path,
    workspace_dir: Path,
    dry_run: bool,
    force: bool,
    log_file: Path
) -> List[dict]:
    """
    Recursively delete directory
    
    Returns:
        List[dict]: Deletion result for each file/directory
    """
    results = []
    
    try:
        relative_path = str(dir_path.relative_to(workspace_dir))
    except ValueError:
        relative_path = str(dir_path)
    
    # Check path safety
    if not is_path_safe(dir_path, workspace_dir):
        write_log(log_file, f"REJECTED: {relative_path} (path escape attempt)")
        return [{
            "status": "error",
            "path": relative_path,
            "message": "Path escape rejected: target not within ai_workspace/ directory"
        }]
    
    # Check if directory exists
    if not dir_path.exists():
        write_log(log_file, f"SKIPPED: {relative_path} (not found)")
        return [{
            "status": "skipped",
            "path": relative_path,
            "message": "Directory not found"
        }]
    
    if not dir_path.is_dir():
        # If it's a file, treat as file
        return [delete_file(dir_path, workspace_dir, dry_run, force, log_file)]
    
    # Collect all files in directory
    protected_found = []
    files_to_delete = []
    
    for item in dir_path.rglob("*"):
        if item.is_file():
            try:
                item_relative = str(item.relative_to(workspace_dir))
            except ValueError:
                item_relative = str(item)
            
            if is_protected(item_relative, force):
                protected_found.append(item_relative)
            else:
                files_to_delete.append(item)
    
    # If protected files found and not force mode, reject deleting entire directory
    if protected_found and not force:
        for p in protected_found:
            results.append({
                "status": "protected",
                "path": p,
                "message": "File is in protected list"
            })
        write_log(log_file, f"REJECTED: Cannot delete {relative_path} (contains protected files: {protected_found})")
        return results
    
    # Execute deletion
    if dry_run:
        write_log(log_file, f"DRY-RUN: Would delete directory {relative_path}")
        results.append({
            "status": "deleted",
            "path": relative_path,
            "message": "Preview mode: directory would be deleted"
        })
    else:
        try:
            shutil.rmtree(dir_path)
            write_log(log_file, f"DELETED: directory {relative_path}")
            results.append({
                "status": "deleted",
                "path": relative_path,
                "message": "Directory deleted"
            })
        except Exception as e:
            write_log(log_file, f"ERROR: Failed to delete directory {relative_path}: {e}")
            results.append({
                "status": "error",
                "path": relative_path,
                "message": f"Delete failed: {e}"
            })
    
    return results


def delete_by_pattern(
    pattern: str,
    workspace_dir: Path,
    dry_run: bool,
    force: bool,
    log_file: Path
) -> List[dict]:
    """
    Delete files by pattern
    
    Args:
        pattern: glob pattern (e.g., *.bak, temp/*.tmp)
    
    Returns:
        List[dict]: Deletion result for each file
    """
    results = []
    
    # Use glob to find matching files
    for item in workspace_dir.rglob(pattern):
        if item.is_file():
            result = delete_file(item, workspace_dir, dry_run, force, log_file)
            results.append(result)
    
    if not results:
        write_log(log_file, f"PATTERN: No files matched '{pattern}'")
    
    return results


def delete_older_than(
    days: int,
    workspace_dir: Path,
    dry_run: bool,
    force: bool,
    log_file: Path
) -> List[dict]:
    """
    Delete files older than N days
    
    Args:
        days: Day threshold
    
    Returns:
        List[dict]: Deletion result for each file
    """
    results = []
    cutoff_time = datetime.now() - timedelta(days=days)
    
    for item in workspace_dir.rglob("*"):
        if item.is_file():
            # Get file modification time
            mtime = datetime.fromtimestamp(item.stat().st_mtime)
            if mtime < cutoff_time:
                result = delete_file(item, workspace_dir, dry_run, force, log_file)
                results.append(result)
    
    if not results:
        write_log(log_file, f"OLDER-THAN: No files older than {days} days")
    
    return results


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="AI Workspace Safe Deletion Script - Restricted File Cleanup Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Safety Mechanisms:
  - Hardcoded path: Can only operate on ai_workspace/ directory
  - Path validation: Prevents path escape attacks (e.g., ../../../etc/passwd)
  - Protected files: README.md, discussion_topics.md, etc. cannot be deleted by default
  - Logging: All operations recorded to ai_workspace/temp/cleanup.log

Examples:
  python cleanup_ai_workspace.py --file temp/old_note.md
  python cleanup_ai_workspace.py --dir temp/test_cleanup
  python cleanup_ai_workspace.py --pattern "*.bak"
  python cleanup_ai_workspace.py --older-than 7
  python cleanup_ai_workspace.py --dry-run --pattern "*.tmp"
  python cleanup_ai_workspace.py --file README.md --force  # Dangerous!
        """
    )
    
    # Mutually exclusive deletion target parameters
    target_group = parser.add_mutually_exclusive_group()
    target_group.add_argument(
        "--file",
        type=str,
        help="Delete specified file (relative to ai_workspace/)"
    )
    target_group.add_argument(
        "--dir",
        type=str,
        help="Delete specified directory (recursive)"
    )
    target_group.add_argument(
        "--pattern",
        type=str,
        help="Delete by glob pattern (e.g., *.bak, temp/*.tmp)"
    )
    target_group.add_argument(
        "--older-than",
        type=int,
        metavar="DAYS",
        help="Delete files older than N days"
    )
    
    # Other options
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview mode, don't actually delete"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Silent mode, no terminal output (still writes to log)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force delete (including protected files, use with caution)"
    )
    
    args = parser.parse_args()
    
    # Check if deletion target specified
    if not any([args.file, args.dir, args.pattern, args.older_than]):
        parser.print_help()
        sys.exit(1)
    
    # Initialize
    workspace_dir = get_workspace_dir()
    log_file = get_log_file(workspace_dir)
    
    # Check if workspace directory exists
    if not workspace_dir.exists():
        result = {
            "success": False,
            "deleted": [],
            "skipped": [],
            "protected": [],
            "errors": ["ai_workspace/ directory does not exist"],
            "dry_run": args.dry_run,
            "log_file": str(log_file.relative_to(workspace_dir.parent))
        }
        if not args.quiet:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    # Execute deletion operation
    results = []
    
    if args.file:
        target_path = workspace_dir / args.file
        results.append(delete_file(target_path, workspace_dir, args.dry_run, args.force, log_file))
    
    elif args.dir:
        target_path = workspace_dir / args.dir
        results.extend(delete_directory(target_path, workspace_dir, args.dry_run, args.force, log_file))
    
    elif args.pattern:
        results.extend(delete_by_pattern(args.pattern, workspace_dir, args.dry_run, args.force, log_file))
    
    elif args.older_than:
        results.extend(delete_older_than(args.older_than, workspace_dir, args.dry_run, args.force, log_file))
    
    # Summarize results
    deleted = [r["path"] for r in results if r["status"] == "deleted"]
    skipped = [r["path"] for r in results if r["status"] == "skipped"]
    protected = [r["path"] for r in results if r["status"] == "protected"]
    errors = [f"{r['path']}: {r['message']}" for r in results if r["status"] == "error"]
    
    success = len(errors) == 0
    
    output = {
        "success": success,
        "deleted": deleted,
        "skipped": skipped,
        "protected": protected,
        "errors": errors,
        "dry_run": args.dry_run,
        "log_file": str(log_file.relative_to(workspace_dir.parent))
    }
    
    # Output result
    if not args.quiet:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    
    # Return exit code
    if not success:
        if deleted:
            sys.exit(2)  # Partial failure
        else:
            sys.exit(1)  # Complete failure
    sys.exit(0)


if __name__ == "__main__":
    main()
