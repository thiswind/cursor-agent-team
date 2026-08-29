# cursor-agent-team · Single-Conversation AI Team Framework

[![DOI](doi-badge.svg)](https://doi.org/10.5281/zenodo.18605311)

> **Frontier-model agents**: read [`AGENTS-GUIDE.md`](AGENTS-GUIDE.md) first — self-assemble personas, scripts, and ai_workspace without slash commands.

---

**The problem with multi-agent systems:** every time one agent hands off to another, the receiving agent starts cold — it only knows what you explicitly passed. Context bleeds. Plans drift. You end up re-explaining yourself.

**cursor-agent-team takes a different approach:** one model, one shared conversation, multiple role masks. Switch from planning to execution to prompt engineering without ever losing context — because everyone in the "meeting room" was there for the whole conversation.

```
/discuss  →  plan agreed  →  /crew execute  →  done
                 ↑
           /writer  →  prose compose loop
           /prompt_engineer  →  new role mask
```

> Supported platforms: **Cursor** · **Claude Code** · **TRAE SOLO**

---

## Quick Start (3 steps)

```bash
# 1. Add as submodule inside your project
git submodule add https://github.com/thiswind/cursor-agent-team.git cursor-agent-team

# 2. Install for your platform
python3 cursor-agent-team/install.py              # Cursor
python3 cursor-agent-team/install_claude_code.py  # Claude Code
python3 cursor-agent-team/install_trae_solo.py    # TRAE SOLO

# 3. In your AI chat, type /discuss and start
```

Or let your agent do it:

```text
Install cursor-agent-team into this project as a git submodule at cursor-agent-team/,
then run the platform installer for my environment.
```

---

## How it works

`cursor-agent-team` is not a traditional multi-agent system. Think of it as a small meeting room: the same model stays in the same conversation, and slash commands make it wear different role masks.

That means context is always shared. `/crew` already knows what `/discuss` planned — because it was in the same conversation.

| Role | Command | Purpose |
|------|---------|-------|
| Discussion Partner | `/discuss` | Explore ideas, clarify requirements, research, generate plans |
| Crew Member | `/crew` | Execute agreed plans strictly, step by step |
| Writer | `/writer` | Execute prose plans with Draft -> Review -> Final quality control |
| Prompt Engineer | `/prompt_engineer` | Create or maintain prompts, commands, new role masks |
| Spec Translator | `/spec_translator` | Convert plan files into spec-kit documents |

---

## Features

- **Single conversation, multiple masks** — role switching without agent handoff or context loss
- **Human-in-the-loop** — discussion, planning, execution, and expansion stay under user control
- **Shared AI workspace** — durable plans, notes, requirements, and execution records in `cursor-agent-team/ai_workspace/`
- **Script-backed constraints** — Python scripts handle preflight checks, phase markers, topic-tree validation, and workspace generation
- **Closed-loop verification** — `verify_response.py` machine-checks that every response carries all phase markers before it is sent
- **Platform adapters** — Cursor, Claude Code, and TRAE SOLO share the same methodology and scripts
- **Optional extensions** — persona output, inspiration cards, TTS helpers, spec-kit translation

---

## Maintaining commands (single source)

All role commands are generated from one source of truth — never hand-edit
`_cursor/commands/`, `_claude/commands/`, or `_trae_solo/` artifacts:

```bash
# 1. Edit semantics in commands.yaml (roles, phases, constraints, history)
# 2. Regenerate all platform artifacts
python3 _scripts/build_commands.py
# 3. Verify no drift (use in CI)
python3 _scripts/build_commands.py --check
```

The generated commands embed two hard contracts: the **phase marker**
requirement (`phase_marker.py`) and the **response self-verification** step
(`verify_response.py`), so every platform gets them for free.

---

## Installation

### Let an agent install it

```text
Install cursor-agent-team into this project as a git submodule at cursor-agent-team/,
then run the platform installer for my environment.

Use:
- Cursor: python3 cursor-agent-team/install.py
- Claude Code: python3 cursor-agent-team/install_claude_code.py
- TRAE SOLO: python3 cursor-agent-team/install_trae_solo.py
```

### Manual install

```bash
git submodule add -f https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
```

| Platform | Install command | What gets installed |
|----------|-----------------|---------------------|
| Cursor | `python3 cursor-agent-team/install.py` | `.cursor/commands/` and `.cursor/rules/` |
| Claude Code | `python3 cursor-agent-team/install_claude_code.py` | `.claude/commands/` mask commands and `.claude/rules/` Writer rules |
| TRAE SOLO | `python3 cursor-agent-team/install_trae_solo.py` | `.trae/skills/` including Writer and an `AGENTS.md` template only when absent |

On Windows, use `py -3` instead of `python3`.

### Update

```bash
git submodule update --remote cursor-agent-team
python3 cursor-agent-team/install.py              # Cursor
python3 cursor-agent-team/install_claude_code.py  # Claude Code
python3 cursor-agent-team/install_trae_solo.py    # TRAE SOLO
```

### Uninstall

```bash
python3 cursor-agent-team/uninstall.py --platform cursor
python3 cursor-agent-team/uninstall.py --platform claude_code
python3 cursor-agent-team/uninstall.py --platform trae_solo
```

TRAE SOLO uninstall is recorded-file-only and safe for user-owned `AGENTS.md`:

```bash
python3 cursor-agent-team/uninstall.py --platform trae_solo
```

The submodule remains unless `--remove-submodule` is explicitly passed. Empty adapter directories are removed only when empty.

---

## Visual overview

<p align="center">
  <img src="logo.png" alt="cursor-agent-team logo" width="160">
</p>

<p align="center">
  <img src="banner.png" alt="cursor-agent-team meeting-room workflow" width="760">
</p>

---

## Paper

This repository is the reference implementation of:

> Hu, K. (2026). *cursor-agent-team: A Multi-Role, Single-Conversation Framework for Human-AI Collaboration*. Zenodo. https://doi.org/10.5281/zenodo.18605311

## Citation

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

---

## Version

Current version: **v0.20.0** — see [CHANGELOG.md](CHANGELOG.md).

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE).

## Author

**thiswind** — [@thiswind](https://github.com/thiswind)
