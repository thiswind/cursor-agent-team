#!/usr/bin/env python3
"""
Intent Recognizer for Master Agent
识别用户自然语言中的执行意图
"""

import re
from typing import Optional, Dict, List
from dataclasses import dataclass


@dataclass
class RecognizedIntent:
    role: str
    confidence: int
    matched_keywords: List[str]


class IntentRecognizer:
    def __init__(self, role_keywords: Dict[str, List[str]]):
        """
        Initialize with role -> keywords mapping
        """
        self.role_keywords = role_keywords

    def recognize(self, message: str) -> Optional[RecognizedIntent]:
        """
        Recognize intent from user message
        Returns None if no execution intent recognized -> use default /discuss
        """
        # Check for direct slash command first (highest priority)
        match = re.match(r'^/(\w+)', message.strip())
        if match:
            role = match.group(1)
            if role in self.role_keywords:
                return RecognizedIntent(
                    role=role,
                    confidence=100,
                    matched_keywords=[f"/{role}"]
                )
            elif role == 'chat':
                # /chat is for free chat, not execution intent
                return None

        # Count keyword matches for each role
        match_counts: Dict[str, List[str]] = {}
        for role, keywords in self.role_keywords.items():
            matched = []
            for kw in keywords:
                if kw.lower() in message.lower():
                    matched.append(kw)
            if matched:
                match_counts[role] = matched

        if not match_counts:
            return None

        # Find role with most matches
        best_role = max(match_counts.keys(), key=lambda r: len(match_counts[r]))
        best_matched = match_counts[best_role]

        return RecognizedIntent(
            role=best_role,
            confidence=len(best_matched),
            matched_keywords=best_matched
        )
