#!/usr/bin/env python3
"""
Session Manager for Master Agent
Maintains (user_id, role) -> session_id mapping with persistence
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class SessionInfo:
    session_id: str
    session_key: str
    create_time: str  # ISO format
    last_active_time: str  # ISO format


class SessionManager:
    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.sessions: Dict[str, Dict[str, SessionInfo]] = {}
        self._load()

    def _load(self):
        """Load session mapping from disk"""
        if not self.storage_path.exists():
            self.sessions = {}
            return

        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.sessions = {}
                for user_id, roles in data.items():
                    self.sessions[user_id] = {}
                    for role, info in roles.items():
                        self.sessions[user_id][role] = SessionInfo(**info)
        except (json.JSONDecodeError, KeyError):
            self.sessions = {}

    def _save(self):
        """Save session mapping to disk"""
        data = {}
        for user_id, roles in self.sessions.items():
            data[user_id] = {}
            for role, info in roles.items():
                data[user_id][role] = asdict(info)

        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_valid_session(self, user_id: str, role: str, timeout_minutes: int) -> Optional[SessionInfo]:
        """Get a valid (non-expired) session if exists"""
        if user_id not in self.sessions:
            return None
        if role not in self.sessions[user_id]:
            return None

        info = self.sessions[user_id][role]

        # Check timeout
        last_active = datetime.fromisoformat(info.last_active_time)
        timeout = timedelta(minutes=timeout_minutes)
        if datetime.now() - last_active > timeout:
            # Expired, remove it
            del self.sessions[user_id][role]
            self._save()
            return None

        return info

    def update_session(self, user_id: str, role: str, session_id: str, session_key: str):
        """Add or update a session"""
        now = datetime.now().isoformat()
        if user_id not in self.sessions:
            self.sessions[user_id] = {}

        if user_id in self.sessions and role in self.sessions[user_id]:
            # Update existing
            existing = self.sessions[user_id][role]
            existing.last_active_time = now
        else:
            # Create new
            self.sessions[user_id][role] = SessionInfo(
                session_id=session_id,
                session_key=session_key,
                create_time=now,
                last_active_time=now
            )

        self._save()

    def remove_session(self, user_id: str, role: str):
        """Remove a specific session"""
        if user_id in self.sessions and role in self.sessions[user_id]:
            del self.sessions[user_id][role]
            self._save()
