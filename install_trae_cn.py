#!/usr/bin/env python3
"""install_trae_cn.py - Install Cursor AI Agent Team Framework for Trae CN (primary host).

Trae CN is the first-class host since v0.26.0: development, testing and
adaptation target Trae CN first; Cursor and Claude Code are compatible
side-targets. The legacy TRAE SOLO adaptation was removed (its capabilities
were merged into Trae CN's unified Agent by upstream v3.3.56+).

Installs (all official Trae CN project-level contracts, docs.trae.cn):
  - .trae/skills/cursor-agent-team-*   (mask + operation skills)
  - .trae/rules/*.md                   (cat-router always-on + six mask rules)
  - .trae/commands/*.md                (slash commands)
  - AGENTS.md at project root          (memory file, IDE + traecli both read)
  - ai_workspace/                      (shared state layer)

Usage:
    python cursor-agent-team/install_trae_cn.py

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
    ("_skills/cursor-agent-team", ".trae/skills/cursor-agent-team"),
    ("_skills/cursor-agent-team-discuss", ".trae/skills/cursor-agent-team-discuss"),
    ("_skills/cursor-agent-team-crew", ".trae/skills/cursor-agent-team-crew"),
    ("_skills/cursor-agent-team-prompt_engineer", ".trae/skills/cursor-agent-team-prompt_engineer"),
    ("_skills/cursor-agent-team-spec_translator", ".trae/skills/cursor-agent-team-spec_translator"),
    ("_skills/cursor-agent-team-writer", ".trae/skills/cursor-agent-team-writer"),
    ("_skills/cursor-agent-team-workflow", ".trae/skills/cursor-agent-team-workflow"),
    ("_skills/cursor-agent-team-writes", ".trae/skills/cursor-agent-team-writes"),
    ("_skills/cursor-agent-team-closing", ".trae/skills/cursor-agent-team-closing"),
    ("_skills/cursor-agent-team-doctor", ".trae/skills/cursor-agent-team-doctor"),
    ("_skills/cursor-agent-team-dispatch", ".trae/skills/cursor-agent-team-dispatch"),
]

COMMAND_FILES = [
    ("_trae_cn/commands/discuss.md", ".trae/commands/discuss.md"),
    ("_trae_cn/commands/crew.md", ".trae/commands/crew.md"),
    ("_trae_cn/commands/prompt_engineer.md", ".trae/commands/prompt_engineer.md"),
    ("_trae_cn/commands/writer.md", ".trae/commands/writer.md"),
    ("_trae_cn/commands/workflow.md", ".trae/commands/workflow.md"),
]

RULE_FILES = [
    ("_trae_cn/rules/cat-router.md", ".trae/rules/cat-router.md"),
    ("_trae_cn/rules/discussion-assistant.md", ".trae/rules/discussion-assistant.md"),
    ("_trae_cn/rules/crew-assistant.md", ".trae/rules/crew-assistant.md"),
    ("_trae_cn/rules/writer-assistant.md", ".trae/rules/writer-assistant.md"),
    ("_trae_cn/rules/prompt-engineer-assistant.md", ".trae/rules/prompt-engineer-assistant.md"),
    ("_trae_cn/rules/spec-translator-assistant.md", ".trae/rules/spec-translator-assistant.md"),
    ("_trae_cn/rules/workflow-assistant.md", ".trae/rules/workflow-assistant.md"),
]

AGENTS_FILE = "_trae_cn/AGENTS.md.template"

_CAT_ROUTING_SECTION = """## CAT Routing (Cursor Agent Team)

The CAT framework is installed in this repo (submodule `cursor-agent-team/`).
- Role-mask rules: `.trae/rules/` (`cat-router` is always on)
- Skills: `.trae/skills/cursor-agent-team-*`
- Shared state: `cursor-agent-team/ai_workspace/`
"""


def _load_owned_files(info_path):
    """Load files owned by a previous valid Trae CN installation."""
    try:
        with open(info_path, encoding="utf-8") as f:
            info = json.load(f)
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(info, dict):
        return []
    if info.get("source") != "cursor-agent-team" or info.get("platform") != "trae_cn":
        return []
    files = info.get("files")
    if not isinstance(files, list):
        return []
    return [item for item in files if isinstance(item, str) and item]


def _install_agents_md(submodule_dir, project_root):
    """Copy AGENTS.md template; append-mode if the host file has foreign content."""
    import shutil
    agents_src = os.path.join(submodule_dir, AGENTS_FILE)
    agents_dst = os.path.join(project_root, "AGENTS.md")
    if not os.path.exists(agents_src):
        u.colored_print("Warning: AGENTS.md template not found", "yellow")
        return []
    if not os.path.exists(agents_dst):
        shutil.copy2(agents_src, agents_dst)
        u.colored_print("✓ AGENTS.md template copied", "green")
        return ["AGENTS.md"]
    with open(agents_dst, encoding="utf-8") as f:
        existing = f.read()
    if "CAT Routing (Cursor Agent Team)" in existing:
        u.colored_print("✓ AGENTS.md CAT routing section already present (skipped)", "yellow")
    else:
        with open(agents_dst, "a", encoding="utf-8") as f:
            f.write("\n" + _CAT_ROUTING_SECTION)
        u.colored_print("✓ AGENTS.md CAT routing section appended (existing content kept)", "green")
    return []


def main():
    script_path = os.path.abspath(__file__)
    submodule_dir = u.get_submodule_dir(script_path)
    project_root = u.get_project_root(script_path)

    print("=" * 42)
    print("Cursor AI Agent Team Framework Installer (Trae CN)")
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
    for d in (".trae/skills", ".trae/commands", ".trae/rules"):
        u.ensure_dir(os.path.join(project_root, d))
    u.ensure_dir(os.path.join(submodule_dir, "config"))
    u.colored_print("✓ Directories created", "green")
    print()

    # Step 2b: Generate ai_workspace from config (PLAN-AF-001; shared across hosts)
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

    # Step 2c: Ownership protection — detect host edits to owned files
    info_path = os.path.join(project_root, ".trae", ".cursor-agent-team-installed")
    owned_files = _load_owned_files(info_path)
    if owned_files:
        owned, edited = u.detect_local_edits(info_path, project_root)
        if edited:
            u.colored_print(
                f"Warning: {len(edited)} installer-owned file(s) have LOCAL "
                "edits that re-installing would overwrite:", "yellow")
            for rel in edited:
                print(f"    {rel}")
            print("  Back them up now (they will be overwritten below).")
            print()

    # Step 3: Copy skills
    print("Step 3: Copying skills...")
    installed_skills, failed_skills = u.copy_dirs(
        SKILL_FILES, submodule_dir, project_root, owned_files=owned_files
    )
    if failed_skills:
        u.colored_print(f"Error: {len(failed_skills)} skill(s) failed to copy", "red")
        sys.exit(1)
    u.colored_print(f"✓ Skills copied ({len(SKILL_FILES)} skills)", "green")
    print()

    # Step 3b: Copy project rules (Trae CN native format)
    print("Step 3b: Copying project rules...")
    installed_rules, failed_rules = u.copy_files(RULE_FILES, submodule_dir, project_root)
    if failed_rules:
        u.colored_print(f"Error: {len(failed_rules)} rule(s) failed to copy", "red")
        sys.exit(1)
    u.colored_print(f"✓ Rules copied ({len(RULE_FILES)} rules)", "green")
    print()

    # Step 3c: Copy slash commands
    print("Step 3c: Copying slash commands...")
    installed_commands, failed_commands = u.copy_files(COMMAND_FILES, submodule_dir, project_root)
    if failed_commands:
        u.colored_print(f"Error: {len(failed_commands)} command(s) failed to copy", "red")
        sys.exit(1)
    u.colored_print(f"✓ Commands copied ({len(COMMAND_FILES)} commands)", "green")
    print()

    # Step 4: AGENTS.md (memory file for IDE + traecli)
    print("Step 4: Installing AGENTS.md...")
    agents_installed = _install_agents_md(submodule_dir, project_root)
    print()

    # Step 5: Installation record
    print("Step 5: Recording installation information...")
    version = u.get_version(submodule_dir)
    all_installed = installed_skills + installed_rules + installed_commands + agents_installed
    u.write_install_info(info_path, version, "trae_cn", all_installed)
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
    print("1. Open this project in Trae CN. First open asks to trust the")
    print("   project — project rules/skills take effect after trusting.")
    print("   Check: Settings > Rules & Memory shows .trae/rules/ entries;")
    print("   the Skills panel lists cursor-agent-team-* skills.")
    print()
    print("2. Slash commands are available in the chat input: /discuss,")
    print("   /crew, /prompt_engineer, /writer, /workflow.")
    print()
    print("3. Trae CLI (traecli) reads .trae/rules/, .trae/skills/ and")
    print("   AGENTS.md natively — no extra setup; trust the project on")
    print("   first CLI entry.")
    print()
    print("4. MCP servers are NOT installed by design — configure them in")
    print("   the GUI (Settings > MCP) or via .trae/mcp.json yourself.")
    print()
    u.print_git_tracking_note([
        ".gitmodules",
        SUBMODULE_NAME,
        ".trae/skills/",
        ".trae/rules/",
        ".trae/commands/",
        "AGENTS.md",
    ])
    print()
    print("Note: The workspace at cursor-agent-team/ai_workspace/ is shared")
    print("      between Trae CN, Cursor and Claude Code.")
    print()


if __name__ == "__main__":
    main()
