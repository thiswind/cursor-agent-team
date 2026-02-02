# AI Workspace

Private workspace for AI agents. All paths are relative to `cursor-agent-team/ai_workspace/`.

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

These files cannot be deleted without `--force` flag:

```
README.md
discussion_topics.md
plans/README.md
plans/INDEX.md
crew/README.md
prompt_engineer/README.md
agent_requirements/INDEX.md
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
| Scripts | `scratchpad/scripts/` | `script_[purpose]_YYYYMMDD_HHMMSS.[ext]` |
| Analysis | `scratchpad/analysis/` | `analysis_[topic]_YYYYMMDD_HHMMSS.md` |
| Temp | `scratchpad/temp/` | `temp_[desc]_YYYYMMDD_HHMMSS.[ext]` |
| Plans | `plans/` | `PLAN-[TopicID]-[Seq].md` |
| Requirements | `agent_requirements/` | `AGENT-REQUIREMENT-[TopicID]-[Seq].md` |

### /crew

Session directory: `crew/sessions/session_YYYYMMDD_HHMMSS/`

| File | Purpose |
|------|---------|
| `session_log.md` | Execution log |
| `plan.md` | Plan copy |
| `research.md` | Pre-execution research |
| `documents.md` | Document summary |
| `execution_steps.md` | Step-by-step record |
| `runtime_research.md` | Runtime search results |
| `results.md` | Execution results |
| `discussion_update.md` | Topic tree update content |

Workflow:
1. Read `plans/PLAN-*.md`
2. Create session in `crew/sessions/`
3. Execute and record
4. Update `discussion_topics.md`

### /prompt_engineer

Session directory: `prompt_engineer/sessions/session_YYYYMMDD_HHMMSS/`

| File | Purpose |
|------|---------|
| `mode.md` | Mode identifier |
| `target_prompt.md` | Target prompt |
| `session_log.md` | Session log |
| `requirements.md` | Requirements analysis |
| `questions.md` | Q&A record |
| `examples.md` | Behavior examples |
| `comparison.md` | Before/after comparison |
| `drafts/` | Draft files |

Final outputs go to (NOT in ai_workspace):
- `cursor-agent-team/ai_prompts/[name]_prompts.md`
- `.cursor/commands/[name].md`
- `.cursor/rules/[name]_assistant.mdc`

### /spec_translator

Session directory: `spec_translator/sessions/session_YYYYMMDD_HHMMSS/`

Output documents (in ai_workspace root):
- `spec-kit-constitution-[TopicID]-[Seq].md`
- `spec-kit-specify-[TopicID]-[Seq].md`
- `spec-kit-plan-[TopicID]-[Seq].md`

### Inspiration Capital (`inspiration_capital/`)

A "scatter card" system for collecting and browsing insights that might spark creativity.

**Key Directories:**
- `cards/` - Scatter cards storage (no categories!)
- `scripts/` - Python tools for creating and drawing cards
- `tests/` - Test cases for scripts

**Tools:**
- `create_card.py` - Create a new card with standardized format
- `draw_cards.py` - Randomly draw cards for inspiration

**Integration:**
- Used by Gleaning aspect (post-work collection)
- Used by Wandering aspect (pre-exploration browsing)

See `inspiration_capital/README.md` for details.

---

## Notes Template

Save to: `scratchpad/notes/note_[topic]_YYYYMMDD.md`

```markdown
# [Topic] Notes

Date: YYYY-MM-DD
Topic: [Related topic]

## Discoveries

1. 
2. 

## Notable Content

- 

## Thoughts

```

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Directory does not exist | Create it |
| File already exists | Append timestamp or increment sequence |
| Protected file deletion attempted | Reject unless `--force` |
| Path escape attempt (`../`) | Reject |

---

## Cleanup

Retention policy:

| Directory | Retention |
|-----------|-----------|
| `scratchpad/` | 7 days |
| `*/sessions/` | 7 days |
| `plans/` | Permanent |
| `agent_requirements/` | Permanent |
| `discussion_topics.md` | Permanent |

Cleanup command:

```bash
python cursor-agent-team/_scripts/cleanup_ai_workspace.py --older-than 7
```

Preview before cleanup:

```bash
python cursor-agent-team/_scripts/cleanup_ai_workspace.py --dry-run --older-than 7
```

---

**Last Updated**: 2026-02-02
