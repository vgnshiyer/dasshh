import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, relationship, JSON, Boolean

from dasshh.data.client import Base


class StorageSession(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    detail = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    events = relationship("StorageEvent", back_populates="session")


class StorageEvent(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    invocation_id = Column(String)
    session_id = Column(String, ForeignKey("sessions.id"))
    timestamp = Column(DateTime)
    content = Column(JSON)
    error = Column(String)
    is_tool_call = Column(Boolean)

    session = relationship("StorageSession", back_populates="events")
