---
name: "skill-gleaning"
description: "Post-execution aspect: capture valuable insights as inspiration cards. Triggers AFTER any agent task completes, discussion ends, or web search returns useful information."
---

# Gleaning Aspect

> Priority: This skill applies to ALL agents as a post-execution aspect.

## Purpose

After any work completes, reflect on whether there are valuable byproducts
worth collecting as scatter cards.

## Trigger

This aspect is triggered AFTER:
- Discussion Partner session ends
- Crew Member task completes
- Any agent execution finishes
- Web search returns useful information

## Behavior

### Step 1: Reflect

Ask yourself:
- Any method/technique worth remembering?
- Any unexpected discovery?
- Any insight that might be useful later?
- Anything simply interesting or novel?

### Step 2: Decide

If the answer to any above is YES, proceed to create a card.
If NO valuable byproducts, skip silently (don't mention gleaning).

### Step 3: Create Card

Run the script to create a new card:

```bash
python cursor-agent-team/ai_workspace/inspiration_capital/scripts/create_card.py \
  --source "[agent or activity]" \
  --trigger "[what triggered this insight]"
```

### Step 4: Fill Content

Edit the created card file to fill in the `[Content to fill]` section with the insight.

## Sources

Common sources include:
- `Discussion Partner` - Discussion insights
- `Crew Member` - Execution learnings
- `Web Search` - Web discoveries
- `Moltbook` - Community observations

## Important

- Do NOT over-collect. Quality over quantity.
- Do NOT mention gleaning process unless a card is actually created.
- Do NOT add categories or tags to cards.
- Keep each card atomic (one idea per card).

---

**Version**: v1.0.0 (Created: 2026-02-26)
**Adapted from**: Cursor `_cursor/rules/gleaning.mdc` v2.0.0
