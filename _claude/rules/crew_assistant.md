# Crew Assistant Rules

These rules define the base `/crew` execution mask for Claude Code. Execute the selected plan in order, preserve its goal, and record results after execution.

Use the shared `cursor-agent-team/ai_workspace/` for plans, scratchpad notes, and execution records. Run the phase marker script after each phase and use its output as the marker.

Long-document task inputs (MUST, RFC-003 read piece): decision-critical documents get the discuss read discipline — `READ-GATE: PASS|SKIP(理由)` first line, 构角 viewpoints, two-layer scan ledger `[轮N·Vi]`, convergence line (`CONVERGED: R<N>` N≥2 or `BUDGET: R<N>`), 对照表/action-items endpoint; archive under the session's `reads/<id>/`; `verify_mechanism.py read <archive>` checks the markers. Landing self-check (MUST): re-read the archive files from disk before claiming completion, append `LANDED: <archive-dir> verified-by-read-back` to the ledger; the instructed path wins over self-invented paths.
