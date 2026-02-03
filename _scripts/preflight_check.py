#!/usr/bin/env python3
"""
Preflight Check - AI Agent Pre-flight Check System

Runs automatically when all roles start, provides:
1. Current time
2. Workspace status check
3. Operation conventions reminder

Core principle: Use scripts to replace memory, reduce AI cognitive load.
"""

import os
from datetime import datetime
from pathlib import Path


def get_project_root() -> Path:
    """Get project root directory (cursor-agent-team/)"""
    return Path(__file__).parent.parent


def check_file_exists(filepath: Path) -> tuple[bool, str]:
    """Check if file exists"""
    exists = filepath.exists()
    status = "✅" if exists else "❌"
    return exists, status


def count_files_in_directory(dirpath: Path, pattern: str = "*.md") -> int:
    """Count files matching pattern in directory"""
    if not dirpath.exists():
        return 0
    return len(list(dirpath.glob(pattern)))


def run_preflight_check() -> str:
    """Execute preflight check, return formatted output"""
    project_root = get_project_root()
    ai_workspace = project_root / "ai_workspace"
    
    # Get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Check key files and directories
    topics_path = ai_workspace / "discussion_topics.md"
    topics_exists, topics_status = check_file_exists(topics_path)
    
    cards_dir = ai_workspace / "inspiration_capital" / "cards"
    cards_count = count_files_in_directory(cards_dir, "*.md")
    cards_status = "✅" if cards_dir.exists() else "❌"
    
    notes_dir = ai_workspace / "notes"
    notes_count = count_files_in_directory(notes_dir, "*.md")
    notes_status = "✅" if notes_dir.exists() else "❌"
    
    # Build output
    output_lines = [
        "=== Preflight Check ===",
        f"⏰ Current Time: {current_time}",
        "",
        "📋 Workspace Status:",
        f"  {topics_status} discussion_topics.md",
        f"  {cards_status} inspiration_capital/ ({cards_count} cards)",
        f"  {notes_status} notes/ ({notes_count} files)",
        "",
        "📌 Operation Conventions:",
        "  • Delete → _scripts/cleanup_ai_workspace.py",
        "  • Create card → ai_workspace/inspiration_capital/scripts/create_card.py",
        "  • Draw cards → ai_workspace/inspiration_capital/scripts/draw_cards.py",
        "",
        "⚠️ Before Ending (DO NOT SKIP):",
        "  1. persona_output.py → Load persona before output",
        "  2. Gleaning → Create card if valuable insights found",
        "",
        "=== Ready ===",
    ]
    
    return "\n".join(output_lines)


def main():
    """Main function"""
    print(run_preflight_check())


if __name__ == "__main__":
    main()
