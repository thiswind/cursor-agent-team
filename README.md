# Cursor AI Agent Team Framework

A three-agent collaboration system for AI-assisted work in Cursor IDE.

## Overview

This framework provides three core team roles that work together:

- **`/discuss`** - Discussion Partner (讨论伙伴): The strategist who analyzes problems, explores ideas, and creates execution plans
- **`/crew`** - Crew Member (万能打工人): The executor who implements plans strictly according to specifications
- **`/prompt_engineer`** - Prompt Engineer (提示词工程师): The HR and trainer who creates and maintains new roles (prompt templates)

With these three core roles, the team can operate and expand.

## Team Roles

### Discussion Partner (`/discuss`)
The strategist of the team. Engages in discussions, analyzes problems, explores solutions, and generates executable plans. Does not modify project files directly—only provides strategies and plans.

### Crew Member (`/crew`)
The executor of the team. Receives plans from the Discussion Partner and executes them step by step. Strictly follows plan specifications without deviation.

### Prompt Engineer (`/prompt_engineer`)
The HR and trainer of the team. Creates and maintains new roles (prompt templates) in LangGPT format. When you need a new specialized role, the Prompt Engineer helps create it.

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
讨论已经可以了，可以生成方案了
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
I need a prompt for generating figure captions
```

The Prompt Engineer creates a new role template that can be used later.

## Installation

### Step 1: Add as Git Submodule
```bash
git submodule add https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
```

### Step 2: Run Install Script
```bash
./cursor-agent-team/install.sh
```

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

Current version: **v0.1.0**

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

**thiswind**

- GitHub: [@thiswind](https://github.com/thiswind)

---

**Note**: This is the first working development version (v0.1.0). The framework is functional but may have limitations. Feedback and contributions are welcome.
