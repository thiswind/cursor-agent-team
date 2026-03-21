---
name: cursor-agent-team-workspace-init
description: Initialize cursor-agent-team workspace structure
user-invocable: true
command-dispatch: tool
command-tool: execute_shell
---
When user runs `/init_workspace`:

1. **Preferred (matches install.py)**: From the `cursor-agent-team` repository root (the folder that contains `_openclaw/` and `_scripts/`), run:
   ```bash
   python _openclaw/install.py -y --merge --ai-workspace
   ```
   This runs `_scripts/generate_ai_workspace.py` (output under the repo) and **non-destructively** syncs seed files into `$OPENCLAW_WORKSPACE/ai_workspace`.

2. **Manual**: Run `python _scripts/generate_ai_workspace.py` with cwd = extension/repo root, then copy missing seed files into `$OPENCLAW_WORKSPACE/ai_workspace` (same rules as install — do not delete user files).

3. Notify the user when done. Runtime data under the OpenClaw workspace must match **install sync**; extension-local `ai_workspace/` alone is not enough for channel-side tools unless documented otherwise.
