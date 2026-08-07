#!/usr/bin/env python3
"""uninstall.py - Uninstall Cursor AI Agent Team Framework.

Usage:
  python cursor-agent-team/uninstall.py [--platform cursor|claude_code|trae_solo] [--yes] [--remove-submodule]
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

_scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_scripts")
sys.path.insert(0, _scripts_dir)
import _install_utils as u  # type: ignore


SUBMODULE_NAME = "cursor-agent-team"
PLATFORM_INSTALL_INFO = {
    "cursor": os.path.join(".cursor", ".cursor-agent-team-installed"),
    "claude_code": os.path.join(".claude", ".cursor-agent-team-installed"),
    "trae_solo": os.path.join(".trae", ".cursor-agent-team-installed"),
}
PLATFORM_DIRS = {
    "cursor": [
        (os.path.join(".cursor", "commands"), ".cursor/commands/"),
        (os.path.join(".cursor", "rules"), ".cursor/rules/"),
        (".cursor", ".cursor/"),
    ],
    "claude_code": [
        (os.path.join(".claude", "commands"), ".claude/commands/"),
        (os.path.join(".claude", "rules"), ".claude/rules/"),
        (".claude", ".claude/"),
    ],
    "trae_solo": [
        (os.path.join(".trae", "skills"), ".trae/skills/"),
        (".trae", ".trae/"),
    ],
}
PLATFORM_LABELS = {
    "cursor": "Cursor",
    "claude_code": "Claude Code",
    "trae_solo": "TRAE SOLO",
}


def _is_dir_empty(path: str) -> bool:
    try:
        return not any(os.scandir(path))
    except FileNotFoundError:
        return True


def _remove_path(abs_path: str) -> bool:
    if not os.path.lexists(abs_path):
        return False
    try:
        if os.path.islink(abs_path) or os.path.isfile(abs_path):
            os.remove(abs_path)
            return True
        if os.path.isdir(abs_path):
            shutil.rmtree(abs_path)
            return True
        os.remove(abs_path)
        return True
    except OSError as e:
        u.colored_print(f"Error removing {abs_path}: {e}", "red")
        return False


def _try_rmdir_if_empty(abs_dir: str, removed_items: list[str], rel_label: str) -> None:
    if os.path.isdir(abs_dir) and _is_dir_empty(abs_dir):
        try:
            os.rmdir(abs_dir)
            removed_items.append(rel_label)
        except OSError:
            pass


def _run_git(project_root: str, args: list[str]) -> tuple[bool, str]:
    try:
        p = subprocess.run(
            ["git", *args],
            cwd=project_root,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return False, "git not found"
    out = (p.stdout or "").strip()
    err = (p.stderr or "").strip()
    if p.returncode != 0:
        return False, (err or out or f"git {' '.join(args)} failed")
    return True, (out or "ok")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yes", action="store_true", help="Skip confirmation prompt")
    ap.add_argument(
        "--platform",
        choices=sorted(PLATFORM_INSTALL_INFO),
        default="cursor",
        help="Platform installation to remove (default: cursor)",
    )
    ap.add_argument(
        "--remove-submodule",
        action="store_true",
        help="Explicitly remove the git submodule (default: keep it)",
    )
    args = ap.parse_args()

    script_path = os.path.abspath(__file__)
    project_root = u.get_project_root(script_path)
    install_info_rel = PLATFORM_INSTALL_INFO[args.platform]
    platform_label = PLATFORM_LABELS[args.platform]

    install_info_path = os.path.join(project_root, install_info_rel)

    print("=" * 42)
    print(f"Cursor AI Agent Team Framework Uninstaller ({platform_label})")
    print("=" * 42)
    print()

    if not os.path.isfile(install_info_path):
        u.colored_print("Framework not installed or installation info missing.", "yellow")
        print("Nothing to uninstall.")
        return 0

    try:
        with open(install_info_path, encoding="utf-8") as f:
            info = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        u.colored_print(f"Error reading install record: {e}", "red")
        return 1

    version = str(info.get("version", "unknown"))
    installed_at = str(info.get("installed_at", "unknown"))
    files = info.get("files", [])
    if not isinstance(files, list):
        files = []

    print("Found installation:")
    print(f"  Version: {version}")
    print(f"  Installed at: {installed_at}")
    print()

    print(f"This will remove installed {platform_label} files recorded by the installer.")
    if args.remove_submodule:
        print("It will also attempt to remove the git submodule cursor-agent-team/.")
    else:
        print("It will NOT remove the git submodule unless you pass --remove-submodule.")
    print()

    if not args.yes:
        reply = input("Are you sure you want to uninstall? (y/n) ").strip().lower()
        if reply not in {"y", "yes"}:
            print("Uninstallation cancelled.")
            return 0

    removed: list[str] = []

    # Remove installed files recorded by installer
    for rel in files:
        if not isinstance(rel, str) or not rel:
            continue
        abs_path = os.path.abspath(os.path.join(project_root, rel))
        resolved_path = os.path.realpath(abs_path)
        if os.path.commonpath([os.path.realpath(project_root), resolved_path]) != os.path.realpath(project_root):
            u.colored_print(f"Warning: ignoring unsafe recorded path {rel}", "yellow")
            continue
        if _remove_path(abs_path):
            removed.append(rel)

    # Always remove install record itself (not included in files list)
    if _remove_path(install_info_path):
        removed.append(install_info_rel)

    # Cleanup empty dirs (best-effort)
    for rel_dir, label in PLATFORM_DIRS[args.platform]:
        _try_rmdir_if_empty(os.path.join(project_root, rel_dir), removed, label)

    # Optional: remove submodule explicitly
    if args.remove_submodule:
        submodule_dir = os.path.join(project_root, SUBMODULE_NAME)
        had_dir = os.path.isdir(submodule_dir)
        ok, msg = _run_git(project_root, ["submodule", "deinit", "-f", SUBMODULE_NAME])
        if ok:
            removed.append("Submodule deinitialized")
        else:
            u.colored_print(f"Warning: {msg}", "yellow")

        ok, msg = _run_git(project_root, ["rm", "-f", SUBMODULE_NAME])
        if ok:
            removed.append("Submodule removed from Git index")
            if had_dir:
                removed.append(f"Submodule directory ({SUBMODULE_NAME}/)")
        else:
            u.colored_print(f"Warning: {msg}", "yellow")

        git_modules = os.path.join(project_root, ".git", "modules", SUBMODULE_NAME)
        if os.path.isdir(git_modules):
            if _remove_path(git_modules):
                removed.append("Git internal module configuration")

        if os.path.isdir(submodule_dir):
            if _remove_path(submodule_dir):
                removed.append(f"Submodule directory ({SUBMODULE_NAME}/)")

    print()
    print("=" * 42)
    u.colored_print("Uninstallation completed!", "green")
    print("=" * 42)
    print()
    print("Removed items:")
    if removed:
        for item in removed:
            print(f"  ✅ {item}")
    else:
        print("  (none)")
    print()

    if args.remove_submodule:
        print("Note: If the submodule was removed, don't forget to commit the changes in your project repo.")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

