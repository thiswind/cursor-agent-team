# Cursor Agent Team - Crew Skill

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

## Input/Output Examples

### Input
```
@执行组员 PLAN-C-001
```

### Output
```
[Phase 0 DONE]
Role: Crew Member
Preflight check passed.

[Phase 1 DONE]
Plan: PLAN-C-001
Goal: Design and implement core features of AI collaboration framework
Steps: 5

[Phase 2 DONE]
Executing step 1: Analyze requirements
Executing step 2: Design architecture
Executing step 3: Implement core features
Executing step 4: Test functionality
Executing step 5: Write documentation

[Phase 3 DONE]
Execution completed successfully.
Plan status updated to completed.

Execution record added to discussion topic tree.
```

## Dependencies
- `cursor-agent-team/_scripts/role_identity/crew.py`
- `cursor-agent-team/_scripts/preflight_check.py`
- `cursor-agent-team/_scripts/phase_marker.py`
- `cursor-agent-team/ai_workspace/plans/`
- `cursor-agent-team/ai_workspace/discussion_topics.md`

## Notes
- Strictly follow the plan, do not deviate from plan goals
- Automatically search for solutions when encountering problems
- Update plan status and discussion records after execution
- Maintain functional consistency with Cursor version
- Follow Phase Markers output validation requirements