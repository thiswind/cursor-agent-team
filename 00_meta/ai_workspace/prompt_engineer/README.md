# Prompt Engineer Workspace

## Directory Description

This directory is the dedicated workspace for the Prompt Engineer (提示词工程师) when using the `/prompt_engineer` command.

## Purpose

The Prompt Engineer uses this workspace to:
- **Record session logs**: Track each prompt creation/maintenance session
- **Store requirements analysis**: Save requirements analysis and clarification questions
- **Generate draft files**: Create draft prompts, commands, and rules before finalization
- **Maintain comparisons**: Store before/after comparisons for prompt updates
- **Isolate work**: Prevent conflicts with other AI agents (like `/discuss`)

## Directory Structure

```
prompt_engineer/
├── sessions/                    # Session directories
│   └── session_YYYYMMDD_HHMMSS/
│       ├── mode.md             # Mode identifier (create/maintain)
│       ├── target_prompt.md    # Target prompt (maintain mode)
│       ├── session_log.md      # Session log
│       ├── requirements.md     # Requirements analysis
│       ├── questions.md        # Multiple-choice questions record
│       ├── examples.md         # Behavior examples
│       ├── comparison.md       # Before/after comparison (maintain mode)
│       ├── drafts/             # Draft files
│       │   ├── prompt_draft.md
│       │   ├── command_draft.md
│       │   └── rule_draft.md
│       └── tests/              # Test files (currently unused)
└── README.md                   # This file
```

## File Naming Conventions

### Session Directories
- Format: `session_YYYYMMDD_HHMMSS/`
- Example: `session_20251229_150530/`

### Session Files
- `mode.md` - Mode identifier (create/maintain)
- `target_prompt.md` - Existing prompt content (maintain mode)
- `session_log.md` - Complete session log
- `requirements.md` - Requirements analysis
- `questions.md` - Multiple-choice questions and answers
- `examples.md` - Behavior examples (Q&A format)
- `comparison.md` - Before/after comparison (maintain mode)

### Draft Files
- `prompt_draft.md` - Draft LangGPT-formatted prompt
- `command_draft.md` - Draft command file
- `rule_draft.md` - Draft rule file

## Usage Rules

1. **Session-Based**: Each prompt engineering session creates a new session directory
2. **Temporary Nature**: Files are temporary and cleaned after finalization
3. **Isolation**: This workspace is separate from other AI workspaces (like `scratchpad/`)
4. **Human Access**: Humans can view this workspace to understand AI's work process
5. **Cleanup**: Session directories can be kept for reference (suggested: 7 days)

## Cleanup Policy

- **After Finalization**: Temporary files are cleaned after user confirms finalization
- **Session Retention**: Session directories can be kept for reference (suggested: 7 days)
- **Important Content**: Important content is saved to permanent locations:
  - Prompt files → `00_meta/ai_prompts/`
  - Command files → `.cursor/commands/`
  - Rule files → `.cursor/rules/`

## Relationship with Other Workspaces

- **`00_meta/ai_workspace/scratchpad/`**: Used by `/discuss` command (separate workspace)
- **`00_meta/ai_workspace/discussion_topics.md`**: Used by `/discuss` command (separate file)
- **`00_meta/ai_workspace/prompt_engineer/`**: Used by `/prompt_engineer` command (this workspace)

Each workspace is isolated to prevent conflicts between different AI agents.

## Notes

1. **Git Management**: This directory is excluded from Git (see `.gitignore`)
2. **Privacy**: Ensure no sensitive information is stored here
3. **Version Control**: Finalized prompts are saved to official directories and tracked in Git
4. **Human Review**: Humans can review this workspace to understand AI's thinking process

---

**Created**: 2025-12-29

**Last Updated**: 2025-12-29

