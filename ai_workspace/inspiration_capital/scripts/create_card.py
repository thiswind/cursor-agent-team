#!/usr/bin/env python3
"""
Create a new scatter card (散卡片) with standardized format.

Usage:
    python create_card.py --source "Moltbook" --trigger "看到一个有趣的讨论"
    
Output:
    Created: /path/to/cards/20260202_143052_001.md
"""
import os
import argparse
from datetime import datetime
from pathlib import Path


def get_next_sequence(cards_dir: str, timestamp_prefix: str) -> str:
    """Get next sequence number for given timestamp prefix."""
    existing = [f for f in os.listdir(cards_dir) 
                if f.startswith(timestamp_prefix) and f.endswith('.md')]
    return str(len(existing) + 1).zfill(3)


def create_card(cards_dir: str, source: str, trigger: str) -> str:
    """
    Create a new scatter card.
    
    Args:
        cards_dir: Directory to store cards
        source: Source of the card (e.g., "Moltbook", "网络搜索", "/discuss")
        trigger: What triggered creating this card
        
    Returns:
        Absolute path to created card file
    """
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')
    timestamp_prefix = now.strftime('%Y%m%d_%H%M%S')
    
    seq = get_next_sequence(cards_dir, timestamp_prefix)
    filename = f"{timestamp_prefix}_{seq}.md"
    filepath = os.path.join(cards_dir, filename)
    
    card_id = f"{timestamp_prefix}_{seq}"
    
    content = f"""# {card_id}

**时间**: {date_str} {time_str}
**来源**: {source}
**触发**: {trigger}

---

[内容待填写]

---

**为什么有意思**: 
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return os.path.abspath(filepath)


def main():
    parser = argparse.ArgumentParser(description='Create a new scatter card')
    parser.add_argument('--source', required=True, help='Source of the card')
    parser.add_argument('--trigger', required=True, help='What triggered this card')
    parser.add_argument('--cards-dir', default=None, 
                        help='Cards directory (default: ../cards relative to script)')
    
    args = parser.parse_args()
    
    if args.cards_dir:
        cards_dir = args.cards_dir
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        cards_dir = os.path.join(script_dir, '..', 'cards')
    
    cards_dir = os.path.abspath(cards_dir)
    os.makedirs(cards_dir, exist_ok=True)
    
    filepath = create_card(cards_dir, args.source, args.trigger)
    print(f"Created: {filepath}")


if __name__ == '__main__':
    main()
