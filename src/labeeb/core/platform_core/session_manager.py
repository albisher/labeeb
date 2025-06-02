"""
Session Manager for Labeeb

Provides atomic session management operations in a platform-agnostic way.

---
description: Atomic session management tool
inputs: [action, session_id]
outputs: [success, sessions, error]
dependencies: []
alwaysApply: false
---
"""

from typing import List, Dict, Any, Optional

class SessionManager:
    """Platform-agnostic session manager."""

    def __init__(self):
        self.sessions = []

    def start_session(self, session_id: str) -> Dict[str, Any]:
        """
        Start a new session.
        Args:
            session_id (str): The session identifier
        Returns:
            dict: {"success": bool, "error": str}
        """
        if session_id in self.sessions:
            return {"success": False, "error": "Session already exists"}
        self.sessions.append(session_id)
        return {"success": True, "error": None}

    def stop_session(self, session_id: str) -> Dict[str, Any]:
        """
        Stop an existing session.
        Args:
            session_id (str): The session identifier
        Returns:
            dict: {"success": bool, "error": str}
        """
        if session_id not in self.sessions:
            return {"success": False, "error": "Session not found"}
        self.sessions.remove(session_id)
        return {"success": True, "error": None}

    def list_sessions(self) -> Dict[str, Any]:
        """
        List all active sessions.
        Returns:
            dict: {"sessions": list, "error": str}
        """
        return {"sessions": self.sessions, "error": None}

# Usage Example:
# mgr = SessionManager()
# print(mgr.start_session("abc123"))
# print(mgr.list_sessions())
# print(mgr.stop_session("abc123"))
