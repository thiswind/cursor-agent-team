# Crew Workspace

## Directory Description

This directory is the dedicated workspace for the Crew Member (万能打工人) when using the `/crew` command.

## Purpose

The Crew uses this workspace to:
- **Record execution logs**: Track each plan execution session
- **Store research results**: Save search and research results before execution
- **Store document analysis**: Save document reading summaries
- **Record execution steps**: Track step-by-step execution progress
- **Store execution results**: Save final execution results
- **Isolate work**: Prevent conflicts with other AI agents (like `/discuss`, `/prompt_engineer`)

## Directory Structure

```
crew/
├── sessions/                    # Session directories
│   └── session_YYYYMMDD_HHMMSS/
│       ├── session_log.md      # Complete execution log
│       ├── plan.md             # Executed plan (copy for reference)
│       ├── research.md         # Search and research results
│       ├── documents.md        # Document reading summary
│       ├── execution_steps.md  # Step-by-step execution record
│       ├── results.md          # Final execution results
│       └── discussion_update.md  # Discussion record update content
└── README.md                   # This file
```

## File Naming Conventions

### Session Directories
- Format: `session_YYYYMMDD_HHMMSS/`
- Example: `session_20251229_160000/`

### Session Files
- `session_log.md` - Complete execution log
- `plan.md` - Executed plan (copy for reference)
- `research.md` - Search and research results
- `documents.md` - Document reading summary
- `execution_steps.md` - Step-by-step execution record
- `results.md` - Final execution results
- `discussion_update.md` - Discussion record update content

## Usage Rules

1. **Session-Based**: Each plan execution creates a new session directory
2. **Temporary Nature**: Files are temporary and can be cleaned periodically
3. **Isolation**: This workspace is separate from other AI workspaces
4. **Human Access**: Humans can view this workspace to understand execution process
5. **Cleanup**: Session directories can be kept for reference (suggested: 7 days)

## Cleanup Policy

- **After Execution**: Temporary files can be cleaned after execution completes
- **Session Retention**: Session directories can be kept for reference (suggested: 7 days)
- **Important Content**: Important execution results are reflected in:
  - Plan files → `00_meta/ai_workspace/plans/PLAN-XXX-XXX.md`
  - Discussion records → `00_meta/ai_workspace/discussion_topics.md`

## Relationship with Other Workspaces

- **`00_meta/ai_workspace/scratchpad/`**: Used by `/discuss` command (separate workspace)
- **`00_meta/ai_workspace/prompt_engineer/`**: Used by `/prompt_engineer` command (separate workspace)
- **`00_meta/ai_workspace/crew/`**: Used by `/crew` command (this workspace)
- **`00_meta/ai_workspace/plans/`**: Shared - stores execution plans

Each workspace is isolated to prevent conflicts between different AI agents.

## Notes

1. **Git Management**: This directory is excluded from Git (see `.gitignore`)
2. **Privacy**: Ensure no sensitive information is stored here
3. **Version Control**: Execution results are reflected in plan files and discussion records
4. **Human Review**: Humans can review this workspace to understand execution process

---

**Created**: 2025-12-29

**Last Updated**: 2025-12-29

