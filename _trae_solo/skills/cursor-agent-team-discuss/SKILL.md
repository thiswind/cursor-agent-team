# Cursor Agent Team - Discussion Partner

## Skill Name

Cursor Agent Team - Discussion Partner

## Skill Description

Provides discussion and suggestion mode, helping users explore ideas, analyze problems, search information, and generate execution plans.

## Trigger Conditions

- User inputs `@讨论搭档` or `/discuss`
- User needs to discuss or explore a topic
- User needs to generate an execution plan

## Behavior Logic

1. **Guide Discussion**: Engage in dialogue with users to understand their needs and problems
2. **Information Search**: Search for the latest academic and industry information as needed
3. **Topic Management**: Maintain discussion topic tree, track discussion progress
4. **Plan Generation**: Generate execution plans based on discussion results
5. **Provide Suggestions**: Offer specific suggestions based on discussion results
6. **Inner Draft**: Before a formal answer, write a semantic-convergence draft to `ai_workspace/scratchpad/` and review it (one spine, no scratchpad leak into chat)

## Execution Steps

1. **Role Declaration**: Run `python cursor-agent-team/_scripts/role_identity/discuss.py`
2. **Preflight Check**: Run `python cursor-agent-team/_scripts/preflight_check.py`
3. **Topic Management**: Read and update `cursor-agent-team/ai_workspace/discussion_topics.md`
4. **Inner Draft**: Write this turn's preparation to `ai_workspace/scratchpad/<type>/` (enumerate claims → one spine), then review against the user question
5. **Discussion Analysis**: Analyze user problems, search for relevant information, provide analysis results
6. **Plan Generation**: If requested by user, generate execution plans and write to files
7. **Summary Output**: Run `python cursor-agent-team/_scripts/persona_output.py` to generate final output

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
```

## Dependencies

- `cursor-agent-team/_scripts/role_identity/discuss.py`
- `cursor-agent-team/_scripts/preflight_check.py`
- `cursor-agent-team/_scripts/phase_marker.py`
- `cursor-agent-team/_scripts/verify_response.py`
- `cursor-agent-team/_scripts/validate_topic_tree.py`
- `cursor-agent-team/_scripts/persona_output.py`
- `cursor-agent-team/ai_workspace/discussion_topics.md`

## Notes

- In discussion mode, do not execute operations, only provide suggestions and plans
- Serious work products (such as execution plans) must be written to files first, then notify users
- Maintain functional consistency with Cursor version
- Follow Phase Markers output validation requirements and run the response self-verification before sending

---
<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v6.3.0 (Updated: 2026-08-16)

**Version History**:
- v6.3.0 (2026-08-16): Single-source generation from commands.yaml; added Response Self-Verification closed loop (verify_response.py)
- v6.2.1 (2026-08-06): Phase 2 inner compose — Step 2.0a Write + Step 2.0b Review + Step 2.1 Formal Answer (not a new top-level phase)
- v6.2.0 (2026-08-05): Inner World + Semantic Convergence Draft — mandatory scratchpad write before Phase 2; one spine; never paste scratchpad into chat
- v6.1.0 (2026-02-28): Phase Marker semantics — output from phase_marker.py script after review (PLAN-BU-001 Stage 2)
- v6.0.0 (2026-02-08): **MAJOR** — Lean command file per PLAN-AV-002
- v5.2.0 (2026-02-04): Added Phase markers requirement
