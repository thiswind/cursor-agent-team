#!/usr/bin/env python3
"""
Master Agent - core logic for single entry + dynamic subagent architecture
Main entry point called from AGENTS.md in OpenClaw workspace
"""

import os
import sys
import json
from typing import Optional, Tuple
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from master_agent.intent_recognizer import IntentRecognizer, RecognizedIntent
from master_agent.session_manager import SessionManager


def get_config_path() -> Path:
    """Get config file path"""
    repo_root = Path(__file__).parent.parent.parent
    return repo_root / "config" / "master_agent.json"


def load_config() -> dict:
    """Load master agent config"""
    config_path = get_config_path()
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_storage_path() -> Path:
    """Get session storage path"""
    repo_root = Path(__file__).parent.parent.parent
    return repo_root / "ai_workspace" / "crew" / "session_map.json"


def check_chat_request(message: str) -> Tuple[bool, str]:
    """Check if message starts with /chat, return (is_chat, message_without_chat)"""
    stripped = message.strip()
    if stripped.startswith('/chat '):
        return True, stripped[6:].strip()
    if stripped == '/chat':
        return True, ''
    return False, message


def handle_message():
    """
    Main entry point - called from AGENTS.md
    Reads user message from context, processes, routes to subagent
    """
    config = load_config()
    if not config.get("enabled", True):
        # Master agent disabled, do nothing
        return

    # Get user message (passed via stdin when called from command line)
    # For OpenClaw integration, we expect the message is in the conversation context
    # This entry point is called at the start of each message processing

    # 1. Initialize components
    role_keywords = {
        role: cfg.get("keywords", [])
        for role, cfg in config["sub_roles"].items()
        if cfg.get("enabled", True)
    }
    recognizer = IntentRecognizer(role_keywords)
    storage_path = get_storage_path()
    session_mgr = SessionManager(str(storage_path))

    # 2. Check for /chat
    # NOTE: In the actual OpenClaw execution flow, the message is already in context
    # This entry point is invoked at the start of processing each message
    # We check for /chat and let it go through without routing

    # For the purpose of this integration, the /chat check is handled here
    # If it's /chat, we just return early and let the normal processing continue

    # Get the current message from stdin if invoked directly
    # (for testing, not used in normal OpenClaw flow)
    if not sys.stdin.isatty():
        message = sys.stdin.read().strip()
    else:
        message = ''

    is_chat, clean_message = check_chat_request(message if message else sys.argv[1] if len(sys.argv) > 1 else '')

    if is_chat:
        # /chat only affects current message, no routing
        # Just return, the normal processing will handle it as free chat
        return

    # 3. Recognize intent
    intent = recognizer.recognize(clean_message if clean_message else message)
    if not intent:
        # No execution intent, proceed as default /discuss
        return

    # 4. Get existing session or create new
    # In OpenClaw, user_id can be extracted from chat context
    # For single user setup, we use a default user id
    user_id = os.environ.get("OPENCLAW_CURRENT_USER", "default_user")

    session_timeout = config.get("session_timeout_minutes", 30)
    existing = session_mgr.get_valid_session(user_id, intent.role, session_timeout)

    # TODO: actual spawn/reuse happens here via sessions_spawn tool call
    # For now, this module provides the structure
    # The actual tool invocation happens in the higher level flow

    # When subagent completes, it announces back to main session
    # This manager keeps the mapping for reuse

    print(f"Recognized intent: {intent.role} (confidence: {intent.confidence}, matched: {intent.matched_keywords})")
    if existing:
        print(f"Reusing existing session: {existing.session_id}")
    else:
        print("No valid existing session, will create new subagent")


if __name__ == "__main__":
    handle_message()
