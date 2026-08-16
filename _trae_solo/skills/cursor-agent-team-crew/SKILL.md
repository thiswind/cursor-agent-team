# Cursor Agent Team - Crew Member

## Skill Name

Cursor Agent Team - Crew Member

## Skill Description

Provides execution mode, strictly follows plans to execute tasks, automatically searches for solutions, and ensures task completion.

## Trigger Conditions

- User inputs `@执行组员` or `/crew`
- User needs to execute specific tasks or plans
- User needs automatic solution searching

## Behavior Logic

1. **Plan Identification**: Identify and load the plan to execute
2. **Task Execution**: Execute tasks according to plan steps
3. **Problem Solving**: Automatically search for solutions when encountering problems
4. **Result Recording**: Record execution results and process
5. **Summary Reporting**: Provide execution summary and recommendations

## Execution Steps

1. **Role Declaration**: Run `python cursor-agent-team/_scripts/role_identity/crew.py`
2. **Preflight Check**: Run `python cursor-agent-team/_scripts/preflight_check.py`
3. **Plan Preparation**: Read plan files in `cursor-agent-team/ai_workspace/plans/`
4. **Task Execution**: Execute tasks according to plan steps, automatically search for solutions when encountering problems
5. **Result Recording**: Update plan status and discussion topic execution records
6. **Summary Output**: Provide execution summary and recommendations

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

- `cursor-agent-team/_scripts/role_identity/crew.py`
- `cursor-agent-team/_scripts/preflight_check.py`
- `cursor-agent-team/_scripts/phase_marker.py`
- `cursor-agent-team/_scripts/verify_response.py`
- `cursor-agent-team/_scripts/update_plan_status.py`
- `cursor-agent-team/ai_workspace/plans/`
- `cursor-agent-team/ai_workspace/discussion_topics.md`

## Notes

- Strictly follow the plan, do not deviate from plan goals
- Automatically search for solutions when encountering problems
- Update plan status and discussion records after execution
- Maintain functional consistency with Cursor version
- Follow Phase Markers output validation requirements and run the response self-verification before sending

---
<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v4.2.0 (Updated: 2026-08-16)

**Version History**:
- v4.2.0 (2026-08-16): Single-source generation from commands.yaml; added Response Self-Verification closed loop (verify_response.py)
- v4.1.0 (2026-02-28): Phase Marker semantics — output from phase_marker.py script after review (PLAN-BU-001 Stage 2)
- v4.0.0 (2026-02-08): **MAJOR** — Lean command file per PLAN-AV-002
- v3.0.0 (2026-02-03): **MAJOR** — Standardized to English-only
