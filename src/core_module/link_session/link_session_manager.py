import uuid
from typing import Dict

from src.core_module.link_session.link_session import LinkSession

class LinkSessionManager:
    """
    Manages multiple LinkSession instances.
    Uses class methods and maintains a default session with ID '0'.
    """
    sessions: Dict[str, LinkSession] = {}

    @classmethod
    def get_session(cls, session_id: str = "0") -> LinkSession: 
        """
        Retrieves an existing session or creates a new one if it doesn't exist.
        """
        if session_id not in cls.sessions:
            if session_id == "0":
                cls.sessions[session_id] = LinkSession()
                cls.sessions[session_id].session_id = "0"
            else:
                cls.sessions[session_id] = LinkSession()
        return cls.sessions[session_id]

    @classmethod
    def remove_session(cls, session_id: str):
        """
        Removes a session by its ID.
        """
        if session_id in cls.sessions and session_id != "0":
            del cls.sessions[session_id]

    @classmethod
    def list_sessions(cls) -> list:
        """
        Lists all active session IDs.
        """
        return list(cls.sessions.keys())

    @classmethod
    def clear_sessions(cls):
        """
        Clears all sessions except the default one.
        """
        cls.sessions = {"0": cls.get_session("0")}
