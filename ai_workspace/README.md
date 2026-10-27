# AI Workspace

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
