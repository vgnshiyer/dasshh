"""
Tests for the session service.
"""
import uuid

from dasshh.data.models import StorageSession


def test_new_session(test_session_service):
    """Test creating a new session."""
    session = test_session_service.new_session(detail="Test Session")
    assert session is not None
    assert isinstance(session, StorageSession)
    assert session.detail == "Test Session"


def test_get_session(test_session_service):
    """Test getting a session by ID."""
    session = test_session_service.new_session(detail="Test Session")
    retrieved_session = test_session_service.get_session(session_id=session.id)
    assert retrieved_session is not None
    assert retrieved_session.id == session.id
    assert retrieved_session.detail == "Test Session"


def test_get_nonexistent_session(test_session_service):
    """Test getting a session that doesn't exist."""
    session = test_session_service.get_session(session_id=str(uuid.uuid4()))
    assert session is None


def test_update_session(test_session_service):
    """Test updating a session."""
    session = test_session_service.new_session(detail="Test Session")

    test_session_service.update_session(
        session_id=session.id,
        detail="Updated Session",
    )

    updated_session = test_session_service.get_session(session_id=session.id)

    assert updated_session is not None
    assert updated_session.detail == "Updated Session"


def test_list_sessions(test_session_service):
    """Test listing sessions."""
    session1 = test_session_service.new_session(detail="Test Session 1")
    session2 = test_session_service.new_session(detail="Test Session 2")

    sessions = test_session_service.list_sessions()
    assert len(sessions) >= 2
    assert any(s.id == session1.id for s in sessions)
    assert any(s.id == session2.id for s in sessions)


def test_list_sessions_with_include_events(test_session_service):
    """Test listing sessions with include_events parameter."""
    session = test_session_service.new_session(detail="Test Session")

    invocation_id = str(uuid.uuid4())
    content = {"message": "Test event"}
    test_session_service.add_event(
        invocation_id=invocation_id,
        session_id=session.id,
        content=content,
    )

    sessions_with_events = test_session_service.list_sessions(include_events=True)

    assert len(sessions_with_events) > 0
    assert any(s.id == session.id for s in sessions_with_events)

    sessions_without_events = test_session_service.list_sessions(include_events=False)
    assert len(sessions_without_events) > 0


def test_delete_session(test_session_service):
    """Test deleting a session."""
    # Create a new session
    session = test_session_service.new_session(detail="Test Session")

    test_session_service.delete_session(session_id=session.id)

    deleted_session = test_session_service.get_session(session_id=session.id)

    assert deleted_session is None


def test_delete_nonexistent_session(test_session_service):
    """Test deleting a session that doesn't exist."""
    nonexistent_id = str(uuid.uuid4())

    test_session_service.delete_session(session_id=nonexistent_id)


def test_get_recent_session(test_session_service):
    """Test getting the most recent session."""
    test_session_service.new_session(detail="Test Session 1")
    session2 = test_session_service.new_session(detail="Test Session 2")

    recent_session = test_session_service.get_recent_session()

    assert recent_session is not None
    assert recent_session.id == session2.id


def test_add_event(test_session_service):
    """Test adding an event to a session."""
    session = test_session_service.new_session(detail="Test Session")

    invocation_id = str(uuid.uuid4())
    content = {"message": "Test event"}
    test_session_service.add_event(
        invocation_id=invocation_id,
        session_id=session.id,
        content=content,
    )

    events = test_session_service.get_events(session_id=session.id)

    assert len(events) == 1
    assert events[0].invocation_id == invocation_id
    assert events[0].session_id == session.id
    assert events[0].content == content
