from datetime import datetime, timezone

from sqlalchemy.orm import noload

from dasshh.data.client import DBClient
from dasshh.data.models import StorageSession, StorageEvent


class SessionService:
    """Dasshh database session service."""

    def __init__(self, db_client: DBClient):
        self.db_client = db_client

    def new_session(
        self,
        detail: str = "New Session",
    ) -> StorageSession:
        """Create a new session."""
        session = StorageSession(detail=detail)
        with self.db_client.get_db() as db:
            db.add(session)
            db.commit()
            db.refresh(session)
            return session

    def get_session(self, *, session_id: str) -> StorageSession | None:
        """Get a session by its ID."""
        with self.db_client.get_db() as db:
            session: StorageSession | None = db.get(StorageSession, session_id)
            if session is None:
                return None
            return session

    def get_events(self, *, session_id: str) -> list[StorageEvent]:
        """Get all events for a session."""
        with self.db_client.get_db() as db:
            events = (
                db.query(StorageEvent)
                .filter(StorageEvent.session_id == session_id)
                .all()
            )
            return events

    def get_recent_session(self) -> StorageSession | None:
        """Get the most recent session."""
        with self.db_client.get_db() as db:
            session: StorageSession | None = (
                db.query(StorageSession)
                .order_by(StorageSession.updated_at.desc())
                .first()
            )
            if not session:
                return None
            return session

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
            session.updated_at = datetime.now(timezone.utc)
            db.commit()

    def list_sessions(self, include_events: bool = False) -> list[StorageSession]:
        """List all sessions."""
        with self.db_client.get_db() as db:
            if include_events:
                sessions = db.query(StorageSession).all()
            else:
                sessions = (
                    db.query(StorageSession)
                    .options(noload(StorageSession.events))
                    .all()
                )
            return sessions

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
