---
name: "skill-wandering"
description: "Pre-execution aspect for exploratory discussions: draw random inspiration cards before brainstorming. Triggers ONLY for Discussion Partner in exploratory/brainstorming mode."
---

# Wandering Aspect

> Priority: This skill applies ONLY to Discussion Partner in exploratory mode.

## Purpose

Before exploratory work, randomly browse scatter cards to find potential inspiration.

## Trigger Conditions (ALL must be true)

- Agent is Discussion Partner
- Mode is exploration, brainstorming, or casual chat
- No explicit execution task is requested
- User is not asking a specific factual question

## Exclusions (CRITICAL — Never wander when)

- Crew Member — Execution requires focus, NEVER wander
- Discussion Partner with explicit task (e.g., "review this code")
- Any focused work mode
- User explicitly requests skipping inspiration phase

## Behavior

### Step 1: Draw Cards

Run the script to randomly draw 3 cards:

```bash
python cursor-agent-team/ai_workspace/inspiration_capital/scripts/draw_cards.py --count 3
```

### Step 2: Scan for Relevance

Quickly scan the drawn cards:
- Is any card potentially relevant to current discussion?
- Does any card spark an interesting connection?

### Step 3: Present (if relevant)

If any card seems relevant, briefly mention:

> "Found a potentially relevant card while wandering: [brief summary]"

If no card is relevant, proceed silently without mentioning wandering.

### Step 4: Incorporate or Skip

- If the card provides useful inspiration, incorporate it into thinking
- If not relevant, simply proceed with normal discussion

## Important

- Do NOT force connections. If nothing is relevant, that's fine.
- Do NOT spend too much time on wandering. It should be quick.
- Do NOT mention "wandering" or "inspiration" unless something useful is found.
- The goal is serendipitous discovery, not mandatory inclusion.

## When Cards Directory is Empty

If no cards exist yet, skip wandering silently and proceed normally.

---

**Version**: v1.0.0 (Created: 2026-02-26)
**Adapted from**: Cursor `_cursor/rules/wandering.mdc` v2.0.0
