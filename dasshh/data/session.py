import json
from datetime import datetime

from dasshh.data.client import DBClient
from dasshh.data.models import StorageSession, StorageEvent
from dasshh.core.dto import Session, Message, ToolCall, ToolCallResult


class SessionService:
    """Dasshh database session service."""

    def __init__(self, db_client: DBClient):
        self.db_client = db_client

    def new_session(
        self,
        detail: str = "New Session",
    ) -> Session:
        """Create a new session."""
        session = StorageSession(detail=detail)
        with self.db_client.get_db() as db:
            db.add(session)
            db.commit()
            db.refresh(session)

        return self._convert_to_session(session, include_events=False)

    def get_session(self, *, session_id: str) -> Session | None:
        """Get a session by its ID."""
        with self.db_client.get_db() as db:
            session: StorageSession | None = db.get(StorageSession, session_id)

            if session is None:
                return None

            return self._convert_to_session(session)

    def get_recent_session(self) -> Session | None:
        """Get the most recent session."""
        with self.db_client.get_db() as db:
            session: StorageSession | None = (
                db.query(StorageSession).order_by(StorageSession.updated_at.desc()).first()
            )
            return self._convert_to_session(session) if session else None

    def update_session(
        self,
        *,
        session_id: str,
        detail: str,
    ) -> None:
        """Update a session."""
        with self.db_client.get_db() as db:
            session = db.get(StorageSession, session_id)
            session.detail = detail
            session.updated_at = datetime.now()
            db.commit()

    def list_sessions(self) -> list[Session]:
        """List all sessions."""
        with self.db_client.get_db() as db:
            sessions = db.query(StorageSession).all()
            return [
                self._convert_to_session(session, include_events=False)
                for session in sessions
            ]

    def delete_session(self, *, session_id: str) -> None:
        """Delete a session by its ID."""
        with self.db_client.get_db() as db:
            session = db.get(StorageSession, session_id)

            if session is None:
                return

            db.delete(session)
            db.commit()

    def append_event(
        self,
        *,
        invocation_id: str,
        session_id: str,
        content: dict,
        error: str | None = None,
    ) -> None:
        """Append an event to a session."""
        event = StorageEvent(
            invocation_id=invocation_id,
            session_id=session_id,
            content=json.dumps(content),
            error=error,
        )
        with self.db_client.get_db() as db:
            db.add(event)
            db.commit()
            db.refresh(event)

    def _convert_to_session(
        self,
        session: StorageSession,
        include_events: bool = True,
    ) -> Session:
        """Convert a storage session to a session."""
        session_dto = Session(
            id=session.id,
            detail=session.detail,
            last_updated_at=session.updated_at,
        )

        if include_events:
            session_dto.messages = []
            session_dto.tools = []
            for event in session.events:
                if event.is_tool_call:
                    session_dto.tools.append(self._convert_to_tool(event))
                else:
                    session_dto.messages.append(self._convert_to_message(event))
        return session_dto

    def _convert_to_message(self, event: StorageEvent) -> Message:
        """Convert a storage event to a message"""
        content = json.loads(event.content)
        # TODO
        pass

    def _convert_to_tool(self, event: StorageEvent) -> ToolCall | ToolCallResult:
        """Convert a storage event to a message"""
        content = json.loads(event.content)
        # TODO
        pass
