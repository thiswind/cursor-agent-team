#!/usr/bin/env python3
"""Shared utilities for cross-platform install scripts."""

import json
import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

COLORS = {
    "red": "\033[0;31m",
    "green": "\033[0;32m",
    "yellow": "\033[1;33m",
}
NC = "\033[0m"


def colored_print(msg, color="green"):
    """Print colored message. Falls back to plain text if color unsupported."""
    code = COLORS.get(color, "")
    if code:
        print(f"{code}{msg}{NC}")
    else:
        print(msg)


def ensure_dir(path):
    """Create directory (and parents) if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def copy_file(src, dst):
    """Copy a single file. Returns True on success, False on failure."""
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        return True
    except (FileNotFoundError, OSError) as e:
        colored_print(f"Error copying {src} -> {dst}: {e}", "red")
        return False


def copy_files(file_list, src_base, dst_base):
    """Batch copy files. file_list is [(src_rel, dst_rel), ...].
    Returns (success_list, fail_list)."""
    success, fail = [], []
    for src_rel, dst_rel in file_list:
        src = os.path.join(src_base, src_rel)
        dst = os.path.join(dst_base, dst_rel)
        if copy_file(src, dst):
            success.append(dst_rel)
            colored_print(f"  ✓ {dst_rel}", "green")
        else:
            fail.append(dst_rel)
            colored_print(f"  ✗ {dst_rel}", "red")
    return success, fail


def copy_dirs(dir_list, src_base, dst_base):
    """Batch copy directories. file_list is [(src_rel, dst_rel), ...].
    Returns (success_list, fail_list)."""
    success, fail = [], []
    for src_rel, dst_rel in dir_list:
        src = os.path.join(src_base, src_rel)
        dst = os.path.join(dst_base, dst_rel)
        try:
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            success.append(dst_rel)
            colored_print(f"  ✓ {dst_rel}", "green")
        except (FileNotFoundError, OSError) as e:
            fail.append(dst_rel)
            colored_print(f"  ✗ {dst_rel}: {e}", "red")
    return success, fail


def get_version(submodule_dir):
    """Get version from git tag or CHANGELOG.md."""
    version = "0.1.0"
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--exact-match", "HEAD"],
            cwd=submodule_dir, capture_output=True, text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        result = subprocess.run(
            ["git", "describe", "--tags", "HEAD"],
            cwd=submodule_dir, capture_output=True, text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except FileNotFoundError:
        pass

    changelog = os.path.join(submodule_dir, "CHANGELOG.md")
    if os.path.isfile(changelog):
        with open(changelog, encoding="utf-8") as f:
            for line in f:
                m = re.match(r"^## \[(.+?)\]", line)
                if m:
                    version = m.group(1)
                    break
    return version


def write_install_info(path, version, platform_name, files_list):
    """Write JSON installation record."""
    data = {
        "version": version,
        "installed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": "cursor-agent-team",
        "platform": platform_name,
        "files": files_list,
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def update_gitignore(project_root, pattern):
    """Add pattern to .gitignore if not already present."""
    gi_path = os.path.join(project_root, ".gitignore")
    existing = ""
    if os.path.isfile(gi_path):
        with open(gi_path, encoding="utf-8") as f:
            existing = f.read()

    lines = existing.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped == pattern or stripped == f"/{pattern}":
            colored_print(f"  Pattern '{pattern}' already in .gitignore", "yellow")
            return

    with open(gi_path, "a", encoding="utf-8") as f:
        if existing and not existing.endswith("\n"):
            f.write("\n")
        f.write(f"# Cursor AI Agent Team Framework (submodule)\n")
        f.write(f"{pattern}\n")
    colored_print(f"  ✓ Added '{pattern}' to .gitignore", "green")


def get_project_root(script_path):
    """Derive project root from install script path (parent of parent)."""
    return str(Path(script_path).resolve().parent.parent)


def get_submodule_dir(script_path):
    """Derive submodule directory from install script path (parent)."""
    return str(Path(script_path).resolve().parent)


def check_environment(project_root, submodule_dir):
    """Check that .git and submodule directory exist. Returns (ok, message)."""
    if not os.path.isdir(os.path.join(project_root, ".git")):
        return False, "Not in a git repository."
    if not os.path.isdir(submodule_dir):
        return False, f"Submodule not found at {submodule_dir}."
    return True, "Environment check passed."


def ensure_ai_workspace(submodule_dir):
    """
    Generate ai_workspace from config if ai_workspace_config.json exists.
    Shared by install.py, install_trae.py, install_qwen.py (ai_workspace is common).
    Returns (True, None) on success, (False, error_message) on failure, (None, None) if skipped (no config).
    """
    config_path = os.path.join(submodule_dir, "ai_workspace_config.json")
    if not os.path.isfile(config_path):
        return None, None
    try:
        import generate_ai_workspace as gen_ws
        gen_ws.run(submodule_dir, config_path=config_path)
        return True, None
    except Exception as e:
        return False, str(e)
