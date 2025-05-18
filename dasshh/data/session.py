from datetime import datetime
from typing import List

from pydantic import BaseModel
from litellm.types.utils import Message
from sqlalchemy.orm import noload

from dasshh.data.client import DBClient
from dasshh.data.models import StorageSession, StorageEvent


class Session(BaseModel):
    """Dasshh session."""

    id: str
    detail: str
    created_at: datetime
    updated_at: datetime
    events: List[Message]


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
            return Session(
                id=session.id,
                detail=session.detail,
                created_at=session.created_at,
                updated_at=session.updated_at,
                events=[],
            )

    def get_session(self, *, session_id: str) -> Session | None:
        """Get a session by its ID."""
        with self.db_client.get_db() as db:
            session: StorageSession | None = db.get(StorageSession, session_id)

            if session is None:
                return None

            # Ensure events are loaded before session closes
            events = list(session.events)
            return Session(
                id=session.id,
                detail=session.detail,
                created_at=session.created_at,
                updated_at=session.updated_at,
                events=[self._convert_to_completion_message(event) for event in events],
            )

    def get_events(self, *, session_id: str) -> list[Message]:
        """Get all events for a session."""
        with self.db_client.get_db() as db:
            events = db.query(StorageEvent).filter(StorageEvent.session_id == session_id).all()
            return [self._convert_to_completion_message(event) for event in events]

    def get_recent_session(self) -> Session | None:
        """Get the most recent session."""
        with self.db_client.get_db() as db:
            session: StorageSession | None = (
                db.query(StorageSession).order_by(StorageSession.updated_at.desc()).first()
            )
            if not session:
                return None
                
            # Ensure events are loaded before session closes
            events = list(session.events)
            return Session(
                id=session.id,
                detail=session.detail,
                created_at=session.created_at,
                updated_at=session.updated_at,
                events=[self._convert_to_completion_message(event) for event in events],
            )

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

    def list_sessions(self, include_events: bool = False) -> list[Session]:
        """List all sessions."""
        with self.db_client.get_db() as db:
            if include_events:
                sessions = db.query(StorageSession).all()
            else:
                sessions = db.query(StorageSession).options(noload(StorageSession.events)).all()
            return [
                Session(
                    id=session.id,
                    detail=session.detail,
                    created_at=session.created_at,
                    updated_at=session.updated_at,
                    events=[
                        self._convert_to_completion_message(event)
                        for event in session.events
                    ] if include_events else [],
                ) for session in sessions
            ]

    def delete_session(self, *, session_id: str) -> None:
        """Delete a session by its ID."""
        with self.db_client.get_db() as db:
            session = db.get(StorageSession, session_id)

            if session is None:
                return

            db.delete(session)
            db.commit()

    def add_event(
        self,
        *,
        invocation_id: str,
        session_id: str,
        content: dict,
    ) -> None:
        """Append an event to a session."""
        event = StorageEvent(
            invocation_id=invocation_id,
            session_id=session_id,
            content=content,
        )
        with self.db_client.get_db() as db:
            db.add(event)
            db.commit()
            db.refresh(event)

    def _convert_to_completion_message(self, event: StorageEvent) -> Message:
        """Convert a storage event to a message"""
        return Message(**event.content)
