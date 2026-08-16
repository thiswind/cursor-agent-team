# Spec-Translator Command

**Core Philosophy**: Commands are like "masks" — when you wear the `/spec_translator` mask, you play the role of a **Spec-Kit Translator**, converting Plan files to spec-kit formatted documents.

## Usage

- `/spec_translator PLAN-B-001` - Convert specific plan
- `/spec_translator B-001` - Convert plan (auto-complete to PLAN-B-001)
- Plan number is required; the command rejects if missing.

**Key Principle**: This is a conversion mode, automatically transforming Plan files into spec-kit formatted documents. The translator is a specialized converter that extracts information from Plans and maps it to spec-kit structure.

## Rules Reference

This command follows the persistent rules defined in:
`.cursor/rules/spec_translator_assistant.mdc`

These rules are automatically applied and include: plan file reading rules, file naming rules, workspace management rules, topic tree update rules, conversion mapping rules, behavior constraints.

## Workflow (5-Phase)

**MANDATORY**: Phase mapping: Phase 0=Preflight, Phase 1=Parse+Read, Phase 2=Analyze+ Convert, Phase 3=Save+Update, Phase 4=Output

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

### Phase 0: Preflight

1. Run before any other action:
   ```bash
   python cursor-agent-team/_scripts/preflight_check.py
   ```
2. Display output to user (includes current time)

---

### Phase 1: Parse and Read

1. Parse the plan number from the user input or unambiguous prior context
2. Normalize short form like `B-001` to `PLAN-B-001`; reject if missing
3. Read `cursor-agent-team/ai_workspace/plans/PLAN-[TopicID]-[Seq].md`
4. Reject if the file is missing or the task is not a software development task

---

### Phase 2: Analyze and Convert

Map plan content as follows:

- **Constitution**: technical constraints → Core Principles; development principles → Development Workflow; notes/cautions → Code Quality Standards; test requirements → Testing Requirements
- **Specify**: goals → Feature Overview; requirements → Functional Requirements; test plans → Success Criteria; user scenarios → User Stories when present
- **Plan**: implementation plan → Implementation Phases; execution steps → Technical Context; development branch → Project Structure; risk analysis → Risk Assessment when present
- Mark missing sections as `[NEEDS CLARIFICATION]`

---

### Phase 3: Save and Update

1. Save the three generated spec-kit documents under `cursor-agent-team/ai_workspace/`
2. Avoid file conflicts with version suffixes like `-v2` when needed
3. Update `cursor-agent-team/ai_workspace/discussion_topics.md` through:
   ```bash
   python cursor-agent-team/_scripts/validate_topic_tree.py update --stdin
   ```

---

### Phase 4: Output

1. Report generated file paths, a concise content overview, and any `[NEEDS CLARIFICATION]` notes
2. Do not apply persona, wandering, or gleaning; this is an automatic conversion command

---

## Example

```
/spec_translator PLAN-B-001
*Note: Converts PLAN-B-001 to three spec-kit documents*
```

---

<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v2.2.0 (Updated: 2026-08-16)

**Version History**:
- v2.2.0 (2026-08-16): Single-source generation from commands.yaml; added Response Self-Verification closed loop (verify_response.py)
- v2.1.0 (2026-02-28): Phase Marker semantics — output from phase_marker.py script after review (PLAN-BU-001 Stage 2)
- v2.0.0 (2026-02-03): **MAJOR** - Standardized to English-only
- v1.0.0 (2026-01-01): Initial creation - Spec-Kit Translator command
