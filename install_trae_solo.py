#!/usr/bin/env python3
"""install_trae_solo.py - Install Cursor AI Agent Team Framework for TRAE SOLO.

Usage:
    python cursor-agent-team/install_trae_solo.py

Prerequisites:
    git submodule add https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
"""

import json
import os
import sys

_scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_scripts")
sys.path.insert(0, _scripts_dir)
import _install_utils as u

SUBMODULE_NAME = "cursor-agent-team"

SKILL_FILES = [
    ("_trae_solo/skills/cursor-agent-team-discuss", ".trae/skills/cursor-agent-team-discuss"),
    ("_trae_solo/skills/cursor-agent-team-crew", ".trae/skills/cursor-agent-team-crew"),
    ("_trae_solo/skills/cursor-agent-team-prompt_engineer", ".trae/skills/cursor-agent-team-prompt_engineer"),
    ("_trae_solo/skills/cursor-agent-team-writer", ".trae/skills/cursor-agent-team-writer"),
    ("_trae_solo/skills/cursor-agent-team-workflow", ".trae/skills/cursor-agent-team-workflow"),
]

COMMAND_FILES = [
    ("_trae_solo/commands/discuss.md", ".trae/commands/discuss.md"),
    ("_trae_solo/commands/crew.md", ".trae/commands/crew.md"),
    ("_trae_solo/commands/prompt_engineer.md", ".trae/commands/prompt_engineer.md"),
    ("_trae_solo/commands/writer.md", ".trae/commands/writer.md"),
    ("_trae_solo/commands/workflow.md", ".trae/commands/workflow.md"),
]

AGENTS_FILE = "_trae_solo/AGENTS.md.template"


def _load_owned_files(info_path):
    """Load files owned by a previous valid TRAE SOLO installation."""
    try:
        with open(info_path, encoding="utf-8") as f:
            info = json.load(f)
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(info, dict):
        return []
    if info.get("source") != "cursor-agent-team" or info.get("platform") != "trae_solo":
        return []
    files = info.get("files")
    if not isinstance(files, list):
        return []
    return [item for item in files if isinstance(item, str) and item]


def main():
    script_path = os.path.abspath(__file__)
    submodule_dir = u.get_submodule_dir(script_path)
    project_root = u.get_project_root(script_path)

    print("=" * 42)
    print("Cursor AI Agent Team Framework Installer (TRAE SOLO)")
    print("=" * 42)
    print()

    # Step 1: Environment check
    print("Step 1: Checking environment...")
    ok, msg = u.check_environment(project_root, submodule_dir)
    if not ok:
        u.colored_print(f"Error: {msg}", "red")
        sys.exit(1)
    u.colored_print(f"✓ {msg}", "green")
    print()

    # Step 2: Create directories
    print("Step 2: Creating directory structure...")
    u.ensure_dir(os.path.join(project_root, ".trae", "skills"))
    u.ensure_dir(os.path.join(project_root, ".trae", "commands"))
    u.ensure_dir(os.path.join(submodule_dir, "config"))
    u.colored_print("✓ Directories created", "green")
    print()

    # Step 2b: Generate ai_workspace from config (PLAN-AF-001; shared with install.py)
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

    # Step 3: Copy skills
    print("Step 3: Copying skills...")
    info_path = os.path.join(project_root, ".trae", ".cursor-agent-team-installed")
    owned_files = _load_owned_files(info_path)
    installed_skills, failed_skills = u.copy_dirs(
        SKILL_FILES, submodule_dir, project_root, owned_files=owned_files
    )
    if failed_skills:
        u.colored_print(f"Error: {len(failed_skills)} skill(s) failed to copy", "red")
        sys.exit(1)
    u.colored_print("✓ Skills copied", "green")
    print()

    # Step 3b: Copy slash commands
    print("Step 3b: Copying slash commands...")
    installed_commands, failed_commands = u.copy_files(
        COMMAND_FILES, submodule_dir, project_root
    )
    if failed_commands:
        u.colored_print(f"Error: {len(failed_commands)} command(s) failed to copy", "red")
        sys.exit(1)
    u.colored_print("✓ Commands copied", "green")
    print()

    # Step 4: Copy AGENTS.md template
    print("Step 4: Copying AGENTS.md template...")
    agents_src = os.path.join(submodule_dir, AGENTS_FILE)
    agents_dst = os.path.join(project_root, "AGENTS.md")
    agents_created = False
    if os.path.exists(agents_src):
        if not os.path.exists(agents_dst):
            import shutil
            shutil.copy2(agents_src, agents_dst)
            agents_created = True
            u.colored_print("✓ AGENTS.md template copied", "green")
        else:
            u.colored_print("✓ AGENTS.md already exists (skipped)", "yellow")
    else:
        u.colored_print("Warning: AGENTS.md template not found", "yellow")
    print()

    # Step 5: Installation record
    print("Step 5: Recording installation information...")
    version = u.get_version(submodule_dir)
    all_installed = installed_skills + installed_commands + (["AGENTS.md"] if agents_created else [])
    u.write_install_info(info_path, version, "trae_solo", all_installed)
    u.colored_print("✓ Installation information recorded", "green")
    print()

    # Step 6: Check git tracking hints
    print("Step 6: Checking git tracking hints...")
    u.warn_if_ignored(project_root, SUBMODULE_NAME)
    print()

    # Summary
    print("=" * 42)
    u.colored_print("Installation completed successfully!", "green")
    print("=" * 42)
    print()
    print("Installed items:")
    for item in all_installed:
        print(f"  ✅ {item}")
    print()
    print(f"Version: {version}")
    print()
    print("Next steps:")
    print()
    print("1. Enable AGENTS.md in TRAE SOLO:")
    print("   - Go to Settings > Rules")
    print("   - Enable 'Include AGENTS.md in context'")
    print()
    print("2. Slash commands installed to .trae/commands/:")
    print("     • /discuss: Discussion partner")
    print("     • /crew: Crew member")
    print("     • /prompt_engineer: Prompt engineer")
    print("     • /writer: Writer (Draft -> Review -> Final)")
    print()
    print("3. You can now use the skills in TRAE SOLO:")
    print("   - cursor-agent-team-discuss")
    print("   - cursor-agent-team-crew")
    print("   - cursor-agent-team-prompt-engineer")
    print("   - cursor-agent-team-writer")
    print()
    u.print_git_tracking_note([
        ".gitmodules",
        SUBMODULE_NAME,
        ".trae/skills/",
        ".trae/commands/",
        "AGENTS.md",
    ])
    print()
    print("Persona System:")
    print(f"  To enable persona, edit: {SUBMODULE_NAME}/config/persona_config.yaml")
    print("  Set 'enabled: true' and provide the absolute path to your persona.yaml")
    print(f"  Check status: python {SUBMODULE_NAME}/_scripts/persona_output.py --check")
    print()
    print("Note: The workspace at cursor-agent-team/ai_workspace/ is shared")
    print("      between Cursor and TRAE SOLO.")
    print()


if __name__ == "__main__":
    main()
