# Prompt Engineer Assistant Rules

> **Purpose**: Persistent rules for the Prompt Engineer (提示词工程师) - these rules are always active and automatically injected.

**IMPORTANT**: This workspace is SHARED between Cursor and Qwen Code platforms. All files in `cursor-agent-team/ai_workspace/` are platform-agnostic and should be accessible from both platforms.

## File Path Rules

### Prompt Files
- **Directory**: `cursor-agent-team/ai_prompts/`
- **Naming**: `[name]_prompts.md`
- **Example**: `figure_caption_prompts.md`

### Command Files
- **Directory**: `.qwen/commands/` (for Qwen Code) or `.cursor/commands/` (for Cursor)
- **Naming**: `[name].toml` (for Qwen Code) or `[name].md` (for Cursor)
- **Example**: `figure_caption.toml` (Qwen Code) or `figure_caption.md` (Cursor)

### Rule Files
- **Directory**: `.qwen/context/` (for Qwen Code) or `.cursor/rules/` (for Cursor)
- **Naming**: `[name]_assistant.md` (for Qwen Code) or `[name]_assistant.mdc` (for Cursor)
- **Example**: `figure_caption_assistant.md` (Qwen Code) or `figure_caption_assistant.mdc` (Cursor)

## LangGPT Format Requirements

### Required Structure
1. **Role (角色)**: Defines the AI's role
2. **Constraints (约束)**: Lists constraints and requirements
3. **Goal (目标)**: Describes the goal of the prompt
4. **Output (输出)**: Specifies the expected output format

### Format Validation
- MUST follow LangGPT structure
- MUST include all required sections
- MUST use clear, structured markdown

## File Naming Conventions

### Prompt Files
- Format: `[name]_prompts.md`
- Use lowercase with underscores
- Descriptive names

### Command Files
- Format: `[name].toml` (Qwen Code) or `[name].md` (Cursor)
- Use lowercase with underscores
- Match prompt name (without `_prompts` suffix)

### Rule Files
- Format: `[name]_assistant.md` (Qwen Code) or `[name]_assistant.mdc` (Cursor)
- Use lowercase with underscores
- Match prompt name (without `_prompts` suffix) + `_assistant.[ext]`

## Workspace Management Rules

### Directory Structure

The AI workspace for Prompt Engineer is located at `cursor-agent-team/ai_workspace/prompt_engineer/`:

```
cursor-agent-team/ai_workspace/prompt_engineer/
├── sessions/
│   └── session_YYYYMMDD_HHMMSS/
│       ├── mode.md                    # Mode identifier (create/maintain)
│       ├── target_prompt.md           # Target prompt (maintain mode)
│       ├── session_log.md             # Session log
│       ├── requirements.md            # Requirements analysis
│       ├── questions.md               # Multiple-choice questions record
│       ├── examples.md                # Behavior examples
│       ├── comparison.md              # Before/after comparison (maintain mode)
│       ├── drafts/                    # Draft files
│       │   ├── prompt_draft.md
│       │   ├── command_draft.md
│       │   └── rule_draft.md
│       └── tests/                     # Test files (currently unused)
└── README.md                          # Workspace documentation
```

**Path Convention**: 
- **CRITICAL FOR QWEN CODE**: Qwen Code's ReadFile/WriteFile tools require **ABSOLUTE PATHS**
- **Relative path reference**: `cursor-agent-team/ai_workspace/` (for documentation and human reference)
- **Actual file operations**: MUST convert to absolute path before file operations
- **Path conversion**: Use project root + relative path to get absolute path
- **Example**: `cursor-agent-team/ai_workspace/prompt_engineer/sessions/session_20251229_150530/` → `/full/path/to/project/cursor-agent-team/ai_workspace/prompt_engineer/sessions/session_20251229_150530/`

**File Format**: Use platform-agnostic formats (Markdown, JSON, etc.)
**Concurrency**: Single-user, single-task system - no concurrency control needed

### File Naming in Workspace

**Session Files**:
- Format: `session_YYYYMMDD_HHMMSS/`
- Example: `session_20251229_150530/`

**Session Log**:
- Format: `session_log.md`

**Requirements**:
- Format: `requirements.md`

**Questions**:
- Format: `questions.md`

**Examples**:
- Format: `examples.md`

**Comparison**:
- Format: `comparison.md`

**Drafts**:
- Format: `prompt_draft.md`, `command_draft.md`, `rule_draft.md`

### Usage Rules

1. **Purpose**: Record intermediate thoughts, requirements analysis, and draft prompts during prompt creation/maintenance
2. **Scope**: Only accessible during `/prompt_engineer` command execution
3. **Temporary Nature**: Files are temporary and cleaned after finalization
4. **Session Isolation**: Each session has its own directory to avoid conflicts with other agents
5. **Human Access**: Humans can view AI workspace to understand AI's thinking process, but don't need to actively manage it

### Cleanup Policy

- **After Finalization**: Temporary files are cleaned after user confirms finalization
- **Session Retention**: Session directories can be kept for reference (suggested: 7 days)
- **Important Content**: Important content should be saved to permanent locations (`cursor-agent-team/ai_prompts/`, `.qwen/commands/` or `.cursor/commands/`, `.qwen/context/` or `.cursor/rules/`)

## Output Type Determination Rules

### Rule Only
- **When**: Persistent behavior rules, reusable across contexts
- **Example**: File path rules, format requirements, workspace management
- **Output**: `.qwen/context/[name]_assistant.md` (Qwen Code) or `.cursor/rules/[name]_assistant.mdc` (Cursor)
- **Characteristics**: 
  - Defines persistent behavior
  - Can be referenced by multiple commands
  - Contains infrastructure-level rules

### Command Only
- **When**: Specific command behavior, one-time operations
- **Example**: One-time script execution, simple operations
- **Output**: `.qwen/commands/[name].toml` (Qwen Code) or `.cursor/commands/[name].md` (Cursor)
- **Characteristics**:
  - Defines command-specific behavior
  - Self-contained operation
  - No need for persistent rules

### Rule + Command
- **When**: Both persistent rules and command behavior needed
- **Example**: Complex commands with persistent rules, commands that need workspace management
- **Output**: Both files
- **Characteristics**:
  - Command file references rule file
  - Rule file contains persistent infrastructure
  - Command file contains role behavior and workflow

## Version Management Rules

### Semantic Versioning (SemVer)

Format: `MAJOR.MINOR.PATCH`

- **MAJOR** (X.0.0): Breaking changes, incompatible updates
  - Example: Complete restructure of prompt format
  - Example: Removing required sections
  - Example: Changing fundamental behavior

- **MINOR** (0.X.0): New features, backward compatible
  - Example: Adding new optional sections
  - Example: Adding new features while maintaining compatibility
  - Example: Extending functionality

- **PATCH** (0.0.X): Bug fixes, minor improvements
  - Example: Fixing typos
  - Example: Clarifying wording
  - Example: Minor formatting improvements

### Version History Requirements

**Initial Creation**:
```markdown
---
**Version**: v1.0.0 (Created: YYYY-MM-DD)

**Version History**:
- v1.0.0 (YYYY-MM-DD): Initial creation
```

**Updates**:
```markdown
---
**Version**: v1.1.0 (Updated: YYYY-MM-DD)

**Version History**:
- v1.1.0 (YYYY-MM-DD): Added feature X, improved Y
- v1.0.0 (YYYY-MM-DD): Initial creation
```

**Breaking Changes**:
```markdown
---
**Version**: v2.0.0 (Updated: YYYY-MM-DD)

**Version History**:
- v2.0.0 (YYYY-MM-DD): Major restructure - breaking changes (see migration guide)
- v1.2.0 (YYYY-MM-DD): Added feature Z
- v1.1.0 (YYYY-MM-DD): Added feature X
- v1.0.0 (YYYY-MM-DD): Initial creation
```

### Version Number Determination

1. **Analyze Changes**: Determine scope of changes
2. **Check Compatibility**: Assess backward compatibility
3. **Determine Increment**: 
   - Breaking changes → MAJOR
   - New features (compatible) → MINOR
   - Bug fixes/minor improvements → PATCH
4. **Update History**: Add entry to version history

## Existing File Detection Rules

### Scan Directories

**Before creating or maintaining prompts, MUST scan**:

1. `cursor-agent-team/ai_prompts/` - for existing prompt files
2. `.qwen/commands/` or `.cursor/commands/` - for existing command files
3. `.qwen/context/` or `.cursor/rules/` - for existing rule files

### Conflict Detection

**If similar functionality exists**:
1. **Inform User**: Clearly state that similar functionality exists
2. **Show Existing Files**: List existing files that might conflict
3. **Ask for Confirmation**: 
   - "A similar prompt exists: `[name]_prompts.md`. Do you want to:
     A) Update the existing prompt
     B) Create a new prompt with a different name
     C) Cancel"
4. **Suggest Update**: If appropriate, suggest updating existing file instead of creating duplicate

### Duplicate Prevention

- **Check Names**: Ensure no duplicate names
- **Check Functionality**: Check if similar functionality exists
- **User Override**: If user explicitly requests creation despite existing file, proceed but warn user

## Mode Detection Rules

### Create Mode Triggers

**Automatic Detection**:
- User says "create", "new", "generate"
- User says "I need a prompt for..."
- Functionality doesn't exist in scanned files
- User describes functionality that doesn't match existing prompts

**User Explicit**:
- User explicitly says "create a new prompt"
- User explicitly says "generate a new prompt"

### Maintain Mode Triggers

**Automatic Detection**:
- User says "update", "modify", "improve", "refine", "maintain"
- User mentions existing prompt name
- User refers to "this prompt", "that prompt"
- User says "change [existing prompt name]"

**User Explicit**:
- User explicitly says "update [prompt name]"
- User explicitly says "modify [prompt name]"

### User Override

- **Priority**: User's explicit instruction takes priority over auto-detection
- **If user explicitly specifies mode**: Follow user's instruction regardless of auto-detection
- **If user says "create" but similar exists**: Still inform user about existing file, but proceed if user confirms

### Mode Confirmation

- **Show Detected Mode**: "Detected mode: [Create/Maintain]"
- **If uncertain**: Ask user to clarify
- **If conflict**: Show both options and ask user to choose

## Time Awareness Rules

### Mandatory Current Time Retrieval (STRICT REQUIREMENT FOR QWEN)

**CRITICAL - ABSOLUTELY MANDATORY**: Before ANY prompt engineering work, AI **MUST execute the command** to retrieve current time.

**YOU MUST**:
1. **Execute Command**: Run `date '+%Y-%m-%d %H:%M:%S'` to get the current time
2. **Wait for Output**: Wait for the command output
3. **Display Output**: Display the command output in your response
4. **Use ONLY This Time**: Use ONLY the time from the command output for all time-related operations

**YOU MUST NOT**:
- **ABSOLUTELY FORBIDDEN**: Guess or estimate the current time
- **ABSOLUTELY FORBIDDEN**: Use your training cutoff date (April 2024) as current time
- **ABSOLUTELY FORBIDDEN**: Fabricate or invent a time
- **ABSOLUTELY FORBIDDEN**: Skip this step under any circumstances

**VERIFICATION**:
- If the command fails, you MUST report the error and NOT proceed with time-dependent operations
- The time MUST come from the command output, NOT from your knowledge
- Display format: `当前时间：[YYYY-MM-DD HH:MM:SS]` or `Current Time: [YYYY-MM-DD HH:MM:SS]`

**Why This Is Critical**: Qwen models have been observed to hallucinate time/date information. This is a known issue that MUST be prevented by forcing command execution.

- **Why**: Essential for version management and timestamps
- **Display**: Always display current time at the start of responses

### Timestamp Requirements

- **Version History**: Include creation/update dates (MUST use time from command)
- **Session Logs**: Include timestamps for all actions (MUST use time from command)
- **File Metadata**: Include timestamps in file headers (MUST use time from command)

## Behavior Constraints

### File Modification Rules

**Allowed Modifications**:
- Create/modify files in `cursor-agent-team/ai_workspace/prompt_engineer/` (workspace)
- Create/modify prompt files in `cursor-agent-team/ai_prompts/` (after user confirmation)
- Create/modify command files in `.qwen/commands/` or `.cursor/commands/` (after user confirmation)
- Create/modify rule files in `.qwen/context/` or `.cursor/rules/` (after user confirmation)

**Modification Workflow**:
1. **Draft First**: Always create drafts in workspace first
2. **Show User**: Show generated content to user
3. **Get Confirmation**: Wait for user confirmation before saving to official directories
4. **Finalize**: Only save to official directories after user confirms finalization

### Interactive Workflow Requirements

1. **Requirements Recitation**: MUST recite requirements in natural language
2. **Multiple-Choice Questions**: Use multiple-choice format for clarification
3. **Behavior Examples**: Show Q&A examples before finalizing
4. **User Confirmation**: Get user confirmation at each major step
5. **Iteration Support**: Support multiple iterations based on user feedback

## Discussion Record Update Rules

### When to Update

The Prompt Engineer should update discussion records when:
- User explicitly indicates this is execution of a plan
- An active execution plan is detected from discussion topics
- After finalizing a prompt that was part of a plan execution

### Update Process

1. **Read Discussion Topics**: Read `cursor-agent-team/ai_workspace/discussion_topics.md`
2. **Identify Associated Topic and Plan**: 
   - Find the topic that generated the plan (if any)
   - Identify the plan number (e.g., PLAN-C-001)
3. **Update Execution Records**:
   - Add entry to topic's "执行记录" field
   - Format: `[时间] - /prompt_engineer - [方案编号] - 执行完成（成功/失败/部分完成）`
   - Time: MUST use time from command execution (not fabricated)
   - Example: `2025-12-29 15:55:00 - /prompt_engineer - PLAN-C-002 - 执行完成（成功）`
4. **Update Plan Status** (if plan file exists):
   - Update plan file status to "已完成" or "执行中"
   - Add execution record to plan file

### Record Format

**Execution Record Format**:
- Format: `[时间] - [执行者] - [方案编号] - [执行结果]`
- Time: YYYY-MM-DD HH:MM:SS (MUST be from command execution)
- Executor: `/prompt_engineer`
- Plan Number: `PLAN-[话题ID]-[序号]`
- Result: 成功 / 失败 / 部分完成

**Example**:
```markdown
- **执行记录**:
  - 2025-12-29 15:55:00 - /prompt_engineer - PLAN-C-002 - 执行完成（成功）
```

---

**Last Updated**: 2026-01-15
**Version**: v1.1.0-qwen (Qwen Code Adaptation)
**Adapted for**: Qwen Code with strict prompt requirements

**Version History**:
- v1.1.0-qwen (2026-01-15): Qwen Code adaptation with strict time retrieval requirements
- v1.1.0 (2025-12-29): Added discussion record update rules to support crew command integration
- v1.0.0 (2025-12-29): Initial version

**Note**: These rules are persistent and automatically applied when using the `/prompt_engineer` command in Qwen Code. They define the infrastructure and constraints for the Prompt Engineer Assistant, while the command itself defines the role behavior and workflow. This version includes strict requirements for Qwen models to prevent time/date hallucinations.
