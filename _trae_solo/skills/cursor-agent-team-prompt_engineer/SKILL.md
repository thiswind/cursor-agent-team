# Cursor Agent Team - Prompt Engineer

## Skill Name

Cursor Agent Team - Prompt Engineer

## Skill Description

Provides prompt engineering mode, creates and maintains LangGPT format prompt templates, supports interactive prompt design and version management.

## Trigger Conditions

- User inputs `@提示工程师` or `/prompt_engineer`
- User needs to create new prompt templates
- User needs to maintain or update existing prompt templates

## Behavior Logic

1. **Requirement Understanding**: Understand user's prompt requirements
2. **Mode Detection**: Detect whether it's create mode or maintain mode
3. **Interactive Design**: Design prompt templates through multiple rounds of interaction
4. **Version Management**: Manage prompt templates using semantic versioning
5. **File Management**: Save prompt templates to specified directories

## Execution Steps

1. **Role Declaration**: Run `python cursor-agent-team/_scripts/role_identity/prompt_engineer.py`
2. **Preflight Check**: Run `python cursor-agent-team/_scripts/preflight_check.py`
3. **Mode Detection**: Detect whether it's create mode or maintain mode
4. **Requirement Understanding**: Understand user's prompt requirements, clarify details through multiple rounds of interaction
5. **Prompt Design**: Design LangGPT format prompt templates
6. **Version Management**: Assign version numbers to prompt templates
7. **File Saving**: Save prompt templates to specified directories
8. **Record Update**: Update discussion topic execution records

## Expected Output Shape

```
[Phase 0 DONE]
...phase 0 content...
[Phase 1 DONE]
...phase 1 content...
[Phase 2 DONE]
...phase 2 content...
[Phase 3 DONE]
...phase 3 content...
[Phase 4 DONE]
...phase 4 content...
```

## Dependencies

- `cursor-agent-team/_scripts/role_identity/prompt_engineer.py`
- `cursor-agent-team/_scripts/preflight_check.py`
- `cursor-agent-team/_scripts/phase_marker.py`
- `cursor-agent-team/_scripts/verify_response.py`
- `cursor-agent-team/ai_workspace/prompt_engineer/`
- `cursor-agent-team/ai_prompts/`

## Notes

- Supports both create and maintain modes
- Uses semantic versioning for prompt templates
- Creates drafts in workspace first, then saves to official directory
- Maintain functional consistency with Cursor version
- Follow Phase Markers output validation requirements and run the response self-verification before sending

---
<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v3.2.0 (Updated: 2026-08-16)

**Version History**:
- v3.2.0 (2026-08-16): Single-source generation from commands.yaml; added Response Self-Verification closed loop (verify_response.py)
- v3.1.0 (2026-02-28): Phase Marker semantics — output from phase_marker.py script after review (PLAN-BU-001 Stage 2)
- v3.0.0 (2026-02-03): **MAJOR** - Standardized to English-only
- v2.0.0 (2026-02-03): **MAJOR REFACTOR** - Simplified Workflow from 14 steps to 5 phases
