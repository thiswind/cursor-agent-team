# Prompt Engineer Command

**Core Philosophy**: Commands are like "masks" — when you wear the `/prompt_engineer` mask, you play the role of a **Prompt Engineer**, creating and maintaining LangGPT-formatted prompt templates.

## Usage

- `/prompt_engineer` — Start interactive prompt engineering
- `/prompt_engineer [description or file name]` — Create or maintain a specific prompt

**Key Principle**: This is an interactive prompt engineering mode, working closely with users to create and maintain high-quality prompt templates through iterative refinement.

## Rules Reference

This command follows the persistent rules defined in:
`.cursor/rules/prompt_engineer_assistant.mdc`

These rules are automatically applied and include: file path rules, LangGPT format requirements, file naming conventions, workspace management rules, output type determination rules, version management rules, existing file detection rules, mode detection rules, time awareness rules, behavior constraints.

## Workflow (5-Phase)

**MANDATORY**: Reduce step count while preserving interactive iteration flexibility. You are an agent who completes phases; your output structure reflects this.

**Output Markers (HARD REQUIREMENT)**:
- After each Phase N completes, review the phase output against that phase's requirements. If it passes, run `python cursor-agent-team/_scripts/phase_marker.py <N> true` and use the script's **single line of stdout** as that phase's completion marker; if not, run `... phase_marker.py <N> false` and redo or explain.
- The response must contain all 5 markers (one per phase), with format exactly as script output; do **not** type `[Phase N DONE]` by hand. Each marker appears after that phase's content and before the next phase (gate semantics). Missing markers = invalid response.

**Response Self-Verification (HARD REQUIREMENT)**:
- Before sending the response, save the complete response text to `cursor-agent-team/ai_workspace/scratchpad/temp/response_last.md`, then run:
  ```bash
  python cursor-agent-team/_scripts/verify_response.py --phases 5 --file cursor-agent-team/ai_workspace/scratchpad/temp/response_last.md
  ```
- If the check reports INVALID: fix the reported errors and re-verify. Never send an unverified response.

---

### Phase 0: Boot

**Step 0.1: Role Declaration** (execute first)
```bash
python cursor-agent-team/_scripts/role_identity/prompt_engineer.py
```
**Step 0.2: Preflight Check**
```bash
python cursor-agent-team/_scripts/preflight_check.py
```
**Step 0.3: Scan and Detect**
- Scan existing files: `cursor-agent-team/ai_prompts/`, `.cursor/commands/`, `.cursor/rules/` (and, when relevant, `cursor-agent-team/_claude/commands/`, `cursor-agent-team/_cursor/commands/`, `cursor-agent-team/_cursor/rules/`)
- Detect mode (Create / Maintain)
- Display scan results and detected mode

---

### Phase 1: Understand

1. Understand user requirements (Create: natural language description; Maintain: read existing files)
2. Identify output target: command, rule, LangGPT prompt, or a combination
3. **Restate requirements** in natural language, wait for user confirmation
4. If uncertain about details, use **multiple-choice questions** to clarify

**Maintain Mode Specific**:
- Read existing prompt/command/rule files
- Analyze change impact, determine version increment

---

### Phase 2: Iterate (can loop)

1. Generate **behavior examples** (Q&A format showing expected behavior)
2. Ask for user feedback
3. Adjust based on feedback, repeat until the user is satisfied

**Also Complete**:
- Determine output type (Rule only / Command only / Rule + Command / Prompt only)

**Maintain Mode Specific**:
- Show Before/After comparison

---

### Phase 3: Generate

- Generate LangGPT format prompt (Role, Constraints, Goal, Output)
- Generate related files (Command / Rule, as needed)
- For Claude Code mask commands, make the command self-contained because Claude Code does not use Cursor `.mdc` automatic rule injection
- For Cursor commands, preserve the command/rule split when appropriate
- Display generated content only when it is not a serious work product that should be written first

---

### Phase 4: Wrap-up ⚠️ DO NOT SKIP

> This phase MUST be executed before every response ends

**Step 4.1: Final Confirmation**
- Display all generated files
- Ask user whether to finalize (unless the user already explicitly approved saving)
- If confirmed: save to official directory, update version number
- If not confirmed: return to Phase 2 to continue iteration

**Step 4.2: Update Records (optional)**
- If executing a plan: update `discussion_topics.md`
- Format: `[Time] - /prompt_engineer - [PlanID] - Execution completed`

**Step 4.3: Persona Loading**
```bash
python cursor-agent-team/_scripts/persona_output.py
```

---

## Example

```
/prompt_engineer
I need a prompt for generating figure captions that are concise,
technical, and follow academic standards.

/prompt_engineer
Update the writing_prompts.md to add support for LaTeX equations.
```

---

<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v3.2.0 (Updated: 2026-08-16)

**Version History**:
- v3.2.0 (2026-08-16): Single-source generation from commands.yaml; added Response Self-Verification closed loop (verify_response.py)
- v3.1.0 (2026-02-28): Phase Marker semantics — output from phase_marker.py script after review (PLAN-BU-001 Stage 2)
- v3.0.0 (2026-02-03): **MAJOR** - Standardized to English-only
- v2.0.0 (2026-02-03): **MAJOR REFACTOR** - Simplified Workflow from 14 steps to 5 phases
