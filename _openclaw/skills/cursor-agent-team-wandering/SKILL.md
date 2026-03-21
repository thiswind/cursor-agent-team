---
name: cursor-agent-team-wandering
description: Draw inspiration cards for exploratory discussions
user-invocable: false
---
When starting an exploratory discussion:
1. Run `draw_cards.py` from the **extension / repo** (scripts ship under `ai_workspace/inspiration_capital/scripts/`). After `install.py --ai-workspace`, the same scripts exist under `$OPENCLAW_WORKSPACE/ai_workspace/...` — prefer that path for runtime:
   ```bash
   python "$OPENCLAW_WORKSPACE/ai_workspace/inspiration_capital/scripts/draw_cards.py" --count 3
   ```
   If the workspace copy is missing, fall back to: `python <cursor-agent-team-root>/ai_workspace/inspiration_capital/scripts/draw_cards.py --count 3`
2. Use the drawn cards as discussion inspiration
