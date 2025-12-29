# Cursor AI Agent Team Framework

A three-agent collaboration system for AI-assisted work in Cursor IDE.

## Overview

The Cursor AI Agent Team Framework provides a structured approach to AI-assisted work through three specialized agents:

- **`/discuss`** - Discussion Partner (讨论伙伴): Analyzes problems, explores ideas, and generates execution plans
- **`/prompt_engineer`** - Prompt Engineer (提示词工程师): Creates and maintains LangGPT-formatted prompt templates
- **`/crew`** - Crew Member (万能打工人): Executes plans strictly according to specifications

## Features

- **Three-Agent Collaboration**: Specialized agents for different tasks
- **AI Workspace**: Dedicated workspace for AI agents to record notes, scripts, and analysis
- **Topic Tree Management**: Automatic tracking of discussion topics
- **Plan Generation**: Automatic execution plan generation from discussions
- **Workspace Isolation**: Each agent has its own isolated workspace
- **Time-Aware**: Always considers timeliness of information
- **Academic-First Search**: Prioritizes top-tier conferences and journals for academic searches

## Installation

### Step 1: Add as Git Submodule

Add the framework as a Git submodule to your project:

```bash
git submodule add https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
```

### Step 2: Run Install Script

Run the installation script to copy files to your project:

```bash
./cursor-agent-team/install.sh
```

This will:
- Copy command files to `.cursor/commands/`
- Copy rule files to `.cursor/rules/`
- Record installation information

### Update

To update to the latest version:

```bash
git submodule update --remote cursor-agent-team
./cursor-agent-team/install.sh
```

The `git submodule update --remote` command will fetch and update the submodule to the latest commit from the remote repository. Then run the install script to copy the updated files to your project.

**Alternative method** (if you prefer to be explicit):

```bash
cd cursor-agent-team
git pull origin main
cd ..
./cursor-agent-team/install.sh
```

The install script will overwrite existing files with the latest versions.

### Uninstall

To remove the framework:

```bash
./cursor-agent-team/uninstall.sh
```

This will:
- Remove all installed files
- Clean up empty directories (with confirmation)
- Ask if you want to remove the submodule

If you choose not to remove the submodule in the script, you can remove it manually later:

```bash
git submodule deinit cursor-agent-team
git rm cursor-agent-team
```

### Alternative: Direct Copy (Not Recommended)

If you prefer not to use Git submodules, you can manually copy files:

1. Copy the `.cursor/` directory to your project root
2. Ensure your project structure follows the recommended naming convention (see below)

**Note**: Using Git submodule is recommended for easier updates and maintenance.

## Directory Structure

After installation, your project structure will be:

```
project-root/
├── .cursor/                    # Installed from submodule
│   ├── commands/
│   │   ├── discuss.md
│   │   ├── prompt_engineer.md
│   │   └── crew.md
│   └── rules/
│       ├── discussion_assistant.mdc
│       ├── prompt_engineer_assistant.mdc
│       └── crew_assistant.mdc
└── cursor-agent-team/           # Git submodule
    ├── ai_workspace/           # Workspace location
    │   ├── README.md
    │   ├── plans/
    │   ├── prompt_engineer/
    │   ├── crew/
    │   └── scratchpad/
    ├── _cursor/                 # Framework source files
    ├── install.sh
    ├── uninstall.sh
    └── ...
```

**Note**: The workspace is directly located at `cursor-agent-team/ai_workspace/`. All path references in rules and commands point directly to this location.

## Workspace Directory Naming Convention

When integrating this framework into your project, we recommend using a numbered prefix system for your actual work directories:

- `00_meta/` - Metadata and configuration (framework location)
- `01_*/` - First major work section
- `02_*/` - Second major work section
- `03_*/` - Third major work section
- ... and so on

This naming convention:
- Keeps metadata separate from actual work
- Provides clear ordering
- Makes it easy to identify the purpose of each directory
- Works well with the `00_meta/` prefix for the framework

**Example structure:**
```
project-root/
├── cursor-agent-team/    # Framework (Git submodule)
│   └── ai_workspace/     # Workspace location
├── 01_method/            # Method section
├── 02_experiments/       # Experiments section
├── 03_theory/            # Theory section
└── ...
```

## Usage

### Using `/discuss`

The discussion partner helps you explore ideas, analyze problems, and generate execution plans.

```bash
/discuss
What are the latest developments in Riemannian metric learning?
```

When ready to generate an execution plan:
```bash
/discuss
讨论已经可以了，可以生成方案了
```

### Using `/prompt_engineer`

The prompt engineer creates and maintains LangGPT-formatted prompt templates.

```bash
/prompt_engineer
I need a prompt for generating figure captions
```

### Using `/crew`

The crew member executes plans generated by `/discuss`.

```bash
/crew PLAN-E-001
```

Or auto-identify the latest plan:
```bash
/crew
```

## Workflow

1. **Discuss**: Use `/discuss` to explore ideas and generate execution plans
2. **Execute**: Use `/crew` to execute plans, or use `/prompt_engineer` for prompt-related tasks
3. **Review**: Execution results are automatically recorded in discussion topics

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

See [LICENSE](LICENSE) file for details.

## Version

Current version: **v0.1.0** (First working development version)

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

**thiswind**

- GitHub: [@thiswind](https://github.com/thiswind)

## Acknowledgments

This framework was developed as part of a research project on human-AI collaboration for academic paper writing.

---

**Note**: This is the first working development version (v0.1.0). The framework is functional but may have limitations. Feedback and contributions are welcome.

