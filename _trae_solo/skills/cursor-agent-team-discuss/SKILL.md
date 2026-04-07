# Cursor Agent Team - Discuss Skill

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

## Execution Steps
1. **Role Declaration**: Run `python cursor-agent-team/_scripts/role_identity/discuss.py`
2. **Preflight Check**: Run `python cursor-agent-team/_scripts/preflight_check.py`
3. **Topic Management**: Read and update `cursor-agent-team/ai_workspace/discussion_topics.md`
4. **Discussion Analysis**: Analyze user problems, search for relevant information, provide analysis results
5. **Plan Generation**: If requested by user, generate execution plans and write to files
6. **Summary Output**: Run `python cursor-agent-team/_scripts/persona_output.py` to generate final output

## Input/Output Examples

### Input
```
@讨论搭档
I want to design a new AI collaboration framework, what suggestions do you have?
```

### Output
```
[Phase 0 DONE]
Role: Discussion Partner
Preflight check passed.

[Phase 1 DONE]
Topic: AI Collaboration Framework Design
Status: in_progress

[Phase 2 DONE]
I understand you want to design a new AI collaboration framework. Based on the latest research, here are some key considerations:

1. **Multi-role Collaboration**: Design different specialized roles, such as Discussion Partner, Crew Member, Prompt Engineer, etc.
2. **Workflow**: Define clear workflows, such as Discussion → Planning → Execution
3. **Context Management**: Ensure context continuity between different roles
4. **Tool Integration**: Integrate necessary tools and scripts
5. **Scalability**: Design a modular architecture to facilitate adding new features

[Phase 3 DONE]
Discussion completed. You can use @执行组员 to execute specific tasks, or @提示工程师 to create new prompt templates.
```

## Dependencies
- `cursor-agent-team/_scripts/role_identity/discuss.py`
- `cursor-agent-team/_scripts/preflight_check.py`
- `cursor-agent-team/_scripts/validate_topic_tree.py`
- `cursor-agent-team/_scripts/persona_output.py`
- `cursor-agent-team/ai_workspace/discussion_topics.md`

## Notes
- In discussion mode, do not execute operations, only provide suggestions and plans
- Serious work products (such as execution plans) must be written to files first, then notify users
- Maintain functional consistency with Cursor version
- Follow Phase Markers output validation requirements