---
name: cursor-agent-team-gleaning
description: Collect valuable insights into inspiration cards after discussions
user-invocable: false
---
When a discussion or task completes:
1. Check if there are any valuable insights, methods, or discoveries
2. If yes, run (adjust `EXT` to your `cursor-agent-team` root — often `~/.openclaw/extensions/cursor-agent-team`):
   ```bash
   python "$EXT/ai_workspace/inspiration_capital/scripts/create_card.py" \
     --source "[command or activity]" \
     --trigger "[what triggered this insight]" \
     --cards-dir "$OPENCLAW_WORKSPACE/ai_workspace/inspiration_capital/cards"
   ```
3. Create one card per insight, keep them atomic
