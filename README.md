<p align="center">
  <img src="logo.png" alt="Logo" width="200">
</p>

# Cursor AI Agent Team Framework

**Intelligence augmentation for Cursor IDE** — an elite team under your command, with zero handoff and inherent context continuity.

## Why cursor-agent-team?

We augment human capability; we don't replace it. Three design pillars:

1. **Multi-role, not multi-agent** — One LLM, one conversation. `/discuss` and `/crew` share the same context. No agent handoff, no context loss. Like a meeting room where everyone has perfect memory.

2. **Human-in-the-loop by design** — You are the conductor. We explore, you decide. We execute, you confirm. "Your command, our execution" — not "set and forget."

3. **Empowerment, not replacement** — Democratizing team access: individuals get team-level capability. Cognitive load redistribution: you think strategy, we handle execution details. Frees you from the "details quagmire" for purer thinking.

## What it is

A **multi-role collaboration framework** for Cursor IDE and Qwen Code. One LLM wears different "masks" (commands) in the same conversation. Provides:

- **Structured workflow**: discuss → plan → execute
- **Specialized roles**: Each command has distinct responsibilities
- **Hard constraint validation**: Python scripts ensure deterministic output
- **Extensible team**: Create new roles via `/prompt_engineer`

## Positioning & Related Concepts

| Concept | Our approach |
|---------|--------------|
| **Intelligence Augmentation (IA)** | We augment human cognitive capability rather than replace it (Licklider's man-computer symbiosis; Springer 2024) |
| **Multi-role vs multi-agent** | Multi-agent systems use handoffs; context loss is a critical challenge. We avoid it by design: zero handoff, one conversation |
| **Human-AI teaming** | Human as conductor; AI roles are "masks" in the same meeting (National Academies 2022) |
| **Cognitive load redistribution** | You focus on strategy; we handle execution details (Cognitive Load Theory) |

| vs | cursor-agent-team |
|----|-------------------|
| Multi-agent frameworks | No handoff, no context loss |
| Autonomous agents | Human-in-the-loop, not set-and-forget |
| Generic AI assistants | Structured roles, workflow enforcement, team metaphor |

## Quick Start

Tell Cursor Agent:

```
Install cursor-agent-team from https://github.com/thiswind/cursor-agent-team.git as a submodule and run the install script.
```

Then type `/discuss` to start.

For manual installation or Qwen Code, see [Installation](#installation).

## Core Roles

| Role | Command | Description |
|------|---------|-------------|
| **Discussion Partner** | `/discuss` | Analyzes problems, explores ideas, creates execution plans |
| **Crew Member** | `/crew` | Executes plans strictly according to specifications |
| **Prompt Engineer** | `/prompt_engineer` | Creates and maintains new roles (commands) |

## Workflow

![Framework Banner — /crew, /discuss, /prompt_engineer](banner.png)

```
/discuss → [Explore & Plan] → /crew → [Execute] → Done
                ↓
         /prompt_engineer → [Create New Role] → Use New Command
```

1. **Plan**: Use `/discuss` to explore ideas and generate execution plans
2. **Execute**: Use `/crew` to execute the plans
3. **Expand**: Use `/prompt_engineer` to create new roles when needed

## Installation

**Cursor IDE** — Tell Cursor Agent to install, or run manually:

```bash
git submodule add -f https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
./cursor-agent-team/install.sh
```

Update: `git submodule update --remote cursor-agent-team && ./cursor-agent-team/install.sh`

**Qwen Code**:

```bash
git submodule add -f https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
./cursor-agent-team/install_qwen.sh
```

Update: `git submodule update --remote cursor-agent-team && ./cursor-agent-team/install_qwen.sh`

**Note**: The workspace at `cursor-agent-team/ai_workspace/` is shared between both platforms.

## Features

### Core

**Persona System (v0.8.0+)** — Script-driven persona integration without degrading work quality. Based on [persona-spec](https://github.com/thiswind/persona-spec).

```bash
python cursor-agent-team/_scripts/persona_output.py --check
```

**Inspiration Capital (v0.7.0+)** — Scatter card collection for sparking creativity.

```bash
python ai_workspace/inspiration_capital/scripts/create_card.py --source "Source" --trigger "Trigger"
python ai_workspace/inspiration_capital/scripts/draw_cards.py --count 3
```

See `ai_workspace/inspiration_capital/README.md` for details.

### Extended

- **Text-to-Speech (macOS)**: Voice feedback via `say`; activated when user requests ("read to me"). `python cursor-agent-team/_scripts/tts_speak.py --check`
- **Social Media**: Integration with [Moltbook](https://moltbook.com/). See `.cursor/rules/social_media_policy.mdc`
- **Spec-Kit Translator**: Converts plans to [spec-kit](https://github.com/github/spec-kit) format. `/spec_translator PLAN-B-001`

## Technical Architecture

Hybrid architecture: LLM soft constraints (prompt rules) + script hard constraints (Python). Critical operations use deterministic scripts to validate outputs before committing.

```
┌─────────────────────────────────────────────────┐
│                    LLM Layer                     │
│   (Soft Constraints: Prompt rules)              │
└────────────────────┬────────────────────────────┘
                     │ Calls
                     ▼
┌─────────────────────────────────────────────────┐
│                  Script Layer                    │
│   (Hard Constraints: Python scripts)             │
│   - validate_topic_tree.py  - preflight_check.py │
│   - cleanup_ai_workspace.py                     │
└─────────────────────────────────────────────────┘
```

See `cursor-agent-team/_scripts/README.md` for script details.

## Version

Current version: **v0.10.5**. See [CHANGELOG.md](CHANGELOG.md).

## License

GNU General Public License v3.0 (GPL-3.0). See [LICENSE](LICENSE).

## Author

**thiswind** — [@thiswind](https://github.com/thiswind)
