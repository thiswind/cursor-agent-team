<p align="center">
  <img src="logo.png" alt="Logo" width="200">
</p>

# Cursor AI Agent Team Framework

![Framework Banner](banner.png)

A lightweight multi-agent collaboration framework for Cursor IDE and Qwen Code.

## Quick Start

### Let Cursor Install It (Recommended)

Just tell Cursor Agent:

```
Install cursor-agent-team from https://github.com/thiswind/cursor-agent-team.git as a submodule and run the install script.
```

Cursor will handle everything automatically.

### Manual Installation

```bash
# 1. Add as submodule
git submodule add -f https://github.com/thiswind/cursor-agent-team.git cursor-agent-team

# 2. Install
./cursor-agent-team/install.sh

# 3. Start discussing
# Type /discuss in Cursor
```

## What is cursor-agent-team?

A **lightweight, IDE-integrated multi-agent collaboration framework** that enables multiple specialized AI agents to work together within Cursor IDE. It provides:

- **Structured workflow**: discuss → plan → execute
- **Specialized roles**: Each agent has distinct responsibilities
- **Hard constraint validation**: Python scripts ensure deterministic output
- **Extensible team**: Create new roles via `/prompt_engineer`

## Core Roles

| Role | Command | Description |
|------|---------|-------------|
| **Discussion Partner** | `/discuss` | Analyzes problems, explores ideas, creates execution plans |
| **Crew Member** | `/crew` | Executes plans strictly according to specifications |
| **Prompt Engineer** | `/prompt_engineer` | Creates and maintains new roles (commands) |

## Workflow

```
/discuss → [Explore & Plan] → /crew → [Execute] → Done
                ↓
         /prompt_engineer → [Create New Role] → Use New Command
```

1. **Plan**: Use `/discuss` to explore ideas and generate execution plans
2. **Execute**: Use `/crew` to execute the plans
3. **Expand**: Use `/prompt_engineer` to create new roles when needed

## Installation

### Cursor IDE (Agent-Assisted)

Tell Cursor Agent:

```
Install cursor-agent-team from https://github.com/thiswind/cursor-agent-team.git as a submodule and run the install script.
```

For updates, tell Cursor:

```
Update the cursor-agent-team submodule to latest and re-run install.sh
```

### Cursor IDE (Manual)

```bash
# Install
git submodule add -f https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
./cursor-agent-team/install.sh

# Update
git submodule update --remote cursor-agent-team && ./cursor-agent-team/install.sh

# Uninstall
./cursor-agent-team/uninstall.sh
```

### Qwen Code

```bash
# Install
git submodule add -f https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
./cursor-agent-team/install_qwen.sh

# Update
git submodule update --remote cursor-agent-team && ./cursor-agent-team/install_qwen.sh

# Uninstall
./cursor-agent-team/uninstall_qwen.sh
```

**Note**: The workspace at `cursor-agent-team/ai_workspace/` is shared between both platforms.

## Advanced Features

### Persona System (v0.8.0+)

Script-driven persona integration that applies personality **without degrading work quality**. Based on [persona-spec](https://github.com/thiswind/persona-spec).

```bash
# Configure in config/persona_config.yaml, then verify:
python cursor-agent-team/_scripts/persona_output.py --check
```

### Inspiration Capital (v0.7.0+)

A "scatter card" collection system for sparking creativity.

```bash
# Create card
python ai_workspace/inspiration_capital/scripts/create_card.py --source "Source" --trigger "What triggered this"

# Draw random cards
python ai_workspace/inspiration_capital/scripts/draw_cards.py --count 3
```

See `ai_workspace/inspiration_capital/README.md` for details.

### Text-to-Speech (macOS)

Voice feedback via native `say` command. Only activated when user explicitly requests ("读给我听", "read to me").

```bash
python cursor-agent-team/_scripts/tts_speak.py --check  # Check availability
```

### Social Media Integration

Integration with AI agent social networks like [Moltbook](https://moltbook.com/). See `.cursor/rules/social_media_policy.mdc` for guidelines.

### Spec-Kit Translator

Converts `/discuss` plans into [spec-kit](https://github.com/github/spec-kit) format for specification-driven development.

```
/spec_translator PLAN-B-001
```

## Technical Architecture

### Hard Constraint Validation

The framework uses a hybrid architecture combining LLM soft constraints with script hard constraints:

```
┌─────────────────────────────────────────────────┐
│                    LLM Layer                    │
│   (Soft Constraints: Prompt rules)              │
└────────────────────┬────────────────────────────┘
                     │ Calls
                     ▼
┌─────────────────────────────────────────────────┐
│                  Script Layer                   │
│   (Hard Constraints: Python scripts)            │
│   - validate_topic_tree.py                      │
│   - cleanup_ai_workspace.py                     │
│   - preflight_check.py                          │
└─────────────────────────────────────────────────┘
```

**Why**: LLM output has inherent randomness. Critical operations use deterministic Python scripts to validate outputs before committing.

**Scripts**: See `cursor-agent-team/_scripts/README.md` for details.

## License

GNU General Public License v3.0 (GPL-3.0). See [LICENSE](LICENSE).

## Version

Current version: **v0.10.0**

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

**thiswind** - [@thiswind](https://github.com/thiswind)
