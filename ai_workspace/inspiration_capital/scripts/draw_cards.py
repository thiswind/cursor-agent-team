#!/usr/bin/env python3
"""
Randomly draw scatter cards for inspiration.

Usage:
    python draw_cards.py --count 3
    
Output:
    Structured text with card contents
"""
import os
import re
import random
import argparse
from datetime import datetime
from typing import Dict, List, Any


def parse_card(filepath: str) -> Dict[str, str]:
    """Parse a card file and extract fields (supports both English and Chinese)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = {
        'filename': os.path.basename(filepath),
        'time': '',
        'source': '',
        'trigger': '',
        'content': '',
        'why_interesting': ''
    }
    
    # Time - try English first, then Chinese
    time_match = re.search(r'\*\*Time\*\*:\s*(.+)', content)
    if not time_match:
        time_match = re.search(r'\*\*时间\*\*:\s*(.+)', content)
    if time_match:
        result['time'] = time_match.group(1).strip()
    
    # Source - try English first, then Chinese
    source_match = re.search(r'\*\*Source\*\*:\s*(.+)', content)
    if not source_match:
        source_match = re.search(r'\*\*来源\*\*:\s*(.+)', content)
    if source_match:
        result['source'] = source_match.group(1).strip()
    
    # Trigger - try English first, then Chinese
    trigger_match = re.search(r'\*\*Trigger\*\*:\s*(.+)', content)
    if not trigger_match:
        trigger_match = re.search(r'\*\*触发\*\*:\s*(.+)', content)
    if trigger_match:
        result['trigger'] = trigger_match.group(1).strip()
    
    # Extract content between first and second ---
    parts = content.split('---')
    if len(parts) >= 2:
        result['content'] = parts[1].strip()
    
    # Why interesting - try English first, then Chinese
    why_match = re.search(r'\*\*Why interesting\*\*:\s*(.*?)(?:$|\n\n)', content, re.DOTALL)
    if not why_match:
        why_match = re.search(r'\*\*为什么有意思\*\*:\s*(.*?)(?:$|\n\n)', content, re.DOTALL)
    if why_match:
        result['why_interesting'] = why_match.group(1).strip()
    
    return result


def draw_cards(cards_dir: str, count: int) -> Dict[str, Any]:
    """
    Randomly draw cards from the cards directory.
    
    Args:
        cards_dir: Directory containing cards
        count: Number of cards to draw
        
    Returns:
        Dict with draw_time, count, and cards list
    """
    if not os.path.exists(cards_dir):
        return {'draw_time': datetime.now().isoformat(), 'count': 0, 'cards': []}
    
    card_files = [f for f in os.listdir(cards_dir) if f.endswith('.md')]
    
    if not card_files:
        return {'draw_time': datetime.now().isoformat(), 'count': 0, 'cards': []}
    
    # Draw random cards
    actual_count = min(count, len(card_files))
    selected = random.sample(card_files, actual_count)
    
    cards = []
    for filename in selected:
        filepath = os.path.join(cards_dir, filename)
        cards.append(parse_card(filepath))
    
    return {
        'draw_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'count': actual_count,
        'cards': cards
    }


def format_output(result: Dict[str, Any]) -> str:
    """Format draw result as structured text."""
    lines = [
        '=== Random Draw Results ===',
        f'Draw time: {result["draw_time"]}',
        f'Draw count: {result["count"]}',
        ''
    ]
    
    for i, card in enumerate(result['cards'], 1):
        lines.extend([
            f'--- Card {i}/{result["count"]} ---',
            f'File: {card["filename"]}',
            f'Time: {card["time"]}',
            f'Source: {card["source"]}',
            f'Trigger: {card["trigger"]}',
            f'Content:',
            card['content'],
            f'Why interesting: {card["why_interesting"]}',
            ''
        ])
    
    lines.append('=== End of Draw ===')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Randomly draw scatter cards')
    parser.add_argument('--count', type=int, default=3, help='Number of cards to draw')
    parser.add_argument('--cards-dir', default=None,
                        help='Cards directory (default: ../cards relative to script)')
    
    args = parser.parse_args()
    
    if args.cards_dir:
        cards_dir = args.cards_dir
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        cards_dir = os.path.join(script_dir, '..', 'cards')
    
    cards_dir = os.path.abspath(cards_dir)
    
    result = draw_cards(cards_dir, args.count)
    print(format_output(result))


if __name__ == '__main__':
    main()
