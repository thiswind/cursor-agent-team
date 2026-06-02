# cursor-agent-team · Single-Conversation AI Team Framework

[![DOI](doi-badge.svg)](https://doi.org/10.5281/zenodo.18605311)

`cursor-agent-team` is a single-conversation, multi-role framework for working with AI in Cursor, Claude Code, and TRAE SOLO. One LLM stays in one shared context and switches role masks such as `/discuss`, `/crew`, and `/prompt_engineer`.

## Installation

<p align="center">
  <img src="logo.png" alt="cursor-agent-team logo" width="160">
</p>

Install `cursor-agent-team` inside the project where you want to use it. The recommended layout is a git submodule at `cursor-agent-team/`.

### Let an agent install it

Give your coding agent this instruction:

```text
Install cursor-agent-team into this project as a git submodule at cursor-agent-team/, then run the platform installer for my environment.

Use:
- Cursor: python3 cursor-agent-team/install.py
- Claude Code: python3 cursor-agent-team/install_claude_code.py
- TRAE SOLO: python3 cursor-agent-team/install_trae_solo.py
```

### Install manually

From the root of your project:

```bash
git submodule add -f https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
```

Then run the installer for your platform:

| Platform | Install command | What gets installed |
|----------|-----------------|---------------------|
| Cursor | `python3 cursor-agent-team/install.py` | `.cursor/commands/` and `.cursor/rules/` |
| Claude Code | `python3 cursor-agent-team/install_claude_code.py` | `.claude/commands/` mask commands |
| TRAE SOLO | `python3 cursor-agent-team/install_trae_solo.py` | `.trae/skills/` and `AGENTS.md` template |

On Windows, use `py -3` instead of `python3` if needed.

### Update

```bash
git submodule update --remote cursor-agent-team
python3 cursor-agent-team/install.py              # Cursor
python3 cursor-agent-team/install_claude_code.py  # Claude Code
python3 cursor-agent-team/install_trae_solo.py    # TRAE SOLO
```

### Uninstall installed platform files

```bash
python3 cursor-agent-team/uninstall.py --platform cursor
python3 cursor-agent-team/uninstall.py --platform claude_code
```

TRAE SOLO files can be removed from `.trae/skills/` and `AGENTS.md` manually if needed.

## What it is

<p align="center">
  <img src="banner.png" alt="cursor-agent-team meeting-room workflow" width="760">
</p>

`cursor-agent-team` is not a traditional multi-agent system. It is closer to a small meeting room: the same model remains in the same conversation, and different commands make it wear different role masks.

That means context is shared. You can discuss a plan with `/discuss`, then tell `/crew` "execute", and the execution role already knows what was discussed because it saw the same conversation.

Core roles:

| Role | Command | Purpose |
|------|---------|---------|
| Discussion Partner | `/discuss` | Explore ideas, clarify requirements, research, and generate plans |
| Crew Member | `/crew` | Execute agreed plans strictly, step by step |
| Prompt Engineer | `/prompt_engineer` | Create or maintain prompts, commands, and new role masks |
| Spec Translator | `/spec_translator` | Convert plan files into spec-kit documents |

Basic workflow:

```text
/discuss -> plan -> /crew -> execute
          |
          +-> /prompt_engineer -> new role mask
```

The shared workspace at `cursor-agent-team/ai_workspace/` stores plans, topic records, scratchpad notes, execution sessions, and other durable artifacts across supported platforms.

## Features

- **Single conversation, multiple masks**: role switching without agent handoff or context loss.
- **Human-in-the-loop workflow**: discussion, planning, execution, and expansion stay under user control.
- **Script-backed constraints**: Python scripts handle preflight checks, phase markers, topic-tree validation, cleanup, and workspace generation.
- **Shared AI workspace**: durable plans, notes, requirements, and execution records live under `cursor-agent-team/ai_workspace/`.
- **Platform adapters**: Cursor, Claude Code, and TRAE SOLO use different host mechanisms while sharing the same methodology and scripts.
- **Optional extensions**: persona output, inspiration cards, text-to-speech helpers, and spec-kit translation.

## Paper

This repository is the reference implementation of:

> Hu, K. (2026). cursor-agent-team: A Multi-Role, Single-Conversation Framework for Human-AI Collaboration. Zenodo. https://doi.org/10.5281/zenodo.18605311

The paper explains the methodology, positioning, and design rationale in more depth.

## Citation

If you use cursor-agent-team in your research, please cite:

```text
Hu, K. (2026). cursor-agent-team: A Multi-Role, Single-Conversation Framework for Human-AI Collaboration. Zenodo. https://doi.org/10.5281/zenodo.18605311
```

Or in BibTeX:

```bibtex
@article{hu2026cursor,
  author    = {Hu, Kuang},
  title     = {cursor-agent-team: A Multi-Role, Single-Conversation Framework for Human-AI Collaboration},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.18605311},
  url       = {https://doi.org/10.5281/zenodo.18605311}
}
```

## Version

Current version: **v0.16.1**. See [CHANGELOG.md](CHANGELOG.md).

## License

GNU General Public License v3.0 (GPL-3.0). See [LICENSE](LICENSE).

## Author

**thiswind** — [@thiswind](https://github.com/thiswind)
