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
    
    # Get current time (compact format, no seconds)
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M")
    
    # Check key files and directories
    topics_path = ai_workspace / "discussion_topics.md"
    topics_status = "OK" if topics_path.exists() else "MISSING"
    
    cards_dir = ai_workspace / "inspiration_capital" / "cards"
    cards_count = count_files_in_directory(cards_dir, "*.md")
    
    notes_dir = ai_workspace / "notes"
    notes_count = count_files_in_directory(notes_dir, "*.md")
    
    # Build compact output
    output_lines = [
        f"PREFLIGHT {current_time}",
        f"STATUS: topics[{topics_status}] cards[{cards_count}] notes[{notes_count}]",
        "SCRIPTS: cleanup_ai_workspace.py | create_card.py | draw_cards.py",
        "END_CHECKLIST: persona_output.py → gleaning",
        # Generic reminder: each command defines its own phase count (discuss=4, prompt_engineer=5, etc.)
        "OUTPUT_MARKERS: [Phase N DONE] required per command workflow",
        "READY",
    ]
    
    return "\n".join(output_lines)


def main():
    """Main function"""
    print(run_preflight_check())


if __name__ == "__main__":
    main()
