# Cursor AI Agent Team Framework

A three-agent collaboration system for Cursor IDE that installs custom commands and enables team expansion.

## Overview

This framework installs three core Cursor commands (roles) into your project:

- **`/discuss`** - Discussion Partner (讨论伙伴): The strategist who analyzes problems, explores ideas, and creates execution plans
- **`/crew`** - Crew Member (万能打工人): The executor who implements plans strictly according to specifications
- **`/prompt_engineer`** - Prompt Engineer (提示词工程师): The HR and trainer who creates new roles (new Cursor commands)

With these three core roles installed, the team can operate. The Prompt Engineer can create additional roles as needed, allowing the team to expand.

## Team Roles

### Discussion Partner (`/discuss`)
The strategist. Engages in discussions, analyzes problems, explores solutions, and generates executable plans. Does not modify project files directly—only provides strategies and plans.

### Crew Member (`/crew`)
The executor. Receives plans from the Discussion Partner and executes them step by step. Strictly follows plan specifications without deviation.

### Prompt Engineer (`/prompt_engineer`)
The HR and trainer. Creates and maintains new roles (Cursor commands). When you need a new specialized role, the Prompt Engineer helps create it as a new command file and rule file.

## Workflow

1. **Plan**: Use `/discuss` to explore ideas and generate execution plans
2. **Execute**: Use `/crew` to execute the plans
3. **Expand**: Use `/prompt_engineer` to create new roles when needed

## Usage Example

### Step 1: Discuss and Plan
```
/discuss
I want to add a new section about computational complexity to the paper. 
What should be included?
```

After discussion, generate a plan:
```
/discuss
The discussion is ready, please generate the execution plan
```

The Discussion Partner generates a plan: `PLAN-A-001`

### Step 2: Execute the Plan
```
/crew PLAN-A-001
```

The Crew Member executes the plan step by step.

### Step 3: Create New Roles (Optional)
If you need a specialized role for a specific task:
```
/prompt_engineer
I need a role for generating figure captions
```

The Prompt Engineer creates:
- `.cursor/commands/figure_caption.md` - A new command `/figure_caption`
- `.cursor/rules/figure_caption_assistant.mdc` - Rules for this role

You can now use `/figure_caption` in Cursor, just like the three core commands.

## Installation

### Step 1: Add as Git Submodule
```bash
git submodule add https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
```

### Step 2: Run Install Script
```bash
./cursor-agent-team/install.sh
```

This installs the three core commands into `.cursor/commands/` and rules into `.cursor/rules/`.

### Update
```bash
git submodule update --remote cursor-agent-team
./cursor-agent-team/install.sh
```

### Uninstall
```bash
./cursor-agent-team/uninstall.sh
```

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

See [LICENSE](LICENSE) file for details.

## Version

Current version: **v0.1.1**

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

**thiswind**

- GitHub: [@thiswind](https://github.com/thiswind)

---

**Note**: This is the first working development version (v0.1.0). The framework is functional but may have limitations. Feedback and contributions are welcome.
