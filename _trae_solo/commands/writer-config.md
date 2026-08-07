# /writer Command Configuration

## Command Name
`writer`

## Description
Writer - Execute prose plans with Draft -> Review -> Final quality control.

## Instructions
Create a command named `/writer` using the installed `cursor-agent-team-writer` skill. Pass user arguments as the plan identifier. Follow the Writer skill and four-phase Crew workflow. For prose, always create a scratchpad draft, append a review, revise until it passes, then write the reviewed final to the plan target. Keep `cursor-agent-team/ai_workspace/` shared with other platforms and do not include scratchpad process notes in deliverables.
