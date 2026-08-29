# Cursor Agent Team - Workflow

## Skill Name

Cursor Agent Team - Workflow

## Skill Description

Executes PLAN-marked parallel work via cross-platform sub-agents with supervised autonomy, structured returns, and full workspace archiving.

## Trigger Conditions

- User invokes `/workflow` or `/ultra`
- A PLAN marked `Executor: workflow` needs execution with parallel fan-out

## Behavior Logic

1. **Plan Gate**: Only execute PLANs with `Executor: workflow`; otherwise recommend `/crew`
2. **Environment Detection**: Claude Code sub-agents / Cursor background tasks / TRAE runner; serial downgrade with warning if unsupported
3. **Dispatch Discipline**: every sub-agent prompt follows SUBAGENT-DISPATCH.md (mask, boundary, output contract)
4. **Verification**: orchestrator re-runs key checks; two-strikes rule on failures
5. **Wrap-up**: plan status + topic tree + gleaning + traceability report

## Execution Steps

1. **Role Declaration**: Run `python cursor-agent-team/_scripts/role_identity/workflow.py`
2. **Preflight Check**: Run `python cursor-agent-team/_scripts/preflight_check.py`
3. **Plan Preparation**: Load the workflow-marked PLAN and split into file-boundary subtasks
4. **Parallel Execution**: Dispatch, verify structured returns, resolve blockers within scope
5. **Result Recording**: update_plan_status + topic tree + promotion of staged artifacts

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

- `cursor-agent-team/_scripts/role_identity/workflow.py`
- `cursor-agent-team/_scripts/preflight_check.py`
- `cursor-agent-team/_scripts/phase_marker.py`
- `cursor-agent-team/_scripts/verify_response.py`
- `cursor-agent-team/_scripts/update_plan_status.py`
- `cursor-agent-team/_scripts/validate_topic_tree.py`
- `cursor-agent-team/ai_workspace/scratchpad/`

## Notes

- Subtasks are read-only by default; heavy writes belong to /crew
- Only structured summaries return to the main session
- Maintain functional consistency with Cursor version
- Follow Phase Markers output validation requirements and run the response self-verification before sending

---
<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v1.0.0 (Updated: 2026-08-29)

**Version History**:
- v1.0.0 (2026-08-29): Initial creation. Cross-platform /workflow executor (RFC #6): scheduler guidance in command body; read-only default; SUBAGENT-DISPATCH.md behavior layer; /ultra alias.
