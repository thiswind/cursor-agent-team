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
    ("_claude/commands/writer.md", ".claude/commands/writer.md"),
    ("_claude/commands/spec_translator.md", ".claude/commands/spec_translator.md"),
    ("_claude/commands/workflow.md", ".claude/commands/workflow.md"),
]

RULE_FILES = [
    ("_claude/rules/crew_assistant.md", ".claude/rules/crew_assistant.md"),
    ("_claude/rules/writer_assistant.md", ".claude/rules/writer_assistant.md"),
]

SKILL_DIRS = [
    ("_skills/cursor-agent-team", ".claude/skills/cursor-agent-team"),
    ("_skills/cursor-agent-team-discuss", ".claude/skills/cursor-agent-team-discuss"),
    ("_skills/cursor-agent-team-crew", ".claude/skills/cursor-agent-team-crew"),
    ("_skills/cursor-agent-team-prompt_engineer", ".claude/skills/cursor-agent-team-prompt_engineer"),
    ("_skills/cursor-agent-team-spec_translator", ".claude/skills/cursor-agent-team-spec_translator"),
    ("_skills/cursor-agent-team-writer", ".claude/skills/cursor-agent-team-writer"),
    ("_skills/cursor-agent-team-workflow", ".claude/skills/cursor-agent-team-workflow"),
]


def _load_owned_files(info_path):
    """Read the previously-installed file list so re-installs can overwrite
    owned files without touching user-added files (same pattern as
    install_trae_solo.py)."""
    import json
    try:
        with open(info_path, "r", encoding="utf-8") as f:
            return set(json.load(f).get("files", []))
    except (FileNotFoundError, ValueError):
        return set()


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
    u.ensure_dir(os.path.join(project_root, ".claude", "rules"))
    u.ensure_dir(os.path.join(project_root, ".claude", "skills"))
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

    print("Step 3: Copying Claude Code commands and rules...")
    installed, failed = u.copy_files(COMMAND_FILES + RULE_FILES, submodule_dir, project_root)
    if failed:
        u.colored_print(f"Error: {len(failed)} file(s) failed to copy", "red")
        sys.exit(1)
    u.colored_print("✓ Commands and rules copied", "green")
    print()

    print("Step 3b: Copying frontier-agent skills...")
    info_path = os.path.join(project_root, ".claude", ".cursor-agent-team-installed")
    owned_files = _load_owned_files(info_path)
    installed_skills, failed_skills = u.copy_dirs(
        SKILL_DIRS, submodule_dir, project_root, owned_files=owned_files
    )
    if failed_skills:
        u.colored_print(f"Error: {len(failed_skills)} skill(s) failed to copy", "red")
        sys.exit(1)
    installed += installed_skills
    u.colored_print("✓ Frontier-agent skills copied (.claude/skills/)", "green")
    print()

    print("Step 4: Recording installation information...")
    version = u.get_version(submodule_dir)
    info_path = os.path.join(project_root, ".claude", ".cursor-agent-team-installed")
    u.write_install_info(info_path, version, "claude_code", installed)
    u.colored_print("✓ Installation information recorded", "green")
    print()

    print("Step 5: Checking git tracking hints...")
    u.warn_if_ignored(project_root, SUBMODULE_NAME)
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
    print("  /writer - Writer (Draft -> Review -> Final)")
    print("  /spec_translator - Spec-Kit translator")
    print()
    print("Claude Code adaptation note:")
    print("  These commands are mask-style slash commands in one shared conversation context.")
    print("  They intentionally do not install isolated subagents by default.")
    print()
    print("Frontier-agent path (since v0.22.0):")
    print("  7 skills installed under .claude/skills/ — the master routing skill")
    print("  `cursor-agent-team` plus one per role mask. A frontier agent that")
    print("  auto-discovers skills can run CAT without slash commands.")
    print()
    u.print_git_tracking_note([
        ".gitmodules",
        SUBMODULE_NAME,
        ".claude/commands/",
        ".claude/rules/",
        ".claude/skills/",
    ])
    print()
    print("Persona System:")
    print(f"  To enable persona, edit: {SUBMODULE_NAME}/config/persona_config.yaml")
    print("  Set 'enabled: true' and provide the absolute path to your persona.yaml")
    print(f"  Check status: python3 {SUBMODULE_NAME}/_scripts/persona_output.py --check")
    print()


if __name__ == "__main__":
    main()
