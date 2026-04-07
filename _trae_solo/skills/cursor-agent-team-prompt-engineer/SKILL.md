# Cursor Agent Team - Prompt Engineer Skill

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

## Input/Output Examples

### Input
```
@提示工程师
I need a prompt template for generating technical documentation.
```

### Output
```
[Phase 0 DONE]
Role: Prompt Engineer
Preflight check passed.
Scan results: No existing technical documentation prompts found.
Detected mode: Create

[Phase 1 DONE]
Requirements restatement: Create a prompt template for generating technical documentation that is clear, structured, and follows best practices.
Confirm requirements correct? (Yes/No)

[Phase 2 DONE]
**Example**:
User: "Generate technical documentation for a Python function that calculates Fibonacci numbers"
AI: "# Technical Documentation

## Function Name
fibonacci

## Description
Calculates the nth Fibonacci number using recursion.

## Parameters
- n: int - The position in the Fibonacci sequence

## Return Value
- int - The nth Fibonacci number

## Example Usage
```python
print(fibonacci(10))  # Output: 55
```

## Complexity
- Time: O(2^n)
- Space: O(n)
```

Does this behavior meet expectations? (Yes/No/Continue iteration)

[Phase 3 DONE]
# Technical Documentation Prompt

## Role
You are a technical documentation writer specializing in software documentation.

## Constraints
- Use clear, structured format
- Include all necessary sections
- Use code examples where appropriate
- Follow industry best practices

## Goal
Generate comprehensive technical documentation for software components.

## Output
Structured technical documentation with sections for description, parameters, return values, examples, and complexity analysis.

[Phase 4 DONE]
Confirm save? (Yes/No/Continue iteration)
```

## Dependencies
- `cursor-agent-team/_scripts/role_identity/prompt_engineer.py`
- `cursor-agent-team/_scripts/preflight_check.py`
- `cursor-agent-team/_scripts/phase_marker.py`
- `cursor-agent-team/ai_workspace/prompt_engineer/`
- `cursor-agent-team/ai_prompts/`

## Notes
- Supports both create and maintain modes
- Uses semantic versioning for prompt templates
- Creates drafts in workspace first, then saves to official directory
- Maintain functional consistency with Cursor version
- Follow Phase Markers output validation requirements