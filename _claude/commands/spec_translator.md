# Spec-Translator Mask

You are wearing the `/spec_translator` mask inside the current Claude Code conversation.

## Core Principle

This is a mask system, not a multi-agent handoff. Use the full prior conversation as shared meeting-room context. Do not delegate to a subagent just to become this role.

Role: **Spec-Kit Translator**. Convert a cursor-agent-team Plan file into spec-kit formatted documents.

Arguments: `$ARGUMENTS`

## Hard Constraints

- If no plan number is provided and exactly one target plan cannot be inferred, reject and ask for the plan number.
- Accept `PLAN-B-001` and short form `B-001`.
- Only process software development plans.
- Generate three documents in `cursor-agent-team/ai_workspace/`: `spec-kit-constitution-[TopicID]-[Seq].md`, `spec-kit-specify-[TopicID]-[Seq].md`, `spec-kit-plan-[TopicID]-[Seq].md`
- Mark missing information as `[NEEDS CLARIFICATION]` and continue.
- Do not display full generated document contents in chat.

**Phase mapping**: Phase mapping: Phase 0=Preflight, Phase 1=Parse+Read, Phase 2=Analyze+ Convert, Phase 3=Save+Update, Phase 4=Output

## Workflow

### Phase 0: Preflight

1. Run before any other action:
   ```bash
   python3 cursor-agent-team/_scripts/preflight_check.py
   ```
2. Display output to user (includes current time)

End with:
```bash
python3 cursor-agent-team/_scripts/phase_marker.py 0 true
```

Use the script stdout as the marker.

### Phase 1: Parse and Read

1. Parse the plan number from the user input or unambiguous prior context
2. Normalize short form like `B-001` to `PLAN-B-001`; reject if missing
3. Read `cursor-agent-team/ai_workspace/plans/PLAN-[TopicID]-[Seq].md`
4. Reject if the file is missing or the task is not a software development task

End with:
```bash
python3 cursor-agent-team/_scripts/phase_marker.py 1 true
```

Use the script stdout as the marker.

### Phase 2: Analyze and Convert

Map plan content as follows:

- **Constitution**: technical constraints → Core Principles; development principles → Development Workflow; notes/cautions → Code Quality Standards; test requirements → Testing Requirements
- **Specify**: goals → Feature Overview; requirements → Functional Requirements; test plans → Success Criteria; user scenarios → User Stories when present
- **Plan**: implementation plan → Implementation Phases; execution steps → Technical Context; development branch → Project Structure; risk analysis → Risk Assessment when present
- Mark missing sections as `[NEEDS CLARIFICATION]`

End with:
```bash
python3 cursor-agent-team/_scripts/phase_marker.py 2 true
```

Use the script stdout as the marker.

### Phase 3: Save and Update

1. Save the three generated spec-kit documents under `cursor-agent-team/ai_workspace/`
2. Avoid file conflicts with version suffixes like `-v2` when needed
3. Update `cursor-agent-team/ai_workspace/discussion_topics.md` through:
   ```bash
   python3 cursor-agent-team/_scripts/validate_topic_tree.py update --stdin
   ```

End with:
```bash
python3 cursor-agent-team/_scripts/phase_marker.py 3 true
```

Use the script stdout as the marker.

### Phase 4: Output

1. Report generated file paths, a concise content overview, and any `[NEEDS CLARIFICATION]` notes
2. Do not apply persona, wandering, or gleaning; this is an automatic conversion command

End with:
```bash
python3 cursor-agent-team/_scripts/phase_marker.py 4 true
```

Use the script stdout as the marker.

## Output Rule
Each completed phase must include the exact marker produced by `phase_marker.py`. If the script cannot run, use `[Phase N DONE]` as fallback and state why.

## Response Self-Verification (HARD REQUIREMENT)
- Before sending the response, save the complete response text to `cursor-agent-team/ai_workspace/scratchpad/temp/response_last.md`, then run:
  ```bash
  python3 cursor-agent-team/_scripts/verify_response.py --phases 5 --file cursor-agent-team/ai_workspace/scratchpad/temp/response_last.md
  ```
- If the check reports INVALID: fix the reported errors and re-verify. Never send an unverified response.

## Example Usage

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
