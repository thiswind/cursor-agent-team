---
name: cursor-agent-team-phase-gate
description: Phase marker validation for 4-phase workflow
user-invocable: false
---
For all commands (/discuss, /crew, /prompt_engineer, /writer):
1. After completing each phase, run (replace `EXT` with your `cursor-agent-team` repository root):
   ```bash
   python "$EXT/_scripts/phase_marker.py" <N> true|false
   ```
2. Use the script's stdout as the phase marker
3. NEVER hand-write [Phase N DONE] markers
