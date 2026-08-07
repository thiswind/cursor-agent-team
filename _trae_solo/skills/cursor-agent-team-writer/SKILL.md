# Cursor Agent Team - Writer Skill

## Skill Name
Cursor Agent Team - Writer

## Skill Description
Executes prose plans using a mandatory Draft -> Review -> Final loop, with general and academic tiers and the shared AI workspace.

## Trigger Conditions
- User invokes `/writer` or `@writer`.
- User needs a paper, report, proposal, documentation, or other prose deliverable.

## Behavior
1. Load the selected plan and execute it in order as Crew.
2. Declare `general` or `academic` tier; use academic for submission-oriented work.
3. Write every prose draft under `cursor-agent-team/ai_workspace/scratchpad/drafts/`.
4. Review for banned AI slop, sentence variation, stance, punctuation, and fit. Academic work also checks PEEL, hedging, numbering, venues, citations, and guides.
5. Write only reviewed prose to the target and remind the user to perform final review.

Use `_trae_solo/commands/writer-config.md` for invocation setup. The shared `ai_workspace/` is the source of plans and records.
