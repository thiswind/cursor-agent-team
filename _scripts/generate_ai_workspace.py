#!/usr/bin/env python3
"""
Generate ai_workspace from config at install time.
PLAN-AF-001: single config (JSON) at cursor-agent-team root; this script creates
dirs and writes seed files. Symlinks at notes/ and inspiration_capital/cards are
removed first if present.
"""

import json
import os
import sys
import argparse
from pathlib import Path


# Directories to create under ai_workspace (parent-before-child order)
DEFAULT_DIRECTORIES = [
    "plans",
    "agent_requirements",
    "inspiration_capital",
    "inspiration_capital/cards",
    "crew",
    "crew/sessions",
    "prompt_engineer",
    "prompt_engineer/sessions",
    "spec_translator",
    "spec_translator/sessions",
    "scratchpad",
    "scratchpad/notes",
    "scratchpad/scripts",
    "scratchpad/analysis",
    "scratchpad/temp",
    "notes",
    "templates",
    "temp",
    "topic_archives",
]


def _root_readme():
    """Root README; Protected list must match cleanup_ai_workspace.PROTECTED_FILES."""
    return """# AI Workspace

Private workspace for AI agents. All paths are relative to `cursor-agent-team/ai_workspace/`.

## Why This Workspace

This is a **dedicated agent workspace** — a core architectural principle of the framework. Agents can write scripts for experiments, take notes, and save intermediate results from searches and research. This design aligns with:

- **Scratchpad reasoning** — intermediate computation improves LLM quality (Nye & Andreassen; EMNLP 2024)
- **External memory** — persistence beyond context window (MemGPT; MemoryAgentBench)
- **Staged generation** — iterative refinement outperforms direct output (IAD 2025)

The workspace functions as **cognitive artifacts** that extend the agent's effective reasoning capacity—enabling higher-quality output than direct generation alone.

---

## Quick Reference (READ FIRST)

| What | Path | Naming |
|------|------|--------|
| Notes | `scratchpad/notes/` | `note_[topic]_YYYYMMDD.md` |
| Topic Tree | `discussion_topics.md` | Fixed |
| Plans | `plans/` | `PLAN-[TopicID]-[Seq].md` |
| Agent Requirements | `agent_requirements/` | `AGENT-REQUIREMENT-[TopicID]-[Seq].md` |

---

## NEVER DO (Hard Constraints)

- NEVER delete protected files (see Protected Files section)
- NEVER save notes outside `scratchpad/notes/`
- NEVER save plans outside `plans/`
- NEVER modify `discussion_topics.md` without following validation flow
- NEVER use paths outside `ai_workspace/` for temporary files

---

## Protected Files

These files cannot be deleted without `--force` flag (must match _scripts/cleanup_ai_workspace.py PROTECTED_FILES):

```
README.md
discussion_topics.md
plans/README.md
plans/INDEX.md
crew/README.md
prompt_engineer/README.md
```

---

## Directory Structure

```
ai_workspace/
├── README.md                     # This file
├── discussion_topics.md          # Topic tree (/discuss)
├── plans/                        # Execution plans
├── agent_requirements/           # Agent requirements
├── inspiration_capital/          # Scatter cards for creativity
│   ├── cards/                    # Card storage (no categories!)
│   ├── scripts/                  # Python tools
│   └── tests/                    # Test cases
├── crew/sessions/                # /crew sessions
├── prompt_engineer/sessions/     # /prompt_engineer sessions
├── spec_translator/sessions/     # /spec_translator sessions
├── spec-kit-*.md                 # Spec-Kit documents
└── scratchpad/                   # Temporary workspace
    ├── notes/                    # Discussion notes
    ├── scripts/                  # Temporary scripts
    ├── analysis/                 # Analysis results
    └── temp/                     # Other temporary files
```

---

## Role-Specific Usage

### /discuss

| Purpose | Path | Format |
|---------|------|--------|
| Topic Tree | `discussion_topics.md` | Fixed |
| Notes | `scratchpad/notes/` | `note_[topic]_YYYYMMDD.md` |
| Plans | `plans/` | `PLAN-[TopicID]-[Seq].md` |
| Requirements | `agent_requirements/` | `AGENT-REQUIREMENT-[TopicID]-[Seq].md` |

### /crew

Session directory: `crew/sessions/session_YYYYMMDD_HHMMSS/`

### /prompt_engineer

Session directory: `prompt_engineer/sessions/session_YYYYMMDD_HHMMSS/`

### Inspiration Capital

- `cards/` — Scatter cards storage
- `scripts/` — create_card.py, draw_cards.py

See `inspiration_capital/README.md` for details.

---

## Cleanup

```bash
python cursor-agent-team/_scripts/cleanup_ai_workspace.py --older-than 7
```

---

**Last Updated**: 2026-03-06
"""


def _discussion_topics_minimal():
    from datetime import datetime as _dt
    _today = _dt.now().strftime("%Y-%m-%d")
    return f"""# Discussion Topics Tree

> Topic tree for `/discuss`. Created at install time.
> Timeline discipline: one `round_NN` entry per working round, appended under the
> topic's detail section (append-only; old rounds are never deleted or rewritten).
> Status enum (canonical, underscore style): in_progress / completed / closed /
> pending / paused / active.

## Active Topic

### [A] First Topic: <one-line goal>

- **Status**: in_progress
- Timeline:
  - round_01 ({_today}): kickoff — replace this skeleton with the project's first real topic; keep this entry as history.

## Topic Index

| ID | Title | Status | Last Active |
|:---|:------|:-------|:------------|
| [A] | First Topic | in_progress | {_today} |

**Last Updated**: {_today}
"""


def _plans_index_minimal():
    return """# Execution Plans Index

> Last Updated: (install time)

## Plan List

| ID | Topic | Goal | Status | Created |
|----|-------|------|--------|---------|
| [PLAN-EXAMPLE-001](PLAN-EXAMPLE-001.md) | [EX] Example | Example plan for new users | pending | (install) |
"""


def _plan_example():
    return """# PLAN-EXAMPLE-001: Example Plan

> **Topic**: [EX] Example
> **Goal**: Demonstrate plan structure for new users.
> **Status**: pending
> **Created**: (install time)

---

## Goal

This is an example plan. Replace with your own goal.

## Steps

1. Step one
2. Step two
3. Step three

---

**Version**: 1.0
"""


def _agent_requirement_example():
    return """# AGENT-REQUIREMENT-EXAMPLE-001: Example Requirement

> **Topic**: [EX] Example
> **Status**: pending
> **Created**: (install time)

---

## Requirement Info

- **Requirement ID**: AGENT-REQUIREMENT-EXAMPLE-001
- **Target Executor**: /prompt_engineer

## Role Design

### Role Name

Example Role

### Core Functions

1. Function one
2. Function two

---

**Version**: 1.0
"""


def _example_card():
    return """# example_card

**Time**: (install date)
**Source**: Install seed
**Trigger**: Example card for new users

---

This is an example scatter card. Use `create_card.py` to add your own; use `draw_cards.py` to browse.

---

**Why interesting**: Demonstrates the card format (Time, Source, Trigger, Content, Why interesting).
"""


def _example_note():
    return """# Example Note

Date: (install date)
Topic: Example

## Discoveries

1. This is an example note under `notes/`.
2. Use it as a template for discussion notes.

## Thoughts

Replace with your content.
"""


def _agent_requirement_template():
    return """# 需求规格说明 AGENT-REQUIREMENT-[话题ID]-[序号]

## 需求信息
- **需求编号**: AGENT-REQUIREMENT-[话题ID]-[序号]
- **关联话题**: [话题ID] - [话题名称]
- **创建时间**: YYYY-MM-DD HH:MM:SS
- **创建者**: /discuss
- **目标执行者**: /prompt_engineer
- **状态**: 待处理 / 处理中 / 已完成

## 角色设计需求

### 角色名称
[角色名称]

### 角色定位
[角色的核心定位和职责]

### 核心功能
1. [功能1描述]
2. [功能2描述]

### 使用场景
[什么情况下使用这个角色]

### 约束条件
- [约束1]
- [约束2]

## 讨论要点
[从讨论中提取的关键设计决策]
"""


def _agent_requirements_index_minimal():
    return """# Agent Requirements Index

> Last Updated: (install time)

## Requirement List

| ID | Topic | Status | Created |
|----|-------|--------|---------|
"""


def get_default_config():
    """Return default config dict: directories (list), files (dict path -> content)."""
    return {
        "directories": list(DEFAULT_DIRECTORIES),
        "files": {
            "README.md": _root_readme(),
            "discussion_topics.md": _discussion_topics_minimal(),
            "plans/README.md": """# Execution Plans

Storage for execution plans generated by `/discuss`. Path: `cursor-agent-team/ai_workspace/plans/`

## Quick Reference

| What | Path | Format |
|------|------|--------|
| Plan File | `plans/` | `PLAN-[TopicID]-[Seq].md` |
| Index | `plans/` | `INDEX.md` |

**Last Updated**: 2026-02-02
""",
            "plans/INDEX.md": _plans_index_minimal(),
            "plans/PLAN-EXAMPLE-001.md": _plan_example(),
            "agent_requirements/README.md": """# Agent Requirements

Storage for agent requirements generated by `/discuss`. Path: `cursor-agent-team/ai_workspace/agent_requirements/`

## Quick Reference

| What | Path | Format |
|------|------|--------|
| Requirement File | `agent_requirements/` | `AGENT-REQUIREMENT-[TopicID]-[Seq].md` |
| Index | `agent_requirements/` | `INDEX.md` |

**Last Updated**: 2026-02-02
""",
            "agent_requirements/AGENT-REQUIREMENT-EXAMPLE-001.md": _agent_requirement_example(),
            "agent_requirements/INDEX.md": _agent_requirements_index_minimal(),
            "inspiration_capital/README.md": """# Inspiration Capital (灵感资本)

> "先有资本，后有主意"

## Overview

Scatter card collection for inspiring creativity.

## Directory Structure

```
inspiration_capital/
├── README.md
├── cards/
├── scripts/
└── tests/
```

## Usage

- Create card: `python scripts/create_card.py --source "..." --trigger "..."`
- Draw cards: `python scripts/draw_cards.py --count 3`

**Last Updated**: 2026-02-02
""",
            "crew/README.md": """# Crew Workspace

Workspace for `/crew` command. Path: `cursor-agent-team/ai_workspace/crew/`

## Quick Reference

| What | Path | Format |
|------|------|--------|
| Session | `sessions/` | `session_YYYYMMDD_HHMMSS/` |

**Last Updated**: 2026-02-02
""",
            "prompt_engineer/README.md": """# Prompt Engineer Workspace

Workspace for `/prompt_engineer` command. Path: `cursor-agent-team/ai_workspace/prompt_engineer/`

## Quick Reference

| What | Path | Format |
|------|------|--------|
| Session | `sessions/` | `session_YYYYMMDD_HHMMSS/` |

**Last Updated**: 2026-02-02
""",
            "spec_translator/README.md": """# Spec Translator Workspace

Workspace for `/spec_translator` command. Path: `cursor-agent-team/ai_workspace/spec_translator/`

## Quick Reference

| What | Path | Format |
|------|------|--------|
| Session | `sessions/` | `session_YYYYMMDD_HHMMSS/` |

**Last Updated**: 2026-02-02
""",
            "scratchpad/README.md": """# Scratchpad

Temporary workspace for `/discuss`. Path: `cursor-agent-team/ai_workspace/scratchpad/`

## Quick Reference

| What | Path | Format |
|------|------|--------|
| Notes | `notes/` | `note_[topic]_YYYYMMDD.md` |
| Scripts | `scripts/` | `script_*.py` |
| Analysis | `analysis/` | `analysis_*.md` |
| Temp | `temp/` | `temp_*` |

**Last Updated**: 2026-02-02
""",
            "inspiration_capital/cards/example_card.md": _example_card(),
            "notes/example_note.md": _example_note(),
            "templates/agent_requirement_template.md": _agent_requirement_template(),
        },
    }


def load_config(config_path):
    """Load config from JSON file. Returns dict with 'directories' and 'files'."""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def remove_symlinks_if_any(ai_workspace_root):
    """Remove symlinks at notes and inspiration_capital/cards if they are symlinks."""
    for subpath in ["notes", "inspiration_capital/cards"]:
        p = Path(ai_workspace_root) / subpath
        if p.exists() and p.is_symlink():
            p.unlink()


def should_write_file(rel_path: str, out_path: Path, *, force: bool) -> bool:
    """
    PLAN-AF-002: Non-destructive defaults.

    - Always write: README files and templates (stable guidance).
    - Write-if-missing: everything else (indexes, topic tree, examples, etc.).
    - Force mode overrides and writes everything.
    """
    if force:
        return True

    # Always-write (safe guidance)
    if rel_path == "README.md" or rel_path.endswith("/README.md"):
        return True
    if rel_path.startswith("templates/"):
        return True

    # Default: do not overwrite existing user/history/index/example files
    return not out_path.exists()


def run(cursor_agent_team_root, config_path=None, *, force: bool = False):
    """
    Generate ai_workspace under cursor_agent_team_root from config.
    If config_path is None, use cursor_agent_team_root/ai_workspace_config.json.
    """
    root = Path(cursor_agent_team_root)
    ai_workspace = root / "ai_workspace"
    if config_path is None:
        config_path = root / "ai_workspace_config.json"
    if not Path(config_path).exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    config = load_config(config_path)
    dirs = config.get("directories", [])
    files = config.get("files", {})

    # (a) Remove symlinks first
    remove_symlinks_if_any(ai_workspace)

    # (b) Create directories (parent-before-child already in DEFAULT_DIRECTORIES)
    for d in dirs:
        (ai_workspace / d).mkdir(parents=True, exist_ok=True)

    # (c) Write files
    for rel_path, content in files.items():
        out_path = ai_workspace / rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if should_write_file(rel_path, out_path, force=force):
            out_path.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Generate ai_workspace from config (non-destructive by default)."
    )
    parser.add_argument(
        "--write-config",
        action="store_true",
        help="Write default ai_workspace_config.json to cursor-agent-team root (does not generate ai_workspace).",
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Path to ai_workspace_config.json (default: cursor-agent-team/ai_workspace_config.json).",
    )
    parser.add_argument(
        "--force",
        "--overwrite",
        dest="force",
        action="store_true",
        help="Overwrite all files defined by config (dangerous).",
    )
    args = parser.parse_args()

    if args.write_config:
        # Write default config to cursor-agent-team root (parent of _scripts)
        script_dir = Path(__file__).resolve().parent
        cursor_agent_team_root = script_dir.parent
        config_path = cursor_agent_team_root / "ai_workspace_config.json"
        config = get_default_config()
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"Wrote {config_path}")
        return

    # Otherwise run generation (called from installers)
    try:
        root = os.environ.get("CURSOR_AGENT_TEAM_ROOT")
        if not root:
            # Assume we're in cursor-agent-team/_scripts
            root = Path(__file__).resolve().parent.parent
        run(root, config_path=args.config, force=args.force)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
