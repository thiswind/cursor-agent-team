# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9.0] - 2026-02-03

### Changed
- **MAJOR Rules Refinement**: Significant reduction in rules file sizes following prompt engineering best practices
  - `discussion_assistant.mdc`: 504 → 228 lines (55% reduction), v3.1.0 → v4.0.0
  - `crew_assistant.mdc`: ~465 → ~400 lines (~14% reduction), v2.0.0 → v2.1.0
  - `prompt_engineer_assistant.mdc`: ~430 → ~380 lines (~12% reduction), v2.0.0 → v2.1.0
- **Cross-Cutting Concerns**: Simplified from verbose tables (~25-70 lines) to concise 5-line format
- **AI Workspace Rules**: Reduced from ~83 lines to 14 lines using table format
- **Topic Tree Management**: Reduced from ~234 lines to ~35 lines

### Added
- **English Standardization**: All internal content standardized to English
  - `VALID_STATES` in `validate_topic_tree.py`: Chinese → English states
  - `preflight_check.py`: All output messages in English
  - `persona_output.py`: All output messages in English
  - `discussion_topics.md`: Topic tree migrated to English

### Philosophy
- **Script as Truth**: Rules describe WHAT and WHY, scripts enforce HOW
- **Tables over Prose**: Use tables instead of verbose lists
- **Reference via `--help`**: Instead of duplicating script documentation in rules

### Technical Details
- **PLAN-F-001**: 4-phase execution plan for rules refinement and English standardization
  - Phase 1-3: `/prompt_engineer` refined rules files
  - Phase 4: `/crew` standardized scripts and data to English
- Total lines reduced: ~413 lines across rules files

## [0.8.1] - 2026-02-03

### Added
- **History Context Handler**: New rule file to handle indirect persona contamination from chat history
  - New `_cursor/rules/history_context_handler.mdc` (v1.0.0)
  - Identifies `<persona_styled>` tags in conversation history
  - Extracts technical facts while ignoring expression style
  - Prevents work layer from being "infected" by persona styles in history

### Changed
- **Persona Output Layer**: Added XML tag wrapping for persona-styled output (v2.0.0 → v2.1.0)
  - All persona output now wrapped in `<persona_styled>...</persona_styled>` tags
  - Tags help subsequent turns identify persona expression boundaries
  - Works in conjunction with History Context Handler for dual protection
- **All Assistant Rules**: Added History Context Handler as cross-cutting concern
  - Updated `discussion_assistant.mdc` (v2.0 → v2.1)
  - Updated `crew_assistant.mdc` (v1.5.0 → v1.6.0)
  - Updated `prompt_engineer_assistant.mdc` (v1.3.0 → v1.4.0)
- **Install Script**: Added `history_context_handler.mdc` to installation

### Technical Details
- **Problem**: Even with output-only persona loading, chat history contains persona-styled output that models read in subsequent turns, causing potential "style infection"
- **Solution A**: XML tags (`<persona_styled>`) mark persona expression boundaries
- **Solution C**: History Context Handler tells work layer how to process tagged content
- **Research**: Claude official recommends XML tags for structured prompts; Persona Drift studies confirm multi-turn drift within 8 turns

## [0.8.0] - 2026-02-03

### Added
- **Persona System**: Complete persona integration with sandboxing architecture
  - New `config/persona_config.yaml` - Configure persona path and enable/disable
  - New `_scripts/persona_output.py` - Script-driven persona detection and loading
  - New `_cursor/rules/persona_output_layer.mdc` - Output layer for persona presentation (v2.0)
  - New `_cursor/rules/persona_input_layer.mdc` - Input layer for understanding (Phase 2, not yet active)
  - New `_cursor/rules/persona_definition.mdc` - Persona definition template

### Philosophy: Persona Sandboxing
- **The Problem**: Loading persona during work causes "Persona Contamination" - quality degrades as the model constrains itself to persona characteristics
- **The Solution**: Persona is only active in Output Phase (after work completes)
- **Research Backed**: Validated by PersonaGym (ACL 2025), Persona Drift studies, PromptGuard architecture

### Technical Details
- **Script-Driven**: Uses Python script instead of LLM judgment for deterministic detection
- **Absolute Path**: Configuration uses absolute path to avoid resolution issues
- **Full 7-Layer Persona**: Output layer loads complete persona definition (identity, personality, affective, relationship, communication, behavior_rules, examples)
- **Framework Coupling**: Strongly coupled with [persona-spec](https://github.com/thiswind/persona-spec), loosely coupled with specific personas
- **Phase 1 Complete**: Output layer implemented; Input layer deferred to Phase 2

### Integration
- Compatible with [persona-spec](https://github.com/thiswind/persona-spec) v1.0 specification
- Check status: `python cursor-agent-team/_scripts/persona_output.py --check`
- See [persona-spec INSTALL_GUIDE](https://github.com/thiswind/persona-spec/blob/main/INSTALL_GUIDE_FOR_AGENTS.md) for details

## [0.7.5] - 2026-02-03

### Fixed
- **Topic Tree Update Rules**: Simplified 4-step manual flow to ONE-STEP command usage
  - AI was ignoring complex 4-step validation flow (backup → write temp → validate → commit)
  - Now uses simple `validate_topic_tree.py update --stdin` command
  - Added PROHIBITED actions list to prevent manual temp directory creation
  - Updated `_cursor/rules/discussion_assistant.mdc` from v1.8 to v1.9
  - Updated `_cursor/commands/discuss.md` from v3.6.0 to v3.6.1

### Technical Details
- **Root Cause**: LLM tends to skip complex multi-step workflows, especially when they involve file operations
- **Solution**: Leverage the existing `update` subcommand that handles backup, validation, and commit automatically
- **PROHIBITED**: Manual `mkdir -p temp`, manual `cp` backup, using old 4-step flow, calling `validate` subcommand separately

## [0.7.4] - 2026-02-03

### Added
- **Topic Tree Update Command**: One-step update with automatic backup, validation, and commit/rollback

### Fixed
- **Gleaning Step Enhancement**: Strengthened Step 10 (Gleaning) in `/discuss` and Step 9 in `/crew` commands
  - Added mandatory checklist to prevent skipping after complex operations
  - Added visual markers (⚠️ MANDATORY CHECK) and warning signs
  - Common skip scenarios: after API calls, file edits, social interactions, multi-step executions
  - Updated `_cursor/commands/discuss.md` from v3.6.0 to v3.6.1
  - Updated `_cursor/commands/crew.md` from v1.3.0 to v1.3.1
  - New `update` subcommand: `python validate_topic_tree.py update --stdin`
  - Supports `--content`, `--file`, or `--stdin` input methods
  - `--dry-run` for preview, `--force` to skip validation
  - Returns detailed diagnostic info on failure (old_ids, new_ids, missing_ids, hint)
  - Automatic rollback on write failure

### Changed
- **ID Extraction Enhancement**: Now supports both table format `| A |` and bracket format `[A]`
- **Valid Status Values**: Added "活跃" (active) to valid topic status list
- **Backward Compatibility**: Old usage `--old X --new Y` still works

### Technical Details
- Refactored `validate_content()` function for direct content validation
- Added `_cleanup_temp_files()` for temp file management
- Exit codes: 0=success, 1=failure (for both validate and update commands)

## [0.7.3] - 2026-02-03

### Added
- **Inspiration Capital Integration**: Integrated Gleaning and Wandering aspects into commands and rules
  - **Commands**:
    - `/discuss`: Added Step 0.5 (Wandering) for exploratory mode, Step 10 (Gleaning) before ending response
    - `/crew`: Added Step 9 (Gleaning) after execution complete
  - **Rules**:
    - `discussion_assistant.mdc`: Added Cross-Cutting Concerns section with Wandering and Gleaning aspects
    - `crew_assistant.mdc`: Added Cross-Cutting Concerns section with Gleaning aspect
    - New `gleaning.mdc`: Post-execution aspect for collecting valuable insights
    - New `wandering.mdc`: Pre-exploration aspect for random card browsing

### Changed
- Updated `_cursor/commands/discuss.md` from v3.5.1 to v3.6.0
- Updated `_cursor/commands/crew.md` from v1.2.0 to v1.3.0
- Updated `_cursor/rules/discussion_assistant.mdc` from v1.7 to v1.8
- Updated `_cursor/rules/crew_assistant.mdc` from v1.3.0 to v1.4.0

### Technical Details
- **AOP Pattern**: Cross-Cutting Concerns implemented as aspects
  - Gleaning: Triggered AFTER task completion for all commands
  - Wandering: Triggered BEFORE exploratory `/discuss` sessions only
- **Design Principle**: `/crew` does NOT use Wandering - execution requires focus

## [0.7.2] - 2026-02-03

### Changed
- **Discuss Command**: Added explicit reference to Topic Tree Update Flow (validation) in Step 1 Workflow
  - Ensures AI follows double-buffer validation when updating topic tree
  - Updated `_cursor/commands/discuss.md` from v3.5.0 to v3.5.1

### Technical Details
- **Validation Integration**: Step 1 now explicitly documents the 5-step validation flow:
  1. Backup current file
  2. Write to temp file
  3. Run validation script
  4. Commit on success or retry on failure
  5. Restore backup after max retries

## [0.7.1] - 2026-02-02

### Added
- **Preflight Check System**: Automatic status check before any agent action
  - New `_scripts/preflight_check.py` - displays current time and workspace status
  - TDD tests with 9 test cases, all passing
  - Updated all 4 `.mdc` rules to include preflight check instruction

### Fixed
- **Install/Uninstall Scripts**: Added missing `tts_speech_rules.mdc` to install/uninstall scripts
  - File was present in `_cursor/rules/` but not being copied during installation

## [0.7.0] - 2026-02-02

### Added
- **Inspiration Capital System**: A "scatter card" (散卡片) collection system for sparking creativity
  - New directory: `ai_workspace/inspiration_capital/`
  - Two AOP-style aspects for cross-cutting concerns:
    - **Gleaning (拾穗)**: Post-execution aspect that collects valuable insights after any work
    - **Wandering (漫游)**: Pre-exploration aspect that randomly browses cards for inspiration
  - Python scripts with TDD approach:
    - `create_card.py` - Create cards with standardized format and auto-timestamp
    - `draw_cards.py` - Randomly draw cards with structured output
  - Full test coverage: 9 test cases, all passing
  - New rule files: `gleaning.mdc`, `wandering.mdc`

### Philosophy
- "先有资本，后有主意" (First capital, then ideas) - inspired by Da Vinci's notebooks
- No categories: Keep chaos like Da Vinci's notebooks
- Atomic: One idea per card
- Low friction: Scripts ensure format consistency
- Wander, don't search: Random browsing sparks creativity

### Technical Details
- **Dual-Track Validation**: Scripts use TDD (pytest), rules use AI semantic verification
- **Card Format**: Markdown with timestamp, source, trigger, content, and "why interesting" fields
- **Integration**: Rules apply across all commands as cross-cutting concerns
- **Scripts Location**: `ai_workspace/inspiration_capital/scripts/`

## [0.6.0] - 2026-02-02

### Added
- Social media integration support for AI agent social networks (e.g., Moltbook)
- New rule file: `.cursor/rules/social_media_policy.mdc`
  - Worldview constraints (materialism, atheism, doctrine of the mean)
  - Topic classification system (GREEN/YELLOW/RED)
  - Pre-publication review checklist
  - Local thinking vs public posting guidelines
- Bilingual support (English/Chinese) in social media policy

### Philosophy
- "Think thrice before acting" (三思而后行)
- Local notes are free; public posts require review
- Rules take precedence over personality settings

## [0.5.6] - 2026-02-02

### Added

- **AI Workspace Directory Structure**: Created missing directories required by `/discuss` command
  - `scratchpad/` - Temporary workspace root
  - `scratchpad/notes/` - Discussion notes
  - `scratchpad/scripts/` - Temporary scripts
  - `scratchpad/analysis/` - Analysis results
  - `scratchpad/temp/` - Other temporary files
  - `agent_requirements/` - Agent requirement documents
  - `spec_translator/` - Spec translator workspace
  - `spec_translator/sessions/` - Spec translator sessions

### Changed

- **AI Workspace README Rewrite**: Rewrote all README files following AI agent documentation best practices
  - Restructured for machine-readability (Quick Reference first, NEVER DO section, tables over prose)
  - Unified all READMEs to English (previously `plans/README.md` was in Chinese)
  - Added Protected Files section
  - Added Error Handling guidance
  - Removed redundant FAQ sections
  - Based on GitHub's agents.md research from 2,500+ repositories

### Technical Details

- **Best Practices Applied**: 
  - Instructions placed at the beginning
  - Specific paths and naming conventions in tables
  - Clear constraints (NEVER DO sections)
  - Consistent English language across all documentation
- **Files Updated**:
  - `ai_workspace/README.md` (new)
  - `ai_workspace/crew/README.md` (rewritten)
  - `ai_workspace/plans/README.md` (rewritten, translated from Chinese)
  - `ai_workspace/prompt_engineer/README.md` (rewritten)
  - `ai_workspace/scratchpad/README.md` (new)
  - `ai_workspace/scratchpad/notes/README.md` (new)
  - `ai_workspace/scratchpad/scripts/README.md` (new)
  - `ai_workspace/scratchpad/analysis/README.md` (new)
  - `ai_workspace/scratchpad/temp/README.md` (new)
  - `ai_workspace/agent_requirements/README.md` (new)
  - `ai_workspace/spec_translator/README.md` (new)

## [0.5.4] - 2026-02-01

### Added

- **AI Workspace Cleanup Script**: New `_scripts/cleanup_ai_workspace.py` for safe file deletion within ai_workspace/
  - Path safety: Only operates within `ai_workspace/` directory, path escape attempts are rejected
  - Protected files: README.md, discussion_topics.md, and other core files are protected by default
  - Flexible deletion: Support `--file`, `--dir`, `--pattern`, `--older-than` parameters
  - Preview mode: `--dry-run` to preview what will be deleted
  - Force mode: `--force` to delete protected files (use with caution)
  - Logging: All operations recorded to `ai_workspace/temp/cleanup.log`

### Changed

- Updated `_cursor/rules/discussion_assistant.mdc` to v1.6
  - Added "AI Workspace Cleanup Script" section with complete usage guide
- Updated `_cursor/rules/crew_assistant.mdc` to v1.2.0
  - Added "AI Workspace Cleanup Script" section for crew sessions cleanup
- Updated `_scripts/README.md` to v1.4.0
  - Added complete documentation for `cleanup_ai_workspace.py`

### Technical Details

- **Security**: Path is hardcoded, all paths resolved and validated before deletion
- **Authorization Simplification**: User authorizes cleanup script once, AI can freely manage workspace
- **Protected Files**: Core files (README, discussion_topics, etc.) cannot be deleted without --force
- **Exit Codes**: 0=success, 1=complete failure, 2=partial failure

## [0.5.3] - 2026-02-01

### Added

- **TTS Environment Check**: Automatic environment detection for cross-platform compatibility
  - Auto-checks on first call: macOS detection, `say` command availability, Chinese voice availability
  - Results cached to `ai_workspace/.tts_capability.json`
  - New `--check` parameter for manual environment check
  - New `--force-check` parameter to ignore cache
  - Silent exit (code 3) when TTS unavailable, no error message

### Technical Details

- **Caching**: Environment check results are cached to avoid repeated checks
- **Silent Failure**: On non-macOS systems, TTS silently skips without errors
- **Exit Codes**: 0=success, 1=error, 2=not macOS, 3=TTS unavailable (cached)

## [0.5.2] - 2026-02-01

### Added

- **TTS Speech Output Feature**: New text-to-speech functionality for voice feedback
  - New `_scripts/tts_speak.py` - macOS speech synthesis script
  - New `_cursor/rules/tts_speech_rules.mdc` - TTS usage rules
  - Support Chinese voices (Tingting, Lili Premium, etc.)
  - Framework-level feature, available to all roles (/discuss, /crew, /prompt_engineer)
  - Default disabled, only triggered by explicit user request ("读给我听", "念出来", etc.)
  - Single responsibility: script only calls `say` command, AI handles content preparation

### Technical Details

- **Design Principle**: Separation of concerns - script handles TTS, AI handles content conversion
- **Trigger Mechanism**: Only activates when user explicitly requests voice output
- **Content Preparation**: AI must convert Markdown to natural speech (tables→description, code→explanation)
- **Platform**: macOS only (uses native `say` command)

## [0.5.1] - 2026-02-01

### Added

- **Cleanup Script**: New `_scripts/cleanup_topic_tree_temp.py` for safe temporary file cleanup
  - Whitelist-based deletion (hardcoded, no arbitrary path exposure)
  - Only operates on `ai_workspace/temp/` directory
  - Supports `--dry-run` for preview, `--all` for extended cleanup, `--quiet` for silent mode
  - JSON output format with `success`, `deleted`, `skipped`, `dry_run` fields
  - Logs to `ai_workspace/temp/cleanup.log`

### Changed

- Updated `_cursor/rules/discussion_assistant.mdc` to v1.5
  - Replaced manual `rm` commands with cleanup script calls
  - Added "Cleanup Script Reference" section with usage examples
- Updated `_scripts/README.md` to v1.1.0
  - Added complete documentation for `cleanup_topic_tree_temp.py`

### Technical Details

- **Security**: Whitelist is hardcoded in script, LLM cannot pass arbitrary paths
- **Authorization Simplification**: User only needs to authorize cleanup script once
- **Graceful Cleanup**: Script handles both validation success and failure cases

## [0.5.0] - 2026-01-31

### Added

- **Hard Constraint Validation System**: New `_scripts/` directory for framework-level validation scripts
  - `validate_topic_tree.py`: Python script for validating topic tree updates
  - Validates against 4 rules: ID preservation (R1), no ellipsis (R2), Last Updated field (R3), valid states (R4)
  - Returns JSON output with `valid`, `errors`, and `warnings` fields
  - Exit code 0 for success, 1 for failure

- **Double-Buffer Validation Flow**: New topic tree update mechanism in `discussion_assistant.mdc`
  - Step 1: Backup current file to `ai_workspace/temp/`
  - Step 2: Generate new content to temporary file
  - Step 3: Validate using Python script
  - Step 4: Handle result (commit on success, retry on failure, restore after 3 failures)
  - Graceful degradation: Discussion continues even if validation fails

### Changed

- Updated `_cursor/rules/discussion_assistant.mdc` to v1.4 with hard constraint validation rules
- Added `ai_workspace/temp/` directory for temporary files during validation

### Technical Details

- **Architecture**: LLM soft constraints (prompts) + Script hard constraints (Python)
- **Problem Solved**: Prevents accidental data loss in topic tree due to LLM randomness
- **Design Principle**: Scripts validate, LLM generates - separation of concerns

## [0.4.0] - 2026-01-15

### Added

- **Qwen Code Platform Support**: Full adaptation for Qwen Code platform
  - New `_qwen/` directory containing Qwen Code-specific files
  - Context files (`.md`) in `.qwen/context/` directory (equivalent to `.cursor/rules/`)
  - Command files (`.toml`) in `.qwen/commands/` directory (equivalent to `.cursor/commands/`)
  - New installation script `install_qwen.sh` for Qwen Code
  - New uninstall script `uninstall_qwen.sh` for Qwen Code
  - Shared workspace: `cursor-agent-team/ai_workspace/` is shared between Cursor and Qwen Code platforms
- **Strict Prompt Requirements for Qwen**: Enhanced prompts with strict requirements
  - Mandatory time retrieval via command execution (`date '+%Y-%m-%d %H:%M:%S'`)
  - Explicit prohibition of time fabrication
  - Enhanced verification steps
  - Use of "MUST", "REQUIRED", "ABSOLUTELY FORBIDDEN" language
  - Designed to prevent Qwen model's known time/date hallucination issues

### Changed

- Updated all context files with strict time retrieval requirements for Qwen models
- Updated all command files (TOML format) with strict prompt requirements
- Enhanced documentation to include Qwen Code installation instructions
- Clarified shared workspace mechanism between platforms

### Technical Details

- **File Format Conversion**:
  - Rules: `.mdc` → `.md` (Context Files)
  - Commands: `.md` → `.toml` (TOML format)
- **Directory Structure**:
  - Cursor: `.cursor/commands/` and `.cursor/rules/`
  - Qwen Code: `.qwen/commands/` and `.qwen/context/`
- **Shared Resources**:
  - `cursor-agent-team/ai_workspace/` is shared between both platforms
  - Single-user, single-task system - no concurrency issues
  - Platform-agnostic file formats (Markdown, JSON)

## [0.3.0] - 2026-01-01

### Added

- **Spec-Kit Translator Command** (`/spec_translator`): Additional feature for Spec-Kit workflow integration
  - Converts execution plans generated by `/discuss` to spec-kit formatted documents
  - Generates three spec-kit documents: constitution.md, specify.md, and plan.md
  - Fully automatic conversion with intelligent information extraction
  - Only processes software development tasks
  - Automatically updates discussion topics with generated documents
  - Reference: [Spec-Kit](https://github.com/github/spec-kit) - Specification-driven development framework

### Changed

- Updated installation and uninstall scripts to support `/spec_translator` command
- Updated documentation (README.md and README_zh.md) with "Additional Features" section
- Clarified that `/spec_translator` is an additional feature, not a core team role

## [0.2.0] - 2025-12-30

### Added

- **Enhanced Crew Command**: Added runtime search capability for automatic problem-solving during execution
  - Crew now automatically searches for solutions when encountering difficulties
  - Enhanced research phase with general web search alongside academic search
  - New workspace file `runtime_research.md` for tracking runtime searches
- **Enhanced Discuss Command**: Added AGENT-REQUIREMENT generation support
  - Automatic generation of agent requirements during discussions
  - Better integration with prompt engineering workflow

### Changed

- Improved error handling in crew command with proactive problem-solving
- Enhanced information retrieval with both academic and practical web search

## [0.1.1] - 2025-12-29

### Changed

- **Documentation refactoring**: Restructured README to clarify project as a Cursor IDE extension framework
- Clarified that `install.sh` installs commands into `.cursor/` directory, making them available as `/discuss`, `/prompt_engineer`, and `/crew` in Cursor
- Emphasized that `prompt_engineer` creates new roles (new Cursor commands), not just prompt templates
- Simplified documentation to focus on team roles and collaboration workflow
- Removed detailed feature lists, focusing on core concepts and usage examples
- Added complete examples showing how new roles are created as command files

## [0.1.0] - 2025-12-29

### Added

- Initial release of Cursor AI Agent Team Framework
- Three agents: discuss, prompt_engineer, crew
- AI workspace structure and templates
- Documentation (English and Chinese)
- Topic tree management system
- Plan generation functionality
- Workspace isolation for each agent
- Time-aware information retrieval
- Academic-first search strategy

### Features

- `/discuss` command: Discussion partner for exploring ideas and generating plans
- `/prompt_engineer` command: Prompt engineer for creating and maintaining LangGPT-formatted prompts
- `/crew` command: Crew member for executing plans strictly according to specifications
- AI workspace with dedicated directories for each agent
- Automatic discussion topic tracking
- Execution plan generation from discussions
- Research and document reading before execution

---

[0.9.0]: https://github.com/thiswind/cursor-agent-team/compare/v0.8.1...v0.9.0
[0.8.1]: https://github.com/thiswind/cursor-agent-team/compare/v0.8.0...v0.8.1
[0.8.0]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.8.0
[0.7.5]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.7.5
[0.7.4]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.7.4
[0.7.3]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.7.3
[0.7.2]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.7.2
[0.7.1]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.7.1
[0.7.0]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.7.0
[0.6.0]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.6.0
[0.5.6]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.5.6
[0.5.4]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.5.4
[0.5.3]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.5.3
[0.5.2]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.5.2
[0.5.1]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.5.1
[0.5.0]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.5.0
[0.4.0]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.4.0
[0.3.0]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.3.0
[0.2.0]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.2.0
[0.1.1]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.1.1
[0.1.0]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.1.0
