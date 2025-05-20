"""
Tests for database models.
"""
import uuid
from datetime import datetime

from dasshh.data.models import StorageSession, StorageEvent


def test_storage_session_model():
    """Test the StorageSession model structure."""
    session_id = str(uuid.uuid4())
    now = datetime.now()
    session = StorageSession(
        id=session_id,
        detail="Test Session",
        created_at=now,
        updated_at=now
    )

    assert session.id == session_id
    assert session.detail == "Test Session"
    assert session.created_at == now
    assert session.updated_at == now

    assert hasattr(session, "events")


def test_storage_event_model():
    """Test the StorageEvent model structure."""
    event_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    invocation_id = str(uuid.uuid4())
    now = datetime.now()
    content = {"message": "Test event"}

    event = StorageEvent(
        id=event_id,
        invocation_id=invocation_id,
        session_id=session_id,
        created_at=now,
        content=content,
    )

    assert event.id == event_id
    assert event.invocation_id == invocation_id
    assert event.session_id == session_id
    assert event.created_at == now
    assert event.content == content
