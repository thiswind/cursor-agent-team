#!/usr/bin/env python3
"""install_claude_code.py - Install Cursor AI Agent Team Framework for Claude Code.

Usage:
    python3 cursor-agent-team/install_claude_code.py

Prerequisites:
    git submodule add https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
"""

import os
import sys

_scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_scripts")
sys.path.insert(0, _scripts_dir)
import _install_utils as u

SUBMODULE_NAME = "cursor-agent-team"

COMMAND_FILES = [
    ("_claude/commands/discuss.md", ".claude/commands/discuss.md"),
    ("_claude/commands/prompt_engineer.md", ".claude/commands/prompt_engineer.md"),
    ("_claude/commands/crew.md", ".claude/commands/crew.md"),
    ("_claude/commands/spec_translator.md", ".claude/commands/spec_translator.md"),
]


def main():
    script_path = os.path.abspath(__file__)
    submodule_dir = u.get_submodule_dir(script_path)
    project_root = u.get_project_root(script_path)

    print("=" * 42)
    print("Cursor AI Agent Team Framework Installer (Claude Code)")
    print("=" * 42)
    print()

    print("Step 1: Checking environment...")
    ok, msg = u.check_environment(project_root, submodule_dir)
    if not ok:
        u.colored_print(f"Error: {msg}", "red")
        sys.exit(1)
    u.colored_print(f"✓ {msg}", "green")
    print()

    print("Step 2: Creating directory structure...")
    u.ensure_dir(os.path.join(project_root, ".claude", "commands"))
    u.ensure_dir(os.path.join(submodule_dir, "config"))
    u.colored_print("✓ Directories created", "green")
    print()

    print("Step 2b: Generating ai_workspace from config...")
    ok, err = u.ensure_ai_workspace(submodule_dir)
    if ok is True:
        u.colored_print("✓ ai_workspace generated", "green")
    elif ok is False:
        u.colored_print(f"Warning: ai_workspace generation failed: {err}", "yellow")
        print("  (Install continues; you may need to run generate_ai_workspace.py manually.)")
    else:
        u.colored_print("Step 2b: Skipped (no ai_workspace_config.json)", "yellow")
    print()

    print("Step 3: Copying Claude Code commands...")
    installed, failed = u.copy_files(COMMAND_FILES, submodule_dir, project_root)
    if failed:
        u.colored_print(f"Error: {len(failed)} file(s) failed to copy", "red")
        sys.exit(1)
    u.colored_print("✓ Commands copied", "green")
    print()

    print("Step 4: Recording installation information...")
    version = u.get_version(submodule_dir)
    info_path = os.path.join(project_root, ".claude", ".cursor-agent-team-installed")
    u.write_install_info(info_path, version, "claude_code", installed)
    u.colored_print("✓ Installation information recorded", "green")
    print()

    print("Step 5: Updating .gitignore...")
    u.update_gitignore(project_root, SUBMODULE_NAME)
    print()

    print("=" * 42)
    u.colored_print("Installation completed successfully!", "green")
    print("=" * 42)
    print()
    print("Installed items:")
    for item in installed:
        print(f"  ✅ {item}")
    print()
    print(f"Version: {version}")
    print()
    print("You can now use the following mask commands in Claude Code:")
    print("  /discuss - Discussion partner")
    print("  /prompt_engineer - Prompt engineer")
    print("  /crew - Crew member")
    print("  /spec_translator - Spec-Kit translator")
    print()
    print("Claude Code adaptation note:")
    print("  These commands are mask-style slash commands in one shared conversation context.")
    print("  They intentionally do not install isolated subagents by default.")
    print()
    print("Persona System:")
    print(f"  To enable persona, edit: {SUBMODULE_NAME}/config/persona_config.yaml")
    print("  Set 'enabled: true' and provide the absolute path to your persona.yaml")
    print(f"  Check status: python3 {SUBMODULE_NAME}/_scripts/persona_output.py --check")
    print()


if __name__ == "__main__":
    main()
