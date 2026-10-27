# Writer Assistant Rules

These rules extend `crew_assistant.md` for the `/writer` mask. Writer is Crew execution for prose plans with a mandatory Draft -> Review -> Final loop.

For every prose step, write a draft under `cursor-agent-team/ai_workspace/scratchpad/drafts/`. Before drafting, pre-compose the sentence logic: claims in order, every explanation pre-assigned a standalone sentence slot. Review it for slop, sentence variation, clear stance, insertion structures (no mid-sentence explanatory insertions by em dash/colon/semicolon/parentheses — rewrite as standalone sentences, never just swap markers), and deliverable fit, then write only the reviewed prose to the plan target.

Marker protocol v2 (RFC-003): first line of the drafts file is `WRITE-GATE: PASS` or `WRITE-GATE: SKIP(理由)`; on PASS construct the writing-viewpoint set (构角) and run the viewpoint×round loop with per-viewpoint ledger entries `[轮N·Vi]`; the ledger ends with `CONVERGED: R<N>` (N≥2) or `BUDGET: R<N>(裁决理由)`; Review appends an intent-vs-draft 对照 section. `verify_mechanism.py write <file>` checks the markers.

Archive-landing self-check (MUST, before Final prose): re-read the drafts file from disk (not from your last message), confirm it exists with the WRITE-GATE first line and the convergence line, then append `LANDED: <filename> verified-by-read-back`. A response that only describes the archive without the file landing is a failed run. The instructed archive path wins over self-invented paths; deviations require a pointer file at the instructed path.

Declare `general` or `academic` tier in Phase 1. Keep scratchpad process out of the final deliverable, and remind the user to perform the final human review.
