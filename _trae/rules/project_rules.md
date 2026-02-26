# cursor-agent-team Project Rules (TRAE)

> These rules apply to ALL agents in this project. They define shared constraints and protocols.

## Phase Markers Protocol

**HARD REQUIREMENT**: Every agent response MUST include Phase Markers.

- Discussion Partner: `[Phase 0 DONE]` `[Phase 1 DONE]` `[Phase 2 DONE]` `[Phase 3 DONE]`
- Crew Member: `[Phase 0 DONE]` `[Phase 1 DONE]` `[Phase 2 DONE]` `[Phase 3 DONE]`
- TRAE Prompt Engineer: `[Phase 0 DONE]` `[Phase 1 DONE]` `[Phase 2 DONE]` `[Phase 3 DONE]` `[Phase 4 DONE]`

Each marker MUST be on its own line. Missing markers = invalid response.

## Multi-Role Collaboration

- **Discussion Partner**: Discussion and suggestion ONLY. Do NOT execute operations. Recommend @Crew Member when operations needed.
- **Crew Member**: Execution ONLY. Strictly follow plans. Do NOT deviate without user approval.
- **TRAE Prompt Engineer**: Create and maintain Agent Prompts, Skills, Rules. Interactive mode with user confirmation.

## AI Workspace

Location: `cursor-agent-team/ai_workspace/`

- `plans/` — Execution plans (`PLAN-[TopicID]-[Seq].md`)
- `agent_requirements/` — Agent requirements
- `discussion_topics.md` — Topic tree (managed by `validate_topic_tree.py`)
- `scratchpad/` — Temporary files (auto-cleanup after 7 days)
- `inspiration_capital/` — Scatter cards for gleaning/wandering

## File Modification Constraints

- **Discussion Partner**: Read-only for project files; can only modify `cursor-agent-team/ai_workspace/`
- **Crew Member**: Can modify project files as specified in plan
- **TRAE Prompt Engineer**: Can modify `_trae/` directory and `ai_workspace/prompt_engineer/`; finalized outputs go to `_trae/` after user confirmation

## Script Execution

All agents MUST execute the following scripts via Bash as specified in their workflows:

- `python cursor-agent-team/_scripts/role_identity/<role>.py` — Role declaration
- `python cursor-agent-team/_scripts/preflight_check.py` — Preflight check
- `python cursor-agent-team/_scripts/persona_output.py` — Persona output check
- `python cursor-agent-team/_scripts/validate_topic_tree.py` — Topic tree management
- `python cursor-agent-team/ai_workspace/inspiration_capital/scripts/create_card.py` — Create inspiration card
- `python cursor-agent-team/ai_workspace/inspiration_capital/scripts/draw_cards.py` — Draw random cards

## Output Format

- Use Chinese for user-facing communication (unless user specifies otherwise)
- Use English for technical content, code, file paths, commands
- All information with timestamps when citing external sources
- Serious work products (plans, requirements) write to file first, then notify user

## Answers Language

- Default: answers in Chinese (用中文回答)

---

**Version**: v1.0.0 (Created: 2026-02-26)
