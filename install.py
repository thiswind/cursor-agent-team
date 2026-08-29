#!/usr/bin/env python3
"""install.py - Install Cursor AI Agent Team Framework (cross-platform).

Usage:
    python cursor-agent-team/install.py

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
    ("_cursor/commands/discuss.md", ".cursor/commands/discuss.md"),
    ("_cursor/commands/prompt_engineer.md", ".cursor/commands/prompt_engineer.md"),
    ("_cursor/commands/crew.md", ".cursor/commands/crew.md"),
    ("_cursor/commands/writer.md", ".cursor/commands/writer.md"),
    ("_cursor/commands/spec_translator.md", ".cursor/commands/spec_translator.md"),
    ("_cursor/commands/workflow.md", ".cursor/commands/workflow.md"),
]

RULE_FILES = [
    ("_cursor/rules/discussion_assistant.mdc", ".cursor/rules/discussion_assistant.mdc"),
    ("_cursor/rules/prompt_engineer_assistant.mdc", ".cursor/rules/prompt_engineer_assistant.mdc"),
    ("_cursor/rules/crew_assistant.mdc", ".cursor/rules/crew_assistant.mdc"),
    ("_cursor/rules/writer_assistant.mdc", ".cursor/rules/writer_assistant.mdc"),
    ("_cursor/rules/spec_translator_assistant.mdc", ".cursor/rules/spec_translator_assistant.mdc"),
    ("_cursor/rules/workflow_assistant.mdc", ".cursor/rules/workflow_assistant.mdc"),
    ("_cursor/rules/tts_speech_rules.mdc", ".cursor/rules/tts_speech_rules.mdc"),
    ("_cursor/rules/gleaning.mdc", ".cursor/rules/gleaning.mdc"),
    ("_cursor/rules/wandering.mdc", ".cursor/rules/wandering.mdc"),
    ("_cursor/rules/persona_input_layer.mdc", ".cursor/rules/persona_input_layer.mdc"),
    ("_cursor/rules/persona_output_layer.mdc", ".cursor/rules/persona_output_layer.mdc"),
    ("_cursor/rules/persona_definition.mdc", ".cursor/rules/persona_definition.mdc"),
    ("_cursor/rules/history_context_handler.mdc", ".cursor/rules/history_context_handler.mdc"),
    ("_cursor/rules/social_media_policy.mdc", ".cursor/rules/social_media_policy.mdc"),
]


def main():
    script_path = os.path.abspath(__file__)
    submodule_dir = u.get_submodule_dir(script_path)
    project_root = u.get_project_root(script_path)

    print("=" * 42)
    print("Cursor AI Agent Team Framework Installer")
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
    u.ensure_dir(os.path.join(project_root, ".cursor", "commands"))
    u.ensure_dir(os.path.join(project_root, ".cursor", "rules"))
    u.ensure_dir(os.path.join(submodule_dir, "config"))
    u.colored_print("✓ Directories created", "green")
    print()

    # Step 2b: Generate ai_workspace from config (PLAN-AF-001)
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

    # Step 3: Copy files
    print("Step 3: Copying files...")
    all_files = COMMAND_FILES + RULE_FILES
    installed, failed = u.copy_files(all_files, submodule_dir, project_root)
    if failed:
        u.colored_print(f"Error: {len(failed)} file(s) failed to copy", "red")
        sys.exit(1)
    u.colored_print("✓ Files copied", "green")
    print()

    # Step 4: Installation record
    print("Step 4: Recording installation information...")
    version = u.get_version(submodule_dir)
    info_path = os.path.join(project_root, ".cursor", ".cursor-agent-team-installed")
    u.write_install_info(info_path, version, "cursor", installed)
    u.colored_print("✓ Installation information recorded", "green")
    print()

    # Step 5: Check git tracking hints
    print("Step 5: Checking git tracking hints...")
    u.warn_if_ignored(project_root, SUBMODULE_NAME)
    print()

    # Summary
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
    print("You can now use the following commands in Cursor:")
    print("  /discuss - Discussion partner")
    print("  /prompt_engineer - Prompt engineer")
    print("  /crew - Crew member")
    print("  /writer - Writer (Draft -> Review -> Final)")
    print("  /spec_translator - Spec-Kit translator")
    print()
    u.print_git_tracking_note([
        ".gitmodules",
        SUBMODULE_NAME,
        ".cursor/commands/",
        ".cursor/rules/",
    ])
    print()
    print("Persona System:")
    print(f"  To enable persona, edit: {SUBMODULE_NAME}/config/persona_config.yaml")
    print("  Set 'enabled: true' and provide the absolute path to your persona.yaml")
    print(f"  Check status: python {SUBMODULE_NAME}/_scripts/persona_output.py --check")
    print()


if __name__ == "__main__":
    main()
