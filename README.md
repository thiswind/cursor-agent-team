<p align="center">
  <img src="logo.png" alt="cursor-agent-team: Multi-Role AI Team for Cursor" width="200">
</p>

# cursor-agent-team · Cursor AI Agent Team Framework for Multi-Role, Single-Conversation Collaboration


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18605311.svg)](https://doi.org/10.5281/zenodo.18605311)

**cursor-agent-team** is a single-conversation, multi-role framework that turns Cursor into a stable AI **agent team** for real-world development work. It gives you an opinionated way to run multiple specialized roles (architect, engineer, reviewer, etc.) inside one Cursor chat, with minimal handoff and strong context continuity.

This project is both a **methodology** and a **framework** for human–AI collaboration in Cursor: it defines how your AI team should think and work together, then ships a concrete setup (prompts + files + workflows) that you can drop into your own repo.

## OpenClaw

For **OpenClaw** (channels / CLI). This section is **separate from [Quick Start](#quick-start)** (Cursor submodule embed): that path installs the framework inside Cursor IDE; this path enables it under OpenClaw.

**`ai_workspace` (runtime workspace)** — `/discuss`, `/crew`, topic tree, inspiration capital, gleaning, etc. depend on the **`ai_workspace` directory contract**. It is **required by the architecture**, not an optional add-on. The installer **generates** the tree next to the extension and **non-destructively syncs** it to **`$OPENCLAW_WORKSPACE/ai_workspace`** (channel side). Non-interactive **`python install.py -y` does this by default**. Use **`--no-ai-workspace`** only if you explicitly want to skip writing the channel-side workspace (rare).

Copy **one** of the **For agents** blocks below in full to your assistant; use **For humans** if you run commands yourself. Requires Python 3.8+, `openclaw` on `PATH`, and a version that passes `_openclaw/install.py` checks. The script **backs up and edits** `~/.openclaw/openclaw.json`. Skip this section if you only use Cursor IDE, not OpenClaw.

### For agents

**Standard** (environment checks + clone path)

```text
Install the cursor-agent-team OpenClaw adapter on this machine, in order:

1) Ensure Python >= 3.8 and that you can run `python` in the terminal (on Windows, `py -3` may apply). Ensure `openclaw` is on PATH and its version satisfies the checks inside this repo’s `_openclaw/install.py`. If OpenClaw CLI is missing, install it from OpenClaw’s official docs first.

2) Work inside this repo’s `_openclaw` directory (`install.py` must exist there). If you have not cloned yet, run `git clone https://github.com/thiswind/cursor-agent-team.git`, then `cd cursor-agent-team/_openclaw`. If already cloned, `cd` to `<your clone root>/_openclaw` (the folder may not be named `cursor-agent-team` if you renamed or moved it).

3) Before installing, confirm the current directory is `_openclaw` (e.g. macOS/Linux: `pwd` should end with `/_openclaw`; Windows PowerShell: `Get-Location`; verify `install.py` is present).

4) From that directory run `python install.py -y`, or on Windows if `python` is missing: `py -3 install.py -y`. This backs up and edits `~/.openclaw/openclaw.json`; appends `skills.load.extraDirs` with the absolute path to this repo’s `_openclaw/skills`; merges `AGENTS.md` / `SOUL.md` templates into the OpenClaw workspace; and **by default** (non-interactive) **generates and non-destructively syncs `ai_workspace` to `$OPENCLAW_WORKSPACE/ai_workspace`** (required for the framework). To skip channel-side sync: `python install.py -y --no-ai-workspace` or `py -3 install.py -y --no-ai-workspace` (not recommended).

5) Run: `openclaw gateway restart`.

Then report: absolute path to `_openclaw`, whether `openclaw gateway restart` ran, and whether channel-side `ai_workspace` exists (e.g. check `$OPENCLAW_WORKSPACE/ai_workspace`; if unset, often `~/.openclaw/workspace/ai_workspace`). Uninstall and troubleshooting: `_openclaw/README.md` in this repo.
```

**Accelerated** (Python + `openclaw` CLI already OK)

```text
Install the cursor-agent-team OpenClaw adapter: if not cloned, `git clone https://github.com/thiswind/cursor-agent-team.git`, then `cd` to `<clone root>/_openclaw` (verify `install.py` exists), run `python install.py -y` or on Windows `py -3 install.py -y` (syncs `ai_workspace` to the OpenClaw workspace by default), then `openclaw gateway restart`. Report the absolute `_openclaw` path and whether the gateway was restarted.
```

### For humans

```bash
git clone https://github.com/thiswind/cursor-agent-team.git
cd cursor-agent-team/_openclaw
python install.py -y
openclaw gateway restart
```

On Windows if only `py` is available, use `py -3 install.py -y` for the third line (see PowerShell example in **`_openclaw/README.md`**). `-y` **by default** generates and syncs channel-side `ai_workspace`. To skip: `python install.py -y --no-ai-workspace` (not recommended). Full flags: `python install.py --help`. Uninstall / troubleshooting: **`_openclaw/README.md`**.

**Where things land**

| Location | Contents |
|----------|----------|
| Your clone root | Repo sources (including `_openclaw/skills`; after install, generated extension-side `ai_workspace`, etc.) |
| `~/.openclaw/openclaw.json` | Backed up; `skills.load.extraDirs` includes the absolute path to this repo’s `_openclaw/skills` |
| OpenClaw workspace (`$OPENCLAW_WORKSPACE`, often `~/.openclaw/workspace` by default) | Merged `AGENTS.md`, `SOUL.md`; **`ai_workspace/`** (channel-side runtime workspace, aligned with command paths) |

## Summary

cursor-agent-team takes a pragmatic approach to "multi-agent" work in Cursor: instead of spawning many separate agents and passing state around, you keep a single LLM in one conversation and let multiple roles collaborate on the same shared context window. It behaves like a small-team workflow and Cursor configuration template, not yet another generic multi-agent framework.

It is meant for developers, researchers, and advanced users who want a reliable "AI team" workflow inside Cursor, rather than a simple Q&A assistant.


## What This Is

- A workflow and methodology centered around a multi-role collaboration pattern, plus a concrete Cursor/Qwen implementation
- A single-conversation, multi-role template for AI collaboration
- A practical repo you can fork and tweak to run real projects (papers, reports, code, experiments)

## What This Is NOT

- Not a hosted SaaS or productized platform
- Not a "cover every use case" multi-agent framework
- Not an autonomous pipeline where the AI runs on its own — a human is always in the loop
- Not a plug-and-play solution for users seeking immediate productivity gains without conceptual investment

## Why cursor-agent-team?

We augment human capability; we don't replace it. Three design pillars:

1. **Multi-role, not multi-agent** — One LLM, one conversation. `/discuss` and `/crew` share the same context. No agent handoff, no context loss. Like a meeting room where everyone has perfect memory.

2. **Human-in-the-loop by design** — You are the conductor. We explore, you decide. We execute, you confirm. "Your command, our execution" — not "set and forget."

3. **Empowerment, not replacement** — Democratizing team access: individuals get team-level capability. Cognitive load redistribution: you think strategy, we handle execution details. Frees you from the "details quagmire" for purer thinking.

**Target users**: Individuals and small teams with methodological awareness—those who think about *how* they work with AI, not just *what* they want AI to do.

**We believe**: AI should augment human judgment, not replace it. Context continuity matters more than agent count. Plans grounded in fresh research beat plans from training data alone. And the human must remain in the loop—as conductor, not spectator.

## Core Model

A **multi-role collaboration framework** for Cursor IDE and Qwen Code. One LLM wears different "masks" (commands) in the same conversation. Provides:

- **Structured workflow**: discuss → plan → execute
- **Specialized roles**: Each command has distinct responsibilities
- **Hard constraint validation**: Python scripts ensure deterministic output
- **Extensible team**: Create new roles via `/prompt_engineer`

## Positioning & Related Concepts

### Concept Mapping

| Concept | Our approach |
|---------|--------------|
| **Intelligence Augmentation (IA)** | We augment human cognitive capability rather than replace it (Licklider's man-computer symbiosis; Springer 2024) |
| **Multi-role vs multi-agent** | Multi-agent systems use handoffs; context loss is a critical challenge. We avoid it by design: zero handoff, one conversation |
| **Human-AI teaming** | Human as conductor; AI roles are "masks" in the same meeting (National Academies 2022) |
| **Cognitive load redistribution** | You focus on strategy; we handle execution details (Cognitive Load Theory) |

### Compared to Adjacent Approaches

| vs | cursor-agent-team |
|----|-------------------|
| Multi-agent frameworks | No handoff, no context loss |
| Autonomous agents | Human-in-the-loop, not set-and-forget |
| Generic AI assistants | Structured roles, workflow enforcement, team metaphor |

### Positioning in the Landscape

We occupy a specific niche: **single-conversation, multi-role, context-preserving** collaboration.

| Approach | Representative | Key Difference |
|----------|---------------|----------------|
| Multi-Agent Handoff | Google ADK, Microsoft AutoGen | They optimize handoff; we eliminate it |
| Role-Playing MAS | ChatCollab, SupportPlay | Multi-instance, multi-conversation; we stay single-instance |
| Single-Model Multi-Ability | CALM | Model-level unification; we focus on workflow orchestration |
| Cursor Ecosystem | cursor-agents, cursor-rules templates | Engineering practice; we add methodology depth |

**Evaluation context**: Among single-conversation, multi-role, context-heavy approaches, cursor-agent-team is a first-tier architectural reference implementation—designed for methodological exploration, not product deployment.


## Who is this for?

cursor-agent-team is designed for developers, researchers, and advanced Cursor users who:

- Want a stable "AI team" inside a single Cursor conversation
- Care about methodology and workflow, not just ad-hoc prompts
- Are willing to spend a bit of time setting things up once, in exchange for a reusable workflow



## Quick Start

To use cursor-agent-team in Cursor:


Tell Cursor Agent:

```
Install cursor-agent-team from https://github.com/thiswind/cursor-agent-team.git as a submodule and run the install script (python cursor-agent-team/install.py).
```

Then type `/discuss` to start and briefly describe what you want to achieve (e.g., "help me design and write a technical report on X").

For manual installation or Qwen Code, see [Installation](#installation).

## Core Roles

| Role | Command | Description |
|------|---------|-------------|
| **Discussion Partner** | `/discuss` | Exploration mode — breadth and depth, no execution. Research-first planning: automatically searches for latest academic and industry research before synthesizing plans (Retrieval-augmented planning; knowledge cutoff mitigation). |
| **Crew Member** | `/crew` | Execution mode — strict adherence to plan as specification. Plan-and-Execute architecture; constrained generation. Exploitation mode. |
| **Prompt Engineer** | `/prompt_engineer` | Creates and maintains new roles (commands) |

**Research-first planning** — Plans should not come from LLM training data alone. Training data has a knowledge cutoff; plans synthesized from it can be outdated or wrong. We design `/discuss` to search for latest academic and industry research *before* synthesizing plans (retrieval-augmented planning). Fresh context, then synthesis—a methodological stance, not just a feature.

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
python cursor-agent-team/install.py
```

Update: `git submodule update --remote cursor-agent-team && python cursor-agent-team/install.py`

**Qwen Code**:

```bash
git submodule add -f https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
python cursor-agent-team/install_qwen.py
```

Update: `git submodule update --remote cursor-agent-team && python cursor-agent-team/install_qwen.py`

**Note**: The workspace at `cursor-agent-team/ai_workspace/` is shared between both platforms.

## Features

- **Single conversation, multi-role**: all roles share one context; no complex state routing or orchestration layer
- **Human-in-the-loop by design**: the workflow assumes you are present; major decisions require your confirmation
- **Hard constraints in code, soft skills in the LLM**: topic tree validation, preflight checks, and other rules live in scripts; the LLM focuses on reasoning and generation
- **Cursor-first experience**: commands and flows are designed around Cursor; no extra backend services required
- **Proven in a real research project**: the cursor-agent-team paper was written using this framework inside Cursor

### Agent Workspace

Dedicated persistent workspace for agents. Agents can write scripts, take notes, save intermediate results from searches and research. Enables staged refinement for higher output quality than direct generation. See `ai_workspace/README.md`.

### Persona System (v0.8.0+)

Script-driven persona integration with **Persona Sandboxing**: the persona expresses at the Output Layer; the Work Layer (code, analysis, reasoning) runs in a clean context. Based on [persona-spec](https://github.com/thiswind/persona-spec).

### Extended Features

- **Inspiration Capital**: Scatter card collection for sparking creativity
- **Text-to-Speech (macOS)**: Voice feedback via `say`
- **Social Media**: Integration with [Moltbook](https://moltbook.com/)
- **Spec-Kit Translator**: Converts plans to spec-kit format

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

**Architecture highlights**: Multi-role + single conversation; Plan-and-Execute; Dedicated agent workspace (context engineering, cognitive artifacts); Hybrid constraints (soft + hard); Phase markers (workflow verification); Command-as-role.

## Why This Architecture

We started from a different point than the Skills wave. Our design addresses problems that traditional rules-based and skill-based architectures cannot solve.

### Orchestration vs Capability

| Approach | Focus | What it solves |
|----------|-------|----------------|
| **Rules** | Passive constraints by scope | Code style, conventions—but cannot role-switch or orchestrate workflow |
| **Skills** | Capability modules (add-and-use) | Extend what the agent can do—but no workflow model, no join points |
| **Ours** | Orchestration-first, methodology-first | *How* humans and AI collaborate—workflow, role switching, spec-driven execution |

We define collaboration workflow; we don't just add capabilities. Command + Rules + Scripts work together: Command defines phases (join points), Rules define aspects, Scripts provide deterministic validation.

### Aspect-Oriented Design

Cross-cutting concerns (Gleaning, Wandering, Persona Output, TTS) are woven into the workflow at defined join points—not embedded in core logic. Commands define Phase/Step as join points; Rules define aspects that invoke scripts at those points. Traditional Skill architectures have no workflow model or join points; they cannot achieve this weaving.

### Spec-Script Integration

Specification (Command + mdc) drives *when* and *why* to call; scripts execute *how* with deterministic validation. This aligns with "Blueprint First, Model Second" (workflow logic in spec, LLM for bounded tasks) and Formal-LLM (hard constraints via script validation). The spec-script loop—LLM reads spec, runs script, script validates—runs in a single conversation.

### Why Cursor

Cursor provides Commands (workflow definition), Rules (aspect definition), and Agent (script execution) in one session. This tight integration enables spec-driven execution and AOP-style weaving.

**This binding is intentional.** We start with Cursor because:
- Its Rules, integrated terminal, and workspace model align naturally with our command–rules–scripts–workspace architecture
- It aggregates state-of-the-art models behind a single subscription
- Its IDE experience (interface, file tree, workspace semantics) matches our needs

We prioritize **depth on Cursor** rather than breadth of platform support. A watered-down, platform-agnostic version would lose the tight spec-script loop that makes our methodology work.

Future ports will be considered only where we can preserve the same methodological guarantees (minimal handoff, HITL, workspace semantics). This is a conscious design choice, not a limitation or oversight.

### TRAE_CN Adaptation

A [TRAE_CN](https://www.trae.com.cn/) (ByteDance) adaptation is available. See [TRAE_README.md](TRAE_README.md) for installation and usage instructions.

TRAE_CN uses custom Agents (instead of Commands), Skills (instead of mdc Rules), and a separate project rules file. The core methodology, scripts, and ai_workspace are shared across both platforms.

See `cursor-agent-team/_scripts/README.md` for script details.

### Minimal Handoff in Numbers

| Handoff Type | Context Cost | Effect |
|--------------|--------------|--------|
| State-transfer (MAS) | 50–200KB compressed state | 10–20% context retention (estimate) |
| Prompt-swap (ours) | 1–3KB rule text | Full history preserved |

We don't transfer state; we swap masks. The "Writer" knows what the "Planner" discussed because they share the same memory stream.

## Research Foundation

This repository is the reference implementation of:

> Hu, K. (2026). cursor-agent-team: A Multi-Role, Single-Conversation Framework for Human-AI Collaboration. Zenodo. https://doi.org/10.5281/zenodo.18605311

The paper itself was written using this framework inside Cursor as a dogfooding case study.

Grounded in peer-reviewed research:
- **Intelligence Augmentation**: Licklider (1960) — human-computer symbiosis
- **Lost in the Middle**: Liu et al. (2023) — context degradation in long sequences
- **Aspect-Oriented Programming**: Kiczales et al. (1997) — cross-cutting concerns separation
- **Retrieval-Augmented Planning**: RaDA, RPG — fresh information before synthesis

## Direction

See [DIRECTION.md](DIRECTION.md) for potential future directions.

We focus on methodology depth over feature breadth. No timeline commitments — the project evolves based on real needs.

## Version

Current version: **v0.13.0**. See [CHANGELOG.md](CHANGELOG.md).

## Citation

If you use cursor-agent-team in your research, please cite:

```
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

## License

GNU General Public License v3.0 (GPL-3.0). See [LICENSE](LICENSE).

## Author

**thiswind** — [@thiswind](https://github.com/thiswind)
