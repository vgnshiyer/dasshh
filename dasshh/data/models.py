import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from dasshh.data.client import Base


class StorageSession(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    detail = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))

    events = relationship("StorageEvent", back_populates="session")


class StorageEvent(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    invocation_id = Column(String)
    session_id = Column(String, ForeignKey("sessions.id"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    content = Column(JSON)

    session = relationship("StorageSession", back_populates="events")
