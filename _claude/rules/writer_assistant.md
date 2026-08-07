# Writer Assistant Rules

These rules extend `crew_assistant.md` for the `/writer` mask. Writer is Crew execution for prose plans with a mandatory Draft -> Review -> Final loop.

For every prose step, write a draft under `cursor-agent-team/ai_workspace/scratchpad/drafts/`, review it for slop, sentence variation, clear stance, punctuation, and deliverable fit, then write only the reviewed prose to the plan target.

Declare `general` or `academic` tier in Phase 1. Keep scratchpad process out of the final deliverable, and remind the user to perform the final human review.
