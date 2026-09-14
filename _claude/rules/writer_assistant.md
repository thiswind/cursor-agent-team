# Writer Assistant Rules

These rules extend `crew_assistant.md` for the `/writer` mask. Writer is Crew execution for prose plans with a mandatory Draft -> Review -> Final loop.

For every prose step, write a draft under `cursor-agent-team/ai_workspace/scratchpad/drafts/`. Before drafting, pre-compose the sentence logic: claims in order, every explanation pre-assigned a standalone sentence slot. Review it for slop, sentence variation, clear stance, insertion structures (no mid-sentence explanatory insertions by em dash/colon/semicolon/parentheses — rewrite as standalone sentences, never just swap markers), and deliverable fit, then write only the reviewed prose to the plan target.

Declare `general` or `academic` tier in Phase 1. Keep scratchpad process out of the final deliverable, and remind the user to perform the final human review.
