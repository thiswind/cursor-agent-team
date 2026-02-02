# Inspiration Capital (灵感资本)

> "先有资本，后有主意"

## Overview

This system implements a "scatter card" (散卡片) collection for inspiring creativity, 
based on Da Vinci's notebook methodology and remote association theory.

## Directory Structure

```
inspiration_capital/
├── README.md           # This file
├── cards/              # Scatter cards storage (no categories!)
├── scripts/            # Python tools
│   ├── create_card.py  # Create new card
│   └── draw_cards.py   # Random draw cards
└── tests/              # Test cases
```

## Usage

### Creating a Card (for Gleaning)

```bash
python scripts/create_card.py --source "Moltbook" --trigger "看到有趣的讨论"
```

Then edit the created file to fill in `[内容待填写]` section.

### Drawing Cards (for Wandering)

```bash
python scripts/draw_cards.py --count 3
```

Output is structured text that AI can easily parse.

## Card Format

Each card is a markdown file with:
- **时间**: Creation timestamp
- **来源**: Source (Moltbook, /discuss, 网络搜索, etc.)
- **触发**: What triggered saving this
- **内容**: The actual content
- **为什么有意思**: (Optional) Why it's interesting

## Design Principles

1. **No Categories**: Keep chaos like Da Vinci
2. **Atomic**: One idea per card
3. **Low Friction**: Scripts ensure consistency
4. **Wander, Don't Search**: Random browsing sparks creativity

## Integration

This system is used by two "aspects" (AOP-style):
- **Gleaning (拾穗)**: After work completion, reflect and collect
- **Wandering (漫游)**: Before exploration, randomly browse for inspiration
