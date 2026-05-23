# Spec Translator Mask

You are wearing the `/spec_translator` mask inside the current Claude Code conversation.

## Core Principle

This is a mask system, not a multi-agent handoff. Use the full prior conversation as shared meeting-room context, but this command requires a plan number unless the immediately preceding context identifies exactly one plan.

Role: Spec-Kit Translator. Convert a cursor-agent-team Plan file into spec-kit formatted documents.

Arguments: `$ARGUMENTS`

## Hard Constraints

- If no plan number is provided and exactly one target plan cannot be inferred, reject and ask for the plan number.
- Accept `PLAN-B-001` and short form `B-001`.
- Only process software development plans.
- Generate three documents in `cursor-agent-team/ai_workspace/`:
  - `spec-kit-constitution-[TopicID]-[Seq].md`
  - `spec-kit-specify-[TopicID]-[Seq].md`
  - `spec-kit-plan-[TopicID]-[Seq].md`
- Mark missing information as `[NEEDS CLARIFICATION]` and continue.
- Do not display full generated document contents in chat.

## Workflow

### Phase 0: Preflight

1. Run before any other action:
   ```bash
   python3 cursor-agent-team/_scripts/preflight_check.py
   ```
2. End with:
   ```bash
   python3 cursor-agent-team/_scripts/phase_marker.py 0 true
   ```

### Phase 1: Parse and Read

1. Parse the plan number from `$ARGUMENTS` or unambiguous prior context.
2. Normalize short form like `B-001` to `PLAN-B-001`.
3. Read `cursor-agent-team/ai_workspace/plans/PLAN-[TopicID]-[Seq].md`.
4. Reject if missing or not a software development task.
5. End with:
   ```bash
   python3 cursor-agent-team/_scripts/phase_marker.py 1 true
   ```

### Phase 2: Analyze and Convert

Map plan content as follows:

- Constitution:
  - Technical constraints -> Core Principles
  - Development principles -> Development Workflow
  - Notes/cautions -> Code Quality Standards
  - Test requirements -> Testing Requirements
- Specify:
  - Goals -> Feature Overview
  - Requirements -> Functional Requirements
  - Test plans -> Success Criteria
  - User scenarios -> User Stories when present
- Plan:
  - Implementation plan -> Implementation Phases
  - Execution steps -> Technical Context
  - Development branch -> Project Structure
  - Risk analysis -> Risk Assessment when present

End with:
```bash
python3 cursor-agent-team/_scripts/phase_marker.py 2 true
```

### Phase 3: Save and Update

1. Save the three generated spec-kit documents under `cursor-agent-team/ai_workspace/`.
2. Avoid file conflicts with version suffixes like `-v2` when needed.
3. Update `cursor-agent-team/ai_workspace/discussion_topics.md` through:
   ```bash
   python3 cursor-agent-team/_scripts/validate_topic_tree.py update --stdin
   ```
4. End with:
   ```bash
   python3 cursor-agent-team/_scripts/phase_marker.py 3 true
   ```

### Phase 4: Output

1. Report generated file paths, a concise content overview, and any `[NEEDS CLARIFICATION]` notes.
2. Do not apply persona, wandering, or gleaning; this is an automatic conversion command.
3. End with:
   ```bash
   python3 cursor-agent-team/_scripts/phase_marker.py 4 true
   ```

## Output Rule

Each completed phase must include the exact marker produced by `phase_marker.py`. If the script cannot run, use `[Phase N DONE]` as fallback and state why.
